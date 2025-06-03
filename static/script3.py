import wmi
import json
import requests

def get_system_product_info():
    try:
        c = wmi.WMI()
        system = c.Win32_ComputerSystemProduct()[0]
        return {
            "device_product_id": system.IdentifyingNumber.strip(),
            "device_model_name": system.Name.strip()
        }
    except Exception as e:
        return {"device_product_id": "Error", "device_model_name": str(e)}

def get_ram_info():
    try:
        c = wmi.WMI()
        ram_list = []
        for mem in c.Win32_PhysicalMemory():
            ram_list.append({
                "serial": mem.SerialNumber.strip() if mem.SerialNumber else "N/A",
                "manufacturer": mem.Manufacturer.strip() if mem.Manufacturer else "N/A",
                "part_number": mem.PartNumber.strip() if mem.PartNumber else "N/A"
            })
        return ram_list
    except Exception as e:
        return [{"error": str(e)}]

def get_physical_disks():
    try:
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_DiskDrive():
            disks.append({
                "model": disk.Model.strip() if disk.Model else "N/A",
                "interface_type": disk.InterfaceType.strip() if disk.InterfaceType else "N/A",
                "serial": disk.SerialNumber.strip() if disk.SerialNumber else "N/A"
            })
        return disks
    except Exception as e:
        return [{"error": str(e)}]

def collect_hardware_data():
    return {
        **get_system_product_info(),
        "ram_modules": get_ram_info(),
        "disks": get_physical_disks()
    }

if __name__ == "__main__":
    data = collect_hardware_data()
    print(json.dumps(data, indent=2))

    try:
        response = requests.post("http://127.0.0.1:8000/owner/data/api/", json=data)
        print(response.status_code, response.text[:5000])
    except Exception as e:
        print("Error submitting data:", str(e))

