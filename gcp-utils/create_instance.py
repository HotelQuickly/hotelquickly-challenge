"""This is a Google Cloud Platform API Utils.

    * Create a new compute engine instance
    * Get IP from new compute engine instance
"""
import argparse
import time
import os
import googleapiclient.discovery


"""Configuration the credentials in the environment.
"""
GOOGLE_APPLICATION_CREDENTIALS = "../credentials/marcelo-barbosa-7562531e527d.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS


def create_instance(compute, project, zone, name):
    """This function create a new compute instance.

    Args:
        compute: google api client
        project: project-id in GCP
        zone: region for run a compute engine instance
        name: identification of compute engine instance

    Returns:
        A compute instance object
    """
    image_response = compute.images().getFromFamily(
        project='centos-cloud', family='centos-7').execute()
    source_disk_image = image_response['selfLink']

    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_only',
                'https://www.googleapis.com/auth/logging.write',
                'https://www.googleapis.com/auth/monitoring.write',
                'https://www.googleapis.com/auth/servicecontrol',
                'https://www.googleapis.com/auth/service.management.readonly',
                'https://www.googleapis.com/auth/trace.append',
                'https://www.googleapis.com/auth/sqlservice.admin',
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        }],
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


def wait_for_operation(compute, project, zone, operation):
    """This function check a operation for create_instance() function
    finished or no pushing a time sleep for waiting creation.

    Args:
        compute: google api client
        project: project-id in GCP
        zone: region for run a compute engine instance
        operation: return of create_instance() function
    """
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            if 'error' in result:
                raise Exception(result['error'])
            break

        time.sleep(1)


def get_ip(compute, project, zone, name):
    """This show the ip from a new compute engine instance.

    Args:
        compute: google api client
        project: project-id in GCP
        zone: region for run a compute engine instance
        name: identification of compute engine instance

    Returns:
        Ip of new compute engine instance or None.
    """
    result = compute.instances().list(project=project, zone=zone).execute()

    for item in result['items']:

        if item['name'] == name:

            for new in item['networkInterfaces']:
                return new['accessConfigs'][0]['natIP']



def main(project, zone, name, wait=True):
    """This main function connection other functions working together.

    Args:
        project: project-id in GCP
        zone: region for run a compute engine instance
        name: identification of compute engine instance
    """
    compute = googleapiclient.discovery.build('compute', 'v1')

    operation = create_instance(compute, project, zone, name)
    wait_for_operation(compute, project, zone, operation['name'])



if __name__ == '__main__':
    """
    For example:
        python create_instance.py project_id --zone zone_gcp --name instance_name
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    args = parser.parse_args()
    main(args.project_id, args.zone, args.name)

    compute_ip = googleapiclient.discovery.build('compute', 'v1')
    print get_ip(compute_ip, args.project_id, args.zone, args.name)
