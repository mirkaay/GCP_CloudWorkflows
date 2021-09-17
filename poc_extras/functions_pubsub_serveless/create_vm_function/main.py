import os
import sys
import time
import requests
# from functions.wait import wait_for_operation

# from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
# from six.moves import input

# [START list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']
# [END list_instances]

def wait_for_operation(compute, project, zone, operation):
    sys.stdout.write('Waiting for operation to finish')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
# [END wait_for_operation]

# [START create_instance]
def create_instance(compute, project, zone, name, disk_images, machinetype, vm_subnetwork, service_account):
    # source_disk_image = "projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20210623"
    source_disk_image = disk_images
    machine_type = machinetype
    startup_script = 'startup-script.sh'

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            # 'network': 'global/networks/default',
            'subnetwork': vm_subnetwork,
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance access to  .......................
        'serviceAccounts': [{
            'email': service_account,
            'scopes': [
                "https://www.googleapis.com/auth/cloud-platform"
                ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': [{
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': open(startup_script, 'r').read()

            }]
        }]
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

def run(project, zone, instance_name, disk_images, machinetype, vm_subnetwork, service_account):
    # credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1')

    print('Creating instance.')

    operation = create_instance(compute, project, zone, instance_name, disk_images, machinetype, vm_subnetwork, service_account)
    wait_for_operation(compute, project, zone, operation['name'])

    instances = list_instances(compute, project, zone)

    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])
    

    print("Instance created")

def main(data, context):
    project = "<project id>"
    zone = 'us-central1-a'
    region = 'us-central1'
    disk_images = 'projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20210623'
    machinetype = 'zones/%s/machineTypes/n1-standard-1' % zone
    vm_subnetwork = 'projects/%s/regions/%s/subnetworks/default' % (project, region)
    service_account = '<SERVICE ACCOUNT NAME>@golang-misbah.iam.gserviceaccount.com'
    print('printing requestor {}'.format(data['attributes']['requestor']))
    instance_name = str(data['attributes']['requestor'])
    run(project, zone, instance_name, disk_images, machinetype, vm_subnetwork, service_account)

if __name__ == '__main__':
    main()

