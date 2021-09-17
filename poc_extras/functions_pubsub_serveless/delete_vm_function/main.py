import os
import sys
import time
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

# [START delete_instance]
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# [END delete_instance]


def run(project, zone, instance_name):
    # credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1')

    print('Deleting instance.')

    operation = delete_instance(compute, project, zone, instance_name)
    wait_for_operation(compute, project, zone, operation['name'])
    url= "<SLACK WEBHOOK URL>"
    payload = '{"text" : "Instance Created"}'
    response = requests.post(url=url, data=payload)
    print(response.text)
    print("Instance deleted.")

    print("Instance deleted.")


def main(data, context):
    project = "<PROJECT ID>"
    zone = 'us-central1-a'
    print('printing vmname {}'.format(data['attributes']['virtualmachine']))
    instance_name = str(data['attributes']['virtualmachine'])

    run(project, zone, instance_name)
    
if __name__ == '__main__':
    main()

