# Challenge for HotelQuickly - DevOps Engineer 
This document contain all steps for reproduce this challenge.


## Requirements
* [Python >= 2.7.12](https://www.python.org/downloads/ "Python")
* [Ansible >= 2.1.2.0](http://docs.ansible.com/ansible/intro_installation.html#installing-the-control-machine "Ansible")
* [OpenVPN client - TunnelBlick](https://tunnelblick.net/ "TunnelBlick")


## Environment
The challenge use [Google Cloud Platform](https://console.cloud.google.com/ "Google Cloud Platform") for Virtual Machine, Firewall and Cloud SQL.


## Repository
The [repository](https://github.com/firemanxbr/hotelquickly-challenge "repository") for this challenge contain all codes used. 


## Credentials
For provisioning new resources in GCP we need create a [service account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey "service account key"). Following the steps below:
* Access [Google Cloud Platform Console](https://console.cloud.google.com/ "Google Cloud Platform Console") in 'Api Manager' > 'Credentials'
* Select 'Compute Engine default service account'
* Select JSON (recommended)

Click in **Create** and move this file to `credentials/marcelo-barbosa-7562531e527d.json`.  

For use ansible in this challenge we need insert your ssh public key. Following the steps below:
* Access [Google Cloud Compute Engine](https://console.cloud.google.com/compute/metadata/sshKeys "Google Cloud Compute Engine") in 'Compute Engine' > 'Metadata' > 'SSH Keys'
* Copy from your computer/laptop, normally in this path: cat ~/.ssh/id_rsa.pub
* Insert this content using the button 'Add item'. Take care the new lines, sometimes you need remove '\n' in this information

Click in **Save**.


## Create a new OpenVPN Server
In this step we'll create a new OpenVPN Server for protect this environment. 

### Provisioning a new compute instance
In /gcp-utils we can use the file(create_instance.py) for create a new instance into Google Compute Engine. 

For example:

`$ cd gcp-utils/`

`$ python create_instance.py project_id --zone zone_gcp --name instance_name`

### Configure the new compute instance
We can use the Ansible for configure and test the OpenVPN Server.

For example:

`$ cd gcp-ansible/`

`$ ansible-playbook openvpn-server.yml`


## Configure the OpenVPN Client
In the client we can use the [Tunnelblick](https://tunnelblick.net/ "Tunnelblick"). In the directory **client/** have the keys and the `client.ovpn` for import and adjust for your system.

For example: (you should adjust the path for your system)

`ca /Users/firemanxbr/Documents/client/ca.crt`

`cert /Users/firemanxbr/Documents/client/client.crt`

`key /Users/firemanxbr/Documents/client/client.key`

`--tls-auth /Users/firemanxbr/Documents/client/ta.key 1`


## Backup and Restore the databases in Google Cloud SQL
For this challenge we can use the scripts in the directory **backup-cloud-sql/**.

For example:

`backup_cloud_sql.py` - Backup and restore production instances to cloned instances.

`restore.sh` - Run the restore using the **gcloud** tool. 


## Repository overview

* gcp-ansible/                  - Ansible resources for provisioning the OpenVPN Server
* ansible/files-openvpn-server  - Files pre-configured for configure this challenge
* backup-cloud-sql/             - Codes for backup and restore instances in Cloud SQL
* client/                       - Files for a OpenVPN Client. 
* credentials/                  - JSON service account for Compute Engine provisioning 
* gcp-utils/                    - Codes for provisioning a new instance in Compute Engine
* LICENSE                       - MIT License for this challenge
* README.md                     - Documentation 



## **WARNING**
All keys and credentials in this repository are only for this challenge. don't use this in production or in your project. Keep safe! 



## TODOLIST
**04/26/2017**
* Implement the Terraform.io, code as infrastructure
* Create a tests for this environment
* Monitoring this environment using Stackdriver - Monitoring
* Improve the hardening of OpenVPN Server and Client
* SSO - Single Sign-On using the Google Apps enterprise email
* Provisioning and configure the Jenkins Server for automate this deploy
