import wmi
import json
import requests

def get_flat_hardware_data():
    try:
        c = wmi.WMI()
        system = c.Win32_ComputerSystemProduct()[0]
        ram = c.Win32_PhysicalMemory()
        disks = c.Win32_DiskDrive()

        # Extract first RAM info (or set N/A)
        ram_info = {
            "ram_serial": ram[0].SerialNumber.strip() if ram and ram[0].SerialNumber else "N/A",
            "ram_manufacturer": ram[0].Manufacturer.strip() if ram and ram[0].Manufacturer else "N/A",
            "ram_part_number": ram[0].PartNumber.strip() if ram and ram[0].PartNumber else "N/A"
        }

        # Extract first Disk info (or set N/A)
        disk_info = {
            "disk_model": disks[0].Model.strip() if disks and disks[0].Model else "N/A",
            "disk_interface_type": disks[0].InterfaceType.strip() if disks and disks[0].InterfaceType else "N/A",
            "disk_serial": disks[0].SerialNumber.strip() if disks and disks[0].SerialNumber else "N/A"
        }

        data = {
            "client_name": "Aayush Prasad Shambhu",
            "client_email": "aayushp336@gmail.com",
            "client_phone": "09328788481",
            "owner_name": "Shop Owner's name",
            "device_product_id": system.IdentifyingNumber.strip(),
            "device_model_name": system.Name.strip(),
            **ram_info,
            **disk_info
        }

        return data

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    data = get_flat_hardware_data()
    print(json.dumps(data, indent=2))

    try:
        response = requests.post("http://127.0.0.1:8000/owner/data/api/", json=data)
        print(response.status_code, response.text[:5000])
    except Exception as e:
        print("Error submitting data:", str(e))
