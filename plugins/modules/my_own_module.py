#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Module for writing content to file

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description:  Module for writing content to file

options:
    path:
        description:
        - Remote absolute path of file to write content.
        type: path
        required: yes
    content:
        description:
        - Content to write to file.
        type: str
        required: yes
    force:
        description:
        - Influence whether the remote file must always be replaced.
        - If C(true), the remote file will be replaced when contents are different than the source.
        - If C(false), the content will be written only if the destination does not exist.
        type: bool
        default: false
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Timur Alekseev (@Timych84)
'''

EXAMPLES = r'''
# Write some content into remote file if remote file not exists
- name: Write some content
  timych.yandex_cloud_cvl.my_own_module:
    path: "/home/user/myfile.txt"
    content: "my new content"
# Write some content into remote file even if file exists and have different content
- name: Write some content
  timych.yandex_cloud_cvl.my_own_module:
    path: "/home/user/myfile.txt"
    content: "my new content"
    force: true
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
file_exists:
    description: File exists on target sytem
    type: bool
    returned: always
    sample: true
same_content:
    description: File have same content on target system
    type: bool
    returned: always
    sample: true
target_content:
    description: Content shoud be written to target
    type: str
    returned: always
    sample: 'test content'
'''
import os
# import hashlib

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        force=dict(type='bool', default=False)
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
    result['file_exists'] = os.path.exists(module.params['path'])
    result['target_content'] = module.params['content']
    # If file exists and force not true check that content in query and in file same
    if (os.path.exists(module.params['path']) and module.params['force'] is False):
        # Usinig read all content from file and compare with content on query
        try:
            with open(module.params['path'], 'r') as file:
                file_content = file.read()
                if file_content == module.params['content']:
                    result['changed'] = False
                    result['same_content'] = True
                    module.exit_json(**result)
                else:
                    result['changed'] = False
                    result['same_content'] = False
                    module.exit_json(**result)
        except Exception as e:
            module.fail_json(msg='Error reading existing file: %s' % e, **result)
        # Using compare with hash of contens(slower)
        # content_hash = hashlib.sha1(module.params['content'].encode()).hexdigest()
        # try:
        #     with open(module.params['path'], 'rb') as file:
        #         file_content = file.read()
        #         file_hash = hashlib.sha1(file_content).hexdigest()
        #         if file_hash == content_hash:
        #             result['changed'] = False
        #             module.exit_json(**result)
        # except Exception as e:
        #     print(f'Error reading existing file: {e}')
        #     module.fail_json(msg='Error reading existing file: %s' % e, **result)

    # Check that path exists and create it if needed
    dir = os.path.dirname(module.params['path'])
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception as e:
            module.fail_json(msg='Error creating directory: %s' % e, **result)

    # Write content to file
    try:
        with open(module.params['path'], 'w') as file:
            try:
                file.write(module.params['content'])
                result['same_content'] = False
                result['changed'] = True
            except Exception as e:
                module.fail_json(msg='Error writing file: %s' % e, **result)
    except Exception as e:
        module.fail_json(msg='Error opening file: %s' % e, **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
