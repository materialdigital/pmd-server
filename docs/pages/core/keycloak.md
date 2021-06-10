---
title: 'Keycloak'
layout: default
nav_order: 2
parent: PMD Core Components
---

Local SSO instance (Keycloak)
===
{: .no_toc }

[![hackmd-github-sync-badge](https://hackmd.io/MmiYyp4fRhiykoY7St4GQw/badge)](https://hackmd.io/MmiYyp4fRhiykoY7St4GQw)

## Table of Contents
{: .no_toc }

- TOC
{:toc}

## Setup
You can setup your own keycloak instance using the provided templates from the [PMD-Server repo](https://github.com/materialdigital/pmd-server).

### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](https://hackmd.io/@materialdigital/HJwVOfQ5_)
* Running reverse proxy as described under - [Reverse Proxy](https://hackmd.io/@materialdigital/H1t3_GQ9O)


### 1. Copy the template files
```bash
# create separate directory
mkdir keycloak

# copy the compose templates
cp compose-templates/docker-compose-keycloak.yml keycloak/docker-compose.yml
# generate random passwords and insert them into the template config
PASS_STR="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c"${1:-128}")"
sed -e "s/\[password\]/${PASS_STR:0:64}/" -e "s/\[db password\]/${PASS_STR:64}/" config-templates/keycloak_config.json > keycloak/config.json

# change into Keycloak directory
cd keycloak
```

### 2. Configure the service
After copying the templates you should view and if necessary adjust the configuration (`config.json`):
{% highlight json %}
{
  "shared": {
    "db_password": "[db password]",
    "db_name": "keycloak",
    "db_user": "keycloak"
  },
  "keycloak.env": {
    "DB_VENDOR": "POSTGRES",
    "DB_ADDR": "keycloak-db",
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
{% endhighlight %}

Make sure to to verify that custom passwords have been inserted for the database and the Keycloak admin user (`[db password]` and `[password]`) before you continue and start the service.

### 3. Start the service

> **Note:** In case your python version is not >=3.5, you can also run the `configure.py`
script within a docker container
```bash
`docker run --rm -v $PWD/:/tmp/ -v $PWD/../scripts/configure.py:/tmp/configure.py -w /tmp python:3-alpine python configure.py`
```
{: .bg-grey-lt-200 .py-2 .px-4 }


```bash
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
```bash
cd ..
```
#### certificate generation
You can now generate the certificate for the service using certbot:

```bash
docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d [KEYCLOAK_URL]
```

After the certificate has been created you can add the nginx configuration:
```bash
# save KeyCloak URL to shell variable
# ! Replace "sso.domain.de" with the actual URL for the service
export KEYCLOAK_URL=sso.domain.de

# add the nginx configuration from the template
sed "s/\[URL\]/${KEYCLOAK_URL}/" data/nginx/keycloak.conf.template > data/nginx/keycloak.conf

# Check and adjust the template if necessary
vi data/nginx/keycloak.conf
```

Finally the new configuration just needs to be loaded by nginx:

```bash
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### 5. Test Your SSO-Instance

Once completed you should now be able to access Keycloak under the `[KEYCLOAK_URL]` and login with the credentials from the configuration (`KEYCLOAK_USER` and `KEYCLOAK_PASSWORD`).

![keycloak landing page](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/local_sso.png?raw=true)



###### tags: `PMD Deployment guide`
{: .no_toc }
{: .no_toc }
