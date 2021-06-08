---
title: 'General information'
---

PMD Deployment Guide
===


[![hackmd-github-sync-badge](https://hackmd.io/biFcWHrUTceoopWdvOmFuw/badge)](https://hackmd.io/biFcWHrUTceoopWdvOmFuw)

## Preface

The PMD-Mesh is envisioned as a network of PMD instances acting as IDS Data Providers and Data Consumers. Every PMD instance has the same underlying base - A PMD Server (PMD-S). 
While the architecture of the PMD-mesh is still work in progress, core functionalities of a PMD-S instance can already be deployed. The usage of docker and docker-compose for that purpose, ensures an easy transition of an initial standalone server into the PMD-Mesh. 

:::warning
**Note:** firewalls and restrictive environments can cause various issues with the docker setup, which we are unable to foresee/test/cover. While we will try to help troubleshoot such issues, try to consult other online ressources as well. If you manage to find a solution without our help - Let us know and we can add it to the Known issues/FAQ section 
:::

## System Requirements
**Required:**
* A Linux x86-64 system (bare metal or virtualized) with at least 2 CPU Cores allocated 
* At least 1GB of available disk space with additional space for applications 
* Admin (root) priviliges 
* [Docker Runtime](https://docs.docker.com/engine/install/) >= 19.03.13 
* [Docker compose](https://docs.docker.com/compose/install/) >= 1.27.41
* [Git](https://git-scm.com) 
* RAM >= 4 GB 
* Activated Container support in the Kernel must be available 

**Recommended:**
* Python >= 3.5 
  - if not part of your system, python 3 can be installed via [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or run in a docker container
 
For a subsequent incorpoaration into the PMD mesh (WIP) it is advisable to fullfill the following requirement as well:
* Linux Kernel >= 5.6 or WireGuard kernel module (DKMS) 

## Setup your environment
* make sure to install all the requirements
* if you haven't done so, ensure the [user is in the docker group](https://docs.docker.com/engine/install/linux-postinstall/) (otherwise prefix all docker commands with `sudo`):
```bash=
# Add user to docker group 
# NOTE: this is equivalent to granting admin priviliges
usermod -a -G docker $(whoami)
```

[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/HJwVOfQ5_)

###### tags: `PMD Deployment guide`