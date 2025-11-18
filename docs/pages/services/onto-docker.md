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

ontodocker is a Flask application-prototype to access a Blazegraph and Jena Fuseki instance via a GUI and an API.

API authentication via JWT and OIDC.
Allowed Content-Types to upload are "text/turtle" and "application/rdf+xml" as .ttl/.rdf files

## Setup
### Requirements
* working directory is base directory of the PMD-Server repo as described under [PMD-S Core](PMD-core-components.md})
* Running reverse proxy as described under - [Reverse Proxy](reverse_proxy.md)

### 1. Clone the repository

```bash
git clone https://github.com/materialdigital/ontodocker.git
cd ontodocker
```
Follow the instructions in the `README.md`. 


[Next <i class="fa fa-arrow-circle-right"></i>](https://hackmd.io/@materialdigital/H1P_XW7qO)


###### tags: `PMD Deployment guide`
{: .no_toc }
