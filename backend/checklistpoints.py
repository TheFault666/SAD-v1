import platform
import os
import subprocess
import winreg
import re

checklist = ['auditee_name', 'auditor_name', 'host_name', 'user_name', 'operating_system', 'genuine', 'os_version', 'os_install_date', 'os_updates', 'autoupdate_status', 'installed_antivirus', 'system_software', 'pirated_software', 'mac_addr', 'ip_addr']

context = {val: None for val in checklist}

context[checklist[0]] = input('Enter your name: ')
context[checklist[1]] = 'auditor'
context[checklist[2]] = platform.node()  # Hostname
context[checklist[3]] = os.environ.get("USERNAME") or os.environ.get("USER")  # Username
context[checklist[4]] = platform.system()  # OS Name
context[checklist[6]] = platform.version()  # OS Version

# checking OS Installation Date !!!
# print('checking os installation date') 
try:
    result = subprocess.run(["wmic", "os", "get", "InstallDate"], capture_output=True, text=True, shell=True)
    date_str = result.stdout.split("\n")[1].strip()[:14]  # Extract date
    context[checklist[7]] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {date_str[8:10]}:{date_str[10:12]}"
except:
    context[checklist[7]] = "Unable to fetch"  
# print('done')

# # Installed Windows Updates
# ~~~~~To be added~~~~~

# Automatic Updates Status
# print('checking automatic update status')
# ~~~~~To be added~~~~~

# Checking Installed Antivirus
# ~~~~~To be added~~~~~

# Checking Installed System Software
print('checking for installed software')
try:
    result = subprocess.run(["wmic", "product", "get", "name"], capture_output=True, text=True, shell=True)
    software_list = [line.strip() for line in result.stdout.split("\n")[1:] if line.strip()]
    context[checklist[11]] = f"{len(software_list)} software installed"
except:
    context[checklist[11]] = "Unable to fetch"
print('done')

# Detecting Pirated Software
print('looking for pirated software')
try:
    pirated_keywords = ["crack", "keygen", "patch", "activator"]
    pirated = [soft for soft in software_list.split("\n") if any(keyword in soft.lower() for keyword in pirated_keywords)]
    context[checklist[12]] = ", ".join(pirated) if pirated else "No pirated software detected"
except:
    context[checklist[12]] = "Unable to scan"
print('done')

#checking for mac and ip addresses
print('done')
try:
    ipconfigs = subprocess.check_output(['ipconfig', '/all']).decode('utf-8').splitlines()
    # print(ipconfigs)
    mac_addresses = [line.split(":")[-1].strip() for line in ipconfigs if "Physical Address" in line]
    ipv4_addresses = [ip for line in ipconfigs for ip in re.findall(r'\d+\.\d+\.\d+\.\d+', line) if "IPv4" in line]
    default_gateways = [ip for line in ipconfigs for ip in re.findall(r'\d+\.\d+\.\d+\.\d+', line) if "Default Gateway" in line]
    # print("MAC Addresses:", mac_addresses)
    # print("IPv4 Addresses:", ipv4_addresses[0])
    # print("Default Gateways:", default_gateways)
    context[checklist[13]] = mac_addresses[0]
    context[checklist[14]] = ipv4_addresses[0]
except:
    context[checklist[13]] = 'Not Found'
    context[checklist[14]] = 'Not Found'
print('done')
    
# Printing the results
print(context)
