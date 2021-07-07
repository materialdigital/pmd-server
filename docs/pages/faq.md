---
title: Troubleshooting/FAQ
layout: page
nav_order: 4
---

Troubleshooting/FAQ
===

{: no_toc }

## Table of Contents
{: .no_toc }

- TOC
{:toc}

## General

In general various `docker-compose` commands exist that help you troubleshoot issues you might encounter.

### `docker-compose config`
provides a summary of the configuration including all the environment variables specified in `.env` and other environment files. It also provides feedback if the current configuration has errors

### `docker-compose logs`
usually provides stderr and stdout of a container that can be used to troubleshoot various issues. You can append the servicename to see only the logs of a specific service use the `--tail` option to limit the output to the last `n` lines or add `-f` to follow the output of the container on the terminal.

**Examples:**
```bash
# list the last 100 lines of the nginx service and follow the output
docker-compose logs --tail 100 -f nginx
```

### `docker-compose exec`
you can get a shell inside a running container with `docker-compose exec`
**Examples:**
```bash
# get a shell inside the nginx container
docker-compose exec nginx sh

# get a bash shell in a container that uses an entrypoint
docker-compose exec --entrypoint=bash app

```


## Known issues
### 1. `Network pmd-reverse-proxy-net declared as external, but could not be found.`
This error is typically encountered when the reverse proxy is not running or has an incorrect network name. Make sure you started the reverse proxy by changing into the base directory and issuing `docker-compose ps`. Furthermore verify that the network name is correct by listing the existing networks using `docker network ls` and checking whether the network of the reverse proxy exists under a different name.

If you prefer to start the service before configuring the reverse proxy, you can  create the network manually as specified in the error message with: `docker network create pmd-reverse-proxy-net`

### 2. nginx fails to start with `nginx: [emerg] host not found in upstream`

This error is typically encountered if you add an nginx configuration with a `proxy_pass` directive to a service that is either not running or not connected to the nginx network, make sure your app configuration has the network specified as follows:

{% highlight yaml %}

services:
  app:
    networks:
      - proxy-net

 networks:
  proxy-net:
    name: pmd-reverse-proxy-net
    external: true

{% endhighlight %}

also make sure the service is running using `docker-compose ps` and if not bring it up using `docker-compose up -d`.
Once the service is running go back to the base dir of the reverse proxy and restart nginx using `docker-compose restart nginx`.

### 3. Externalize Image Retrieval and Build and Reinmport to the Deployment Machine.

If pulling or building your container images aborts due to failed connection
attempts, you can try to do the same on a different machine with unrestricted
access to the internet and import the images to the deployment machine.

In case pulling is problematic, do the following.  A typical
`docker-compose.yml` file looks like this:

{% highlight yaml %}
services:
  hub-db:
    image: postgres:9.5@sha256:ee604a9025ec864da512736f765ae714112a77ffc39d762c76b67ca0f8597e9e
    container_name: jupyterhub-db
{% endhighlight %}

Spot all occurrences of `image:` therein, and do a manual pull with the
image-name(s): 

```bash
docker pull postgres:9.5@sha256:ee604a9025ec864da512736f765ae714112a77ffc39d762c76b67ca0f8597e9e
```

Save the container image to some archive file: 

```bash 
docker save postgres:9.5@sha256:ee604... -o pgres9.5.tgz
```

The final step involves copying the output archive to the deployment machine.
There, import the file via:

```bash
docker load <epgres9.5.tgz
```

You can do without the intermediate archive file with only one step:

```bash
docker save  postgres:9.5@sha256:ee604... | ssh user@remote.machine "docker load"
```
