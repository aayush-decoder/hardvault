import platform
import subprocess
import json
import psutil

def get_disk_serial_windows():
    try:
        result = subprocess.run(["wmic", "diskdrive", "get", "serialnumber"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_disk_serial_linux():
    try:
        result = subprocess.run(["lsblk", "-o", "NAME,SERIAL"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_system_info_windows():
    try:
        result = subprocess.run(["wmic", "csproduct", "get", "name,identifyingnumber,vendor"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_system_info_linux():
    try:
        result = subprocess.run(["sudo", "dmidecode", "-t", "system"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_ram_serials_windows():
    try:
        result = subprocess.run(["wmic", "memorychip", "get", "serialnumber"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_ram_serials_linux():
    try:
        result = subprocess.run(["sudo", "dmidecode", "--type", "17"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_basic_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "cpu": platform.processor(),
        "ram_gb": round(psutil.virtual_memory().total / 1e9, 2)
    }

def get_all_hardware_info():
    system = platform.system().lower()
    info = get_basic_info()

    if system == "windows":
        info.update({
            "disk_serials": get_disk_serial_windows(),
            "system_info": get_system_info_windows(),
            "ram_serials": get_ram_serials_windows()
        })
    elif system == "linux":
        info.update({
            "disk_serials": get_disk_serial_linux(),
            "system_info": get_system_info_linux(),
            "ram_serials": get_ram_serials_linux()
        })
    else:
        info.update({
            "disk_serials": "Unsupported OS",
            "system_info": "Unsupported OS",
            "ram_serials": "Unsupported OS"
        })

    return info

hardware_info = get_all_hardware_info()
hardware_info_json = json.dumps(hardware_info, indent=2)
print("hardware info: ", hardware_info)
print(hardware_info['system_info'])
hardware_info_json[:3000]  # Truncated for display if too long

import wmi
c = wmi.WMI()
for mem in c.Win32_PhysicalMemory():
    print(mem.SerialNumber, mem.Manufacturer, mem.PartNumber)


import wmi

def get_physical_disk_serials():
    c = wmi.WMI()
    result = []
    for disk in c.Win32_DiskDrive():
        result.append({
            'model': disk.Model,
            'interface_type': disk.InterfaceType,
            'serial': disk.SerialNumber.strip() if disk.SerialNumber else "N/A"
        })
    return result

print(get_physical_disk_serials())



import requests
try:
    response = requests.post("http://127.0.0.1:8000/owner/data/api/", json=data)
    print(response.status_code, response.text[:5000])
except Exception as e:
    print("Error submitting data:", str(e))
