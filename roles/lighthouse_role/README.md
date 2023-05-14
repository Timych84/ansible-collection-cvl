ansible-lighthouse
=========

Simple Lighthouse deploy.

Supported OS: CentOS 7

Configuring: Firewalld service and set SElinux context


Role Variables
--------------
F: You can specify git hash for a particular version.
```yaml
git_version_hash: "d701335"
```

F: You can set location if Lighthouse Nginx site
```yaml
document_root: /var/www/html
app_root: lighthouse
```


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
- name: Install lighthouse
  tags: lighthouse_install
  become: true
  hosts: lighthouse
  roles:
    - lighthouse-role
```

License
-------

MIT

Author Information
------------------
Role by [Timur Alekseev](https://github.com/Timych84).

Dear contributors, thank you.
