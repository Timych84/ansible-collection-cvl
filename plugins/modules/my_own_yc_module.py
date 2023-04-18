#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''
import os
import pprint
import json
# import hashlib

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        state=dict(type='str', choices=['present',
                                        'terminated',
                                        'running',
                                        'started',
                                        'stopped',
                                        'restarted',
                                        'rebooted',
                                        'absent']),
        update=dict(type='bool', required=False, default=False),
        zone=dict(type='str', required=True),
        ssh_key=dict(type='str', required=False),
        hostname=dict(type='str', required=False),
        memory=dict(type='int', required=False, default="2"),
        cores=dict(type='int', required=False, default="2"),
        core_fraction=dict(type='int', required=False, default="20", choices=[5,20,50,100]),
        public_ip=dict(type='bool', required=False, default=True),
        preemptible=dict(type='bool', required=False, default=False),
        boot_disk=dict(type='dict', options=dict(
            image_family=dict(type='str', required=False),
            image_folder_id=dict(type='str', required=False),
            size=dict(type='int', required=False, default="10"),
            type=dict(type='str', required=False, default="network-hdd"),
        )),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target

    yc_params = {
        'name': module.params['name'],
        'description': module.params['description'],
        'zone': module.params['zone'],
        'ssh-key': module.params['ssh_key'],
        'hostname': module.params['hostname'],
        'create-boot-disk': {
            'image-family': module.params['boot_disk']['image_family'],
            'image-folder-id': module.params['boot_disk']['image_folder_id'],
            'size': module.params['boot_disk']['size'],
            'type': module.params['boot_disk']['type'],
        },
        'memory': (module.params['memory']),
        'cores': module.params['cores'],
        'core-fraction': module.params['core_fraction'],
        'public-ip': module.params['public_ip'],
        'preemptible': module.params['preemptible'],
    }
    yc_args = []
    for key, value in yc_params.items():
        if isinstance(value, dict):
            yc_args.append(("--" + key))
            output = ""
            for key2, value2 in value.items():
                # output += f"{key2}={value2}," #only Python3
                output += key2 + "=" + str(value2) + ","
            output = output[:-1]
            yc_args.append(output)
        elif isinstance(value, bool):
            yc_args.append("--" + key)
        elif isinstance(value, (str, int)):
            yc_args.append("--" + key)
            yc_args.append(str(value))
            # if value in ("true", "false"):
            #     yc_args.append("--" + key)
            #     count_bool = count_bool + 1
            # else:
            #     yc_args.append("--" + key)
            #     yc_args.append(str(value))

    yc_check_installed = module.run_command(["yc",  "config", "list"], check_rc=True)
    result['yc_check_installed_rc'] = yc_check_installed[0]
    result['yc_check_installed'] = yc_check_installed

    yc_compute_instance_get = module.run_command(["yc", "compute", "instance", "get", yc_params['name'], "--format", "json"])
    result['yc_compute_instance_get'] = yc_compute_instance_get
    if yc_compute_instance_get[0] == 0:
        yc_compute_instance_info = json.loads(yc_compute_instance_get[1])


    if (module.params['state'] == 'present'):
        if (yc_compute_instance_get[0] != 0):
            yc_args.extend(["--format", "json-rest"])
            create_instance_command = "yc compute instance create"
            yc_full_command = create_instance_command.split() + yc_args + ["--format", "json"]
            yc_joined = (' '.join(yc_full_command))
            yc_result = module.run_command(yc_full_command, check_rc=True)
            result['create'] = yc_result[1]
            result['message'] = yc_result
            result['vm'] = json.loads(yc_result[1])
        else:
            if ((module.params['update'] is True) and
               ((yc_params['memory'] != int(yc_compute_instance_info['resources']['memory'])/1073741824) or
               (yc_params['cores'] != int(yc_compute_instance_info['resources']['cores'])) or
               (yc_params['core-fraction'] != int(yc_compute_instance_info['resources']['core_fraction'])))):
                result['params'] = yc_compute_instance_info['resources']
                yc_stop = module.run_command(["yc", "compute", "instance", "stop", yc_params['name']], check_rc=True)
                result['yc_stop'] = yc_stop
                yc_update = module.run_command(["yc",
                                                "compute",
                                                "instance",
                                                "update",
                                                yc_params['name'],
                                                "--memory",
                                                str(yc_params['memory']),
                                                "--cores",
                                                str(yc_params['cores']),
                                                "--core-fraction",
                                                str(yc_params['core-fraction'])],
                                               check_rc=True)
                result['yc_update'] = yc_update
                yc_start = module.run_command(["yc",
                                               "compute",
                                               "instance",
                                               "start",
                                               yc_params['name'],
                                               "--format", "json"],
                                              check_rc=True)
                result['yc_start'] = yc_start
                result['changed'] = True
            else:
                result['changed'] = False
                result['params'] = "Not changing same"

            # module.fail_json(msg=('VM exists with name: ' + yc_params['name']), **result)

    if (module.params['state'] == 'absent') or (module.params['state'] == 'terminated'):
        if (yc_compute_instance_get[0] == 0):
            yc_delete = module.run_command(["yc", "compute", "instance", "delete", yc_params['name'], "--format", "json"], check_rc=True)
            result['yc_delete'] = yc_delete
            result['changed'] = True
        else:
            module.fail_json(msg=('No VM exists with name: ' + yc_params['name']), **result)

    if (module.params['state'] == 'stopped'):
        if (yc_compute_instance_get[0] == 0) and (yc_compute_instance_info['status'] == "RUNNING"):
            yc_stop = module.run_command(["yc", "compute", "instance", "stop", yc_params['name'], "--format", "json"], check_rc=True)
            result['yc_stop'] = yc_stop
            result['changed'] = True
        else:
            module.fail_json(msg=('No VM exists with name: ' + yc_params['name']), **result)

    if (module.params['state'] == 'started'):
        if (yc_compute_instance_get[0] == 0) and (yc_compute_instance_info['status'] == "STOPPED") :
            yc_start = module.run_command(["yc", "compute", "instance", "start", yc_params['name'], "--format", "json"], check_rc=True)
            result['yc_start'] = yc_start
            result['changed'] = True
        else:
            module.fail_json(msg=('No VM exists with state STOPPED and name: ' + yc_params['name']), **result)

    if (module.params['state'] == 'restarted'):
        if (yc_compute_instance_get[0] == 0) and (yc_compute_instance_info['status'] == "RUNNING"):
            yc_restart = module.run_command(["yc", "compute", "instance", "restart", yc_params['name'], "--format", "json"], check_rc=True)
            result['yc_restart'] = yc_restart
            result['changed'] = True
        else:
            module.fail_json(msg=('No VM exists in state RUNNING with name: ' + yc_params['name']), **result)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results

    # yc_compute_instance_list = module.run_command(["yc", "compute", "instance", "list", "--format", "json"])
    # result['yc_compute_instance_list'] = yc_compute_instance_list



    # d = json.loads(yc_compute_instance_list[1])
    # names = []
    # for elem in d:
    #     if elem['name'] == yc_params['name']:
    #         result['exists'] = (elem['name'] + " exists")
    # result['names'] = names
    result['yc_joined'] = yc_joined
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
