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
* Public IP4 address and an appropriate DNS entry
* Minimum Linux Kernel version 5.6. Distros with older releases may provide
  backported wireguard kernel modules.
* Wireguard kernel module (see
  [https://www.wireguard.com/install/](https://www.wireguard.com/install/))
* Docker (see [System Requirements](../index.md/#system-requirements))
* docker-compose (see [System Requirements](../index.md/#system-requirements))

### Request Certificate

* Send an email to foo@bar.org with the public domain name you reserved for the
  PMD connector to request the Wireguard certificate---you will receive a ZIp
  file containing your identity certificate and key files.

### Adjust Firewall

* Make sure your public IP can be reached via port 29292 with both UDP and TCP.

### Check IPv6 is Enabled on Your System

* Check with e.g. `sysctl net.ipv6.conf.all.disable_ipv6`, which should show 0.
  Otherwise enable it (typically with `sysctl net.ipv6.conf.all.disable_ipv6=0`
  and/or by making changes persitent with editing `/etc/sysctl.conf`).

### Check Wireguard

* Check that the wireguard kernel module is actually loaded:

```
sudo modprobe wireguard 
sudo lsmod | grep wireguard
```


###  Get the Wireguard-Mesh Repository

```
git clone [REPO_URL]
cd wireguard-mesh
```

## Automatic Setup (Recommended)

  * Place the ZIP-archive you received via email in the subdirectory `wg-mesh`.
    Change into it.
  * Run the following command in the `wg-mesh` directory:
  
  ```
  docker run --rm -v $(pwd):/composer_root -v /run/docker.sock:/run/docker.sock materialdigital/setup
  ```

  * Make sure you're up to date with the container images:
  
  ```
  docker-compose pull
  ```

  * Start the container 
  
  ```
  docker-compose up -d
  ```
  
## Troubleshooting

  * When migrating from an old installation, you may receive error messages
    like these when starting the wireguard-mesh containers via `docker-compose up`:
    
    ```
    ERROR: for init  Cannot create container for service init: Conflict. The container name "/init" is already in use by container "c82255ee2f5c1beb2177967415c81a06c798e3fa165f201b52a3af63d6c13c3b". You have to remove (or rename) that container to be able to reuse that name.
    ```
    
    In that case, try to remove the old containers with the respective container
    id:
    
    ```
    docker rm c82255ee2f5c1beb2177967415c81a06c798e3fa165f201b52a3af63d6c13c3b
    ```

<!-- ## Configure Everything to Match Your PMD-S -->

<!-- * review and adjust `config.json` -->
<!-- * create `.env` file -->
<!-- ``` -->
<!-- python ../scripts/configure.py -->
<!-- ``` -->

<!-- ### Extract the Archive File -->

<!-- * Extract the archive with Your satellite server's certificate and the private -->
<!--   key into the `/pmd_config/wg/` directory:  -->
  
<!--   ```  -->
<!--   unzip <your-host>.zip -d <directory to pmd-connector>/pmd_config/wg -->
<!--   ``` -->

<!-- * For the wg-daemon to work properly, the file `dapsRootCA.cert` must be appended -->
<!--   to the end of your certificate file: -->

<!-- ``` -->
<!--   cat dapsRootCA.cert >> <your_host>.cert -->
<!-- ``` -->

<!-- ## Start the Wireguard Container -->
<!-- ``` -->
<!-- docker-compose up -d -->
<!-- ``` -->

<!-- ## Connect to other servers -->
<!-- ``` -->
<!-- docker-compose exec wg curl http://localhost:8000/connect/[HOSTNAME]/29292 -->
<!-- ``` -->
{: .no_toc }
