#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Создает файл по указанному пути с указанным наполнением.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Создает файл по указанному пути с указанным наполнением. Если файл уже существует, ничего не делает.

options:
    path:
        description: Путь для создания файла.
        required: true
        type: str
    content:
        description:
            - Содержимое файла. Если не указано, создается пустой файл.
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - vp_netology.learn_ansible.my_own_module

author:
    - Dmitriev Nikolay (@VP32)
'''

EXAMPLES = r'''
# Создание пустого файла.
- name: Create empty file 
  vp_netology.learn_ansible.my_own_module:
    path: ~/test/my.test

# Создание файла с содержимым.
- name: Create file with content My new content
  vp_netology.learn_ansible.my_own_module:
    path: ~/test/my.test
    content: My new content

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: Сообщение, поясняющее, что файл создался.
    type: str
    returned: always
    sample: 'File ~/test/my.test was created'
message:
    description: Сообщение, поясняющее, что файл уже существует.
    type: str
    returned: always
    sample: 'File ~/test/my.test already exists'
'''

from ansible.module_utils.basic import AnsibleModule
from pathlib import Path
from os import path


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
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

    # module logic
    my_file = Path(module.params['path'])
    if my_file.exists():
        result['changed'] = False
        result['message'] = f'File {module.params["path"]} already exists'
        module.exit_json(**result)

    my_dir = Path(path.dirname(module.params['path']))
    if not my_dir.exists():
        my_dir.mkdir(parents=True)

    with open(module.params['path'], 'w', encoding='utf-8') as f:
        f.write(module.params['content'])
        result['changed'] = True
        result['message'] = f'File {module.params["path"]} was created'

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
