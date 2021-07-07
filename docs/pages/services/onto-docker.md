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

OntoDocker is a Flask application-prototype to access a Blazegraph instance via a GUI and an API.

- Accessible at <https://ontodocker.material-digital.de/>
- API authentication via JWT and OIDC.
  - Allowed Content-Types to upload are "text/turtle" and "application/rdf+xml" as .ttl/.rdf files

## Setup
### Requirements
* The working directory is the base directory of the PMD-Server repo as described under [PMD-S Core](PMD-core-components.md)).
* A running reverse proxy as described under [Reverse Proxy](reverse_proxy.md).

### 1. Clone the Repository

```bash
git clone https://git.material-digital.de/apps/ontodocker.git
cd ontodocker
```

### 2. Copy Compose Template

```bash
# copy (or link) the compose file template
cp docker-compose-prod.yml docker-compose.yml
```

### 3. Connect to SSO Identity Provider (IDP)
In order to connect OntoDocker to the IDP you might need an initial access token
(IAT) or generate one, if you want to connect it to your local Instance. (see
"Initial Access Token" section of the [Keycloak manual](https://www.keycloak.org/docs/latest/securing_apps/#_initial_access_token)).


```bash
# Build the containers
docker-compose build

# generate the client_secrets.json for OntoDocker
docker-compose run --rm -w /app/app -v ${PWD}/flask_app/:/app ontodocker oidc-register --initial-access-token [TOKEN] https://[SSO_URL]/auth/realms/[SSO_REALM] [ONTODOCKER_URL]
```

{: .info }
> **Note:** For brevity, we build and deploy the OntoDocker container image on
> just the same machine.  This may, however, not work in restrictive firewalled
> environments.   If your build fails due to unsuccessful connection attempts,
> you may want to externalize the process and reimport the artifact image, as
> shown [here](faq.md).



### 4. Start OntoDocker
After successful configuration of the SSO you can start OntoDocker:

```bash
# Start OntoDocker after rebuild to ensure `client_secrets.json` is added to the image
docker-compose up -d --build

# verify OntoDocker and blazegraph are running properly
docker-compose ps
```

### 5. Connect OntoDocker to the Reverse Proxy

> **Note:** This example assumes you chose the reverse proxy with certbot.
{: .warning }

#### Add nginx Configuration

```bash
# save OntoDocker URL to shell variable
# ! Replace "ontodocker.domain.de" with the actual URL for the service
export ONTODOCKER_URL=ontodocker.domain.de

# change to pmd-server directory
cd ..

# add the nginx configuration from the template
sed "s/\[URL\]/${ONTODOCKER_URL}/" ontodocker/nginx/prod.conf > data/nginx/ontodocker.conf
```

#### Retrieve Let's Encrypt Certificate

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
