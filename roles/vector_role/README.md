ansible-vector
=========

Simple Vector deploy with demo connect to Clickhouse.

Activate two demo sources:
- demo_logs
- journald

And two demo sinks:
- test_console for demo_logs
- clickhouse_syslog for journald


Role Variables
--------------
F: You can specify a particular version.
```yaml
vector_version: "0.27.0"
```

F: You have to set IP address for Clickhouse sink
```yaml
clickhouse_ipaddress: "192.168.171.221"
```
F: You can change vector config file:
```yaml
vector_config:
  sources:
    dummy_logs:
      type: demo_logs
      format: syslog
      interval: 5
    journald_src:
      type: journald
      current_boot_only: true
      since_now: false
  sinks:
    test_console:
      type: console
      inputs:
        - dummy_logs
      encoding:
        codec: json
    clickhouse_syslog:
      type: clickhouse
      inputs:
        - journald_src
      endpoint: "http://{{ clickhouse_ipaddress }}:8123"
      database: "logs"
      table: "syslogd"
      skip_unknown_fields: true
      healthcheck: false
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
- name: Install Vector
  hosts: vector
  vars:
    clickhouse_ipaddress: "192.168.171.221"
  roles:
    - vector-role
```

License
-------

MIT

Author Information
------------------
Role by [Timur Alekseev](https://github.com/Timych84).

Dear contributors, thank you.
