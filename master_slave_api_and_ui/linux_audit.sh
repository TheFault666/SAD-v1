#!/bin/bash

tput clear
trap ctrl_c INT 

function ctrl_c() {
    echo "Pressed CTRL+C...Exiting"
    exit 0
}

START=$(date +%s)

# Get User & Privileges
USER_NAME=$(whoami)
USER_GROUPS=$(groups "$USER_NAME" | tr -d '\n')

check_sudo() {
    if sudo -n true 2>/dev/null; then
        echo "Yes"
    else
        echo "No"
    fi
}
SUDO_STATUS=$(check_sudo)

# Get OS Information
OS_NAME=$(grep "^NAME=" /etc/os-release | cut -d '=' -f2 | tr -d '"')
OS_VERSION=$(grep "^VERSION=" /etc/os-release | cut -d '=' -f2 | tr -d '"')
OS_RELEASE=$(grep "^VERSION_ID=" /etc/os-release | cut -d '=' -f2 | tr -d '"')

# Get System Information
CPU_MODEL=$(lscpu | grep "Model name" | awk -F: '{print $2}' | sed 's/^ *//' | tr -d '\n')
CPU_CORES=$(nproc)
RAM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
RAM_USED=$(free -m | awk '/Mem:/ {print $3}')
RAM_FREE=$(free -m | awk '/Mem:/ {print $4}')
ARCHITECTURE=$(uname -m)
HOSTNAME=$(hostname)
KERNEL_VERSION=$(uname -r)
DISK_USAGE=$(df -h / | awk 'NR==2 {print $3 "/" $2 " used"}')

# Get Network Details (Sanitizing output)
Network_Details=$(ip -o -4 addr show | awk '{print $2 ": " $4}' | jq -Rs .)

# Check Firewall Status (Sanitizing output)
Firewall_Status=$(ufw status verbose 2>/dev/null || echo "UFW Not Installed")
Firewall_Status=$(echo "$Firewall_Status" | jq -Rs .)

# Secure Boot Check (Fixed for empty file issues)
check_secure_boot() {
    if [ ! -d /sys/firmware/efi ]; then
        echo "Legacy BIOS"
    else
        SecureBootFile=$(find /sys/firmware/efi/vars/ -name "SecureBoot-*/data" 2>/dev/null | head -n 1)
        
        if [[ -n "$SecureBootFile" && -f "$SecureBootFile" ]]; then
            STATUS=$(cat "$SecureBootFile" | hexdump -e '"%d"' 2>/dev/null)
            if [[ "$STATUS" =~ ^[0-9]+$ ]]; then
                [[ "$STATUS" -eq 1 ]] && echo "Enabled" || echo "Disabled"
            else
                echo "Status Unknown"
            fi
        else
            echo "Status Unknown"
        fi
    fi
}
Secure_boot=$(check_secure_boot)

# Get Installed Third-Party Software with Versions (Fixing newlines)
installed=$(comm -23 <(apt list --installed 2>/dev/null | awk -F'[/ ]' '{print $1, $2}' | sort) \
                    <(apt list --installed 2>/dev/null | grep '\[installed,automatic\]' | awk -F'[/ ]' '{print $1, $2}' | sort))

declare -A Software_Status

while read -r package version; do
    latest=$(apt-cache policy "$package" | grep Candidate | awk '{print $2}')
    if [[ "$latest" != "$version" && "$latest" != "(none)" ]]; then
        Software_Status["$package"]="{\"Current Version\": \"$version\", \"Status\": \"Update available ($latest)\"}"
    else
        Software_Status["$package"]="{\"Current Version\": \"$version\", \"Status\": \"Up-to-date\"}"
    fi
done <<< "$installed"

# Build JSON Output
json_output=$(cat <<EOF
{
    "User": {
        "Username": $(echo "$USER_NAME" | jq -Rs .),
        "Groups": $(echo "$USER_GROUPS" | jq -Rs .),
        "Sudo Privilege": "$SUDO_STATUS"
    },
    "System Info": {
        "Hostname": "$HOSTNAME",
        "OS Name": "$OS_NAME",
        "OS Version": "$OS_VERSION",
        "OS Release": "$OS_RELEASE",
        "Kernel Version": "$KERNEL_VERSION",
        "Architecture": "$ARCHITECTURE",
        "CPU Model": $(echo "$CPU_MODEL" | jq -Rs .),
        "CPU Cores": "$CPU_CORES",
        "RAM Total (MB)": "$RAM_TOTAL",
        "RAM Used (MB)": "$RAM_USED",
        "RAM Free (MB)": "$RAM_FREE",
        "Disk Usage": "$DISK_USAGE"
    },
    "Network": {
        "Details": $Network_Details
    },
    "Firewall": {
        "Status": $Firewall_Status
    },
    "Secure Boot": "$Secure_boot",
    "Installed Software": {
EOF
)

for key in "${!Software_Status[@]}"; do
    json_output+="\"$key\": ${Software_Status[$key]},"
done

# Remove last comma and close JSON
json_output=${json_output%,}
json_output+="}}"

# Print JSON Output
echo "$json_output" | jq .

END=$(date +%s)
DIFF=$(( END - START ))
echo "Script completed in $DIFF seconds."

exit 0
