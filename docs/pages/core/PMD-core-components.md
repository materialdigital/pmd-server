---
title: PMD Core Components
layout: default
nav_order: 2
has_children: true
has_toc: false
---

PMD Core components
===

[![hackmd-github-sync-badge](https://hackmd.io/SYBY8yRPRrq0hyx-fqyi2g/badge)](https://hackmd.io/SYBY8yRPRrq0hyx-fqyi2g)

The initial PMD instance setup currently includes the following components:

* [Reverse Proxy (nginx)](reverse_proxy.md) including an optional SSL-Certificate Service (certbot)
* [UserManagement (Keycloak - optional in the standalone context)](keycloak.md)

## Clone the core repository

In order to establish a base configuration clone the PMD server repository and change into it.

```bash
# clone the repo and change into it
git clone https://github.com/materialdigital/pmd-server.git
cd pmd server
```


###### tags: `PMD Deployment guide`
