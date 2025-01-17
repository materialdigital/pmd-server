---
title: Wireguard-Mesh
layout: default
nav_order: 3
parent: PMD Core Components
---

Wireguard-Mesh
===
{: .no_toc }

## Table of Contents
{: .no_toc }

- TOC
{:toc}



## Requirements
* Public IPv4 address and a corresponding public DNS
* Linux Kernel version 5.6 or wireguard kernel modules installed. (see
  [https://www.wireguard.com/install/](https://www.wireguard.com/install/))
* Docker (see [System Requirements](../index.md/#system-requirements))
* docker-compose (see [System Requirements](../index.md/#system-requirements))

### Request Certificate

Please send your request for a PMD-S certificate via our contact form (login required!) [https://www.material-digital.de/contact/?subject=Netzwerk-+und+Sicherheitsarchitektur](https://www.material-digital.de/contact/?subject=Netzwerk-+und+Sicherheitsarchitektur).

If the direct link above does not work, go to [https://material-digital.de/contact/](https://material-digital.de/contact/), log in and choose the subject "Network and security architecture".

Your request MUST include at least the following information:
  - The public (sub)domain which points to your PMD-S' public IPv4 address
  - Your country code (DE, FR, UK, US etc.)
  - Name of your company/institute (Fraunhofer ABC, KIT, BAM etc.)
  - Name of your business unit (IT, Materials Department etc.)

If everything is alright, you will receive a ZIP file containing your identity certificate and key file.

### Adjust Firewall

* Make sure your public IP can be reached via **port 29292** for **both UDP and TCP**.

### Check IPv6 is Enabled on Your System

* Check with e.g. `sysctl net.ipv6.conf.all.disable_ipv6`, which should show 0.
  Otherwise enable it (typically with `sysctl net.ipv6.conf.all.disable_ipv6=0` and by making changes persistent through editing `/etc/sysctl.conf`).

### Check Wireguard (Kernels < 5.6 only!)

* When using a **kernel version < 5.6**, check that the wireguard kernel module is available and loaded:

```
sudo modprobe wireguard 
sudo lsmod | grep wireguard
```

### Get the Repository

If not done yet, download/clone this (`pmd-server`) repository on your PMD-S.

```
git clone https://github.com/materialdigital/pmd-server.git
cd pmd-server
```

## Setup

### Automatic Setup using PMD Setup Container
- Change (`cd`) into the mesh directory (i.e. `wg-mesh`).
- *When migrating from an old setup, do `docker compose down` to stop the currently running mesh containers and remove the old Docker network via `docker network rm wgnet`.*
- Run `docker run --rm --pull always -v $(pwd):/composer_root -v /run/docker.sock:/run/docker.sock -e IEK=<your-iek-uuid> materialdigital/setup` from within this directory.
- Check the output for setup warnings and resolve them accordingly.

<details>
<summary>Example result</summary>

```
Status: Downloaded newer image for materialdigital/setup:latest
Performing initial enrollment via EST...
Establish trust into PMD CA...
The CA fingerprint was successfully checked, trust anchor has been established.
Generating private key and certificate signing request (CSR)...
-----
Performing EST enrollment request...
Certificate acquired, enrollment successful!
Executing configuration script...
DEBUG - Client Assertion Payload: {"iss":"...", ...,"aud":"https://daps.material-digital.de"}
DEBUG - Client Assertion (encoded): ...
DEBUG - Access Token: ...
Retrieving OpenID Config from https://daps.material-digital.de/.well-known/openid-configuration...
Retrieving JWKS from https://daps.material-digital.de/jwks.json...

### THIS IS YOUR PMD CONFIGURATION: ###
PMDC_SUBNET_PREFIX=xxxx:x:x:x::
WG_ENDPOINT=pmd-s.open-semantic-lab.org:29292
SUBNET_PREFIX=xxxx:x:x:x::
PMD_ZONE=xxx.pmd.internal
CA_FP=xxx

Sourcing newly created .env file...

Setting up docker network for PMD mesh...
PMD mesh Docker network created with ID "xxx"
```
</details>

### Manual Setup (NOT Recommended!)
- Obtain your identity certificate/key files from https://daps.material-digital.de, place them under `pmd_config/wg/` and name them `participant.{crt/key}`. Make sure that `participant.crt` contains the full chain (cert, sub-ca and ca, in that order). Additionally, place the root certificate in `pmd_config/wg/root.crt`.
- Create the wgnet Docker network with `docker network create --ipv6 --subnet=172.31.0.0/16 --subnet=<your-wg-mesh-subnet> wgnet`, using the IPv6 subnet which has been assigned to you.
- Create/edit the `.env` file, and adapt `WG_ENDPOINT`, `SUBNET_PREFIX` and `PMD_ZONE` to the values which have been assigned to you. You should normally not alter the `PMDC_SUBNET_PREFIX` variable.
- *In case subnet `172.31.0.0/16` has not been available, you also have to specify `IPV4_DNS_IP` (IPv4 IP of DNS service) and `IPV4_SUBNET` (IPv4 subnet of `wgnet` in CIDR notation).*

## Usage

When properly set up, you should be able to start your mesh via `docker compose pull && docker compose up -d`.
*(The `docker compose pull &&` part is optional but strongly recommended to make sure that you don't use any outdated images.)*

If you also want to start a demo app container for testing, run `docker compose --profile debug up -d`.
(This requires that you launch the commands from the PMD mesh git repository with the corresponding `Dockerfile`.)

Run `curl http://localhost:8000/connect/<DOMAIN>/<PORT>` on the host (assuming the wireguard container `materialdigital/wg` has exposed port 8000) to connect to another mesh participant.
<details>
<summary>Example result</summary>
  
```
peer: WireGuardPeerConfig { endpoint: "<DOMAIN>:<PORT>", subnet: "xxxx:x:x:x::/xx", pub_key: "xxx" }, dat: ...
```
</details>

Run `wg` within the wireguard container (`materialdigital/wg`) to list all active connections. 
<details>
<summary>Example result</summary>
  
```
interface: wg0
  public key: xxx/xxx
  private key: (hidden)
  listening port: xxxxx

peer: XXX (e.g. PMD-C)
  endpoint: xxx.xxx.xxx.xxx:xxxxx
  allowed ips: xxxx:x:x:x::/xx
  latest handshake: 1 minute, 21 seconds ago
  transfer: 8.16 KiB received, 8.23 KiB sent
  persistent keepalive: every 25 seconds

peer: XXX (e.g. another institute)
  endpoint: xxx.xxx.xxx.xxx:xxxxx
  allowed ips: xxxx:x:x:x::/xx
  latest handshake: 1 minute, 30 seconds ago
  transfer: 220 B received, 180 B sent
  persistent keepalive: every 25 seconds
```
</details>

To test the connection the an exposed service of another participant run, e.g. within your app container, `ping <APP-NAME>.<PARTICIPANT>.pmd.internal` .

### Adding Services (Docker Containers) to the Mesh

In order to join the PMD mesh, containers have to fulfill a few requirements:
- IPv6 has to be enabled, typically via `--sysctl net.ipv6.conf.all.disable_ipv6=0` or in `compose.yml` files via the `sysctl` section.
- In order to resolve PMD mesh domains, the local PMD DNS server has to be specified. This can be done in `compose.yml` files via the `dns` section of the service, or via the `--dns` switch when using the docker CLI. It is recommended to specify both the IPv4 (normally `172.31.53.53`) and IPv6 (normally `<your-wg-mesh-subnet-prefix>::fe`) address. (You should find your IPv6 prefix in your `.env` file after a successful setup.)

For a docker compose service definition example, see the `app` service in the `compose.yml` of this setup.

When all requirements are met, containers can be added to the mesh in these two ways:
- Using the docker compose CLI plugin, you can leverage the example `app` service (see `compose.yml`) as a template, add the external `wgnet` network to your `networks` section and the service in your `compose.yml`, and start added/modified services via `docker compose up -d`.
- Using the CLI or other tools, when properly configured, you can add the container to the `wgnet` via `docker network connect wgnet <container-id/name>`. As this is more error-prone, please check mesh connectivity and DNS resolution carefully according to the requirements mentioned above.

#### wgnet Containers DNS

In a properly working setup, each container added to `wgnet` will **automatically receive a PMD DNS entry**.
Assuming your DNS zone reads `participant.pmd`, and the name of the container added to `wgnet` is `_my.awesome_container_.123.`, the container will be available as `my-awesome-container-123.participant.pmd`.

The mapping of names happens as follows:
- All sequences of characters which are not latin characters (A-Z and a-z) or numbers (0-9), are replaced by a single minus (`-`) character.
- Minuses at the beginning or end of the sequence are discarded.

**Warning:** Please beware, that container names **mapping to the same sequence** can cause **unexpected behavior!** Later containers may override former ones, and especially removal of a container will cause the corresponding DNS entries to be discarded, whereas the entry of a former container will not be restored!


###### tags: `PMD Deployment guide`
{: .no_toc }
