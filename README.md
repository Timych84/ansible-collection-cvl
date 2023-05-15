Documentation for the collection.
# Clickhouse - Vector - Lighthouse Ansible collection for Yandex Cloud using yc command line tool

Modules:
- Content
- Yandex command line tool

Roles:
- Lighthouse
- Vector

**Table of Contents**

- [Zabbix collection for Ansible](#zabbix-collection-for-ansible)
  * [Introduction](#introduction)
  * [Included content](#included-content)
  * [Installation](#installation)
    + [Requirements](#requirements)
    + [Installing the Collection from Ansible Galaxy](#installing-the-collection-from-ansible-galaxy)
    + [Upgrading collection](#upgrading-collection)
  * [Usage](#usage)
  * [Supported Zabbix versions](#supported-zabbix-versions)
  * [Collection life cycle and support](#collection-life-cycle-and-support)
  * [Contributing](#contributing)
  * [License](#license)

## Introduction

This repo hosts the `timych.yandex_cloud_cvl` Ansible Collection.

The collection includes modules and roles to deploy Clickhouse-Vector-Lighthouse stack.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Modules**:
    - [Content](https://docs.ansible.com/ansible/latest/collections/community/zabbix/zabbix_action_module.html)
    - [yc](https://docs.ansible.com/ansible/latest/collections/community/zabbix/zabbix_authentication_module.html)
  - **Roles**:
    - [Lighthouse](docs/ZABBIX_AGENT_ROLE.md)
    - [Vector](docs/ZABBIX_JAVAGATEWAY_ROLE.md)

## Installation

### Requirements

Each component in this collection requires additional dependencies. Review components you are interested in by visiting links present in the [Included content](#included-content) section.

This is especially important for some of the Zabbix roles that require you to **install additional standalone roles** from Ansible Galaxy.

For the majority of modules, however, you can get away with just:

```bash
pip install zabbix-api
```
#### Ansible 2.10 and higher

With the release of Ansible 2.10, modules have been moved into collections.  With the exception of ansible.builtin modules, this means additonal collections must be installed in order to use modules such as seboolean (now ansible.posix.seboolean).  The following collections are now frequently required: `ansible.posix` and `community.general`.  Installing the collections:

```bash
ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.netcommon
```
### Installing the Collection from Ansible Galaxy

Before using the Zabbix collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install community.zabbix
```

You can also include it in a `requirements.yml` file along with other required collections and install them via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.zabbix
    version: 1.9.3
  - name: ansible.posix
    version: 1.3.0
  - name: community.general
    version: 3.7.0
```

### Upgrading collection

Make sure to read [UPGRADE](docs/UPGRADE.md) document before installing newer version of this collection.

## Usage

To use a module or role from this collection, reference them with their Fully Qualified Collection Namespace (FQCN) like so:

```yaml
---
- name: Using Zabbix collection to install Zabbix Agent
  hosts: localhost
  roles:
    - role: community.zabbix.zabbix_agent
      zabbix_agent_server: zabbix.example.com
      ...

- name: If Zabbix WebUI runs on non-default (zabbix) path, e.g. http://<FQDN>/zabbixeu
  set_fact:
    ansible_zabbix_url_path: 'zabbixeu'

- name: Using Zabbix collection to manage Zabbix Server's elements with username/password
  hosts: zabbix.example.com
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 80
    ansible_httpapi_use_ssl: false  # Set to true for HTTPS
    ansible_httpapi_validate_certs: false  # For HTTPS et to true to validate server's certificate
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
  tasks:
    - name: Ensure host is monitored by Zabbix
      community.zabbix.zabbix_host:
        ...

- name: Using Zabbix collection to manage Zabbix Server's elements with authentication key
  hosts: zabbix.example.net
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 80
    ansible_httpapi_use_ssl: false  # Set to true for HTTPS
    ansible_httpapi_validate_certs: false  # For HTTPS set to true to validate server's certificate
    ansible_zabbix_auth_key: 8ec0d52432c15c91fcafe9888500cf9a607f44091ab554dbee860f6b44fac895
  tasks:
    - name: Ensure host is monitored by Zabbix
      community.zabbix.zabbix_host:
        ...
```

Or you include collection name `community.zabbix` in the playbook's `collections` element, like this:

```yaml
---
- name: Using Zabbix collection
  hosts: localhost
  collections:
    - community.zabbix

  roles:
    - role: zabbix_agent
      zabbix_agent_server: zabbix.example.com
      ...

- name: Using Zabbix collection to manage Zabbix Server's elements with username/password
  hosts: zabbix.example.com
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 80
    ansible_httpapi_use_ssl: false  # Set to true for HTTPS
    ansible_httpapi_validate_certs: false  # For HTTPS et to true to validate server's certificate
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
  tasks:
    - name: Ensure host is monitored by Zabbix
      zabbix.zabbix_host:
        ...

- name: Using Zabbix collection to manage Zabbix Server's elements with authentication key
  hosts: zabbix.example.net
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 80
    ansible_httpapi_use_ssl: false  # Set to true for HTTPS
    ansible_httpapi_validate_certs: false  # For HTTPS et to true to validate server's certificate
    ansible_zabbix_auth_key: 8ec0d52432c15c91fcafe9888500cf9a607f44091ab554dbee860f6b44fac895
  tasks:
    - name: Ensure host is monitored by Zabbix
      zabbix_host:
        ...
```

If Basic Authentication is required to access Zabbix server add following variables:
```
zabbix_api_http_user: "user"
zabbix_api_http_password: "password"
```

## Supported Zabbix versions

Main priority is to support Zabbix releases which have official full support from Zabbix LLC. Please checkout the versions at [Zabbix Life Cycle & Release Policy](https://www.zabbix.com/life_cycle_and_release_policy) page.

> We aim to cover at least two LTS releases. For example, currently we support LTS 4.0 + 5.0 and with LTS 6.0 we will drop 4.0. But we do our best to also include the latest point releases - for example currently this is 5.4 which should be supperseeded by 6.2 then.

Support for Zabbix LTS versions will be dropped with Major releases of the collection and mostly affect modules. Each role is following its unique support matrix. You should always consult documentation of roles in *docs/* directory.

If you find any inconsistencies with the version of Zabbix you are using, feel free to open a pull request or an issue and we will try to address it as soon as possible. In case of pull requests, please make sure that your changes will not break any existing functionality for currently supported Zabbix releases.

## Collection life cycle and support

See [RELEASE](docs/RELEASE.md) document for more information regarding life cycle and support for the collection.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information about how to contribute to this repository.

Please also feel free to stop by our [Gitter community](https://gitter.im/community-zabbix/community).

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) to see the full text.
