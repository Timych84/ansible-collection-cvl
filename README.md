Documentation for the collection.
# Clickhouse - Vector - Lighthouse Stack Ansible collection for Yandex Cloud. Deploy using yc command line tool

**Table of Contents**

* [Introduction](#introduction)
* [Included content](#included-content)
    + [Modules](#modules)
    + [Roles](#roles)
    + [Playbooks](#playbooks)
* [Installation](#installation)
* [Requirements](#requirements)
* [Usage](#usage)

## Introduction

This repo hosts the `timych.yandex_cloud_cvl` Ansible Collection.

The collection includes modules and roles to deploy Clickhouse-Vector-Lighthouse stack.

## Included content

Click on the name of a plugin or module to view that content's documentation:

### Modules:
  - Content
      - Module for writing content to file
  - yc
      - Module for working with Yandex cloud compute instances
### Roles:
  - lighthouse_role
      - Simple lighthouse deployment
  - vector_role
      - Simple Vector deployment

### Playbooks:
  - Sample playbooks for using included modules and roles

## Installation

You can install collection using commands:.

```bash
ansible-galaxy collection install git+https://github.com/Timych84/ansible-collection-cvl.git
ansible-galaxy collection install git@github.com:Timych84/ansible-collection-cvl.git
```


For Clickhouse-Vector-Lighthouse stack you have to install Clickhouse role:
[https://github.com/AlexeySetevoi/ansible-clickhouse.git](https://github.com/AlexeySetevoi/ansible-clickhouse.git)

Requred role placed in the "requirements.yml" file in "playbooks" folder.

## Requirements
Ansible 2.10 and higher

## Usage
To use module for creating file with specified content use "Content" role, example playbook:

```yml
---
- name: Write content
  tags: write_content
  hosts: all
  roles:
    - timych.yandex_cloud_cvl.content
  vars:
    - path: "/home/timych/timych/testfile5.txt"
    - content: "test\ncontent2"
    - force: false
```

To deploy Clickhouse-Vector-Lighthouse stack use these files in playbook folder:
- create_site.yml
    - Playbook that creates 3 compute instances on Yandex Cloud and installs Clickhouse-Vector-Lighthouse stack on them
        - clickhouse-01 - Clickhouse instance with sample logs database and syslogd table in it for recieving syslogd entries from Vector
        - vector-01 - Instance with Vector, sending syslogd entries to Clickhouse
        - lighthouse-01 - Instance with Lighthouse to visualise Clickhouse queries
    - After execution it creates gen_inv.yml inventory file containing all created hosts
- destroy_site.yml
    - Playbook that destroys compute instances
- HostsFile.j2
    - Template file for gen_inv.yml inventory file
- inventory.yml
    - Initial inventory file
- requirements.yml
    - Contain required Clickhouse role
- clickhouse.yml
    - Clickhouse initial configuration variables and query that creates sample table for syslogd entries
Note: yc client should be configured on ansible host.

If you intend to use yc module for manage Yandex Cloud compute instances, you can use yc module. Example playbooks placed in playbooks folder.
