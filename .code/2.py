import os
from google.cloud import compute_v1

# Set up credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

# Create a VM instance
def create_vm(project_id, zone, instance_name, machine_type, image_family, disk_size_gb):
    compute_client = compute_v1.InstancesClient()

    project_zone = f"projects/{project_id}/zones/{zone}"
    image_response = compute_client.get_image(project_zone, image_family)

    config = {
        "name": instance_name,
        "machine_type": f"zones/{zone}/machineTypes/{machine_type}",
        "disks": [
            {
                "boot": True,
                "auto_delete": True,
                "initialize_params": {
                    "source_image": image_response.self_link,
                    "disk_size_gb": disk_size_gb,
                },
            }
        ],
    }

    operation = compute_client.insert(project_zone, config)
    operation.result()

    print(f"VM instance {instance_name} created successfully!")

# Delete a VM instance
def delete_vm(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()

    project_zone = f"projects/{project_id}/zones/{zone}"
    instance_response = compute_client.get(project_zone, instance_name)

    operation = compute_client.delete(project_zone, instance_name)
    operation.result()

    print(f"VM instance {instance_name} deleted successfully!")

# Main function
def main():
    project_id = "86000DDDE7"
    zone = "your-zone"
    instance_name = "your-instance-name"
    machine_type = "linux_X86_64-debian_chromeos"
    image_family = "your-image-family"
    disk_size_gb = 10

    try:
        create_vm(project_id, zone, instance_name, machine_type, image_family, disk_size_gb)
        delete_vm(project_id, zone, instance_name)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
