# import json
# import socket
# import platform
# import subprocess
# import os
# import winreg
# import wmi
# import requests
# import re

# def get_pc_specs():
#     specs = {}
#     c = wmi.WMI()
    
#     # Get system details
#     specs["Computer Name"] = socket.gethostname()
#     specs["OS"] = platform.system()
#     specs["OS Version"] = platform.version()
#     specs["OS Release"] = platform.release()
#     specs["OS Architecture"] = platform.architecture()[0]
#     specs["OS Licensed"] = check_os_license()
#     specs["Processor"] = get_processor_info()
#     specs["RAM"] = get_memory_info()
#     specs["GPU"] = get_gpu_info()
    
#     # Get IP & MAC addresses
#     specs["Network"] = get_network_details()
    
#     return specs

# def get_processor_info():
#     try:
#         c = wmi.WMI()
#         for cpu in c.Win32_Processor():
#             return f"{cpu.Name} ({cpu.NumberOfCores} Cores, {cpu.NumberOfLogicalProcessors} Threads)"
#     except:
#         return "Unknown"

# def get_memory_info():
#     try:
#         c = wmi.WMI()
#         for mem in c.Win32_ComputerSystem():
#             return f"{round(int(mem.TotalPhysicalMemory) / (1024**3), 2)} GB RAM"
#     except:
#         return "Unknown"

# def get_gpu_info():
#     try:
#         c = wmi.WMI()
#         gpus = [gpu.Name for gpu in c.Win32_VideoController()]
#         return gpus if gpus else "No GPU detected"
#     except:
#         return "Unknown"

# def get_network_details():
#     network_info = {}
#     count = 1  # Counter for numbering adapters
    
#     for interface in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True):
#         adapter_name = interface.Description
#         mac_address = interface.MACAddress if interface.MACAddress else "None"
#         ip_address = interface.IPAddress[0] if interface.IPAddress else "Unknown"

#         network_info[f"Adapter {count}"] = {
#             "Network Adapter": adapter_name,
#             "MAC Address": mac_address,
#             "IP Address": ip_address
#         }
#         count += 1  # Increment adapter numbering
    
#     return network_info

# def check_os_license():
#     try:
#         output = subprocess.check_output("cscript //NoLogo C:\\Windows\\System32\\slmgr.vbs /dli", shell=True, text=True)
#         return "Licensed" if "License Status: Licensed" in output else "Pirated"
#     except:
#         return "Unknown"

# def get_user_info():
#     user_info = {}
#     user_info["Current User"] = os.getlogin()
#     try:
#         output = subprocess.check_output("whoami /groups", shell=True, text=True)
#         user_info["Admin Access"] = "Yes" if "Administrators" in output else "No"
#     except:
#         user_info["Admin Access"] = "Unknown"
#     return user_info

# def check_antivirus():
#     av_info = {"Antivirus Installed": "No"}
    
#     try:
#         c = wmi.WMI(namespace="root\\SecurityCenter2")
#         av_products = c.ExecQuery("SELECT * FROM AntivirusProduct")

#         if av_products:
#             av_list = []
#             for av in av_products:
#                 av_name = av.displayName
#                 av_list.append({
#                     "Name": av_name,
#                     "Update Available": check_av_update(av_name)
#                 })
#             av_info["Antivirus Installed"] = "Yes"
#             av_info["Antiviruses"] = av_list
#     except Exception as e:
#         av_info["Error"] = str(e)
    
#     return av_info

# def check_av_update(av_name):
#     try:
#         response = requests.get(f"https://api.antivirus-updates.com/check?name={av_name}")
#         return "Yes" if response.json().get("update_available", False) else "No"
#     except:
#         return "Unknown"

# def is_bitlocker_enabled():
#     try:
#         output = subprocess.check_output("manage-bde -status C:", shell=True, text=True)
#         return "Enabled" if "Protection On" in output else "Disabled"
#     except:
#         return "OS does not support Bitlocker"

# def is_usb_disabled():
#     try:
#         key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, winreg.KEY_READ)
#         value, _ = winreg.QueryValueEx(key, "Start")
#         return "Disabled" if value == 4 else "Enabled"
#     except:
#         return "Unknown"

# def is_rdp_disabled():
#     try:
#         key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Control\\Terminal Server", 0, winreg.KEY_READ)
#         value, _ = winreg.QueryValueEx(key, "fDenyTSConnections")
#         return "Disabled" if value == 1 else "Enabled"
#     except:
#         return "Unknown"

# def check_secure_boot():
#     cmd = "powershell Confirm-SecureBootUEFI"
#     result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
#     if "True" in result.stdout:
#         return "Secure Boot is enabled."
#     else:
#         return "Secure Boot is not enabled."

# def check_outdated_apps():
#     cmd = "winget upgrade"
#     result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    
#     outdated_apps = []
    
#     if result.stdout:
#         lines = result.stdout.split("\n")
#         for line in lines:
#             if not line.strip() or re.match(r"[-|\\]+", line.strip()):
#                 continue
#             if "Name" in line and "Version" in line and "Available" in line:
#                 continue
#             if "upgrade" in line.lower():
#                 continue
            
#             parts = re.split(r'\s{2,}', line.strip())  # Split by multiple spaces
#             if len(parts) >= 3:
#                 app_name = parts[0]
#                 current_version = parts[1]
#                 available_version = parts[2]
#                 outdated_apps.append(f"{app_name} {current_version} → {available_version}")
    
#     return outdated_apps if outdated_apps else ["No outdated applications detected."]

# def security_audit():
#     audit_result = {
#         "PC Specs": get_pc_specs(),
#         "User Account": get_user_info(),
#         "Antivirus": check_antivirus(),
#         "BitLocker": is_bitlocker_enabled(),
#         "USB Access": is_usb_disabled(),
#         "RDP Status": is_rdp_disabled(),
#         "Secure Boot": check_secure_boot(),
#         "Outdated Applications": check_outdated_apps()
#     }
    
#     print(json.dumps(audit_result, indent=4))

# if __name__ == "__main__":
#     security_audit()
# import json
# import socket
# import platform
# import subprocess
# import os
# import winreg
# import wmi
# import requests
# import re

# def get_pc_specs():
#     specs = {}
#     c = wmi.WMI()

#     # Get system details
#     specs["Computer Name"] = socket.gethostname()
#     specs["OS"] = platform.system()
#     specs["OS Version"] = platform.version()
#     specs["OS Release"] = platform.release()
#     specs["OS Architecture"] = platform.architecture()[0]
#     specs["OS Licensed"] = check_os_license()
#     specs["Processor"] = get_processor_info()
#     specs["RAM"] = get_memory_info()
#     specs["GPU"] = get_gpu_info()
    
#     # Get IP & MAC addresses
#     specs["Network"] = get_network_details()
    
#     return specs

# def get_processor_info():
#     try:
#         c = wmi.WMI()
#         for cpu in c.Win32_Processor():
#             return f"{cpu.Name} ({cpu.NumberOfCores} Cores, {cpu.NumberOfLogicalProcessors} Threads)"
#     except:
#         return "Unknown"

# def get_memory_info():
#     try:
#         c = wmi.WMI()
#         for mem in c.Win32_ComputerSystem():
#             return f"{round(int(mem.TotalPhysicalMemory) / (1024**3), 2)} GB RAM"
#     except:
#         return "Unknown"

# def get_gpu_info():
#     try:
#         c = wmi.WMI()
#         gpus = [gpu.Name for gpu in c.Win32_VideoController()]
#         return gpus if gpus else "No GPU detected"
#     except:
#         return "Unknown"

# def get_network_details():
#     network_info = {}
#     count = 1  
#     for interface in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True):
#         adapter_name = interface.Description
#         mac_address = interface.MACAddress if interface.MACAddress else "None"
#         ip_address = interface.IPAddress[0] if interface.IPAddress else "Unknown"

#         network_info[f"Adapter {count}"] = {
#             "Network Adapter": adapter_name,
#             "MAC Address": mac_address,
#             "IP Address": ip_address
#         }
#         count += 1  
    
#     return network_info

# def check_os_license():
#     try:
#         output = subprocess.check_output("cscript //NoLogo C:\\Windows\\System32\\slmgr.vbs /dli", shell=True, text=True)
#         return "Licensed" if "License Status: Licensed" in output else "Pirated"
#     except:
#         return "Unknown"

# def get_user_info():
#     user_info = {}
#     user_info["Current User"] = os.getlogin()
#     try:
#         output = subprocess.check_output("whoami /groups", shell=True, text=True)
#         user_info["Admin Access"] = "Yes" if "Administrators" in output else "No"
#     except:
#         user_info["Admin Access"] = "Unknown"
#     return user_info

# def check_antivirus():
#     av_info = {"Antivirus Installed": "No"}
#     try:
#         c = wmi.WMI(namespace="root\\SecurityCenter2")
#         av_products = c.ExecQuery("SELECT * FROM AntivirusProduct")

#         if av_products:
#             av_list = []
#             for av in av_products:
#                 av_name = av.displayName
#                 av_list.append({"Name": av_name})
#             av_info["Antivirus Installed"] = "Yes"
#             av_info["Antiviruses"] = av_list
#     except:
#         av_info["Error"] = "Unable to retrieve antivirus info"
    
#     return av_info

# def is_bitlocker_enabled():
#     try:
#         output = subprocess.check_output("manage-bde -status C:", shell=True, text=True)
#         return "Enabled" if "Protection On" in output else "Disabled"
#     except:
#         return "OS does not support Bitlocker"

# def is_usb_disabled():
#     try:
#         key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, winreg.KEY_READ)
#         value, _ = winreg.QueryValueEx(key, "Start")
#         return "Disabled" if value == 4 else "Enabled"
#     except:
#         return "Unknown"

# def is_rdp_disabled():
#     try:
#         key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Control\\Terminal Server", 0, winreg.KEY_READ)
#         value, _ = winreg.QueryValueEx(key, "fDenyTSConnections")
#         return "Disabled" if value == 1 else "Enabled"
#     except:
#         return "Unknown"

# def check_secure_boot():
#     cmd = "powershell Confirm-SecureBootUEFI"
#     result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
#     if "True" in result.stdout:
#         return "Secure Boot is enabled."
#     else:
#         return "Secure Boot is not enabled."

# def get_installed_software():
#     """Fetch a list of installed software excluding Microsoft applications."""
#     try:
#         cmd = [
#             "powershell", "-Command",
#             "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, "
#             "HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | "
#             "Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | "
#             "Where-Object { $_.DisplayName -and ($_.Publisher -notmatch 'Microsoft|Microsoft Corporation') } | "
#             "ForEach-Object { $_.InstallDate = if ($_.InstallDate -match '^\d{8}$') "
#             "{ [datetime]::ParseExact($_.InstallDate, 'yyyyMMdd', $null).ToString('dd/MM/yyyy') } "
#             "else { 'Unknown' } $_ } | ConvertTo-Json -Depth 3"
#         ]
        
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
#         if result.returncode != 0:
#             return {"Error": f"PowerShell execution failed: {result.stderr}"}
        
#         try:
#             software_list = json.loads(result.stdout)
#             return software_list if isinstance(software_list, list) else [software_list]
#         except json.JSONDecodeError:
#             return {"Error": "Failed to parse PowerShell output as JSON"}

#     except Exception as e:
#         return {"Error": str(e)}

# def check_outdated_apps():
#     cmd = "winget upgrade"
#     result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    
#     outdated_apps = []
    
#     if result.stdout:
#         lines = result.stdout.split("\n")
#         for line in lines:
#             if not line.strip() or re.match(r"[-|\\]+", line.strip()):
#                 continue
#             if "Name" in line and "Version" in line and "Available" in line:
#                 continue
#             if "upgrade" in line.lower():
#                 continue
            
#             parts = re.split(r'\s{2,}', line.strip())  # Split by multiple spaces
#             if len(parts) >= 3:
#                 app_name = parts[0]
#                 current_version = parts[1]
#                 available_version = parts[2]
#                 outdated_apps.append(f"{app_name} {current_version} → {available_version}")
    
#     return outdated_apps if outdated_apps else ["No outdated applications detected."]

# def security_audit():
#     audit_result = {
#         "PC Specs": get_pc_specs(),
#         "User Account": get_user_info(),
#         "Antivirus": check_antivirus(),
#         "BitLocker": is_bitlocker_enabled(),
#         "USB Access": is_usb_disabled(),
#         "RDP Status": is_rdp_disabled(),
#         "Secure Boot": check_secure_boot(),
#         "Installed Software": get_installed_software(),
#         "Outdated Applications": check_outdated_apps()
#     }
    
#     print(json.dumps(audit_result, indent=4))

# if __name__ == "__main__":
#     security_audit()

import json
import socket
import platform
import subprocess
import os
import winreg
import wmi
import re
from datetime import datetime

def run_powershell(cmd):
    """Runs a PowerShell command and returns output."""
    try:
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", cmd], capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def get_pc_specs():
    specs = {}
    c = wmi.WMI()

    specs["Computer Name"] = socket.gethostname()
    specs["OS"] = platform.system()
    specs["OS Version"] = platform.version()
    specs["OS Release"] = platform.release()
    specs["OS Architecture"] = platform.architecture()[0]
    specs["OS Licensed"] = check_os_license()
    specs["Processor"] = get_processor_info()
    specs["RAM"] = get_memory_info()
    specs["GPU"] = get_gpu_info()
    specs["Network"] = get_network_details()
    
    return specs

def get_processor_info():
    try:
        c = wmi.WMI()
        cpu = c.Win32_Processor()[0]
        return f"{cpu.Name} ({cpu.NumberOfCores} Cores, {cpu.NumberOfLogicalProcessors} Threads)"
    except:
        return "Unknown"

def get_memory_info():
    try:
        c = wmi.WMI()
        mem = c.Win32_ComputerSystem()[0]
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
    for count, interface in enumerate(wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True), start=1):
        network_info[f"Adapter {count}"] = {
            "Network Adapter": interface.Description,
            "MAC Address": interface.MACAddress or "None",
            "IP Address": interface.IPAddress[0] if interface.IPAddress else "Unknown"
        }
    return network_info

def check_os_license():
    output = run_powershell("cscript //NoLogo C:\\Windows\\System32\\slmgr.vbs /dli")
    return "Licensed" if "License Status: Licensed" in output else "Pirated"

def get_user_info():
    user_info = {"Current User": os.getlogin()}
    user_info["Admin Access"] = "Yes" if "Administrators" in run_powershell("whoami /groups") else "No"
    return user_info

def get_windows_defender_status():
    output = run_powershell("Get-MpComputerStatus | ConvertTo-Json")
    try:
        defender_data = json.loads(output)
        return {
            "Status": "Enabled" if defender_data.get("AntivirusEnabled", False) else "Disabled",
            "Version": defender_data.get("AntivirusSignatureVersion", "Unknown"),
            "Last Update": defender_data.get("SignatureLastUpdated", "Unknown"),
            "Real-Time Protection": "Enabled" if defender_data.get("RealTimeProtectionEnabled", False) else "Disabled"
        }
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from PowerShell"}

def get_installed_antivirus():
    antivirus_list = []
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, path)

        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(reg, path + "\\" + subkey_name)

            try:
                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]

                av_keywords = ["defender", "kaspersky", "mcafee", "avast", "bitdefender", "norton", "eset", "sophos", "trend micro"]
                if any(av in name.lower() for av in av_keywords):
                    antivirus_list.append({"Name": name, "Version": version, "Status": "Unknown", "Real-Time Protection": "Unknown"})
            
            except FileNotFoundError:
                pass

    except Exception as e:
        return {"error": str(e)}

    return antivirus_list

def get_third_party_av_status():
    output = run_powershell("Get-CimInstance -Namespace root\\SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName, productState | ConvertTo-Json")
    
    try:
        av_data = json.loads(output)
        av_list = av_data if isinstance(av_data, list) else [av_data]

        return [{
            "Name": av.get("displayName", "Unknown"),
            "Status": "Enabled" if str(av.get("productState", "0000")).startswith("4") else "Disabled",
            "Real-Time Protection": "Enabled" if str(av.get("productState", "0000"))[1] == "1" else "Disabled"
        } for av in av_list]

    except json.JSONDecodeError:
        return []

def check_antivirus():
    installed_av = get_installed_antivirus()
    third_party_status = get_third_party_av_status()

    for av in installed_av:
        for status in third_party_status:
            if av["Name"].lower() in status["Name"].lower():
                av["Status"], av["Real-Time Protection"] = status["Status"], status["Real-Time Protection"]

    return {"Third-Party Antivirus": installed_av or "None detected", "Windows Defender": get_windows_defender_status()}

def is_bitlocker_enabled():
    return "Enabled" if "Protection On" in run_powershell("manage-bde -status C:") else "Disabled"

def is_usb_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, winreg.KEY_READ)
        return "Disabled" if winreg.QueryValueEx(key, "Start")[0] == 4 else "Enabled"
    except:
        return "Unknown"

def is_rdp_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Control\\Terminal Server", 0, winreg.KEY_READ)
        return "Disabled" if winreg.QueryValueEx(key, "fDenyTSConnections")[0] == 1 else "Enabled"
    except:
        return "Unknown"

def check_secure_boot():
    return "Secure Boot is enabled." if "True" in run_powershell("Confirm-SecureBootUEFI") else "Secure Boot is not enabled."

import json

def get_installed_software():
    output = run_powershell(
        "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, "
        "HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | "
        "Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | ConvertTo-Json -Depth 3"
    )
    
    try:
        software_list = json.loads(output)
        
        # Ensure the result is always a list
        software_list = software_list if isinstance(software_list, list) else [software_list]
        
        # Function to extract the first word of a given string
        def get_first_word(text):
            return text.split()[0] if text and isinstance(text, str) else "Unknown"

        # Filter out Microsoft built-in software and format names
        filtered_software = [
            {
                "DisplayName": get_first_word(software.get("DisplayName", "Unknown")),
                "DisplayVersion": software.get("DisplayVersion", "-"),
                "Publisher": get_first_word(software.get("Publisher", "Unknown")),
                "InstallDate": software.get("InstallDate", "-")
            }
            for software in software_list
            if software.get("Publisher") and "Microsoft" not in software["Publisher"]  # Exclude Microsoft Publisher
            and software.get("DisplayName") and "Microsoft" not in software["DisplayName"]  # Exclude built-in apps
        ]

        return filtered_software

    except json.JSONDecodeError:
        return {"Error": "Failed to parse PowerShell output as JSON"}


def check_outdated_apps():
    return [line for line in run_powershell("winget upgrade").split("\n") if line.strip() and not re.match(r"[-|\\]+", line.strip())]

def security_audit():
    print(json.dumps({
        "PC Specs": get_pc_specs(),
        "User Account": get_user_info(),
        "Antivirus": check_antivirus(),
        "BitLocker": is_bitlocker_enabled(),
        "USB Access": is_usb_disabled(),
        "RDP Status": is_rdp_disabled(),
        "Secure Boot": check_secure_boot(),
        "Installed Software": get_installed_software(),
        "Outdated Applications": check_outdated_apps()
    }, indent=4))

if __name__ == "__main__":
    security_audit()
