ansible-content
=========

Simple place content to file on remote host.

Supported OS: CentOS 7

Role Variables
--------------
F: You have to specify file location.
```yaml
path: "/home/user/file.out"
```

F: You have to specify file content.
```yaml
content: "test content"
```


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
---
- name: Write content
  tags: write_content
  hosts: all
  roles:
    - timych.yandex_cloud_cvl.content
  vars:
    - path: "/home/user/file.out"
    - content: "test content"
```

License
-------

MIT

Author Information
------------------
Role by [Timur Alekseev](https://github.com/Timych84).

Dear contributors, thank you.
