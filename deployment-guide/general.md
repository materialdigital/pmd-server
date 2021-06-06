---
title: 'General information'
---

PMD Deployment Guide
===

## Preface

The PMD-Mesh is envisioned as a network of PMD instances acting as IDS Data Providers and Data Consumers. Every PMD instance has the same underlying base - A PMD Server (PMD-S). 
While the architecture of the PMD-mesh is still work in progress, core functionalities of a PMD-S instance can already be deployed. The usage of docker and docker-compose for that purpose, ensures an easy transition of an initial standalone server into the PMD-Mesh. 

## System Requirements

* A Linux x86-64 system (bare metal or virtualized) with at least 2 CPU Cores allocated 
* At least 1GB of available disk space with additional space for applications 
* Admin (root) priviliges 
* [Docker Runtime](https://docs.docker.com/engine/install/) >= 19.03.13 
* [Docker compose](https://docs.docker.com/compose/install/) >= 1.27.41 
* RAM >= 4 GB 
* Activated Container support in the Kernel must be available 

For a subsequent incorpoaration into into the PMD mesh (WIP) it is advisable to fullfill the following requirement as well:
* Linux Kernel >= 5.6 or WireGuard kernel module (DKMS) 

[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/HJwVOfQ5_)

###### tags: `PMD Deployment guide`