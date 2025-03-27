import subprocess
import winreg
import os
import platform

# Function to check Windows OS version
def check_os_version():
    return platform.system(), platform.release(), platform.version()

# Function to check if OS auto-update is enabled
def check_auto_update():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU")
        value, _ = winreg.QueryValueEx(key, "NoAutoUpdate")
        return "Auto-update is disabled." if value == 1 else "Auto-update is enabled."
    except FileNotFoundError:
        return "Auto-update settings not found, assuming enabled by default."

# Function to check antivirus installation and status
def check_antivirus():
    cmd = "powershell Get-CimInstance -Namespace root\\SecurityCenter2 -ClassName AntivirusProduct"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return result.stdout if result.stdout else "No antivirus detected."

# Function to check if BitLocker is enabled
def check_bitlocker():
    cmd = "powershell Get-BitLockerVolume | Select-Object -Property VolumeStatus"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    if "FullyEncrypted" in result.stdout:
        return "BitLocker is enabled."
    else:
        return "BitLocker is not enabled."

# Function to check for pirated software (Basic Approach)
def check_pirated_software():
    pirated_keywords = ["crack", "keygen", "patch", "pirate"]
    suspect_files = []
    for root, _, files in os.walk("C:\\"):
        for file in files:
            if any(keyword in file.lower() for keyword in pirated_keywords):
                suspect_files.append(os.path.join(root, file))
    return suspect_files if suspect_files else "No pirated software detected."

# Function to check if USB storage devices are authorized (checks for enabled USB Mass Storage Service)
def check_usb_storage():
    cmd = "powershell Get-Service -Name USBSTOR"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    if "Running" in result.stdout:
        return "USB storage is enabled."
    else:
        return "USB storage is disabled."

# Function to check firewall status
def check_firewall():
    cmd = "powershell Get-NetFirewallProfile -Profile Domain,Public,Private | Select-Object -Property Enabled"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    if "True" in result.stdout:
        return "System firewall is active."
    else:
        return "System firewall is inactive."

# Function to check for BIOS password (Requires Manual Check)
def check_bios_password():
    return "Manual check required: Verify BIOS password in BIOS setup."

# Function to check if Secure Boot is enabled
def check_secure_boot():
    cmd = "powershell Confirm-SecureBootUEFI"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    if "True" in result.stdout:
        return "Secure Boot is enabled."
    else:
        return "Secure Boot is not enabled."

# Generate Report
def generate_report():
    print("Generating System Security Report:\n")
    print("OS Version:", check_os_version())
    print("Auto-Update Status:", check_auto_update())
    print("Antivirus Status:", check_antivirus())
    print("BitLocker Status:", check_bitlocker())
    pirated_files = check_pirated_software()
    print("Pirated Software Check:", pirated_files if isinstance(pirated_files, str) else f"Suspicious files: {len(pirated_files)} detected.")
    print("USB Storage Access:", check_usb_storage())
    print("Firewall Status:", check_firewall())
    print("BIOS Password Status:", check_bios_password())
    print("Secure Boot Status:", check_secure_boot())

if __name__ == "__main__":
    generate_report()
