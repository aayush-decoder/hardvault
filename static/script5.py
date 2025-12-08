# goal of this file is to build an exe file which displays all the config on the screen

import wmi
import json
import requests
import time

def get_flat_hardware_data():
    try:
        c = wmi.WMI()

        system = c.Win32_ComputerSystemProduct()[0]
        ram_modules = c.Win32_PhysicalMemory()
        disks = c.Win32_DiskDrive()

        # Collect all RAM modules
        ram_info = []
        for r in ram_modules:
            ram_info.append({
                "serial": (r.SerialNumber or "N/A").strip(),
                "manufacturer": (r.Manufacturer or "N/A").strip(),
                "part_number": (r.PartNumber or "N/A").strip(),
                "capacity_gb": round(int(r.Capacity) / (1024**3), 2) if r.Capacity else "N/A"
            })

        # Collect all disks
        disk_info = []
        for d in disks:
            disk_info.append({
                "model": (d.Model or "N/A").strip(),
                "interface": (d.InterfaceType or "N/A").strip(),
                "serial": (d.SerialNumber or "N/A").strip(),
                "size_gb": round(int(d.Size) / (1024**3), 2) if d.Size else "N/A"
            })

        # Summary Info
        data = {
            "client_name": "$NAME",
            "client_email": "$EMAIL",
            "client_phone": "$PHONE",
            "owner_name": "$OWNER_NAME",
            "device_product_id": system.IdentifyingNumber.strip(),
            "device_model_name": system.Name.strip(),
            "ram_modules": ram_info,
            "disks": disk_info
        }

        return data

    except Exception as e:
        return {"error": str(e)}

def pretty_print(data):
    print("\n================ HARDWARE CONFIGURATION ================\n")

    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key.upper()}:")
            for idx, item in enumerate(value, start=1):
                print(f"  [{idx}]")
                for sub_k, sub_v in item.items():
                    print(f"    {sub_k}: {sub_v}")
            print()
        else:
            print(f"{key}: {value}")
    print("========================================================\n")


if __name__ == "__main__":
    data = get_flat_hardware_data()

    # Display all config clearly on the screen
    pretty_print(data)

    # Also print raw JSON (optional)
    print(json.dumps(data, indent=2))

    # time.sleep(30)

    try:
        response = requests.post("http://127.0.0.1:8000/owner/data/api/", json=data)
        print("\nServer Response:", response.status_code)
        print(response.text[:5000])

    except Exception as e:
        print("\nError submitting data:", str(e))
