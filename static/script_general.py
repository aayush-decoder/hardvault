import wmi
import json
import requests

def get_flat_hardware_data(client_code):
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
            "client_code": client_code,
            "device_product_id": system.IdentifyingNumber.strip(),
            "device_model_name": system.Name.strip(),
            **ram_info,
            **disk_info
        }

        return data

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 50)
    print("Hardware Information Collector")
    print("=" * 50)
    
    # Prompt user for their client code
    client_code = input("\nPlease enter your client code: ").strip().upper()
    
    if not client_code:
        print("Error: Client code is required!")
        input("Press Enter to exit...")
        exit(1)
    
    print("\nCollecting hardware information...")
    data = get_flat_hardware_data(client_code)
    
    if "error" in data:
        print(f"Error collecting hardware data: {data['error']}")
        input("Press Enter to exit...")
        exit(1)
    
    print("\nHardware data collected successfully!")
    print(json.dumps(data, indent=2))
    
    print("\nSubmitting data to server...")
    try:
        response = requests.post("https://hardvault.onrender.com/owner/data/api/", json=data)
        
        if response.status_code == 200:
            print("\n✓ Success! Your hardware information has been submitted.")
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"\n✗ Error submitting data: {str(e)}")
    
    input("\nPress Enter to exit...")
