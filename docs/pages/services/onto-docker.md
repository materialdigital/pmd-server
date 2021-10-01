---
title: OntoDocker
nav_order: 1
parent: PMD-S Services
---

OntoDocker
===
{: .no_toc }

## Table of Contents
{: .no_toc }

- TOC
{:toc}

## Description

OntoDocker is a Flask application-prototype to access a Blazegraph and Jena instance via a GUI and an API.

API authentication via JWT and OIDC.
Allowed Content-Types to upload are "text/turtle" and "application/rdf+xml" as .ttl/.rdf files

## Setup
### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](PMD-core-components.md})
* Running reverse proxy as described under - [Reverse Proxy](reverse_proxy.md)

### 1. Clone the repository

```bash
git clone https://git.material-digital.de/apps/ontodocker.git
cd ontodocker
```

### 2. Connect to SSO Identity Provider (IDP)

> **Note:** If you have a valid client_secrets.json already, place it in `./data/oidc/`
{: .warning }

Otherwise in order to connect OntoDocker to the IDP you might need an initial access token (IAT) or generate one, if you want to connect it to your local Instance. (see "Initial Access Token" section of the [Keycloak manual](https://www.keycloak.org/docs/latest/securing_apps/#_initial_access_token))

Save the Initial Access Token as ```ia.jwt```

Replace KEYCLOAK_URL, REALM_NAME in ```provider_info.json``` accordingly to the IDPs properties

Set the APPLICATION_URL to the url where your instance is supposed to be accessible at

Copy both ```ia.jwt``` and the customized ```provider_info.json``` files to ```./data/oidc/```

```bash
# Build the containers
docker-compose build
```

### 3. Start OntoDocker
After successful build you can start OntoDocker:

```bash
# Start onto-docker after rebuild to ensure `client_secrets.json` is added to the image
docker-compose up -d --build

# verify onto-docker and blazegraph are running properly
docker-compose ps
```

### 5. Connect onto-docker to the reverse proxy

> **Note:** This example assumes you chose the reverse proxy with certbot.
{: .warning }

#### Add nginx configuration

```bash
# save OntoDocker URL to shell variable
# ! Replace "ontodocker.domain.de" with the actual URL for the service
export ONTODOCKER_URL=ontodocker.domain.de

# change to pmd-server directory
cd ..

# add the nginx configuration from the template
sed "s/\[URL\]/${ONTODOCKER_URL}/" ontodocker/nginx/prod.conf > data/nginx/ontodocker.conf
```

#### Retrieve Let's Encrypt certificate

```bash

docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d ${ONTODOCKER_URL}
```

#### Test and load the configuration
```bash
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### 6. Test Installation

Open your browser and navigate to the URL of your OntoDocker installation. If the installation succeeded you should now be redirected to the SSO Login Screen and after successful authentication see the OntoDocker landing page:

![](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/ontodocker.png?raw=true)

## Usage

Refer to [`api_usage_examples.py`](https://git.material-digital.de/apps/ontodocker/-/blob/master/api_usage_examples.py) for examples on how to use the API.


Graph visualization via WebVOWL 1.1.7

If the visualization doesn't load, clear the browsers cache and refresh the page.


[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/H1P_XW7qO)


###### tags: `PMD Deployment guide`
{: .no_toc }
