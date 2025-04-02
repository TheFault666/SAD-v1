import platform
import os
import subprocess
import winreg

checklist = ['auditee_name', 'auditor_name', 'host_name', 'user_name', 'operating_system', 'genuine', 'os_version', 'os_install_date', 'os_updates', 'autoupdate_status', 'installed_antivirus', 'system_software', 'pirated_software']

context = {val: None for val in checklist}

context[checklist[0]] = input('Enter your name: ')
context[checklist[1]] = 'auditor'
context[checklist[2]] = platform.node()  # Hostname
context[checklist[3]] = os.environ.get("USERNAME") or os.environ.get("USER")  # Username
context[checklist[4]] = platform.system()  # OS Name
context[checklist[6]] = platform.version()  # OS Version

# checking OS Installation Date
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
print('checking for installed antivirus')
try:
    result = subprocess.run(["wmic", "antivirusproduct", "get", "displayName"], capture_output=True, text=True, shell=True)
    antiviruses = [line.strip() for line in result.stdout.split("\n")[1:] if line.strip()]
    context[checklist[10]] = ", ".join(antiviruses) if antiviruses else "No antivirus found"
except:
    context[checklist[10]] = "Unable to fetch"
print('done')

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

# Printing the results
print(context)

# Render the Word document with the collected data
# doc.render(context)
# output_path = fr'{cur_dir}/audit_report_filled.docx'
# doc.save(output_path)
# print(f"Audit report saved as: {output_path}")
