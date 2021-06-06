---
title: 'Keycloak'
---

Local SSO instance (Keycloak)
===

[<i class="fa fa-arrow-circle-left"></i> Previous](https://hackmd.io/@materialdigital/H1t3_GQ9O)

## Table of Contents

[TOC]

## Setup
You can setup your own keycloak instance using the provided templates from the [PMD-Server repo](https://github.com/materialdigital/pmd-server).

### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](https://hackmd.io/@materialdigital/HJwVOfQ5_)
* Running reverse proxy as described under - [Reverse Proxy](https://hackmd.io/@materialdigital/H1t3_GQ9O) 


### 1. Copy the template files
```bash=
# create separate directory 
mkdir keycloak

# copy the compose and config templates
cp compose-templates/docker-compose-keycloak.yml keycloak/docker-compose.yml
cp config-templates/keycloak_config.json keycloak/

# change into Keycloak direcory
cd keycloak
```

### 2. Configure the service
After copying the templates you should view and adjust the configuration (`config.json`):
```json
{
  "shared": {
    "db_password": "[db password]",
    "db_name": "keycloak",
    "db_user": "keycloak"
  },
  "keycloak.env": {
    "DB_VENDOR": "POSTGRES",
    "DB_ADDR": "keycloak_db",
    "DB_DATABASE": "shared:db_name",
    "DB_USER": "shared:db_user",
    "DB_SCHEMA": "public",
    "DB_PASSWORD": "shared:db_password",
    "KEYCLOAK_USER": "admin",
    "KEYCLOAK_PASSWORD": "[password]"
  },
  "keycloak_db.env": {
    "POSTGRES_DB": "shared:db_name",
    "POSTGRES_USER": "shared:db_user",
    "POSTGRES_PASSWORD": "shared:db_password"
  }
}
```
Make sure to set custom passwords for the database and the Keycloak admin user by replacing `[db password]` and `[password]` before you continue and start the service.

### 3. Start the service
```bash=+
# create environment files from config
python ../scripts/configure.py

# start the keycloak service
docker-compose up -d
# check if the service is up and running
docker-compose ps
```

### 4. Make the service available by adding it to the reverse proxy
Finally, you just need to add the service to the reverse proxy to make it available. 
:::info
This section assumes you are using Let's Encrypt certificates. If you want to use your own certificates, skip the "certificate generation" part and adjust the paths to the certificates accordingly, as described under [Reverse Proxy configuration](https://hackmd.io/@materialdigital/H1t3_GQ9O)
:::

First you need to change back to the `pmd-server` directory
```bash=+
cd ..
```
#### certificate generation
You can now generate the certificate for the service using certbot:

```bash=+
docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d [KEYCLOAK_URL]
```

After the certificate has been created you can add the nginx configuration:
```bash=+
# copy the nginx template
cp data/nginx/keycloak.conf.template data/nginx/keycloak.conf

# Ajust the template 
vi data/nginx/keycloak.conf
```

Finally the new configuration just needs to be loaded by nginx:

```bash=
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### 5. Test Your SSO-Instance

Once completed you should now be able to acceess Keycloak under the `[KEYCLOAK_URL]` and login with the credentials from the configuration (`KEYCLOAK_USER` and `KEYCLOAK_PASSWORD`).

![keycloak landing page](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/local_sso.png?raw=true)

[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/rJKjpvmc_)

###### tags: `PMD Deployment guide`