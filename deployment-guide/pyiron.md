---
title: 'pyiron (PMD App)'
---

Pyiron
===

[<i class="fa fa-arrow-circle-left"></i> Previous](https://hackmd.io/@materialdigital/rJFe5vQ5_)

## Table of Contents

[TOC]

## Repository
 
Clone the required configuration files:

```bash=
git clone https://int-gitlab.int.kit.edu/architektur/jupyterhub_deployment.git
```

The repository provides the configuration files, needed for a semi-automated deployment of a pre-configured jupyterhub to run pyiron workflows.

## Content
| File | Description |
| ----------------- | ----------- |
|`auto_config.json` | a json file containing the needed info for ssl certificate path, keycloak client details, name of pyiron docker images, |
| `.env` | includes all the default environmental variable essential for running the docker-compose script |
| `create_hub.py` | the python script which appends the given key-value pairs in the `auto_config.json` file, as environmental variable into `.env` file. Additionally it creates the necessary docker network, docker volumes. It also pulls the necessary docker images from DockerHub. |
| `docker-compose.yml` | the docker-compose file, which runs jupyterhub and its Postgres database services. |
   
## Deployment Guide
### The infrastructure, OS and other required packages
As an infrastructure, the deployment requires:  
- A server running a Linux operating system
- Installation of docker engine and docker-compose
- Adequate resources for running jupyterhub: (>2GB of RAM + 2 VCPU) 
- The users' resources on the server should be proportional to the number of users (~2GB of RAM, 2VCPU, 10GB of storage per users)

### Assumptions
- For the authentication of the users, keycloak is assumed as authentication provider. Therefore, a client id and secret is needed.
- Here, it is assumed that all the jobs are run on the same server
- Hosting configuration is assumed to be done separately by the admin, e.g. the defintion of a A-record for the DNS

### The process of the deployment
1) cloning the current git repository.
2) Providing the values for the keys in the `auto_config.json` file. The keys are:
- `HOST_KEY_PATH`: Path to the SSL key on the server 
- `HOST_CERT_PATH`: Path to the SSL certificate on the server
- `OAUTH2_TOKEN_URL`: Keycloak Tocken URL
- `OAUTH2_AUTHORIZE_URL`:Keycloak authorize URL
- `OAUTH2_USERDATA_URL`: Keycloak userdate URL
- `OAUTH_CALLBACK_URL`: Keycloak call back URL
- `CLIENT_ID`: The client ID defined in Keycloak
- `CLIENT_SECRET`: The secret for the client, provided from the Keycloak instance 
- `PYIRON_BASE`: the relavant information of pyiron_base image in the form of `image_name:tag`
- `PYIRON_ATOMISTIC`:the relavant information of pyiron_atomistics image in the form of `image_name:tag`
- `PYIRON_CONTINUUM`:the relavant information of pyiron_continuum image in the form of `image_name:tag`
- `MEM_LIMIT`: The limiting amount of RAM per user
- `CPU_LIMIT`: The limiting amount of VCPU per user
- `ADMIN_USER`: The username of jupyterhub admin 

3) run the `create_hub.py` script.  
4) run docker-compose script via `docker-compose up -d`


### HPC connection (will be added soon)  
In principal, the pyiron docker containers can submit jobs to the cluster according to pyiron documentation in [here](https://pyiron.readthedocs.io/en/latest/source/installation.html#submit-to-remote-hpc).
This feature will be added to pyiron docker images in the next release.

## Room for modification
Here we assumed a semi-automated deployment with minimal changes needed from the side of IT adminstrators. However, many things can be changed, such as:
- building a customized jupyterhub; this gives the possibility to change the jupyterhub configuration
- In the current setup, we assumed to have three jupyter environment based on: `pyiron_base`, `pyiron_atomistics`, and `pyiron_continuum`. This list can be extended in the case of a customized jupyterhub build. 


###### tags: `PMD Deployment guide`