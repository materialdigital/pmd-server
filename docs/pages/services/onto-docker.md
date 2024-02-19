---
title: ontodocker
nav_order: 1
parent: PMD-S Services
---

ontodocker
===
{: .no_toc }

## Table of Contents
{: .no_toc }

- TOC
{:toc}

## Description

ontodocker is a Flask application to access a Blazegraph and Jena instance via a GUI and an API.

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
#### Create an environment file
In order to connect your ontodocker to the IDP you must create a `.env` file with the folloewing contents and store it in the root folder after cloning the respository.

```lines=-1
ADMIN_EMAIL=ab@c.de
JWT_SECRET_KEY=
JWT_DAYS_VALID=90
FUSEKI_ADMIN_USER=admin
FUSEKI_ADMIN_PW=admin
KEYCLOAK_URL=
KEYCLOAK_CLIENT_ID=
KEYCLOAK_CLIENT_SECRET=
```

Set `KEYCLOAK_URL`, `KEYCLOAK_CLIENT_ID` and `KEYCLOAK_CLIENT_SECRET` accordingly to the IDPs properties.

Set `JWT_SECRET_KEY` to a random alphanumeric value (for example by using `openssl rand -hex 48`).

Change the `FUSEKI_ADMIN` password it here in the `docker-compose-prod.yml` file as well.

Change the `ADMIN_EMAIL` and `JWT_DAYS_VALID` as desired.

##### docker-compose.yml

If you want to use docker volumes instead of bind mounts, change it as desired in the docker-compose-prod.yml.

Create a symlink in the repository's root directory via

```bash
# Create a symlink
ln -s docker-compose-prod.yml docker-compose.yml
```

Build the container:
```bash
# Build the containers
docker compose build
```

### 3. Start ontodocker
After successful build you can start the container:

```bash
# Start ontodocker
docker compose up -d

# verify ontodocker, jena fuseki and blazegraph are running properly
docker compose ps

# check the logs 
docker compose logs -f
```

### 5. Connect ontodocker to the reverse proxy

> **Note:** This example assumes you chose the reverse proxy with certbot.
{: .warning }

#### Add nginx configuration

```bash
# save ontodocker URL to shell variable
# ! Replace "ontodocker.domain.de" with the actual URL for the service
export ONTODOCKER_URL=ontodocker.domain.de

# change to pmd-server directory
cd ..

# add the nginx configuration from the template
sed "s/\[URL\]/${ONTODOCKER_URL}/" ontodocker/prod.conf > data/nginx/ontodocker.conf
```

#### Retrieve Let's Encrypt certificate

```bash

docker compose exec certbot certbot certonly --webroot -w /var/www/certbot -d ${ONTODOCKER_URL}
```

#### Test and load the configuration
```bash
# Test the new configuration
docker compose exec nginx nginx -t

# Reload nginx
docker compose exec nginx nginx -s reload
```

### 6. Test Installation

Open your browser and navigate to the URL of your ontodocker installation. If the installation succeeded you should now be redirected to the SSO Login Screen and after successful authentication and clicking on a Tensile Tests Example Dataet you see the following page:

![](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/ontodocker.png?raw=true)

## Usage

Create new datasets by adding a Title in the corresponding "New Title" field and click "Add".

Excecute SPARQL queries via the "Query" and "Update" Buttons.

Destroy the Dataset permanatly by clicking "Destroy".

Upload RDF or TURTLE files by clicking "Upload File".

Refer to [`api_usage_examples.py`](https://git.material-digital.de/apps/ontodocker/-/blob/master/api_usage_examples.py) for examples on how to use the API.


Graph visualization via WebVOWL 1.1.7

If the visualization doesn't load, clear the browsers cache and refresh the page.


[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/H1P_XW7qO)


###### tags: `PMD Deployment guide`
{: .no_toc }
