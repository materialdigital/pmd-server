---
title: 'OntoDocker'
---

OntoDocker
===


[![hackmd-github-sync-badge](https://hackmd.io/HjZbIFIGS7yAvZGHI0rhMQ/badge)](https://hackmd.io/HjZbIFIGS7yAvZGHI0rhMQ)

[<i class="fa fa-arrow-circle-left"></i> Previous](https://hackmd.io/@materialdigital/rJKjpvmc_)



## Table of Contents

[TOC]

## Description

OntoDocker is a Flask application-prototype to access a Blazegraph instance via a GUI and an API.

- Accessible at https://ontodocker.material-digital.de/
- API authentication via JWT and OIDC.
  - Allowed Content-Types to upload are "text/turtle" and "application/rdf+xml" as .ttl/.rdf files

## Setup
### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](https://hackmd.io/@materialdigital/HJwVOfQ5_)
* Running reverse proxy as described under - [Reverse Proxy](https://hackmd.io/@materialdigital/H1t3_GQ9O) 

### 1. Clone the repository

```bash=
git clone https://git.materialdigital.de/apps/ontodocker.git
cd ontodocker
```

### 2. Copy compose template 

```bash=
# copy (or link) the compose file template
cp docker-compose-prod.yml docker-compose.yml
```

### 3. Connect to SSO Identity Provider (IDP)
In order to connect OntoDocker to the IDP you might need an initial access token (IAT) or generate one, if you want to connect it to your local Instance. (see "Initial Access Token" section of the [Keycloak manual](https://www.keycloak.org/docs/latest/securing_apps/#_initial_access_token))


```bash=+
# Build the containers
docker-compose build

# generate the client-secrets.json for onto-docker
docker-compose run --rm -w /app/app -v ${PWD}/flask_app/:/app ontodocker oidc-register --initial-access-token [TOKEN] https://[SSO_URL]/auth/realms/[SSO_REALM] [ONTODOCKER_URL]
```

### 4. Start OntoDocker 
After successful configuration of the SSO you can start OntoDocker:

```bash=+
# Start onto-docker after rebuild to ensure `client_secret.json` is added to the image
docker-compose up -d --build

# verify onto-docker and blazegraph are running properly
docker-compose ps
```

### 5. Connect onto-docker to the reverse proxy
:::warning
This example assumes you chose the reverse proxy with certbot.
:::

#### Add nginx configuration

```bash=+
# save OntoDocker URL to shell variable
# ! Replace "ontodocker.domain.de" with the actual URL for the service
export ONTODOCKER_URL=ontodocker.domain.de

# change to pmd-server directory
cd ..

# add the nginx configuration from the template 
sed "s/\[URL\]/${ONTODOCKER_URL}/" ontodocker/nginx/prod.conf > data/nginx/ontodocker.conf
```

#### Retrieve Let's Encrypt certificate

```bash=+

docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d ${ONTODOCKER_URL}
```

#### Test and load the configuration
```bash=
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### 6. Test Installation

Open you browser and navigate to the URL of your OntoDocker installation. If the installation succeeded you should now be redirected to the SSO Login Screen and after successful authentication see the OntoDocker landing page:

![](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/ontodocker.png?raw=true)

## Usage

Refer to [`api_usage_examples.py`](https://git.material-digital.de/apps/ontodocker/-/blob/master/api_usage_examples.py) for examples on how to use the API.


Graph visualization via WebVOWL 1.1.7

If the visualization doesn't load, clear the browsers cache and refresh the page.

## Appendix and FAQ

:::info
**Find this document incomplete?** Leave a comment!
:::

[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/H1P_XW7qO)

###### tags: `PMD Deployment guide`
