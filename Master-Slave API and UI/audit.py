import subprocess
import winreg
import os
import platform
import json

def run_powershell(command):
    """Executes a PowerShell command and returns its output."""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None
# Function to check Windows OS version
def check_os_version():
    return {"system": platform.system(), "release": platform.release(), "version": platform.version()}

# Function to check if OS auto-update is enabled
def check_auto_update():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU")
        value, _ = winreg.QueryValueEx(key, "NoAutoUpdate")
        return "Disabled" if value == 1 else "Enabled"
    except FileNotFoundError:
        return "Not Found (Assumed Enabled)"

# Function to check antivirus installation and status
def check_antivirus():
    cmd = "powershell Get-CimInstance -Namespace root\\SecurityCenter2 -ClassName AntivirusProduct"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    
    # Convert multi-line output into a single string
    antivirus_output = result.stdout.strip()
    return antivirus_output.replace("\n", " | ") if antivirus_output else "No antivirus detected."



# Function to check if BitLocker is enabled
def check_bitlocker():
    cmd = "powershell Get-BitLockerVolume | Select-Object -Property VolumeStatus"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return "Enabled" if "FullyEncrypted" in result.stdout else "Not Enabled"

# Function to check for pirated software
# def check_pirated_software():
#     pirated_keywords = ["crack", "keygen", "patch", "pirate"]
#     suspect_files = []
#     for root, _, files in os.walk("C:\\"):
#         for file in files:
#             if any(keyword in file.lower() for keyword in pirated_keywords):
#                 suspect_files.append(os.path.join(root, file))
#     return suspect_files if suspect_files else "No pirated software detected."

# Function to check if USB storage devices are authorized
def check_usb_storage():
    cmd = "powershell Get-Service -Name USBSTOR"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return "Enabled" if "Running" in result.stdout else "Disabled"

# Function to check firewall status
def check_firewall():
    cmd = "powershell Get-NetFirewallProfile -Profile Domain,Public,Private | Select-Object -Property Enabled"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return "Active" if "True" in result.stdout else "Inactive"

# Function to check for BIOS password (Requires Manual Check)
def check_bios_password():
    return "Manual check required: Verify BIOS password in BIOS setup."

# Function to check if Secure Boot is enabled
def check_secure_boot():
    cmd = "powershell Confirm-SecureBootUEFI"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return "Enabled" if "True" in result.stdout else "Not Enabled"

# Generate JSON Report
# def generate_report():
#     report = {
#         "OS_Version": check_os_version(),
#         "Auto_Update": check_auto_update(),
#         "Antivirus_Status": check_antivirus(),
#         "BitLocker_Status": check_bitlocker(),
#         # "Pirated_Software_Check": check_pirated_software(),
#         "USB_Storage_Access": check_usb_storage(),
#         "Firewall_Status": check_firewall(),
#         "BIOS_Password_Status": check_bios_password(),
#         "Secure_Boot_Status": check_secure_boot(),
#     }

if __name__ == "__main__":
     report = {
        "OS_Version": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version()
        },
        "Auto_Update": check_auto_update(),
        "Antivirus_Status": check_antivirus(),
        "BitLocker_Status": check_bitlocker(),
        "USB_Storage_Access": check_usb_storage(),
        "Firewall_Status": check_firewall(),
        "BIOS_Password_Status": check_bios_password(),
        "Secure_Boot_Status": check_secure_boot()
    }

    # Print JSON properly
     print(json.dumps(report)) # For Valid Parsing of the report to JSON
