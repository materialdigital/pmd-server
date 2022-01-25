---
title: Reverse Proxy
layout: default
nav_order: 1
parent: PMD Core Components
---

Reverse Proxy (nginx)
===
{: no_toc }

## Table of Contents
{: .no_toc }

- TOC
{:toc}

The reverse proxy provides a single entry point and optionally TLS encryption for all externally exposed web interfaces.


## Choosing and starting a reverse proxy configuration

### Requirements

Make sure You've cloned the repository as detailed in [PMD-S Core Components](PMD-core-components.md)

The core setup provides various compose file templates for the reverse Proxy. Choose the one that best matches your needs:
* I. Simple reverse proxy&mdash;no SSL (test environments)
* II. Reverse proxy with automatically generated Let's Encrypt certificates (Recommended)
* III. Reverse proxy with independently retrieved certificates


### I. Simple reverse proxy &mdash; no SSL
This reverse proxy provides a quick entry point for local test setups.

You can start out by copying the compose example into your main working directory.

```bash
# copy the proxy configuration
cp compose-templates/docker-compose-nginx.yml docker-compose.yml
# Add a default configuration
cp data/nginx/local.conf.template data/nginx/local.conf
```

You should than have a `docker-compose.yml` file with the following contents:

{% highlight yaml %}
version: '3.7'
services:
  nginx:
    image: nginx:1.21-alpine
    ports:
      - "80:80"
    volumes:
      - ./data/nginx:/etc/nginx/conf.d
    networks:
      - proxy-net

networks:
  proxy-net:
    name: pmd-reverse-proxy-net
    driver: bridge
{% endhighlight %}

This is all that is required. You can start the reverse proxy using `docker-compose`:
```bash
docker-compose up -d
# Check whether the service started properly
docker-compose ps
```

You should now be able to see the default landing page of the reverse proxy.

![reverse_proxy_local](https://github.com/materialdigital/deployment-guide-assets/blob/main/images/reverse_proxy_local.png?raw=true)

---

### II. Reverse proxy with automtically generated Let's Encrypt certificates (Recommended)
In order to add TLS encryption, you can use automatically generated certificates from [Let's Encrypt](https://letsencrypt.org).

**Requirements**
* Port 80 needs to be accessible from the internet.
* The nginx configuration needs to be refreshed periodically to load new certificates.


**Benefits**
* automated generation of valid certificates
* automated renewal of certificates

For this setup slight modifications of the simple compose setup are required:
1. Adjusted `command` of the nginx service to ensure new/renewed certificates are automatically loaded
2. A `certbot` service that generates and renews certificates
3. shared volumes between the `nginx` and `certbot` service that hold the acme challenge and certificates
4. An nginx configuration that serves requests to the `/.well-known/acme-challenge/` endpoint

#### Setup:

First copy the compose example into your main working directory.

```bash
# copy the proxy configuration
cp compose-templates/docker-compose-nginx-certbot.yml docker-compose.yml
```

The added settings in this compose file include

{% highlight yaml %}
services:
  nginx:
    command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"
    ports:
      - "443:443"
    volumes:
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot


  certbot:
    image: certbot/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    volumes:
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot
{% endhighlight %}

In order to serve requests for the Let's encrypt challenge, you need a simple nginx configuration

```bash
# save Server URL to shell variable
# ! Replace "pmd-s.domain.de" with the actual URL for the service
export PMD_URL=pmd-s.domain.de

# add the nginx configuration from the template
sed "s/\[URL\]/${PMD_URL}/" data/nginx/nginx_certbot.conf.template > data/nginx/site.conf
```

Next you need to adjust the configuration in the `init-letsencrypt.sh` script:

{% highlight bash %}
#!/bin/bash
set -e

# Script parameters -------------------------------------------------------------

domains=(example.com)
rsa_key_size=4096
data_path="./data/certbot"
email="info@example.com" # Adding a valid address is strongly recommended
staging=0 # Set to 1 if you're testing your setup to avoid hitting request limits


# Script - Do not change content below unless you know what you are doing -------
...
{% endhighlight %}

Open it in an editor and enter the domain name for which the certificate should be issued and an e-mail address for renewal reminders in case certbot fails to renew the certificate.

```bash
# open the letsencrypt script in your editor
vi scripts/init-letsencrypt.sh


# run the script
bash scripts/init-letsencrypt.sh

# Check if both service are indeed up and running
docker-compose ps
```

If everything executed successfully both services should be reported as `UP`:

```console
$ docker-compose ps
       Name                     Command               State                                   Ports
------------------------------------------------------------------------------------------------------------------------------------
pmd-core_certbot_1   /bin/sh -c trap exit TERM; ...   Up      443/tcp, 80/tcp
pmd-core_nginx_1     /docker-entrypoint.sh /bin ...   Up      0.0.0.0:443->443/tcp,:::443->443/tcp, 0.0.0.0:80->80/tcp,:::80->80/tcp
```


#### Test your certificate
If you would like to test whether the certificate is working properly, you can uncomment the server block listening to port 443 in `data/nginx/site.conf`:

{% highlight nginx %}
server {
    listen 443 ssl;
    server_name [URL];

    ssl_certificate /etc/letsencrypt/live/[URL]/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/[URL]/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page  404              /404.html;

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
{% endhighlight %}

Just replace the `[URL]` part with the domain for which you requested the certificate and load the updated configuration:

```bash
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```


---

### III. Reverse proxy with independently retrieved certificates
In case you prefer to use a certificate from another certificate authority or
can not make port 80 publicly available, you can also provide your own
certificates.

We use explicitly generated Diffie-Hellman parameters for the Diffie-Hellman
key-exchange. You may generate these with a command as simple as:

```bash
openssl dhparam -out dhparam.pem 4096
```

> **Note:** the time required for computing these parameters is considerable.
{: .info }

Now, assuming that the certificate including the certificate chain (`cert.pem`), private
key (`key.pem`), and Diffie-Hellman parameters (`dhparam.pem`) are all located
in an `nginx` subdirectory, you can add them to your compose file as secrets:

{% highlight yaml %}
services:
  nginx:
    secrets:
      - cert.pem
      - key.pem
      - dhparam.pem

secrets:
  cert.pem:
    file: ${CERT_PATH:-./nginx/cert.pem}
  key.pem:
    file: ${KEY_PATH:-./nginx/key.pem}
  dhparam.pem:
    file: ${DHPARAM_PATH:-./nginx/dhparam.pem}
{% endhighlight %}

The certificate are then loaded in nginx with the following directives:

{% highlight nginx %}
...

    ssl_certificate     /run/secrets/cert.pem;
    ssl_certificate_key /run/secrets/key.pem;
    ssl_dhparam         /run/secrets/dhparam.pem;
...
{% endhighlight %}

Setting up the reverse proxy thus only requires a few simple steps:

Make sure that the nginx-subdirectory exists and is populated with the
following files:

```console
~/pmd-server$ ls nginx
cert.pem  dhparam.pem  key.pem
```

Then, copy the nginx configuration from the template by replacing occurrences of a placeholder string (`[URL]`) with your
 actual virtual host name, for instance, `foo.bar.org`:

```bash
sed "s/[URL]/foo.bar.org/" data/nginx/nginx_ssl.conf.template > data/nginx/nginx_ssl.conf
```

Finally:
```bash
# copy the proxy compose file
cp compose-templates/docker-compose-nginx-ssl.yml docker-compose.yml

# start the service
docker-compose up -d

# Check whether the service started properly
docker-compose ps
```


## Connecting services to the running reverse proxy

> **Note:** this section just explains how a generic app can be incorporated,
and does not represent a working example. If you are interested in a real
example follow the OntoDocker or pyiron section.  
{: .info }

Assuming the service is to be incorporated under the domain name pmd-app.mydomain.de via a `proxy_pass` to port 8000 and has this minimal compose file:

{% highlight yaml %}
version: '3.7'
services:
  pmd-app:
    image: pmd-app:latest
{% endhighlight %}
You only need to connect your service to the network of the reverse proxy by extending the compose file as follows:
{% highlight yaml %}
version: '3.7'
services:
  pmd-app:
    image: pmd-app:latest
    networks:
      - proxy-net

networks:
  proxy-net:
    name: pmd-reverse-proxy-net
    external: true
{% endhighlight %}


Once you have adjusted the compose file bring up the service using docker compose:

```bash
cd [path_to_pmd_app]
docker-compose up -d
cd [path to pmd-server]
```

You can now generate the certificate for pmd-app.mydomain.de using certbot:

```bash
docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d pmd-app.mydomain.de
```

After the certificate has been created you can add the nginx configuration of the service to `data/nginx/pmd-app.conf`:

{% highlight nginx %}
# pmd-app.conf:

server {
    listen 443 ssl;
    server_name pmd-app.mydomain.de;

    ssl_certificate /etc/letsencrypt/live/pmd-app.mydomain.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pmd-app.mydomain.de/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://pmd-app:8000;
    }
}
{% endhighlight %}

Finally the new configuration just needs to be loaded by nginx to handle requests to the new service. If the reverse proxy is used for other services as well, it is however advisable to test the new configuration before reloading nginx.

```bash
# Test the new configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload
```

###### tags: `PMD Deployment guide`
{: .no_toc }
