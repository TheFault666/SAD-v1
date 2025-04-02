import json
import socket
import platform
import subprocess
import os
import winreg
import wmi
import requests

def get_pc_specs():
    specs = {}
    c = wmi.WMI()
    
    # Get system details
    specs["Computer Name"] = socket.gethostname()
    specs["OS"] = platform.system()
    specs["OS Version"] = platform.version()
    specs["OS Release"] = platform.release()
    specs["OS Architecture"] = platform.architecture()[0]
    specs["OS Licensed"] = check_os_license()
    specs["Processor"] = get_processor_info()
    specs["RAM"] = get_memory_info()
    specs["GPU"] = get_gpu_info()
    
    # Get IP & MAC addresses
    specs["Network"] = get_network_details()
    
    return specs

def get_processor_info():
    try:
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            return f"{cpu.Name} ({cpu.NumberOfCores} Cores, {cpu.NumberOfLogicalProcessors} Threads)"
    except:
        return "Unknown"

def get_memory_info():
    try:
        c = wmi.WMI()
        for mem in c.Win32_ComputerSystem():
            return f"{round(int(mem.TotalPhysicalMemory) / (1024**3), 2)} GB RAM"
    except:
        return "Unknown"

def get_gpu_info():
    try:
        c = wmi.WMI()
        gpus = [gpu.Name for gpu in c.Win32_VideoController()]
        return gpus if gpus else "No GPU detected"
    except:
        return "Unknown"

def get_network_details():
    network_info = {}
    for interface in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True):
        network_info[interface.Description] = {
            "MAC Address": interface.MACAddress,
            "IP Address": interface.IPAddress[0] if interface.IPAddress else "Unknown"
        }
    return network_info

def check_os_license():
    try:
        output = subprocess.check_output("cscript //NoLogo C:\\Windows\\System32\\slmgr.vbs /dli", shell=True, text=True)
        return "Licensed" if "License Status: Licensed" in output else "Pirated"
    except:
        return "Unknown"

def get_user_info():
    user_info = {}
    user_info["Current User"] = os.getlogin()
    try:
        output = subprocess.check_output("whoami /groups", shell=True, text=True)
        user_info["Admin Access"] = "Yes" if "Administrators" in output else "No"
    except:
        user_info["Admin Access"] = "Unknown"
    return user_info

def check_antivirus():
    av_info = {"Antivirus Installed": "No"}
    
    try:
        c = wmi.WMI(namespace="root\\SecurityCenter2")
        av_products = c.ExecQuery("SELECT * FROM AntivirusProduct")

        if av_products:
            av_list = []
            for av in av_products:
                av_name = av.displayName
                av_list.append({
                    "Name": av_name,
                    "Update Available": check_av_update(av_name)
                })
            av_info["Antivirus Installed"] = "Yes"
            av_info["Antiviruses"] = av_list
    except Exception as e:
        av_info["Error"] = str(e)
    
    return av_info

def check_av_update(av_name):
    try:
        response = requests.get(f"https://api.antivirus-updates.com/check?name={av_name}")
        return "Yes" if response.json().get("update_available", False) else "No"
    except:
        return "Unknown"

def is_bitlocker_enabled():
    try:
        output = subprocess.check_output("manage-bde -status C:", shell=True, text=True)
        return "Enabled" if "Protection On" in output else "Disabled"
    except:
        return "Unknown"

def is_usb_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "Start")
        return "Disabled" if value == 4 else "Enabled"
    except:
        return "Unknown"

def is_rdp_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Control\\Terminal Server", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "fDenyTSConnections")
        return "Disabled" if value == 1 else "Enabled"
    except:
        return "Unknown"

def security_audit():
    audit_result = {
        "PC Specs": get_pc_specs(),
        "User Account": get_user_info(),
        "Antivirus": check_antivirus(),
        "BitLocker": is_bitlocker_enabled(),
        "USB Access": is_usb_disabled(),
        "RDP Status": is_rdp_disabled()
    }
    
    print(json.dumps(audit_result, indent=4))

if __name__ == "__main__":
    security_audit()
