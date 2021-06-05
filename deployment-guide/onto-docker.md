---
title: 'Onto-Docker'
---

Onto-Docker
===

[<i class="fa fa-arrow-circle-left"></i> Previous](https://hackmd.io/@materialdigital/rJKjpvmc_)



## Table of Contents

[TOC]

## Setup
### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](https://hackmd.io/@materialdigital/HJwVOfQ5_)
* Running reverse proxy as described under - [Reverse Proxy](https://hackmd.io/@materialdigital/H1t3_GQ9O) 

### 1. clone the repository

```bash=
git clone https://git.material-digital.de/apps/onto-docker.git
cd onto-docker
```

### 2. copy compose template 

```bash=
# copy (or link) the compose file template
cp docker-compose-prod.yml docker-compose.yml
```

### 3. connect to SSO Identity Provider (IDP)
In order to connect Onto-Docker to the IDP you might need an initial access token (IAT) or generate one if you want to connect it to you local Instance. (see "Generate an Initial Access Token" under [User Management](https://hackmd.io/@materialdigital/SJa76P7cO))


```bash=
# generate the client-secrets.json for onto-docker
docker-compose run --rm ontodocker oidc-register --initial-access-token [TOKEN] https://[SSO-URL]/auth/realms/[SSO-REALM] [ONTODOCKER-URL]
```

### 3. connect 

## Appendix and FAQ

:::info
**Find this document incomplete?** Leave a comment!
:::

[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/H1P_XW7qO)

###### tags: `PMD Deployment guide`
