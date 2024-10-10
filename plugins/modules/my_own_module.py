#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_file_creator

short_description: This module creates a file with specified content on the remote host.

version_added: "1.0.0"

description: This module allows you to create a file on the remote host with content specified by the user.

options:
    path:
        description: The full path where the file will be created.
        required: true
        type: str
    content:
        description: The content to write into the file.
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a file with the given content
- name: Create a file on the remote host
  my_namespace.my_collection.my_file_creator:
    path: /tmp/myfile.txt
    content: Hello, World!

# Create another file with different content
- name: Create another file
  my_namespace.my_collection.my_file_creator:
    path: /tmp/anotherfile.txt
    content: Ansible is awesome!
'''

RETURN = r'''
path:
    description: The path where the file was created.
    type: str
    returned: always
    sample: '/tmp/myfile.txt'
content:
    description: The content written to the file.
    type: str
    returned: always
    sample: 'Hello, World!'
changed:
    description: Whether the file was created or modified.
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
        path='',
        content=''
    )

    # create the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # if check mode is on, return current state without making changes
    if module.check_mode:
        result['path'] = path
        result['content'] = content
        module.exit_json(**result)

    # Check if the file already exists and has the same content
    if os.path.exists(path):
        with open(path, 'r') as file:
            existing_content = file.read()
        if existing_content == content:
            result['path'] = path
            result['content'] = content
            module.exit_json(**result)

    # Write the content to the file
    try:
        with open(path, 'w') as file:
            file.write(content)
        result['changed'] = True
        result['path'] = path
        result['content'] = content
    except Exception as e:
        module.fail_json(msg=f"Failed to write to file: {str(e)}", **result)

    # exit with the result
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()