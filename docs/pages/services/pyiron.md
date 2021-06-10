---
title: 'pyiron'
---

Pyiron
===


[![hackmd-github-sync-badge](https://hackmd.io/ut4CsaYCSAq4K3XDOnGAqA/badge)](https://hackmd.io/ut4CsaYCSAq4K3XDOnGAqA)

[<i class="fa fa-arrow-circle-left"></i> Previous](https://hackmd.io/@materialdigital/rJFe5vQ5_)

## Table of Contents

[TOC]

# Deployment of pyiron workflow environment 
[This repository](https://github.com/materialdigital/pyiron_workflow_environment_deployment) provides the configuration files, needed for the deployment of a pre-configured jupyterhub to run pyiron workflows.

## Content of the repository
| File | Description |
| ----------------- | ----------- |
| `config.json` | a json file containing the configurable environment variables: keycloak client details, name of pyiron docker images, users' resources, and Postgres database Password |
| `static.json` | a json file containing the non-configurable environment variables |
| `nginx/pyiron.conf` | A template of the configuration file for the Nginx reverse proxy |
| `docker-compose.yml` | the compose file, which runs jupyterhub and its Postgres database services. |
   
## Deployment Guide
### The infrastructure, OS and other required packages
As an infrastructure, the deployment requires:  
- A server running a Linux operating system
- Installation of docker engine and docker-compose
- Adequate resources for running jupyterhub: (>2GB of RAM + 2 VCPU) 
- The users' resources on the server should be proportional to the number of users (~2GB of RAM, 2VCPU, 10GB of storage per users)

### Assumptions
- For the authentication of the users, keycloak is assumed as the authentication provider. Therefore, a client id and secret are needed.
- Here, it is assumed that all the jobs are run on the same server as the jupyterhub.
- The configuration of the hostnames is assumed to be done separately by the admin, e.g. creating the A-record, etc

### pyiron docker images  
In the configuration file `config.json`, it is needed to pass in a set of pyiron docker image. pyiron offers various docker images corresponding to its modules, atomistics, continuum, md, ... . The docker images are available on docker hub: [https://hub.docker.com/u/pyiron](https://hub.docker.com/u/pyiron), and the corresponding dockerfiles can also be found via [https://github.com/pyiron/docker-stacks](https://github.com/pyiron/docker-stacks).   

### Nginx configuration
For the Nginx reverse proxy, you need to provide a configuration file, e.g. `pyiron.conf`. A template of such file is provided in the repository under `repo_path/nginx/pyiron.conf`  
After adding the domain, and the path to the SSL certificates and key (as described [here](https://hackmd.io/@materialdigital/H1t3_GQ9O)), you should copy it to the nginx directory:
```bash
cp nginx/pyiron.conf ../data/nginx/
```
Of course, here it is assumed that the PMD-S core repo is the parent directory of the pyiron deployment directory.

### Adding pyiron client to Keycloak
For configuring the hub to authenticate the users via keycloak, you need to create a client in the keycloak instance. You can create the client via the following steps:
1) Signing in as the admin of the keycloak instance,
2) Select your desirable realm
3) Select clients from the left panel
4) On the top right-hand side, select create.
5) Enter a client ID, and a root URL. For the URL, you should provide the url of pyiron.
   ![](client.png)
6) click save.
7) In the setting tab, change the access type to confidential, and save.
8) From the credential tab, you can obtain the client secret.

For configuring pyiron, you need the keycloak domain, the realm, the client id, and the client secret.

### The process of the deployment
It is assumed that the current working directory is the root of [PMD-S core repository](https://github.com/materialdigital/pmd-server).
1) cloning the current git repository.
   ```bash
   git clone https://github.com/materialdigital/pyiron_workflow_environment_deployment.git pyiron/
   cd pyiron
   ```
2) Providing the values for the keys in the `config.json` file. The keys are:
- `OAUTH2_TOKEN_URL`: Keycloak Tocken URL; here you need only to change the domain and the realm
- `OAUTH2_AUTHORIZE_URL`:Keycloak authorize URL; here you need only to change the domain and the realm
- `OAUTH2_USERDATA_URL`: Keycloak userdate URL; here you need only to change the domain and the realm
- `OAUTH_CALLBACK_URL`: Keycloak call back URL; here you need only to change the domain
- `CLIENT_ID`: The client ID defined in Keycloak
- `CLIENT_SECRET`: The secret for the client, provided from the Keycloak instance 
- `PYIRON_BASE`: The relavant information of pyiron_base image in the form of `image_name:tag, e.g. pyiron/base:2021-06-04`
- `PYIRON_ATOMISTIC`: The relavant information of pyiron_atomistics image in the form of `image_name:tag, e.g. pyiron/pyiron:2021-06-04`
- `PYIRON_CONTINUUM`: The relavant information of pyiron_continuum image in the form of `image_name:tag, e.g. pyiron/continuum:2021-06-04`.
- `PYIRON_EXPERIMENTAL`: The relavant information of pyiron_experimental image in the form of `image_name:tag, e.g. pyiron/experimental:2021-06-04`
- `MEM_LIMIT`: The limiting amount of RAM per user
- `CPU_LIMIT`: The limiting amount of VCPU per user
- `ADMIN_USER`: The username of jupyterhub admin, this username should be consistent with the username in the keycloak instance 
- `POSTGRES_PASSWORD`: A password for the postgres database

3) run the `config.py` script from the pmd-server parent directory.
   - in the case that python3 is installed on the host OS:
      ```bash
       python3 ../scripts/configure.py
      ```
   - in the case of no python3 installation on the host OS:
      ```bash
       docker run --rm -v $PWD/:/tmp/ -v $PWD/../scripts/configure.py:/tmp/configure.py -w /tmp  python:3-alpine  python configure.py
      ```
4) run docker-compose script via
   ```bash
      docker-compose up -d
   ```
   

### HPC connection (will be added soon)  
In principal, the pyiron docker containers can submit jobs to the cluster according to pyiron documentation in [here](https://pyiron.readthedocs.io/en/latest/source/installation.html#submit-to-remote-hpc).
This feature will be added to pyiron docker images in the next release.

## Room for modification
Here we assumed a semi-automated deployment with minimal changes needed from the side of IT adminstrators. However, many things can be changed, such as:
- building a customized jupyterhub; this gives the possibility to change the jupyterhub configuration
- In the current setup, we assumed to have four jupyter environments based on: `pyiron_base`, `pyiron_atomistics`, and `pyiron_continuum`, `pyiron_experimental`. This list can be extended in the case of a customized jupyterhub build.

 


###### tags: `PMD Deployment guide`