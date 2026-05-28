# Ansible-Core - Collections

**Pages:** 319

---

## ansible.builtin.sha1 filter – SHA-1 hash of input data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sha1_filter.html

**Contents:**
- ansible.builtin.sha1 filter – SHA-1 hash of input data
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sha1. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sha1 for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a SHA-1 hash of the input data.

This describes the input of the filter, the value before | ansible.builtin.sha1.

This requires the SHA-1 algorithm to be available on the system, security contexts like FIPS might prevent this.

SHA-1 has been deemed insecure and is not recommended for security related uses.

The SHA-1 hash of the input.

**Examples:**

Example 1 (javascript):
```javascript
# sha1hash => "dc724af18fbdd4e59189f5fe768a5f8311527050"
sha1hash: "{{ 'testing' | sha1 }}"
```

---

## ansible.builtin.to_nice_yaml filter – Convert variable to YAML string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_nice_yaml_filter.html

**Contents:**
- ansible.builtin.to_nice_yaml filter – Convert variable to YAML string
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_nice_yaml. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_nice_yaml for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts an Ansible variable into a YAML string representation.

This filter functions as a wrapper to the Python PyYAML library‘s yaml.dump function.

Ansible internally auto-converts YAML strings into variable structures so this plugin is used to force it into a YAML string.

This describes the input of the filter, the value before | ansible.builtin.to_nice_yaml.

A variable or expression that returns a data structure.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.to_nice_yaml(key1=value1, key2=value2, ...)

Number of spaces to indent Python structures, mainly used for display to humans.

Affects sorting of dictionary keys.

More options may be available, see PyYAML documentation for details.

These parameters to yaml.dump will be ignored, as they are overridden internally: default_flow_style

The YAML serialized string representing the variable structure inputted.

**Examples:**

Example 1 (unknown):
```unknown
# dump variable in a template to create a YAML document
{{ github_workflow | to_nice_yaml }}
```

---

## ansible.builtin.subset test – is the list a subset of this other list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/subset_test.html

**Contents:**
- ansible.builtin.subset test – is the list a subset of this other list
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name subset. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.subset for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Validate if the first list is a sub set (is included) of the second list.

This describes the input of the test, the value before is ansible.builtin.subset or is not ansible.builtin.subset.

list / elements=any / required

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.subset(key1=value1, key2=value2, ...) and input is not ansible.builtin.subset(key1=value1, key2=value2, ...)

list / elements=any / required

List to test against.

Returns True if the specified list is a subset of the provided list, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
big: [1,2,3,4,5]
small: [3,4]
issmallinbig: '{{ small is subset(big) }}'
```

---

## Contributing to collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_contributing.html

**Contents:**
- Contributing to collections
- Contributing to a collection: community.general
  - Prerequisites
  - Creating a PR

If you want to add functionality to an existing collection, modify a collection you are using to fix a bug, or change the behavior of a module in a collection, clone the Git repository for that collection and make changes on a branch. You can combine changes to a collection with a local checkout of Ansible (source hacking/env-setup). You should first check the collection repository to see if it has specific contribution guidelines. These are typically listed in the README.md or CONTRIBUTING.md files within the repository. See Creating your first collection pull request for more general guidelines and Testing Ansible and Collections for testing guidelines.

These instructions apply to collections hosted in the ansible_collections GitHub organization. For other collections, especially for collections not hosted on GitHub, check the README.md of the collection for information on contributing to it.

This example uses the community.general collection. To contribute to other collections in the same GitHub org, replace the folder names community and general with the namespace and collection name of a different collection.

Include ~/dev/ansible/collections/ in COLLECTIONS_PATHS

If that path mentions multiple directories, make sure that no other directory earlier in the search path contains a copy of community.general.

Create the directory ~/dev/ansible/collections/ansible_collections/community:

Clone the community.general Git repository or a fork of it into the directory general:

If you clone from a fork, add the original repository as a remote upstream:

Create a branch and commit your changes on the branch.

Remember to add tests for your changes, see Testing collections.

Push your changes to your fork of the collection and create a Pull Request.

You can test your changes by using this checkout of community.general in playbooks and roles with whichever version of Ansible you have installed locally, including a local checkout of ansible/ansible’s devel branch.

Learn how to install and use collections.

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
mkdir -p ~/dev/ansible/collections/ansible_collections/community
```

Example 2 (unknown):
```unknown
cd ~/dev/ansible/collections/ansible_collections/community
git clone [email protected]:ansible-collections/community.general.git general
```

Example 3 (unknown):
```unknown
cd ~/dev/ansible/collections/ansible_collections/community/general
git remote add upstream [email protected]:ansible-collections/community.general.git
```

---

## ansible.builtin.include_vars module – Load variables from files, dynamically within a task — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/include_vars_module.html

**Contents:**
- ansible.builtin.include_vars module – Load variables from files, dynamically within a task
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name include_vars even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.include_vars for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Loads YAML/JSON variables dynamically from a file or directory, recursively, during task runtime.

If loading a directory, the files are sorted alphabetically before being loaded.

This module is also supported for Windows targets.

To assign included variables to a different host than inventory_hostname, use delegate_to and set delegate_facts=yes.

This module has a corresponding action plugin.

When using dir, this module will, by default, recursively go through each sub directory and load up the variables. By explicitly setting the depth, this module will only go as deep as the depth.

The directory name from which the variables should be loaded.

If the path is relative and the task is inside a role, it will look inside the role’s vars/ subdirectory.

If the path is relative and not inside a role, it will be parsed relative to the playbook.

list / elements=string

List of file extensions to read when using dir.

Default: ["json", "yaml", "yml"]

The file name from which variables should be loaded.

If the path is relative, it will look for the file in vars/ subdirectory of a role or relative to playbook.

Limit the files that are loaded within any directory to this regular expression.

This module allows you to specify the file option directly without any other options.

There is no free-form option, this is just an indicator, see example below.

added in ansible-core 2.12

If set to merge, merges existing hash variables instead of overwriting them.

If omitted (null), the behavior falls back to the global hash_behaviour configuration.

This option is self-contained and does not apply to individual files in dir. You can use a loop to apply hash_behaviour per file.

list / elements=string

List of file names to ignore.

ignore_unknown_extensions

Ignore unknown file extensions within the directory.

This allows users to specify a directory containing vars files that are intermingled with non-vars files extension types (e.g. a directory with a README in it and vars files).

The name of a variable into which assign the included vars.

If omitted (null) they will be made top level vars.

While the action plugin does do some of the work it relies on the core engine to actually create the variables, that part cannot be overridden

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

While parts of this action are implemented in core, other parts are still available as normal plugins and can be partially overridden

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

while variable assignment can be delegated to a different host the execution context is always the current inventory_hostname

connection variables, if set at all, would reflect the host it would target, even if we are not connecting at all in this case

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Set host variable(s) and fact(s).

More information related to task delegation.

Common return values are documented here, the following are the fields unique to this module:

ansible_included_var_files

list / elements=string

A list of files that were successfully included

Sample: ["/path/to/file.json", "/path/to/file.yaml"]

Allen Sanabria (@linuxdynasty)

**Examples:**

Example 1 (unknown):
```unknown
- name: Include vars of stuff.yaml into the 'stuff' variable (2.2).
  ansible.builtin.include_vars:
    file: stuff.yaml
    name: stuff

- name: Conditionally decide to load in variables into 'plans' when x is 0, otherwise do not. (2.2)
  ansible.builtin.include_vars:
    file: contingency_plan.yaml
    name: plans
  when: x == 0

- name: Load a variable file based on the OS type, or a default if not found. Using free-form to specify the file.
  ansible.builtin.include_vars: "{{ lookup('ansible.builtin.first_found', params) }}"
  vars:
    params:
      files:
        - '{{ansible_distribution}}.yaml'
        - '{{ansible_os_family}}.yaml'
        - default.yaml
      paths:
        - 'vars'

- name: Bare include (free-form)
  ansible.builtin.include_vars: myvars.yaml

- name: Include all .json and .jsn files in vars/all and all nested directories (2.3)
  ansible.builtin.include_vars:
    dir: vars/all
    extensions:
      - 'json'
      - 'jsn'

- name: Include all default extension files in vars/all and all nested directories and save the output in test. (2.2)
  ansible.builtin.include_vars:
    dir: vars/all
    name: test

- name: Include default extension files in vars/services (2.2)
  ansible.builtin.include_vars:
    dir: vars/services
    depth: 1

- name: Include only files matching bastion.yaml (2.2)
  ansible.builtin.include_vars:
    dir: vars
    files_matching: bastion.yaml

- name: Include all .yaml files except bastion.yaml (2.3)
  ansible.builtin.include_vars:
    dir: vars
    ignore_files:
      - 'bastion.yaml'
    extensions:
      - 'yaml'

- name: Ignore warnings raised for files with unknown extensions while loading (2.7)
  ansible.builtin.include_vars:
    dir: vars
    ignore_unknown_extensions: True
    extensions:
      - ''
      - 'yaml'
      - 'yml'
      - 'json'
```

---

## ansible.builtin.win_basename filter – Get a Windows path’s base name — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/win_basename_filter.html

**Contents:**
- ansible.builtin.win_basename filter – Get a Windows path’s base name
- Synopsis
- Input
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name win_basename. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.win_basename for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the last name component of a Windows path, what is left in the string that is not ‘win_dirname’.

While specifying an UNC (Universal Naming Convention) path, please make sure the path conforms to the UNC path syntax.

This describes the input of the filter, the value before | ansible.builtin.win_basename.

Get a Windows path’s directory.

The base name from the Windows path provided.

**Examples:**

Example 1 (unknown):
```unknown
# To get the last name of a file Windows path, like 'foo.txt' out of 'C:\Users\asdf\foo.txt'
filename: "{{ mypath | win_basename }}"

# Get basename from the UNC path in the form of '\\<SERVER_NAME>\<SHARE_NAME>\<FILENAME.FILE_EXTENSION>'
# like '\\server1\test\foo.txt' returns 'foo.txt'
filename: "{{ mypath | win_basename }}"
```

---

## ansible.builtin.together lookup – merges lists into synchronized list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/together_lookup.html

**Contents:**
- ansible.builtin.together lookup – merges lists into synchronized list
- Synopsis
- Terms
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name together. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.together for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Creates a list with the iterated elements of the supplied lists

To clarify with an example, [ ‘a’, ‘b’ ] and [ 1, 2 ] turn into [ (‘a’,1), (‘b’, 2) ]

This is basically the same as the ‘zip_longest’ filter and Python function

Any ‘unbalanced’ elements will be substituted with ‘None’

list of lists to merge

**Examples:**

Example 1 (unknown):
```unknown
- name: item.0 returns from the 'a' list, item.1 returns from the '1' list
  ansible.builtin.debug:
    msg: "{{ item.0 }} and {{ item.1 }}"
  with_together:
    - ['a', 'b', 'c', 'd']
    - [1, 2, 3, 4]
```

---

## ansible.builtin.include_role module – Load and execute a role — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/include_role_module.html

**Contents:**
- ansible.builtin.include_role module – Load and execute a role
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name include_role even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.include_role for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Dynamically loads and executes a specified role as a task.

May be used only where Ansible tasks are allowed - inside pre_tasks, tasks, or post_tasks play objects, or as a task inside a role.

Task-level keywords, loops, and conditionals apply only to the include_role statement itself.

To apply keywords to the tasks within the role, pass them using the apply option or use ansible.builtin.import_role instead.

Ignores some keywords, like until and retries.

This module is also supported for Windows targets.

Does not work in handlers.

Overrides the role’s metadata setting to allow using a role more than once with the same parameters.

Accepts a hash of task keywords (for example tags, become) that will be applied to all tasks within the included role.

File to load from a role’s defaults/ directory.

File to load from a role’s handlers/ directory.

The name of the role to be executed.

This option dictates whether the role’s vars and defaults are exposed to the play. If set to true the variables will be available to tasks following the include_role task. This functionality differs from standard variable exposure for roles listed under the roles header or ansible.builtin.import_role as they are exposed to the play at playbook parsing time, and available to earlier roles and tasks as well.

added in ansible-core 2.11

Perform role argument spec validation if an argument spec is defined.

File to load from a role’s tasks/ directory.

File to load from a role’s vars/ directory.

While this action executes locally on the controller it is not governed by an action plugin

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Since there are no connection nor facts, there is no sense in delegating includes

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Tags are interpreted by this action but are not automatically inherited by the include tasks, see apply

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Handlers and are made available to the whole play.

After Ansible 2.4, you can use ansible.builtin.import_role for static behaviour and this action for dynamic one.

Import a role into a play.

Dynamically include a task list.

More information related to including and importing playbooks, roles and tasks.

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- ansible.builtin.include_role:
    name: myrole

- name: Run tasks/other.yaml instead of 'main'
  ansible.builtin.include_role:
    name: myrole
    tasks_from: other

- name: Pass variables to role
  ansible.builtin.include_role:
    name: myrole
  vars:
    rolevar1: value from task

- name: Use role in loop
  ansible.builtin.include_role:
    name: '{{ roleinputvar }}'
  loop:
    - '{{ roleinput1 }}'
    - '{{ roleinput2 }}'
  loop_control:
    loop_var: roleinputvar

- name: Conditional role
  ansible.builtin.include_role:
    name: myrole
  when: not idontwanttorun

- name: Apply tags to tasks within included file
  ansible.builtin.include_role:
    name: install
    apply:
      tags:
        - install
  tags:
    - always
```

---

## ansible.builtin.path_join filter – Join one or more path components — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/path_join_filter.html

**Contents:**
- ansible.builtin.path_join filter – Join one or more path components
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name path_join. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.path_join for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-base 2.10

Returns a path obtained by joining one or more path components.

If a path component is an absolute path, then all previous components are ignored and joining continues from the absolute path. See examples for details.

This describes the input of the filter, the value before | ansible.builtin.path_join.

list / elements=string / required

A path, or a list of paths.

The concatenated path.

Anthony Bourguignon (@Toniob)

**Examples:**

Example 1 (javascript):
```javascript
# If path == 'foo/bar' and file == 'baz.txt', the result is '/etc/foo/bar/subdir/baz.txt'
{{ ('/etc', path, 'subdir', file) | path_join }}

# equivalent to '/etc/subdir/{{filename}}'
wheremyfile: "{{ ['/etc', 'subdir', filename] | path_join }}"

# trustme => '/etc/apt/trusted.d/mykey.gpg'
trustme: "{{ ['/etc', 'apt', 'trusted.d', 'mykey.gpg'] | path_join }}"

# If one of the paths is absolute, then path_join ignores all previous path components
# If backup_dir == '/tmp' and backup_file == '/sample/baz.txt', the result is '/sample/baz.txt'
# backup_path => "/sample/baz.txt"
backup_path: "{{ ('/etc', backup_dir, backup_file) | path_join }}"
```

---

## ansible.builtin.realpath filter – Turn path into real path — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/realpath_filter.html

**Contents:**
- ansible.builtin.realpath filter – Turn path into real path
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name realpath. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.realpath for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Resolves/follows symlinks to return the ‘real path’ from a given path.

Filters always run on the controller so this path is resolved using the controller’s filesystem.

This describes the input of the filter, the value before | ansible.builtin.realpath.

darkone23 (@darkone23)

**Examples:**

Example 1 (javascript):
```javascript
# realpath => /usr/bin/somebinary
realpath: {{ '/path/to/synlink' | realpath }}
```

---

## ansible.builtin.ini lookup – read data from an ini file — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ini_lookup.html

**Contents:**
- ansible.builtin.ini lookup – read data from an ini file
- Synopsis
- Terms
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ini. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ini for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

The ini lookup reads the contents of a file in INI format key1=value1. This plugin retrieves the value on the right side after the equal sign '=' of a given section [section].

You can also read a property file which - in this case - does not contain section.

The key(s) to look up.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.ini', key1=value1, key2=value2, ...) and query('ansible.builtin.ini', key1=value1, key2=value2, ...)

added in ansible-core 2.12

Read an ini file which contains key without value and without ‘=’ symbol.

added in ansible-core 2.12

Whether key names read from file should be case sensitive. This prevents duplicate key errors if keys only differ in case.

Return value if the key is not in the ini file.

Text encoding to use.

Name of the file to load.

Default: "ansible.ini"

added in ansible-core 2.18

Allows for interpolation of values, see https://docs.python.org/3/library/configparser.html#configparser.BasicInterpolation

Flag to indicate if the key supplied is a regexp.

Section where to lookup the key.

Type of the file. ‘properties’ refers to the Java properties files.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.ini', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.ini', term1, term2, key1=value1, key2=value2)

Search paths used for relative files.

list / elements=string

value(s) of the key(s) in the ini file

Yannig Perre <yannig.perre(at)gmail.com>

**Examples:**

Example 1 (unknown):
```unknown
- ansible.builtin.debug: msg="User in integration is {{ lookup('ansible.builtin.ini', 'user', section='integration', file='users.ini') }}"

- ansible.builtin.debug: msg="User in production  is {{ lookup('ansible.builtin.ini', 'user', section='production',  file='users.ini') }}"

- ansible.builtin.debug: msg="user.name is {{ lookup('ansible.builtin.ini', 'user.name', type='properties', file='user.properties') }}"

- ansible.builtin.debug:
    msg: "{{ item }}"
  loop: "{{ q('ansible.builtin.ini', '.*', section='section1', file='test.ini', re=True) }}"

- name: Read an ini file with allow_no_value
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.ini', 'user', file='mysql.ini', section='mysqld', allow_no_value=True) }}"
```

---

## ansible.builtin.b64encode filter – Encode a string as Base64 — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/b64encode_filter.html

**Contents:**
- ansible.builtin.b64encode filter – Encode a string as Base64
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name b64encode. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.b64encode for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Base64 encoding function.

This describes the input of the filter, the value before | ansible.builtin.b64encode.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.b64encode(key1=value1, key2=value2, ...)

The encoding to use to transform from a text string to a byte string.

Defaults to using ‘utf-8’.

added in ansible-core 2.19

Encode string using URL- and filesystem-safe alphabet, which substitutes - instead of + and _ instead of / in the Base64 alphabet.

A Base64 encoded string.

**Examples:**

Example 1 (javascript):
```javascript
# Base64 encode a string
b64lola: "{{ 'lola'| b64encode }}"

# Base64 encode the content of 'stuff' variable
b64stuff: "{{ stuff | b64encode }}"

# Base64 encode the content with different encoding
b64stuff: "{{ 'Ansible - くらとみ\n' | b64encode(encoding='utf-16-le') }}"
# => 'QQBuAHMAaQBiAGwAZQAgAC0AIABPMIkwaDB/MAoA'

# URL-safe Base64 encoding
b64stuff: "{{ 'https://www.python.org/example-1' | b64encode(urlsafe=True) }}"
# => 'aHR0cHM6Ly93d3cucHl0aG9uLm9yZy9leGFtcGxlLTE='
```

---

## ansible.builtin.basename filter – get a path’s base name — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/basename_filter.html

**Contents:**
- ansible.builtin.basename filter – get a path’s base name
- Synopsis
- Input
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name basename. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.basename for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the last name component of a path, what is left in the string that is not ‘dirname’.

This describes the input of the filter, the value before | ansible.builtin.basename.

The result of this filter is different from the Unix basename program; where basename for /foo/bar/ returns bar, the basename filter returns an empty string ('').

get a path’s directory name.

The base name from the path provided.

**Examples:**

Example 1 (unknown):
```unknown
# To get the last name of a file path, like 'foo.txt' out of '/etc/asdf/foo.txt'.
{{ mypath | basename }}
```

---

## ansible.builtin.rpm_key module – Adds or removes a gpg key from the rpm db — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/rpm_key_module.html

**Contents:**
- ansible.builtin.rpm_key module – Adds or removes a gpg key from the rpm db
- Synopsis
- Parameters
- Attributes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name rpm_key even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.rpm_key for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Adds or removes rpm --import a gpg key to your rpm database.

list / elements=string

The long-form fingerprint of the key being imported.

This will be used to verify the specified key.

Key that will be modified. Can be a url, a file on the managed node, or a keyid if the key already exists in the database.

If the key will be imported or removed from the rpm db.

"present" ← (default)

If false and the key is a url starting with https, SSL certificates will not be validated.

This should only be used on personally controlled sites using self-signed certificates.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Hector Acosta (@hacosta)

**Examples:**

Example 1 (unknown):
```unknown
- name: Import a key from a url
  ansible.builtin.rpm_key:
    state: present
    key: http://apt.sw.be/RPM-GPG-KEY.dag.txt

- name: Import a key from a file
  ansible.builtin.rpm_key:
    state: present
    key: /path/to/key.gpg

- name: Ensure a key is not present in the db
  ansible.builtin.rpm_key:
    state: absent
    key: DEADB33F

- name: Verify the key, using a fingerprint, before import
  ansible.builtin.rpm_key:
    key: /path/to/RPM-GPG-KEY.dag.txt
    fingerprint: EBC6 E12C 62B1 C734 026B  2122 A20E 5214 6B8D 79E6

- name: Verify the key, using multiple fingerprints, before import
  ansible.builtin.rpm_key:
    key: /path/to/RPM-GPG-KEY.dag.txt
    fingerprint:
      - EBC6 E12C 62B1 C734 026B  2122 A20E 5214 6B8D 79E6
      - 19B7 913E 6284 8E3F 4D78 D6B4 ECD9 1AB2 2EB6 8D86
```

---

## Collection Galaxy metadata structure — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/collections_galaxy_meta.html

**Contents:**
- Collection Galaxy metadata structure
- Structure
- Examples

A key component of an Ansible collection is the galaxy.yml file placed in the root directory of a collection. This file contains the metadata of the collection that is used to generate a collection artifact.

The galaxy.yml file must contain the following keys in valid YAML:

The namespace of the collection.

This can be a company/brand/organization or product namespace under which all content lives.

May only contain alphanumeric lowercase characters and underscores. Namespaces cannot start with underscores or numbers and cannot contain consecutive underscores.

The name of the collection.

Has the same character restrictions as namespace.

The version of the collection.

Must be compatible with semantic versioning.

The path to the Markdown (.md) readme file.

This path is relative to the root of the collection.

A list of the collection’s content authors.

Can be just the name or in the format ‘Full Name <email> (url) @nicks:irc/im.site#channel’.

A short summary description of the collection.

Either a single license or a list of licenses for content inside of a collection.

Ansible Galaxy currently only accepts SPDX licenses

This key is mutually exclusive with license_file.

The path to the license file for the collection.

This path is relative to the root of the collection.

This key is mutually exclusive with license.

A list of tags you want to associate with the collection for indexing/searching.

A tag name has the same character requirements as namespace and name.

Collections that this collection requires to be installed for it to be usable.

The key of the dict is the collection label namespace.name.

The value is a version range specifiers.

Multiple version range specifiers can be set and are separated by ,.

The URL of the originating SCM repository.

The URL to any online docs.

The URL to the homepage of the collection/project.

The URL to the collection issue tracker.

A list of file glob-like patterns used to filter any files or directories that should not be included in the build artifact.

A pattern is matched from the relative path of the file or directory of the collection directory.

This uses fnmatch to match the files or directories.

Some directories and files like galaxy.yml, *.pyc, *.retry, and .git are always filtered.

Mutually exclusive with manifest

A dict controlling use of manifest directives used in building the collection artifact.

The key directives is a list of MANIFEST.in style directives

The key omit_default_directives is a boolean that controls whether the default directives are used

Mutually exclusive with build_ignore

Develop or modify a collection.

Learn about how to write Ansible modules

Learn how to install and use collections.

The development mailing list

#ansible IRC chat channel

**Examples:**

Example 1 (unknown):
```unknown
namespace: "namespace_name"
name: "collection_name"
version: "1.0.12"
readme: "README.md"
authors:
    - "Author1"
    - "Author2 (https://author2.example.com)"
    - "Author3 <[email protected]>"
dependencies:
    "other_namespace.collection1": ">=1.0.0"
    "other_namespace.collection2": ">=2.0.0,<3.0.0"
    "anderson55.my_collection": "*"    # note: "*" selects the highest version available
license:
    - "MIT"
tags:
    - demo
    - collection
repository: "https://www.github.com/my_org/my_collection"
```

---

## ansible.builtin.set_stats module – Define and display stats for the current ansible run — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/set_stats_module.html

**Contents:**
- ansible.builtin.set_stats module – Define and display stats for the current ansible run
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name set_stats even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.set_stats for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module allows setting/accumulating stats on the current ansible run, either per host or for all hosts in the run.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

Whether the provided value is aggregated to the existing stat true or will replace it false.

dictionary / required

A dictionary of which each key represents a stat (or variable) you want to keep track of.

Whether the stats are per host or for all hosts in the run.

While the action plugin does do some of the work it relies on the core engine to actually create the variables, that part cannot be overridden

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

While parts of this action are implemented in core, other parts are still available as normal plugins and can be partially overridden

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

In order for custom stats to be displayed, you must set show_custom_stats in section [defaults] in ansible.cfg or by defining environment variable ANSIBLE_SHOW_CUSTOM_STATS to true. See the ansible.builtin.default callback plugin for details.

**Examples:**

Example 1 (unknown):
```unknown
- name: Aggregating packages_installed stat per host
  ansible.builtin.set_stats:
    data:
      packages_installed: 31
    per_host: yes

- name: Aggregating random stats for all hosts using complex arguments
  ansible.builtin.set_stats:
    data:
      one_stat: 11
      other_stat: "{{ local_var * 2 }}"
      another_stat: "{{ some_registered_var.results | map(attribute='ansible_facts.some_fact') | list }}"
    per_host: no

- name: Setting stats (not aggregating)
  ansible.builtin.set_stats:
    data:
      the_answer: 42
    aggregate: no
```

---

## ansible.builtin.gather_facts module – Gathers facts about remote hosts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/gather_facts_module.html

**Contents:**
- ansible.builtin.gather_facts module – Gathers facts about remote hosts
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name gather_facts even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.gather_facts for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module takes care of executing the configured facts modules, the default is to use the ansible.builtin.setup module.

This module is automatically called by playbooks to gather useful variables about remote hosts that can be used in playbooks.

It can also be executed directly by /usr/bin/ansible to check what variables are available to a host.

Ansible provides many facts about the system, automatically.

This module has a corresponding action plugin.

A toggle that controls if the fact modules are executed in parallel or serially and in order. This can guarantee the merge order of module facts at the expense of performance.

By default it will be true if more than one fact module is used.

For low cost/delay fact modules parallelism overhead might end up meaning the whole process takes longer. Test your specific case to see if it is a speed improvement or not.

The ansible_facts_parallel variable can be used to set this option, overriding the default, but not the direct assignment of the option in the task.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

while this action does not support the task ‘async’ keywords it can do its own parallel processing using the parallel option.

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

since this action should just query the target system info it always runs in check mode

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

The action plugin should be able to automatically select the specific platform modules automatically or can be configured manually

Target OS/families that can be operated against

This is mostly a wrapper around other fact gathering modules.

Options passed into this action must be supported by all the underlying fact modules configured.

If using gather_timeout and parallel execution, it will limit the total execution time of modules that do not accept gather_timeout themselves.

Facts returned by each module will be merged, conflicts will favor ‘last merged’. Order is not guaranteed, when doing parallel gathering on multiple modules.

**Examples:**

Example 1 (unknown):
```unknown
# Display facts from all hosts and store them indexed by hostname at /tmp/facts.
# ansible all -m ansible.builtin.gather_facts --tree /tmp/facts
```

---

## ansible.builtin.minimal callback – minimal Ansible screen output — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/minimal_callback.html

**Contents:**
- ansible.builtin.minimal callback – minimal Ansible screen output
- Callback plugin
- Synopsis
- Parameters
  - Collection links

This callback plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name minimal. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.minimal for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same callback plugin name.

This plugin is a stdout callback. You can use only use one stdout callback at a time. Additional aggregate or notification callbacks can be enabled though. See Callback plugins for more information on callback plugins.

This is the default output callback used by the ansible command (ad-hoc)

added in ansible-core 2.13

Configure the result format to be more readable.

When result_format is set to yaml this option defaults to true, and defaults to false when configured to json.

Setting this option to true will force json and yaml results to always be pretty printed regardless of verbosity.

When set to true and used with the yaml result format, this option will modify module responses in an attempt to produce a more human friendly output at the expense of correctness, and should not be relied upon to aid in writing variable manipulations or conditionals. For correctness, set this option to false or set result_format to json.

Environment variable: ANSIBLE_CALLBACK_FORMAT_PRETTY

added in ansible-core 2.13

Define the task result format used in the callback output.

These formats do not cause the callback to emit valid JSON or YAML formats.

The output contains these formats interspersed with other non-machine parsable data.

Environment variable: ANSIBLE_CALLBACK_RESULT_FORMAT

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
callback_format_pretty = VALUE
```

Example 2 (unknown):
```unknown
[defaults]
callback_result_format = json
```

---

## ansible.builtin.product filter – cartesian product of lists — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/product_filter.html

**Contents:**
- ansible.builtin.product filter – cartesian product of lists
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name product. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.product for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Combines two lists into one with each element being the product of the elements of the input lists.

Creates ‘nested loops’. Looping over listA and listB is the same as looping over listA | product(listB).

This describes the input of the filter, the value before | ansible.builtin.product.

list / elements=string / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.product(positional1, positional2, ...)

list / elements=string

Additional list for the product.

Number of times to repeat the product against itself.

This is a passthrough to Python’s itertools.product

List of lists of combined elements from the input lists.

**Examples:**

Example 1 (javascript):
```javascript
# product => [ [ 1, "a" ], [ 1, "b" ], [ 1, "c" ], [ 2, "a" ], [ 2, "b" ], [ 2, "c" ], [ 3, "a" ], [ 3, "b" ], [ 3, "c" ], [ 4, "a" ], [ 4, "b" ], [ 4, "c" ], [ 5, "a" ], [ 5, "b" ], [ 5, "c" ] ]
product:  "{{ [1,2,3,4,5] | product(['a', 'b', 'c']) }}"

# repeat_original => [ [ 1, 1 ], [ 1, 2 ], [ 2, 1 ], [ 2, 2 ] ]
repeat_original: "{{ [1,2] | product(repeat=2) }}"

# repeat_product => [ [ 1, "a", 1, "a" ], [ 1, "a", 1, "b" ], [ 1, "a", 2, "a" ], [ 1, "a", 2, "b" ], [ 1, "b", 1, "a" ], [ 1, "b", 1, "b" ], [ 1, "b", 2, "a" ], [ 1, "b", 2, "b" ], [ 2, "a", 1, "a" ], [ 2, "a", 1, "b" ], [ 2, "a", 2, "a" ], [ 2, "a", 2, "b" ], [ 2, "b", 1, "a" ], [ 2, "b", 1, "b" ], [ 2, "b", 2, "a" ], [ 2, "b", 2, "b" ] ]
repeat_product:  "{{ [1,2] | product(['a', 'b'], repeat=2) }}"

# domains => [ 'example.com', 'ansible.com', 'redhat.com' ]
domains: "{{ [ 'example', 'ansible', 'redhat'] | product(['com']) | map('join', '.') }}"
```

---

## ansible.builtin.filter test – Check if a filter exists by name. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/filter_test.html

**Contents:**
- ansible.builtin.filter test – Check if a filter exists by name.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name filter. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.filter for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if a filter exists by name.

This is the Jinja builtin test plugin ‘filter’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.filter

---

## ansible.builtin.default filter – If the value is undefined it will return the passed default value, otherwise the value of the variable. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/default_filter.html

**Contents:**
- ansible.builtin.default filter – If the value is undefined it will return the passed default value, otherwise the value of the variable.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name default. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.default for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

If the value is undefined it will return the passed default value, otherwise the value of the variable.

This is the Jinja builtin filter plugin ‘default’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.default

---

## ansible.builtin.vault filter – vault your secrets — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/vault_filter.html

**Contents:**
- ansible.builtin.vault filter – vault your secrets
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name vault. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.vault for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.12

Positional parameters

Put your information into an encrypted Ansible Vault.

This describes the input of the filter, the value before | ansible.builtin.vault.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.vault(positional1, positional2, ...)

Vault secret, the key that lets you open the vault.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.vault(key1=value1, key2=value2, ...)

Encryption salt, will be random if not provided.

While providing one makes the resulting encrypted string reproducible, it can lower the security of the vault.

Secret identifier, used internally to try to best match a secret when multiple are provided.

Default: "filter_default"

This toggle can force the return of a VaultedValue-tagged string object, when False, you get a simple string.

Mostly useful when combining with the to_yaml filter to output the ‘inline vault’ format.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.vault(positional1, positional2, key1=value1, key2=value2)

The vault string that contains the secret data (or VaultedValue-tagged string object).

**Examples:**

Example 1 (unknown):
```unknown
# Encrypt a value using the vault filter
vars:
  myvaultedkey: "{{ 'my_secret_key' | vault('my_vault_password') }}"

# Encrypt a value and save it to a file using the template module
vars:
  template_data: "{{ 'my_sensitive_data' | vault('another_vault_password', salt=(2**256 | random(seed=inventory_hostname))) }}"

# The content of dump_template_data.j2 looks like
#     Encrypted secret: {{ template_data }}
- name: Save vaulted data
  template:
    src: dump_template_data.j2
    dest: /some/key/vault.txt
```

---

## ansible.builtin.undefined test – Like :func:`defined` but the other way round. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/undefined_test.html

**Contents:**
- ansible.builtin.undefined test – Like :func:`defined` but the other way round.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name undefined. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.undefined for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Like :func:`defined` but the other way round.

This is the Jinja builtin test plugin ‘undefined’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.undefined

---

## ansible.builtin.to_yaml filter – Convert variable to YAML string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_yaml_filter.html

**Contents:**
- ansible.builtin.to_yaml filter – Convert variable to YAML string
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_yaml. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_yaml for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts an Ansible variable into a YAML string representation.

This filter functions as a wrapper to the Python PyYAML library‘s yaml.dump function.

Ansible automatically converts YAML strings into variable structures so this plugin is used to forcibly retain a YAML string.

This describes the input of the filter, the value before | ansible.builtin.to_yaml.

A variable or expression that returns a data structure.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.to_yaml(key1=value1, key2=value2, ...)

Number of spaces to indent Python structures, mainly used for display to humans.

Affects sorting of dictionary keys.

More options may be available, see PyYAML documentation for details.

The YAML serialized string representing the variable structure inputted.

**Examples:**

Example 1 (unknown):
```unknown
# dump variable in a template to create a YAML document
{{ github_workflow | to_yaml }}

# same as above but 'prettier' (equivalent to to_nice_yaml filter)
{{ docker_config | to_yaml(indent=4) }}
```

---

## ansible.builtin.finished test – Did async task finish — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/finished_test.html

**Contents:**
- ansible.builtin.finished test – Did async task finish
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name finished. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.finished for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Used to test if an async task has finished, it will also work with normal tasks but will issue a warning.

This test checks for the existence of a finished key in the input dictionary and that it is True if present

This describes the input of the test, the value before is ansible.builtin.finished or is not ansible.builtin.finished.

dictionary / required

registered result from an Ansible task

Returns True if the async task has finished, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ (asynctaskpoll is finished}}
```

---

## ansible.builtin.filesizeformat filter – Format the value like a ‘human-readable’ file size. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/filesizeformat_filter.html

**Contents:**
- ansible.builtin.filesizeformat filter – Format the value like a ‘human-readable’ file size.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name filesizeformat. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.filesizeformat for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Format the value like a ‘human-readable’ file size.

This is the Jinja builtin filter plugin ‘filesizeformat’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.filesizeformat

---

## ansible.builtin.center filter – Centers the value in a field of a given width. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/center_filter.html

**Contents:**
- ansible.builtin.center filter – Centers the value in a field of a given width.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name center. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.center for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Centers the value in a field of a given width.

This is the Jinja builtin filter plugin ‘center’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.center

---

## ansible.builtin.dict2items filter – Convert a dictionary into an itemized list of dictionaries — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dict2items_filter.html

**Contents:**
- ansible.builtin.dict2items filter – Convert a dictionary into an itemized list of dictionaries
- Synopsis
- Input
- Positional parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name dict2items. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dict2items for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Takes a dictionary and transforms it into a list of dictionaries, with each having a key and value keys that correspond to the keys and values of the original.

This describes the input of the filter, the value before | ansible.builtin.dict2items.

dictionary / required

The dictionary to transform

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.dict2items(positional1, positional2, ...)

The name of the property on the item representing the dictionary’s keys.

The name of the property on the item representing the dictionary’s values.

Consolidate a list of itemized dictionaries into a dictionary.

list / elements=dictionary

A list of dictionaries.

**Examples:**

Example 1 (javascript):
```javascript
# items => [ { "key": "a", "value": 1 }, { "key": "b", "value": 2 } ]
items: "{{ {'a': 1, 'b': 2}| dict2items }}"

# files_dicts: [
#       {
#           "file": "users",
#           "path": "/etc/passwd"
#       },
#       {
#           "file": "groups",
#           "path": "/etc/group"
#       }
# ]
vars:
  files:
    users: /etc/passwd
    groups: /etc/group
  files_dicts: "{{ files | dict2items(key_name='file', value_name='path') }}"
```

---

## ansible.builtin.random_choice lookup – return random element from list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/random_choice_lookup.html

**Contents:**
- ansible.builtin.random_choice lookup – return random element from list
- Synopsis
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name random_choice. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.random_choice for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

The ‘random_choice’ feature can be used to pick something at random. While it’s not a load balancer (there are modules for those), it can somewhat be used as a poor man’s load balancer in a MacGyver like situation.

At a more basic level, they can be used to add chaos and excitement to otherwise predictable automation environments.

**Examples:**

Example 1 (unknown):
```unknown
- name: Magic 8 ball for MUDs
  ansible.builtin.debug:
    msg: "{{ item }}"
  with_random_choice:
     - "go through the door"
     - "drink from the goblet"
     - "press the red button"
     - "do nothing"
```

---

## ansible.builtin.wait_for_connection module – Waits until remote system is reachable/usable — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/wait_for_connection_module.html

**Contents:**
- ansible.builtin.wait_for_connection module – Waits until remote system is reachable/usable
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name wait_for_connection even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.wait_for_connection for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Waits for a total of timeout seconds.

Retries the transport connection after a timeout of connect_timeout.

Tests the transport connection every sleep seconds.

This module makes use of internal ansible transport (and configuration) and the ansible.builtin.ping/ansible.windows.win_ping modules to guarantee correct end-to-end functioning.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

Maximum number of seconds to wait for a connection to happen before closing and retrying.

Number of seconds to wait before starting to poll.

Number of seconds to sleep between checks.

Maximum number of seconds to wait for.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

As long as there is a connection plugin

Target OS/families that can be operated against

Waits for a condition before continuing.

The official documentation on the ansible.windows.win_wait_for module.

The official documentation on the community.windows.win_wait_for_process module.

Common return values are documented here, the following are the fields unique to this module:

The number of seconds that elapsed waiting for the connection to appear.

Dag Wieers (@dagwieers)

**Examples:**

Example 1 (unknown):
```unknown
- name: Wait 600 seconds for target connection to become reachable/usable
  ansible.builtin.wait_for_connection:

- name: Wait 300 seconds, but only start checking after 60 seconds
  ansible.builtin.wait_for_connection:
    delay: 60
    timeout: 300

# Wake desktops, wait for them to become ready and continue playbook
- hosts: all
  gather_facts: no
  tasks:
  - name: Send magic Wake-On-Lan packet to turn on individual systems
    community.general.wakeonlan:
      mac: '{{ mac }}'
      broadcast: 192.168.0.255
    delegate_to: localhost

  - name: Wait for system to become reachable
    ansible.builtin.wait_for_connection:

  - name: Gather facts for first time
    ansible.builtin.setup:

# Build a new VM, wait for it to become ready and continue playbook
- hosts: all
  gather_facts: no
  tasks:
  - name: Clone new VM, if missing
    community.vmware.vmware_guest:
      hostname: '{{ vcenter_ipaddress }}'
      name: '{{ inventory_hostname_short }}'
      template: Windows 2012R2
      customization:
        hostname: '{{ vm_shortname }}'
        runonce:
        - cmd.exe /c winrm.cmd quickconfig -quiet -force
    delegate_to: localhost

  - name: Wait for system to become reachable over WinRM
    ansible.builtin.wait_for_connection:
      timeout: 900

  - name: Gather facts for first time
    ansible.builtin.setup:
```

---

## ansible.builtin.splitext filter – split a path into root and file extension — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/splitext_filter.html

**Contents:**
- ansible.builtin.splitext filter – split a path into root and file extension
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name splitext. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.splitext for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a list of two, with the elements consisting of filename root and extension.

This describes the input of the filter, the value before | ansible.builtin.splitext.

list / elements=string

A list consisting of root of the path and the extension.

**Examples:**

Example 1 (javascript):
```javascript
# gobble => [ '/etc/make', '.conf' ]
gobble: "{{ '/etc/make.conf' | splitext }}"

# file_n_ext => [ 'ansible', '.cfg' ]
file_n_ext: "{{ 'ansible.cfg' | splitext }}"

# hoax => [ '/etc/hoasdf', '' ]
hoax: "{{ '/etc/hoasdf' | splitext }}"
```

---

## ansible.builtin.timedout test – did the task time out — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/timedout_test.html

**Contents:**
- ansible.builtin.timedout test – did the task time out
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name timedout. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.timedout for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-core 2.18

Tests if task finished ended due to a time out

This describes the input of the test, the value before is ansible.builtin.timedout or is not ansible.builtin.timedout.

dictionary / required

registered result from an Ansible task

A dictionary with 2 keys ‘frame’ showing the ‘frame of code’ in which the timeout occurred and ‘period’ with the time limit that was enforced.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is timedout }}
```

---

## ansible.builtin.boolean test – Return true if the object is a boolean value. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/boolean_test.html

**Contents:**
- ansible.builtin.boolean test – Return true if the object is a boolean value.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name boolean. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.boolean for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is a boolean value.

This is the Jinja builtin test plugin ‘boolean’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.boolean

---

## ansible.builtin.service_facts module – Return service state information as fact data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/service_facts_module.html

**Contents:**
- ansible.builtin.service_facts module – Return service state information as fact data
- Synopsis
- Requirements
- Attributes
- Notes
- Examples
- Returned Facts
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name service_facts even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.service_facts for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Return service state information as fact data for various service management utilities.

The below requirements are needed on the host that executes this module.

Any of the following supported init systems: systemd, sysv, upstart, openrc, AIX SRC

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

Target OS/families that can be operated against

When accessing the ansible_facts.services facts collected by this module, it is recommended to not use “dot notation” because services can have a - character in their name which would result in invalid “dot notation”, such as ansible_facts.services.zuul-gateway. It is instead recommended to using the string value of the service name as the key in order to obtain the fact data value like ansible_facts.services['zuul-gateway']

AIX SRC was added in version 2.11.

Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.

list / elements=dictionary

States of the services with service name as key.

Sample: "arp-ethers.service"

Init system of the service.

One of rcctl, systemd, sysv, upstart, src.

State of the service.

This commonly includes (but is not limited to) the following: failed, running, stopped or unknown.

Depending on the used init system additional states might be returned.

State of the service.

Either enabled, disabled, static, indirect or unknown.

Returned: systemd systems or RedHat/SUSE flavored sysvinit/upstart or OpenBSD

Adam Miller (@maxamillion)

**Examples:**

Example 1 (unknown):
```unknown
- name: Populate service facts
  ansible.builtin.service_facts:

- name: Print service facts
  ansible.builtin.debug:
    var: ansible_facts.services

- name: show names of existing systemd services, sometimes systemd knows about services that were never installed
  debug: msg={{ existing_systemd_services | map(attribute='name') }}
  vars:
     known_systemd_services: "{{ ansible_facts['services'].values() | selectattr('source', 'equalto', 'systemd') }}"
     existing_systemd_services: "{{ known_systemd_services | rejectattr('status', 'equalto', 'not-found') }}"

- name: restart systemd service if it exists
  service:
    state: restarted
    name: ntpd.service
  when: ansible_facts['services']['ntpd.service']['status'] | default('not-found') != 'not-found'
```

---

## ansible.builtin.systemd module — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/systemd_module.html

**Contents:**
- ansible.builtin.systemd module

This redirect is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name systemd even without specifying the collections keyword. Despite that, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.systemd for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This is a redirect to the ansible.builtin.systemd_service module.

---

## ansible.builtin.raw module – Executes a low-down and dirty command — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/raw_module.html

**Contents:**
- ansible.builtin.raw module – Executes a low-down and dirty command
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name raw even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.raw for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Executes a low-down and dirty SSH command, not going through the module subsystem.

This is useful and should only be done in a few cases. A common case is installing python on a system without python installed by default. Another is speaking to any devices such as routers that do not have any Python installed. In any other case, using the ansible.builtin.shell or ansible.builtin.command module is much more appropriate.

Arguments given to raw are run directly through the configured remote shell.

Standard output, error output and return code are returned when available.

There is no change handler support for this module.

This module does not require python on the remote system, much like the ansible.builtin.script module.

This module is also supported for Windows targets.

If the command returns non UTF-8 data, it must be encoded to avoid issues. One option is to pipe the output through base64.

This module has a corresponding action plugin.

Change the shell used to execute the command. Should be an absolute path to the executable.

When using privilege escalation (become) a default shell will be assigned if one is not provided as privilege escalation requires a shell.

The raw module takes a free form command to run.

There is no parameter actually named ‘free form’; see the examples!

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

This action is one of the few that requires no Python on the remote as it passes the command directly into the connection string

Target OS/families that can be operated against

Indicates if an action takes a ‘raw’ or ‘free form’ string as an option and has it’s own special parsing of it

If using raw from a playbook, you may need to disable fact gathering using gather_facts: no if you’re using raw to bootstrap python onto the machine.

If you want to execute a command securely and predictably, it may be better to use the ansible.builtin.command or ansible.builtin.shell modules instead.

The environment keyword does not work with raw normally, it requires a shell which means it only works if executable is set or using the module with privilege escalation (become).

Execute commands on targets.

Execute shell commands on targets.

The official documentation on the ansible.windows.win_command module.

The official documentation on the ansible.windows.win_shell module.

**Examples:**

Example 1 (unknown):
```unknown
- name: Bootstrap a host without Python installed
  ansible.builtin.raw: dnf install -y python3 python3-libdnf

- name: Run a command that uses non-posix shell-isms (in this example /bin/sh doesn't handle redirection and wildcards together but bash does)
  ansible.builtin.raw: cat < /tmp/*txt
  args:
    executable: /bin/bash

- name: Safely use templated variables. Always use quote filter to avoid injection issues.
  ansible.builtin.raw: "{{ package_mgr|quote }} {{ pkg_flags|quote }} install {{ python|quote }}"

- name: List user accounts on a Windows system
  ansible.builtin.raw: Get-WmiObject -Class Win32_UserAccount
```

---

## ansible.builtin.sudo become – Substitute User DO — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sudo_become.html

**Contents:**
- ansible.builtin.sudo become – Substitute User DO
- Synopsis
- Parameters
  - Authors
  - Collection links

This become plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sudo. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sudo for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same become plugin name.

This become plugin allows your remote/login user to execute commands as another user via the sudo utility.

Environment variable: ANSIBLE_BECOME_EXE

Environment variable: ANSIBLE_SUDO_EXE

Variable: ansible_become_exe

Variable: ansible_sudo_exe

Options to pass to sudo

Environment variable: ANSIBLE_BECOME_FLAGS

Environment variable: ANSIBLE_SUDO_FLAGS

Keyword: become_flags

Variable: ansible_become_flags

Variable: ansible_sudo_flags

Password to pass to sudo

Environment variable: ANSIBLE_BECOME_PASS

Environment variable: ANSIBLE_SUDO_PASS

Variable: ansible_become_password

Variable: ansible_become_pass

Variable: ansible_sudo_pass

User you ‘become’ to execute the task

Environment variable: ANSIBLE_BECOME_USER

Environment variable: ANSIBLE_SUDO_USER

Variable: ansible_become_user

Variable: ansible_sudo_user

added in ansible-core 2.19

Directory to change to before invoking sudo; can avoid permission errors when dropping privileges.

Environment variable: ANSIBLE_SUDO_CHDIR

Variable: ansible_sudo_chdir

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[privilege_escalation]
become_exe = sudo
```

Example 2 (unknown):
```unknown
[sudo_become_plugin]
executable = sudo
```

Example 3 (unknown):
```unknown
[privilege_escalation]
become_flags = -H -S -n
```

Example 4 (unknown):
```unknown
[sudo_become_plugin]
flags = -H -S -n
```

---

## ansible.builtin.to_datetime filter – Get datetime from string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_datetime_filter.html

**Contents:**
- ansible.builtin.to_datetime filter – Get datetime from string
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_datetime. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_datetime for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Using the input string attempt to create a matching Python datetime object.

Adding or Subtracting two datetime objects will result in a Python timedelta object.

This describes the input of the filter, the value before | ansible.builtin.to_datetime.

A string containing date time information.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.to_datetime(key1=value1, key2=value2, ...)

strformat formatted string that describes the expected format of the input string.

For a full list of format codes for working with Python date format strings, see the Python documentation.

The timedelta object produced by the difference of two datetimes store the days, seconds, and microseconds of the delta. This results in the seconds attribute being the total seconds of the minutes and hours of that delta. See datatime.timedelta for more information about how a timedelta works.

datetime object from the represented value.

**Examples:**

Example 1 (unknown):
```unknown
# Get total amount of seconds between two dates. Default date format is %Y-%m-%d %H:%M:%S but you can pass your own format
secsdiff: '{{ (("2016-08-14 20:00:12" | to_datetime) - ("2015-12-25" | to_datetime("%Y-%m-%d"))).total_seconds()  }}'

# Get remaining seconds after delta has been calculated. NOTE: This does NOT convert years and days to seconds. For that, use total_seconds()
{{ (("2016-08-14 20:00:12" | to_datetime) - ("2016-08-14 18:00:00" | to_datetime)).seconds  }}
# This expression evaluates to "7212". Delta is 2 hours, 12 seconds

# get amount of days between two dates. This returns only number of days and discards remaining hours, minutes, and seconds
{{ (("2016-08-14 20:00:12" | to_datetime) - ("2015-12-25" | to_datetime('%Y-%m-%d'))).days  }}

# difference between to dotnet (100ns precision) and iso8601 microsecond timestamps
# the date1_short regex replace will work for any timestamp that has a higher than microsecond precision
# by cutting off anything more precise than microseconds
vars:
  date1: '2022-11-15T03:23:13.6869568Z'
  date2: '2021-12-15T16:06:24.400087Z'
  date1_short: '{{ date1|regex_replace("([^.]+)(\.\d{6})(\d*)(.+)", "\1\2\4") }}' # shorten to microseconds
  iso8601format: '%Y-%m-%dT%H:%M:%S.%fZ'
  date_diff_isoed: '{{ (date1_short|to_datetime(iso8601format) - date2|to_datetime(iso8601format)).total_seconds() }}'
```

---

## ansible.builtin.find module – Return a list of files based on specific criteria — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/find_module.html

**Contents:**
- ansible.builtin.find module – Return a list of files based on specific criteria
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name find even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.find for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Return a list of files based on specific criteria. Multiple criteria are AND’d together.

For Windows targets, use the ansible.windows.win_find module instead.

This module does not use the find command, it is a much simpler and slower Python implementation. It is intended for small and simple uses. Those that need the extra power or speed and have expertise with the UNIX command, should use it directly.

Select files whose age is equal to or greater than the specified time.

Use a negative age to find files equal to or less than the specified time.

You can choose seconds, minutes, hours, days, or weeks by specifying the first letter of any of those words (e.g., “1w”).

Choose the file property against which we compare age.

aliases: checksum, checksum_algo

added in ansible-core 2.19

Algorithm to determine checksum of file.

Will throw an error if the host is unable to use specified algorithm.

The remote host has to support the hashing method specified, md5 can be unavailable if the host is FIPS-140 compliant.

Availability might be restricted by the target system, for example FIPS systems won’t allow md5 use

A regular expression or pattern which should be matched against the file content.

If read_whole_file=false it matches against the beginning of the line (uses re.match()). If read_whole_file=true, it searches anywhere for that pattern (uses re.search()).

Works only when file_type is file.

Set the maximum number of levels to descend into.

Setting recurse=false will override this value, which is effectively depth 1.

Default is unlimited depth.

added in ansible-core 2.17

When doing a contains search, determine the encoding of the files to be searched.

added in ansible-core 2.16

Restrict mode matching to exact matches only, and not as a minimum set of permissions to match.

list / elements=string

One or more (shell or regex) patterns, which type is controlled by use_regex option.

Items whose basenames match an excludes pattern are culled from patterns matches. Multiple patterns can be specified using a list.

Type of file to select.

The link and any choices were added in Ansible 2.3.

Set this to true to follow symlinks in path for systems with python 2.6+.

Whether to return a checksum of the file.

Set this to true to include hidden files, otherwise they will be ignored.

added in ansible-core 2.18

Limit the maximum number of matching paths returned. After finding this many, the find action will stop looking.

Matches are made from the top, down (i.e. shallowest directory first).

If not set, or set to v(null), it will do unlimited matches.

Default is unlimited matches.

added in ansible-core 2.16

Choose objects matching a specified permission. This value is restricted to modes that can be applied using the python os.chmod function.

The mode can be provided as an octal such as "0644" or as symbolic such as u=rw,g=r,o=r.

list / elements=path / required

List of paths of directories to search. All paths must be fully qualified.

From ansible-core 2.18 and onwards, the data type has changed from str to path.

list / elements=string

One or more (shell or regex) patterns, which type is controlled by use_regex option.

The patterns restrict the list of files to be returned to those whose basenames match at least one of the patterns specified. Multiple patterns can be specified using a list.

The pattern is matched against the file base name, excluding the directory.

When using regexen, the pattern MUST match the ENTIRE file name, not just parts of it. So if you are looking to match all files ending in .default, you’d need to use .*\.default as a regexp and not just \.default.

This parameter expects a list, which can be either comma separated or YAML. If any of the patterns contain a comma, make sure to put them in a list to avoid splitting the patterns in undesirable ways.

Defaults to * when use_regex=False, or .* when use_regex=True.

added in ansible-core 2.11

When doing a contains search, determines whether the whole file should be read into memory or if the regex should be applied to the file line-by-line.

Setting this to true can have performance and memory implications for large files.

This uses re.search() instead of re.match().

If target is a directory, recursively descend into the directory looking for files.

Select files whose size is equal to or greater than the specified size.

Use a negative size to find files equal to or less than the specified size.

Unqualified values are in bytes but b, k, m, g, and t can be appended to specify bytes, kilobytes, megabytes, gigabytes, and terabytes, respectively.

Size is not evaluated for directories.

If false, the patterns are file globs (shell).

If true, they are python regexes.

since this action does not modify the target it just executes normally during check mode

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

The official documentation on the ansible.windows.win_find module.

Common return values are documented here, the following are the fields unique to this module:

Number of filesystem objects looked at

list / elements=string

All matches found with the specified criteria (see stat module for full output of each dictionary)

Sample: [{"...": "...", "checksum": "16fac7be61a6e4591a33ef4b729c5c3302307523", "mode": "0644", "path": "/var/tmp/test1"}, {"...": "...", "path": "/var/tmp/test2"}]

added in ansible-core 2.12

skipped paths and reasons they were skipped

Sample: {"/laskdfj": "'/laskdfj' is not a directory"}

**Examples:**

Example 1 (unknown):
```unknown
- name: Recursively find /tmp files older than 2 days
  ansible.builtin.find:
    paths: /tmp
    age: 2d
    recurse: yes

- name: Recursively find /tmp files older than 4 weeks and equal or greater than 1 megabyte
  ansible.builtin.find:
    paths: /tmp
    age: 4w
    size: 1m
    recurse: yes

- name: Recursively find /var/tmp files with last access time greater than 3600 seconds
  ansible.builtin.find:
    paths: /var/tmp
    age: 3600
    age_stamp: atime
    recurse: yes

- name: Find /var/log files equal or greater than 10 megabytes ending with .old or .log.gz
  ansible.builtin.find:
    paths: /var/log
    patterns: '*.old,*.log.gz'
    size: 10m

# Note that YAML double quotes require escaping backslashes but yaml single quotes do not.
- name: Find /var/log files equal or greater than 10 megabytes ending with .old or .log.gz via regex
  ansible.builtin.find:
    paths: /var/log
    patterns: "^.*?\\.(?:old|log\\.gz)$"
    size: 10m
    use_regex: yes

- name: Find /var/log all directories, exclude nginx and mysql
  ansible.builtin.find:
    paths: /var/log
    recurse: no
    file_type: directory
    excludes: 'nginx,mysql'

# When using patterns that contain a comma, make sure they are formatted as lists to avoid splitting the pattern
- name: Use a single pattern that contains a comma formatted as a list
  ansible.builtin.find:
    paths: /var/log
    file_type: file
    use_regex: yes
    patterns: ['^_[0-9]{2,4}_.*.log$']

- name: Use multiple patterns that contain a comma formatted as a YAML list
  ansible.builtin.find:
    paths: /var/log
    file_type: file
    use_regex: yes
    patterns:
      - '^_[0-9]{2,4}_.*.log$'
      - '^[a-z]{1,5}_.*log$'

- name: Find file containing "wally" without necessarily reading all files
  ansible.builtin.find:
    paths: /var/log
    file_type: file
    contains: wally
    read_whole_file: true
    patterns: "^.*\\.log$"
    use_regex: true
    recurse: true
    limit: 1
```

---

## ansible.builtin.unvault filter – Open an Ansible Vault — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/unvault_filter.html

**Contents:**
- ansible.builtin.unvault filter – Open an Ansible Vault
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name unvault. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.unvault for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.12

Positional parameters

Retrieve your information from an encrypted Ansible Vault.

This describes the input of the filter, the value before | ansible.builtin.unvault.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.unvault(positional1, positional2, ...)

Vault secret, the key that lets you open the vault.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.unvault(key1=value1, key2=value2, ...)

Secret identifier, used internally to try to best match a secret when multiple are provided.

Default: "filter_default"

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.unvault(positional1, positional2, key1=value1, key2=value2)

The string that was contained in the vault.

**Examples:**

Example 1 (unknown):
```unknown
# simply decrypt my key from a vault
vars:
  mykey: "{{ myvaultedkey | unvault(passphrase) }} "

- name: save templated unvaulted data
  template: src=dump_template_data.j2 dest=/some/key/clear.txt
  vars:
    template_data: '{{ secretdata | unvault(vaultsecret) }}'
```

---

## ansible.builtin.apt_repository module – Add and remove APT repositories — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/apt_repository_module.html

**Contents:**
- ansible.builtin.apt_repository module – Add and remove APT repositories
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name apt_repository even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.apt_repository for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Add or remove an APT repositories in Ubuntu and Debian.

The below requirements are needed on the host that executes this module.

Override the distribution codename to use for PPA repositories. Should usually only be set when working with a PPA on a non-Ubuntu target (for example, Debian or Mint).

Sets the name of the source list file in sources.list.d. Defaults to a file name based on the repository source url. The .list extension will be automatically added.

Whether to automatically try to install the Python apt library or not, if it is not already installed. Without this library, the module does not work.

Runs apt-get install python3-apt.

Only works with the system Python. If you are using a Python on the remote that is not the system Python, set install_python_apt=false and ensure that the Python apt library for your Python version is installed some other way.

The octal mode for newly created files in sources.list.d.

Default is what system uses (probably 0644).

A source string for the repository.

A source string state.

"present" ← (default)

aliases: update-cache

Run the equivalent of apt-get update when a change occurs. Cache updates are run after making changes.

added in ansible-base 2.10

Amount of retries if the cache update fails. Also see update_cache_retry_max_delay.

update_cache_retry_max_delay

added in ansible-base 2.10

Use an exponential backoff delay for each retry (see update_cache_retries) up to this max delay in seconds.

If false, SSL certificates for the target repo will not be validated. This should only be used on personally controlled sites using self-signed certificates.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

This module supports Debian Squeeze (version 6) as well as its successors and derivatives.

Add and remove deb822 formatted repositories.

Common return values are documented here, the following are the fields unique to this module:

A source string for the repository

Sample: "deb https://artifacts.elastic.co/packages/6.x/apt stable main"

list / elements=string

added in ansible-core 2.15

List of sources added

Returned: success, sources were added

Sample: ["/etc/apt/sources.list.d/artifacts_elastic_co_packages_6_x_apt.list"]

list / elements=string

added in ansible-core 2.15

List of sources removed

Returned: success, sources were removed

Sample: ["/etc/apt/sources.list.d/artifacts_elastic_co_packages_6_x_apt.list"]

Alexander Saltanov (@sashka)

**Examples:**

Example 1 (unknown):
```unknown
- name: Add specified repository into sources list
  ansible.builtin.apt_repository:
    repo: deb http://archive.canonical.com/ubuntu hardy partner
    state: present

- name: Add specified repository into sources list using specified filename
  ansible.builtin.apt_repository:
    repo: deb http://dl.google.com/linux/chrome/deb/ stable main
    state: present
    filename: google-chrome

- name: Add source repository into sources list
  ansible.builtin.apt_repository:
    repo: deb-src http://archive.canonical.com/ubuntu hardy partner
    state: present

- name: Remove specified repository from sources list
  ansible.builtin.apt_repository:
    repo: deb http://archive.canonical.com/ubuntu hardy partner
    state: absent

- name: Add nginx stable repository from PPA and install its signing key on Ubuntu target
  ansible.builtin.apt_repository:
    repo: ppa:nginx/stable

- name: Add nginx stable repository from PPA and install its signing key on Debian target
  ansible.builtin.apt_repository:
    repo: 'ppa:nginx/stable'
    codename: trusty

- name: One way to avoid apt_key once it is removed from your distro
  block:
    - name: somerepo |no apt key
      ansible.builtin.get_url:
        url: https://download.example.com/linux/ubuntu/gpg
        dest: /etc/apt/keyrings/somerepo.asc

    - name: somerepo | apt source
      ansible.builtin.apt_repository:
        repo: "deb [arch=amd64 signed-by=/etc/apt/keyrings/somerepo.asc] https://download.example.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present
```

---

## ansible.builtin.true test – Return true if the object is True. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/true_test.html

**Contents:**
- ansible.builtin.true test – Return true if the object is True.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name true. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.true for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is True.

This is the Jinja builtin test plugin ‘true’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.true

---

## ansible.builtin.any test – is any condition in a list true — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/any_test.html

**Contents:**
- ansible.builtin.any test – is any condition in a list true
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name any. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.any for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This test checks each condition in a list for truthiness.

Same as the any Python function.

This describes the input of the test, the value before is ansible.builtin.any or is not ansible.builtin.any.

list / elements=any / required

List of conditions, each can be a boolean or conditional expression that results in a boolean value.

Returns True if any element of the list was true, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
varexpression: "{{ 3 == 3 }}"
# is any statement true?
{{ [false, booleanvar, varexpression] is any}}
```

---

## Collection structure — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_structure.html

**Contents:**
- Collection structure
- Collection directories and files
  - galaxy.yml
  - docs directory
    - Plugin and module documentation
  - plugins directory
    - module_utils
  - roles directory
  - playbooks directory
  - tests directory

A collection is a simple data structure. None of the directories are required unless you have specific content that belongs in one of them. A collection does require a galaxy.yml file at the root level of the collection. This file contains all of the metadata that Galaxy and other tools need in order to package, build and publish the collection.

Collection directories and files

A collection can contain these directories and files:

Ansible only accepts .md extensions for the README file and any files in the /docs folder.

See the ansible-collections GitHub Org for examples of collection structure.

Not all directories are currently in use. Those are placeholders for future features.

A collection must have a galaxy.yml file that contains the necessary information to build a collection artifact. See Collection Galaxy metadata structure for details.

Use the docs folder to describe how to use the roles and plugins the collection provides, role requirements, and so on.

For certified collections, Automation Hub displays documents written in markdown in the main docs directory with no subdirectories. This documentation is not published to docs.ansible.com.

For community collections included in the Ansible PyPI package, docs.ansible.com displays documents written in reStructuredText (.rst) in a docsite/rst/ subdirectory. Define the structure of your extra documentation in docs/docsite/extra-docs.yml:

The index page of the documentation for your collection displays the title you define in docs/docsite/extra-docs.yml with a link to your extra documentation. For an example, see the community.docker collection repo and the community.docker collection documentation.

You can add extra links to your collection index page and plugin pages with the docs/docsite/links.yml file. This populates the links under Description and Communications headings as well as links at the end of the individual plugin pages. See the collection_template links.yml file for a complete description of the structure and use of this file to create links.

Keep the specific documentation for plugins and modules embedded as Python docstrings. Use ansible-doc to view documentation for plugins inside a collection:

The ansible-doc command requires the fully qualified collection name (FQCN) to display specific plugin documentation. In this example, my_namespace is the Galaxy namespace and my_collection is the collection name within that namespace.

The Galaxy namespace of an Ansible collection is defined in the galaxy.yml file. It can be different from the GitHub organization or repository name.

Add a ‘per plugin type’ specific subdirectory here, including module_utils which is usable not only by modules, but by most plugins by using their FQCN. This is a way to distribute modules, lookups, filters, and so on without having to import a role in every play.

Vars plugins in collections are not loaded automatically, and always require being explicitly enabled by using their fully qualified collection name. See Enabling vars plugins for details.

Cache plugins in collections may be used for fact caching, but are not supported for inventory plugins.

When coding with module_utils in a collection, the Python import statement needs to take into account the FQCN along with the ansible_collections convention. The resulting Python import will look like from ansible_collections.{namespace}.{collection}.plugins.module_utils.{util} import {something}

The following example snippets show a Python and PowerShell module using both default Ansible module_utils and those provided by a collection. In this example the namespace is community, the collection is test_collection. In the Python example the module_util in question is called qradar such that the FQCN is community.test_collection.plugins.module_utils.qradar:

Note that importing something from an __init__.py file requires using the file name:

In the PowerShell example the module_util in question is called hyperv such that the FQCN is community.test_collection.plugins.module_utils.hyperv:

Collection roles are mostly the same as existing roles, but with a couple of limitations:

Role names are now limited to contain only lowercase alphanumeric characters, plus _ and start with an alpha character.

Roles in a collection cannot contain plugins any more. Plugins must live in the collection plugins directory tree. Each plugin is accessible to all roles in the collection.

The directory name of the role is used as the role name. Therefore, the directory name must comply with the above role name rules. The collection import into Galaxy will fail if a role name does not comply with these rules.

You can migrate ‘traditional roles’ into a collection but they must follow the rules above. You may need to rename roles if they don’t conform. You will have to move or link any role-based plugins to the collection specific directories.

For roles imported into Galaxy directly from a GitHub repository, setting the role_name value in the role’s metadata overrides the role name used by Galaxy. For collections, that value is ignored. When importing a collection, Galaxy uses the role directory as the name of the role and ignores the role_name metadata value.

In prior releases, you could reference playbooks in this directory using the full path to the playbook file from the command line. In ansible-core 2.11 and later, you can use the FQCN, namespace.collection.playbook (with or without extension), to reference the playbooks from the command line or from import_playbook. This will keep the playbook in ‘collection context’, as if you had added collections: [ namespace.collection ] to it.

You can have most of the subdirectories you would expect, such files/, vars/ or templates/ but not roles/ since those are handled already in the collection.

Also, playbooks within a collection follow the same guidelines as any playbooks except for these few adjustments:

Directory: It must be in the playbooks/ directory.

Hosts: The host should be defined as a variable so the users of a playbook do not mistakenly run the plays against their entire inventory (if the host is set to all). For example - hosts: '{{target|default("all")}}'.

To run the plays, users can now use such commands as ansible-playbook --e 'targets=webservers' or ansible-playbook --limit webservers. Either way, the collection owner should document their playbooks and how to use them in the docs/ folder or README file.

Ansible Collections are tested much like Ansible itself, by using the ansible-test utility which is released as part of Ansible, version 2.9.0 and newer. Because Ansible Collections are tested using the same tooling as Ansible itself, by using the ansible-test, all Ansible developer documentation for testing is applicable for authoring Collections Tests with one key concept to keep in mind.

See Testing collections for specific information on how to test collections with ansible-test.

When reading the Testing Ansible documentation, there will be content that applies to running Ansible from source code through a Git clone, which is typical of an Ansible developer. However, it is not always typical for an Ansible Collection author to be running Ansible from source but instead from a stable release, and to create Collections it is not necessary to run Ansible from source. Therefore, when references of dealing with ansible-test binary paths, command completion, or environment variables are presented throughout the Testing Ansible documentation; keep in mind that it is not needed for Ansible Collection Testing because the act of installing the stable release of Ansible containing ansible-test is expected to setup those things for you.

A collection can store some additional metadata in a runtime.yml file in the collection’s meta directory. The runtime.yml file supports the top level keys:

The version of Ansible Core (ansible-core) required to use the collection. Multiple versions can be separated with a comma.

although the version is a PEP440 Version Specifier under the hood, Ansible deviates from PEP440 behavior by truncating prerelease segments from the Ansible version. This means that Ansible 2.11.0b1 is compatible with something that requires_ansible: ">=2.11".

Content in a collection that Ansible needs to load from another location or that has been deprecated/removed. The top level keys of plugin_routing are types of plugins, with individual plugin names as subkeys. To define a new location for a plugin, set the redirect field to another name. To deprecate a plugin, use the deprecation field to provide a custom warning message and the removal version or date. If the plugin has been renamed or moved to a new location, the redirect field should also be provided. If a plugin is being removed entirely, tombstone can be used for the fatal error message and removal version or date.

A mapping of names for Python import statements and their redirected locations.

A mapping of groups and the list of action plugin and module names they contain. They may also have a special ‘metadata’ dictionary in the list, which can be used to include actions from other groups.

If your collection has requirements, you can specify them in the execution-environment.yml file in the meta directory. This ensures users do not need to add these requirements manually when building Execution Environments containing your collection. See the collection-level metadata guide for details.

Learn how to package and publish your collection

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
collection/
├── docs/
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   ├── modules/
│   │   └── module1.py
│   ├── inventory/
│   └── .../
├── README.md
├── roles/
│   ├── role1/
│   ├── role2/
│   └── .../
├── playbooks/
│   ├── files/
│   ├── vars/
│   ├── templates/
│   └── tasks/
└── tests/
```

Example 2 (unknown):
```unknown
---
sections:
- title: Scenario Guide
  toctree:
    - scenario_guide
```

Example 3 (unknown):
```unknown
ansible-doc -t lookup my_namespace.my_collection.lookup1
```

Example 4 (python):
```python
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible.module_utils.six.moves.urllib.parse import urlencode, quote_plus
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.community.test_collection.plugins.module_utils.qradar import QRadarRequest

argspec = dict(
    name=dict(required=True, type='str'),
    state=dict(choices=['present', 'absent'], required=True),
)

module = AnsibleModule(
    argument_spec=argspec,
    supports_check_mode=True
)

qradar_request = QRadarRequest(
    module,
    headers={"Content-Type": "application/json"},
    not_rest_data_keys=['state']
)
```

---

## ansible.builtin.intersect filter – intersection of lists — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/intersect_filter.html

**Contents:**
- ansible.builtin.intersect filter – intersection of lists
- Synopsis
- Input
- Keyword parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name intersect. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.intersect for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Provide a list with the common elements from other lists.

Items in the resulting list are returned in arbitrary order.

This describes the input of the filter, the value before | ansible.builtin.intersect.

list / elements=string / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.intersect(key1=value1, key2=value2, ...)

list / elements=string / required

the difference of one list from another.

different items from two lists.

set of unique items of a list.

list / elements=string

A list with unique elements common to both lists, also known as a set.

**Examples:**

Example 1 (javascript):
```javascript
# return only the common elements of list1 and list2
# list1: [1, 2, 5, 3, 4, 10]
# list2: [1, 2, 3, 4, 5, 11, 99]
{{ list1 | intersect(list2) }}
# => [1, 2, 5, 3, 4]
```

---

## ansible.builtin.jsonfile cache – JSON formatted files. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/jsonfile_cache.html

**Contents:**
- ansible.builtin.jsonfile cache – JSON formatted files.
- Synopsis
- Parameters
  - Authors
  - Collection links

This cache plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name jsonfile. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.jsonfile for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same cache plugin name.

This cache uses JSON formatted, per host, files saved to the filesystem.

User defined prefix to use when creating the JSON files

Environment variable: ANSIBLE_CACHE_PLUGIN_PREFIX

Expiration timeout for the cache plugin data

Environment variable: ANSIBLE_CACHE_PLUGIN_TIMEOUT

Path in which the cache plugin will save the JSON files

Environment variable: ANSIBLE_CACHE_PLUGIN_CONNECTION

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

Ansible Core (@ansible-core)

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
fact_caching_prefix = VALUE
```

Example 2 (unknown):
```unknown
[defaults]
fact_caching_timeout = 86400
```

Example 3 (unknown):
```unknown
[defaults]
fact_caching_connection = VALUE
```

---

## ansible.builtin.reject filter – Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/reject_filter.html

**Contents:**
- ansible.builtin.reject filter – Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name reject. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.reject for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.

This is the Jinja builtin filter plugin ‘reject’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.reject

---

## ansible.builtin.b64decode filter – Decode a Base64 string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/b64decode_filter.html

**Contents:**
- ansible.builtin.b64decode filter – Decode a Base64 string
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name b64decode. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.b64decode for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Base64 decoding function.

The return value is a string.

Trying to store a binary blob in a string most likely corrupts the binary. To Base64 decode a binary blob, use the base64 command and pipe the encoded data through standard input. For example, in the ansible.builtin.shell module, ``cmd=”base64 --decode > myfile.bin” stdin=”{{ encoded }}”``.

This describes the input of the filter, the value before | ansible.builtin.b64decode.

A Base64 string to decode.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.b64decode(key1=value1, key2=value2, ...)

The encoding to use to transform from a text string to a byte string.

Defaults to using ‘utf-8’.

added in ansible-core 2.19

Decode string using URL- and filesystem-safe alphabet, which substitutes - instead of + and _ instead of / in the Base64 alphabet.

The contents of the Base64 encoded string.

**Examples:**

Example 1 (javascript):
```javascript
# Base64 decode a string
lola: "{{ 'bG9sYQ==' | b64decode }}"

# Base64 decode the content of 'b64stuff' variable
stuff: "{{ b64stuff | b64decode }}"

# Base64 decode the content with different encoding
stuff: "{{ 'QQBuAHMAaQBiAGwAZQAgAC0AIABPMIkwaDB/MAoA' | b64decode(encoding='utf-16-le') }}"
# => 'Ansible - くらとみ\n'

# URL-Safe Base64 decoding
stuff: "{{ 'aHR0cHM6Ly93d3cucHl0aG9uLm9yZy9leGFtcGxlLTE=' | b64decode(urlsafe=True) }}"
# => 'https://www.python.org/example-1'
```

---

## ansible.builtin.mount test – does the path resolve to mount point — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/mount_test.html

**Contents:**
- ansible.builtin.mount test – does the path resolve to mount point
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name mount. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.mount for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to a filesystem mount point on the controller (localhost).

This describes the input of the test, the value before is ansible.builtin.mount or is not ansible.builtin.mount.

Returns True if the path corresponds to a mount point on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
vars:
  ihopefalse: "{{ '/etc/hosts' is mount }}"
  normallytrue: "{{ '/tmp' is mount }}"
```

---

## ansible.builtin.ne test – Same as a . — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ne_test.html

**Contents:**
- ansible.builtin.ne test – Same as a .
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ne. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ne for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘ne’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.ne

---

## ansible.builtin.template lookup – retrieve contents of file after templating with Jinja2 — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/template_lookup.html

**Contents:**
- ansible.builtin.template lookup – retrieve contents of file after templating with Jinja2
- Synopsis
- Terms
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name template. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.template for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Returns a list of strings; for each template in the list of templates you pass in, returns a string containing the results of processing that template.

list of files to template

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.template', key1=value1, key2=value2, ...) and query('ansible.builtin.template', key1=value1, key2=value2, ...)

added in ansible-core 2.12

The string marking the end of a comment statement.

added in ansible-core 2.12

The string marking the beginning of a comment statement.

Removed in: version 2.23

Why: This option is no longer used in the Ansible Core code base.

Alternative: Jinja2 native mode is now the default and only option, which is mutually exclusive with this option.

Whether to convert YAML into data. If False, strings that are YAML will be left untouched.

Mutually exclusive with the jinja2_native option.

added in ansible-core 2.11

Removed in: version 2.23

Why: This option is no longer used in the Ansible Core code base.

Alternative: Jinja2 native mode is now the default and only option.

Controls whether to use Jinja2 native types.

It is off by default even if global jinja2_native is True.

Has no effect if global jinja2_native is False.

This offers more flexibility than the template module which does not use Jinja2 native types at all.

A dictionary, the keys become additional variables available for templating.

added in ansible-core 2.19

Determine when newlines should be removed from blocks.

When set to yes the first newline after a block is removed (block, not variable tag!).

The string marking the end of a print statement.

variable_start_string

The string marking the beginning of a print statement.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.template', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.template', term1, term2, key1=value1, key2=value2)

Search paths used for relative templates.

file(s) content after templating

**Examples:**

Example 1 (unknown):
```unknown
- name: show templating results
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.template', './some_template.j2') }}"

- name: show templating results with different variable start and end string
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.template', './some_template.j2', variable_start_string='[%', variable_end_string='%]') }}"

- name: show templating results with different comment start and end string
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.template', './some_template.j2', comment_start_string='[#', comment_end_string='#]') }}"

- name: show templating results with trim_blocks
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.template', './some_template.j2', trim_blocks=True) }}"
```

---

## ansible.builtin.float test – Return true if the object is a float. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/float_test.html

**Contents:**
- ansible.builtin.float test – Return true if the object is a float.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name float. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.float for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is a float.

This is the Jinja builtin test plugin ‘float’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.float

---

## ansible.builtin.superset test – is the list a superset of this other list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/superset_test.html

**Contents:**
- ansible.builtin.superset test – is the list a superset of this other list
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name superset. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.superset for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Validate if the first list is a super set (includes) the second list.

This describes the input of the test, the value before is ansible.builtin.superset or is not ansible.builtin.superset.

list / elements=any / required

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.superset(key1=value1, key2=value2, ...) and input is not ansible.builtin.superset(key1=value1, key2=value2, ...)

list / elements=any / required

List to test against.

Returns True if the specified list is a superset of the provided list, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
big: [1,2,3,4,5]
small: [3,4]
issmallinbig: '{{ big is superset(small) }}'
```

---

## ansible.builtin.copy module – Copy files to remote locations — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/copy_module.html

**Contents:**
- ansible.builtin.copy module – Copy files to remote locations
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name copy even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.copy for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.copy module copies a file or a directory structure from the local or remote machine to a location on the remote machine. File system meta-information (permissions, ownership, etc.) may be set, even when the file or directory already exists on the target system. Some meta-information may be copied on request.

Get meta-information with the ansible.builtin.stat module.

Set meta-information with the ansible.builtin.file module.

Use the ansible.builtin.fetch module to copy files from remote locations to the local box.

If you need variable interpolation in copied files, use the ansible.builtin.template module. Using a variable with the content parameter produces unpredictable results.

For Windows targets, use the ansible.windows.win_copy module instead.

This module has a corresponding action plugin.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

SHA1 checksum of the file being transferred.

Used to validate that the copy of the file was successful.

If this is not provided, ansible will use the local calculated checksum of the src file.

When used instead of src, sets the contents of a file directly to the specified value.

Works only when dest is a file. Creates the file if it does not exist.

For advanced formatting or if content contains a variable, use the ansible.builtin.template module.

This option controls the auto-decryption of source files using vault.

Remote absolute path where the file should be copied to.

If src is a directory, this must be a directory too.

If dest is a non-existent path and if either dest ends with / or src is a directory, dest is created.

If dest is a relative path, the starting directory is determined by the remote host.

If src and dest are files, the parent directory of dest is not created and the task fails if it does not already exist.

Set the access permissions of newly created directories to the given mode. Permissions on existing directories do not change.

See mode for the syntax of accepted values.

The target system’s defaults determine permissions when this parameter is not set.

This flag indicates that filesystem links in the destination, if they exist, should be followed.

Influence whether the remote file must always be replaced.

If true, the remote file will be replaced when contents are different than the source.

If false, the file will only be transferred if the destination does not exist.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

This flag indicates that filesystem links in the source tree, if they exist, should be followed.

The permissions of the destination file or directory.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must either add a leading zero so that Ansible’s YAML parser knows it is an octal number (like 0644 or 01777) or quote it (like '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Giving Ansible a number without following one of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

As of Ansible 2.3, the mode may also be the special string preserve.

preserve means that the file will be given the same permissions as the source file.

When doing a recursive copy, see also directory_mode.

If mode is not specified and the destination file does not exist, the default umask on the system will be used when setting the mode for the newly created file.

If mode is not specified and the destination file does exist, the mode of the existing file will be used.

Specifying mode is the best way to ensure files are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

Influence whether src needs to be transferred or already is present remotely.

If false, it will search for src on the controller node.

If true, it will search for src on the managed (remote) node.

remote_src supports recursive copying as of version 2.8.

remote_src only works with mode=preserve as of version 2.6.

Auto-decryption of files does not work when remote_src=yes.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Local path to a file to copy to the remote server.

This can be absolute or relative.

If path is a directory, it is copied recursively. In this case, if path ends with /, only inside contents of that directory are copied to destination. Otherwise, if it does not end with /, the directory itself with all contents is copied. This behavior is similar to the rsync command line tool.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying the updated file into the final destination.

A temporary file path is used to validate, passed in through %s which must be present as in the examples below.

Also, the command is passed securely so shell features such as expansion and pipes will not work.

For an example on how to handle more complex validation than what this option provides, see handling complex validation.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

The ansible.builtin.copy module recursively copy facility does not scale to lots (>hundreds) of files.

Assemble configuration files from fragments.

Fetch files from remote nodes.

Manage files and file properties.

Template a file out to a target host.

The official documentation on the ansible.posix.synchronize module.

The official documentation on the ansible.windows.win_copy module.

Common return values are documented here, the following are the fields unique to this module:

Name of backup file created.

Returned: changed and if backup=yes

Sample: "/path/to/file.txt.2015-02-12@22:09~"

SHA1 checksum of the file after running copy.

Sample: "6e642bb8dd5c2e027bf21dd923337cbb4214f827"

Destination file/path.

Sample: "/path/to/file.txt"

Group id of the file, after execution.

Group of the file, after execution.

MD5 checksum of the file after running copy.

Returned: when supported

Sample: "2a5aeecc61dc98c4d780b14b330e3282"

Permissions of the target, after execution.

Owner of the file, after execution.

Size of the target, after execution.

Source file used for the copy on the target machine.

Sample: "/home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source"

State of the target, after execution.

Owner id of the file, after execution.

**Examples:**

Example 1 (unknown):
```unknown
- name: Copy file with owner and permissions
  ansible.builtin.copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
    owner: foo
    group: foo
    mode: '0644'

- name: Copy file with owner and permission, using symbolic representation
  ansible.builtin.copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
    owner: foo
    group: foo
    mode: u=rw,g=r,o=r

- name: Another symbolic mode example, adding some permissions and removing others
  ansible.builtin.copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
    owner: foo
    group: foo
    mode: u+rw,g-wx,o-rwx

- name: Copy a new "ntp.conf" file into place, backing up the original if it differs from the copied version
  ansible.builtin.copy:
    src: /mine/ntp.conf
    dest: /etc/ntp.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes

- name: Copy a new "sudoers" file into place, after passing validation with visudo
  ansible.builtin.copy:
    src: /mine/sudoers
    dest: /etc/sudoers
    validate: /usr/sbin/visudo -csf %s

- name: Copy a "sudoers" file on the remote machine for editing
  ansible.builtin.copy:
    src: /etc/sudoers
    dest: /etc/sudoers.edit
    remote_src: yes
    validate: /usr/sbin/visudo -csf %s

- name: Copy using inline content
  ansible.builtin.copy:
    content: '# This file was moved to /etc/other.conf'
    dest: /etc/mine.conf

- name: If follow=yes, /path/to/file will be overwritten by contents of foo.conf
  ansible.builtin.copy:
    src: /etc/foo.conf
    dest: /path/to/link  # link to /path/to/file
    follow: yes

- name: If follow=no, /path/to/link will become a file and be overwritten by contents of foo.conf
  ansible.builtin.copy:
    src: /etc/foo.conf
    dest: /path/to/link  # link to /path/to/file
    follow: no
```

---

## ansible.builtin.zip filter – combine list elements — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/zip_filter.html

**Contents:**
- ansible.builtin.zip filter – combine list elements
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name zip. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.zip for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Iterate over several iterables in parallel, producing tuples with an item from each one.

This describes the input of the filter, the value before | ansible.builtin.zip.

list / elements=any / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.zip(positional1, positional2, ...)

list / elements=any / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.zip(key1=value1, key2=value2, ...)

If True return an error on mismatching list length, otherwise shortest list determines output.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.zip(positional1, positional2, key1=value1, key2=value2)

This is mostly a passthrough to Python’s zip function.

List of lists made of elements matching the positions of the input lists.

**Examples:**

Example 1 (javascript):
```javascript
# two => [[1, "a"], [2, "b"], [3, "c"], [4, "d"], [5, "e"], [6, "f"]]
two: "{{ [1,2,3,4,5,6] | zip(['a','b','c','d','e','f']) }}"

# three => [ [ 1, "a", "d" ], [ 2, "b", "e" ], [ 3, "c", "f" ] ]
three: "{{ [1,2,3] | zip(['a','b','c'], ['d','e','f']) }}"

# shorter => [[1, "a"], [2, "b"], [3, "c"]]
shorter: "{{ [1,2,3] | zip(['a','b','c','d','e','f']) }}"

# compose dict from lists of keys and values
mydict: "{{ dict(keys_list | zip(values_list)) }}"
```

---

## Installing collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_installing.html

**Contents:**
- Installing collections
- Installing collections in containers
- Installing collections with ansible-galaxy
- Installing collections with signature verification
- Installing an older version of a collection
- Install multiple collections with a requirements file
- Downloading a collection for offline use
- Installing collections adjacent to playbooks
- Installing a collection from source files
- Installing a collection from a Git repository

If you install a collection manually as described in this paragraph, the collection will not be upgraded automatically when you upgrade the ansible package or ansible-core.

You can install collections with their dependencies in containers known as Execution Environments. See Getting started with Execution Environments for details.

By default, ansible-galaxy collection install uses https://galaxy.ansible.com as the Galaxy server (as listed in the ansible.cfg file under GALAXY_SERVER). You do not need any further configuration. By default, Ansible installs the collection in ~/.ansible/collections under the ansible_collections directory.

See Configuring the ansible-galaxy client if you are using any other Galaxy server, such as Red Hat Automation Hub.

To install a collection hosted in Galaxy:

To upgrade a collection to the latest available version from the Galaxy server you can use the --upgrade option:

You can also directly use the tarball from your build:

You can build and install a collection from a local source directory. The ansible-galaxy utility builds the collection using the MANIFEST.json or galaxy.yml metadata in the directory.

You can also install multiple collections in a namespace directory.

The install command automatically appends the path ansible_collections to the one specified with the -p option unless the parent directory is already in a folder called ansible_collections.

When using the -p option to specify the install path, use one of the values configured in COLLECTIONS_PATHS, as this is where Ansible itself will expect to find collections. If you don’t specify a path, ansible-galaxy collection install installs the collection to the first path defined in COLLECTIONS_PATHS, which by default is ~/.ansible/collections

If a collection has been signed by a distribution server, the server will provide ASCII armored, detached signatures to verify the authenticity of the MANIFEST.json before using it to verify the collection’s contents. This option is not available on all distribution servers. See Distributing collections for a table listing the servers that support collection signing.

To use signature verification for signed collections:

Configured a GnuPG keyring for ansible-galaxy, or provide the path to the keyring with the --keyring option when you install the signed collection.

Import the public key from the distribution server into that keyring.

Verify the signature when you install the collection.

The --keyring option is not necessary if you have configured a GnuPG keyring.

Optionally, verify the signature at any point after installation to prove the collection has not been tampered with. See Verifying signed collections for details.

You can also include signatures in addition to those provided by the distribution server. Use the --signature option to verify the collection’s MANIFEST.json with these additional signatures. Supplemental signatures should be provided as URIs.

GnuPG verification only occurs for collections installed from a distribution server. User-provided signatures are not used to verify collections installed from Git repositories, source directories, or URLs/paths to tar.gz files.

You can also include additional signatures in the collection requirements.yml file under the signatures key.

See collection requirements file for details on how to install collections with this file.

By default, verification is considered successful if a minimum of 1 signature successfully verifies the collection. The number of required signatures can be configured with --required-valid-signature-count or GALAXY_REQUIRED_VALID_SIGNATURE_COUNT. All signatures can be required by setting the option to all. To fail signature verification if no valid signatures are found, prepend the value with +, such as +all or +1.

Certain GnuPG errors can be ignored with --ignore-signature-status-code or GALAXY_REQUIRED_VALID_SIGNATURE_COUNT. GALAXY_REQUIRED_VALID_SIGNATURE_COUNT should be a list, and --ignore-signature-status-code can be provided multiple times to ignore multiple additional error status codes.

This example requires any signatures provided by the distribution server to verify the collection except if they fail due to NO_PUBKEY:

If verification fails for the example above, only errors other than NO_PUBKEY will be displayed.

If verification is unsuccessful, the collection will not be installed. GnuPG signature verification can be disabled with --disable-gpg-verify or by configuring GALAXY_DISABLE_GPG_VERIFY.

You can only have one version of a collection installed at a time. By default, ansible-galaxy installs the latest available version. If you want to install a specific version, you can add a version range identifier. For example, to install the 1.0.0-beta.1 version of the collection:

You can specify multiple range identifiers separated by ,. Use single quotes so the shell passes the entire command, including >, !, and other operators, along. For example, to install the most recent version that is greater than or equal to 1.0.0 and less than 2.0.0:

Ansible will always install the most recent version that meets the range identifiers you specify. You can use the following range identifiers:

*: The most recent version. This is the default.

!=: Not equal to the version specified.

==: Exactly the version specified.

>=: Greater than or equal to the version specified.

>: Greater than the version specified.

<=: Less than or equal to the version specified.

<: Less than the version specified.

By default, ansible-galaxy ignores pre-release versions. To install a pre-release version, you must use the == range identifier to require it explicitly.

You can set up a requirements.yml file to install multiple collections in one command. This file is a YAML file in the format:

You can specify the following keys for each collection entry:

The version key uses the same range identifier format documented in Installing an older version of a collection.

The signatures key accepts a list of signature sources that are used to supplement those found on the Galaxy server during collection installation and ansible-galaxy collection verify. Signature sources should be URIs that contain the detached signature. The --keyring CLI option must be provided if signatures are specified.

Signatures are only used to verify collections on Galaxy servers. User-provided signatures are not used to verify collections installed from git repositories, source directories, or URLs/paths to tar.gz files.

The type key can be set to file, galaxy, git, url, dir, or subdirs. If type is omitted, the name key is used to implicitly determine the source of the collection.

When you install a collection with type: git, the version key can refer to a branch or to a git commit-ish object (commit or tag). For example:

You can also add roles to a requirements.yml file, under the roles key. The values follow the same format as a requirements file used in older Ansible releases.

To install both roles and collections at the same time with one command, run the following:

Running ansible-galaxy collection install -r or ansible-galaxy role install -r will only install collections, or roles respectively.

Installing both roles and collections from the same requirements file will not work when specifying a custom collection or role install path. In this scenario the collections will be skipped and the command will process each like ansible-galaxy role install would.

To download the collection tarball from Galaxy for offline use:

Navigate to the collection page.

Click on Download tarball.

You may also need to manually download any dependent collections.

You can install collections locally next to your playbooks inside your project instead of in a global location on your system or on AWX.

Using locally installed collections adjacent to playbooks has some benefits, such as:

Ensuring that all users of the project use the same collection version.

Using self-contained projects makes it easy to move across different environments. Increased portability also reduces overhead when setting up new environments. This is a benefit when deploying Ansible playbooks in cloud environments.

Managing collections locally lets you version them along with your playbooks.

Installing collections locally isolates them from global installations in environments that have multiple projects.

Here is an example of keeping a collection adjacent to the current playbook, under a collections/ansible_collections/ directory structure.

See Collection structure for details on the collection directory structure.

Ansible can also install from a source directory in several ways:

Ansible can also install a collection collected with ansible-galaxy collection build or downloaded from Galaxy for offline use by specifying the output file directly:

Relative paths are calculated from the current working directory (where you are invoking ansible-galaxy install -r from). They are not taken relative to the requirements.yml file.

You can install a collection from a git repository instead of from Galaxy or Automation Hub. As a developer, installing from a git repository lets you review your collection before you create the tarball and publish the collection. As a user, installing from a git repository lets you use collections or versions that are not in Galaxy or Automation Hub yet. This functionality is meant as a minimal shortcut for developers of content as previously described, and git repositories may not support the full set of features from the ansible-galaxy CLI. In complex cases, a more flexible option may be to git clone the repository into the correct file structure of the collection installation directory.

The repository must contain a galaxy.yml or MANIFEST.json file. This file provides metadata such as the version number and namespace of the collection.

To install a collection from a git repository at the command line, use the URI of the repository instead of a collection name or path to a tar.gz file. Use the prefix git+, unless you’re using SSH authentication with the user git (for example, git@github.com:ansible-collections/ansible.windows.git). You can specify a branch, commit, or tag using the comma-separated git commit-ish syntax.

Embedding credentials into a git URI is not secure. Use safe authentication options to prevent your credentials from being exposed in logs or elsewhere.

Use SSH authentication

Use netrc authentication

Use http.extraHeader in your git configuration

Use url.<base>.pushInsteadOf in your git configuration

When you install a collection from a git repository, Ansible uses the collection galaxy.yml or MANIFEST.json metadata file to build the collection. By default, Ansible searches two paths for collection galaxy.yml or MANIFEST.json metadata files:

The top level of the repository.

Each directory in the repository path (one level deep).

If a galaxy.yml or MANIFEST.json file exists in the top level of the repository, Ansible uses the collection metadata in that file to install an individual collection.

If a galaxy.yml or MANIFEST.json file exists in one or more directories in the repository path (one level deep), Ansible installs each directory with a metadata file as a collection. For example, Ansible installs both collection1 and collection2 from this repository structure by default:

If you have a different repository structure or only want to install a subset of collections, you can add a fragment to the end of your URI (before the optional comma-separated version) to indicate the location of the metadata file or files. The path should be a directory, not the metadata file itself. For example, to install only collection2 from the example repository with two collections:

In some repositories, the main directory corresponds to the namespace:

You can install all collections in this repository, or install one collection from a specific commit:

By default, ansible-galaxy uses https://galaxy.ansible.com as the Galaxy server (as listed in the ansible.cfg file under GALAXY_SERVER).

You can use either option below to configure ansible-galaxy collection to use other servers (such as a custom Galaxy server):

Set the server list in the GALAXY_SERVER_LIST configuration option in The configuration file.

Use the --server command line argument to limit to an individual server.

To configure a Galaxy server list in ansible.cfg:

Add the server_list option under the [galaxy] section to one or more server names.

Create a new section for each server name.

Set the url option for each server name.

Optionally, set the API token for each server name. Go to https://galaxy.ansible.com/me/preferences and click Show API key.

The url option for each server name must end with a forward slash /. If you do not set the API token in your Galaxy server list, use the --api-key argument to pass in the token to the ansible-galaxy collection publish command.

The following example shows how to configure multiple servers:

You can use the --server command line argument to select an explicit Galaxy server in the server_list and the value of this argument should match the name of the server. To use a server not in the server list, set the value to the URL to access that server (all servers in the server list will be ignored). Also you cannot use the --api-key argument for any of the predefined servers. You can only use the api_key argument if you did not define a server list or if you specify a URL in the --server argument.

Galaxy server list configuration options

The GALAXY_SERVER_LIST option is a list of server identifiers in a prioritized order. When searching for a collection, the install process will search in that order, for example, automation_hub first, then my_org_hub, release_galaxy, and finally test_galaxy until the collection is found. The actual Galaxy instance is then defined under the section [galaxy_server.{{ id }}] where {{ id }} is the server identifier defined in the list. This section can then define the following keys:

url: The URL of the Galaxy instance to connect to. Required.

token: An API token key to use for authentication against the Galaxy instance. Mutually exclusive with username.

username: The username to use for basic authentication against the Galaxy instance. Mutually exclusive with token.

password: The password to use, in conjunction with username, for basic authentication.

auth_url: The URL of a Keycloak server ‘token_endpoint’ if using SSO authentication (for example, galaxyNG). Mutually exclusive with username. Requires token.

validate_certs: Whether or not to verify TLS certificates for the Galaxy server. This defaults to True unless the --ignore-certs option is provided or GALAXY_IGNORE_CERTS is configured to True.

client_id: The Keycloak token’s client_id to use for authentication. Requires auth_url and token. The default client_id is cloud-services to work with Red Hat SSO.

timeout: The maximum number of seconds to wait for a response from the Galaxy server.

As well as defining these server options in the ansible.cfg file, you can also define them as environment variables. The environment variable is in the form ANSIBLE_GALAXY_SERVER_{{ id }}_{{ key }} where {{ id }} is the upper case form of the server identifier and {{ key }} is the key to define. For example, you can define token for release_galaxy by setting ANSIBLE_GALAXY_SERVER_RELEASE_GALAXY_TOKEN=secret_token.

For operations that use only one Galaxy server (for example, the publish, info, or install commands). the ansible-galaxy collection command uses the first entry in the server_list, unless you pass in an explicit server with the --server argument.

ansible-galaxy can seek out dependencies on other configured Galaxy instances to support the use case where a collection can depend on a collection from another Galaxy instance.

If you no longer need a collection, simply remove the installation directory from your filesystem. The path can be different depending on your operating system:

**Examples:**

Example 1 (unknown):
```unknown
ansible-galaxy collection install my_namespace.my_collection
```

Example 2 (unknown):
```unknown
ansible-galaxy collection install my_namespace.my_collection --upgrade
```

Example 3 (unknown):
```unknown
ansible-galaxy collection install my_namespace-my_collection-1.0.0.tar.gz -p ./collections
```

Example 4 (unknown):
```unknown
ansible-galaxy collection install /path/to/collection -p ./collections
```

---

## ansible.builtin.e filter – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/e_filter.html

**Contents:**
- ansible.builtin.e filter – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name e. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.e for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.

This is the Jinja builtin filter plugin ‘e’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.e

---

## ansible.builtin.paramiko_ssh connection – Run tasks via Python SSH (paramiko) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/paramiko_ssh_connection.html

**Contents:**
- ansible.builtin.paramiko_ssh connection – Run tasks via Python SSH (paramiko)
- Synopsis
- Parameters
  - Authors
  - Collection links

This connection plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name paramiko_ssh. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.paramiko_ssh for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same connection plugin name.

Use the Python SSH implementation (Paramiko) to connect to targets

The paramiko transport is provided because many distributions, in particular EL6 and before do not support ControlPersist in their SSH implementations.

This is needed on the Ansible control machine to be reasonably efficient with connections. Thus paramiko is faster for most users on these platforms. Users with ControlPersist capability can consider using -c ssh or configuring the transport in the configuration file.

This plugin also borrows a lot of settings from the ssh plugin as they both cover the same protocol.

added in ansible-core 2.14

Configures, in seconds, the amount of time to wait for the SSH banner to be presented. This option is supported by paramiko version 1.15.0 or newer.

Environment variable: ANSIBLE_PARAMIKO_BANNER_TIMEOUT

Automatically add host keys

Environment variable: ANSIBLE_PARAMIKO_HOST_KEY_AUTO_ADD

Set this to “False” if you want to avoid host key checking by the underlying tools Ansible uses to connect to the host

Environment variable: ANSIBLE_HOST_KEY_CHECKING

Environment variable: ANSIBLE_SSH_HOST_KEY_CHECKING

Environment variable: ANSIBLE_PARAMIKO_HOST_KEY_CHECKING

Variable: ansible_host_key_checking

Variable: ansible_ssh_host_key_checking

Variable: ansible_paramiko_host_key_checking

False to disable searching for private key files in ~/.ssh/

Environment variable: ANSIBLE_PARAMIKO_LOOK_FOR_KEYS

Secret used to either login the ssh server or as a passphrase for ssh keys that require it

Can be set from the CLI via the --ask-pass option.

Variable: ansible_password

Variable: ansible_ssh_pass

Variable: ansible_ssh_password

Variable: ansible_paramiko_pass

Variable: ansible_paramiko_password

Remote port to connect to.

added in ansible-core 2.15

Environment variable: ANSIBLE_REMOTE_PORT

Environment variable: ANSIBLE_REMOTE_PARAMIKO_PORT

added in ansible-core 2.15

Variable: ansible_port

Variable: ansible_ssh_port

Variable: ansible_paramiko_port

added in ansible-core 2.15

Path to private key file to use for authentication.

added in ansible-core 2.15

Environment variable: ANSIBLE_PRIVATE_KEY_FILE

Environment variable: ANSIBLE_PARAMIKO_PRIVATE_KEY_FILE

added in ansible-core 2.15

CLI argument: --private-key

Variable: ansible_private_key_file

Variable: ansible_ssh_private_key_file

Variable: ansible_paramiko_private_key_file

added in ansible-core 2.15

Proxy information for running the connection via a jumphost.

Environment variable: ANSIBLE_PARAMIKO_PROXY_COMMAND

Variable: ansible_paramiko_proxy_command

added in ansible-core 2.15

SUDO usually requires a PTY, True to give a PTY and False to not give a PTY.

Environment variable: ANSIBLE_PARAMIKO_PTY

Save the host keys to a file

Environment variable: ANSIBLE_PARAMIKO_RECORD_HOST_KEYS

Address of the remote target

Default: "inventory_hostname"

Variable: inventory_hostname

Variable: ansible_host

Variable: ansible_ssh_host

Variable: ansible_paramiko_host

User to login/authenticate as

Can be set from the CLI via the --user or -u options.

Environment variable: ANSIBLE_REMOTE_USER

Environment variable: ANSIBLE_PARAMIKO_REMOTE_USER

Variable: ansible_user

Variable: ansible_ssh_user

Variable: ansible_paramiko_user

Number of seconds until the plugin gives up on failing to establish a TCP connection.

added in ansible-core 2.11

added in ansible-core 2.15

Environment variable: ANSIBLE_TIMEOUT

Environment variable: ANSIBLE_SSH_TIMEOUT

added in ansible-core 2.11

Environment variable: ANSIBLE_PARAMIKO_TIMEOUT

added in ansible-core 2.15

CLI argument: --timeout

Variable: ansible_ssh_timeout

added in ansible-core 2.11

Variable: ansible_paramiko_timeout

added in ansible-core 2.15

use_persistent_connections

Toggles the use of persistence for connections

Environment variable: ANSIBLE_USE_PERSISTENT_CONNECTIONS

use_rsa_sha2_algorithms

added in ansible-core 2.14

Whether or not to enable RSA SHA2 algorithms for pubkeys and hostkeys

On paramiko versions older than 2.9, this only affects hostkeys

For behavior matching paramiko<2.9 set this to False

Environment variable: ANSIBLE_PARAMIKO_USE_RSA_SHA2_ALGORITHMS

Variable: ansible_paramiko_use_rsa_sha2_algorithms

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[paramiko_connection]
banner_timeout = 30.0
```

Example 2 (unknown):
```unknown
[paramiko_connection]
host_key_auto_add = VALUE
```

Example 3 (unknown):
```unknown
[defaults]
host_key_checking = true
```

Example 4 (unknown):
```unknown
[paramiko_connection]
host_key_checking = true
```

---

## ansible.builtin.yum module — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/yum_module.html

**Contents:**
- ansible.builtin.yum module

This redirect is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name yum even without specifying the collections keyword. Despite that, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.yum for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This is a redirect to the ansible.builtin.dnf module.

---

## ansible.builtin.le test – Same as a <= b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/le_test.html

**Contents:**
- ansible.builtin.le test – Same as a <= b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name le. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.le for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘le’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.le

---

## ansible.builtin.powershell shell – Windows PowerShell — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/powershell_shell.html

**Contents:**
- ansible.builtin.powershell shell – Windows PowerShell
- Synopsis
- Parameters
  - Collection links

This shell plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name powershell. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.powershell for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same shell plugin name.

The only option when using ‘winrm’ or ‘psrp’ as a connection plugin.

Can also be used when using ‘ssh’ as a connection plugin and the DefaultShell has been configured to PowerShell.

Aliases: formerly_core_powershell

Directory in which ansible will keep async job information.

Before Ansible 2.8, this was set to remote_tmp + "\.ansible_async".

Default: "%USERPROFILE%\\.ansible_async"

Variable: ansible_async_dir

Temporary directory to use on targets when copying files to the host.

Variable: ansible_remote_tmp

Controls if we set the locale for modules when executing on the target.

Windows only supports no as an option.

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[powershell]
async_dir = %USERPROFILE%\.ansible_async
```

Example 2 (unknown):
```unknown
[powershell]
remote_tmp = %TEMP%
```

---

## ansible.builtin.wordcount filter – Count the words in that string. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/wordcount_filter.html

**Contents:**
- ansible.builtin.wordcount filter – Count the words in that string.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name wordcount. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.wordcount for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Count the words in that string.

This is the Jinja builtin filter plugin ‘wordcount’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.wordcount

---

## ansible.builtin.relpath filter – Make a path relative — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/relpath_filter.html

**Contents:**
- ansible.builtin.relpath filter – Make a path relative
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name relpath. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.relpath for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Converts the given path to a relative path from the start, or relative to the directory given in start.

This describes the input of the filter, the value before | ansible.builtin.relpath.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.relpath(positional1, positional2, ...)

The directory the path should be relative to. If not supplied the current working directory will be used.

Jakub Jirutka (@jirutka)

**Examples:**

Example 1 (javascript):
```javascript
# foobar => ../test/me.txt
testing: "{{ '/tmp/test/me.txt' | relpath('/tmp/other/') }}"
otherrelpath: "{{ mypath | relpath(mydir) }}"
```

---

## ansible.builtin.first_found lookup – return first file found from list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/first_found_lookup.html

**Contents:**
- ansible.builtin.first_found lookup – return first file found from list
- Synopsis
- Terms
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name first_found. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.first_found for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

This lookup checks a list of files and paths and returns the full path to the first combination found.

As all lookups, when fed relative paths it will try use the current task’s location first and go up the chain to the containing locations of role / play / include and so on.

The list of files has precedence over the paths searched. For example, A task in a role has a ‘file1’ in the play’s relative path, this will be used, ‘file2’ in role’s relative path will not.

Either a list of files _terms or a key files with a list of files is required for this plugin to operate.

A list of file names.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.first_found', key1=value1, key2=value2, ...) and query('ansible.builtin.first_found', key1=value1, key2=value2, ...)

list / elements=string

A list of file names.

list / elements=string

A list of paths in which to look for the files.

When True, return an empty list when no files are matched.

This is useful when used with with_first_found, as an empty list return to with_ calls causes the calling task to be skipped.

When used as a template via lookup or query, setting skip=True will *not* cause the task to skip. Tasks must handle the empty list return from the template.

When False and lookup or query specifies errors='ignore' all errors (including no file found, but potentially others) return None or an empty list respectively.

When True and lookup or query specifies errors='ignore', no file found will return an empty list and other potential errors return None or empty list depending on the template call (in other words return values of lookup vs query).

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.first_found', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.first_found', term1, term2, key1=value1, key2=value2)

This lookup can be used in ‘dual mode’, either passing a list of file names or a dictionary that has files and paths.

Search paths used for relative paths/files.

**Examples:**

Example 1 (unknown):
```unknown
- name: Set _found_file to the first existing file, raising an error if a file is not found
  ansible.builtin.set_fact:
    _found_file: "{{ lookup('ansible.builtin.first_found', findme) }}"
  vars:
    findme:
      - /path/to/foo.txt
      - bar.txt  # will be looked in files/ dir relative to role and/or play
      - /path/to/biz.txt

- name: Set _found_file to the first existing file, or an empty list if no files found
  ansible.builtin.set_fact:
    _found_file: "{{ lookup('ansible.builtin.first_found', files, paths=['/extra/path'], skip=True) }}"
  vars:
    files:
      - /path/to/foo.txt
      - /path/to/bar.txt

- name: Include tasks only if one of the files exist, otherwise skip the task
  ansible.builtin.include_tasks:
    file: "{{ item }}"
  with_first_found:
    - files:
      - path/tasks.yaml
      - path/other_tasks.yaml
      skip: True

- name: Include tasks only if one of the files exists, otherwise skip
  ansible.builtin.include_tasks: '{{ tasks_file }}'
  when: tasks_file != ""
  vars:
    tasks_file: "{{ lookup('ansible.builtin.first_found', files=['tasks.yaml', 'other_tasks.yaml'], errors='ignore') }}"

- name: |
        copy first existing file found to /some/file,
        looking in relative directories from where the task is defined and
        including any play objects that contain it
  ansible.builtin.copy:
    src: "{{ lookup('ansible.builtin.first_found', findme) }}"
    dest: /some/file
  vars:
    findme:
      - foo
      - "{{ inventory_hostname }}"
      - bar

- name: same copy but specific paths
  ansible.builtin.copy:
    src: "{{ lookup('ansible.builtin.first_found', params) }}"
    dest: /some/file
  vars:
    params:
      files:
        - foo
        - "{{ inventory_hostname }}"
        - bar
      paths:
        - /tmp/production
        - /tmp/staging

- name: INTERFACES | Create Ansible header for /etc/network/interfaces
  ansible.builtin.template:
    src: "{{ lookup('ansible.builtin.first_found', findme)}}"
    dest: "/etc/foo.conf"
  vars:
    findme:
      - "{{ ansible_virtualization_type }}_foo.conf"
      - "default_foo.conf"

- name: read vars from first file found, use 'vars/' relative subdir
  ansible.builtin.include_vars: "{{lookup('ansible.builtin.first_found', params)}}"
  vars:
    params:
      files:
        - '{{ ansible_distribution }}.yml'
        - '{{ ansible_os_family }}.yml'
        - default.yml
      paths:
        - 'vars'
```

---

## ansible.builtin.urldecode filter – Decode percent-encoded sequences — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/urldecode_filter.html

**Contents:**
- ansible.builtin.urldecode filter – Decode percent-encoded sequences
- Synopsis
- Input
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name urldecode. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.urldecode for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Replace %xx escapes with their single-character equivalent in the given string.

Also replace plus signs with spaces, as required for unquoting HTML form values.

This describes the input of the filter, the value before | ansible.builtin.urldecode.

URL encoded string to decode.

URL decoded value for the given string

**Examples:**

Example 1 (javascript):
```javascript
# Decode urlencoded string
{{ '%7e/abc+def' | urldecode }}
# => "~/abc def"

# Decode plus sign as well
{{ 'El+Ni%C3%B1o' | urldecode }}
# => "El Niño"
```

---

## ansible.builtin.stat module – Retrieve file or file system status — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/stat_module.html

**Contents:**
- ansible.builtin.stat module – Retrieve file or file system status
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name stat even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.stat for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Retrieves facts for a file similar to the Linux/Unix stat command.

For Windows targets, use the ansible.windows.win_stat module instead.

aliases: checksum, checksum_algo

Algorithm to determine checksum of file.

Will throw an error if the host is unable to use specified algorithm.

The remote host has to support the hashing method specified, md5 can be unavailable if the host is FIPS-140 compliant.

Availability might be restricted by the target system, for example FIPS systems won’t allow md5 use

Whether to follow symlinks.

aliases: attr, attributes

Get file attributes using lsattr tool if present.

Whether to return a checksum of the file.

aliases: mime, mime_type, mime-type

Use file magic and return data about the nature of the file. This uses the file utility found on most Linux/Unix systems.

This will add both stat.mimetype and stat.charset fields to the return, if possible.

In Ansible 2.3 this option changed from mime to get_mime and the default changed to true.

The full path of the file/object to get the facts of.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Manage files and file properties.

The official documentation on the ansible.windows.win_stat module.

Common return values are documented here, the following are the fields unique to this module:

Dictionary containing all the stat data, some platforms might add additional fields.

Returned: success, path exists and user can read stats

Sample: 1424348972.575

list / elements=string

list of file attributes

Returned: success, path exists and user can execute the path

Sample: ["immutable", "extent"]

file character set or encoding

Returned: success, path exists and user can read stats and installed python supports it and the get_mime option was true, will return unknown on error.

Returned: success, path exists, user can read stats, path supports hashing and supplied checksum algorithm is available

Sample: "50ba294cdf28c0d5bcde25708df53346825a429f"

Time of last metadata update or creation (depends on OS)

Returned: success, path exists and user can read stats

Sample: 1424348972.575

Device the inode resides on

Returned: success, path exists and user can read stats

Tells you if the invoking user has execute permission on the path

Returned: success, path exists and user can execute the path

If the destination path actually exists or not

Numeric id representing the group of the owner

Returned: success, path exists and user can read stats

Returned: success, path exists, user can read stats, owner group can be looked up and installed python supports it

Inode number of the path

Returned: success, path exists and user can read stats

Tells you if the path is a block device

Returned: success, path exists and user can read stats

Tells you if the path is a character device

Returned: success, path exists and user can read stats

Tells you if the path is a directory

Returned: success, path exists and user can read stats

Tells you if the path is a named pipe

Returned: success, path exists and user can read stats

Tells you if the invoking user’s group id matches the owner’s group id

Returned: success, path exists and user can read stats

Tells you if the path is a symbolic link

Returned: success, path exists and user can read stats

Tells you if the path is a regular file

Returned: success, path exists and user can read stats

Tells you if the path is a unix domain socket

Returned: success, path exists and user can read stats

Tells you if the invoking user’s id matches the owner’s id

Returned: success, path exists and user can read stats

Target of the symlink normalized for the remote filesystem

Returned: success, path exists and user can read stats and the path is a symbolic link

Sample: "/home/foobar/21102015-1445431274-908472971"

Target of the symlink. Note that relative paths remain relative

Returned: success, path exists and user can read stats and the path is a symbolic link

Sample: "../foobar/21102015-1445431274-908472971"

file magic data or mime-type

Returned: success, path exists and user can read stats and installed python supports it and the get_mime option was true, will return unknown on error.

Sample: "application/pdf; charset=binary"

Unix permissions of the file in octal representation as a string

Returned: success, path exists and user can read stats

Time of last modification

Returned: success, path exists and user can read stats

Sample: 1424348972.575

Number of links to the inode (hard links)

Returned: success, path exists and user can read stats

The full path of the file/object to get the facts of

Returned: success and if path exists

Sample: "/path/to/file"

Returned: success, path exists, user can read stats, owner name can be looked up and installed python supports it

Tells you if the invoking user has the right to read the path

Returned: success, path exists and user can read the path

Tells you if the owner’s group has read permission

Returned: success, path exists and user can read stats

Tells you if others have read permission

Returned: success, path exists and user can read stats

Tells you if the owner has read permission

Returned: success, path exists and user can read stats

Size in bytes for a plain file, amount of data for some special files

Returned: success, path exists and user can read stats

Numeric id representing the file owner

Returned: success, path exists and user can read stats

The version/generation attribute of a file according to the filesystem

Returned: success, path exists, user can execute the path, lsattr is available and filesystem supports

Tells you if the owner’s group has write permission

Returned: success, path exists and user can read stats

Tells you if others have write permission

Returned: success, path exists and user can read stats

Tells you if the invoking user has the right to write the path

Returned: success, path exists and user can write the path

Tells you if the owner has write permission

Returned: success, path exists and user can read stats

Tells you if the owner’s group has execute permission

Returned: success, path exists and user can read stats

Tells you if others have execute permission

Returned: success, path exists and user can read stats

Tells you if the owner has execute permission

Returned: success, path exists and user can read stats

Bruce Pennypacker (@bpennypacker)

**Examples:**

Example 1 (unknown):
```unknown
# Obtain the stats of /etc/foo.conf, and check that the file still belongs
# to 'root'. Fail otherwise.
- name: Get stats of a file
  ansible.builtin.stat:
    path: /etc/foo.conf
  register: st
- name: Fail if the file does not belong to 'root'
  ansible.builtin.fail:
    msg: "Whoops! file ownership has changed"
  when: st.stat.pw_name != 'root'

# Determine if a path exists and is a symlink. Note that if the path does
# not exist, and we test sym.stat.islnk, it will fail with an error. So
# therefore, we must test whether it is defined.
# Run this to understand the structure, the skipped ones do not pass the
# check performed by 'when'
- name: Get stats of the FS object
  ansible.builtin.stat:
    path: /path/to/something
  register: sym

- name: Print a debug message
  ansible.builtin.debug:
    msg: "islnk isn't defined (path doesn't exist)"
  when: sym.stat.islnk is not defined

- name: Print a debug message
  ansible.builtin.debug:
    msg: "islnk is defined (path must exist)"
  when: sym.stat.islnk is defined

- name: Print a debug message
  ansible.builtin.debug:
    msg: "Path exists and is a symlink"
  when: sym.stat.islnk is defined and sym.stat.islnk

- name: Print a debug message
  ansible.builtin.debug:
    msg: "Path exists and isn't a symlink"
  when: sym.stat.islnk is defined and sym.stat.islnk == False


# Determine if a path exists and is a directory.  Note that we need to test
# both that p.stat.isdir actually exists, and also that it's set to true.
- name: Get stats of the FS object
  ansible.builtin.stat:
    path: /path/to/something
  register: p
- name: Print a debug message
  ansible.builtin.debug:
    msg: "Path exists and is a directory"
  when: p.stat.isdir is defined and p.stat.isdir

- name: Do not calculate the checksum
  ansible.builtin.stat:
    path: /path/to/myhugefile
    get_checksum: no

- name: Use sha256 to calculate the checksum
  ansible.builtin.stat:
    path: /path/to/something
    checksum_algorithm: sha256
```

---

## ansible.builtin.sequence lookup – generate a list based on a number sequence — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sequence_lookup.html

**Contents:**
- ansible.builtin.sequence lookup – generate a list based on a number sequence
- Synopsis
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sequence. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sequence for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

generates a sequence of items. You can specify a start value, an end value, an optional “stride” value that specifies the number of steps to increment the sequence, and an optional printf-style format string.

Arguments can be specified as key=value pair strings or as a shortcut form of the arguments string is also accepted: [start-]end[/stride][:format].

Numerical values can be specified in decimal, hexadecimal (0x3f8) or octal (0600).

Starting at version 1.9.2, negative strides are allowed.

Generated items are strings. Use Jinja2 filters to convert items to preferred type, e.g. {{ 1 + item|int }}.

See also Jinja2 range filter as an alternative.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.sequence', key1=value1, key2=value2, ...) and query('ansible.builtin.sequence', key1=value1, key2=value2, ...)

number of elements in the sequence, this is not to be used with end

number at which to end the sequence, dont use this with count

return a string with the generated number formatted in

number at which to start the sequence

increments between sequence numbers, the default is 1 unless the end is less than the start, then it is -1.

list / elements=string

A list containing generated sequence of items

**Examples:**

Example 1 (unknown):
```unknown
- name: create some test users
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    groups: "evens"
  with_sequence: start=0 end=32 format=testuser%02x

- name: create a series of directories with even numbers for some reason
  ansible.builtin.file:
    dest: "/var/stuff/{{ item }}"
    state: directory
  with_sequence: start=4 end=16 stride=2

- name: a simpler way to use the sequence plugin create 4 groups
  ansible.builtin.group:
    name: "group{{ item }}"
    state: present
  with_sequence: count=4

- name: the final countdown
  ansible.builtin.debug:
    msg: "{{item}} seconds to detonation"
  with_sequence: start=10 end=0 stride=-1

- name: Use of variable
  ansible.builtin.debug:
    msg: "{{ item }}"
  with_sequence: start=1 end="{{ end_at }}"
  vars:
    - end_at: 10
```

---

## ansible.builtin.abs test – is the path absolute — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/abs_test.html

**Contents:**
- ansible.builtin.abs test – is the path absolute
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name abs. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.abs for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path is absolute, not relative.

An absolute path expresses the location of a filesystem object starting at the filesystem root and requires no context.

A relative path does not start at the filesystem root and requires a ‘current’ directory as a context to resolve.

This describes the input of the test, the value before is ansible.builtin.abs or is not ansible.builtin.abs.

Returns True if the path is absolute, False if it is relative.

**Examples:**

Example 1 (unknown):
```unknown
is_path_absolute: "{{ '/etc/hosts' is abs }}}"
relative_paths: "{{ all_paths | reject('abs') }}"
```

---

## ansible.builtin.count filter – Return the number of items in a container. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/count_filter.html

**Contents:**
- ansible.builtin.count filter – Return the number of items in a container.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name count. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.count for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the number of items in a container.

This is the Jinja builtin filter plugin ‘count’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.count

---

## ansible.builtin.root filter – root of (math operation) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/root_filter.html

**Contents:**
- ansible.builtin.root filter – root of (math operation)
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name root. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.root for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Math operation that returns the Nth root of inputted number X ^^ N.

This describes the input of the filter, the value before | ansible.builtin.root.

Number to operate on.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.root(positional1, positional2, ...)

**Examples:**

Example 1 (javascript):
```javascript
# => 8
fiveroot: "{{ 32768 | root(5) }}"

# 2
sqrt_of_2: "{{ 4 | root }}"

# me ^^ 3
cuberoot_me: "{{ me | root(3) }}"
```

---

## ansible.builtin.regex_replace filter – replace a string via regex — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/regex_replace_filter.html

**Contents:**
- ansible.builtin.regex_replace filter – replace a string via regex
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name regex_replace. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.regex_replace for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Replace a substring defined by a regular expression with another defined by another regular expression based on the first match.

This describes the input of the filter, the value before | ansible.builtin.regex_replace.

String to match against.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.regex_replace(positional1, positional2, ...)

Regular expression string that defines the match.

Regular expression string that defines the replacement.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.regex_replace(key1=value1, key2=value2, ...)

added in ansible-core 2.17

Maximum number of pattern occurrences to replace. If zero, replace all occurrences.

Force the search to be case insensitive if True, case sensitive otherwise.

added in ansible-core 2.17

Except a certain number of replacements. Raises an error otherwise. If zero, ignore.

Search across line endings if True, do not if otherwise.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.regex_replace(positional1, positional2, key1=value1, key2=value2)

Maps to Python’s re.sub.

The substring matched by the group is accessible via the symbolic group name or the ``\{number}`` special sequence. See examples section.

String with substitution (or original if no match).

**Examples:**

Example 1 (javascript):
```javascript
# whatami => 'able'
whatami: "{{ 'ansible' | regex_replace('^a.*i(.*)$', 'a\\1') }}"

# commalocal => 'localhost, 80'
commalocal: "{{ 'localhost:80' | regex_replace('^(?P<host>.+):(?P<port>\\d+)$', '\\g<host>, \\g<port>') }}"

# piratecomment => '#CAR\n#tar\nfoo\n#bar\n'
piratecomment: "{{ 'CAR\ntar\nfoo\nbar\n' | regex_replace('^(.ar)$', '#\\1', multiline=True, ignorecase=True) }}"

# Using inline regex flags instead of passing options to filter
# See https://docs.python.org/3/library/re.html for more information
# on inline regex flags
# piratecomment => '#CAR\n#tar\nfoo\n#bar\n'
piratecomment: "{{ 'CAR\ntar\nfoo\nbar\n' | regex_replace('(?im)^(.ar)$', '#\\1') }}"

# 'foo=bar=baz' => 'foo:bar=baz'
key_value: "{{ 'foo=bar=baz' | regex_replace('=', ':', count=1) }}"
```

---

## ansible.builtin.to_nice_json filter – Convert variable to ‘nicely formatted’ JSON string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_nice_json_filter.html

**Contents:**
- ansible.builtin.to_nice_json filter – Convert variable to ‘nicely formatted’ JSON string
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_nice_json. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_nice_json for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts an Ansible variable into a ‘nicely formatted’ JSON string representation

This filter functions as a wrapper to the Python json.dumps function.

Ansible automatically converts JSON strings into variable structures so this plugin is used to forcibly retain a JSON string.

This describes the input of the filter, the value before | ansible.builtin.to_nice_json.

A variable or expression that returns a data structure.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.to_nice_json(key1=value1, key2=value2, ...)

When False, out-of-range float values nan, inf and -inf will result in an error.

When True, out-of-range float values will be represented using their JavaScript equivalents, NaN, Infinity and -Infinity.

Controls the usage of the internal circular reference detection, if off can result in overflow errors.

Escapes all non ASCII characters.

Specifies an indentation level. Passed to an underlying json.dumps call.

Toggle to represent unsafe values directly in JSON or create a unsafe object in JSON.

If True, keys that are not basic Python types will be skipped.

Affects sorting of dictionary keys. Passed to an underlying json.dumps call.

Toggle to either unvault a vault or create the JSON version of a vaulted object.

Both vault_to_text and preprocess_unsafe defaulted to False between Ansible 2.9 and 2.12.

These parameters to json.dumps will be ignored, they are overridden for internal use: cls, default, separators.

The ‘nicely formatted’ JSON serialized string representing the variable structure inputted.

**Examples:**

Example 1 (unknown):
```unknown
# dump variable in a template to create a nicely formatted JSON document
{{ docker_config | to_nice_json }}
```

---

## ansible.builtin.debconf module – Configure a .deb package — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/debconf_module.html

**Contents:**
- ansible.builtin.debconf module – Configure a .deb package
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name debconf even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.debconf for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Configure a .deb package using debconf-set-selections.

Or just query existing selections.

The below requirements are needed on the host that executes this module.

Name of package to configure.

aliases: selection, setting

A debconf configuration setting.

Do not set seen flag when pre-seeding.

Value to set the configuration to.

After Ansible 2.17, value is of type raw.

The type of the value supplied.

It is highly recommended to add no_log=True to task while specifying vtype=password.

seen was added in Ansible 2.2.

After Ansible 2.17, user can specify value as a list, if vtype is set as multiselect.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

This module requires the command line debconf tools.

Several questions have to be answered (depending on the package). Use ‘debconf-show <package>’ on any Debian or derivative with the package installed to see questions/settings available.

Some distros will always record tasks involving the setting of passwords as changed. This is due to debconf-get-selections masking passwords.

It is highly recommended to add no_log=True to the task while handling sensitive information using this module.

The ansible.builtin.debconf module does not reconfigure packages, it just updates the debconf database. An additional step is needed (typically with notify if debconf makes a change) to reconfigure the package and apply the changes. debconf is extensively used for pre-seeding configuration prior to installation rather than modifying configurations. So, while dpkg-reconfigure does use debconf data, it is not always authoritative and you may need to check how your package is handled.

Also note dpkg-reconfigure is a 3-phase process. It invokes the control scripts from the /var/lib/dpkg/info directory with the <package>.prerm reconfigure <version>, <package>.config reconfigure <version> and <package>.postinst control <version> arguments.

The main issue is that the <package>.config reconfigure step for many packages will first reset the debconf database (overriding changes made by this module) by checking the on-disk configuration. If this is the case for your package then dpkg-reconfigure will effectively ignore changes made by debconf.

However as dpkg-reconfigure only executes the <package>.config step if the file exists, it is possible to rename it to /var/lib/dpkg/info/<package>.config.ignore before executing dpkg-reconfigure -f noninteractive <package> and then restore it. This seems to be compliant with Debian policy for the .config file.

**Examples:**

Example 1 (unknown):
```unknown
- name: Set default locale to fr_FR.UTF-8
  ansible.builtin.debconf:
    name: locales
    question: locales/default_environment_locale
    value: fr_FR.UTF-8
    vtype: select

- name: Set to generate locales
  ansible.builtin.debconf:
    name: locales
    question: locales/locales_to_be_generated
    value: en_US.UTF-8 UTF-8, fr_FR.UTF-8 UTF-8
    vtype: multiselect

- name: Accept oracle license
  ansible.builtin.debconf:
    name: oracle-java7-installer
    question: shared/accepted-oracle-license-v1-1
    value: 'true'
    vtype: select

- name: Specifying package you can register/return the list of questions and current values
  ansible.builtin.debconf:
    name: tzdata

- name: Pre-configure tripwire site passphrase
  ansible.builtin.debconf:
    name: tripwire
    question: tripwire/site-passphrase
    value: "{{ site_passphrase }}"
    vtype: password
  no_log: True
```

---

## ansible.builtin.runas become – Run As user — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/runas_become.html

**Contents:**
- ansible.builtin.runas become – Run As user
- Synopsis
- Parameters
- Notes
  - Authors
  - Collection links

This become plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name runas. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.runas for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same become plugin name.

This become plugin allows your remote/login user to execute commands as another user via the windows runas facility.

Options to pass to runas, a space delimited list of k=v pairs

Environment variable: ANSIBLE_BECOME_FLAGS

Environment variable: ANSIBLE_RUNAS_FLAGS

Keyword: become_flags

Variable: ansible_become_flags

Variable: ansible_runas_flags

Environment variable: ANSIBLE_BECOME_PASS

Environment variable: ANSIBLE_RUNAS_PASS

Variable: ansible_become_password

Variable: ansible_become_pass

Variable: ansible_runas_pass

User you ‘become’ to execute the task

Environment variable: ANSIBLE_BECOME_USER

Environment variable: ANSIBLE_RUNAS_USER

Variable: ansible_become_user

Variable: ansible_runas_user

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

runas is really implemented in the powershell module handler and as such can only be used with winrm connections.

This plugin ignores the ‘become_exe’ setting as it uses an API and not an executable.

The Secondary Logon service (seclogon) must be running to use runas

**Examples:**

Example 1 (unknown):
```unknown
[privilege_escalation]
become_flags = ""
```

Example 2 (unknown):
```unknown
[runas_become_plugin]
flags = ""
```

Example 3 (unknown):
```unknown
[runas_become_plugin]
password = VALUE
```

Example 4 (unknown):
```unknown
[privilege_escalation]
become_user = VALUE
```

---

## ansible.builtin.package_facts module – Package information as facts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/package_facts_module.html

**Contents:**
- ansible.builtin.package_facts module – Package information as facts
- Synopsis
- Requirements
- Parameters
- Attributes
- Examples
- Returned Facts
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name package_facts even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.package_facts for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Return information about installed packages as facts.

The below requirements are needed on the host that executes this module.

See details per package manager in the manager option.

list / elements=string

The package manager(s) used by the system so we can query the package information. This is a list and can support multiple package managers per system, since version 2.8.

The portage and pkg options were added in version 2.8.

The apk option was added in version 2.11.

The pkg_info‘ option was added in version 2.13.

Aliases were added in 2.18, to support using manager={{ansible_facts['pkg_mgr']}}

"apk": Alpine Linux package manager

"apt": For DEB based distros, python-apt package must be installed on targeted hosts

"auto" (default): Depending on strategy, will match the first or all package managers provided, in order

"openbsd_pkg": Alias to pkg_info

"pacman": Archlinux package manager/builder

"pkg": libpkg front end (FreeBSD)

"pkg_info": OpenBSD package manager

"pkgng": Alias to pkg

"portage": Handles ebuild packages, it requires the qlist utility, which is part of ‘app-portage/portage-utils’

"rpm": For RPM based distros, requires RPM Python bindings, not installed by default on Suse or Fedora 41+ (python3-rpm)

"zypper": Alias to rpm

This option controls how the module queries the package managers on the system.

"all": returns information for all supported and available package managers on the system.

"first" (default): returns only information for the first supported package manager available.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

Target OS/families that can be operated against

Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.

Maps the package name to a non-empty list of dicts with package information.

Every dict in the list corresponds to one installed version of the package.

The fields described below are present for all package managers. Depending on the package manager, there might be more fields for a package.

Returned: when operating system level package manager is specified or auto detected manager

Sample: "{\n \"packages\": {\n \"kernel\": [\n {\n \"name\": \"kernel\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\",\n ...\n },\n {\n \"name\": \"kernel\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\",\n ...\n },\n ...\n ],\n \"kernel-tools\": [\n {\n \"name\": \"kernel-tools\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\",\n ...\n }\n ],\n ...\n }\n}\n# Sample rpm\n{\n \"packages\": {\n \"kernel\": [\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel\",\n \"release\": \"514.26.2.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n },\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel\",\n \"release\": \"514.16.1.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n },\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel\",\n \"release\": \"514.10.2.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n },\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel\",\n \"release\": \"514.21.1.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n },\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel\",\n \"release\": \"693.2.2.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n }\n ],\n \"kernel-tools\": [\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel-tools\",\n \"release\": \"693.2.2.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n }\n ],\n \"kernel-tools-libs\": [\n {\n \"arch\": \"x86_64\",\n \"epoch\": null,\n \"name\": \"kernel-tools-libs\",\n \"release\": \"693.2.2.el7\",\n \"source\": \"rpm\",\n \"version\": \"3.10.0\"\n }\n ],\n }\n}\n# Sample deb\n{\n \"packages\": {\n \"libbz2-1.0\": [\n {\n \"version\": \"1.0.6-5\",\n \"source\": \"apt\",\n \"arch\": \"amd64\",\n \"name\": \"libbz2-1.0\"\n }\n ],\n \"patch\": [\n {\n \"version\": \"2.7.1-4ubuntu1\",\n \"source\": \"apt\",\n \"arch\": \"amd64\",\n \"name\": \"patch\"\n }\n ],\n }\n}\n# Sample pkg_info\n{\n \"packages\": {\n \"curl\": [\n {\n \"name\": \"curl\",\n \"source\": \"pkg_info\",\n \"version\": \"7.79.0\"\n }\n ],\n \"intel-firmware\": [\n {\n \"name\": \"intel-firmware\",\n \"source\": \"pkg_info\",\n \"version\": \"20210608v0\"\n }\n ],\n }\n}"

Where information on the package came from.

The package’s version.

Matthew Jones (@matburt)

Adam Miller (@maxamillion)

**Examples:**

Example 1 (unknown):
```unknown
- name: Gather the package facts
  ansible.builtin.package_facts:
    manager: auto

- name: Print the package facts
  ansible.builtin.debug:
    var: ansible_facts.packages

- name: Check whether a package called foobar is installed
  ansible.builtin.debug:
    msg: "{{ ansible_facts.packages['foobar'] | length }} versions of foobar are installed!"
  when: "'foobar' in ansible_facts.packages"
```

---

## ansible.builtin.regex_escape filter – escape regex chars — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/regex_escape_filter.html

**Contents:**
- ansible.builtin.regex_escape filter – escape regex chars
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name regex_escape. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.regex_escape for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Escape special characters in a string for use in a regular expression.

This describes the input of the filter, the value before | ansible.builtin.regex_escape.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.regex_escape(positional1, positional2, ...)

Which type of escaping to use.

posix_extended is not implemented yet

**Examples:**

Example 1 (javascript):
```javascript
# safe_for_regex => '\^f\.\*o\(\.\*\)\$'
safe_for_regex: "{{ '^f.*o(.*)$' | regex_escape() }}"
```

---

## ansible.builtin.tree callback – Save host events to files — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/tree_callback.html

**Contents:**
- ansible.builtin.tree callback – Save host events to files
- Callback plugin
- Synopsis
- Requirements
- Parameters
  - Collection links

This callback plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name tree. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.tree for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same callback plugin name.

This plugin is a notification callback. It sends information for a playbook run to other applications, services, or systems. See Callback plugins for more information on callback plugins.

This callback is used by the Ansible (adhoc) command line option -t|--tree.

This produces a JSON dump of events in a directory, a file for each host, the directory used MUST be passed as a command line option.

The below requirements are needed on the local controller node that executes this callback.

invoked in the command line

added in ansible-core 2.11

directory that will contain the per host JSON files. Also set by the --tree option when using adhoc.

Default: "~/.ansible/tree"

Environment variable: ANSIBLE_CALLBACK_TREE_DIR

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[callback_tree]
directory = ~/.ansible/tree
```

---

## ansible.builtin.oneline callback – oneline Ansible screen output — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/oneline_callback.html

**Contents:**
- ansible.builtin.oneline callback – oneline Ansible screen output
- Callback plugin
- Synopsis
  - Collection links

This callback plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name oneline. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.oneline for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same callback plugin name.

This plugin is a stdout callback. You can use only use one stdout callback at a time. Additional aggregate or notification callbacks can be enabled though. See Callback plugins for more information on callback plugins.

This is the output callback used by the -o/--one-line command line option.

---

## ansible.builtin.length filter – Return the number of items in a container. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/length_filter.html

**Contents:**
- ansible.builtin.length filter – Return the number of items in a container.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name length. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.length for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the number of items in a container.

This is the Jinja builtin filter plugin ‘length’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.length

---

## ansible.builtin.human_readable filter – Make bytes/bits human-readable — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/human_readable_filter.html

**Contents:**
- ansible.builtin.human_readable filter – Make bytes/bits human-readable
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name human_readable. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.human_readable for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Convert byte or bit figures to more human-readable formats.

This describes the input of the filter, the value before | ansible.builtin.human_readable.

Number of bytes, or bits. Depends on isbits.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.human_readable(positional1, positional2, ...)

Whether the input is bits, instead of bytes.

Unit to force output into. If none specified the largest unit arrived at will be used.

human-readable byte or bit size.

**Examples:**

Example 1 (javascript):
```javascript
# size => "1.15 GB"
size: "{{ 1232345345 | human_readable }}"

# size => "1.15 Gb"
size_bits: "{{ 1232345345 | human_readable(true) }}"

# size => "1175.26 MB"
size_MB: "{{ 1232345345 | human_readable(unit='M') }}"
```

---

## ansible.builtin.nested lookup – composes a list with nested elements of other lists — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/nested_lookup.html

**Contents:**
- ansible.builtin.nested lookup – composes a list with nested elements of other lists
- Synopsis
- Keyword parameters
- Examples
- Return Value
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name nested. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.nested for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Takes the input lists and returns a list with elements that are lists composed of the elements of the input lists

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.nested', key1=value1, key2=value2, ...) and query('ansible.builtin.nested', key1=value1, key2=value2, ...)

list / elements=string

A list composed of lists paring the elements of the input lists

**Examples:**

Example 1 (unknown):
```unknown
- name: give users access to multiple databases
  community.mysql.mysql_user:
    name: "{{ item[0] }}"
    priv: "{{ item[1] }}.*:ALL"
    append_privs: yes
    password: "foo"
  with_nested:
    - [ 'alice', 'bob' ]
    - [ 'clientdb', 'employeedb', 'providerdb' ]
# As with the case of 'with_items' above, you can use previously defined variables.:

- name: here, 'users' contains the above list of employees
  community.mysql.mysql_user:
    name: "{{ item[0] }}"
    priv: "{{ item[1] }}.*:ALL"
    append_privs: yes
    password: "foo"
  with_nested:
    - "{{ users }}"
    - [ 'clientdb', 'employeedb', 'providerdb' ]
```

---

## ansible.builtin.difference filter – the difference of one list from another — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/difference_filter.html

**Contents:**
- ansible.builtin.difference filter – the difference of one list from another
- Synopsis
- Input
- Keyword parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name difference. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.difference for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Provide a unique list of all the elements of the first list that do not appear in the second one.

Items in the resulting list are returned in arbitrary order.

This describes the input of the filter, the value before | ansible.builtin.difference.

list / elements=string / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.difference(key1=value1, key2=value2, ...)

list / elements=string / required

intersection of lists.

different items from two lists.

set of unique items of a list.

list / elements=string

A unique list of the elements from the first list that do not appear on the second.

**Examples:**

Example 1 (javascript):
```javascript
# return the elements of list1 not in list2
# list1: [1, 2, 5, 1, 3, 4, 10]
# list2: [1, 2, 3, 4, 5, 11, 99]
{{ list1 | difference(list2) }}
# => [10]
```

---

## ansible.builtin.import_role module – Import a role into a play — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/import_role_module.html

**Contents:**
- ansible.builtin.import_role module – Import a role into a play
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name import_role even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.import_role for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Much like the roles: keyword, this task loads a role, but it allows you to control when the role tasks run in between other tasks of the play.

Most keywords, loops and conditionals will only be applied to the imported tasks, not to this statement itself. If you want the opposite behavior, use ansible.builtin.include_role instead.

Does not work in handlers.

Overrides the role’s metadata setting to allow using a role more than once with the same parameters.

File to load from a role’s defaults/ directory.

File to load from a role’s handlers/ directory.

The name of the role to be executed.

added in ansible-core 2.17

This option dictates whether the role’s vars and defaults are exposed to the play.

Variables are exposed to the play at playbook parsing time, and available to earlier roles and tasks as well unlike include_role.

The default depends on the configuration option DEFAULT_PRIVATE_ROLE_VARS.

added in ansible-core 2.11

Perform role argument spec validation if an argument spec is defined.

File to load from a role’s tasks/ directory.

File to load from a role’s vars/ directory.

While this action executes locally on the controller it is not governed by an action plugin

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

While the import can be host specific and runs per host it is not dealing with all available host variables, use an include instead for those cases

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

The task itself is not looped, but the loop is applied to each imported task

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Since there are no connection nor facts, there is no sense in delegating imports

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

While the action itself will ignore the conditional, it will be inherited by the imported tasks themselves

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Tags are not interpreted for this action, they are applied to the imported tasks

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Handlers are made available to the whole play.

Since Ansible 2.7 variables defined in vars and defaults for the role are exposed to the play at playbook parsing time. Due to this, these variables will be accessible to roles and tasks executed before the location of the ansible.builtin.import_role task.

Unlike ansible.builtin.include_role variable exposure is not configurable, and will always be exposed.

Load and execute a role.

Dynamically include a task list.

More information related to including and importing playbooks, roles and tasks.

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- hosts: all
  tasks:
    - ansible.builtin.import_role:
        name: myrole

    - name: Run tasks/other.yaml instead of 'main'
      ansible.builtin.import_role:
        name: myrole
        tasks_from: other

    - name: Pass variables to role
      ansible.builtin.import_role:
        name: myrole
      vars:
        rolevar1: value from task

    - name: Apply condition to each task in role
      ansible.builtin.import_role:
        name: myrole
      when: not idontwanttorun
```

---

## ansible.builtin.subelements lookup – traverse nested key from a list of dictionaries — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/subelements_lookup.html

**Contents:**
- ansible.builtin.subelements lookup – traverse nested key from a list of dictionaries
- Synopsis
- Terms
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name subelements. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.subelements for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Subelements walks a list of hashes (aka dictionaries) and then traverses a list with a given (nested sub-)key inside of those records.

tuple of list of dictionaries and dictionary key to extract

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.subelements', key1=value1, key2=value2, ...) and query('ansible.builtin.subelements', key1=value1, key2=value2, ...)

Lookup accepts this flag from a dictionary as optional. See Example section for more information.

If set to True, the lookup plugin will skip the lists items that do not contain the given subkey.

If set to False, the plugin will yield an error and complain about the missing subkey.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.subelements', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.subelements', term1, term2, key1=value1, key2=value2)

list of subelements extracted

Serge van Ginderachter

**Examples:**

Example 1 (unknown):
```unknown
- name: show var structure as it is needed for example to make sense
  hosts: all
  vars:
    users:
      - name: alice
        authorized:
          - /tmp/alice/onekey.pub
          - /tmp/alice/twokey.pub
        mysql:
            password: mysql-password
            hosts:
              - "%"
              - "127.0.0.1"
              - "::1"
              - "localhost"
            privs:
              - "*.*:SELECT"
              - "DB1.*:ALL"
        groups:
          - wheel
      - name: bob
        authorized:
          - /tmp/bob/id_rsa.pub
        mysql:
            password: other-mysql-password
            hosts:
              - "db1"
            privs:
              - "*.*:SELECT"
              - "DB2.*:ALL"
  tasks:
    - name: Set authorized ssh key, extracting just that data from 'users'
      ansible.posix.authorized_key:
        user: "{{ item.0.name }}"
        key: "{{ lookup('file', item.1) }}"
      with_subelements:
         - "{{ users }}"
         - authorized

    - name: Setup MySQL users, given the mysql hosts and privs subkey lists
      community.mysql.mysql_user:
        name: "{{ item.0.name }}"
        password: "{{ item.0.mysql.password }}"
        host: "{{ item.1 }}"
        priv: "{{ item.0.mysql.privs | join('/') }}"
      with_subelements:
        - "{{ users }}"
        - mysql.hosts

    - name: list groups for users that have them, don't error if groups key is missing
      ansible.builtin.debug: var=item
      loop: "{{ q('ansible.builtin.subelements', users, 'groups', {'skip_missing': True}) }}"
```

---

## ansible.builtin.tempfile module – Creates temporary files and directories — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/tempfile_module.html

**Contents:**
- ansible.builtin.tempfile module – Creates temporary files and directories
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name tempfile even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.tempfile for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.tempfile module creates temporary files and directories. mktemp command takes different parameters on various systems, this module helps to avoid troubles related to that. Files/directories created by module are accessible only by creator. In case you need to make them world-accessible you need to use ansible.builtin.file module.

For Windows targets, use the ansible.windows.win_tempfile module instead.

Location where temporary file or directory should be created.

If path is not specified, the default system temporary directory will be used.

Prefix of file/directory name created by module.

Whether to create file or directory.

Suffix of file/directory name created by module.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Manage files and file properties.

The official documentation on the ansible.windows.win_tempfile module.

Common return values are documented here, the following are the fields unique to this module:

Path to created file or directory.

Sample: "/tmp/ansible.bMlvdk"

Krzysztof Magosa (@krzysztof-magosa)

**Examples:**

Example 1 (unknown):
```unknown
- name: Create temporary build directory
  ansible.builtin.tempfile:
    state: directory
    suffix: build

- name: Create temporary file
  ansible.builtin.tempfile:
    state: file
    suffix: temp
  register: tempfile_1

- name: Create a temporary file with a specific prefix
  ansible.builtin.tempfile:
     state: file
     suffix: txt
     prefix: myfile_

- name: Use the registered var and the file module to remove the temporary file
  ansible.builtin.file:
    path: "{{ tempfile_1.path }}"
    state: absent
  when: tempfile_1.path is defined
```

---

## ansible.builtin.winrm connection – Run tasks over Microsoft’s WinRM — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/winrm_connection.html

**Contents:**
- ansible.builtin.winrm connection – Run tasks over Microsoft’s WinRM
- Synopsis
- Requirements
- Parameters
  - Authors
  - Collection links

This connection plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name winrm. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.winrm for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same connection plugin name.

Run commands or put/fetch on a target via WinRM

This plugin allows extra arguments to be passed that are supported by the protocol but not explicitly defined here. They should take the form of variables declared with the following pattern ansible_winrm_<option>.

The below requirements are needed on the local controller node that executes this connection.

pywinrm (python library)

Despite its name, sets both the ‘operation’ and ‘read’ timeout settings for the WinRM connection.

The operation timeout belongs to the WS-Man layer and runs on the winRM-service on the managed windows host.

The read timeout belongs to the underlying python Request call (http-layer) and runs on the ansible controller.

The operation timeout sets the WS-Man ‘Operation timeout’ that runs on the managed windows host. The operation timeout specifies how long a command will run on the winRM-service before it sends the message ‘WinRMOperationTimeoutError’ back to the client. The client (silently) ignores this message and starts a new instance of the operation timeout, waiting for the command to finish (long running commands).

The read timeout sets the client HTTP-request timeout and specifies how long the client (ansible controller) will wait for data from the server to come back over the HTTP-connection (timeout for waiting for in-between messages from the server). When this timer expires, an exception will be thrown and the ansible connection will be terminated with the error message ‘Read timed out’

To avoid the above exception to be thrown, the read timeout will be set to 10 seconds higher than the WS-Man operation timeout, thus make the connection more robust on networks with long latency and/or many hops between server and client network wise.

Setting the difference between the operation and the read timeout to 10 seconds aligns it to the defaults used in the winrm-module and the PSRP-module which also uses 10 seconds (30 seconds for read timeout and 20 seconds for operation timeout)

Corresponds to the operation_timeout_sec and read_timeout_sec args in pywinrm so avoid setting these vars with this one.

The default value is whatever is set in the installed version of pywinrm.

Variable: ansible_winrm_connection_timeout

kerberos command to use to request a authentication ticket

Variable: ansible_winrm_kinit_cmd

The managed option means Ansible will obtain kerberos ticket.

While the manual one means a ticket must already have been obtained by the user.

Variable: ansible_winrm_kinit_mode

added in ansible-core 2.11

Extra arguments to pass to kinit when getting the Kerberos authentication ticket.

By default no extra arguments are passed into kinit unless ansible_winrm_kerberos_delegation is also set. In that case -f is added to the kinit args so a forwardable ticket is retrieved.

If set, the args will overwrite any existing defaults for kinit, including -f for a delegated ticket.

Variable: ansible_winrm_kinit_args

list / elements=string

added in ansible-core 2.12

A list of environment variables to pass through to kinit when getting the Kerberos authentication ticket.

By default no environment variables are passed through and kinit is run with a blank slate.

The environment variable KRB5CCNAME cannot be specified here as it’s used to store the temp Kerberos ticket used by WinRM.

Variable: ansible_winrm_kinit_env_vars

URI path to connect to

Variable: ansible_winrm_path

Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

This can result in a very significant performance improvement when enabled.

However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable requiretty in the sudoers file for the target hosts, which is why this feature is disabled by default.

Environment variable: ANSIBLE_PIPELINING

Variable: ansible_pipelining

port for winrm to connect on remote target

The default is the https (5986) port, if using http it should be 5985

Variable: ansible_port

Variable: ansible_winrm_port

Address of the windows machine

Default: "inventory_hostname"

Variable: inventory_hostname

Variable: ansible_host

Variable: ansible_winrm_host

Authentication password for the remote_user. Can be supplied as CLI option.

Variable: ansible_password

Variable: ansible_winrm_pass

Variable: ansible_winrm_password

The user to log in as to the Windows machine

Variable: ansible_user

Variable: ansible_winrm_user

If not set, then will default to https or http if port is 5985.

Variable: ansible_winrm_scheme

list / elements=string

List of winrm transports to attempt to use (ssl, plaintext, kerberos, etc)

If None (the default) the plugin will try to automatically guess the correct list

The choices available depend on your version of pywinrm

Variable: ansible_winrm_transport

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[winrm]
kinit_env_vars =
```

Example 2 (unknown):
```unknown
[defaults]
pipelining = false
```

Example 3 (unknown):
```unknown
[connection]
pipelining = false
```

---

## ansible.builtin.human_to_bytes filter – Get bytes from string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/human_to_bytes_filter.html

**Contents:**
- ansible.builtin.human_to_bytes filter – Get bytes from string
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name human_to_bytes. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.human_to_bytes for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Convert a human-readable byte or bit string into a number bytes.

This describes the input of the filter, the value before | ansible.builtin.human_to_bytes.

human-readable description of a number of bytes.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.human_to_bytes(positional1, positional2, ...)

Unit to assume when input does not specify it.

If True, force to interpret only bit input; if False, force bytes. Otherwise use the notation to guess.

Integer representing the bytes from the input.

**Examples:**

Example 1 (javascript):
```javascript
# size => 1234803098
size: '{{ "1.15 GB" | human_to_bytes }}'

# size => 1234803098
size: '{{ "1.15" | human_to_bytes(default_unit="G") }}'

# this is an error, wants bits, got bytes
ERROR: '{{ "1.15 GB" | human_to_bytes(isbits=true) }}'

# size => 2684354560
size: '{{ "2.5 gigabyte" | human_to_bytes }}'

# size => 1073741824
size: '{{ "1 Gigabyte" | human_to_bytes }}'

# this is an error, because gigggabyte is not a valid unit
size: '{{ "1 gigggabyte" | human_to_bytes }}'
```

---

## ansible.builtin.odd test – Return true if the variable is odd. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/odd_test.html

**Contents:**
- ansible.builtin.odd test – Return true if the variable is odd.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name odd. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.odd for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is odd.

This is the Jinja builtin test plugin ‘odd’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.odd

---

## ansible.builtin.random filter – random number or list item — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/random_filter.html

**Contents:**
- ansible.builtin.random filter – random number or list item
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name random. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.random for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Use the input to either select a random element of a list or generate a random number.

This describes the input of the filter, the value before | ansible.builtin.random.

A number or list/sequence, if it is a number it is the top bound for random number generation, if it is a sequence or list, the source of the random element selected.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.random(positional1, positional2, ...)

Bottom bound for the random number/element generated.

Subsets the defined range by only using this value to select the increments of it between start and end.

If specified use a pseudo random selection instead (repeatable).

Random number or list element.

**Examples:**

Example 1 (unknown):
```unknown
# can be any item from the list
random_item: "{{ ['a','b','c'] | random }}"

# cron line, select random minute repeatable for each host
"{{ 60 | random(seed=inventory_hostname) }} * * * * root /script/from/cron"
```

---

## ansible.builtin.urlsplit filter – get components from URL — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/urlsplit_filter.html

**Contents:**
- ansible.builtin.urlsplit filter – get components from URL
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name urlsplit. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.urlsplit for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Split a URL into its component parts.

This describes the input of the filter, the value before | ansible.builtin.urlsplit.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.urlsplit(positional1, positional2, ...)

Specify a single component to return.

A dictionary with components as keyword and their value.

If query is provided, a string or integer will be returned instead, depending on query.

**Examples:**

Example 1 (javascript):
```javascript
parts: '{{ "http://user:[email protected]:9000/dir/index.html?query=term#fragment" | urlsplit }}'
# =>
#   {
#       "fragment": "fragment",
#       "hostname": "www.acme.com",
#       "netloc": "user:[email protected]:9000",
#       "password": "password",
#       "path": "/dir/index.html",
#       "port": 9000,
#       "query": "query=term",
#       "scheme": "http",
#       "username": "user"
#   }

hostname: '{{ "http://user:[email protected]:9000/dir/index.html?query=term#fragment" | urlsplit("hostname") }}'
# => 'www.acme.com'

query: '{{ "http://user:[email protected]:9000/dir/index.html?query=term#fragment" | urlsplit("query") }}'
# => 'query=term'

path: '{{ "http://user:[email protected]:9000/dir/index.html?query=term#fragment" | urlsplit("path") }}'
# => '/dir/index.html'
```

---

## ansible.builtin.int filter – Convert the value into an integer. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/int_filter.html

**Contents:**
- ansible.builtin.int filter – Convert the value into an integer.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name int. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.int for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert the value into an integer.

This is the Jinja builtin filter plugin ‘int’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.int

---

## Index of all Collection Environment Variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/environment_variables.html

**Contents:**
- Index of all Collection Environment Variables

The following index documents all environment variables declared by plugins in collections. Environment variables used by the ansible-core configuration are documented in Ansible Configuration Settings.

list of users to be expected to have admin privileges. This is used by the controller to determine how to share temporary files between the remote user and the become user.

Used by: ansible.builtin.sh shell plugin

Directory in which ansible will keep async job information.

Used by: ansible.builtin.sh shell plugin

See the documentations for the options where this environment variable is used.

Used by: ansible.builtin.runas become plugin, ansible.builtin.su become plugin, ansible.builtin.sudo become plugin

Configure the result format to be more readable.

When result_format is set to yaml this option defaults to true, and defaults to false when configured to json.

Setting this option to true will force json and yaml results to always be pretty printed regardless of verbosity.

When set to true and used with the yaml result format, this option will modify module responses in an attempt to produce a more human friendly output at the expense of correctness, and should not be relied upon to aid in writing variable manipulations or conditionals. For correctness, set this option to false or set result_format to json.

Used by: ansible.builtin.default callback plugin, ansible.builtin.minimal callback plugin

Define the task result format used in the callback output.

These formats do not cause the callback to emit valid JSON or YAML formats.

The output contains these formats interspersed with other non-machine parsable data.

Used by: ansible.builtin.default callback plugin, ansible.builtin.minimal callback plugin

directory that will contain the per host JSON files. Also set by the --tree option when using adhoc.

Used by: ansible.builtin.tree callback plugin

Toggle to control displaying markers when running in check mode.

The markers are DRY RUN at the beginning and ending of playbook execution (when calling ansible-playbook --check) and CHECK MODE as a suffix at every play and task that is run in check mode.

Used by: ansible.builtin.default callback plugin

Checked when Ansible needs to execute a module as a different user.

If setfacl and chown both fail and do not let the different user access the module’s files, they will be chgrp’d to this group.

In order for this to work, the remote_user and become_user must share a common group and this setting must be set to that group.

Used by: ansible.builtin.sh shell plugin

Toggle to control whether failed and unreachable tasks are displayed to STDERR rather than STDOUT.

Used by: ansible.builtin.default callback plugin

Toggle to control displaying ‘ok’ task/host results in a task.

Used by: ansible.builtin.default callback plugin

list of ‘valid’ extensions for files containing YAML

Used by: ansible.builtin.yaml inventory plugin

Toggle display of stderr even when script was successful

Used by: ansible.builtin.script inventory plugin

Merge extra vars into the available variables for composition (highest precedence).

Used by: ansible.builtin.constructed inventory plugin

User-Agent to use in the request. The default was changed in 2.11 to ansible-httpget.

Used by: ansible.builtin.url lookup plugin

String of file system path to CA cert bundle to use

Used by: ansible.builtin.url lookup plugin

SSL/TLS Ciphers to use for the request

When a list is provided, all ciphers are joined in order with :

See the OpenSSL Cipher List Format for more details.

The available ciphers is dependent on the Python and OpenSSL/LibreSSL versions

Used by: ansible.builtin.url lookup plugin

Whether or not the URI module should follow redirects.

Used by: ansible.builtin.url lookup plugin

Whether or not to set “cache-control” header with value “no-cache”

Used by: ansible.builtin.url lookup plugin

Force basic authentication

Used by: ansible.builtin.url lookup plugin

How long to wait for the server to send data before giving up

Used by: ansible.builtin.url lookup plugin

String of file system path to unix socket file to use when establishing connection to the provided url

Used by: ansible.builtin.url lookup plugin

A list of headers to not attach on a redirected request

Used by: ansible.builtin.url lookup plugin

Use GSSAPI handler of requests

As of Ansible 2.11, GSSAPI credentials can be specified with username and password.

Used by: ansible.builtin.url lookup plugin

Determining whether to use credentials from ``~/.netrc`` file

By default .netrc is used with Basic authentication headers

When set to False, .netrc credentials are ignored

Used by: ansible.builtin.url lookup plugin

Configures, in seconds, the amount of time to wait for the SSH banner to be presented. This option is supported by paramiko version 1.15.0 or newer.

Used by: ansible.builtin.paramiko_ssh connection plugin

Set this to “False” if you want to avoid host key checking by the underlying tools Ansible uses to connect to the host

Used by: ansible.builtin.paramiko_ssh connection plugin

Path to private key file to use for authentication.

Used by: ansible.builtin.paramiko_ssh connection plugin

Proxy information for running the connection via a jumphost.

Used by: ansible.builtin.paramiko_ssh connection plugin

SUDO usually requires a PTY, True to give a PTY and False to not give a PTY.

Used by: ansible.builtin.paramiko_ssh connection plugin

Save the host keys to a file

Used by: ansible.builtin.paramiko_ssh connection plugin

User to login/authenticate as

Can be set from the CLI via the --user or -u options.

Used by: ansible.builtin.paramiko_ssh connection plugin

Number of seconds until the plugin gives up on failing to establish a TCP connection.

Used by: ansible.builtin.paramiko_ssh connection plugin

Whether or not to enable RSA SHA2 algorithms for pubkeys and hostkeys

On paramiko versions older than 2.9, this only affects hostkeys

For behavior matching paramiko<2.9 set this to False

Used by: ansible.builtin.paramiko_ssh connection plugin

PKCS11 SmartCard provider such as opensc, example: /usr/local/lib/opensc-pkcs11.so

Used by: ansible.builtin.ssh connection plugin

Private key contents in PEM format. Requires the SSH_AGENT configuration to be enabled.

Used by: ansible.builtin.ssh connection plugin

Private key passphrase, dependent on private_key.

This does NOT have any effect when used with private_key_file.

Used by: ansible.builtin.ssh connection plugin

Remote port to connect to.

Used by: ansible.builtin.paramiko_ssh connection plugin

Temporary directory to use on targets when executing tasks.

Used by: ansible.builtin.sh shell plugin

Temporary directory to use on targets when executing tasks.

Used by: ansible.builtin.sh shell plugin

Options to pass to runas, a space delimited list of k=v pairs

Used by: ansible.builtin.runas become plugin

Used by: ansible.builtin.runas become plugin

User you ‘become’ to execute the task

Used by: ansible.builtin.runas become plugin

This defines the location of the scp binary. It defaults to scp which will use the first binary available in $PATH.

Used by: ansible.builtin.ssh connection plugin

Extra exclusive to the scp CLI

Used by: ansible.builtin.ssh connection plugin

When set to True, sftp will be run in batch mode, allowing detection of transfer errors.

When set to False, sftp will not be run in batch mode, preventing detection of transfer errors.

Used by: ansible.builtin.ssh connection plugin

This defines the location of the sftp binary. It defaults to sftp which will use the first binary available in $PATH.

Used by: ansible.builtin.ssh connection plugin

Extra exclusive to the sftp CLI

Used by: ansible.builtin.ssh connection plugin

This makes the temporary files created on the machine world-readable and will issue a warning instead of failing the task.

It is useful when becoming an unprivileged user.

Used by: ansible.builtin.sh shell plugin

This adds output that shows when a task starts to execute for each host.

Used by: ansible.builtin.default callback plugin

When a task fails, display the path to the file containing the failed task and the line number. This information is displayed automatically for every task when running with -vv or greater verbosity.

Used by: ansible.builtin.default callback plugin

Arguments to pass to all SSH CLI tools.

Used by: ansible.builtin.ssh connection plugin

Common extra args for all SSH CLI tools.

Used by: ansible.builtin.ssh connection plugin

This is the location to save SSH’s ControlPath sockets, it uses SSH’s variable substitution.

Since 2.3, if null (default), ansible will generate a unique hash. Use ``%(directory)s`` to indicate where to use the control dir path setting.

Before 2.3 it defaulted to ``control_path=%(directory)s/ansible-ssh-%%h-%%p-%%r``.

Be aware that this setting is ignored if -o ControlPath is set in ssh args.

Used by: ansible.builtin.ssh connection plugin

This sets the directory to use for ssh control path if the control path setting is null.

Also, provides the ``%(directory)s`` variable for the control path setting.

Used by: ansible.builtin.ssh connection plugin

This defines the location of the SSH binary. It defaults to ssh which will use the first SSH binary available in $PATH.

This option is usually not required, it might be useful when access to system SSH is restricted, or when using SSH wrappers to connect to remote hosts.

Used by: ansible.builtin.ssh connection plugin

Extra exclusive to the SSH CLI.

Used by: ansible.builtin.ssh connection plugin

See the documentations for the options where this environment variable is used.

Used by: ansible.builtin.paramiko_ssh connection plugin, ansible.builtin.ssh connection plugin

Mechanism to use for handling ssh password prompt

Used by: ansible.builtin.ssh connection plugin

Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

This can result in a very significant performance improvement when enabled.

However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable requiretty in the sudoers file for the target hosts, which is why this feature is disabled by default.

Used by: ansible.builtin.ssh connection plugin

Number of attempts to connect.

Ansible retries connections only if it gets an SSH error with a return code of 255.

Any errors with return codes other than 255 indicate an issue with program execution.

Used by: ansible.builtin.ssh connection plugin

See the documentations for the options where this environment variable is used.

Used by: ansible.builtin.paramiko_ssh connection plugin, ansible.builtin.ssh connection plugin

Preferred method to use when transferring files over ssh

Used by: ansible.builtin.ssh connection plugin

add -tt to ssh commands to force tty allocation.

Used by: ansible.builtin.ssh connection plugin

Requested verbosity level for the SSH CLI.

Used by: ansible.builtin.ssh connection plugin

Password prompt that sshpass/SSH_ASKPASS should search for.

Supported by sshpass 1.06 and up when password_mechanism set to sshpass.

Defaults to Enter PIN for when pkcs11_provider is set.

Defaults to assword when password_mechanism set to ssh_askpass.

Used by: ansible.builtin.ssh connection plugin

Used by: ansible.builtin.su become plugin

Options to pass to su

Used by: ansible.builtin.su become plugin

Password to pass to su

Used by: ansible.builtin.su become plugin

List of localized strings to match for prompt detection

If empty we’ll use the built in one

Do NOT add a colon (:) to your custom entries. Ansible adds a colon at the end of each prompt; if you add another one in your string, your prompt will fail with a “Timeout” error.

Used by: ansible.builtin.su become plugin

User you ‘become’ to execute the task

Used by: ansible.builtin.su become plugin

Directory to change to before invoking sudo; can avoid permission errors when dropping privileges.

Used by: ansible.builtin.sudo become plugin

Used by: ansible.builtin.sudo become plugin

Options to pass to sudo

Used by: ansible.builtin.sudo become plugin

Password to pass to sudo

Used by: ansible.builtin.sudo become plugin

User you ‘become’ to execute the task

Used by: ansible.builtin.sudo become plugin

List of valid system temporary directories on the managed machine for Ansible to validate remote_tmp against, when specific permissions are needed. These must be world readable, writable, and executable. This list should only contain directories which the system administrator has pre-created with the proper ownership and permissions otherwise security issues can arise.

When remote_tmp is required to be a system temp dir and it does not match any in the list, the first one from the list will be used instead.

Used by: ansible.builtin.sh shell plugin

Control when this vars plugin may be executed.

Setting this option to all will run the vars plugin after importing inventory and whenever it is demanded by a task.

Setting this option to task will only run the vars plugin whenever it is demanded by a task.

Setting this option to inventory will only run the vars plugin after parsing inventory.

If this option is omitted, the global RUN_VARS_PLUGINS configuration is used to determine when to execute the vars plugin.

Used by: ansible.builtin.host_group_vars vars plugin

Consider any tasks reporting “changed” as a junit test failure

Used by: ansible.builtin.junit callback plugin

Consider failed tasks as a junit test failure even if ignore_on_error is set

Used by: ansible.builtin.junit callback plugin

Hide the arguments for a task

Used by: ansible.builtin.junit callback plugin

Should the setup tasks be included in the final report

Used by: ansible.builtin.junit callback plugin

Directory to write XML files to.

Used by: ansible.builtin.junit callback plugin

Replace the directory portion of an out-of-tree relative task path with the given placeholder

Used by: ansible.builtin.junit callback plugin

Configure the output to be one class per yaml file

Used by: ansible.builtin.junit callback plugin

Configure the output to use relative paths to given directory

Used by: ansible.builtin.junit callback plugin

Consider a task only as test case if it has this value as prefix. Additionally failing tasks are recorded as failed test cases.

Used by: ansible.builtin.junit callback plugin

---

## ansible.builtin.split filter – split a string into a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/split_filter.html

**Contents:**
- ansible.builtin.split filter – split a string into a list
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name split. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.split for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.11

Positional parameters

Using Python’s text object method split we turn strings into lists via a ‘splitting character’.

This describes the input of the filter, the value before | ansible.builtin.split.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.split(positional1, positional2, ...)

A string on which to split the original.

This is a passthrough to Python’s str.split.

list / elements=string

List of substrings split from the original.

**Examples:**

Example 1 (javascript):
```javascript
# listjojo => [ "jojo", "is", "a" ]
listjojo: "{{ 'jojo is a' | split }}"

# listjojocomma => [ "jojo is", " a" ]
listjojocomma: "{{ 'jojo is, a' | split(',') }}"
```

---

## ansible.builtin.quote filter – shell quoting — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/quote_filter.html

**Contents:**
- ansible.builtin.quote filter – shell quoting
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name quote. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.quote for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-base 2.10

Quote a string to safely use as in a POSIX shell.

This describes the input of the filter, the value before | ansible.builtin.quote.

This is a passthrough to Python’s shlex.quote.

**Examples:**

Example 1 (unknown):
```unknown
- name: Run a shell command
  shell: echo {{ string_value | quote }}
```

---

## ansible.builtin.dnf module – Manages packages with the dnf package manager — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dnf_module.html

**Contents:**
- ansible.builtin.dnf module – Manages packages with the dnf package manager
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name dnf even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dnf for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Installs, upgrade, removes, and lists packages and groups with the dnf package manager.

This module has a corresponding action plugin.

The below requirements are needed on the host that executes this module.

Specify if the named package and version is allowed to downgrade a maybe already installed higher version of that package. Note that setting allow_downgrade=true can make this module behave in a non-idempotent way. The task could end up with a set of packages that does not match the complete list of specified packages to install (because dependencies between the downgraded package and others can cause changes to the packages which were in the earlier transaction).

Since this feature is not provided by dnf itself but by ansible.builtin.dnf module, using this in combination with wildcard characters in name may result in an unexpected results.

added in ansible-base 2.10

If true it allows erasing of installed packages to resolve dependencies.

If true, removes all “leaf” packages from the system that were originally installed as dependencies of user-installed packages but which are no longer required by any such package. Should be used alone or when state=absent.

added in ansible-core 2.17

When set to true, either use a package with the highest version available or fail.

When set to false, if the latest version cannot be installed go with the lower version.

Default is set by the operating system distribution.

If set to true, and state=latest then only installs updates that have been marked bugfix related.

Note that, similar to dnf upgrade-minimal, this filter applies to dependencies as well.

added in ansible-core 2.12

Tells dnf to run entirely from system cache; does not download or update metadata.

The remote dnf configuration file to use for the transaction.

Disable the excludes defined in DNF config files.

If set to all, disables all excludes.

If set to main, disable excludes defined in [main] in dnf.conf.

If set to repoid, disable excludes defined for given repo id.

Whether to disable the GPG checking of signatures of packages being installed. Has an effect only if state=present or state=latest.

This setting affects packages installed from a repository as well as “local” packages installed from the filesystem or a URL.

list / elements=string

Plugin name to disable for the install/update operation. The disabled plugins will not persist beyond the transaction.

list / elements=string

Repoid of repositories to disable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a ,.

Specifies an alternate directory to store packages.

Has an effect only if download_only is specified.

Only download the packages, do not install them.

list / elements=string

Plugin name to enable for the install/update operation. The enabled plugin will not persist beyond the transaction.

list / elements=string

Repoid of repositories to enable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a “,”.

list / elements=string

Package name(s) to exclude when state=present, or latest. This can be a list or a comma separated string.

This is effectively a no-op in DNF as it is not needed with DNF.

This option is deprecated and will be removed in ansible-core 2.20.

Will also install all packages linked by a weak dependency relation.

Specifies an alternative installroot, relative to which all packages will be installed.

Various (non-idempotent) commands for usage with /usr/bin/ansible and not playbooks. Use ansible.builtin.package_facts instead of the list argument as a best practice.

Amount of time to wait for the dnf lockfile to be freed.

list / elements=string

A package name or package specifier with version, like name-1.0. When using state=latest, this can be ‘*’ which means run: dnf -y update. You can also pass a url or a local path to an rpm file. To operate on several packages this can accept a comma separated string of packages or a list of packages.

Comparison operators for package version are valid here >, <, >=, <=. Example - name >= 1.0. Spaces around the operator are required.

You can also pass an absolute path for a binary which is provided by the package to install. See examples for more information.

added in ansible-core 2.11

This is the opposite of the best option kept for backwards compatibility.

Since ansible-core 2.17 the default value is set by the operating system distribution.

Specifies an alternative release from which all packages will be installed.

If set to true, and state=latest then only installs updates that have been marked security related.

Note that, similar to dnf upgrade-minimal, this filter applies to dependencies as well.

Skip all unavailable packages or packages with broken dependencies without raising an error. Equivalent to passing the --skip-broken option.

added in ansible-core 2.13

Disables SSL validation of the repository server for this transaction.

This should be set to false if one of the configured repositories is using an untrusted or self-signed certificate.

Whether to install (present, latest), or remove (absent) a package.

Default is None, however in effect the default action is present unless the autoremove=true, then absent is inferred.

aliases: expire-cache

Force dnf to check if cache is out of date and redownload if needed. Has an effect only if state=present or state=latest.

When using latest, only update installed packages. Do not install packages.

Has an effect only if state=present or state=latest.

added in ansible-core 2.15

Backend module to use.

"auto" (default): Automatically select the backend based on the ansible_facts.pkg_mgr fact.

"dnf": ansible.builtin.dnf

"dnf4": Alias for dnf

"dnf5": ansible.builtin.dnf5

"yum": Alias for auto (see Notes)

"yum4": Alias for dnf

This only applies if using a https url as the source of the rpm. For example, for localinstall. If set to false, the SSL certificates will not be validated.

This should only set to false used on personally controlled sites using self-signed certificates as it avoids verifying the source site.

dnf has 2 action plugins that use it under the hood, ansible.builtin.dnf and ansible.builtin.package.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

When used with a loop: each package will be processed individually, it is much more efficient to pass the list directly to the name option.

Group removal doesn’t work if the group was installed with Ansible because upstream dnf’s API doesn’t properly mark groups as installed, therefore upon removal the module is unable to detect that the group is installed https://bugzilla.redhat.com/show_bug.cgi?id=1620324.

While use_backend=yum and the ability to call the action plugin as ansible.builtin.yum are provided for syntax compatibility, the YUM backend was removed in ansible-core 2.17 because the required libraries are not available for any supported version of Python. If you rely on this functionality, use an older version of Ansible.

Igor Gnatenko (@ignatenkobrain)

Cristian van Ee (@DJMuggs) <cristian at cvee.org>

Berend De Schouwer (@berenddeschouwer)

Adam Miller (@maxamillion)

**Examples:**

Example 1 (unknown):
```unknown
- name: Install the latest version of Apache
  ansible.builtin.dnf:
    name: httpd
    state: latest

- name: Install Apache >= 2.4
  ansible.builtin.dnf:
    name: httpd >= 2.4
    state: present

- name: Install the latest version of Apache and MariaDB
  ansible.builtin.dnf:
    name:
      - httpd
      - mariadb-server
    state: latest

- name: Remove the Apache package
  ansible.builtin.dnf:
    name: httpd
    state: absent

- name: Install the latest version of Apache from the testing repo
  ansible.builtin.dnf:
    name: httpd
    enablerepo: testing
    state: present

- name: Upgrade all packages
  ansible.builtin.dnf:
    name: "*"
    state: latest

- name: Update the webserver, depending on which is installed on the system. Do not install the other one
  ansible.builtin.dnf:
    name:
      - httpd
      - nginx
    state: latest
    update_only: yes

- name: Install the nginx rpm from a remote repo
  ansible.builtin.dnf:
    name: 'http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm'
    state: present

- name: Install nginx rpm from a local file
  ansible.builtin.dnf:
    name: /usr/local/src/nginx-release-centos-6-0.el6.ngx.noarch.rpm
    state: present

- name: Install Package based upon the file it provides
  ansible.builtin.dnf:
    name: /usr/bin/cowsay
    state: present

- name: Install the 'Development tools' package group
  ansible.builtin.dnf:
    name: '@Development tools'
    state: present

- name: Autoremove unneeded packages installed as dependencies
  ansible.builtin.dnf:
    autoremove: yes

- name: Uninstall httpd but keep its dependencies
  ansible.builtin.dnf:
    name: httpd
    state: absent
    autoremove: no

- name: Install a modularity appstream with defined stream and profile
  ansible.builtin.dnf:
    name: '@postgresql:9.6/client'
    state: present

- name: Install a modularity appstream with defined stream
  ansible.builtin.dnf:
    name: '@postgresql:9.6'
    state: present

- name: Install a modularity appstream with defined profile
  ansible.builtin.dnf:
    name: '@postgresql/client'
    state: present
```

---

## ansible.builtin.groupby filter – Group a sequence of objects by an attribute using Python’s :func:`itertools. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/groupby_filter.html

**Contents:**
- ansible.builtin.groupby filter – Group a sequence of objects by an attribute using Python’s :func:`itertools.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name groupby. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.groupby for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Group a sequence of objects by an attribute using Python’s :func:`itertools.

This is the Jinja builtin filter plugin ‘groupby’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.groupby

---

## ansible.builtin.slurp module – Slurps a file from remote nodes — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/slurp_module.html

**Contents:**
- ansible.builtin.slurp module – Slurps a file from remote nodes
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name slurp even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.slurp for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module works like ansible.builtin.fetch. It is used for fetching a base64- encoded blob containing the data in a remote file.

This module is also supported for Windows targets.

The file on the remote system to fetch. This must be a file, not a directory.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Platforms: posix, windows

Target OS/families that can be operated against

This module returns an ‘in memory’ base64 encoded version of the file, take into account that this will require at least twice the RAM as the original file size.

Fetch files from remote nodes.

Common return values are documented here, the following are the fields unique to this module:

Type of encoding used for file

Actual path of file slurped

Sample: "/var/run/sshd.pid"

Michael DeHaan (@mpdehaan)

**Examples:**

Example 1 (javascript):
```javascript
- name: Find out what the remote machine's mounts are
  ansible.builtin.slurp:
    src: /proc/mounts
  register: mounts

- name: Print returned information
  ansible.builtin.debug:
    msg: "{{ mounts['content'] | b64decode }}"

# From the commandline, find the pid of the remote machine's sshd
# $ ansible host -m ansible.builtin.slurp -a 'src=/var/run/sshd.pid'
# host | SUCCESS => {
#     "changed": false,
#     "content": "MjE3OQo=",
#     "encoding": "base64",
#     "source": "/var/run/sshd.pid"
# }
# $ echo MjE3OQo= | base64 -d
# 2179
```

---

## ansible.builtin.escaped test – Check if the value is escaped. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/escaped_test.html

**Contents:**
- ansible.builtin.escaped test – Check if the value is escaped.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name escaped. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.escaped for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the value is escaped.

This is the Jinja builtin test plugin ‘escaped’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.escaped

---

## ansible.builtin.vault_encrypted test – Is this an encrypted vault string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/vault_encrypted_test.html

**Contents:**
- ansible.builtin.vault_encrypted test – Is this an encrypted vault string
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name vault_encrypted. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.vault_encrypted for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-base 2.10

Verifies if the input string is an Ansible vault or not

This describes the input of the test, the value before is ansible.builtin.vault_encrypted or is not ansible.builtin.vault_encrypted.

The possible vault string

Returns True if the input is a valid ansible vault, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
thisisfalse: '{{ "any string" is vault_encryped}}'
thisistrue: '{{ "$ANSIBLE_VAULT;1.2;AES256;dev...." is vault_encrypted}}'
```

---

## ansible.builtin.round filter – Round the number to a given precision. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/round_filter.html

**Contents:**
- ansible.builtin.round filter – Round the number to a given precision.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name round. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.round for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Round the number to a given precision.

This is the Jinja builtin filter plugin ‘round’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.round

---

## ansible.builtin.psrp connection – Run tasks over Microsoft PowerShell Remoting Protocol — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/psrp_connection.html

**Contents:**
- ansible.builtin.psrp connection – Run tasks over Microsoft PowerShell Remoting Protocol
- Synopsis
- Requirements
- Parameters
  - Authors
  - Collection links

This connection plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name psrp. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.psrp for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same connection plugin name.

Run commands or put/fetch on a target via PSRP (WinRM plugin)

This is similar to the ansible.builtin.winrm connection plugin which uses the same underlying transport but instead runs in a PowerShell interpreter.

The below requirements are needed on the local controller node that executes this connection.

pypsrp>=0.4.0, <1.0.0 (Python library)

The authentication protocol to use when authenticating the remote user.

The default, negotiate, will attempt to use Kerberos (kerberos) if it is available and fall back to NTLM (ntlm) if it isn’t.

"negotiate" ← (default)

Variable: ansible_psrp_auth

aliases: cert_trust_path

The path to a PEM certificate chain to use when validating the server’s certificate.

This value is ignored if cert_validation is set to ignore.

Variable: ansible_psrp_cert_trust_path

Variable: ansible_psrp_ca_cert

Whether to validate the remote server’s certificate or not.

Set to ignore to not validate any certificates.

ca_cert can be set to the path of a PEM certificate chain to use in the validation.

"validate" ← (default)

Variable: ansible_psrp_cert_validation

The local path to an X509 certificate key to use with certificate auth.

Variable: ansible_psrp_certificate_key_pem

The local path to an X509 certificate to use with certificate auth.

Variable: ansible_psrp_certificate_pem

The name of the PowerShell configuration endpoint to connect to.

Default: "Microsoft.PowerShell"

Variable: ansible_psrp_configuration_name

The connection timeout for making the request to the remote host.

This is measured in seconds.

Variable: ansible_psrp_connection_timeout

credssp_auth_mechanism

The sub authentication mechanism to use with CredSSP auth.

When auto, both Kerberos and NTLM is attempted with kerberos being preferred.

Variable: ansible_psrp_credssp_auth_mechanism

credssp_disable_tlsv1_2

Disables the use of TLSv1.2 on the CredSSP authentication channel.

This should not be set to yes unless dealing with a host that does not have TLSv1.2.

Variable: ansible_psrp_credssp_disable_tlsv1_2

credssp_minimum_version

The minimum CredSSP server authentication version that will be accepted.

Set to 5 to ensure the server has been patched and is not vulnerable to CVE 2018-0886.

Variable: ansible_psrp_credssp_minimum_version

Will disable any environment proxy settings and connect directly to the remote host.

This option is ignored if proxy is set.

Variable: ansible_psrp_ignore_proxy

Sets the maximum size of each WSMan message sent to the remote host.

This is measured in bytes.

Defaults to 150KiB for compatibility with older hosts.

Variable: ansible_psrp_max_envelope_size

Controls the message encryption settings, this is different from TLS encryption when protocol is https.

Only the auth protocols negotiate, kerberos, ntlm, and credssp can do message encryption. The other authentication protocols only support encryption when protocol is set to https.

auto means means message encryption is only used when not using TLS/HTTPS.

always is the same as auto but message encryption is always used even when running over TLS/HTTPS.

never disables any encryption checks that are in place when running over HTTP and disables any authentication encryption processes.

Variable: ansible_psrp_message_encryption

Allow the remote user the ability to delegate it’s credentials to another server, i.e. credential delegation.

Only valid when Kerberos was the negotiated auth or was explicitly set as the authentication.

Ignored when NTLM was the negotiated auth.

Variable: ansible_psrp_negotiate_delegate

negotiate_hostname_override

Override the remote hostname when searching for the host in the Kerberos lookup.

This allows Ansible to connect over IP but authenticate with the remote server using it’s DNS name.

Only valid when Kerberos was the negotiated auth or was explicitly set as the authentication.

Ignored when NTLM was the negotiated auth.

Variable: ansible_psrp_negotiate_hostname_override

Send the Channel Binding Token (CBT) structure when authenticating.

CBT is used to provide extra protection against Man in the Middle MitM attacks by binding the outer transport channel to the auth channel.

CBT is not used when using just HTTP, only HTTPS.

Variable: ansible_psrp_negotiate_send_cbt

Override the service part of the SPN used during Kerberos authentication.

Only valid when Kerberos was the negotiated auth or was explicitly set as the authentication.

Ignored when NTLM was the negotiated auth.

Variable: ansible_psrp_negotiate_service

Sets the WSMan timeout for each operation.

This is measured in seconds.

This should not exceed the value for connection_timeout.

Variable: ansible_psrp_operation_timeout

The URI path to connect to.

Variable: ansible_psrp_path

Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

This can result in a very significant performance improvement when enabled.

However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable requiretty in the sudoers file for the target hosts, which is why this feature is disabled by default.

Environment variable: ANSIBLE_PIPELINING

Variable: ansible_pipelining

The port for PSRP to connect on the remote target.

Default is 5986 if protocol is not defined or is https, otherwise the port is 5985.

Variable: ansible_port

Variable: ansible_psrp_port

Set the protocol to use for the connection.

Default is https if port is not defined or port is not 5985.

Variable: ansible_psrp_protocol

Set the proxy URL to use when connecting to the remote host.

Variable: ansible_psrp_proxy

The read timeout for receiving data from the remote host.

This value must always be greater than operation_timeout.

This option requires pypsrp >= 0.3.

This is measured in seconds.

Variable: ansible_psrp_read_timeout

The backoff time to use in between reconnection attempts. (First sleeps X, then sleeps 2*X, then sleeps 4*X, …)

This is measured in seconds.

The ansible_psrp_reconnection_backoff variable was added in Ansible 2.9.

Variable: ansible_psrp_connection_backoff

Variable: ansible_psrp_reconnection_backoff

The number of retries on connection errors.

Variable: ansible_psrp_reconnection_retries

The hostname or IP address of the remote host.

Default: "inventory_hostname"

Variable: inventory_hostname

Variable: ansible_host

Variable: ansible_psrp_host

Authentication password for the remote_user. Can be supplied as CLI option.

Variable: ansible_password

Variable: ansible_winrm_pass

Variable: ansible_winrm_password

The user to log in as.

Variable: ansible_user

Variable: ansible_psrp_user

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
pipelining = false
```

Example 2 (unknown):
```unknown
[connection]
pipelining = false
```

---

## ansible.builtin.list filter – Convert the value into a list. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/list_filter.html

**Contents:**
- ansible.builtin.list filter – Convert the value into a list.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name list. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.list for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert the value into a list.

This is the Jinja builtin filter plugin ‘list’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.list

---

## ansible.builtin.git module – Deploy software (or files) from git checkouts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/git_module.html

**Contents:**
- ansible.builtin.git module – Deploy software (or files) from git checkouts
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name git even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.git for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Manage git checkouts of repositories to deploy files or software.

The below requirements are needed on the host that executes this module.

git>=1.7.1 (the command line tool)

Will ensure or not that -o StrictHostKeyChecking=no is present as an ssh option.

Be aware that this disables a protection against MITM attacks.

Those using OpenSSH >= 7.5 might want to use accept_newhostkey or set ssh_opts to StrictHostKeyChecking=accept-new instead, it does not remove the MITM issue but it does restrict it to the first attempt.

added in ansible-core 2.12

As of OpenSSH 7.5, -o StrictHostKeyChecking=accept-new can be used which is safer and will only accepts host keys which are not present or are the same. If true, ensure that -o StrictHostKeyChecking=accept-new is present as an ssh option.

Specify archive file path with extension. If specified, creates an archive file of the specified format containing the tree structure for the source tree. Allowed archive formats [“zip”, “tar.gz”, “tar”, “tgz”].

This will clone and perform git archive from local directory as not all git servers support git archive.

added in ansible-base 2.10

Specify a prefix to add to each file path in archive. Requires archive to be specified.

If true, repository will be created as a bare repo, otherwise it will be a standard repo with a workspace.

If false, do not clone the repository even if it does not exist locally.

Create a shallow clone with a history truncated to the specified number or revisions. The minimum possible value is 1, otherwise ignored. Needs git>=1.9.1 to work correctly.

The path of where the repository should be checked out. This is equivalent to git clone [repo_url] [directory]. The repository named in repo is not appended to this path and the destination directory must be empty. This parameter is required, unless clone is set to false.

Path to git executable to use. If not supplied, the normal mechanism for resolving binary paths will be used.

If true, any modified files in the working repository will be discarded. Prior to 0.7, this was always true and could not be disabled. Prior to 1.9, the default was true.

aliases: gpg_whitelist

list / elements=string

A list of trusted GPG fingerprints to compare to the fingerprint of the GPG-signed commit.

Only used when verify_commit=yes.

Use of this feature requires Git 2.6+ due to its reliance on git’s --raw flag to verify-commit and verify-tag.

Alias gpg_allowlist is added in version 2.17.

Alias gpg_whitelist is deprecated and will be removed in version 2.21.

Specify an optional private key file path, on the target host, to use for the checkout.

This ensures IdentitiesOnly=yes is present in ssh_opts.

If false, repository will be cloned without the --recursive option, skipping sub-modules.

Reference repository (see git clone --reference ...).

Add an additional refspec to be fetched. If version is set to a SHA-1 not reachable from any branch or tag, this option may be necessary to specify the ref containing the SHA-1. Uses the same syntax as the git fetch command. An example value could be “refs/meta/config”.

git, SSH, or HTTP(S) protocol address of the git repository.

Avoid embedding usernames and passwords within Git repository URLs. This practice is insecure and can lead to unauthorized access to your repositories. For secure authentication, configure SSH keys (recommended) or use a credential helper. See Git documentation on SSH keys/credential helpers for instructions.

The path to place the cloned repository. If specified, Git repository can be separated from working tree.

added in ansible-core 2.11

Clone only the history leading to the tip of the specified revision.

Options git will pass to ssh when used as protocol, it works via git‘s GIT_SSH/GIT_SSH_COMMAND environment variables.

For older versions it appends GIT_SSH_OPTS (specific to this module) to the variables above or via a wrapper script.

Other options can add to this list, like key_file and accept_hostkey.

An example value could be -o StrictHostKeyChecking=no (although this particular option is better set by accept_hostkey).

The module ensures that BatchMode=yes is always present to avoid prompts.

If true, submodules will track the latest commit on their master branch (or other branch specified in .gitmodules). If false, submodules will be kept at the revision specified by the main project. This is equivalent to specifying the --remote flag to git submodule update.

The umask to set before doing any checkouts, or any other repository maintenance.

If false, do not retrieve new revisions from the origin repository.

Operations like archive will work on the existing (old) repository and might not respond to changes to the options version or remote.

If true, when cloning or checking out a version verify the signature of a GPG signed commit. This requires git version>=2.1.0 to be installed. The commit MUST be signed and the public key MUST be present in the GPG keyring.

What version of the repository to check out. This can be the literal string HEAD, a branch name, a tag name. It can also be a SHA-1 hash, in which case refspec needs to be specified if the given revision is not already available.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

If the task seems to be hanging, first verify remote host is in known_hosts. SSH will prompt user to authorize the first contact with a remote host. To avoid this prompt, one solution is to use the option accept_hostkey. Another solution is to add the remote host public key in /etc/ssh/ssh_known_hosts before calling the git module, with the following command: ssh-keyscan -H remote_host.com >> /etc/ssh/ssh_known_hosts.

Common return values are documented here, the following are the fields unique to this module:

Last commit revision of the repository retrieved during the update.

Sample: "4c020102a9cd6fe908c9a4a326a38f972f63a903"

Commit revision before the repository was updated, “null” for new repository.

Sample: "67c04ebe40a003bda0efb34eacfb93b0cafdf628"

Contains the original path of .git directory if it is changed.

Sample: "/path/to/old/git/dir"

Contains the new path of .git directory if it is changed.

Sample: "/path/to/new/git/dir"

Contains True or False whether or not the remote URL was changed.

**Examples:**

Example 1 (unknown):
```unknown
- name: Git checkout
  ansible.builtin.git:
    repo: 'https://github.com/ansible/ansible.git'
    dest: /tmp/checkout
    version: release-0.22

- name: Read-write git checkout from github
  ansible.builtin.git:
    repo: [email protected]:ansible/ansible.git
    dest: /tmp/checkout

- name: Just ensuring the repo checkout exists
  ansible.builtin.git:
    repo: 'https://github.com/ansible/ansible.git'
    dest: /tmp/checkout
    update: no

- name: Just get information about the repository whether or not it has already been cloned locally
  ansible.builtin.git:
    repo: [email protected]:ansible/ansible.git
    dest: /tmp/checkout
    clone: no
    update: no

- name: Checkout a github repo and use refspec to fetch all pull requests
  ansible.builtin.git:
    repo: 'https://github.com/ansible/ansible.git'
    dest: /tmp/checkout
    refspec: '+refs/pull/*:refs/heads/*'

- name: Create git archive from repo
  ansible.builtin.git:
    repo: [email protected]:ansible/ansible.git
    dest: /tmp/checkout
    archive: /tmp/ansible.zip

- name: Clone a repo with separate git directory
  ansible.builtin.git:
    repo: 'https://github.com/ansible/ansible.git'
    dest: /tmp/checkout
    separate_git_dir: /tmp/repo

- name: Example clone of a single branch
  ansible.builtin.git:
    repo: [email protected]:ansible/ansible.git
    dest: /tmp/checkout
    single_branch: yes
    version: master

- name: Avoid hanging when http(s) password is missing
  ansible.builtin.git:
    repo: 'https://github.com/ansible/ansible.git'
    dest: /tmp/checkout
  environment:
    GIT_TERMINAL_PROMPT: 0 # reports "terminal prompts disabled" on missing password
    # or GIT_ASKPASS: /bin/true # for git before version 2.3.0, reports "Authentication failed" on missing password
```

---

## ansible.builtin.fail module – Fail with custom message — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/fail_module.html

**Contents:**
- ansible.builtin.fail module – Fail with custom message
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name fail even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.fail for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module fails the progress with a custom message.

It can be useful for bailing out when a certain condition is met using when.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

The customized message used for failing execution.

If omitted, fail will simply bail out with a generic message.

Default: "Failed as requested from task"

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

Aside from register and/or in combination with delegate_facts, it has little effect.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Asserts given expressions are true.

Print statements during execution.

Execute Ansible ‘actions’.

Dag Wieers (@dagwieers)

**Examples:**

Example 1 (unknown):
```unknown
- name: Example using fail and when together
  ansible.builtin.fail:
    msg: The system may not be provisioned according to the CMDB status.
  when: cmdb_status != "to-be-staged"
```

---

## ansible.builtin.mandatory filter – make a variable’s existence mandatory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/mandatory_filter.html

**Contents:**
- ansible.builtin.mandatory filter – make a variable’s existence mandatory
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name mandatory. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.mandatory for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Depending on context undefined variables can be ignored or skipped, this ensures they force an error.

This describes the input of the filter, the value before | ansible.builtin.mandatory.

Mandatory expression.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.mandatory(key1=value1, key2=value2, ...)

The customized message that is printed when the given variable is not defined.

The input if defined, otherwise an error.

**Examples:**

Example 1 (unknown):
```unknown
# results in a Filter Error
{{ notdefined | mandatory }}

# print a custom error message
{{ notdefined | mandatory(msg='This variable is required.') }}
```

---

## ansible.builtin.replace filter – Return a copy of the value with all occurrences of a substring replaced with a new one. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/replace_filter.html

**Contents:**
- ansible.builtin.replace filter – Return a copy of the value with all occurrences of a substring replaced with a new one.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name replace. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.replace for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a copy of the value with all occurrences of a substring replaced with a new one.

This is the Jinja builtin filter plugin ‘replace’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.replace

---

## ansible.builtin.batch filter – A filter that batches items. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/batch_filter.html

**Contents:**
- ansible.builtin.batch filter – A filter that batches items.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name batch. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.batch for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

A filter that batches items.

This is the Jinja builtin filter plugin ‘batch’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.batch

---

## ansible.builtin.pipe lookup – read output from a command — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/pipe_lookup.html

**Contents:**
- ansible.builtin.pipe lookup – read output from a command
- Synopsis
- Terms
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name pipe. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.pipe for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Run a command and return the output.

The given command is passed to a shell for execution, therefore all variables that are part of the command and come from a remote/untrusted source MUST be sanitized using the ansible.builtin.quote filter to avoid shell injection vulnerabilities. See the example section.

Like all lookups this runs on the Ansible controller and is unaffected by other keywords, such as become, so if you need to different permissions you must change the command or run Ansible as another user.

Alternatively you can use a shell/command task that runs against localhost and registers the result.

The directory of the play is used as the current working directory.

list / elements=string

Daniel Hokka Zakrisson

**Examples:**

Example 1 (unknown):
```unknown
- name: raw result of running date command
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.pipe', 'date') }}"

- name: Always use quote filter to make sure your variables are safe to use with shell
  ansible.builtin.debug:
    msg: "{{ lookup('ansible.builtin.pipe', 'getent passwd ' + myuser | quote ) }}"
```

---

## ansible.builtin.wait_for module – Waits for a condition before continuing — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/wait_for_module.html

**Contents:**
- ansible.builtin.wait_for module – Waits for a condition before continuing
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name wait_for even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.wait_for for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

You can wait for a set amount of time timeout, this is the default if nothing is specified or just timeout is specified. This does not produce an error.

Waiting for a port to become available is useful for when services are not immediately available after their init scripts return which is true of certain Java application servers.

It is also useful when starting guests with the community.libvirt.virt module and needing to pause until they are ready.

This module can also be used to wait for a regex match a string to be present in a file.

In Ansible 1.6 and later, this module can also be used to wait for a file to be available or absent on the filesystem.

In Ansible 1.8 and later, this module can also be used to wait for active connections to be closed before continuing, useful if a node is being rotated out of a load balancer pool.

For Windows targets, use the ansible.windows.win_wait_for module instead.

active_connection_states

list / elements=string

The list of TCP connection states which are counted as active connections.

Default: ["ESTABLISHED", "FIN_WAIT1", "FIN_WAIT2", "SYN_RECV", "SYN_SENT", "TIME_WAIT"]

Maximum number of seconds to wait for a connection to happen before closing and retrying.

Number of seconds to wait before starting to poll.

list / elements=string

List of hosts or IPs to ignore when looking for active TCP connections for drained state.

A resolvable hostname or IP address to wait for.

This overrides the normal error message from a failure to meet the required conditions.

Path to a file on the filesystem that must exist before continuing.

path and port are mutually exclusive parameters.

path and port are mutually exclusive parameters.

Can be used to match a string in either a file or a socket connection.

Defaults to a multiline regex.

When inspecting a system log file and a static string, remember that Ansible by default logs its own actions there; see the notes and examples for information.

Number of seconds to sleep between checks.

Before Ansible 2.3 this was hardcoded to 1 second.

Either present, started, or stopped, absent, or drained.

When checking a port started will ensure the port is open, stopped will check that it is closed, drained will check for active connections.

When checking for a file or a search string present or started will ensure that the file or string is present before continuing, absent will check that file is absent or removed.

"started" ← (default)

Maximum number of seconds to wait for, when used with another condition it will force an error.

When used without other conditions it is equivalent of just sleeping.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Under some circumstances when using mandatory access control, a path may always be treated as being absent even if it exists, but can’t be modified or created by the remote user either.

When waiting for a path, symbolic links will be followed. Many other modules that manipulate files do not follow symbolic links, so operations on the path using other modules may not work exactly as expected.

When searching a static string within a system log file, it is important to account for potential self-matching against log entries generated by the Ansible modules. To prevent this, add a regular expression construct into the search string. For example, to match a literal string ‘this thing’, one could use a regular expression like ‘this t[h]ing’.

Waits until remote system is reachable/usable.

The official documentation on the ansible.windows.win_wait_for module.

The official documentation on the community.windows.win_wait_for_process module.

Common return values are documented here, the following are the fields unique to this module:

The number of seconds that elapsed while waiting

Dictionary containing all the named subgroups of the match, keyed by the subgroup name, as returned by https://docs.python.org/3/library/re.html#re.MatchObject.groupdict

Sample: {"group": "match"}

list / elements=string

Tuple containing all the subgroups of the match as returned by https://docs.python.org/3/library/re.html#re.MatchObject.groups

Sample: ["match 1", "match 2"]

Jeroen Hoekx (@jhoekx)

Andrii Radyk (@AnderEnder)

**Examples:**

Example 1 (unknown):
```unknown
- name: Sleep for 300 seconds and continue with play
  ansible.builtin.wait_for:
    timeout: 300
  delegate_to: localhost

- name: Wait for port 8000 to become open on the host, don't start checking for 10 seconds
  ansible.builtin.wait_for:
    port: 8000
    delay: 10

- name: Waits for port 8000 of any IP to close active connections, don't start checking for 10 seconds
  ansible.builtin.wait_for:
    host: 0.0.0.0
    port: 8000
    delay: 10
    state: drained

- name: Wait for port 8000 of any IP to close active connections, ignoring connections for specified hosts
  ansible.builtin.wait_for:
    host: 0.0.0.0
    port: 8000
    state: drained
    exclude_hosts: 10.2.1.2,10.2.1.3

- name: Wait until the file /tmp/foo is present before continuing
  ansible.builtin.wait_for:
    path: /tmp/foo

- name: Wait until the string "completed" is in the file /tmp/foo before continuing
  ansible.builtin.wait_for:
    path: /tmp/foo
    search_regex: completed

- name: Wait until the string "tomcat up" is in syslog, use regex character set to avoid self match
  ansible.builtin.wait_for:
    path: /var/log/syslog
    search_regex: 'tomcat [u]p'

- name: Wait until regex pattern matches in the file /tmp/foo and print the matched group
  ansible.builtin.wait_for:
    path: /tmp/foo
    search_regex: completed (?P<task>\w+)
  register: waitfor
- ansible.builtin.debug:
    msg: Completed {{ waitfor['match_groupdict']['task'] }}

- name: Wait until the lock file is removed
  ansible.builtin.wait_for:
    path: /var/lock/file.lock
    state: absent

- name: Wait until the process is finished and pid was destroyed
  ansible.builtin.wait_for:
    path: /proc/3466/status
    state: absent

- name: Output customized message when failed
  ansible.builtin.wait_for:
    path: /tmp/foo
    state: present
    msg: Timeout to find file /tmp/foo

# Do not assume the inventory_hostname is resolvable and delay 10 seconds at start
- name: Wait 300 seconds for port 22 to become open and contain "OpenSSH"
  ansible.builtin.wait_for:
    port: 22
    host: '{{ (ansible_ssh_host|default(ansible_host))|default(inventory_hostname) }}'
    search_regex: OpenSSH
    delay: 10
    timeout: 300
  delegate_to: localhost

# Same as above but using config lookup for the target,
# most plugins use 'remote_addr', but ssh uses 'host'
- name: Wait 300 seconds for port 22 to become open and contain "OpenSSH"
  ansible.builtin.wait_for:
    port: 22
    host: "{{ lookup('config', 'host', plugin_name='ssh', plugin_type='connection') }}"
    search_regex: OpenSSH
    delay: 10
    timeout: 300
  delegate_to: localhost
```

---

## ansible.builtin.extract filter – extract a value based on an index or key — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/extract_filter.html

**Contents:**
- ansible.builtin.extract filter – extract a value based on an index or key
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name extract. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.extract for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Extract a value from a list or dictionary based on an index/key.

User must ensure that index or key used matches the type of container.

Equivalent of using list[index] and dictionary[key] but useful as a filter to combine with map.

This describes the input of the filter, the value before | ansible.builtin.extract.

Index or key to extract.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.extract(positional1, positional2, ...)

Dictionary or list from which to extract a value.

list / elements=dictionary / required

Indices or keys to extract from the initial result (subkeys/subindices).

Resulting merge of supplied dictionaries.

**Examples:**

Example 1 (javascript):
```javascript
# extracted => 'b', same as ['a', 'b', 'c'][1]
extracted: "{{ 1 | extract(['a', 'b', 'c']) }}"

# extracted_key => '2', same as {'a': 1, 'b': 2, 'c': 3}['b']
extracted_key: "{{ 'b' | extract({'a': 1, 'b': 2, 'c': 3}) }}"

# extracted_key_r => '2', same as [{'a': 1, 'b': 2, 'c': 3}, {'x': 9, 'y': 10}][0]['b']
extracted_key_r: "{{ 0 | extract([{'a': 1, 'b': 2, 'c': 3}, {'x': 9, 'y': 10}], morekeys='b') }}"
```

---

## ansible.builtin.validate_argument_spec module – Validate role argument specs. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/validate_argument_spec_module.html

**Contents:**
- ansible.builtin.validate_argument_spec module – Validate role argument specs.
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name validate_argument_spec even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.validate_argument_spec for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

New in ansible-core 2.11

This module validates role arguments with a defined argument specification.

This module has a corresponding action plugin.

A dictionary like AnsibleModule argument_spec.

See the options parameter for the specification format.

A dictionary of the arguments that will be validated according to argument_spec.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

It is unnecessary to call this module explicitly if the role contains an argument spec.

Common return values are documented here, the following are the fields unique to this module:

list / elements=string

A list of arg validation errors.

Sample: ["error message 1", "error message 2"]

A dict of the data from the ‘argument_spec’ arg.

Sample: {"some_arg": {"type": "str"}, "some_other_arg": {"required": true, "type": "int"}}

validate_args_context

A dict of info about where validate_args_spec was used

Sample: {"argument_spec_name": "main", "name": "my_role", "path": "/home/user/roles/my_role/", "type": "role"}

**Examples:**

Example 1 (unknown):
```unknown
- name: verify vars needed for this task file are present when included
  ansible.builtin.validate_argument_spec:
    argument_spec: '{{ required_data }}'
  vars:
    required_data:
      # unlike spec file, just put the options in directly
      stuff:
        description: stuff
        type: str
        choices: ['who', 'knows', 'what']
        default: what
      but:
        description: i guess we need one
        type: str
        required: true


- name: verify vars needed for this task file are present when included, with spec from a spec file
  ansible.builtin.validate_argument_spec:
    argument_spec: "{{ (lookup('ansible.builtin.file', 'myargspec.yml') | from_yaml )['specname']['options'] }}"


- name: verify vars needed for next include and not from inside it, also with params i'll only define there
  block:
    - ansible.builtin.validate_argument_spec:
        argument_spec: "{{ lookup('ansible.builtin.file', 'nakedoptions.yml') }}"
        provided_arguments:
          but: "that i can define on the include itself, like in it's `vars:` keyword"

    - name: the include itself
      vars:
        stuff: knows
        but: nobuts!
```

---

## ansible.builtin.from_yaml_all filter – Convert a series of YAML documents into a variable structure — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/from_yaml_all_filter.html

**Contents:**
- ansible.builtin.from_yaml_all filter – Convert a series of YAML documents into a variable structure
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name from_yaml_all. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.from_yaml_all for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts a YAML documents in a string representation into an equivalent structured Ansible variable.

Ansible internally auto-converts YAML strings into variable structures in most contexts, but by default does not handle ‘multi document’ YAML files or strings.

If multiple YAML documents are not supplied, this is the equivalence of using from_yaml.

This describes the input of the filter, the value before | ansible.builtin.from_yaml_all.

This filter functions as a wrapper to the Python yaml.safe_load_all function, part of the pyyaml Python library.

Possible conflicts in variable names from the multiple documents are resolved directly by the pyyaml library.

The variable resulting from deserializing the YAML documents.

**Examples:**

Example 1 (unknown):
```unknown
# variable from string variable containing YAML documents
{{ multidoc_yaml_string | from_yaml_all }}

# variable from multidocument YAML string
{{ '---\n{"a": true, "b": 54, "c": [1,2,3]}\n...\n---{"x": 1}\n...\n' | from_yaml_all }}
```

---

## ansible.builtin.user module – Manage user accounts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/user_module.html

**Contents:**
- ansible.builtin.user module – Manage user accounts
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name user even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.user for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Manage user accounts and user attributes.

For Windows targets, use the ansible.windows.win_user module instead.

If true, add the user to the groups specified in groups.

If false, user will only be added to the groups specified in groups, removing them from all other groups.

Sets the authorization of the user.

Can set multiple authorizations using comma separation.

To delete all authorizations, use authorization=''.

Currently supported on Illumos/Solaris. Does nothing when used with other platforms.

Optionally sets the description (aka GECOS) of user account.

On macOS, this defaults to the name option.

Unless set to false, a home directory will be made for the user when the account is created or if the home directory does not exist.

Changed from createhome to create_home in Ansible 2.5.

An expiry time for the user in epoch, it will be ignored on platforms that do not support this.

Currently supported on GNU/Linux, FreeBSD, and DragonFlyBSD.

Since Ansible 2.6 you can remove the expiry time by specifying a negative value. Currently supported on GNU/Linux and FreeBSD.

This only affects state=absent, it forces removal of the user and associated directories on supported platforms.

The behavior is the same as userdel --force, check the man page for userdel on your system for details and support.

When used with generate_ssh_key=yes this forces an existing key to be overwritten.

Whether to generate a SSH key for the user in question.

This will not overwrite an existing SSH key unless used with force=yes.

Optionally sets the user’s primary group (takes a group name).

On macOS, this defaults to staff.

list / elements=string

A list of supplementary groups which the user is also a member of.

By default, the user is removed from all other groups. Configure append to modify this.

When set to an empty string '', the user is removed from all groups except the primary group.

Before Ansible 2.3, the only input format allowed was a comma separated string.

macOS only, optionally hide the user from the login window and system preferences.

The default will be true if the system option is used.

Optionally set the user’s home directory.

Forces the use of “local” command alternatives on platforms that implement it.

This is useful in environments that use centralized authentication when you want to manipulate the local users (in other words, it uses luseradd instead of useradd).

This will check /etc/passwd for an existing account before invoking commands. If the local account database exists somewhere other than /etc/passwd, this setting will not work properly.

This requires that the above commands as well as /etc/passwd must exist on the target host, otherwise it will be a fatal error.

Optionally sets the user’s login class, a feature of most BSD OSs.

If set to true when used with home, attempt to move the user’s old home directory to the specified directory if it isn’t there already and the old home exists.

Name of the user to create, remove or modify.

Optionally when used with the -u option, this option allows to change the user ID to a non-unique value.

If provided, set the user’s password to the provided encrypted hash (Linux) or plain text password (macOS).

Linux/Unix/POSIX: Enter the hashed password as the value.

See FAQ entry for details on various ways to generate the hash of a password.

To create an account with a locked/disabled password on Linux systems, set this to '!' or '*'.

To create an account with a locked/disabled password on OpenBSD, set this to '*************'.

OS X/macOS: Enter the cleartext password as the value. Be sure to take relevant security precautions.

On macOS, the password specified in the password option will always be set, regardless of whether the user account already exists or not.

When the password is passed as an argument, the ansible.builtin.user module will always return changed to true for macOS systems. Since macOS no longer provides access to the hashed passwords directly.

password_expire_account_disable

added in ansible-core 2.18

Number of days after a password expires until the account is disabled.

Currently supported on AIX, Linux, NetBSD, OpenBSD.

added in ansible-core 2.11

Maximum number of days between password change.

Supported on Linux only.

added in ansible-core 2.11

Minimum number of days between password change.

Supported on Linux only.

added in ansible-core 2.16

Number of days of warning before password expires.

Supported on Linux only.

Lock the password (usermod -L, usermod -U, pw lock).

Implementation differs by platform. This option does not always mean the user cannot login using other methods.

This option does not disable the user, only lock the password.

This must be set to false in order to unlock a currently locked password. The absence of this parameter will not unlock a password.

Currently supported on Linux, FreeBSD, DragonFlyBSD, NetBSD, OpenBSD.

Sets the profile of the user.

Can set multiple profiles using comma separation.

To delete all the profiles, use profile=''.

Currently supported on Illumos/Solaris. Does nothing when used with other platforms.

This only affects state=absent, it attempts to remove directories associated with the user.

The behavior is the same as userdel --remove, check the man page for details and support.

Sets the role of the user.

Can set multiple roles using comma separation.

To delete all roles, use role=''.

Currently supported on Illumos/Solaris. Does nothing when used with other platforms.

Optionally sets the seuser type user_u on SELinux enabled systems.

Optionally set the user’s shell.

On macOS, before Ansible 2.5, the default shell for non-system users was /usr/bin/false. Since Ansible 2.5, the default shell for non-system users on macOS is /bin/bash.

On other operating systems, the default shell is determined by the underlying tool invoked by this module. See Notes for a per platform list of invoked tools.

From Ansible 2.18, the type is changed to path from str.

Optionally set a home skeleton directory.

Requires create_home option!

Optionally specify number of bits in SSH key to create.

The default value depends on ssh-keygen.

Optionally define the comment for the SSH key.

Default: "ansible-generated on $HOSTNAME"

Optionally specify the SSH key filename.

If this is a relative filename then it will be relative to the user’s home directory.

This parameter defaults to .ssh/id_rsa.

Set a passphrase for the SSH key.

If no passphrase is provided, the SSH key will default to having no passphrase.

Optionally specify the type of SSH key to generate.

Available SSH key types will depend on implementation present on target host.

Whether the account should exist or not, taking action if the state is different from what is stated.

See this FAQ entry for additional requirements when removing users on macOS systems.

"present" ← (default)

When creating an account state=present, setting this to true makes the user a system account.

This setting cannot be changed on existing users.

Optionally sets the UID of the user.

added in ansible-core 2.18

Sets the UID_MAX value for user creation.

Overwrites /etc/login.defs default value.

Currently supported on Linux. Does nothing when used with other platforms.

Requires local is omitted or False.

added in ansible-core 2.18

Sets the UID_MIN value for user creation.

Overwrites /etc/login.defs default value.

Currently supported on Linux. Does nothing when used with other platforms.

Requires local is omitted or False.

added in ansible-core 2.12

Sets the umask of the user.

Currently supported on Linux. Does nothing when used with other platforms.

Requires local is omitted or false.

always will update passwords if they differ.

on_create will only set the password for newly created users.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

There are specific requirements per platform on user management utilities. However they generally come pre-installed with the system and Ansible will require they are present at runtime. If they are not, a descriptive error message will be shown.

On SunOS platforms, the shadow file is backed up automatically since this module edits it directly. On other platforms, the shadow file is backed up by the underlying tools used by this module.

On macOS, this module uses dscl to create, modify, and delete accounts. dseditgroup is used to modify group membership. Accounts are hidden from the login window by modifying /Library/Preferences/com.apple.loginwindow.plist.

On FreeBSD, this module uses pw useradd and chpass to create, pw usermod and chpass to modify, pw userdel remove, pw lock to lock, and pw unlock to unlock accounts.

On all other platforms, this module uses useradd to create, usermod to modify, and userdel to remove accounts.

The official documentation on the ansible.posix.authorized_key module.

Add or remove groups.

The official documentation on the ansible.windows.win_user module.

Common return values are documented here, the following are the fields unique to this module:

Whether or not to append the user to groups.

Returned: When state is present and the user exists

Comment section from passwd file, usually the user name.

Returned: When user exists

Sample: "Agent Smith"

Whether or not to create the home directory.

Returned: When user does not exist and not check mode

Whether or not a user account was forcibly deleted.

Returned: When state is absent and user exists

Primary user group ID

Returned: When user exists

List of groups of which the user is a member.

Returned: When groups is not empty and state is present

Sample: "chrony,apache"

Path to user’s home directory.

Returned: When state is present

Sample: "/home/asmith"

Whether or not to move an existing home directory.

Returned: When state is present and user exists

Masked value of the password.

Returned: When state is present and password is not empty

Sample: "NOT_LOGGING_PASSWORD"

Whether or not to remove the user account.

Returned: When state is absent and user exists

Returned: When state is present

Fingerprint of generated SSH key.

Returned: When generate_ssh_key is True

Sample: "2048 SHA256:aYNHYcyVm87Igh0IMEDMbvW0QDlRQfE0aJugp684ko8 ansible-generated on host (RSA)"

Path to generated SSH private key file.

Returned: When generate_ssh_key is True

Sample: "/home/asmith/.ssh/id_rsa"

Generated SSH public key file.

Returned: When generate_ssh_key is True

Sample: "'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC95opt4SPEC06tOYsJQJIuN23BbLMGmYo8ysVZQc4h2DZE9ugbjWWGS1/pweUGjVstgzMkBEeBCByaEf/RJKNecKRPeGd2Bw9DCj/bn5Z6rGfNENKBmo 618mUJBvdlEgea96QGjOwSB7/gmonduC7gsWDMNcOdSE3wJMTim4lddiBx4RgC9yXsJ6Tkz9BHD73MXPpT5ETnse+A3fw3IGVSjaueVnlUyUmOBf7fzmZbhlFVXf2Zi2rFTXqvbdGHKkzpw1U8eB8xFPP7y d5u1u0e6Acju/8aZ/l17IDFiLke5IzlqIMRTEbDwLNeO84YQKWTm9fODHzhYe0yvxqLiK07 ansible-generated on host'\n"

Standard error from running commands.

Returned: When stderr is returned by a command that is run

Sample: "Group wheels does not exist"

Standard output from running commands.

Returned: When standard output is returned by the command that is run

Whether or not the account is a system account.

Returned: When system is passed to the module and the account does not exist

User ID of the user account.

Returned: When uid is passed to the module

Stephen Fromm (@sfromm)

**Examples:**

Example 1 (unknown):
```unknown
- name: Add the user 'johnd' with a specific uid and a primary group of 'admin'
  ansible.builtin.user:
    name: johnd
    comment: John Doe
    uid: 1040
    group: admin

- name: Create a user 'johnd' with a home directory
  ansible.builtin.user:
    name: johnd
    create_home: yes

- name: Add the user 'james' with a bash shell, appending the group 'admins' and 'developers' to the user's groups
  ansible.builtin.user:
    name: james
    shell: /bin/bash
    groups: admins,developers
    append: yes

- name: Remove the user 'johnd'
  ansible.builtin.user:
    name: johnd
    state: absent
    remove: yes

- name: Create a 2048-bit SSH key for user jsmith in ~jsmith/.ssh/id_rsa
  ansible.builtin.user:
    name: jsmith
    generate_ssh_key: yes
    ssh_key_bits: 2048
    ssh_key_file: .ssh/id_rsa

- name: Added a consultant whose account you want to expire
  ansible.builtin.user:
    name: james18
    shell: /bin/zsh
    groups: developers
    expires: 1422403387

- name: Starting at Ansible 2.6, modify user, remove expiry time
  ansible.builtin.user:
    name: james18
    expires: -1

- name: Set maximum expiration date for password
  ansible.builtin.user:
    name: ram19
    password_expire_max: 10

- name: Set minimum expiration date for password
  ansible.builtin.user:
    name: pushkar15
    password_expire_min: 5

- name: Set number of warning days for password expiration
  ansible.builtin.user:
    name: jane157
    password_expire_warn: 30

- name: Set number of days after password expires until account is disabled
  ansible.builtin.user:
    name: jimholden2016
    password_expire_account_disable: 15
```

---

## ansible.builtin.include_tasks module – Dynamically include a task list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/include_tasks_module.html

**Contents:**
- ansible.builtin.include_tasks module – Dynamically include a task list
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name include_tasks even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.include_tasks for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Includes a file with a list of tasks to be executed in the current playbook.

Accepts a hash of task keywords (for example tags, become) that will be applied to the tasks within the include.

Specifies the name of the file that lists tasks to add to the current playbook.

Specifies the name of the imported file directly without any other option - include_tasks: file.yml.

Is the equivalent of specifying an argument for the file parameter.

Most keywords, including loop, with_items, and conditionals, apply to this statement unlike ansible.builtin.import_tasks.

The do-until loop is not supported.

While this action executes locally on the controller it is not governed by an action plugin

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Since there are no connection nor facts, there is no sense in delegating includes

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Tags are interpreted by this action but are not automatically inherited by the include tasks, see apply

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Import a role into a play.

Load and execute a role.

More information related to including and importing playbooks, roles and tasks.

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: task1

    - name: Include task list in play
      ansible.builtin.include_tasks:
        file: stuff.yaml

    - ansible.builtin.debug:
        msg: task10

- hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: task1

    - name: Include task list in play only if the condition is true
      ansible.builtin.include_tasks: "{{ hostvar }}.yaml"
      when: hostvar is defined

- name: Apply tags to tasks within included file
  ansible.builtin.include_tasks:
    file: install.yml
    apply:
      tags:
        - install
  tags:
    - always

- name: Apply tags to tasks within included file when using free-form
  ansible.builtin.include_tasks: install.yml
  args:
    apply:
      tags:
        - install
  tags:
    - always
```

---

## Migrating Roles to Roles in Collections on Galaxy — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/migrating_roles.html

**Contents:**
- Migrating Roles to Roles in Collections on Galaxy
- Comparing standalone roles to collection roles
- Migrating a role to a collection
- Migrating a role that contains plugins to a collection
  - Migrating other role plugins to a collection
    - Updating module_utils
    - Importing from __init__.py
  - Example: Migrating a standalone role with plugins to a collection
  - Example: Supporting standalone roles and migrated collection roles in a downstream RPM
- Using ansible.legacy to access local custom modules from collections-based roles

You can migrate any existing standalone role into a collection and host the collection on Galaxy. With Ansible collections, you can distribute many roles in a single cohesive unit of reusable automation. Inside a collection, you can share custom plugins across all roles in the collection instead of duplicating them in each role’s library/` directory.

You must migrate roles to collections if you want to distribute them as certified Ansible content.

If you want to import your collection to Galaxy, you need a Galaxy namespace.

See Developing collections for details on collections.

Comparing standalone roles to collection roles

Migrating a role to a collection

Migrating a role that contains plugins to a collection

Using ansible.legacy to access local custom modules from collections-based roles

Standalone roles have the following directory structure:

The highlighted directories above will change when you migrate to a collection-based role. The collection directory structure includes a roles/ directory:

You will need to use the Fully Qualified Collection Name (FQCN) to use the roles and plugins when you migrate your role into a collection. The FQCN is the combination of the collection namespace, collection name, and the content item you are referring to.

So for example, in the above collection, the FQCN to access role1 would be:

A collection can contain one or more roles in the roles/ directory and these are almost identical to standalone roles, except you need to move plugins out of the individual roles, and use the FQCN in some places, as detailed in the next section.

In standalone roles, some of the plugin directories referenced their plugin types in the plural sense; this is not the case in collections.

To migrate from a standalone role that contains no plugins to a collection role:

Create a local ansible_collections directory and cd to this new directory.

Create a collection. If you want to import this collection to Ansible Galaxy, you need a Galaxy namespace.

This creates the collection directory structure.

Copy the standalone role directory into the roles/ subdirectory of the collection. Roles in collections cannot have hyphens in the role name. Rename any such roles to use underscores instead.

Update galaxy.yml to include any role dependencies.

Update the collection README.md file to add links to any role README.md files.

To migrate from a standalone role that has plugins to a collection role:

Create a local ansible_collections directory and cd to this new directory.

Create a collection. If you want to import this collection to Ansible Galaxy, you need a Galaxy namespace.

This creates the collection directory structure.

Copy the standalone role directory into the roles/ subdirectory of the collection. Roles in collections cannot have hyphens in the role name. Rename any such roles to use underscores instead.

Move any modules to the plugins/modules/ directory.

Move any other plugins to the appropriate plugins/PLUGINTYPE/ directory. See Migrating other role plugins to a collection for additional steps that may be required.

Update galaxy.yml to include any role dependencies.

Update the collection README.md file to add links to any role README.md files.

Change any references to the role to use the FQCN.

You can alternately use the collections keyword to simplify this:

To migrate other role plugins to a collection:

Move each nonmodule plugins to the appropriate plugins/PLUGINTYPE/ directory. The mynamespace/mycollection/plugins/README.md file explains the types of plugins that the collection can contain within optionally created subdirectories.

Update documentation to use the FQCN. Plugins that use doc_fragments need to use FQCN (for example, mydocfrag becomes mynamespace.mycollection.mydocfrag).

Update relative imports work in collections to start with a period. For example, ./filename and ../asdfu/filestuff works but filename in same directory must be updated to ./filename.

If you have a custom module_utils or import from __init__.py, you must also:

Change the Python namespace for custom module_utils to use the FQCN along with the ansible_collections convention. See Updating module_utils.

Change how you import from __init__.py. See Importing from __init__.py.

If any of your custom modules use a custom module utility, once you migrate to a collection you cannot address the module utility in the top level ansible.module_utils Python namespace. Ansible does not merge content from collections into the Ansible internal Python namespace. Update any Python import statements that refer to custom module utilities when you migrate your custom content to collections. See module_utils in collections for more details.

When coding with module_utils in a collection, the Python import statement needs to take into account the FQCN along with the ansible_collections convention. The resulting Python import looks similar to the following example:

You need to follow the same rules in changing paths and using namespaced names for subclassed plugins.

The following example code snippets show a Python and a PowerShell module using both default Ansible module_utils and those provided by a collection. In this example the namespace is ansible_example and the collection is community.

In the Python example the module_utils is helper and the FQCN is ansible_example.community.plugins.module_utils.helper:

In the PowerShell example the module_utils is hyperv and the FQCN is ansible_example.community.plugins.module_utils.hyperv:

Because of the way that the CPython interpreter does imports, combined with the way the Ansible plugin loader works, if your custom embedded module or plugin requires importing something from an __init__.py file, that also becomes part of your collection. You can either originate the content inside a standalone role or use the file name in the Python import statement. The following example is an __init__.py file that is part of a callback plugin found inside a collection named ansible_example.community.

In this example we have a standalone role called my-standalone-role.webapp to emulate a standalone role that contains dashes in the name (which is not valid in collections). This standalone role contains a custom module in the library/ directory called manage_webserver.

Create a new collection, for example, acme.webserver:

Create the webapp role inside the collection and copy all contents from the standalone role:

Move the manage_webserver module to its new home in acme/webserver/plugins/modules/:

This example changed the original source file manage_webserver.py to the destination file manage.py. This is optional but the FQCN provides the webserver context as acme.webserver.manage.

Change manage_webserver to acme.webserver.manage in tasks/ files in the role ( for example, my-standalone-role.webapp/tasks/main.yml) and any use of the original module name.

This name change is only required if you changed the original module name, but illustrates content referenced by FQCN can offer context and in turn can make module and plugin names shorter. If you anticipate using these modules independent of the role, keep the original naming conventions. Users can add the collections keyword in their playbooks. Typically roles are an abstraction layer and users won’t use components of the role independently.

A standalone role can co-exist with its collection role counterpart (for example, as part of a support lifecycle of a product). This should only be done for a transition period, but these two can exist in downstream in packages such as RPMs. For example, the RHEL system roles could coexist with an example of a RHEL system roles collection and provide existing backwards compatibility with the downstream RPM.

This section walks through an example creating this coexistence in a downstream RPM and requires Ansible 2.9.0 or later.

To deliver a role as both a standalone role and a collection role:

Place the collection in /usr/share/ansible/collections/ansible_collections/.

Copy the contents of the role inside the collection into a directory named after the standalone role and place the standalone role in /usr/share/ansible/roles/.

All previously bundled modules and plugins used in the standalone role are now referenced by FQCN so even though they are no longer embedded, they can be found from the collection contents.This is an example of how the content inside the collection is a unique entity and does not have to be bound to a role or otherwise. You could alternately create two separate collections: one for the modules and plugins and another for the standalone role to migrate to. The role must use the modules and plugins as FQCN.

The following is an example RPM spec file that accomplishes this using this example content:

Some roles within a collection use local custom modules that are not part of the collection itself. If there is a conflict between the custom module short name and the collection module name, you need to specify which module your tasks call. You can update the tasks to change local_module_name to ansible.legacy.local_module_name to ensure you are using the custom module.

**Examples:**

Example 1 (unknown):
```unknown
role/
  ├── defaults
  ├── files
  ├── handlers
  ├── library
  ├── meta
  ├── module_utils
  ├── [*_plugins]
  ├── tasks
  ├── templates
  ├── tests
  └── vars
```

Example 2 (unknown):
```unknown
mynamespace/
└── mycollection/
  ├── docs/
  ├── galaxy.yml
  ├── plugins/
  │   ├── modules/
  │   │   └── module1.py
  │   ├── inventory/
  │   └── .../
  ├── README.md
  ├── roles/
  │   ├── role1/
  │   ├── role2/
  │   └── .../
  ├── playbooks/
  │   ├── files/
  │   ├── vars/
  │   ├── templates/
  │   └── tasks/
  └── tests/
```

Example 3 (unknown):
```unknown
mynamespace.mycollection.role1
```

Example 4 (unknown):
```unknown
$ ansible-galaxy collection init mynamespace.mycollection
```

---

## Testing collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_testing.html

**Contents:**
- Testing collections
- Testing tools
  - Sanity tests
  - Adding unit tests
  - Adding integration tests

Testing your collection ensures that your code works well and integrates well with the rest of the Ansible ecosystem. Your collection should pass the sanity tests for Ansible code. You should also add unit tests to cover the code in your collection and integration tests to cover the interactions between your collection and ansible-core.

Adding integration tests

The main tool for testing collections is ansible-test, Ansible’s testing tool described in Testing Ansible and provided by both the ansible and ansible-core packages.

Use ansible-test tool from your collection directory, which must include ansible_collections in the path, for example collections/ansible_collections/community/general for the community.general collection. See Testing Collection Contributions and Testing Ansible and Collections for testing guidelines.

You can run several sanity tests, as well as run unit and integration tests for plugins using ansible-test. When you test collections, test against the ansible-core version(s) you are targeting.

You must always execute ansible-test from the root directory of a collection. You can run ansible-test in Docker containers without installing any special requirements. The Ansible team uses this approach in Azure Pipelines both in the ansible/ansible GitHub repository and in the large community collections such as community.general and community.network to automatically run the tests when pull requests are submitted.

Many collections which do not require running tests on different OS distributions use GitHub Actions as their continuous integration (CI) platform. The collection_template repository contains GitHub Actions workflow templates that collection developers are free to use to easily set up CI in their collection repositories.

The examples below demonstrate running tests in Docker containers.

To run all sanity tests:

See Sanity Tests for more information. See the full list of sanity tests for details on the sanity tests and how to fix identified issues.

You must place unit tests in the appropriate tests/unit/plugins/ directory. For example, you would place tests for plugins/module_utils/foo/bar.py in tests/unit/plugins/module_utils/foo/test_bar.py or tests/unit/plugins/module_utils/foo/bar/test_bar.py. For examples, see the unit tests in community.general.

To run all unit tests for all supported Python versions:

To run all unit tests only for a specific Python version:

To run only a specific unit test:

You can specify Python requirements in the tests/unit/requirements.txt file. See Unit Tests for more information, especially on fixture files.

You must place integration tests in the appropriate tests/integration/targets/ directory. For module integration tests, you can use the module name alone. For example, you would place integration tests for plugins/modules/foo.py in a directory called tests/integration/targets/foo/. For non-module plugin integration tests, you must add the plugin type to the directory name. For example, you would place integration tests for plugins/connections/bar.py in a directory called tests/integration/targets/connection_bar/. For lookup plugins, the directory must be called lookup_foo, for inventory plugins, inventory_foo, and so on.

You can write two different kinds of integration tests:

Ansible role tests run with ansible-playbook and validate various aspects of the module. They can depend on other integration tests (usually named prepare_bar or setup_bar, which prepare a service or install a requirement named bar in order to test module foo) to set-up required resources, such as installing required libraries or setting up server services.

runme.sh tests run directly as scripts. They can set up inventory files, and execute ansible-playbook or ansible-inventory with various settings.

For examples, see the integration tests in community.general. See also Integration tests for more details.

Since integration tests can install requirements, and set-up, start and stop services, we recommended running them in docker containers or otherwise restricted environments whenever possible. By default, ansible-test supports Docker images for several operating systems. See the list of supported docker images for all options. Use the default image mainly for platform-independent integration tests, such as those for cloud modules. The following examples use the fedora35 image.

To execute all integration tests for a collection:

If you want more detailed output, run the command with -vvv instead of -v. Alternatively, specify --retry-on-error to automatically re-run failed tests with higher verbosity levels.

To execute only the integration tests in a specific directory:

You can specify multiple target names. Each target name is the name of a directory in tests/integration/targets/.

More resources on testing Ansible

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
ansible-test sanity --docker default -v
```

Example 2 (unknown):
```unknown
ansible-test units --docker default -v
```

Example 3 (unknown):
```unknown
ansible-test units --docker default -v --python 3.6
```

Example 4 (unknown):
```unknown
ansible-test units --docker default -v --python 3.6 tests/unit/plugins/module_utils/foo/test_bar.py
```

---

## ansible.builtin.known_hosts module – Add or remove a host from the known_hosts file — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/known_hosts_module.html

**Contents:**
- ansible.builtin.known_hosts module – Add or remove a host from the known_hosts file
- Synopsis
- Parameters
- Attributes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name known_hosts even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.known_hosts for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.known_hosts module lets you add or remove host keys from the known_hosts file.

Starting at Ansible 2.2, multiple entries per host are allowed, but only one for each key type supported by ssh. This is useful if you’re going to want to use the ansible.builtin.git module over ssh, for example.

If you have a very large number of host keys to manage, you will find the ansible.builtin.template module more useful.

Hash the hostname in the known_hosts file.

The SSH public host key, as a string.

Required if state=present, optional when state=absent, in which case all keys for the host are removed.

The key must be in the right format for SSH (see sshd(8), section “SSH_KNOWN_HOSTS FILE FORMAT”).

Specifically, the key should not match the format that is found in an SSH pubkey file, but should rather have the hostname prepended to a line that includes the pubkey, the same way that it would appear in the known_hosts file. The value prepended to the line must also match the value of the name parameter.

Should be of format <hostname[,IP]> ssh-rsa <pubkey>.

For custom SSH port, key needs to specify port as well. See example section.

The host to add or remove (must match a host specified in key). It will be converted to lowercase so that ssh-keygen can find it.

Must match with <hostname> or <ip> present in key attribute.

For custom SSH port, name needs to specify port as well. See example section.

The known_hosts file to edit.

The known_hosts file will be created if needed. The rest of the path must exist prior to running the module.

Default: "~/.ssh/known_hosts"

present to add host keys.

absent to remove host keys.

"present" ← (default)

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Matthew Vernon (@mcv21)

**Examples:**

Example 1 (unknown):
```unknown
- name: Tell the host about our servers it might want to ssh to
  ansible.builtin.known_hosts:
    path: /etc/ssh/ssh_known_hosts
    name: foo.com.invalid
    key: "{{ lookup('ansible.builtin.file', 'pubkeys/foo.com.invalid') }}"

- name: Another way to call known_hosts
  ansible.builtin.known_hosts:
    name: host1.example.com   # or 10.9.8.77
    key: host1.example.com,10.9.8.77 ssh-rsa ASDeararAIUHI324324  # some key gibberish
    path: /etc/ssh/ssh_known_hosts
    state: present

- name: Add host with custom SSH port
  ansible.builtin.known_hosts:
    name: '[host1.example.com]:2222'
    key: '[host1.example.com]:2222 ssh-rsa ASDeararAIUHI324324' # some key gibberish
    path: /etc/ssh/ssh_known_hosts
    state: present
```

---

## ansible.builtin.password_hash filter – convert input password into password_hash — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/password_hash_filter.html

**Contents:**
- ansible.builtin.password_hash filter – convert input password into password_hash
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name password_hash. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.password_hash for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a password_hash of a secret.

This describes the input of the filter, the value before | ansible.builtin.password_hash.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.password_hash(key1=value1, key2=value2, ...)

Hashing algorithm to use.

Algorithm identifier.

Number of encryption rounds, default varies by algorithm used.

Secret string used for the hashing. If none is provided a random one can be generated. Use only numbers and letters (characters matching [./0-9A-Za-z]+).

Algorithms available might be restricted by the system.

Algorithms may restrict salt length or content. For example, Blowfish/bcrypt requires a 22-character salt.

The resulting password hash.

**Examples:**

Example 1 (javascript):
```javascript
# pwdhash => "$6$/bQCntzQ7VrgVcFa$VaMkmevkY1dqrx8neaenUDlVU.6L/.ojRbrnI4ID.yBHU6XON1cB422scCiXfUL5wRucMdLgJU0Fn38uoeBni/"
pwdhash: "{{ 'testing' | password_hash }}"

# Using hash type
# wireguard_admin_password_hash => "$2b$12$ujYVRD9v9z87lpvLqeWNuOFDI4QzSSYHoRyYydW6XK4.kgqfwOXzO"
wireguard_admin_password_hash: "{{ 'vagrant-libvirt' | password_hash(hashtype='bcrypt') }}"

# Using salt value for idempotency
# wireguard_admin_password_hash => "$2b$12$abcdefghijklmnopqrstuuTEw8POU2MwwuYEM7WaKcjqZ948Hm7.W"
wireguard_admin_password_hash: "{{ 'vagrant-libvirt' | password_hash(hashtype='bcrypt', salt='abcdefghijklmnopqrstuv') }}"
```

---

## ansible.builtin.items filter – Return an iterator over the ``(key, value)`` items of a mapping. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/items_filter.html

**Contents:**
- ansible.builtin.items filter – Return an iterator over the ``(key, value)`` items of a mapping.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name items. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.items for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return an iterator over the ``(key, value)`` items of a mapping.

This is the Jinja builtin filter plugin ‘items’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.items

---

## ansible.builtin.sum filter – Returns the sum of a sequence of numbers plus the value of parameter ‘start’. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sum_filter.html

**Contents:**
- ansible.builtin.sum filter – Returns the sum of a sequence of numbers plus the value of parameter ‘start’.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sum. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sum for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the sum of a sequence of numbers plus the value of parameter ‘start’.

This is the Jinja builtin filter plugin ‘sum’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.sum

---

## ansible.builtin.contains test – does the list contain this element — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/contains_test.html

**Contents:**
- ansible.builtin.contains test – does the list contain this element
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name contains. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.contains for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Checks the supplied element against the input list to see if it exists within it.

This describes the input of the test, the value before is ansible.builtin.contains or is not ansible.builtin.contains.

list / elements=any / required

List of elements to compare.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.contains(key1=value1, key2=value2, ...) and input is not ansible.builtin.contains(key1=value1, key2=value2, ...)

Returns True if the specified element is contained in the supplied sequence, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# simple expression
{{ listofthings is contains('this') }}

# as a selector
- action: module=doessomething
  when: (lacp_groups|selectattr('interfaces', 'contains', 'em1')|first).master
  vars:
    lacp_groups:
      - master: lacp0
        network: 10.65.100.0/24
        gateway: 10.65.100.1
        dns4:
          - 10.65.100.10
          - 10.65.100.11
        interfaces:
          - em1
          - em2

      - master: lacp1
        network: 10.65.120.0/24
        gateway: 10.65.120.1
        dns4:
          - 10.65.100.10
          - 10.65.100.11
        interfaces:
            - em3
            - em4
```

---

## ansible.builtin.commonpath filter – gets the common path — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/commonpath_filter.html

**Contents:**
- ansible.builtin.commonpath filter – gets the common path
- Synopsis
- Input
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name commonpath. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.commonpath for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.15

Returns the longest common path from the given list of paths.

This describes the input of the filter, the value before | ansible.builtin.commonpath.

list / elements=path / required

get a path’s base name.

The longest common path from the given list of paths.

**Examples:**

Example 1 (unknown):
```unknown
# To get the longest common path (for example - '/foo/bar') from the given list of paths
# (for example - ['/foo/bar/foobar','/foo/bar'])
{{ listofpaths | commonpath }}
```

---

## ansible.builtin.equalto test – Same as a == b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/equalto_test.html

**Contents:**
- ansible.builtin.equalto test – Same as a == b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name equalto. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.equalto for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘equalto’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.equalto

---

## ansible.builtin.sort filter – Sort an iterable using Python’s :func:`sorted`. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sort_filter.html

**Contents:**
- ansible.builtin.sort filter – Sort an iterable using Python’s :func:`sorted`.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sort. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sort for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Sort an iterable using Python’s :func:`sorted`.

This is the Jinja builtin filter plugin ‘sort’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.sort

---

## ansible.builtin.safe filter – Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/safe_filter.html

**Contents:**
- ansible.builtin.safe filter – Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name safe. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.safe for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.

This is the Jinja builtin filter plugin ‘safe’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.safe

---

## ansible.builtin.iptables module – Modify iptables rules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/iptables_module.html

**Contents:**
- ansible.builtin.iptables module – Modify iptables rules
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name iptables even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.iptables for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

ansible.builtin.iptables is used to set up, maintain, and inspect the tables of IP packet filter rules in the Linux kernel.

This module does not handle the saving and/or loading of rules, but rather only manipulates the current rules that are present in memory. This is the same as the behaviour of the iptables and ip6tables command which this module uses internally.

Whether the rule should be appended at the bottom or inserted at the top.

If the rule already exists the chain will not be modified.

Specify the iptables chain to modify.

This could be a user-defined chain or one of the standard iptables chains, like INPUT, FORWARD, OUTPUT, PREROUTING, POSTROUTING, SECMARK or CONNSECMARK.

added in ansible-core 2.13

If true and state is present, the chain will be created if needed.

If true and state is absent, the chain will be deleted if the only other parameter passed are chain and optionally table.

This specifies a comment that will be added to the rule.

list / elements=string

A list of the connection states to match in the conntrack module.

Possible values are INVALID, NEW, ESTABLISHED, RELATED, UNTRACKED, SNAT, DNAT.

Destination specification.

Address can be either a network name, a hostname, a network IP address (with /mask), or a plain IP address.

Hostnames will be resolved once only, before the rule is submitted to the kernel. Please note that specifying any name to be resolved with a remote query such as DNS is a really bad idea.

The mask can be either a network mask or a plain number, specifying the number of 1’s at the left side of the network mask. Thus, a mask of 24 is equivalent to 255.255.255.0. A ! argument before the address specification inverts the sense of the address.

Destination port or port range specification. This can either be a service name or a port number. An inclusive range can also be specified, using the format first:last. If the first port is omitted, ‘0’ is assumed; if the last is omitted, ‘65535’ is assumed. If the first port is greater than the second one they will be swapped. This is only valid if the rule also specifies one of the following protocols: tcp, udp, dccp or sctp.

list / elements=string

added in ansible-core 2.11

This specifies multiple destination port numbers or port ranges to match in the multiport module.

It can only be used in conjunction with the protocols tcp, udp, udplite, dccp and sctp.

Specifies the destination IP range to match in the iprange module.

Flushes the specified table and chain of all rules.

If no chain is specified then the entire table is purged.

Ignores all other parameters.

This means that the rule only refers to second and further fragments of fragmented packets.

Since there is no way to tell the source or destination ports of such a packet (or ICMP type), such a packet will not match any rules which specify them.

When the “!” argument precedes the fragment argument, the rule will only match head fragments, or unfragmented packets.

This specifies the IP address of the host to send the cloned packets.

This option is only valid when jump=TEE.

Specifies the GID or group to use in the match by owner rule.

This specifies that the processing should continue in a user-specified chain.

Unlike the jump argument return will not continue processing in this chain but instead in the chain that called us via jump.

This allows specification of the ICMP type, which can be a numeric ICMP type, type/code pair, or one of the ICMP type names shown by the command iptables -p icmp -h.

Name of an interface via which a packet was received (only for packets entering the INPUT, FORWARD and PREROUTING chains).

When the ! argument is used before the interface name, the sense is inverted.

If the interface name ends in a +, then any interface which begins with this name will match.

If this option is omitted, any interface name will match.

Which version of the IP protocol this rule should apply to.

This specifies the target of the rule; i.e., what to do if the packet matches it.

The target can be a user-defined chain (other than the one this rule is in), one of the special builtin targets that decide the fate of the packet immediately, or an extension (see EXTENSIONS below).

If this option is omitted in a rule (and the goto parameter is not used), then matching the rule will have no effect on the packet’s fate, but the counters on the rule will be incremented.

Specifies the maximum average number of matches to allow per second.

The number can specify units explicitly, using /second, /minute, /hour or /day, or parts of them (so 5/second is the same as 5/s).

Specifies the maximum burst before the above limit kicks in.

Logging level according to the syslogd-defined priorities.

The value can be strings or numbers from 1-8.

This parameter is only applicable if jump=LOG.

Specifies a log text for the rule. Only makes sense with a LOG jump.

list / elements=string

Specifies a match to use, that is, an extension module that tests for a specific property.

The set of matches makes up the condition under which a target is invoked.

Matches are evaluated first to last if specified as an array and work in short-circuit fashion, in other words if one extension yields false, the evaluation will stop.

added in ansible-core 2.11

Specifies a set name that can be defined by ipset.

Must be used together with the match_set_flags parameter.

When the ! argument is prepended then it inverts the rule.

Uses the iptables set extension.

added in ansible-core 2.11

Specifies the necessary flags for the match_set parameter.

Must be used together with the match_set parameter.

Uses the iptables set extension.

Choices dst,dst and src,src added in version 2.17.

added in ansible-core 2.15

This parameter controls the running of the list -action of iptables, which is used internally by the module.

Does not affect the actual functionality. Use this if iptables hang when creating a chain or altering policy.

If true, then iptables skips the DNS-lookup of the IP addresses in a chain when it uses the list -action.

Listing is used internally for example when setting a policy or creating a chain.

Name of an interface via which a packet is going to be sent (for packets entering the FORWARD, OUTPUT and POSTROUTING chains).

When the ! argument is used before the interface name, the sense is inverted.

If the interface name ends in a +, then any interface which begins with this name will match.

If this option is omitted, any interface name will match.

Set the policy for the chain to the given target.

Only built-in chains can have policies.

This parameter requires the chain parameter.

If you specify this parameter, all other parameters will be ignored.

This parameter is used to set the default policy for the given chain. Do not confuse this with jump parameter.

The protocol of the rule or of the packet to check.

The specified protocol can be one of tcp, udp, udplite, icmp, ipv6-icmp or icmpv6, esp, ah, sctp or the special keyword all, or it can be a numeric value, representing one of these protocols or a different one.

A protocol name from /etc/protocols is also allowed.

A ! argument before the protocol inverts the test.

The number zero is equivalent to all.

all will match with all protocols and is taken as default when this option is omitted.

Specifies the error packet type to return while rejecting. It implies jump=REJECT.

Insert the rule as the given rule number.

This works only with action=insert.

This enables the administrator to initialize the packet and byte counters of a rule (during INSERT, APPEND, REPLACE operations).

This allows specifying a DSCP mark to be added to packets. It takes either an integer or hex value.

If the parameter is set, jump is set to DSCP.

Mutually exclusive with set_dscp_mark_class.

This allows specifying a predefined DiffServ class which will be translated to the corresponding DSCP mark.

If the parameter is set, jump is set to DSCP.

Mutually exclusive with set_dscp_mark.

Source specification.

Address can be either a network name, a hostname, a network IP address (with /mask), or a plain IP address.

Hostnames will be resolved once only, before the rule is submitted to the kernel. Please note that specifying any name to be resolved with a remote query such as DNS is a really bad idea.

The mask can be either a network mask or a plain number, specifying the number of 1’s at the left side of the network mask. Thus, a mask of 24 is equivalent to 255.255.255.0. A ! argument before the address specification inverts the sense of the address.

Source port or port range specification.

This can either be a service name or a port number.

An inclusive range can also be specified, using the format first:last.

If the first port is omitted, 0 is assumed; if the last is omitted, 65535 is assumed.

If the first port is greater than the second one they will be swapped.

Specifies the source IP range to match the iprange module.

Whether the rule should be absent or present.

"present" ← (default)

This allows matching packets that have the SYN bit set and the ACK and RST bits unset.

When negated, this matches all packets with the RST or the ACK bits set.

This option specifies the packet matching table on which the command should operate.

If the kernel is configured with automatic module loading, an attempt will be made to load the appropriate module for that table if it is not already there.

TCP flags specification.

tcp_flags expects a dict with the two keys flags and flags_set.

list / elements=string

List of flags you want to examine.

list / elements=string

This specifies a destination address to use with ctstate=DNAT.

Without this, the destination address is never altered.

This specifies a destination port or range of ports to use, without this, the destination port is never altered.

This is only valid if the rule also specifies one of the protocol tcp, udp, dccp or sctp.

This specifies a source address to use with ctstate=SNAT.

Without this, the source address is never altered.

Specifies the UID or username to use in the match by owner rule.

From Ansible 2.6 when the ! argument is prepended then the it inverts the rule to apply instead to all users except that one specified.

added in ansible-base 2.10

Wait N seconds for the xtables lock to prevent multiple instances of the program from running concurrently.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

This module just deals with individual rules. If you need advanced chaining of rules the recommended way is to template the iptables restore file.

Linus Unnebäck (@LinusU)

Sébastien DA ROCHA (@sebastiendarocha)

**Examples:**

Example 1 (unknown):
```unknown
- name: Block specific IP
  ansible.builtin.iptables:
    chain: INPUT
    source: 8.8.8.8
    jump: DROP
  become: yes

- name: Forward port 80 to 8600
  ansible.builtin.iptables:
    table: nat
    chain: PREROUTING
    in_interface: eth0
    protocol: tcp
    match: tcp
    destination_port: 80
    jump: REDIRECT
    to_ports: 8600
    comment: Redirect web traffic to port 8600
  become: yes

- name: Allow related and established connections
  ansible.builtin.iptables:
    chain: INPUT
    ctstate: ESTABLISHED,RELATED
    jump: ACCEPT
  become: yes

- name: Allow new incoming SYN packets on TCP port 22 (SSH)
  ansible.builtin.iptables:
    chain: INPUT
    protocol: tcp
    destination_port: 22
    ctstate: NEW
    syn: match
    jump: ACCEPT
    comment: Accept new SSH connections.

- name: Match on IP ranges
  ansible.builtin.iptables:
    chain: FORWARD
    src_range: 192.168.1.100-192.168.1.199
    dst_range: 10.0.0.1-10.0.0.50
    jump: ACCEPT

- name: Allow source IPs defined in ipset "admin_hosts" on port 22
  ansible.builtin.iptables:
    chain: INPUT
    match_set: admin_hosts
    match_set_flags: src
    destination_port: 22
    jump: ALLOW

- name: Tag all outbound tcp packets with DSCP mark 8
  ansible.builtin.iptables:
    chain: OUTPUT
    jump: DSCP
    table: mangle
    set_dscp_mark: 8
    protocol: tcp

- name: Tag all outbound tcp packets with DSCP DiffServ class CS1
  ansible.builtin.iptables:
    chain: OUTPUT
    jump: DSCP
    table: mangle
    set_dscp_mark_class: CS1
    protocol: tcp

# Create the user-defined chain ALLOWLIST
- iptables:
    chain: ALLOWLIST
    chain_management: true

# Delete the user-defined chain ALLOWLIST
- iptables:
    chain: ALLOWLIST
    chain_management: true
    state: absent

- name: Insert a rule on line 5
  ansible.builtin.iptables:
    chain: INPUT
    protocol: tcp
    destination_port: 8080
    jump: ACCEPT
    action: insert
    rule_num: 5

# Think twice before running following task as this may lock target system
- name: Set the policy for the INPUT chain to DROP
  ansible.builtin.iptables:
    chain: INPUT
    policy: DROP

- name: Reject tcp with tcp-reset
  ansible.builtin.iptables:
    chain: INPUT
    protocol: tcp
    reject_with: tcp-reset
    ip_version: ipv4

- name: Set tcp flags
  ansible.builtin.iptables:
    chain: OUTPUT
    jump: DROP
    protocol: tcp
    tcp_flags:
      flags: ALL
      flags_set:
        - ACK
        - RST
        - SYN
        - FIN

- name: Iptables flush filter
  ansible.builtin.iptables:
    chain: "{{ item }}"
    flush: yes
  with_items:  [ 'INPUT', 'FORWARD', 'OUTPUT' ]

- name: Iptables flush nat
  ansible.builtin.iptables:
    table: nat
    chain: '{{ item }}'
    flush: yes
  with_items: [ 'INPUT', 'OUTPUT', 'PREROUTING', 'POSTROUTING' ]

- name: Log packets arriving into an user-defined chain
  ansible.builtin.iptables:
    chain: LOGGING
    action: append
    state: present
    limit: 2/second
    limit_burst: 20
    log_prefix: "IPTABLES:INFO: "
    log_level: info

- name: Allow connections on multiple ports
  ansible.builtin.iptables:
    chain: INPUT
    protocol: tcp
    destination_ports:
      - "80"
      - "443"
      - "8081:8083"
    jump: ACCEPT
```

---

## ansible.builtin.list lookup – simply returns what it is given. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/list_lookup.html

**Contents:**
- ansible.builtin.list lookup – simply returns what it is given.
- Synopsis
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name list. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.list for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

this is mostly a noop, to be used as a with_list loop when you dont want the content transformed in any way.

basically the same as you fed in

**Examples:**

Example 1 (unknown):
```unknown
- name: unlike with_items you will get 3 items from this loop, the 2nd one being a list
  ansible.builtin.debug: var=item
  with_list:
    - 1
    - [2,3]
    - 4
```

---

## ansible.builtin.reverse filter – Reverse the object or return an iterator that iterates over it the other way round. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/reverse_filter.html

**Contents:**
- ansible.builtin.reverse filter – Reverse the object or return an iterator that iterates over it the other way round.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name reverse. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.reverse for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Reverse the object or return an iterator that iterates over it the other way round.

This is the Jinja builtin filter plugin ‘reverse’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.reverse

---

## ansible.builtin.reboot module – Reboot a machine — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/reboot_module.html

**Contents:**
- ansible.builtin.reboot module – Reboot a machine
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name reboot even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.reboot for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Reboot a machine, wait for it to go down, come back up, and respond to commands.

For Windows targets, use the ansible.windows.win_reboot module instead.

This module has a corresponding action plugin.

added in ansible-base 2.10

Command to run that returns a unique string indicating the last time the system was booted.

Setting this to a command that has different output each time it is run will cause the task to fail.

Default: "cat /proc/sys/kernel/random/boot_id"

Maximum seconds to wait for a successful connection to the managed hosts before trying again.

If unspecified, the default setting for the underlying connection plugin is used.

Message to display to users before reboot.

Default: "Reboot initiated by Ansible"

Seconds to wait after the reboot command was successful before attempting to validate the system rebooted successfully.

This is useful if you want wait for something to settle despite your connection already working.

Seconds to wait before reboot. Passed as a parameter to the reboot command.

On Linux, macOS and OpenBSD, this is converted to minutes and rounded down. If less than 60, it will be set to 0.

On Solaris and FreeBSD, this will be seconds.

added in ansible-core 2.11

Command to run that reboots the system, including any parameters passed to the command.

Can be an absolute path to the command or just the command name. If an absolute path to the command is not given, search_paths on the target system will be searched to find the absolute path.

This will cause pre_reboot_delay, post_reboot_delay, and msg to be ignored.

Default: "[determined based on target OS]"

Maximum seconds to wait for machine to reboot and respond to a test command.

This timeout is evaluated separately for both reboot verification and test command success so the maximum execution time for the module is twice this amount.

list / elements=string

Paths to search on the remote machine for the shutdown command.

Only these paths will be searched for the shutdown command. PATH is ignored in the remote node when searching for the shutdown command.

Default: ["/sbin", "/bin", "/usr/sbin", "/usr/bin", "/usr/local/sbin"]

Command to run on the rebooted host and expect success from to determine the machine is ready for further tasks.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

PATH is ignored on the remote node when searching for the shutdown command. Use search_paths to specify locations to search if the default paths do not work.

The official documentation on the ansible.windows.win_reboot module.

Common return values are documented here, the following are the fields unique to this module:

The number of seconds that elapsed waiting for the system to be rebooted.

true if the machine was rebooted

Matt Davis (@nitzmahone)

Sam Doran (@samdoran)

**Examples:**

Example 1 (unknown):
```unknown
- name: Unconditionally reboot the machine with all defaults
  ansible.builtin.reboot:

- name: Reboot a slow machine that might have lots of updates to apply
  ansible.builtin.reboot:
    reboot_timeout: 3600

- name: Reboot a machine with shutdown command in unusual place
  ansible.builtin.reboot:
    search_paths:
     - '/lib/molly-guard'

- name: Reboot machine using a custom reboot command
  ansible.builtin.reboot:
    reboot_command: launchctl reboot userspace
    boot_time_command: uptime | cut -d ' ' -f 5

- name: Reboot machine and send a message
  ansible.builtin.reboot:
    msg: "Rebooting machine in 5 seconds"
```

---

## ansible.builtin.expandvars filter – expand environment variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/expandvars_filter.html

**Contents:**
- ansible.builtin.expandvars filter – expand environment variables
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name expandvars. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.expandvars for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Will do a shell-like substitution of environment variables on the provided input.

This describes the input of the filter, the value before | ansible.builtin.expandvars.

A string that contains environment variables.

The string with translated environment variable values.

**Examples:**

Example 1 (unknown):
```unknown
# To get '/home/myuser/stuff.txt' from '$HOME/stuff.txt'
{{ mypath | expandvars }}
```

---

## ansible.builtin.success test – check task success — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/success_test.html

**Contents:**
- ansible.builtin.success test – check task success
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name success. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.success for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task finished successfully, opposite of failed.

This test checks for the existence of a failed key in the input dictionary and that it is False if present

Aliases: succeeded, successful

This describes the input of the test, the value before is ansible.builtin.success or is not ansible.builtin.success.

dictionary / required

registered result from an Ansible task

Returns True if the task was successfully completed, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is success }}
```

---

## Verifying collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_verifying.html

**Contents:**
- Verifying collections
- Verifying collections with ansible-galaxy
- Verifying signed collections

Once installed, you can verify that the content of the installed collection matches the content of the collection on the server. This feature expects that the collection is installed in one of the configured collection paths and that the collection exists on one of the configured galaxy servers.

The output of the ansible-galaxy collection verify command is quiet if it is successful. If a collection has been modified, the altered files are listed under the collection name.

You can use the -vvv flag to display additional information, such as the version and path of the installed collection, the URL of the remote collection used for validation, and successful verification output.

If you have a pre-release or non-latest version of a collection installed you should include the specific version to verify. If the version is omitted, the installed collection is verified against the latest version available on the server.

In addition to the namespace.collection_name:version format, you can provide the collections to verify in a requirements.yml file. Dependencies listed in requirements.yml are not included in the verify process and should be verified separately.

Verifying against tar.gz files is not supported. If your requirements.yml contains paths to tar files or URLs for installation, you can use the --ignore-errors flag to ensure that all collections using the namespace.name format in the file are processed.

If a collection has been signed by a distribution server, the server will provide ASCII armored, detached signatures to verify the authenticity of the MANIFEST.json before using it to verify the collection’s contents. This option is not available on all distribution servers. See Distributing collections for a table listing the servers that support collection signing. See Installing collections with signature verification for how to verify a signed collection when you install it.

To verify a signed installed collection:

Use the --signature option to verify collection name(s) provided on the CLI with an additional signature. This option can be used multiple times to provide multiple signatures.

Optionally, you can verify a collection signature with a requirements.yml file.

When a collection is installed from a distribution server, the signatures provided by the server to verify the collection’s authenticity are saved alongside the installed collections. This data is used to verify the internal consistency of the collection without querying the distribution server again when the --offline option is provided.

**Examples:**

Example 1 (unknown):
```unknown
ansible-galaxy collection verify my_namespace.my_collection
```

Example 2 (unknown):
```unknown
ansible-galaxy collection verify my_namespace.my_collection
Collection my_namespace.my_collection contains modified content in the following files:
my_namespace.my_collection
    plugins/inventory/my_inventory.py
    plugins/modules/my_module.py
```

Example 3 (unknown):
```unknown
ansible-galaxy collection verify my_namespace.my_collection -vvv
...
Verifying 'my_namespace.my_collection:1.0.0'.
Installed collection found at '/path/to/ansible_collections/my_namespace/my_collection/'
Remote collection found at 'https://galaxy.ansible.com/download/my_namespace-my_collection-1.0.0.tar.gz'
Successfully verified that checksums for 'my_namespace.my_collection:1.0.0' match the remote collection
```

Example 4 (unknown):
```unknown
ansible-galaxy collection verify my_namespace.my_collection:1.0.0
```

---

## ansible.builtin.ternary filter – Ternary operation filter — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ternary_filter.html

**Contents:**
- ansible.builtin.ternary filter – Ternary operation filter
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ternary. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ternary for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Return the first value if the input is True, the second if False.

This describes the input of the filter, the value before | ansible.builtin.ternary.

A boolean expression, must evaluate to True or False.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.ternary(positional1, positional2, ...)

Value to return if the input is True.

Value to return if the input is False.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.ternary(key1=value1, key2=value2, ...)

Value to return if the input is None. If not set, None will be treated as False.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.ternary(positional1, positional2, key1=value1, key2=value2)

Vars as values are evaluated even when not returned. This is due to them being evaluated before being passed into the filter.

The value indicated by the input.

**Examples:**

Example 1 (unknown):
```unknown
# set first 10 volumes rw, rest as dp
volume_mode: "{{ (item|int < 11)|ternary('rw', 'dp') }}"

# choose correct vpc subnet id, note that vars as values are evaluated even if not returned
vpc_subnet_id: "{{ (ec2_subnet_type == 'public') | ternary(ec2_vpc_public_subnet_id, ec2_vpc_private_subnet_id) }}"

- name: service-foo, use systemd module unless upstart is present, then use old service module
  service:
    state: restarted
    enabled: yes
    use: "{{ (ansible_service_mgr == 'upstart') | ternary('service', 'systemd') }}"
```

---

## ansible.builtin.iterable test – Check if it’s possible to iterate over an object. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/iterable_test.html

**Contents:**
- ansible.builtin.iterable test – Check if it’s possible to iterate over an object.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name iterable. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.iterable for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if it’s possible to iterate over an object.

This is the Jinja builtin test plugin ‘iterable’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.iterable

---

## ansible.builtin.free strategy – Executes tasks without waiting for all hosts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/free_strategy.html

**Contents:**
- ansible.builtin.free strategy – Executes tasks without waiting for all hosts
- Synopsis
  - Authors
  - Collection links

This strategy plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name free. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.free for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same strategy plugin name.

Task execution is as fast as possible per batch as defined by serial (default all). Ansible will not wait for other hosts to finish the current task before queuing more tasks for other hosts. All hosts are still attempted for the current task, but it prevents blocking new tasks for hosts that have already finished.

With the free strategy, unlike the default linear strategy, a host that is slow or stuck on a specific task won’t hold up the rest of the hosts and tasks.

---

## ansible.builtin.url test – is the string a valid URL — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/url_test.html

**Contents:**
- ansible.builtin.url test – is the string a valid URL
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name url. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.url for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-core 2.14

Validates a string to conform to the URL standard.

This describes the input of the test, the value before is ansible.builtin.url or is not ansible.builtin.url.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.url(key1=value1, key2=value2, ...) and input is not ansible.builtin.url(key1=value1, key2=value2, ...)

list / elements=string

Subset of URI schemas to validate against, otherwise any scheme is considered valid.

Returns false if the string is not a URL, true otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# simple URL
{{ 'http://example.com' is url }}
# looking only for file transfers URIs
{{ 'mailto://[email protected]' is not uri(schemes=['ftp', 'ftps', 'sftp', 'file']) }}
#  but it is according to standard
{{ 'mailto://[email protected]' is not uri }}
# more complex URL
{{ 'ftp://admin:[email protected]/path/to/myfile.yml' is url }}
```

---

## ansible.builtin.script module – Runs a local script on a remote node after transferring it — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/script_module.html

**Contents:**
- ansible.builtin.script module – Runs a local script on a remote node after transferring it
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name script even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.script for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.script module takes the script name followed by a list of space-delimited arguments.

Either a free-form command or cmd parameter is required, see the examples.

The local script at the path will be transferred to the remote node and then executed.

The given script will be processed through the shell environment on the remote node.

This module does not require Python on the remote system, much like the ansible.builtin.raw module.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

Change into this directory on the remote node before running the script.

Path to the local script to run followed by optional arguments.

A filename on the remote node, when it already exists, this step will not be run.

This option controls the auto-decryption of source files using vault.

Name or path of an executable to invoke the script with.

Path to the local script file followed by optional arguments.

A filename on the remote node, when it does not exist, this step will not be run.

while the script itself is arbitrary and cannot be subject to the check mode semantics it adds creates/removes options as a workaround

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

This action is one of the few that requires no Python on the remote as it passes the command directly into the connection string

Target OS/families that can be operated against

Indicates if an action takes a ‘raw’ or ‘free form’ string as an option and has it’s own special parsing of it

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

It is usually preferable to write Ansible modules rather than pushing scripts. Convert your script to an Ansible module for bonus points!

The ansible.builtin.ssh connection plugin will force pseudo-tty allocation via -tt when scripts are executed. Pseudo-ttys do not have a stderr channel and all stderr is sent to stdout. If you depend on separated stdout and stderr result keys, please switch to a set of tasks that comprises ansible.builtin.copy with ansible.builtin.command instead of using ansible.builtin.script.

If the path to the local script contains spaces, it needs to be quoted.

This module is also supported for Windows targets.

If the script returns non-UTF-8 data, it must be encoded to avoid issues. One option is to pipe the output through base64.

Execute shell commands on targets.

The official documentation on the ansible.windows.win_shell module.

**Examples:**

Example 1 (unknown):
```unknown
- name: Run a script with arguments (free form)
  ansible.builtin.script: /some/local/script.sh --some-argument 1234

- name: Run a script with arguments (using 'cmd' parameter)
  ansible.builtin.script:
    cmd: /some/local/script.sh --some-argument 1234

- name: Run a script only if file.txt does not exist on the remote node
  ansible.builtin.script: /some/local/create_file.sh --some-argument 1234
  args:
    creates: /the/created/file.txt

- name: Run a script only if file.txt exists on the remote node
  ansible.builtin.script: /some/local/remove_file.sh --some-argument 1234
  args:
    removes: /the/removed/file.txt

- name: Run a script using an executable in a non-system path
  ansible.builtin.script: /some/local/script
  args:
    executable: /some/remote/executable

- name: Run a script using an executable in a system path
  ansible.builtin.script: /some/local/script.py
  args:
    executable: python3

- name: Run a Powershell script on a Windows host
  script: subdirectories/under/path/with/your/playbook/script.ps1
```

---

## ansible.builtin.falsy test – Pythonic false — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/falsy_test.html

**Contents:**
- ansible.builtin.falsy test – Pythonic false
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name falsy. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.falsy for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-base 2.10

This check is a more Python version of what is ‘false’.

It is the opposite of ‘truthy’.

This describes the input of the test, the value before is ansible.builtin.falsy or is not ansible.builtin.falsy.

An expression that can be expressed in a boolean context.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.falsy(key1=value1, key2=value2, ...) and input is not ansible.builtin.falsy(key1=value1, key2=value2, ...)

Attempts to convert the result to a strict Python boolean vs normally acceptable values (yes/no, on/off, 0/1, etc).

Returns False if the condition is not “Python truthy”, True otherwise.

**Examples:**

Example 1 (unknown):
```unknown
thisisfalse: '{{ "any string" is falsy }}'
thisistrue: '{{ "" is falsy }}'
```

---

## ansible.builtin.wordwrap filter – Wrap a string to the given width. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/wordwrap_filter.html

**Contents:**
- ansible.builtin.wordwrap filter – Wrap a string to the given width.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name wordwrap. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.wordwrap for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Wrap a string to the given width.

This is the Jinja builtin filter plugin ‘wordwrap’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.wordwrap

---

## ansible.builtin.version test – compare version strings — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/version_test.html

**Contents:**
- ansible.builtin.version test – compare version strings
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name version. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.version for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Compare version strings using various versioning schemes

Aliases: version_compare

This describes the input of the test, the value before is ansible.builtin.version or is not ansible.builtin.version.

Left hand version to compare

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.version(key1=value1, key2=value2, ...) and input is not ansible.builtin.version(key1=value1, key2=value2, ...)

Whether to use strict version scheme. Mutually exclusive with version_type

Right hand version to compare

Version scheme to use for comparison. Mutually exclusive with strict. See notes for descriptions on the version types.

loose - This type corresponds to the Python distutils.version.LooseVersion class. All version formats are valid for this type. The rules for comparison are simple and predictable, but may not always give expected results.

strict - This type corresponds to the Python distutils.version.StrictVersion class. A version number consists of two or three dot-separated numeric components, with an optional “pre-release” tag on the end. The pre-release tag consists of a single letter a or b followed by a number. If the numeric components of two version numbers are equal, then one with a pre-release tag will always be deemed earlier (lesser) than one without.

semver/semantic - This type implements the Semantic Version scheme for version comparison.

pep440 - This type implements the Python PEP-440 versioning rules for version comparison. Added in version 2.14.

Returns True or False depending on the outcome of the comparison.

**Examples:**

Example 1 (unknown):
```unknown
- name: version test examples
  assert:
    that:
      - "'1.0' is version_compare('1.0', '==')"  # old name
      - "'1.0' is version('1.0', '==')"
      - "'1.0' is version('2.0', '!=')"
      - "'1.0' is version('2.0', '<')"
      - "'2.0' is version('1.0', '>')"
      - "'1.0' is version('1.0', '<=')"
      - "'1.0' is version('1.0', '>=')"
      - "'1.0' is version_compare('1.0', '==', strict=true)"  # old name
      - "'1.0' is version('1.0', '==', strict=true)"
      - "'1.0' is version('2.0', '!=', strict=true)"
      - "'1.0' is version('2.0', '<', strict=true)"
      - "'2.0' is version('1.0', '>', strict=true)"
      - "'1.0' is version('1.0', '<=', strict=true)"
      - "'1.0' is version('1.0', '>=', strict=true)"
      - "'1.2.3' is version('2.0.0', 'lt', version_type='semver')"
      - "'2.14.0rc1' is version('2.14.0', 'lt', version_type='pep440')"
```

---

## ansible.builtin.to_uuid filter – namespaced UUID generator — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_uuid_filter.html

**Contents:**
- ansible.builtin.to_uuid filter – namespaced UUID generator
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_uuid. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_uuid for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Use to generate namespaced Universal Unique ID.

This describes the input of the filter, the value before | ansible.builtin.to_uuid.

String to use as base of the UUID.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.to_uuid(positional1, positional2, ...)

UUID namespace to use.

Default: "361E6D51-FAEC-444A-9079-341386DA8E2E"

**Examples:**

Example 1 (unknown):
```unknown
# To create a namespaced UUIDv5
uuid: "{{ string | to_uuid(namespace='11111111-2222-3333-4444-555555555555') }}"


# To create a namespaced UUIDv5 using the default Ansible namespace '361E6D51-FAEC-444A-9079-341386DA8E2E'
uuid: "{{ string | to_uuid }}"
```

---

## ansible.builtin.striptags filter – Strip SGML/XML tags and replace adjacent whitespace by one space. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/striptags_filter.html

**Contents:**
- ansible.builtin.striptags filter – Strip SGML/XML tags and replace adjacent whitespace by one space.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name striptags. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.striptags for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Strip SGML/XML tags and replace adjacent whitespace by one space.

This is the Jinja builtin filter plugin ‘striptags’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.striptags

---

## ansible.builtin.same_file test – compares two paths to see if they resolve to the same filesystem object — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/same_file_test.html

**Contents:**
- ansible.builtin.same_file test – compares two paths to see if they resolve to the same filesystem object
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name same_file. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.same_file for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided paths map to the same location on the controller’s filesystem (localhost).

Aliases: is_file, is_same_file

This describes the input of the test, the value before is ansible.builtin.same_file or is not ansible.builtin.same_file.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.same_file(key1=value1, key2=value2, ...) and input is not ansible.builtin.same_file(key1=value1, key2=value2, ...)

Returns True if the paths correspond to the same location on the filesystem on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
amionelevelfromroot: "{{ '/etc/hosts' is same_file('../etc/hosts') }}"
```

---

## ansible.builtin.map filter – Applies a filter on a sequence of objects or looks up an attribute. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/map_filter.html

**Contents:**
- ansible.builtin.map filter – Applies a filter on a sequence of objects or looks up an attribute.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name map. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.map for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Applies a filter on a sequence of objects or looks up an attribute.

This is the Jinja builtin filter plugin ‘map’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.map

---

## ansible.builtin.group module – Add or remove groups — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/group_module.html

**Contents:**
- ansible.builtin.group module – Add or remove groups
- Synopsis
- Requirements
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name group even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.group for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Manage presence of groups on a host.

For Windows targets, use the ansible.windows.win_group module instead.

The below requirements are needed on the host that executes this module.

added in ansible-core 2.15

Whether to delete a group even if it is the primary group of a user.

Only applicable on platforms which implement a --force flag on the group deletion command.

Optional GID to set for the group.

added in ansible-core 2.18

Sets the GID_MAX value for group creation.

Overwrites /etc/login.defs default value.

Currently supported on Linux. Does nothing when used with other platforms.

Requires local is omitted or False.

added in ansible-core 2.18

Sets the GID_MIN value for group creation.

Overwrites /etc/login.defs default value.

Currently supported on Linux. Does nothing when used with other platforms.

Requires local is omitted or False.

Forces the use of “local” command alternatives on platforms that implement it.

This is useful in environments that use centralized authentication when you want to manipulate the local groups. (for example, it uses lgroupadd instead of groupadd).

This requires that these commands exist on the targeted host, otherwise it will be a fatal error.

Name of the group to manage.

This option allows to change the group ID to a non-unique value. Requires gid.

Not supported on macOS or BusyBox distributions.

Whether the group should be present or not on the remote host.

"present" ← (default)

If yes, indicates that the group created is a system group.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Manage user accounts.

The official documentation on the ansible.windows.win_group module.

Common return values are documented here, the following are the fields unique to this module:

Group ID of the group.

Returned: When state is present

Whether the group is present or not.

Whether the group is a system group or not.

Returned: When state is present

Stephen Fromm (@sfromm)

**Examples:**

Example 1 (unknown):
```unknown
- name: Ensure group "somegroup" exists
  ansible.builtin.group:
    name: somegroup
    state: present

- name: Ensure group "docker" exists with correct gid
  ansible.builtin.group:
    name: docker
    state: present
    gid: 1750
```

---

## ansible.builtin.win_splitdrive filter – Split a Windows path by the drive letter — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/win_splitdrive_filter.html

**Contents:**
- ansible.builtin.win_splitdrive filter – Split a Windows path by the drive letter
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name win_splitdrive. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.win_splitdrive for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a list with the first component being the drive letter and the second, the rest of the path.

If the path contains a drive letter, drive will contain everything up to and including the colon.

If the path contains a UNC (Universal Naming Convention) path, drive will contain the host name and share, up to but not including the fourth separator.

This describes the input of the filter, the value before | ansible.builtin.win_splitdrive.

list / elements=string

List in which the first element is the drive letter with colon and the second the rest of the path.

In case of UNC path, first element is the hostname and share and the second the rest of the path.

**Examples:**

Example 1 (unknown):
```unknown
# To get the last name of a file Windows path, like ['C:', '\Users\asdf\foo.txt'] out of 'C:\Users\asdf\foo.txt'
{{ mypath | win_splitdrive }}

# To get path from UNC (Universal Naming Convention) path, like ['//host/computer', '/dir/a'] out of '//host/computer/dir/a'

# just the drive letter, like ['C:'] out of 'C:\Users\asdf\foo.txt'
{{ mypath | win_splitdrive | first }}

# path w/o drive letter, like ['\Users\asdf\foo.txt'] out of 'C:\Users\asdf\foo.txt'
{{ mypath | win_splitdrive | last }}

# just the hostname and share, like ['//host/computer'] out of '//host/computer/dir/a'
{{ mypath | win_splitdrive | first }}

# path w/o hostname and share, like ['/dir/a'] out of '//host/computer/dir/a'
{{ mypath | win_splitdrive | last }}
```

---

## ansible.builtin.flatten filter – flatten lists within a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/flatten_filter.html

**Contents:**
- ansible.builtin.flatten filter – flatten lists within a list
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name flatten. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.flatten for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

For a given list, take any elements that are lists and insert their elements into the parent list directly.

This describes the input of the filter, the value before | ansible.builtin.flatten.

list / elements=any / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.flatten(positional1, positional2, ...)

Number of recursive list depths to flatten.

Skip null/None elements when inserting into the top list.

list / elements=string

**Examples:**

Example 1 (unknown):
```unknown
# [1,2,3,4,5,6]
flat: "{{ [1 , 2, [3, [4, 5]], 6] | flatten }}"

# [1,2,3,[4,5],6]
flatone: "{{ [1, 2, [3, [4, 5]], 6] | flatten(1) }}"
```

---

## ansible.builtin.lower test – Return true if the variable is lowercased. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lower_test.html

**Contents:**
- ansible.builtin.lower test – Return true if the variable is lowercased.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name lower. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lower for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is lowercased.

This is the Jinja builtin test plugin ‘lower’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.lower

---

## ansible.builtin.forceescape filter – Enforce HTML escaping. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/forceescape_filter.html

**Contents:**
- ansible.builtin.forceescape filter – Enforce HTML escaping.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name forceescape. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.forceescape for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Enforce HTML escaping.

This is the Jinja builtin filter plugin ‘forceescape’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.forceescape

---

## ansible.builtin.local connection – execute on controller — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/local_connection.html

**Contents:**
- ansible.builtin.local connection – execute on controller
- Synopsis
- Parameters
- Notes
  - Authors
  - Collection links

This connection plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name local. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.local for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same connection plugin name.

This connection plugin allows ansible to execute tasks on the Ansible ‘controller’ instead of on a remote host.

Aliases: redirected_local

become_strip_preamble

added in ansible-core 2.19

Strip internal become output preceding command execution. Disable for additional diagnostics.

Variable: ansible_local_become_strip_preamble

become_success_timeout

added in ansible-core 2.19

Number of seconds to wait for become to succeed when enabled.

The default will be used if the configured value is less than 1.

Variable: ansible_local_become_success_timeout

Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

This can result in a very significant performance improvement when enabled.

However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable requiretty in the sudoers file for the target hosts, which is why this feature is disabled by default.

Environment variable: ANSIBLE_PIPELINING

Variable: ansible_pipelining

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

The remote user is ignored, the user with which the ansible CLI was executed is used instead.

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
pipelining = false
```

Example 2 (unknown):
```unknown
[connection]
pipelining = false
```

---

## ansible.builtin.gt test – Same as a > b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/gt_test.html

**Contents:**
- ansible.builtin.gt test – Same as a > b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name gt. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.gt for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘gt’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.gt

---

## ansible.builtin.systemd_service module – Manage systemd units — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/systemd_service_module.html

**Contents:**
- ansible.builtin.systemd_service module – Manage systemd units
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name systemd_service even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.systemd_service for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Controls systemd units (services, timers, and so on) on remote hosts.

ansible.builtin.systemd is renamed to ansible.builtin.systemd_service to better reflect the scope of the module. ansible.builtin.systemd is kept as an alias for backward compatibility.

The below requirements are needed on the host that executes this module.

A system managed by systemd.

aliases: daemon-reexec

Run daemon_reexec command before doing any other operations, the systemd manager will serialize the manager state.

aliases: daemon-reload

Run daemon-reload before doing any other operations, to make sure systemd has read any changes.

When set to true, runs daemon-reload even if the module does not start or stop anything.

Whether the unit should start on boot. At least one of state or enabled are required.

If set, requires name.

Whether to override existing symlinks.

Whether the unit should be masked or not. A masked unit is impossible to start.

If set, requires name.

aliases: service, unit

Name of the unit. This parameter takes the name of exactly one unit to work with.

When no extension is given, it is implied to a .service as systemd.

When using in a chroot environment you always need to specify the name of the unit with the extension. For example, crond.service.

Do not synchronously wait for the requested operation to finish. Enqueued job will continue without Ansible blocking on its completion.

Run systemctl within a given service manager scope, either as the default system scope system, the current user’s scope user, or the scope of all users global.

For systemd to work with user, the executing user must have its own instance of dbus started and accessible (systemd requirement).

The user dbus process is normally started during normal login, but not during the run of Ansible tasks. Otherwise you will probably get a ‘Failed to connect to bus: no such file or directory’ error.

The user must have access, normally given via setting the XDG_RUNTIME_DIR variable, see the example below.

started/stopped are idempotent actions that will not run commands unless necessary. restarted will always bounce the unit. reloaded will always reload and if the service is not running at the moment of the reload, it is started.

If set, requires name.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

state, enabled, masked requires name.

Before 2.4 you always required name.

Globs are not supported in name, in other words, postgres*.service.

The service names might vary by specific OS/distribution.

The order of execution when having multiple properties is to first enable/disable, then mask/unmask and then deal with the service state. It has been reported that systemctl can behave differently depending on the order of operations if you do the same manually.

Common return values are documented here, the following are the fields unique to this module:

A dictionary with the key=value pairs returned from systemctl show.

Sample: {"ActiveEnterTimestamp": "Sun 2016-05-15 18:28:49 EDT", "ActiveEnterTimestampMonotonic": "8135942", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "auditd.service systemd-user-sessions.service time-sync.target systemd-journald.socket basic.target system.slice", "AllowIsolate": "no", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "1000", "CPUAccounting": "no", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "1024", "CanIsolate": "no", "CanReload": "yes", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2016-05-15 18:28:49 EDT", "ConditionTimestampMonotonic": "7902742", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/crond.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Command Scheduler", "DevicePolicy": "auto", "EnvironmentFile": "/etc/sysconfig/crond (ignore_errors=no)", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "595", "ExecMainStartTimestamp": "Sun 2016-05-15 18:28:49 EDT", "ExecMainStartTimestampMonotonic": "8134990", "ExecMainStatus": "0", "ExecReload": "{ path=/bin/kill ; argv[]=/bin/kill -HUP $MAINPID ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStart": "{ path=/usr/sbin/crond ; argv[]=/usr/sbin/crond -n $CRONDARGS ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "FragmentPath": "/usr/lib/systemd/system/crond.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "crond.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestampMonotonic": "0", "InactiveExitTimestamp": "Sun 2016-05-15 18:28:49 EDT", "InactiveExitTimestampMonotonic": "8135942", "JobTimeoutUSec": "0", "KillMode": "process", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "3902", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "3902", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "595", "MemoryAccounting": "no", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "crond.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureIsolate": "no", "PermissionsStartOnly": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "simple", "UMask": "0022", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "Wants": "system.slice", "WatchdogTimestampMonotonic": "0", "WatchdogUSec": "0"}

**Examples:**

Example 1 (unknown):
```unknown
- name: Make sure a service unit is running
  ansible.builtin.systemd_service:
    state: started
    name: httpd

- name: Stop service cron on debian, if running
  ansible.builtin.systemd_service:
    name: cron
    state: stopped

- name: Restart service cron on centos, in all cases, also issue daemon-reload to pick up config changes
  ansible.builtin.systemd_service:
    state: restarted
    daemon_reload: true
    name: crond

- name: Reload service httpd, in all cases
  ansible.builtin.systemd_service:
    name: httpd.service
    state: reloaded

- name: Enable service httpd and ensure it is not masked
  ansible.builtin.systemd_service:
    name: httpd
    enabled: true
    masked: no

- name: Enable a timer unit for dnf-automatic
  ansible.builtin.systemd_service:
    name: dnf-automatic.timer
    state: started
    enabled: true

- name: Just force systemd to reread configs (2.4 and above)
  ansible.builtin.systemd_service:
    daemon_reload: true

- name: Just force systemd to re-execute itself (2.8 and above)
  ansible.builtin.systemd_service:
    daemon_reexec: true

- name: Run a user service when XDG_RUNTIME_DIR is not set on remote login
  ansible.builtin.systemd_service:
    name: myservice
    state: started
    scope: user
  environment:
    XDG_RUNTIME_DIR: "/run/user/{{ myuid }}"
```

---

## ansible.builtin.mapping test – Return true if the object is a mapping. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/mapping_test.html

**Contents:**
- ansible.builtin.mapping test – Return true if the object is a mapping.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name mapping. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.mapping for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is a mapping.

This is the Jinja builtin test plugin ‘mapping’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.mapping

---

## ansible.builtin.escape filter – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/escape_filter.html

**Contents:**
- ansible.builtin.escape filter – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name escape. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.escape for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.

This is the Jinja builtin filter plugin ‘escape’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.escape

---

## ansible.builtin.indent filter – Return a copy of the string with each line indented by 4 spaces. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/indent_filter.html

**Contents:**
- ansible.builtin.indent filter – Return a copy of the string with each line indented by 4 spaces.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name indent. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.indent for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a copy of the string with each line indented by 4 spaces.

This is the Jinja builtin filter plugin ‘indent’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.indent

---

## ansible.builtin.link test – does the path reference existing symbolic link — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/link_test.html

**Contents:**
- ansible.builtin.link test – does the path reference existing symbolic link
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name link. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.link for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to an existing symlink on the controller’s filesystem (localhost).

Aliases: is_link, islink

This describes the input of the test, the value before is ansible.builtin.link or is not ansible.builtin.link.

Returns True if the path corresponds to an existing symlink on the filesystem on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
ismyhostsalink: "{{ '/etc/hosts' is link}}"
list_of_symlinks: "{{ list_of_paths | select('link') }}"
```

---

## ansible.builtin.debug strategy – Executes tasks in interactive debug session. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/debug_strategy.html

**Contents:**
- ansible.builtin.debug strategy – Executes tasks in interactive debug session.
- Synopsis
  - Authors
  - Collection links

This strategy plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name debug. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.debug for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same strategy plugin name.

Task execution is ‘linear’ but controlled by an interactive debug session.

---

## ansible.builtin.changed test – did the task require changes — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/changed_test.html

**Contents:**
- ansible.builtin.changed test – did the task require changes
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name changed. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.changed for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task required changes to complete

This test checks for the existence of a changed key in the input dictionary and that it is True if present

This describes the input of the test, the value before is ansible.builtin.changed or is not ansible.builtin.changed.

dictionary / required

registered result from an Ansible task

Returns True if the task was required changes, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is changed }}
```

---

## ansible.builtin.fileglob filter – explode a path glob to matching files — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/fileglob_filter.html

**Contents:**
- ansible.builtin.fileglob filter – explode a path glob to matching files
- Synopsis
- Input
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name fileglob. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.fileglob for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a list of files that matches the supplied path glob pattern.

Filters run on the controller, so the files are matched from the controller’s file system.

This describes the input of the filter, the value before | ansible.builtin.fileglob.

list / elements=string

List of files matched.

**Examples:**

Example 1 (unknown):
```unknown
# found = ['/etc/hosts', '/etc/hasts']
found: "{{ '/etc/h?sts' | fileglob }}"
```

---

## ansible.builtin.even test – Return true if the variable is even. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/even_test.html

**Contents:**
- ansible.builtin.even test – Return true if the variable is even.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name even. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.even for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is even.

This is the Jinja builtin test plugin ‘even’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.even

---

## Testing Ansible and Collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_running_locally.html

**Contents:**
- Testing Ansible and Collections
- Setup
  - Testing an Ansible Collection
  - Testing ansible-core
- Commands
- Environments
  - Containers
    - Choosing a container
      - Custom containers
    - Docker and SELinux

This document describes how to run tests using ansible-test.

Testing an Ansible Collection

Docker Desktop with WSL2

Configuration requirements

Linux cgroup configuration

Remote virtual machines

Python virtual environments

Composite environment arguments

Additional Requirements

Environment variables

Before running ansible-test, set up your environment for Testing an Ansible Collection or Testing ansible-core, depending on which scenario applies to you.

If you use git for version control, make sure the files you are working with are not ignored by git. If they are, ansible-test will ignore them as well.

If you are testing an Ansible Collection, you need a copy of the collection, preferably a Git clone. For example, to work with the community.windows collection, follow these steps:

Clone the collection you want to test into a valid collection root:

The path must end with /ansible_collections/{collection_namespace}/{collection_name} where {collection_namespace} is the namespace of the collection and {collection_name} is the collection name.

Clone any collections on which the collection depends:

If your collection has any dependencies on other collections, they must be in the same collection root, since ansible-test will not use your configured collection roots (or other Ansible configuration).

See the collection’s galaxy.yml for a list of possible dependencies.

Switch to the directory where the collection to test resides:

If you are testing ansible-core itself, you need a copy of the ansible-core source code, preferably a Git clone. Having an installed copy of ansible-core is not sufficient or required. For example, to work with the ansible-core source cloned from GitHub, follow these steps:

Clone the ansible-core repository:

Switch to the directory where the ansible-core source resides:

Add ansible-core programs to your PATH:

You can skip this step if you only need to run ansible-test, and not other ansible-core programs. In that case, simply run bin/ansible-test from the root of the ansible-core source.

If you have an installed version of ansible-core and are trying to run ansible-test from your PATH, make sure the program found by your shell is the one from the ansible-core source:

The most commonly used test commands are:

ansible-test sanity - Run sanity tests (mostly linters and static analysis).

ansible-test integration - Run integration tests.

ansible-test units - Run unit tests.

Run ansible-test --help to see a complete list of available commands.

For detailed help on a specific command, add the --help option after the command.

Most ansible-test commands support running in one or more isolated test environments to simplify testing.

Containers are recommended for running sanity, unit and integration tests, since they provide consistent environments. Unit tests will be run with network isolation, which avoids unintentional dependencies on network resources.

The --docker option runs tests in a container using either Docker or Podman.

If both Docker and Podman are installed, Docker will be used. To override this, set the environment variable ANSIBLE_TEST_PREFER_PODMAN to any non-empty value.

Without an additional argument, the --docker option uses the default container. To use another container, specify it immediately after the --docker option.

The default container is recommended for all sanity and unit tests.

To see the list of supported containers, use the --help option with the ansible-test command you want to use.

The list of available containers is dependent on the ansible-test command you are using.

You can also specify your own container. When doing so, you will need to indicate the Python version in the container with the --python option.

When building custom containers, keep in mind the following requirements:

The USER should be root.

Use an init process, such as systemd.

Include sshd and accept connections on the default port of 22.

Include a POSIX compatible sh shell which can be found on PATH.

Include a sleep utility which runs as a subprocess.

Include a supported version of Python.

Avoid using the VOLUME statement.

Using Docker on a host with SELinux may require setting the system in permissive mode. Consider using Podman instead.

These instructions explain how to use ansible-test with WSL2 and Docker Desktop without systemd support.

If your WSL2 environment includes systemd support, these steps are not required.

Open Docker Desktop and go to the Settings screen.

On the the General tab:

Uncheck the Start Docker Desktop when you log in checkbox.

Check the Use the WSL 2 based engine checkbox.

On the Resources tab under the WSL Integration section:

Enable distros you want to use under the Enable integration with additional distros section.

Click Apply and restart if changes were made.

If all WSL instances have been stopped, these changes will need to be re-applied.

Verify Docker Desktop is properly configured (see Configuration requirements).

Quit Docker Desktop if it is running:

Right click the Docker Desktop taskbar icon.

Click the Quit Docker Desktop option.

Stop any running WSL instances with the command:

Verify all WSL instances have stopped with the command:

Start a WSL instance and perform the following steps as root:

Verify the systemd subsystem is not registered:

Check for the systemd cgroup hierarchy with the following command:

If any matches are found, re-check the Configuration requirements and follow the Setup instructions again.

Mount the systemd cgroup hierarchy with the following commands:

Start Docker Desktop.

You should now be able to use ansible-test with the --docker option.

These changes will need to be re-applied each time the container host is booted.

For certain container hosts and container combinations, additional setup on the container host may be required. In these situations ansible-test will report an error and provide additional instructions to run as root:

If you are using rootless Podman, an additional command must be run, also as root. Make sure to substitute your user and group for {user} and {group} respectively:

When using Podman, you may need to stop existing Podman processes after following the Linux cgroup configuration instructions. Otherwise Podman may be unable to see the new mount point.

You can check to see if Podman is running by looking for podman and catatonit processes.

Remote virtual machines are recommended for running integration tests not suitable for execution in containers.

The --remote option runs tests in a cloud hosted ephemeral virtual machine.

An API key is required to use this feature, unless running under an approved Azure Pipelines organization.

To see the list of supported systems, use the --help option with the ansible-test command you want to use.

The list of available systems is dependent on the ansible-test command you are using.

Python virtual environments provide a simple way to achieve isolation from the system and user Python environments. They are recommended for unit and integration tests when the --docker and --remote options cannot be used.

The --venv option runs tests in a virtual environment managed by ansible-test. Requirements are automatically installed before tests are run.

The environment arguments covered in this document are sufficient for most use cases. However, some scenarios may require the additional flexibility offered by composite environment arguments.

The --controller and --target options are alternatives to the --docker, --remote and --venv options.

When using the shell command, the --target option is replaced by three platform specific options.

Add the --help option to your ansible-test command to learn more about the composite environment arguments.

Some ansible-test commands have additional requirements. You can use the --requirements option to automatically install them.

When using a test environment managed by ansible-test the --requirements option is usually unnecessary.

When using environment variables to manipulate tests there some limitations to keep in mind. Environment variables are:

Not propagated from the host to the test environment when using the --docker or --remote options.

Not exposed to the test environment unless enabled in test/lib/ansible_test/_internal/util.py in the common_environment function.

Example: ANSIBLE_KEEP_REMOTE_FILES=1 can be set when running ansible-test integration --venv. However, using the --docker option would require running ansible-test shell to gain access to the Docker environment. Once at the shell prompt, the environment variable could be set and the tests executed. This is useful for debugging tests inside a container by following the Debugging modules instructions.

Use the ansible-test shell command to get an interactive shell in the same environment used to run tests. Examples:

ansible-test shell --docker - Open a shell in the default docker container.

ansible-test shell --venv --python 3.10 - Open a shell in a Python 3.10 virtual environment.

Code coverage reports make it easy to identify untested code for which more tests should be written. Online reports are available but only cover the devel branch (see Testing Ansible). For new code local reports are needed.

Add the --coverage option to any test command to collect code coverage data. If you aren’t using the --venv or --docker options which create an isolated python environment then you may have to use the --requirements option to ensure that the correct version of the coverage module is installed:

Reports can be generated in several different formats:

ansible-test coverage report - Console report.

ansible-test coverage html - HTML report.

ansible-test coverage xml - XML report.

To clear data between test runs, use the ansible-test coverage erase command.

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/ansible-collections/community.windows ~/dev/ansible_collections/community/windows
```

Example 2 (unknown):
```unknown
git clone https://github.com/ansible-collections/ansible.windows ~/dev/ansible_collections/ansible/windows
```

Example 3 (unknown):
```unknown
cd ~/dev/ansible_collections/community/windows
```

Example 4 (unknown):
```unknown
git clone https://github.com/ansible/ansible ~/dev/ansible
```

---

## ansible.builtin.shuffle filter – randomize a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/shuffle_filter.html

**Contents:**
- ansible.builtin.shuffle filter – randomize a list
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name shuffle. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.shuffle for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Take the elements of the input list and return in a random order.

This describes the input of the filter, the value before | ansible.builtin.shuffle.

list / elements=any / required

A number or list to randomize.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.shuffle(key1=value1, key2=value2, ...)

If specified use a pseudo random selection instead (repeatable).

Random number or list element.

**Examples:**

Example 1 (unknown):
```unknown
randomized_list: "{{ ['a','b','c'] | shuffle}}"
per_host_repeatable: "{{ ['a','b','c'] | shuffle(seed=inventory_hostname) }}"
```

---

## ansible.builtin.blockinfile module – Insert/update/remove a text block surrounded by marker lines — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/blockinfile_module.html

**Contents:**
- ansible.builtin.blockinfile module – Insert/update/remove a text block surrounded by marker lines
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name blockinfile even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.blockinfile for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module will insert/update/remove a block of multi-line text surrounded by customizable marker lines.

added in ansible-core 2.16

Append a blank line to the inserted block, if this does not appear at the end of the file.

Note that this attribute is not considered when state is set to absent

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

The text to insert inside the marker lines.

If it is missing or an empty string, the block will be removed as if state were specified to absent.

Create a new file if it does not exist.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

If specified and no begin/ending marker lines are found, the block will be inserted after the last match of specified regular expression.

A special value is available; EOF for inserting the block at the end of the file.

If specified regular expression has no matches or no value is passed, EOF will be used instead.

The presence of the multiline flag (?m) in the regular expression controls whether the match is done line by line or with multiple lines. This behaviour was added in ansible-core 2.14.

If specified and no begin/ending marker lines are found, the block will be inserted before the last match of specified regular expression.

A special value is available; BOF for inserting the block at the beginning of the file.

If specified regular expression has no matches, the block will be inserted at the end of the file.

The presence of the multiline flag (?m) in the regular expression controls whether the match is done line by line or with multiple lines. This behaviour was added in ansible-core 2.14.

The marker line template.

{mark} will be replaced with the values in marker_begin (default=BEGIN) and marker_end (default=END).

Using a custom marker without the {mark} variable may result in the block being repeatedly inserted on subsequent playbook runs.

Multi-line markers are not supported and will result in the block being repeatedly inserted on subsequent playbook runs.

A newline is automatically appended by the module to marker_begin and marker_end.

Default: "# {mark} ANSIBLE MANAGED BLOCK"

This will be inserted at {mark} in the opening ansible block marker.

This will be inserted at {mark} in the closing ansible block marker.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

aliases: dest, destfile, name

Before Ansible 2.3 this option was only usable as dest, destfile and name.

added in ansible-core 2.16

Prepend a blank line to the inserted block, if this does not appear at the beginning of the file.

Note that this attribute is not considered when state is set to absent

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Whether the block should be there or not.

"present" ← (default)

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying the updated file into the final destination.

A temporary file path is used to validate, passed in through %s which must be present as in the examples below.

Also, the command is passed securely so shell features such as expansion and pipes will not work.

For an example on how to handle more complex validation than what this option provides, see handling complex validation.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

When using with_* loops be aware that if you do not set a unique mark the block will be overwritten on each iteration.

As of Ansible 2.3, the dest option has been changed to path as default, but dest still works as well.

Option follow has been removed in Ansible 2.5, because this module modifies the contents of the file so follow=no does not make sense.

When more than one block should be handled in one file you must change the marker per task.

Yaegashi Takeshi (@yaegashi)

**Examples:**

Example 1 (unknown):
```unknown
# Before Ansible 2.3, option 'dest' or 'name' was used instead of 'path'
- name: Insert/Update "Match User" configuration block in /etc/ssh/sshd_config prepending and appending a new line
  ansible.builtin.blockinfile:
    path: /etc/ssh/sshd_config
    append_newline: true
    prepend_newline: true
    block: |
      Match User ansible-agent
      PasswordAuthentication no

- name: Insert/Update eth0 configuration stanza in /etc/network/interfaces
        (it might be better to copy files into /etc/network/interfaces.d/)
  ansible.builtin.blockinfile:
    path: /etc/network/interfaces
    block: |
      iface eth0 inet static
          address 192.0.2.23
          netmask 255.255.255.0

- name: Insert/Update configuration using a local file and validate it
  ansible.builtin.blockinfile:
    block: "{{ lookup('ansible.builtin.file', './local/sshd_config') }}"
    path: /etc/ssh/sshd_config
    backup: yes
    validate: /usr/sbin/sshd -T -f %s

- name: Insert/Update HTML surrounded by custom markers after <body> line
  ansible.builtin.blockinfile:
    path: /var/www/html/index.html
    marker: "<!-- {mark} ANSIBLE MANAGED BLOCK -->"
    insertafter: "<body>"
    block: |
      <h1>Welcome to {{ ansible_hostname }}</h1>
      <p>Last updated on {{ ansible_date_time.iso8601 }}</p>

- name: Remove HTML as well as surrounding markers
  ansible.builtin.blockinfile:
    path: /var/www/html/index.html
    marker: "<!-- {mark} ANSIBLE MANAGED BLOCK -->"
    block: ""

- name: Add mappings to /etc/hosts
  ansible.builtin.blockinfile:
    path: /etc/hosts
    block: |
      {{ item.ip }} {{ item.name }}
    marker: "# {mark} ANSIBLE MANAGED BLOCK {{ item.name }}"
  loop:
    - { name: host1, ip: 10.10.1.10 }
    - { name: host2, ip: 10.10.1.11 }
    - { name: host3, ip: 10.10.1.12 }

- name: Search with a multiline search flags regex and if found insert after
  blockinfile:
    path: listener.ora
    block: "{{ listener_line | indent(width=8, first=True) }}"
    insertafter: '(?m)SID_LIST_LISTENER_DG =\n.*\(SID_LIST ='
    marker: "    <!-- {mark} ANSIBLE MANAGED BLOCK -->"
```

---

## ansible.builtin.greaterthan test – Same as a > b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/greaterthan_test.html

**Contents:**
- ansible.builtin.greaterthan test – Same as a > b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name greaterthan. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.greaterthan for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘greaterthan’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.greaterthan

---

## ansible.builtin.replace module – Replace all instances of a particular string in a file using a back-referenced regular expression — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/replace_module.html

**Contents:**
- ansible.builtin.replace module – Replace all instances of a particular string in a file using a back-referenced regular expression
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name replace even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.replace for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module will replace all instances of a pattern within a file.

It is up to the user to maintain idempotence by ensuring that the same pattern would never match any replacements made.

If specified, only content after this match will be replaced/removed.

Can be used in combination with before.

Uses Python regular expressions; see https://docs.python.org/3/library/re.html.

Uses DOTALL, which means the . special character can match newlines.

Does not use MULTILINE, so ^ and $ will only match the beginning and end of the file.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

If specified, only content before this match will be replaced/removed.

Can be used in combination with after.

Uses Python regular expressions; see https://docs.python.org/3/library/re.html.

Uses DOTALL, which means the . special character can match newlines.

Does not use MULTILINE, so ^ and $ will only match the beginning and end of the file.

The character encoding for reading and writing the file.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

aliases: dest, destfile, name

Before Ansible 2.3 this option was only usable as dest, destfile and name.

The regular expression to look for in the contents of the file.

Uses Python regular expressions; see https://docs.python.org/3/library/re.html.

Uses MULTILINE mode, which means ^ and $ match the beginning and end of the file, as well as the beginning and end respectively of each line of the file.

Does not use DOTALL, which means the . special character matches any character except newlines. A common mistake is to assume that a negated character set like [^#] will also not match newlines.

In order to exclude newlines, they must be added to the set like [^#\n].

Note that, as of Ansible 2.0, short form tasks should have any escape sequences backslash-escaped in order to prevent them being parsed as string literal escapes. See the examples.

The string to replace regexp matches.

May contain backreferences that will get expanded with the regexp capture groups if the regexp matches.

If not set, matches are removed entirely.

Backreferences can be used ambiguously like \1, or explicitly like \g<1>.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying the updated file into the final destination.

A temporary file path is used to validate, passed in through %s which must be present as in the examples below.

Also, the command is passed securely so shell features such as expansion and pipes will not work.

For an example on how to handle more complex validation than what this option provides, see handling complex validation.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

As of Ansible 2.3, the dest option has been changed to path as default, but dest still works as well.

As of Ansible 2.7.10, the combined use of before and after works properly. If you were relying on the previous incorrect behavior, you may be need to adjust your tasks. See https://github.com/ansible/ansible/issues/31354 for details.

Option follow has been removed in Ansible 2.5, because this module modifies the contents of the file so follow=no does not make sense.

Evan Kaufman (@EvanK)

**Examples:**

Example 1 (unknown):
```unknown
- name: Replace old hostname with new hostname (requires Ansible >= 2.4)
  ansible.builtin.replace:
    path: /etc/hosts
    regexp: '(\s+)old\.host\.name(\s+.*)?$'
    replace: '\1new.host.name\2'

- name: Replace after the expression till the end of the file (requires Ansible >= 2.4)
  ansible.builtin.replace:
    path: /etc/apache2/sites-available/default.conf
    after: 'NameVirtualHost [*]'
    regexp: '^(.+)$'
    replace: '# \1'

- name: Replace before the expression from the beginning of the file (requires Ansible >= 2.4)
  ansible.builtin.replace:
    path: /etc/apache2/sites-available/default.conf
    before: '# live site config'
    regexp: '^(.+)$'
    replace: '# \1'

# Prior to Ansible 2.7.10, using before and after in combination did the opposite of what was intended.
# see https://github.com/ansible/ansible/issues/31354 for details.
# Note (?m) which turns on MULTILINE mode so ^ matches any line's beginning
- name: Replace between the expressions (requires Ansible >= 2.4)
  ansible.builtin.replace:
    path: /etc/hosts
    after: '(?m)^<VirtualHost [*]>'
    before: '</VirtualHost>'
    regexp: '^(.+)$'
    replace: '# \1'

- name: Supports common file attributes
  ansible.builtin.replace:
    path: /home/jdoe/.ssh/known_hosts
    regexp: '^old\.host\.name[^\n]*\n'
    owner: jdoe
    group: jdoe
    mode: '0644'

- name: Supports a validate command
  ansible.builtin.replace:
    path: /etc/apache/ports
    regexp: '^(NameVirtualHost|Listen)\s+80\s*$'
    replace: '\1 127.0.0.1:8080'
    validate: '/usr/sbin/apache2ctl -f %s -t'

- name: Short form task (in ansible 2+) necessitates backslash-escaped sequences
  ansible.builtin.replace: path=/etc/hosts regexp='\\b(localhost)(\\d*)\\b' replace='\\1\\2.localdomain\\2 \\1\\2'

- name: Long form task does not
  ansible.builtin.replace:
    path: /etc/hosts
    regexp: '\b(localhost)(\d*)\b'
    replace: '\1\2.localdomain\2 \1\2'

- name: Explicitly specifying positional matched groups in replacement
  ansible.builtin.replace:
    path: /etc/ssh/sshd_config
    regexp: '^(ListenAddress[ ]+)[^\n]+$'
    replace: '\g<1>0.0.0.0'

- name: Explicitly specifying named matched groups
  ansible.builtin.replace:
    path: /etc/ssh/sshd_config
    regexp: '^(?P<dctv>ListenAddress[ ]+)(?P<host>[^\n]+)$'
    replace: '#\g<dctv>\g<host>\n\g<dctv>0.0.0.0'
```

---

## ansible.builtin.defined test – Return true if the variable is defined. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/defined_test.html

**Contents:**
- ansible.builtin.defined test – Return true if the variable is defined.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name defined. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.defined for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is defined.

This is the Jinja builtin test plugin ‘defined’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.defined

---

## ansible.builtin.first filter – Return the first item of a sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/first_filter.html

**Contents:**
- ansible.builtin.first filter – Return the first item of a sequence.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name first. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.first for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the first item of a sequence.

This is the Jinja builtin filter plugin ‘first’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.first

---

## ansible.builtin.format filter – Apply the given values to a `printf-style`_ format string, like ``string % values``. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/format_filter.html

**Contents:**
- ansible.builtin.format filter – Apply the given values to a `printf-style`_ format string, like ``string % values``.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name format. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.format for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Apply the given values to a `printf-style`_ format string, like ``string % values``.

This is the Jinja builtin filter plugin ‘format’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.format

---

## ansible.builtin.getent module – A wrapper to the unix getent utility — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/getent_module.html

**Contents:**
- ansible.builtin.getent module – A wrapper to the unix getent utility
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
- Returned Facts
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name getent even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.getent for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Runs getent against one of its various databases and returns information into the host’s facts, in a getent_<database> prefixed variable.

The name of a getent database supported by the target system (passwd, group, hosts, etc).

If a supplied key is missing this will make the task fail if true.

Key from which to return values from the specified database, otherwise the full contents are returned.

Override all databases with the specified service

The underlying system must support the service flag which is not always available.

Character used to split the database values into lists/arrays such as : or \t, otherwise it will try to pick one depending on the database.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

Target OS/families that can be operated against

Not all databases support enumeration, check system documentation for details.

Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.

list / elements=string

A list of results or a single result as a list of the fields the db provides

The list elements depend on the database queried, see getent man page for the structure

Starting at 2.11 it now returns multiple duplicate entries, previously it only returned the last one

**Examples:**

Example 1 (unknown):
```unknown
- name: Get root user info
  ansible.builtin.getent:
    database: passwd
    key: root
- ansible.builtin.debug:
    var: ansible_facts.getent_passwd

- name: Get all groups
  ansible.builtin.getent:
    database: group
    split: ':'
- ansible.builtin.debug:
    var: ansible_facts.getent_group

- name: Get all hosts, split by tab
  ansible.builtin.getent:
    database: hosts
- ansible.builtin.debug:
    var: ansible_facts.getent_hosts

- name: Get http service info, no error if missing
  ansible.builtin.getent:
    database: services
    key: http
    fail_key: False
- ansible.builtin.debug:
    var: ansible_facts.getent_services

- name: Get user password hash (requires sudo/root)
  ansible.builtin.getent:
    database: shadow
    key: www-data
    split: ':'
- ansible.builtin.debug:
    var: ansible_facts.getent_shadow
```

---

## ansible.builtin.union filter – union of lists — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/union_filter.html

**Contents:**
- ansible.builtin.union filter – union of lists
- Synopsis
- Input
- Keyword parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name union. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.union for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Provide a unique list of all the elements of two lists.

Items in the resulting list are returned in arbitrary order.

This describes the input of the filter, the value before | ansible.builtin.union.

list / elements=string / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.union(key1=value1, key2=value2, ...)

list / elements=string / required

the difference of one list from another.

intersection of lists.

different items from two lists.

set of unique items of a list.

list / elements=string

A unique list of all the elements from both lists.

**Examples:**

Example 1 (javascript):
```javascript
# return the unique elements of list1 added to list2
# list1: [1, 2, 5, 1, 3, 4, 10]
# list2: [1, 2, 3, 4, 5, 11, 99]
{{ list1 | union(list2) }}
# => [1, 2, 5, 3, 4, 10, 11, 99]
```

---

## ansible.builtin.float filter – Convert the value into a floating point number. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/float_filter.html

**Contents:**
- ansible.builtin.float filter – Convert the value into a floating point number.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name float. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.float for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert the value into a floating point number.

This is the Jinja builtin filter plugin ‘float’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.float

---

## ansible.builtin.slice filter – Slice an iterator and return a list of lists containing those items. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/slice_filter.html

**Contents:**
- ansible.builtin.slice filter – Slice an iterator and return a list of lists containing those items.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name slice. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.slice for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Slice an iterator and return a list of lists containing those items.

This is the Jinja builtin filter plugin ‘slice’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.slice

---

## ansible.builtin.host_pinned strategy – Executes tasks on each host without interruption — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/host_pinned_strategy.html

**Contents:**
- ansible.builtin.host_pinned strategy – Executes tasks on each host without interruption
- Synopsis
  - Authors
  - Collection links

This strategy plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name host_pinned. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.host_pinned for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same strategy plugin name.

Task execution is as fast as possible per host in batch as defined by serial (default all). Ansible will not start a play for a host unless the play can be finished without interruption by tasks for another host, i.e. the number of hosts with an active play does not exceed the number of forks. Ansible will not wait for other hosts to finish the current task before queuing the next task for a host that has finished. Once a host is done with the play, it opens it’s slot to a new host that was waiting to start. Other than that, it behaves just like the “free” strategy.

---

## ansible.builtin.linear strategy – Executes tasks in a linear fashion — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/linear_strategy.html

**Contents:**
- ansible.builtin.linear strategy – Executes tasks in a linear fashion
- Synopsis
- Notes
  - Authors
  - Collection links

This strategy plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name linear. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.linear for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same strategy plugin name.

Task execution is in lockstep per host batch as defined by serial (default all). Up to the fork limit of hosts will execute each task at the same time and then the next series of hosts until the batch is done, before going on to the next task.

This was the default Ansible behaviour before ‘strategy plugins’ were introduced in 2.0.

---

## Migrating Ansible content to a different collection — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_migrating.html

**Contents:**
- Migrating Ansible content to a different collection
- Migrating content
  - Adding the content to the new collection
  - Removing the content from the old collection
  - Updating BOTMETA.yml

You might decide to move content from one collection to another; for example, to extract a set of related modules out of community.general or community.network to create a more focused collection. When you migrate content between collections, you must take certain steps to ensure users can follow the transition.

Adding the content to the new collection

Removing the content from the old collection

If the collection from which you are going to migrate content is included in the Ansible community package, ensure the target collection satisfies the Ansible community package collections requirements. After you satisfy the requirements, you can migrate the content as follows:

Copy content from the source (old) collection to the target (new) collection.

Change M(), examples, seealso, extended_documentation_fragments to use actual FQCNs in moved content, old collection, and in other collections that have references to the content.

Move all related issues, pull requests, and wiki pages.

Look through the docs/docsite directory of the ansible-documentation GitHub repository (for example, using the grep command-line utility) to check if there are examples using the moved modules and plugins so that you can update those FQCNs.

Deprecate the module/plugin with removal_version scheduled for the next major version in meta/runtime.yml of the old collection. The deprecation must be released after the copied content has been included in a release of the new collection.

When the next major release of the old collection is prepared:

remove the module/plugin from the old collection

remove related unit and integration tests

remove specific module utils (if they are NOT used by other modules/plugins or module_utils)

remove specific documentation fragments if there are any in the old collection

add a changelog fragment containing entries for removed_features and breaking_changes; you can see an example of a changelog fragment in this pull request

change meta/runtime.yml in the old collection:

add redirect to the corresponding module/plugin’s entry

in particular, add redirect for the removed module utils and documentation fragments if applicable

remove removal_version from there

remove related entries from tests/sanity/ignore.txt files if exist

remove changelog fragments for removed content that are not yet part of the changelog (in other words, do not modify changelogs/changelog.yaml and do not delete files mentioned in it)

remove requirements that are no longer required in tests/unit/requirements.txt, tests/requirements.yml and galaxy.yml

To implement these changes, you need to create at least three PRs:

Create a PR against the new collection to copy the content.

Deprecate the module/plugin in the old collection.

Later create a PR against the old collection to remove the content according to the schedule.

Create a PR in the new collection to:

Copy ALL the related files from the old collection.

If it is an action plugin, include the corresponding module with documentation.

If it is a module, check if it has a corresponding action plugin that should move with it.

Check meta/ for relevant updates to runtime.yml if it exists.

Carefully check the moved tests/integration and tests/units and update for FQCN.

Review tests/sanity/ignore-*.txt entries in the old collection.

Update meta/runtime.yml in the old collection.

Create a PR against the source collection repository to remove the modules, module_utils, plugins, and docs_fragments related to this migration:

If you are removing an action plugin, remove the corresponding module that contains the documentation.

If you are removing a module, remove any corresponding action plugin that should stay with it.

Remove any entries about removed plugins from meta/runtime.yml. Ensure they are added into the new repo.

Remove sanity ignore lines from tests/sanity/ignore\*.txt

Remove associated integration tests from tests/integrations/targets/ and unit tests from tests/units/plugins/.

if you are removing from content from community.general or community.network, remove entries from .github/BOTMETA.yml.

Carefully review meta/runtime.yml for any entries you may need to remove or update, in particular deprecated entries.

Update meta/runtime.yml to contain redirects for EVERY PLUGIN, pointing to the new collection name.

Maintainers for the old collection have to make sure that the PR is merged in a way that it does not break user experience and semantic versioning:

A new version containing the merged PR must not be released before the collection the content has been moved to has been released again, with that content contained in it. Otherwise the redirects cannot work and users relying on that content will experience breakage.

Once 1.0.0 of the collection from which the content has been removed has been released, such PRs can only be merged for a new major version (in other words, 2.0.0, 3.0.0, and so on).

The BOTMETA.yml, for example in community.general collection repository, is the source of truth for:

If the old and/or new collection has ansibullbot, its BOTMETA.yml must be updated correspondingly.

Ansibulbot will know how to redirect existing issues and PRs to the new repo. The build process for docs.ansible.com will know where to find the module docs.

The migrated_to: key must be added explicitly for every file. You cannot add migrated_to at the directory level. This is to allow module and plugin webdocs to be redirected to the new collection docs.

migrated_to: MUST be added for every:

contrib/inventory script

You do NOT need to add migrated_to for:

ReStructured Text docs (anything under docs/docsite/rst/)

Files that never existed in ansible/ansible:devel

Learn how to install and use collections.

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
$modules/monitoring/grafana/grafana_plugin.py:
    migrated_to: community.grafana
$modules/monitoring/grafana/grafana_dashboard.py:
    migrated_to: community.grafana
$modules/monitoring/grafana/grafana_datasource.py:
    migrated_to: community.grafana
$plugins/callback/grafana_annotations.py:
    maintainers: $team_grafana
    labels: monitoring grafana
    migrated_to: community.grafana
$plugins/doc_fragments/grafana.py:
    maintainers: $team_grafana
    labels: monitoring grafana
    migrated_to: community.grafana
```

---

## ansible.builtin.varnames lookup – Lookup matching variable names — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/varnames_lookup.html

**Contents:**
- ansible.builtin.varnames lookup – Lookup matching variable names
- Synopsis
- Terms
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name varnames. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.varnames for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Retrieves a list of matching Ansible variable names.

List of Python regex patterns to search for in variable names.

Lookup templated value of variables.

list / elements=string

List of the variable names requested.

**Examples:**

Example 1 (unknown):
```unknown
- name: List variables that start with qz_
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.varnames', '^qz_.+') }}"
  vars:
    qz_1: hello
    qz_2: world
    qa_1: "I won't show"
    qz_: "I won't show either"

- name: Show all variables
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.varnames', '.+') }}"

- name: Show variables with 'hosts' in their names
  ansible.builtin.debug: msg="{{ q('varnames', 'hosts') }}"

- name: Find several related variables that end specific way
  ansible.builtin.debug: msg="{{ query('ansible.builtin.varnames', '.+_zone$', '.+_location$') }}"

- name: display values from variables found via varnames (note "*" is used to dereference the list to a 'list of arguments')
  debug: msg="{{ lookup('vars', *lookup('varnames', 'ansible_play_.+')) }}"
```

---

## ansible.builtin.md5 filter – MD5 hash of input data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/md5_filter.html

**Contents:**
- ansible.builtin.md5 filter – MD5 hash of input data
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name md5. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.md5 for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns an MD5 hash of the input data

This describes the input of the filter, the value before | ansible.builtin.md5.

This requires the MD5 algorithm to be available on the system, security contexts like FIPS might prevent this.

MD5 has long been deemed insecure and is not recommended for security related uses.

The MD5 hash of the input.

**Examples:**

Example 1 (javascript):
```javascript
# md5hash => "ae2b1fca515949e5d54fb22b8ed95575"
md5hash: "{{ 'testing' | md5 }}"
```

---

## ansible.builtin.meta module – Execute Ansible ‘actions’ — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/meta_module.html

**Contents:**
- ansible.builtin.meta module – Execute Ansible ‘actions’
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name meta even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.meta for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Meta tasks are a special kind of task which can influence Ansible internal execution or state.

Meta tasks can be used anywhere within your playbook.

This module is also supported for Windows targets.

This module takes a free form command, as a string. There is not an actual option named “free form”. See the examples!

flush_handlers makes Ansible run any handler tasks which have thus far been notified. Ansible inserts these tasks internally at certain points to implicitly trigger handler runs (after pre/post tasks, the final role execution, and the main tasks section of your plays).

refresh_inventory (added in Ansible 2.0) forces the reload of the inventory, which in the case of dynamic inventory scripts means they will be re-executed. If the dynamic inventory script is using a cache, Ansible cannot know this and has no way of refreshing it (you can disable the cache or, if available for your specific inventory datasource (for example amazon.aws.aws_ec2), you can use the an inventory plugin instead of an inventory script). This is mainly useful when additional hosts are created and users wish to use them instead of using the ansible.builtin.add_host module.

Note that neither refresh_inventory nor the ansible.builtin.add_host add hosts to the hosts the current play iterates over. However, if needed, you can explicitly delegate tasks to new hosts with delegate_to. Generally, delegate_to can be used against hosts regardless of whether they are in the inventory or not, as long as the value supplied is sufficient for the connection plugin to access the host.

noop (added in Ansible 2.0) This literally does ‘nothing’. It is mainly used internally and not recommended for general use.

clear_facts (added in Ansible 2.1) causes the gathered facts for the hosts specified in the play’s list of hosts to be cleared, including the fact cache.

clear_host_errors (added in Ansible 2.1) clears the failed state (if any) from hosts specified in the play’s list of hosts. This will make them available for targetting in subsequent plays, but not continue execution in the current play.

end_play (added in Ansible 2.2) causes the play to end without failing the host(s). Note that this affects all hosts.

reset_connection (added in Ansible 2.3) interrupts a persistent connection (i.e. ssh + control persist)

end_host (added in Ansible 2.8) is a per-host variation of end_play. Causes the play to end for the current host without failing it.

end_batch (added in Ansible 2.12) causes the current batch (see serial) to end without failing the host(s). Note that with serial=0 or undefined this behaves the same as end_play.

end_role (added in Ansible 2.18) causes the currently executing role to end without failing the host(s). Effectively all tasks from within a role after end_role is executed are ignored. Since handlers live in a global, play scope, all handlers added via the role are unaffected and are still executed if notified. It is an error to call end_role from outside of a role or from a handler. Note that end_role does not have an effect to the parent roles or roles that depend (via dependencies in meta/main.yml) on a role executing end_role.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Some of the subactions ignore the host loop, see the description above for each specific action for the exceptions

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Most of the subactions ignore the task loop, see the description above for each specific action for the exceptions

These tasks ignore the loop and with_ keywords

While these actions don’t modify the targets directly they do change possible states of the target within the run

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Most options in this action do not use a connection, except reset_connection which still does not connect to the remote

Uses the target’s configured connection information to execute code on it

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Only some options support conditionals and when they do they act ‘bypassing the host loop’, taking the values from first available host

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

clear_facts will remove the persistent facts from ansible.builtin.set_fact using cacheable=True, but not the current host variable it creates for the current run.

Skipping ansible.builtin.meta tasks with tags is not supported before Ansible 2.11.

Asserts given expressions are true.

Fail with custom message.

**Examples:**

Example 1 (unknown):
```unknown
# Example showing flushing handlers on demand, not at end of play
- ansible.builtin.template:
    src: new.j2
    dest: /etc/config.txt
  notify: myhandler

- name: Force all notified handlers to run at this point, not waiting for normal sync points
  ansible.builtin.meta: flush_handlers

# Example showing how to refresh inventory during play
- name: Reload inventory, useful with dynamic inventories when play makes changes to the existing hosts
  cloud_guest:            # this is fake module
    name: newhost
    state: present

- name: Refresh inventory to ensure new instances exist in inventory
  ansible.builtin.meta: refresh_inventory

# Example showing how to clear all existing facts of targeted hosts
- name: Clear gathered facts from all currently targeted hosts
  ansible.builtin.meta: clear_facts

# Example showing how to continue using a failed target, for the next play
- name: Bring host back to play after failure
  ansible.builtin.copy:
    src: file
    dest: /etc/file
  remote_user: imightnothavepermission

- ansible.builtin.meta: clear_host_errors

# Example showing how to reset an existing connection
- ansible.builtin.user:
    name: '{{ ansible_user }}'
    groups: input

- name: Reset ssh connection to allow user changes to affect 'current login user'
  ansible.builtin.meta: reset_connection

# Example showing how to end the play for specific targets
- name: End the play for hosts that run CentOS 6
  ansible.builtin.meta: end_host
  when:
  - ansible_distribution == 'CentOS'
  - ansible_distribution_major_version == '6'
```

---

## ansible.builtin.set_fact module – Set host variable(s) and fact(s). — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/set_fact_module.html

**Contents:**
- ansible.builtin.set_fact module – Set host variable(s) and fact(s).
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name set_fact even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.set_fact for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This action allows setting variables associated to the current host.

These variables will be available to subsequent plays during an ansible-playbook run via the host they were set on.

Set cacheable to true to save variables across executions using a fact cache. Variables will keep the set_fact precedence for the current run, but will used ‘cached fact’ precedence for subsequent ones.

Per the standard Ansible variable precedence rules, other types of variables have a higher priority, so this value may be overridden.

This module has a corresponding action plugin.

This boolean converts the variable into an actual ‘fact’ which will also be added to the fact cache. It does not enable fact caching across runs, it just means it will work with it if already enabled.

Normally this module creates ‘host level variables’ and has much higher precedence, this option changes the nature and precedence (by 7 steps) of the variable created. https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable

This actually creates 2 copies of the variable, a normal ‘set_fact’ host variable with high precedence and a lower ‘ansible_fact’ one that is available for persistence via the facts cache plugin. This creates a possibly confusing interaction with meta: clear_facts as it will remove the ‘ansible_fact’ but not the host variable.

The ansible.builtin.set_fact module takes key=value pairs or key: value (YAML notation) as variables to set in the playbook scope. The ‘key’ is the resulting variable name and the value is, of course, the value of said variable.

You can create multiple variables at once, by supplying multiple pairs, but do NOT mix notations.

While the action plugin does do some of the work it relies on the core engine to actually create the variables, that part cannot be overridden

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

While parts of this action are implemented in core, other parts are still available as normal plugins and can be partially overridden

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

while variable assignment can be delegated to a different host the execution context is always the current inventory_hostname

connection variables, if set at all, would reflect the host it would target, even if we are not connecting at all in this case

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Because of the nature of tasks, set_fact will produce ‘static’ values for a variable. Unlike normal ‘lazy’ variables, the value gets evaluated and templated on assignment.

Some boolean values (yes, no, true, false) will always be converted to boolean type, This is done so the var=value booleans, otherwise it would only be able to create strings, but it also prevents using those values to create YAML strings. Using the setting will restrict k=v to strings, but will allow you to specify string or boolean in YAML.

To create lists/arrays or dictionary/hashes use YAML notation var: [val1, val2].

Since ‘cacheable’ is now a module param, ‘cacheable’ is no longer a valid fact name.

Load variables from files, dynamically within a task.

More information related to variable precedence and which type of variable wins over others.

Dag Wieers (@dagwieers)

**Examples:**

Example 1 (unknown):
```unknown
- name: Setting host facts using key=value pairs, this format can only create strings or booleans
  ansible.builtin.set_fact: one_fact="something" other_fact="{{ local_var }}"

- name: Setting host facts using complex arguments
  ansible.builtin.set_fact:
    one_fact: something
    other_fact: "{{ local_var * 2 }}"
    another_fact: "{{ some_registered_var.results | map(attribute='ansible_facts.some_fact') | list }}"

- name: Setting facts so that they will be persisted in the fact cache
  ansible.builtin.set_fact:
    one_fact: something
    other_fact: "{{ local_var * 2 }}"
    cacheable: yes

- name: Creating list and dictionary variables
  ansible.builtin.set_fact:
    one_dict:
        something: here
        other: there
    one_list:
        - a
        - b
        - c
# As of Ansible 1.8, Ansible will convert boolean strings ('true', 'false', 'yes', 'no')
# to proper boolean values when using the key=value syntax, however it is still
# recommended that booleans be set using the complex argument style:
- name: Setting booleans using complex argument style
  ansible.builtin.set_fact:
    one_fact: yes
    other_fact: no

- name: Creating list and dictionary variables using 'shorthand' YAML
  ansible.builtin.set_fact:
    two_dict: {'something': here2, 'other': somewhere}
    two_list: [1,2,3]
```

---

## ansible.builtin.title filter – Return a titlecased version of the value. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/title_filter.html

**Contents:**
- ansible.builtin.title filter – Return a titlecased version of the value.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name title. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.title for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a titlecased version of the value.

This is the Jinja builtin filter plugin ‘title’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.title

---

## ansible.builtin.abs filter – Return the absolute value of the argument. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/abs_filter.html

**Contents:**
- ansible.builtin.abs filter – Return the absolute value of the argument.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name abs. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.abs for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the absolute value of the argument.

This is the Jinja builtin filter plugin ‘abs’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.abs

---

## Generating changelogs and porting guide entries in a collection — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_changelogs.html

**Contents:**
- Generating changelogs and porting guide entries in a collection
- Understanding antsibull-changelog
  - Generating changelogs
  - Porting Guide entries from changelog fragments
- Including collection changelogs into Ansible

You can create and share changelog and porting guide entries for your collection. If your collection is part of the Ansible Community package, we recommend that you use the antsibull-changelog tool to generate Ansible-compatible changelogs. The Ansible changelog uses the output of this tool to collate all the collections included in an Ansible release into one combined changelog for the release.

Ansible here refers to the Ansible 2.10 or later release that includes a curated set of collections.

Understanding antsibull-changelog

Generating changelogs

Porting Guide entries from changelog fragments

Including collection changelogs into Ansible

The antsibull-changelog tool allows you to create and update changelogs for Ansible collections that are compatible with the combined Ansible changelogs. This is an update to the changelog generator used in prior Ansible releases. The tool adds three new changelog fragment categories: breaking_changes, security_fixes and trivial. The tool also generates the changelog.yaml file that Ansible uses to create the combined CHANGELOG.rst file and Porting Guide for the release.

See Creating a changelog fragment and the antsibull-changelog documentation for complete details.

The collection maintainers set the changelog policy for their collections. See the individual collection contributing guidelines for complete details.

To initialize changelog generation:

Install antsibull-changelog: pip install antsibull-changelog.

Initialize changelogs for your repository: antsibull-changelog init <path/to/your/collection>.

Optionally, edit the changelogs/config.yaml file to customize the location of the generated changelog .rst file or other options. See Bootstrapping changelogs for collections for details.

To generate changelogs from the changelog fragments you created:

Optionally, validate your changelog fragments: antsibull-changelog lint.

Generate the changelog for your release: antsibull-changelog release [--version version_number].

Add the --reload-plugins option if you ran the antsibull-changelog release command previously and the version of the collection has not changed. antsibull-changelog caches the information on all plugins and does not update its cache until the collection version changes.

The Ansible changelog generator automatically adds several changelog fragment categories to the Ansible Porting Guide:

If your collection is part of Ansible, use one of the following three options to include your changelog into the Ansible release changelog:

Use the antsibull-changelog tool.

If are not using this tool, include the properly formatted changelog.yaml file into your collection. See the changelog.yaml format for details.

Add a link to own changelogs or release notes in any format by opening an issue at https://github.com/ansible-community/ansible-build-data/ with the HTML link to that information.

For the first two options, Ansible pulls the changelog details from Galaxy so your changelogs must be included in the collection version on Galaxy that is included in the upcoming Ansible release.

Learn how to create good changelog fragments.

Learn how to install and use collections.

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## ansible.builtin.package module – Generic OS package manager — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/package_module.html

**Contents:**
- ansible.builtin.package module – Generic OS package manager
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name package even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.package for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This modules manages packages on a target without specifying a package manager module (like ansible.builtin.dnf, ansible.builtin.apt, …). It is convenient to use in an heterogeneous environment of machines without having to create a specific task for each package manager. ansible.builtin.package calls behind the module for the package manager used by the operating system discovered by the module ansible.builtin.setup. If ansible.builtin.setup was not yet run, ansible.builtin.package will run it.

This module acts as a proxy to the underlying package manager module. While all arguments will be passed to the underlying module, not all modules support the same arguments. This documentation only covers the minimum intersection of module arguments that all packaging modules support.

For Windows targets, use the ansible.windows.win_package module instead.

This module has a corresponding action plugin.

The below requirements are needed on the host that executes this module.

Whatever is required for the package plugins specific for each system.

Package name, or package specifier with version.

Syntax varies with package manager. For example name-1.0 or name=1.0.

Package names also vary with package manager; this module will not “translate” them per distribution. For example libyaml-dev, libyaml-devel.

To operate on several packages this can accept a comma separated string of packages or a list of packages, depending on the underlying package manager.

Whether to install (present), or remove (absent) a package.

You can use other states like latest ONLY if they are supported by the underlying package module(s) executed.

The required package manager module to use (dnf, apt, and so on). The default auto will use existing facts or try to auto-detect it.

You should only use this field if the automatic selection is not working for some reason.

Since version 2.17 you can use the ansible_package_use variable to override the automatic detection, but this option still takes precedence.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

support depends on the underlying plugin invoked

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

support depends on the underlying plugin invoked

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The support depends on the availability for the specific plugin for each platform and if fact gathering is able to detect it

Target OS/families that can be operated against

While ansible.builtin.package abstracts package managers to ease dealing with multiple distributions, package name often differs for the same software.

**Examples:**

Example 1 (unknown):
```unknown
- name: Install ntpdate
  ansible.builtin.package:
    name: ntpdate
    state: present

# This uses a variable as this changes per distribution.
- name: Remove the apache package
  ansible.builtin.package:
    name: "{{ apache }}"
    state: absent

- name: Install the latest version of Apache and MariaDB
  ansible.builtin.package:
    name:
      - httpd
      - mariadb-server
    state: latest

- name: Use the dnf package manager to install httpd
  ansible.builtin.package:
    name: httpd
    state: present
    use: dnf
```

---

## ansible.builtin.sameas test – Check if an object points to the same memory address than another object. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sameas_test.html

**Contents:**
- ansible.builtin.sameas test – Check if an object points to the same memory address than another object.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sameas. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sameas for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if an object points to the same memory address than another object.

This is the Jinja builtin test plugin ‘sameas’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.sameas

---

## ansible.builtin.tojson filter – Serialize an object to a string of JSON, and mark it safe to render in HTML. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/tojson_filter.html

**Contents:**
- ansible.builtin.tojson filter – Serialize an object to a string of JSON, and mark it safe to render in HTML.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name tojson. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.tojson for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Serialize an object to a string of JSON, and mark it safe to render in HTML.

This is the Jinja builtin filter plugin ‘tojson’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.tojson

---

## ansible.builtin.pprint filter – Pretty print a variable. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/pprint_filter.html

**Contents:**
- ansible.builtin.pprint filter – Pretty print a variable.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name pprint. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.pprint for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Pretty print a variable.

This is the Jinja builtin filter plugin ‘pprint’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.pprint

---

## ansible.builtin.number test – Return true if the variable is a number. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/number_test.html

**Contents:**
- ansible.builtin.number test – Return true if the variable is a number.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name number. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.number for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is a number.

This is the Jinja builtin test plugin ‘number’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.number

---

## ansible.builtin.search test – Does string match a regular expression — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/search_test.html

**Contents:**
- ansible.builtin.search test – Does string match a regular expression
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name search. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.search for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Compare string against regular expression using Python’s search function.

Aliases: formerly_core_masked_test, formerly_core_test

This describes the input of the test, the value before is ansible.builtin.search or is not ansible.builtin.search.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.search(key1=value1, key2=value2, ...) and input is not ansible.builtin.search(key1=value1, key2=value2, ...)

Use case insensitive matching.

Match against multiple lines in string.

Regex to match against.

Returns True if there is a match, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
url: "https://example.com/users/foo/resources/bar"
foundmatch: url is search("https://example.com/users/.*/resources")
alsomatch: url is search("users/.*/resources")
```

---

## ansible.builtin.dirname filter – get a path’s directory name — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dirname_filter.html

**Contents:**
- ansible.builtin.dirname filter – get a path’s directory name
- Synopsis
- Input
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name dirname. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dirname for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the ‘head’ component of a path, basically everything that is not the ‘basename’.

This describes the input of the filter, the value before | ansible.builtin.dirname.

The result of this filter is different from the Unix dirname program; where dirname for /foo/bar/ returns /foo, the dirname filter returns the full path (/foo/bar/).

get a path’s base name.

The directory portion of the original path.

**Examples:**

Example 1 (unknown):
```unknown
# To get the dir name of a file path, like '/etc/asdf' out of '/etc/asdf/foo.txt'.
{{ mypath | dirname }}
```

---

## ansible.builtin.link_exists test – does the path exist, no follow — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/link_exists_test.html

**Contents:**
- ansible.builtin.link_exists test – does the path exist, no follow
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name link_exists. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.link_exists for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to an existing symlink on the controller’s filesystem (localhost).

Does not follow symlinks, so it only verifies that the link itself exists.

This describes the input of the test, the value before is ansible.builtin.link_exists or is not ansible.builtin.link_exists.

Returns True if the path corresponds to an existing filesystem object on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
ismyhostsalink: "{{ '/etc/hosts' is link_exists}}"
list_of_symlinks: "{{ list_of_paths | select('link_exists') }}"
```

---

## ansible.builtin.none test – Return true if the variable is none. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/none_test.html

**Contents:**
- ansible.builtin.none test – Return true if the variable is none.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name none. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.none for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is none.

This is the Jinja builtin test plugin ‘none’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.none

---

## ansible.builtin.string test – Return true if the object is a string. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/string_test.html

**Contents:**
- ansible.builtin.string test – Return true if the object is a string.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name string. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.string for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is a string.

This is the Jinja builtin test plugin ‘string’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.string

---

## ansible.builtin.unique filter – set of unique items of a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/unique_filter.html

**Contents:**
- ansible.builtin.unique filter – set of unique items of a list
- Synopsis
- Input
- Keyword parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name unique. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.unique for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Creates a list of unique elements (a set) from the provided input list.

This describes the input of the filter, the value before | ansible.builtin.unique.

list / elements=string / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.unique(key1=value1, key2=value2, ...)

Filter objects with unique values for this attribute.

Whether to consider case when comparing elements.

the difference of one list from another.

intersection of lists.

different items from two lists.

list / elements=string

A list with unique elements, also known as a set.

**Examples:**

Example 1 (javascript):
```javascript
# return only the unique elements of list1
# list1: [1, 2, 5, 1, 3, 4, 10]
{{ list1 | unique }}
# => [1, 2, 5, 3, 4, 10]

# return case sensitive unique elements
{{ ['a', 'A', 'a'] | unique(case_sensitive='true') }}
# => ['a', 'A']

# return case insensitive unique elements
{{ ['b', 'B', 'b'] | unique() }}
# => ['b']

# return unique elements of list based on attribute
# => [{"age": 12, "name": "a" }, { "age": 14, "name": "b"}]
- debug:
    msg: "{{ sample | unique(attribute='age') }}"
  vars:
    sample:
      - name: a
        age: 12
      - name: b
        age: 14
      - name: c
        age: 14
```

---

## ansible.builtin.items2dict filter – Consolidate a list of itemized dictionaries into a dictionary — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/items2dict_filter.html

**Contents:**
- ansible.builtin.items2dict filter – Consolidate a list of itemized dictionaries into a dictionary
- Synopsis
- Input
- Positional parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name items2dict. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.items2dict for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Takes a list of dicts with each having a key and value keys, and transforms the list into a dictionary, effectively as the reverse of dict2items.

This describes the input of the filter, the value before | ansible.builtin.items2dict.

list / elements=dictionary / required

A list of dictionaries.

Every dictionary must have keys key and value.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.items2dict(positional1, positional2, ...)

The name of the key in the element dictionaries that holds the key to use at destination.

The name of the key in the element dictionaries that holds the value to use at destination.

Convert a dictionary into an itemized list of dictionaries.

Dictionary with the consolidated key/values.

**Examples:**

Example 1 (javascript):
```javascript
# mydict =>  { "hi": "bye", "ciao": "ciao" }
mydict: {{ [{'key': 'hi', 'value': 'bye'}, {'key': 'ciao', 'value': 'ciao'} ]| items2dict}}

# The output is a dictionary with two key/value pairs:
#     Application: payment
#     Environment: dev
vars:
  tags:
    - key: Application
      value: payment
    - key: Environment
      value: dev
  consolidated: "{{ tags | items2dict }}"
```

---

## ansible.builtin.xmlattr filter – Create an SGML/XML attribute string based on the items in a dict. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/xmlattr_filter.html

**Contents:**
- ansible.builtin.xmlattr filter – Create an SGML/XML attribute string based on the items in a dict.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name xmlattr. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.xmlattr for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Create an SGML/XML attribute string based on the items in a dict.

This is the Jinja builtin filter plugin ‘xmlattr’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.xmlattr

---

## ansible.builtin.symmetric_difference filter – different items from two lists — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/symmetric_difference_filter.html

**Contents:**
- ansible.builtin.symmetric_difference filter – different items from two lists
- Synopsis
- Input
- Keyword parameters
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name symmetric_difference. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.symmetric_difference for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Provide a unique list of all the elements unique to each list.

Items in the resulting list are returned in arbitrary order.

This describes the input of the filter, the value before | ansible.builtin.symmetric_difference.

list / elements=string / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.symmetric_difference(key1=value1, key2=value2, ...)

list / elements=string / required

the difference of one list from another.

intersection of lists.

set of unique items of a list.

list / elements=string

A unique list of the elements from two lists that are unique to each one.

**Examples:**

Example 1 (javascript):
```javascript
# return the elements of list1 not in list2 and the elements in list2 not in list1
# list1: [1, 2, 5, 1, 3, 4, 10]
# list2: [1, 2, 3, 4, 5, 11, 99]
{{ list1 | symmetric_difference(list2) }}
# => [10, 11, 99]
```

---

## ansible.builtin.all test – are all conditions in a list true — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/all_test.html

**Contents:**
- ansible.builtin.all test – are all conditions in a list true
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name all. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.all for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This test checks each condition in a list for truthiness.

Same as the all Python function.

This describes the input of the test, the value before is ansible.builtin.all or is not ansible.builtin.all.

list / elements=any / required

List of conditions, each can be a boolean or conditional expression that results in a boolean value.

Returns True if all elements of the list were True, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
varexpression: "{{ 3 == 3 }}"
# are all statements true?
{{ [true, booleanvar, varexpression] is all }}
```

---

## Using shared resources in collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_shared.html

**Contents:**
- Using shared resources in collections
- Using documentation fragments in collections
- Leveraging optional module utilities in collections
- Listing collection dependencies

Although developing Ansible modules contained in collections is similar to developing standalone Ansible modules, you use shared resources like documentation fragments and module utilities differently in collections. You can use documentation fragments within and across collections. You can use optional module utilities to support multiple versions of ansible-core in your collection. Collections can also depend on other collections.

Using documentation fragments in collections

Leveraging optional module utilities in collections

Listing collection dependencies

To include documentation fragments in your collection:

Create the documentation fragment: plugins/doc_fragments/fragment_name.

Refer to the documentation fragment with its FQCN.

Documentation fragments covers the basics for documentation fragments. The kubernetes.core collection includes a complete example.

If you use FQCN, you can use documentation fragments from one collection in another collection.

Optional module utilities let you adopt the latest features from the most recent ansible-core release in your collection-based modules without breaking your collection on older Ansible versions. With optional module utilities, you can use the latest features when running against the latest versions, while still providing fallback behaviors when running against older versions.

This implementation, widely used in Python programming, wraps optional imports in conditionals or defensive try/except blocks, and implements fallback behaviors for missing imports. Ansible’s module payload builder supports these patterns by treating any module_utils import nested in a block (e.g., if, try) as optional. If the requested import cannot be found during the payload build, it is simply omitted from the target payload and assumed that the importing code will handle its absence at runtime. Missing top-level imports of module_utils packages (imports that are not wrapped in a block statement of any kind) will fail the module payload build, and will not execute on the target.

For example, the ansible.module_utils.common.respawn package is only available in Ansible 2.11 and higher. The following module code would fail during the payload build on Ansible 2.10 or earlier (as the requested Python module does not exist, and is not wrapped in a block to signal to the payload builder that it can be omitted from the module payload):

By wrapping the import statement in a try block, the payload builder will omit the Python module if it cannot be located, and assume that the Ansible module will handle it at runtime:

The optional import behavior also applies to module_utils imported from collections.

We recommend that collections work as standalone, independent units, depending only on ansible-core. However, if your collection must depend on features and functionality from another collection, list the other collection or collections under dependencies in your collection’s galaxy.yml file. Use the meta/runtime.yml file to set the ansible-core version that your collection depends on. For more information on the galaxy.yml file, see Collection Galaxy metadata structure.

You can use Git repositories for collection dependencies during local development and testing. For example:

Do not use Git repositories as dependencies for published collections. Dependencies for published collections must be other published collections.

Learn how to install and use collections.

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
extends_documentation_fragment:
  - kubernetes.core.k8s_name_options
  - kubernetes.core.k8s_auth_options
  - kubernetes.core.k8s_resource_options
  - kubernetes.core.k8s_scale_options
```

Example 2 (python):
```python
from ansible.module_utils.common.respawn import respawn_module
```

Example 3 (python):
```python
try:
    from ansible.module_utils.common.respawn import respawn_module
except ImportError:
    respawn_module = None
...
if needs_respawn:
    if respawn_module:
        respawn_module(target)
    else:
        module.fail_json('respawn is not available in Ansible < 2.11, ensure that foopkg is installed')
```

Example 4 (unknown):
```unknown
dependencies: {'[email protected]:organization/repo_name.git': 'devel'}
```

---

## ansible.builtin.hostname module – Manage hostname — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/hostname_module.html

**Contents:**
- ansible.builtin.hostname module – Manage hostname
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name hostname even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.hostname for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Set system’s hostname. Supports most OSs/Distributions including those using systemd.

Windows, HP-UX, and AIX are not currently supported.

The below requirements are needed on the host that executes this module.

If the value is a fully qualified domain name that does not resolve from the given host, this will cause the module to hang for a few seconds while waiting for the name resolution attempt to timeout.

Which strategy to use to update the hostname.

If not set we try to autodetect, but this can be problematic, particularly with containers as they can present misleading information.

Note that systemd should be specified for RHEL/EL/CentOS 7+. Older distributions should use redhat.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

Target OS/families that can be operated against

This module does NOT modify /etc/hosts. You need to modify it yourself using other modules such as ansible.builtin.template or ansible.builtin.replace.

On macOS, this module uses scutil to set HostName, ComputerName, and LocalHostName. Since LocalHostName cannot contain spaces or most special characters, this module will replace characters when setting LocalHostName.

Adrian Likins (@alikins)

Hideki Saito (@saito-hideki)

**Examples:**

Example 1 (unknown):
```unknown
- name: Set a hostname
  ansible.builtin.hostname:
    name: web01

- name: Set a hostname specifying strategy
  ansible.builtin.hostname:
    name: web01
    use: systemd
```

---

## ansible.builtin.type_debug filter – show input data type — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/type_debug_filter.html

**Contents:**
- ansible.builtin.type_debug filter – show input data type
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name type_debug. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.type_debug for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the equivalent of Python’s type function.

This describes the input of the filter, the value before | ansible.builtin.type_debug.

Variable or expression of which you want to determine type.

The Python ‘type’ of the _input provided.

Adrian Likins (@alikins)

**Examples:**

Example 1 (unknown):
```unknown
# get type of 'myvar'
{{ myvar | type_debug }}
```

---

## ansible.builtin.directory test – does the path resolve to an existing directory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/directory_test.html

**Contents:**
- ansible.builtin.directory test – does the path resolve to an existing directory
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name directory. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.directory for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to an existing directory on the controller’s filesystem (localhost).

This describes the input of the test, the value before is ansible.builtin.directory or is not ansible.builtin.directory.

Returns True if the path corresponds to an existing directory on the filesystem on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
vars:
  my_etc_hosts_not_a_dir: "{{ '/etc/hosts' is directory}}"
  list_of_files: "{{ list_of_paths | reject('directory') }}"
```

---

## ansible.builtin.config lookup – Display the ‘resolved’ Ansible option values. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/config_lookup.html

**Contents:**
- ansible.builtin.config lookup – Display the ‘resolved’ Ansible option values.
- Synopsis
- Terms
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name config. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.config for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Retrieves the value of an Ansible configuration setting, resolving all sources, from defaults, ansible.cfg, environment, CLI, and variables, but not keywords.

The values returned assume the context of the current host or inventory_hostname.

You can use ansible-config list to see the global available settings, add -t all to also show plugin options.

The option(s) to look up.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.config', key1=value1, key2=value2, ...) and query('ansible.builtin.config', key1=value1, key2=value2, ...)

Action to take if term is missing from config

"error" (default): Issue an error message and raise fatal signal

"skip": Silently ignore

"warn": Issue a warning message and continue

added in ansible-core 2.12

The name of the plugin for which you want to retrieve configuration settings.

added in ansible-core 2.12

The type of the plugin referenced by ‘plugin_name’ option.

added in ansible-core 2.16

Set this to return what configuration subsystem the value came from (defaults, config file, environment, CLI, or variables).

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.config', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.config', term1, term2, key1=value1, key2=value2)

Be aware that currently this lookup cannot take keywords nor delegation into account, so for options that support keywords or are affected by delegation, it is at best a good guess or approximation.

A list of value(s) of the key(s) in the config if show_origin is false (default)

Optionally, a list of 2 element lists (value, origin) if show_origin is true

**Examples:**

Example 1 (unknown):
```unknown
- name: Show configured default become user
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.config', 'DEFAULT_BECOME_USER')}}"

- name: print out role paths
  ansible.builtin.debug:
    msg: "These are the configured role paths: {{lookup('ansible.builtin.config', 'DEFAULT_ROLES_PATH')}}"

- name: find retry files, skip if missing that key
  ansible.builtin.find:
    paths: "{{lookup('ansible.builtin.config', 'RETRY_FILES_SAVE_PATH')|default(playbook_dir, True)}}"
    patterns: "*.retry"

- name: see the colors
  ansible.builtin.debug: msg="{{item}}"
  loop: "{{lookup('ansible.builtin.config', 'COLOR_OK', 'COLOR_CHANGED', 'COLOR_SKIP', wantlist=True)}}"

- name: skip if bad value in var
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.config', config_in_var, on_missing='skip')}}"
  var:
    config_in_var: UNKNOWN

- name: show remote user and port for ssh connection
  ansible.builtin.debug: msg={{q("ansible.builtin.config", "remote_user", "port", plugin_type="connection", plugin_name="ssh", on_missing='skip')}}

- name: show remote_tmp setting for shell (sh) plugin
  ansible.builtin.debug: msg={{q("ansible.builtin.config", "remote_tmp", plugin_type="shell", plugin_name="sh")}}
```

---

## ansible.builtin.cmd shell – Windows Command Prompt — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/cmd_shell.html

**Contents:**
- ansible.builtin.cmd shell – Windows Command Prompt
- Synopsis
- Parameters
  - Collection links

This shell plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name cmd. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.cmd for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same shell plugin name.

Used with the ‘ssh’ connection plugin and no DefaultShell has been set on the Windows host.

Directory in which ansible will keep async job information.

Before Ansible 2.8, this was set to remote_tmp + "\.ansible_async".

Default: "%USERPROFILE%\\.ansible_async"

Variable: ansible_async_dir

Temporary directory to use on targets when copying files to the host.

Variable: ansible_remote_tmp

Controls if we set the locale for modules when executing on the target.

Windows only supports no as an option.

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[powershell]
async_dir = %USERPROFILE%\.ansible_async
```

Example 2 (unknown):
```unknown
[powershell]
remote_tmp = %TEMP%
```

---

## ansible.builtin.unreachable test – Did task end due to the host was unreachable — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/unreachable_test.html

**Contents:**
- ansible.builtin.unreachable test – Did task end due to the host was unreachable
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name unreachable. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.unreachable for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task was not able to reach the host for execution

This test checks for the existence of a unreachable key in the input dictionary and that it’s value is True

This describes the input of the test, the value before is ansible.builtin.unreachable or is not ansible.builtin.unreachable.

dictionary / required

registered result from an Ansible task

Returns True if the task flagged the host as unreachable, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is unreachable }}
```

---

## ansible.builtin.truthy test – Pythonic true — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/truthy_test.html

**Contents:**
- ansible.builtin.truthy test – Pythonic true
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name truthy. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.truthy for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-base 2.10

This check is a more Python version of what is ‘true’.

It is the opposite of ansible.builtin.falsy.

This describes the input of the test, the value before is ansible.builtin.truthy or is not ansible.builtin.truthy.

An expression that can be expressed in a boolean context.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.truthy(key1=value1, key2=value2, ...) and input is not ansible.builtin.truthy(key1=value1, key2=value2, ...)

Attempts to convert to strict python boolean vs normally acceptable values (yes/no, on/off, 0/1, etc).

Returns True if the condition is not “Python truthy”, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
thisistrue: '{{ "any string" is truthy }}'
thisisfalse: '{{ "" is truthy }}'
```

---

## ansible.builtin.rejectattr filter – Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/rejectattr_filter.html

**Contents:**
- ansible.builtin.rejectattr filter – Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name rejectattr. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.rejectattr for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.

This is the Jinja builtin filter plugin ‘rejectattr’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.rejectattr

---

## ansible.builtin.subversion module – Deploys a subversion repository — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/subversion_module.html

**Contents:**
- ansible.builtin.subversion module – Deploys a subversion repository
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name subversion even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.subversion for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Deploy given repository URL / revision to dest. If dest exists, update to the specified revision, otherwise perform a checkout.

The below requirements are needed on the host that executes this module.

subversion (the command line tool with svn entrypoint)

If false, do not check out the repository if it does not exist locally.

Absolute path where the repository should be deployed.

The destination directory must be specified unless checkout=no, update=no, and export=no.

Path to svn executable to use. If not supplied, the normal mechanism for resolving binary paths will be used.

If true, do export instead of checkout/update.

If true, modified files will be discarded. If false, module will fail if it encounters modified files. Prior to 1.9 the default was true.

If the directory exists, then the working copy will be checked-out over-the-top using svn checkout --force; if force is specified then existing files with different content are reverted.

--password parameter passed to svn when svn is less than version 1.10.0. This is not secure and the password will be leaked to argv.

--password-from-stdin parameter when svn is greater or equal to version 1.10.0.

aliases: name, repository

The subversion URL to the repository.

aliases: rev, version

Specific revision to checkout.

If false, do not call svn switch before update.

If false, do not retrieve new revisions from the origin repository.

--username parameter passed to svn.

added in ansible-core 2.11

If false, passes the --trust-server-cert flag to svn.

If true, does not pass the flag.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

This module does not handle externals.

Dane Summers (@dsummersl)

**Examples:**

Example 1 (unknown):
```unknown
- name: Checkout subversion repository to specified folder
  ansible.builtin.subversion:
    repo: svn+ssh://an.example.org/path/to/repo
    dest: /src/checkout

- name: Export subversion directory to folder
  ansible.builtin.subversion:
    repo: svn+ssh://an.example.org/path/to/repo
    dest: /src/export
    export: yes

- name: Get information about the repository whether or not it has already been cloned locally
  ansible.builtin.subversion:
    repo: svn+ssh://an.example.org/path/to/repo
    dest: /src/checkout
    checkout: no
    update: no
```

---

## ansible.builtin.in test – Check if value is in seq. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/in_test.html

**Contents:**
- ansible.builtin.in test – Check if value is in seq.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name in. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.in for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if value is in seq.

This is the Jinja builtin test plugin ‘in’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.in

---

## ansible.builtin.urlize filter – Convert URLs in text into clickable links. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/urlize_filter.html

**Contents:**
- ansible.builtin.urlize filter – Convert URLs in text into clickable links.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name urlize. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.urlize for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert URLs in text into clickable links.

This is the Jinja builtin filter plugin ‘urlize’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.urlize

---

## Collections index — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_index.html

**Contents:**
- Collections index

You can find an index of collections at Collection Index.

---

## ansible.builtin.su become – Substitute User — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/su_become.html

**Contents:**
- ansible.builtin.su become – Substitute User
- Synopsis
- Parameters
  - Authors
  - Collection links

This become plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name su. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.su for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same become plugin name.

This become plugin allows your remote/login user to execute commands as another user via the su utility.

Environment variable: ANSIBLE_BECOME_EXE

Environment variable: ANSIBLE_SU_EXE

Variable: ansible_become_exe

Variable: ansible_su_exe

Options to pass to su

Environment variable: ANSIBLE_BECOME_FLAGS

Environment variable: ANSIBLE_SU_FLAGS

Keyword: become_flags

Variable: ansible_become_flags

Variable: ansible_su_flags

Password to pass to su

Environment variable: ANSIBLE_BECOME_PASS

Environment variable: ANSIBLE_SU_PASS

Variable: ansible_become_password

Variable: ansible_become_pass

Variable: ansible_su_pass

User you ‘become’ to execute the task

Environment variable: ANSIBLE_BECOME_USER

Environment variable: ANSIBLE_SU_USER

Variable: ansible_become_user

Variable: ansible_su_user

list / elements=string

List of localized strings to match for prompt detection

If empty we’ll use the built in one

Do NOT add a colon (:) to your custom entries. Ansible adds a colon at the end of each prompt; if you add another one in your string, your prompt will fail with a “Timeout” error.

Environment variable: ANSIBLE_SU_PROMPT_L10N

Variable: ansible_su_prompt_l10n

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[privilege_escalation]
become_exe = su
```

Example 2 (unknown):
```unknown
[su_become_plugin]
executable = su
```

Example 3 (unknown):
```unknown
[privilege_escalation]
become_flags = ""
```

Example 4 (unknown):
```unknown
[su_become_plugin]
flags = ""
```

---

## ansible.builtin.expect module – Executes a command and responds to prompts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/expect_module.html

**Contents:**
- ansible.builtin.expect module – Executes a command and responds to prompts
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name expect even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.expect for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.expect module executes a command and responds to prompts.

The given command will be executed on all selected nodes. It will not be processed through the shell, so variables like $HOME and operations like "<", ">", "|", and "&" will not work.

The below requirements are needed on the host that executes this module.

Change into this directory before running the command.

The command module takes command to run.

A filename, when it already exists, this step will not be run.

Whether or not to echo out your response strings.

A filename, when it does not exist, this step will not be run.

dictionary / required

Mapping of prompt regular expressions and corresponding answer(s).

Each key in responses is a Python regex https://docs.python.org/3/library/re.html#regular-expression-syntax.

The value of each key is a string or list of strings. If the value is a string and the prompt is encountered multiple times, the answer will be repeated. Provide the value as a list to give different answers for successive matches.

Amount of time in seconds to wait for the expected strings. Use null to disable timeout.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

If you want to run a command through the shell (say you are using <, >, |, and so on), you must specify a shell in the command such as /bin/bash -c "/path/to/something | grep else".

Case insensitive searches are indicated with a prefix of (?i).

The pexpect library used by this module operates with a search window of 2000 bytes, and does not use a multiline regex match. To perform a start of line bound match, use a pattern like (?m^pattern).

The ansible.builtin.expect module is designed for simple scenarios. For more complex needs, consider the use of expect code with the ansible.builtin.shell or ansible.builtin.script modules. (An example is part of the ansible.builtin.shell module documentation).

If the command returns non UTF-8 data, it must be encoded to avoid issues. One option is to pipe the output through base64.

Runs a local script on a remote node after transferring it.

Execute shell commands on targets.

**Examples:**

Example 1 (unknown):
```unknown
- name: Case insensitive password string match
  ansible.builtin.expect:
    command: passwd username
    responses:
      (?i)password: "MySekretPa$$word"
  # you don't want to show passwords in your logs
  no_log: true

- name: Match multiple regular expressions and demonstrate individual and repeated responses
  ansible.builtin.expect:
    command: /path/to/custom/command
    responses:
      Question:
        # give a unique response for each of the 3 hypothetical prompts matched
        - response1
        - response2
        - response3
      # give the same response for every matching prompt
      "^Match another prompt$": "response"

- name: Multiple questions with responses
  ansible.builtin.expect:
    command: /path/to/custom/command
    responses:
        "Please provide your name":
            - "Anna"
        "Database user":
            - "{{ db_username }}"
        "Database password":
            - "{{ db_password }}"
```

---

## ansible.builtin.debug module – Print statements during execution — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/debug_module.html

**Contents:**
- ansible.builtin.debug module – Print statements during execution
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name debug even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.debug for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module prints statements during execution and can be useful for debugging variables or expressions without necessarily halting the playbook.

Useful for debugging together with the when: directive.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

The customized message that is printed. If omitted, prints a generic message.

Default: "Hello world!"

A variable name to debug.

Mutually exclusive with the msg option.

Be aware that this option already runs in Jinja2 context and has an implicit {{ }} wrapping, so you should not be using Jinja2 delimiters unless you are looking for double interpolation.

A number that controls when the debug is run, if you set to 3 it will only run debug when -vvv or above.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

Aside from register and/or in combination with delegate_facts, it has little effect.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Asserts given expressions are true.

Fail with custom message.

Dag Wieers (@dagwieers)

**Examples:**

Example 1 (unknown):
```unknown
- name: Print the gateway for each host when defined
  ansible.builtin.debug:
    msg: System {{ inventory_hostname }} has gateway {{ ansible_default_ipv4.gateway }}
  when: ansible_default_ipv4.gateway is defined

- name: Get uptime information
  ansible.builtin.shell: /usr/bin/uptime
  register: result

- name: Print return information from the previous task
  ansible.builtin.debug:
    var: result
    verbosity: 2

- name: Display all variables/facts known for a host
  ansible.builtin.debug:
    var: hostvars[inventory_hostname]
    verbosity: 4

- name: Prints two lines of messages, but only if there is an environment value set
  ansible.builtin.debug:
    msg:
    - "Provisioning based on YOUR_KEY which is: {{ lookup('ansible.builtin.env', 'YOUR_KEY') }}"
    - "These servers were built using the password of '{{ password_used }}'. Please retain this for later use."
```

---

## ansible.builtin.permutations filter – permutations from the elements of a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/permutations_filter.html

**Contents:**
- ansible.builtin.permutations filter – permutations from the elements of a list
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name permutations. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.permutations for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Create a list of the permutations of lists from the elements of a list.

Unlike combinations, in permutations order is significant.

This describes the input of the filter, the value before | ansible.builtin.permutations.

list / elements=string / required

Elements to base the permutations on.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.permutations(positional1, positional2, ...)

The size of the list for each permutation.

list / elements=string

List of permutations lists resulting from the supplied elements and list size.

**Examples:**

Example 1 (javascript):
```javascript
# ptrs_of_two => [ [ 1, 2 ], [ 1, 3 ], [ 1, 4 ], [ 1, 5 ], [ 2, 1 ], [ 2, 3 ], [ 2, 4 ], [ 2, 5 ], [ 3, 1 ], [ 3, 2 ], [ 3, 4 ], [ 3, 5 ], [ 4, 1 ], [ 4, 2 ], [ 4, 3 ], [ 4, 5 ], [ 5, 1 ], [ 5, 2 ], [ 5, 3 ], [ 5, 4 ] ]
prts_of_two:  "{{ [1,2,3,4,5] | permutations(2) }}"
```

---

## ansible.builtin.uri module – Interacts with webservices — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/uri_module.html

**Contents:**
- ansible.builtin.uri module – Interacts with webservices
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name uri even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.uri for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Interacts with HTTP and HTTPS web services and supports Digest, Basic and WSSE HTTP authentication mechanisms.

For Windows targets, use the ansible.windows.win_uri module instead.

This module has a corresponding action plugin.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

The body of the http request/response to the web service. If body_format is set to json it will take an already formatted JSON string or convert a data structure into JSON.

If body_format is set to form-urlencoded it will convert a dictionary or list of tuples into an application/x-www-form-urlencoded string. (Added in v2.7)

If body_format is set to form-multipart it will convert a dictionary into multipart/form-multipart body. (Added in v2.10)

If body_format is set to form-multipart the option ‘multipart_encoding’ allows to change multipart file encoding. (Added in v2.19)

The serialization format of the body. When set to json, form-multipart, or form-urlencoded, encodes the body argument, if needed, and automatically sets the Content-Type header accordingly.

As of v2.3 it is possible to override the Content-Type header, when set to json or form-urlencoded via the headers option.

The Content-Type header cannot be overridden when using form-multipart.

form-urlencoded was added in v2.7.

form-multipart was added in v2.10.

added in ansible-core 2.11

PEM formatted file that contains a CA certificate to be used for validation.

list / elements=string

added in ansible-core 2.14

SSL/TLS Ciphers to use for the request.

When a list is provided, all ciphers are joined in order with :

See the OpenSSL Cipher List Format for more details.

The available ciphers is dependent on the Python and OpenSSL/LibreSSL versions.

PEM formatted certificate chain file to be used for SSL client authentication.

This file can also include the key as well, and if the key is included, client_key is not required.

PEM formatted file that contains your private key to be used for SSL client authentication.

If client_cert contains both the certificate and key, this option is not required.

A filename, when it already exists, this step will not be run.

added in ansible-core 2.14

Whether to attempt to decompress gzip content-encoded responses.

A path of where to download the file to (if desired). If dest is a directory, the basename of the file on the remote server will be used.

Whether or not the URI module should follow redirects.

"all": Will follow all redirects.

"no": (DEPRECATED, removed in 2.22) alias of none.

"none": Will not follow any redirects.

"safe" (default): Only redirects doing GET or HEAD requests will be followed.

"urllib2": Defer to urllib2 behavior (As of writing this follows HTTP redirects).

"yes": (DEPRECATED, removed in 2.22) alias of all.

If true do not get a cached copy.

Force the sending of the Basic authentication header upon initial request.

When this setting is false, this module will first try an unauthenticated request, and when the server replies with an HTTP 401 error, it will submit the Basic authentication header.

When this setting is true, this module will immediately send a Basic authentication header on the first request.

Use this setting in any of the following scenarios:

You know the webservice endpoint always requires HTTP Basic authentication, and you want to speed up your requests by eliminating the first roundtrip.

The web service does not properly send an HTTP 401 error to your client, so Ansible’s HTTP library will not properly respond with HTTP credentials, and logins will fail.

The webservice bans or rate-limits clients that cause any HTTP 401 errors.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

Add custom HTTP headers to a request in the format of a YAML hash. As of Ansible 2.3 supplying Content-Type here will override the header generated by supplying json or form-urlencoded for body_format.

Header to identify as, generally appears in web server logs.

Default: "ansible-httpget"

The HTTP method of the request or response.

In more recent versions we do not restrict the method at the module level anymore but it still must be a valid method accepted by the service handling the request.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

If false, the module will search for the src on the controller node.

If true, the module will search for the src on the managed (remote) node.

A filename, when it does not exist, this step will not be run.

Whether or not to return the body of the response as a “content” key in the dictionary result no matter it succeeded or failed.

Independently of this option, if the reported Content-Type is application/json, then the JSON is always loaded into a key called json in the dictionary results.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Path to file to be submitted to the remote server.

Cannot be used with body.

Should be used with force_basic_auth to ensure success when the remote end sends a 401.

list / elements=integer

A list of valid, numeric, HTTP status codes that signifies success of the request.

The socket level timeout in seconds

Path to Unix domain socket to use for connection.

list / elements=string

added in ansible-core 2.12

A list of header names that will not be sent on subsequent redirected requests. This list is case insensitive. By default all headers will be redirected. In some cases it may be beneficial to list headers such as Authorization here to avoid potential credential exposure.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

HTTP or HTTPS URL in the form (http|https)://host.domain[:port]/path.

A password for the module to use for Digest, Basic or WSSE authentication.

A username for the module to use for Digest, Basic or WSSE authentication.

added in ansible-core 2.11

Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

Requires the Python library gssapi to be installed.

Credentials for GSSAPI can be specified with url_username/url_password or with the GSSAPI env var KRB5CCNAME that specified a custom Kerberos credential cache.

NTLM authentication is not supported even if the GSSAPI mech for NTLM has been installed.

added in ansible-core 2.14

Determining whether to use credentials from ~/.netrc file.

By default .netrc is used with Basic authentication headers.

When false, .netrc credentials are ignored.

If false, it will not use a proxy, even if one is defined in an environment variable on the target hosts.

If false, SSL certificates will not be validated.

This should only set to false used on personally controlled sites using self-signed certificates.

Prior to 1.9.2 the code defaulted to false.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

The dependency on httplib2 was removed in Ansible 2.1.

The module returns all the HTTP headers in lower-case.

For Windows targets, use the ansible.windows.win_uri module instead.

Downloads files from HTTP, HTTPS, or FTP to node.

The official documentation on the ansible.windows.win_uri module.

Common return values are documented here, the following are the fields unique to this module:

The response body content.

Returned: status not in status_code or return_content is true

The cookie values placed in cookie jar.

Sample: {"SESSIONID": "[SESSIONID]"}

The value for future request Cookie headers.

Sample: "SESSIONID=[SESSIONID]"

The number of seconds that elapsed while performing the download.

The HTTP message from the request.

Sample: "OK (unknown bytes)"

destination file/path

Returned: dest is defined

Sample: "/path/to/file.txt"

Whether the request was redirected.

The HTTP status code from the request.

The actual URL used for the request.

Sample: "https://www.ansible.com/"

Romeo Theriault (@romeotheriault)

**Examples:**

Example 1 (unknown):
```unknown
- name: Check that you can connect (GET) to a page and it returns a status 200
  ansible.builtin.uri:
    url: http://www.example.com

- name: Check that a page returns successfully but fail if the word AWESOME is not in the page contents
  ansible.builtin.uri:
    url: http://www.example.com
    return_content: true
  register: this
  failed_when: "this is failed or 'AWESOME' not in this.content"

- name: Create a JIRA issue
  ansible.builtin.uri:
    url: https://your.jira.example.com/rest/api/2/issue/
    user: your_username
    password: your_pass
    method: POST
    body: "{{ lookup('ansible.builtin.file','issue.json') }}"
    force_basic_auth: true
    status_code: 201
    body_format: json

- name: Login to a form based webpage, then use the returned cookie to access the app in later tasks
  ansible.builtin.uri:
    url: https://your.form.based.auth.example.com/index.php
    method: POST
    body_format: form-urlencoded
    body:
      name: your_username
      password: your_password
      enter: Sign in
    status_code: 302
  register: login

- name: Login to a form based webpage using a list of tuples
  ansible.builtin.uri:
    url: https://your.form.based.auth.example.com/index.php
    method: POST
    body_format: form-urlencoded
    body:
    - [ name, your_username ]
    - [ password, your_password ]
    - [ enter, Sign in ]
    status_code: 302
  register: login

- name: Upload a file via multipart/form-multipart
  ansible.builtin.uri:
    url: https://httpbin.org/post
    method: POST
    body_format: form-multipart
    body:
      file1:
        filename: /bin/true
        mime_type: application/octet-stream
        multipart_encoding: base64
      file2:
        content: text based file content
        filename: fake.txt
        mime_type: text/plain
        multipart_encoding: 7or8bit
      text_form_field: value

- name: Connect to website using a previously stored cookie
  ansible.builtin.uri:
    url: https://your.form.based.auth.example.com/dashboard.php
    method: GET
    return_content: true
    headers:
      Cookie: "{{ login.cookies_string }}"

- name: Queue build of a project in Jenkins
  ansible.builtin.uri:
    url: http://{{ jenkins.host }}/job/{{ jenkins.job }}/build?token={{ jenkins.token }}
    user: "{{ jenkins.user }}"
    password: "{{ jenkins.password }}"
    method: GET
    force_basic_auth: true
    status_code: 201

- name: POST from contents of local file
  ansible.builtin.uri:
    url: https://httpbin.org/post
    method: POST
    src: file.json

- name: POST from contents of remote file
  ansible.builtin.uri:
    url: https://httpbin.org/post
    method: POST
    src: /path/to/my/file.json
    remote_src: true

- name: Create workspaces in Log analytics Azure
  ansible.builtin.uri:
    url: https://www.mms.microsoft.com/Embedded/Api/ConfigDataSources/LogManagementData/Save
    method: POST
    body_format: json
    status_code: [200, 202]
    return_content: true
    headers:
      Content-Type: application/json
      x-ms-client-workspace-path: /subscriptions/{{ sub_id }}/resourcegroups/{{ res_group }}/providers/microsoft.operationalinsights/workspaces/{{ w_spaces }}
      x-ms-client-platform: ibiza
      x-ms-client-auth-token: "{{ token_az }}"
    body:

- name: Pause play until a URL is reachable from this host
  ansible.builtin.uri:
    url: "http://192.0.2.1/some/test"
    follow_redirects: none
    method: GET
  register: _result
  until: _result.status == 200
  retries: 720 # 720 * 5 seconds = 1hour (60*60/5)
  delay: 5 # Every 5 seconds

- name: Provide SSL/TLS ciphers as a list
  uri:
    url: https://example.org
    ciphers:
      - '@SECLEVEL=2'
      - ECDH+AESGCM
      - ECDH+CHACHA20
      - ECDH+AES
      - DHE+AES
      - '!aNULL'
      - '!eNULL'
      - '!aDSS'
      - '!SHA1'
      - '!AESCCM'

- name: Provide SSL/TLS ciphers as an OpenSSL formatted cipher list
  uri:
    url: https://example.org
    ciphers: '@SECLEVEL=2:ECDH+AESGCM:ECDH+CHACHA20:ECDH+AES:DHE+AES:!aNULL:!eNULL:!aDSS:!SHA1:!AESCCM'
```

---

## ansible.builtin.memory cache – RAM backed, non persistent — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/memory_cache.html

**Contents:**
- ansible.builtin.memory cache – RAM backed, non persistent
- Synopsis
  - Authors
  - Collection links

This cache plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name memory. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.memory for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same cache plugin name.

RAM backed cache that is not persistent.

This is the default used if no other plugin is specified.

There are no options to configure.

core team (@ansible-core)

---

## ansible.builtin.dictsort filter – Sort a dict and yield. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dictsort_filter.html

**Contents:**
- ansible.builtin.dictsort filter – Sort a dict and yield.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name dictsort. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dictsort for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Sort a dict and yield.

This is the Jinja builtin filter plugin ‘dictsort’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.dictsort

---

## ansible.builtin.csvfile lookup – read data from a TSV or CSV file — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/csvfile_lookup.html

**Contents:**
- ansible.builtin.csvfile lookup – read data from a TSV or CSV file
- Synopsis
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name csvfile. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.csvfile for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

The csvfile lookup reads the contents of a file in CSV (comma-separated value) format. The lookup looks for the row where the first column matches keyname (which can be multiple words) and returns the value in the col column (default 1, which indexed from 0 means the second column in the file).

At least one keyname is required, provided as a positional argument(s) to the lookup.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.csvfile', key1=value1, key2=value2, ...) and query('ansible.builtin.csvfile', key1=value1, key2=value2, ...)

column to return (0 indexed).

what to return if the value is not found in the file.

field separator in the file, for a tab you can specify TAB or \t.

Encoding (character set) of the used CSV file.

name of the CSV/TSV file to open.

Default: "ansible.csv"

added in ansible-core 2.17

column to search in (0 indexed).

The default is for TSV files (tab delimited) not CSV (comma delimited) … yes the name is misleading.

As of version 2.11, the search parameter (text that must match the first column of the file) and filename parameter can be multi-word.

For historical reasons, in the search keyname, quotes are treated literally and cannot be used around the string unless they appear (escaped as required) in the first column of the file you are parsing.

Search paths used for relative files.

list / elements=string

value(s) stored in file column

Jan-Piet Mens (@jpmens) <jpmens(at)gmail.com>

**Examples:**

Example 1 (unknown):
```unknown
- name:  Match 'Li' on the first column, return the second column (0 based index)
  ansible.builtin.debug: msg="The atomic number of Lithium is {{ lookup('ansible.builtin.csvfile', 'Li file=elements.csv delimiter=,') }}"

- name: msg="Match 'Li' on the first column, but return the 3rd column (columns start counting after the match)"
  ansible.builtin.debug: msg="The atomic mass of Lithium is {{ lookup('ansible.builtin.csvfile', 'Li file=elements.csv delimiter=, col=2') }}"

# Contents of bgp_neighbors.csv
# 127.0.0.1,10.0.0.1,24,nones,lola,pepe,127.0.0.2
# 128.0.0.1,10.1.0.1,20,notes,lolita,pepito,128.0.0.2
# 129.0.0.1,10.2.0.1,23,nines,aayush,pepete,129.0.0.2

- name: Define values from CSV file, this reads file in one go, but you could also use col= to read each in it's own lookup.
  ansible.builtin.set_fact:
    '{{ columns[item|int] }}': "{{ csvline }}"
  vars:
    csvline: "{{ lookup('csvfile', bgp_neighbor_ip, file='bgp_neighbors.csv', delimiter=',', col=item) }}"
    columns: ['loop_ip', 'int_ip', 'int_mask', 'int_name', 'local_as', 'neighbour_as', 'neight_int_ip']
    bgp_neighbor_ip: '127.0.0.1'
  loop: '{{ range(columns|length|int) }}'
  delegate_to: localhost
  delegate_facts: true

# Contents of people.csv
# # Last,First,Email,Extension
# Smith,Jane,[email protected],1234

- name: Specify the column (by keycol) in which the string should be searched
  assert:
    that:
    - lookup('ansible.builtin.csvfile', 'Jane', file='people.csv', delimiter=',', col=0, keycol=1) == "Smith"

# Contents of debug.csv
# test1 ret1.1 ret2.1
# test2 ret1.2 ret2.2
# test3 ret1.3 ret2.3

- name: "Lookup multiple keynames in the first column (index 0), returning the values from the second column (index 1)"
  debug:
    msg: "{{ lookup('csvfile', 'test1', 'test2', file='debug.csv', delimiter=' ') }}"

- name: Lookup multiple keynames using old style syntax
  debug:
    msg: "{{ lookup('csvfile', term1, term2) }}"
  vars:
    term1: "test1 file=debug.csv delimiter=' '"
    term2: "test2 file=debug.csv delimiter=' '"
```

---

## ansible.builtin.match test – Does string match regular expression from the start — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/match_test.html

**Contents:**
- ansible.builtin.match test – Does string match regular expression from the start
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name match. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.match for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Compare string against regular expression using Python’s match function, this means the regex is automatically anchored at the start of the string.

This describes the input of the test, the value before is ansible.builtin.match or is not ansible.builtin.match.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.match(key1=value1, key2=value2, ...) and input is not ansible.builtin.match(key1=value1, key2=value2, ...)

Use case insensitive matching.

Match against multiple lines in string.

Regex to match against.

Returns True if there is a match, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
url: "https://example.com/users/foo/resources/bar"
foundmatch: url is match("https://example.com/users/.*/resources")
nomatch: url is match("/users/.*/resources")
```

---

## ansible.builtin.divisibleby test – Check if a variable is divisible by a number. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/divisibleby_test.html

**Contents:**
- ansible.builtin.divisibleby test – Check if a variable is divisible by a number.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name divisibleby. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.divisibleby for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if a variable is divisible by a number.

This is the Jinja builtin test plugin ‘divisibleby’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.divisibleby

---

## ansible.builtin.win_dirname filter – Get a Windows path’s directory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/win_dirname_filter.html

**Contents:**
- ansible.builtin.win_dirname filter – Get a Windows path’s directory
- Synopsis
- Input
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name win_dirname. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.win_dirname for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns the directory component of a Windows path, what is left in the string that is not ‘win_basename’.

While specifying an UNC (Universal Naming Convention) path, please make sure the path conforms to the UNC path syntax.

This describes the input of the filter, the value before | ansible.builtin.win_dirname.

Get a Windows path’s base name.

The directory from the Windows path provided.

**Examples:**

Example 1 (unknown):
```unknown
# To get the last name of a file Windows path, like 'C:\users\asdf' out of 'C:\Users\asdf\foo.txt'
{{ mypath | win_dirname }}

# Get dirname from the UNC path in the form of '\\<SERVER_NAME>\<SHARE_NAME>\<FILENAME.FILE_EXTENSION>'
# like '\\server1\test\foo.txt' returns '\\\\server1\\test\\'
filename: "{{ mypath | win_dirname }}"
```

---

## ansible.builtin.fileglob lookup – list files matching a pattern — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/fileglob_lookup.html

**Contents:**
- ansible.builtin.fileglob lookup – list files matching a pattern
- Synopsis
- Terms
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name fileglob. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.fileglob for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Matches all files in a single directory, non-recursively, that match a pattern. It calls Python’s “glob” library.

path(s) of files to read

Patterns are only supported on files, not directory/paths.

See Ansible task paths to understand how file lookup occurs with paths.

Matching is against local system files on the Ansible controller. To iterate a list of files on a remote node, use the ansible.builtin.find module.

Returns a string list of paths joined by commas, or an empty list if no files match. For a ‘true list’ pass wantlist=True to the lookup.

Search paths used for relative files.

**Examples:**

Example 1 (unknown):
```unknown
- name: Display paths of all .txt files in dir
  ansible.builtin.debug: msg={{ lookup('ansible.builtin.fileglob', '/my/path/*.txt') }}

- name: Copy each file over that matches the given pattern
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: "/etc/fooapp/"
    owner: "root"
    mode: 0600
  with_fileglob:
    - "/playbooks/files/fooapp/*"
```

---

## ansible.builtin.unvault lookup – read vaulted file(s) contents — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/unvault_lookup.html

**Contents:**
- ansible.builtin.unvault lookup – read vaulted file(s) contents
- Synopsis
- Terms
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name unvault. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.unvault for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

New in ansible-base 2.10

This lookup returns the contents from vaulted (or not) file(s) on the Ansible controller’s file system.

path(s) of files to read

This lookup does not understand ‘globbing’ nor shell environment variables.

Search paths used for relative files.

content of file(s) as bytes

**Examples:**

Example 1 (unknown):
```unknown
- ansible.builtin.debug: msg="the value of foo.txt is {{ lookup('ansible.builtin.unvault', '/etc/foo.txt') | string | trim }}"
```

---

## ansible.builtin.expanduser filter – Returns a path with ~ translation. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/expanduser_filter.html

**Contents:**
- ansible.builtin.expanduser filter – Returns a path with ~ translation.
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name expanduser. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.expanduser for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Translates ~ in a path to the proper user’s home directory.

This describes the input of the filter, the value before | ansible.builtin.expanduser.

A string that contains a path.

**Examples:**

Example 1 (unknown):
```unknown
# To get '/home/myuser/stuff.txt' from '~/stuff.txt'.
{{ mypath | expanduser }}
```

---

## ansible.builtin.password lookup – retrieve or generate a random password, stored in a file — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/password_lookup.html

**Contents:**
- ansible.builtin.password lookup – retrieve or generate a random password, stored in a file
- Synopsis
- Terms
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name password. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.password for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Generates a random plaintext password and stores it in a file at a given filepath.

If the file exists previously, it will retrieve its contents, behaving just like with_file.

Usage of variables like "{{ inventory_hostname }}" in the filepath can be used to set up random passwords per host, which simplifies password management in "host_vars" variables.

A special case is using /dev/null as a path. The password lookup will generate a new random password each time, but will not write it to /dev/null. This can be used when you need a password without storing it on the controller.

path to the file that stores/will store the passwords

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.password', key1=value1, key2=value2, ...) and query('ansible.builtin.password', key1=value1, key2=value2, ...)

list / elements=string

A list of names that compose a custom character set in the generated passwords.

This parameter defines the possible character sets in the resulting password, not the required character sets. If you want to require certain character sets for passwords, you can use the community.general.random_string lookup plugin.

By default generated passwords contain a random mix of upper and lowercase ASCII letters, the numbers 0-9, and punctuation (”. , : - _”).

They can be either parts of Python’s string module attributes or represented literally ( :, -).

Though string modules can vary by Python version, valid values for both major releases include: ‘ascii_lowercase’, ‘ascii_uppercase’, ‘digits’, ‘hexdigits’, ‘octdigits’, ‘printable’, ‘punctuation’ and ‘whitespace’.

Be aware that Python’s ‘hexdigits’ includes lower and upper case versions of a-f, so it is not a good choice as it doubles the chances of those values for systems that won’t distinguish case, distorting the expected entropy.

when using a comma separated string, to enter comma use two commas ‘,,’ somewhere - preferably at the end. Quotes and double quotes are not supported.

Default: ["ascii_letters", "digits", ".,:-_"]

Which hash scheme to encrypt the returning password, should be one hash scheme from passlib.hash; md5_crypt, bcrypt, sha256_crypt, sha512_crypt.

If not provided, the password will be returned in plain text.

Note that the password is always stored as plain text, only the returning password is encrypted.

Encrypt also forces saving the salt value for idempotence.

Note that before 2.6 this option was incorrectly labeled as a boolean for a long time.

added in ansible-core 2.12

Specify version of Bcrypt algorithm to be used while using encrypt as bcrypt.

The parameter is only available for bcrypt - https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html#passlib.hash.bcrypt.

Other hash types will simply ignore this parameter.

Valid values for this parameter are: 2, 2a, 2y, 2b.

The length of the generated password.

added in ansible-core 2.12

A seed to initialize the random number generator.

Identical seeds will yield identical passwords.

Use this for random-but-idempotent password generation.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.password', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.password', term1, term2, key1=value1, key2=value2)

A great alternative to the password lookup plugin, if you don’t need to generate random passwords on a per-host basis, would be to use Vault in playbooks. Read the documentation there and consider using it first, it will be more desirable for most applications.

If the file already exists, no data will be written to it. If the file has contents, those contents will be read in as the password. Empty files cause the password to return as an empty string.

As all lookups, this runs on the Ansible host as the user running the playbook, and “become” does not apply, the target file must be readable by the playbook user, or, if it does not exist, the playbook user must have sufficient privileges to create it. (So, for example, attempts to write into areas such as /etc will fail unless the entire playbook is being run as root).

list / elements=string

Daniel Hokka Zakrisson

**Examples:**

Example 1 (unknown):
```unknown
- name: create a mysql user with a random password
  community.mysql.mysql_user:
    name: "{{ client }}"
    password: "{{ lookup('ansible.builtin.password', 'credentials/' + client + '/' + tier + '/' + role + '/mysqlpassword', length=15) }}"
    priv: "{{ client }}_{{ tier }}_{{ role }}.*:ALL"

- name: create a mysql user with a random password using only ascii letters
  community.mysql.mysql_user:
    name: "{{ client }}"
    password: "{{ lookup('ansible.builtin.password', '/tmp/passwordfile', chars=['ascii_letters']) }}"
    priv: '{{ client }}_{{ tier }}_{{ role }}.*:ALL'

- name: create a mysql user with an 8 character random password using only digits
  community.mysql.mysql_user:
    name: "{{ client }}"
    password: "{{ lookup('ansible.builtin.password', '/tmp/passwordfile', length=8, chars=['digits']) }}"
    priv: "{{ client }}_{{ tier }}_{{ role }}.*:ALL"

- name: create a mysql user with a random password using many different char sets
  community.mysql.mysql_user:
    name: "{{ client }}"
    password: "{{ lookup('ansible.builtin.password', '/tmp/passwordfile', chars=['ascii_letters', 'digits', 'punctuation']) }}"
    priv: "{{ client }}_{{ tier }}_{{ role }}.*:ALL"

- name: create lowercase 8 character name for Kubernetes pod name
  ansible.builtin.set_fact:
    random_pod_name: "web-{{ lookup('ansible.builtin.password', '/dev/null', chars=['ascii_lowercase', 'digits'], length=8) }}"

- name: create random but idempotent password
  ansible.builtin.set_fact:
    password: "{{ lookup('ansible.builtin.password', '/dev/null', seed=inventory_hostname) }}"
```

---

## ansible.builtin.to_json filter – Convert variable to JSON string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/to_json_filter.html

**Contents:**
- ansible.builtin.to_json filter – Convert variable to JSON string
- Synopsis
- Input
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name to_json. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.to_json for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts an Ansible variable into a JSON string representation.

This filter functions as a wrapper to the Python json.dumps function.

Ansible internally auto-converts JSON strings into variable structures so this plugin is used to force it into a JSON string.

This describes the input of the filter, the value before | ansible.builtin.to_json.

A variable or expression that returns a data structure.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.to_json(key1=value1, key2=value2, ...)

When False, out-of-range float values nan, inf and -inf will result in an error.

When True, out-of-range float values will be represented using their JavaScript equivalents, NaN, Infinity and -Infinity.

Controls the usage of the internal circular reference detection, if off can result in overflow errors.

Escapes all non ASCII characters.

Number of spaces to indent Python structures, mainly used for display to humans.

Toggle to represent unsafe values directly in JSON or create a unsafe object in JSON.

list / elements=string

The item and key separator to be used in the serialized output, default may change depending on indent and Python version.

Default: [", ", ": "]

If True, keys that are not basic Python types will be skipped.

Affects sorting of dictionary keys.

Toggle to either unvault a vault or create the JSON version of a vaulted object.

Both vault_to_text and preprocess_unsafe defaulted to False between Ansible 2.9 and 2.12.

These parameters to json.dumps will be ignored, as they are overridden internally: cls, default

The JSON serialized string representing the variable structure inputted.

**Examples:**

Example 1 (unknown):
```unknown
# dump variable in a template to create a JSON document
{{ docker_config | to_json }}

# same as above but 'prettier' (equivalent to to_nice_json filter)
{{ docker_config | to_json(indent=4, sort_keys=True) }}
```

---

## ansible.builtin.urn test – is the string a valid URN — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/urn_test.html

**Contents:**
- ansible.builtin.urn test – is the string a valid URN
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name urn. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.urn for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-core 2.14

Validates that the input string conforms to the URN standard.

This describes the input of the test, the value before is ansible.builtin.urn or is not ansible.builtin.urn.

Returns true if the string is a URN and false if it is not.

**Examples:**

Example 1 (unknown):
```unknown
# ISBN in URN format
{{ 'urn:isbn:9780302376463' is urn }}
# this is URL/URI but not URN
{{ 'mailto://[email protected]' is not urn }}
```

---

## ansible.builtin.async_status module – Obtain status of asynchronous task — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/async_status_module.html

**Contents:**
- ansible.builtin.async_status module – Obtain status of asynchronous task
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name async_status even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.async_status for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module gets the status of an asynchronous task.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

Job or task identifier

If status, obtain the status.

If cleanup, clean up the async job cache (by default in ~/.ansible_async/) for the specified job jid, without waiting for it to finish.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

added in ansible-core 2.17

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Platforms: posix, windows

Target OS/families that can be operated against

The started and finished return values were updated to return True or False instead of 1 or 0 in ansible-core 2.19.

Detailed information on how to use asynchronous actions and polling.

Common return values are documented here, the following are the fields unique to this module:

The asynchronous job id

Sample: "360874038559.4169"

Path to erased job file

Returned: when file is erased

Whether the asynchronous job has finished or not

Whether the asynchronous job has started or not

Any errors returned by async_wrapper

Any output returned by async_wrapper

**Examples:**

Example 1 (unknown):
```unknown
---
- name: Asynchronous dnf task
  ansible.builtin.dnf:
    name: docker-io
    state: present
  async: 1000
  poll: 0
  register: dnf_sleeper

- name: Wait for asynchronous job to end
  ansible.builtin.async_status:
    jid: '{{ dnf_sleeper.ansible_job_id }}'
  register: job_result
  until: job_result is finished
  retries: 100
  delay: 10

- name: Clean up async file
  ansible.builtin.async_status:
    jid: '{{ dnf_sleeper.ansible_job_id }}'
    mode: cleanup
```

---

## ansible.builtin.callable test – Return whether the object is callable. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/callable_test.html

**Contents:**
- ansible.builtin.callable test – Return whether the object is callable.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name callable. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.callable for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return whether the object is callable.

This is the Jinja builtin test plugin ‘callable’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.callable

---

## ansible.builtin.group_by module – Create Ansible groups based on facts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/group_by_module.html

**Contents:**
- ansible.builtin.group_by module – Create Ansible groups based on facts
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name group_by even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.group_by for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Use facts to create ad-hoc groups that can be used later in a playbook.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

The variables whose values will be used as groups.

list / elements=string

The list of the parent groups.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

These tasks ignore the loop and with_ keywords

While this makes no changes to target systems the ‘in memory’ inventory will still be altered

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

While parts of this action are implemented in core, other parts are still available as normal plugins and can be partially overridden

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

Spaces in group names are converted to dashes ‘-’.

Though this module does not change the remote host, we do provide ‘changed’ status as it can be useful for those trying to track inventory changes.

Add a host (and alternatively a group) to the ansible-playbook in-memory inventory.

Jeroen Hoekx (@jhoekx)

**Examples:**

Example 1 (unknown):
```unknown
- name: Create groups based on the machine architecture
  ansible.builtin.group_by:
    key: machine_{{ ansible_machine }}

- name: Create groups like 'virt_kvm_host'
  ansible.builtin.group_by:
    key: virt_{{ ansible_virtualization_type }}_{{ ansible_virtualization_role }}

- name: Create nested groups
  ansible.builtin.group_by:
    key: el{{ ansible_distribution_major_version }}-{{ ansible_architecture }}
    parents:
      - el{{ ansible_distribution_major_version }}

- name: Add all active hosts to a static group
  ansible.builtin.group_by:
    key: done
```

---

## ansible.builtin.capitalize filter – Capitalize a value. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/capitalize_filter.html

**Contents:**
- ansible.builtin.capitalize filter – Capitalize a value.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name capitalize. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.capitalize for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

This is the Jinja builtin filter plugin ‘capitalize’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.capitalize

---

## ansible.builtin.integer test – Return true if the object is an integer. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/integer_test.html

**Contents:**
- ansible.builtin.integer test – Return true if the object is an integer.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name integer. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.integer for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is an integer.

This is the Jinja builtin test plugin ‘integer’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.integer

---

## ansible.builtin.trim filter – Strip leading and trailing characters, by default whitespace. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/trim_filter.html

**Contents:**
- ansible.builtin.trim filter – Strip leading and trailing characters, by default whitespace.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name trim. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.trim for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Strip leading and trailing characters, by default whitespace.

This is the Jinja builtin filter plugin ‘trim’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.trim

---

## ansible.builtin.assert module – Asserts given expressions are true — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/assert_module.html

**Contents:**
- ansible.builtin.assert module – Asserts given expressions are true
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name assert even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.assert for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module asserts that given expressions are true with an optional custom message.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

The customized message used for a failing assertion.

This argument was called msg before Ansible 2.7, now it is renamed to fail_msg with alias msg.

Set this to true to avoid verbose output.

The customized message used for a successful assertion.

list / elements=string / required

A list of string expressions of the same form that can be passed to the when statement.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

Aside from register and/or in combination with delegate_facts, it has little effect.

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Print statements during execution.

Fail with custom message.

Execute Ansible ‘actions’.

**Examples:**

Example 1 (unknown):
```unknown
- name: A single condition can be supplied as string instead of list
  ansible.builtin.assert:
    that: "ansible_os_family != 'RedHat'"

- name: Use yaml multiline strings to ease escaping
  ansible.builtin.assert:
    that:
      - "'foo' in some_command_result.stdout"
      - number_of_the_counting == 3
      - >
        "reject" not in some_command_result.stderr

- name: After version 2.7 both O(msg) and O(fail_msg) can customize failing assertion message
  ansible.builtin.assert:
    that:
      - my_param <= 100
      - my_param >= 0
    fail_msg: "'my_param' must be between 0 and 100"
    success_msg: "'my_param' is between 0 and 100"

- name: Please use O(msg) when ansible version is smaller than 2.7
  ansible.builtin.assert:
    that:
      - my_param <= 100
      - my_param >= 0
    msg: "'my_param' must be between 0 and 100"

- name: Use quiet to avoid verbose output
  ansible.builtin.assert:
    that:
      - my_param <= 100
      - my_param >= 0
    quiet: true
```

---

## Downloading collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_downloading.html

**Contents:**
- Downloading collections

To download a collection and its dependencies for an offline install, run ansible-galaxy collection download. This downloads the collections specified and their dependencies to the specified folder and creates a requirements.yml file which can be used to install those collections on a host without access to a Galaxy server. All the collections are downloaded by default to the ./collections folder.

Just like the install command, the collections are sourced based on the configured galaxy server config. Even if a collection to download was specified by a URL or path to a tarball, the collection will be re-downloaded from the configured Galaxy server.

Collections can be specified as one or multiple collections or with a requirements.yml file just like ansible-galaxy collection install.

To download a single collection and its dependencies:

To download a single collection at a specific version:

To download multiple collections either specify multiple collections as command line arguments as shown above or use a requirements file in the format documented with Install multiple collections with a requirements file.

You can also download a source collection directory. The collection is built with the mandatory galaxy.yml file.

You can download multiple source collections from a single namespace by providing the path to the namespace.

All the collections are downloaded by default to the ./collections folder but you can use -p or --download-path to specify another path:

Once you have downloaded the collections, the folder contains the collections specified, their dependencies, and a requirements.yml file. You can use this folder as is with ansible-galaxy collection install to install the collections on a host without access to a Galaxy server.

**Examples:**

Example 1 (unknown):
```unknown
ansible-galaxy collection download my_namespace.my_collection
```

Example 2 (unknown):
```unknown
ansible-galaxy collection download my_namespace.my_collection:1.0.0
```

Example 3 (unknown):
```unknown
ansible-galaxy collection download -r requirements.yml
```

Example 4 (unknown):
```unknown
ansible-galaxy collection download /path/to/collection

ansible-galaxy collection download git+file:///path/to/collection/.git
```

---

## ansible.builtin.test test – Check if a test exists by name. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/test_test.html

**Contents:**
- ansible.builtin.test test – Check if a test exists by name.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name test. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.test for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if a test exists by name.

This is the Jinja builtin test plugin ‘test’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.test

---

## ansible.builtin.ge test – Same as a >= b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ge_test.html

**Contents:**
- ansible.builtin.ge test – Same as a >= b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ge. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ge for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘ge’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.ge

---

## ansible.builtin.items lookup – list of items — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/items_lookup.html

**Contents:**
- ansible.builtin.items lookup – list of items
- Synopsis
- Terms
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name items. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.items for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

this lookup returns a list of items given to it, if any of the top level items is also a list it will flatten it, but it will not recurse

this is the standard lookup used for loops in most examples

check out the ‘flattened’ lookup for recursive flattening

if you do not want flattening nor any other transformation look at the ‘list’ lookup.

list / elements=string

**Examples:**

Example 1 (unknown):
```unknown
- name: "loop through list"
  ansible.builtin.debug:
    msg: "An item: {{ item }}"
  with_items:
    - 1
    - 2
    - 3

- name: add several users
  ansible.builtin.user:
    name: "{{ item }}"
    groups: "wheel"
    state: present
  with_items:
     - testuser1
     - testuser2

- name: "loop through list from a variable"
  ansible.builtin.debug:
    msg: "An item: {{ item }}"
  with_items: "{{ somelist }}"

- name: more complex items to add several users
  ansible.builtin.user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
    groups: "{{ item.groups }}"
    state: present
  with_items:
     - { name: testuser1, uid: 1002, groups: "wheel, staff" }
     - { name: testuser2, uid: 1003, groups: staff }
```

---

## ansible.builtin.max filter – Return the largest item from the sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/max_filter.html

**Contents:**
- ansible.builtin.max filter – Return the largest item from the sequence.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name max. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.max for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the largest item from the sequence.

This is the Jinja builtin filter plugin ‘max’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.max

---

## ansible.builtin.regex test – Does string match regular expression from the start — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/regex_test.html

**Contents:**
- ansible.builtin.regex test – Does string match regular expression from the start
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name regex. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.regex for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Compare string against regular expression using Python’s match or search functions.

This describes the input of the test, the value before is ansible.builtin.regex or is not ansible.builtin.regex.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.regex(key1=value1, key2=value2, ...) and input is not ansible.builtin.regex(key1=value1, key2=value2, ...)

Use case insensitive matching.

Decide which function to be used to do the matching.

Match against multiple lines in string.

Regex to match against.

Returns True if there is a match, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
url: "https://example.com/users/foo/resources/bar"
foundmatch: url is regex("example\.com/\w+/foo")
```

---

## ansible.builtin.upper test – Return true if the variable is uppercased. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/upper_test.html

**Contents:**
- ansible.builtin.upper test – Return true if the variable is uppercased.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name upper. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.upper for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is uppercased.

This is the Jinja builtin test plugin ‘upper’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.upper

---

## ansible.builtin.false test – Return true if the object is False. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/false_test.html

**Contents:**
- ansible.builtin.false test – Return true if the object is False.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name false. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.false for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the object is False.

This is the Jinja builtin test plugin ‘false’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.false

---

## ansible.builtin.dict lookup – returns key/value pair items from dictionaries — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dict_lookup.html

**Contents:**
- ansible.builtin.dict lookup – returns key/value pair items from dictionaries
- Synopsis
- Terms
- Examples
- Return Value
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name dict. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dict for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Takes dictionaries as input and returns a list with each item in the list being a dictionary with ‘key’ and ‘value’ as keys to the previous dictionary’s structure.

A list of dictionaries

list / elements=string

list of composed dictionaries with key and value

**Examples:**

Example 1 (unknown):
```unknown
vars:
  users:
    alice:
      name: Alice Appleworth
      telephone: 123-456-7890
    bob:
      name: Bob Bananarama
      telephone: 987-654-3210
tasks:
  # with predefined vars
  - name: Print phone records
    ansible.builtin.debug:
      msg: "User {{ item.key }} is {{ item.value.name }} ({{ item.value.telephone }})"
    loop: "{{ lookup('ansible.builtin.dict', users) }}"
  # with inline dictionary
  - name: show dictionary
    ansible.builtin.debug:
      msg: "{{item.key}}: {{item.value}}"
    with_dict: {a: 1, b: 2, c: 3}
  # Items from loop can be used in when: statements
  - name: set_fact when alice in key
    ansible.builtin.set_fact:
      alice_exists: true
    loop: "{{ lookup('ansible.builtin.dict', users) }}"
    when: "'alice' in item.key"
```

---

## ansible.builtin.uri test – is the string a valid URI — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/uri_test.html

**Contents:**
- ansible.builtin.uri test – is the string a valid URI
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name uri. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.uri for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-core 2.14

Validates that the input string conforms to the URI standard, optionally that is also in the list of schemas provided.

This describes the input of the test, the value before is ansible.builtin.uri or is not ansible.builtin.uri.

This describes keyword parameters of the test. These are the values key1=value1, key2=value2 and so on in the following examples: input is ansible.builtin.uri(key1=value1, key2=value2, ...) and input is not ansible.builtin.uri(key1=value1, key2=value2, ...)

list / elements=string

Subset of URI schemas to validate against, otherwise any scheme is considered valid.

Returns false if the string is not a URI or the schema extracted does not match the supplied list.

**Examples:**

Example 1 (unknown):
```unknown
# URLs are URIs
{{ 'http://example.com' is uri }}
# but not all URIs are URLs
{{ 'mailto://[email protected]' is uri }}
# looking only for file transfers URIs
{{ 'mailto://[email protected]' is not uri(schemes=['ftp', 'ftps', 'sftp', 'file']) }}
# make sure URL conforms to the 'special schemas'
{{ 'http://nobody:[email protected]' is uri(['ftp', 'ftps', 'http', 'https', 'ws', 'wss']) }}
```

---

## ansible.builtin.pip module – Manages Python library dependencies — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/pip_module.html

**Contents:**
- ansible.builtin.pip module – Manages Python library dependencies
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name pip even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.pip for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Manage Python library dependencies. To use this module, one of the following keys is required: name or requirements.

The below requirements are needed on the host that executes this module.

setuptools or packaging

break_system_packages

added in ansible-core 2.17

Allow pip to modify an externally-managed Python installation as defined by PEP 668.

This is typically required when installing packages outside a virtual environment on modern systems.

cd into this directory before running the command.

Pass the editable flag.

The explicit executable or pathname for the pip executable, if different from the Ansible Python interpreter. For example pip3.13, if there are multiple Python installations in the system and you want to run pip for the Python 3.13 installation.

Mutually exclusive with virtualenv (added in 2.1).

Does not affect the Ansible Python interpreter.

The setuptools package must be installed for both the Ansible Python interpreter and for the version of Python specified by this option.

Extra arguments passed to pip.

list / elements=string

The name of a Python library to install or the url(bzr+,hg+,git+,svn+) of the remote package.

This can be a list (since 2.2) and contain version specifiers (since 2.7).

The path to a pip requirements file, which should be local to the remote system. File can be specified as a relative path if using the chdir option.

The forcereinstall option is only available in Ansible 2.1 and above.

"present" ← (default)

The system umask to apply before installing the pip package. This is useful, for example, when installing on systems that have a very restrictive umask by default (e.g., 0077) and you want to pip install packages which are to be used by all users. Note that this requires you to specify desired umask mode as an octal string, (e.g., 0022).

The version number to install of the Python library specified in the name parameter.

An optional path to a virtualenv directory to install into. It cannot be specified together with the executable parameter (added in 2.1). If the virtualenv does not exist, it will be created before installing packages. The optional virtualenv_site_packages, virtualenv_command, and virtualenv_python options affect the creation of the virtualenv.

The command or a pathname to the command to create the virtual environment with. For example pyvenv, virtualenv, virtualenv2, ~/bin/virtualenv, /usr/local/bin/virtualenv.

Default: "virtualenv"

The Python executable used for creating the virtual environment. For example python3.13. When not specified, the Python version used to run the ansible module is used. This parameter should not be used when virtualenv_command is using pyvenv or the -m venv module.

virtualenv_site_packages

Whether the virtual environment will inherit packages from the global site-packages directory. Note that if this setting is changed on an already existing virtual environment it will not have any effect, the environment must be deleted and newly created.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Python installations marked externally-managed (as defined by PEP668) cannot be updated by pip versions >= 23.0.1 without the use of a virtual environment or setting the break_system_packages option.

The virtualenv (http://www.virtualenv.org/) must be installed on the remote host if the virtualenv parameter is specified and the virtualenv needs to be created.

Although it executes using the Ansible Python interpreter, the pip module shells out to run the actual pip command, so it can use any pip version you specify with executable. By default, it uses the pip version for the Ansible Python interpreter.

The interpreter used by Ansible (see ansible_python_interpreter) requires the setuptools package, regardless of the version of pip set with the executable option.

Common return values are documented here, the following are the fields unique to this module:

pip command used by the module

Sample: "pip2 install ansible six"

list / elements=string

list of python modules targeted by pip

Sample: ["ansible", "six"]

Path to the requirements file

Returned: success, if a requirements file was provided

Sample: "/srv/git/project/requirements.txt"

Version of the package specified in ‘name’

Returned: success, if a name and version were provided

Path to the virtualenv

Returned: success, if a virtualenv path was provided

Sample: "/tmp/virtualenv"

Matt Wright (@mattupstate)

**Examples:**

Example 1 (unknown):
```unknown
- name: Install bottle python package
  ansible.builtin.pip:
    name: bottle

- name: Install bottle python package on version 0.11
  ansible.builtin.pip:
    name: bottle==0.11

- name: Install bottle python package with version specifiers
  ansible.builtin.pip:
    name: bottle>0.10,<0.20,!=0.11

- name: Install multi python packages with version specifiers
  ansible.builtin.pip:
    name:
      - django>1.11.0,<1.12.0
      - bottle>0.10,<0.20,!=0.11

- name: Install python package using a proxy
  ansible.builtin.pip:
    name: six
  environment:
    http_proxy: 'http://127.0.0.1:8080'
    https_proxy: 'https://127.0.0.1:8080'

# You do not have to supply '-e' option in extra_args
- name: Install MyApp using one of the remote protocols (bzr+,hg+,git+,svn+)
  ansible.builtin.pip:
    name: svn+http://myrepo/svn/MyApp#egg=MyApp

- name: Install MyApp using one of the remote protocols (bzr+,hg+,git+)
  ansible.builtin.pip:
    name: git+http://myrepo/app/MyApp

- name: Install MyApp from local tarball
  ansible.builtin.pip:
    name: file:///path/to/MyApp.tar.gz

- name: Install bottle into the specified (virtualenv), inheriting none of the globally installed modules
  ansible.builtin.pip:
    name: bottle
    virtualenv: /my_app/venv

- name: Install bottle into the specified (virtualenv), inheriting globally installed modules
  ansible.builtin.pip:
    name: bottle
    virtualenv: /my_app/venv
    virtualenv_site_packages: yes

- name: Install bottle into the specified (virtualenv), using Python 3.13
  ansible.builtin.pip:
    name: bottle
    virtualenv: /my_app/venv
    virtualenv_command: virtualenv-3.13

- name: Install bottle within a user home directory
  ansible.builtin.pip:
    name: bottle
    extra_args: --user

- name: Install specified python requirements
  ansible.builtin.pip:
    requirements: /my_app/requirements.txt

- name: Install specified python requirements in indicated (virtualenv)
  ansible.builtin.pip:
    requirements: /my_app/requirements.txt
    virtualenv: /my_app/venv

- name: Install specified python requirements and custom Index URL
  ansible.builtin.pip:
    requirements: /my_app/requirements.txt
    extra_args: -i https://example.com/pypi/simple

- name: Install specified python requirements offline from a local directory with downloaded packages
  ansible.builtin.pip:
    requirements: /my_app/requirements.txt
    extra_args: "--no-index --find-links=file:///my_downloaded_packages_dir"

- name: Install bottle for Python 3.13 specifically, using the 'pip3.13' executable
  ansible.builtin.pip:
    name: bottle
    executable: pip3.13

- name: Install bottle, forcing reinstallation if it's already installed
  ansible.builtin.pip:
    name: bottle
    state: forcereinstall

- name: Install bottle while ensuring the umask is 0022 (to ensure other users can use it)
  ansible.builtin.pip:
    name: bottle
    umask: "0022"
  become: True

- name: Run a module inside a virtual environment
  block:
    - name: Ensure the virtual environment exists
      pip:
        name: psutil
        virtualenv: "{{ venv_dir }}"
        # On Debian-based systems the correct python*-venv package must be installed to use the `venv` module.
        virtualenv_command: "{{ ansible_python_interpreter }} -m venv"

    - name: Run a module inside the virtual environment
      wait_for:
        port: 22
      vars:
        # Alternatively, use a block to affect multiple tasks, or use set_fact to affect the remainder of the playbook.
        ansible_python_interpreter: "{{ venv_python }}"

  vars:
    venv_dir: /tmp/pick-a-better-venv-path
    venv_python: "{{ venv_dir }}/bin/python"
```

---

## ansible.builtin.hash filter – hash of input data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/hash_filter.html

**Contents:**
- ansible.builtin.hash filter – hash of input data
- Synopsis
- Input
- Keyword parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name hash. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.hash for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a configurable hash of the input data. Uses SHA-1 by default.

This describes the input of the filter, the value before | ansible.builtin.hash.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.hash(key1=value1, key2=value2, ...)

Type of algorithm to produce the hash.

The list of available choices depends on the installed Python’s hashlib.

The checksum of the input, as configured in hashtype.

**Examples:**

Example 1 (javascript):
```javascript
# sha1_hash => "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"
sha1_hash: {{ 'test2' | hash('sha1') }}
# md5 => "5a105e8b9d40e1329780d62ea2265d8a"
md5: {{ 'test2' | hash('md5') }}
```

---

## ansible.builtin.reachable test – Task did not end due to unreachable host — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/reachable_test.html

**Contents:**
- ansible.builtin.reachable test – Task did not end due to unreachable host
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name reachable. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.reachable for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task was able to reach the host for execution

This test checks for the existence of a unreachable key in the input dictionary and that it is False if present

This describes the input of the test, the value before is ansible.builtin.reachable or is not ansible.builtin.reachable.

dictionary / required

registered result from an Ansible task

Returns True if the task did not flag the host as unreachable, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is reachable }}
```

---

## ansible.builtin.sequence test – Return true if the variable is a sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sequence_test.html

**Contents:**
- ansible.builtin.sequence test – Return true if the variable is a sequence.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sequence. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sequence for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Return true if the variable is a sequence.

This is the Jinja builtin test plugin ‘sequence’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.sequence

---

## ansible.builtin.unarchive module – Unpacks an archive after (optionally) copying it from the local machine — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/unarchive_module.html

**Contents:**
- ansible.builtin.unarchive module – Unpacks an archive after (optionally) copying it from the local machine
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name unarchive even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.unarchive for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.unarchive module unpacks an archive. It will not unpack a compressed file that does not contain an archive.

By default, it will copy the source file from the local system to the target before unpacking.

Set remote_src=yes to unpack an archive which already exists on the target.

If checksum validation is desired, use ansible.builtin.get_url or ansible.builtin.uri instead to fetch the file and set remote_src=yes.

For Windows targets, use the community.windows.win_unzip module instead.

This module has a corresponding action plugin.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

If true, the file is copied from local controller to the managed (remote) node, otherwise, the plugin will look for src archive on the managed machine.

This option has been deprecated in favor of remote_src.

This option is mutually exclusive with remote_src.

If the specified absolute path (file or directory) already exists, this step will not be run.

The specified absolute path (file or directory) must be below the base path given with dest.

This option controls the auto-decryption of source files using vault.

Remote absolute path where the archive should be unpacked.

The given path must exist. Base directory is not created by this module.

list / elements=string

List the directory and file entries that you would like to exclude from the unarchive action.

Mutually exclusive with include.

list / elements=string

Specify additional options by passing in an array.

Each space-separated command-line option should be a new element of the array. See examples.

Command-line options with multiple elements must use multiple lines in the array, one for each element.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

list / elements=string

added in ansible-core 2.11

List of directory and file entries that you would like to extract from the archive. If include is not empty, only files listed here will be extracted.

Mutually exclusive with exclude.

added in ansible-core 2.12

Size of the volatile memory buffer that is used for extracting files from the archive in bytes.

Do not replace existing files that are newer than files from the archive.

If set to True, return the list of files that are contained in the tarball.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

Set to true to indicate the archived file is already on the remote system and not local to the Ansible controller.

This option is mutually exclusive with copy.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

If remote_src=no (default), local path to archive file to copy to the target server; can be absolute or relative. If remote_src=yes, path on the target server to existing archive file to unpack.

If remote_src=yes and src contains ://, the remote machine will download the file from the URL first. (version_added 2.0). This is only for simple cases, for full download support use the ansible.builtin.get_url module.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

This only applies if using a https URL as the source of the file.

This should only set to false used on personally controlled sites using self-signed certificate.

Prior to 2.2 the code worked as if this was set to true.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Not supported for gzipped tar files.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses gtar’s --diff arg to calculate if changed or not. If this arg is not supported, it will always unpack the archive.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

Requires zipinfo and gtar/unzip command on target host.

Requires zstd command on target host to expand .tar.zst files.

Can handle .zip files using unzip as well as .tar, .tar.gz, .tar.bz2, .tar.xz, and .tar.zst files using gtar.

Does not handle .gz files, .bz2 files, .xz, or .zst files that do not contain a .tar archive.

Existing files/directories in the destination which are not in the archive are not touched. This is the same behavior as a normal archive extraction.

Existing files/directories in the destination which are not in the archive are ignored for purposes of deciding if the archive should be unpacked or not.

The official documentation on the community.general.archive module.

The official documentation on the community.general.iso_extract module.

The official documentation on the community.windows.win_unzip module.

Common return values are documented here, the following are the fields unique to this module:

Path to the destination directory.

Sample: "/opt/software"

list / elements=string

List of all the files in the archive.

Returned: When list_files is True

Sample: ["[\"file1\"", " \"file2\"]"]

Numerical ID of the group that owns the destination directory.

Name of the group that owns the destination directory.

Archive software handler used to extract and decompress the archive.

String that represents the octal permissions of the destination directory.

Name of the user that owns the destination directory.

The size of destination directory in bytes. Does not include the size of files or subdirectories contained within.

The source archive’s path.

If src was a remote web URL, or from the local ansible controller, this shows the temporary location where the download was stored.

Sample: "/home/paul/test.tar.gz"

State of the destination. Effectively always “directory”.

Numerical ID of the user that owns the destination directory.

**Examples:**

Example 1 (unknown):
```unknown
- name: Extract foo.tgz into /var/lib/foo
  ansible.builtin.unarchive:
    src: foo.tgz
    dest: /var/lib/foo

- name: Unarchive a file that is already on the remote machine
  ansible.builtin.unarchive:
    src: /tmp/foo.zip
    dest: /usr/local/bin
    remote_src: yes

- name: Unarchive a file that needs to be downloaded (added in 2.0)
  ansible.builtin.unarchive:
    src: https://example.com/example.zip
    dest: /usr/local/bin
    remote_src: yes

- name: Unarchive a file with extra options
  ansible.builtin.unarchive:
    src: /tmp/foo.zip
    dest: /usr/local/bin
    extra_opts:
    - --transform
    - s/^xxx/yyy/
```

---

## ansible.builtin.checksum filter – checksum of input data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/checksum_filter.html

**Contents:**
- ansible.builtin.checksum filter – checksum of input data
- Synopsis
- Input
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name checksum. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.checksum for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Returns a checksum (SHA-1) hash of the input data.

This describes the input of the filter, the value before | ansible.builtin.checksum.

The checksum (SHA-1) of the input.

**Examples:**

Example 1 (javascript):
```javascript
# csum => "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"
csum: "{{ 'test2' | checksum }}"
```

---

## ansible.builtin.skipped test – Was task skipped — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/skipped_test.html

**Contents:**
- ansible.builtin.skipped test – Was task skipped
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name skipped. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.skipped for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task was skipped

This test checks for the existence of a skipped key in the input dictionary and that it is True if present

This describes the input of the test, the value before is ansible.builtin.skipped or is not ansible.builtin.skipped.

dictionary / required

registered result from an Ansible task

Returns True if the task was skipped, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is skipped }}
```

---

## ansible.builtin.urlencode filter – Quote data for use in a URL path or query using UTF-8. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/urlencode_filter.html

**Contents:**
- ansible.builtin.urlencode filter – Quote data for use in a URL path or query using UTF-8.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name urlencode. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.urlencode for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Quote data for use in a URL path or query using UTF-8.

This is the Jinja builtin filter plugin ‘urlencode’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.urlencode

---

## ansible.builtin.fetch module – Fetch files from remote nodes — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/fetch_module.html

**Contents:**
- ansible.builtin.fetch module – Fetch files from remote nodes
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name fetch even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.fetch for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module works like ansible.builtin.copy, but in reverse.

It is used for fetching files from remote machines and storing them locally in a file tree, organized by hostname.

Files that already exist at dest will be overwritten if they are different than the src.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

A directory to save the file into.

For example, if dest=/backup, then src=/etc/profile on host host.example.com, would save the file into /backup/host.example.com/etc/profile. The host name is based on the inventory name.

When set to true, the task will fail if the remote file cannot be read for any reason.

Prior to Ansible 2.5, setting this would only fail if the source file was missing.

The default was changed to true in Ansible 2.5.

Allows you to override the default behavior of appending hostname/path/to/file to the destination.

If dest ends with ‘/’, it will use the basename of the source file, similar to the copy module.

This can be useful if working with a single host, or if retrieving files that are uniquely named per host.

If using multiple hosts with the same filename, the file will be overwritten for each host.

The file on the remote system to fetch.

This must be a file, not a directory.

Recursive fetching may be supported in a later release.

Verify that the source and destination checksums match after the files are fetched.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Platforms: posix, windows

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

When running fetch with become, the ansible.builtin.slurp module will also be used to fetch the contents of the file for determining the remote checksum. This effectively doubles the transfer size, and depending on the file size can consume all available memory on the remote or local hosts causing a MemoryError. Due to this it is advisable to run this module without become whenever possible.

Prior to Ansible 2.5 this module would not fail if reading the remote file was impossible unless fail_on_missing was set.

In Ansible 2.5 or later, playbook authors are encouraged to use fail_when or ignore_errors to get this ability. They may also explicitly set fail_on_missing to false to get the non-failing behaviour.

Copy files to remote locations.

Slurps a file from remote nodes.

**Examples:**

Example 1 (unknown):
```unknown
- name: Store file into /tmp/fetched/host.example.com/tmp/somefile
  ansible.builtin.fetch:
    src: /tmp/somefile
    dest: /tmp/fetched

- name: Specifying a path directly
  ansible.builtin.fetch:
    src: /tmp/somefile
    dest: /tmp/prefix-{{ inventory_hostname }}
    flat: yes

- name: Specifying a destination path
  ansible.builtin.fetch:
    src: /tmp/uniquefile
    dest: /tmp/special/
    flat: yes

- name: Storing in a path relative to the playbook
  ansible.builtin.fetch:
    src: /tmp/uniquefile
    dest: special/prefix-{{ inventory_hostname }}
    flat: yes
```

---

## ansible.builtin.combinations filter – combinations from the elements of a list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/combinations_filter.html

**Contents:**
- ansible.builtin.combinations filter – combinations from the elements of a list
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name combinations. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.combinations for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Create a list of combinations of sets from the elements of a list.

This describes the input of the filter, the value before | ansible.builtin.combinations.

list / elements=string / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.combinations(positional1, positional2, ...)

The size of the set for each combination.

list / elements=string

List of combination sets resulting from the supplied elements and set size.

**Examples:**

Example 1 (javascript):
```javascript
# combos_of_two => [ [ 1, 2 ], [ 1, 3 ], [ 1, 4 ], [ 1, 5 ], [ 2, 3 ], [ 2, 4 ], [ 2, 5 ], [ 3, 4 ], [ 3, 5 ], [ 4, 5 ] ]
combos_of_two: "{{ [1,2,3,4,5] | combinations(2) }}"
```

---

## ansible.builtin.regex_findall filter – extract all regex matches from string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/regex_findall_filter.html

**Contents:**
- ansible.builtin.regex_findall filter – extract all regex matches from string
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name regex_findall. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.regex_findall for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Search in a string or extract all the parts of a string matching a regular expression.

This describes the input of the filter, the value before | ansible.builtin.regex_findall.

String to match against.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.regex_findall(positional1, positional2, ...)

Regular expression string that defines the match.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.regex_findall(key1=value1, key2=value2, ...)

Force the search to be case insensitive if True, case sensitive otherwise.

Search across line endings if True, do not if otherwise.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.regex_findall(positional1, positional2, key1=value1, key2=value2)

list / elements=string

List of matched strings.

**Examples:**

Example 1 (javascript):
```javascript
# all_pirates => ['CAR', 'tar', 'bar']
all_pirates: "{{ 'CAR\ntar\nfoo\nbar\n' | regex_findall('^.ar$', multiline=True, ignorecase=True) }}"

# Using inline regex flags instead of passing options to filter
# See https://docs.python.org/3/library/re.html for more information
# on inline regex flags
# all_pirates => ['CAR', 'tar', 'bar']
all_pirates: "{{ 'CAR\ntar\nfoo\nbar\n' | regex_findall('(?im)^.ar$') }}"

# get_ips => ['8.8.8.8', '8.8.4.4']
get_ips: "{{ 'Some DNS servers are 8.8.8.8 and 8.8.4.4' | regex_findall('\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b') }}"
```

---

## ansible.builtin.default callback – default Ansible screen output — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/default_callback.html

**Contents:**
- ansible.builtin.default callback – default Ansible screen output
- Callback plugin
- Synopsis
- Requirements
- Parameters
  - Collection links

This callback plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name default. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.default for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same callback plugin name.

This plugin is a stdout callback. You can use only use one stdout callback at a time. Additional aggregate or notification callbacks can be enabled though. See Callback plugins for more information on callback plugins.

This is the default output callback for ansible-playbook.

The below requirements are needed on the local controller node that executes this callback.

set as stdout in configuration

Toggle to control displaying markers when running in check mode.

The markers are DRY RUN at the beginning and ending of playbook execution (when calling ansible-playbook --check) and CHECK MODE as a suffix at every play and task that is run in check mode.

Environment variable: ANSIBLE_CHECK_MODE_MARKERS

display_failed_stderr

Toggle to control whether failed and unreachable tasks are displayed to STDERR rather than STDOUT.

Environment variable: ANSIBLE_DISPLAY_FAILED_STDERR

Toggle to control displaying ‘ok’ task/host results in a task.

Environment variable: ANSIBLE_DISPLAY_OK_HOSTS

display_skipped_hosts

Toggle to control displaying skipped task/host results in a task.

Environment variable: ANSIBLE_DISPLAY_SKIPPED_HOSTS

added in ansible-core 2.13

Configure the result format to be more readable.

When result_format is set to yaml this option defaults to true, and defaults to false when configured to json.

Setting this option to true will force json and yaml results to always be pretty printed regardless of verbosity.

When set to true and used with the yaml result format, this option will modify module responses in an attempt to produce a more human friendly output at the expense of correctness, and should not be relied upon to aid in writing variable manipulations or conditionals. For correctness, set this option to false or set result_format to json.

Environment variable: ANSIBLE_CALLBACK_FORMAT_PRETTY

added in ansible-core 2.13

Define the task result format used in the callback output.

These formats do not cause the callback to emit valid JSON or YAML formats.

The output contains these formats interspersed with other non-machine parsable data.

Environment variable: ANSIBLE_CALLBACK_RESULT_FORMAT

This adds the custom stats set via the set_stats plugin to the play recap.

Environment variable: ANSIBLE_SHOW_CUSTOM_STATS

This adds output that shows when a task starts to execute for each host.

Environment variable: ANSIBLE_SHOW_PER_HOST_START

show_task_path_on_failure

added in ansible-core 2.11

When a task fails, display the path to the file containing the failed task and the line number. This information is displayed automatically for every task when running with -vv or greater verbosity.

Environment variable: ANSIBLE_SHOW_TASK_PATH_ON_FAILURE

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
check_mode_markers = false
```

Example 2 (unknown):
```unknown
[defaults]
display_failed_stderr = false
```

Example 3 (unknown):
```unknown
[defaults]
display_ok_hosts = true
```

Example 4 (unknown):
```unknown
[defaults]
display_skipped_hosts = true
```

---

## ansible.builtin.lower filter – Convert a value to lowercase. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lower_filter.html

**Contents:**
- ansible.builtin.lower filter – Convert a value to lowercase.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name lower. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lower for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert a value to lowercase.

This is the Jinja builtin filter plugin ‘lower’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.lower

---

## ansible.builtin.vars lookup – Lookup templated value of variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/vars_lookup.html

**Contents:**
- ansible.builtin.vars lookup – Lookup templated value of variables
- Synopsis
- Terms
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name vars. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.vars for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Retrieves the value of an Ansible variable. Note: Only returns top level variable names.

The variable names to look up.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.vars', key1=value1, key2=value2, ...) and query('ansible.builtin.vars', key1=value1, key2=value2, ...)

What to return if a variable is undefined.

If no default is set, it will result in an error if any of the variables is undefined.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.vars', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.vars', term1, term2, key1=value1, key2=value2)

Lookup matching variable names.

value of the variables requested.

**Examples:**

Example 1 (unknown):
```unknown
- name: Show value of 'variablename'
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.vars', 'variabl' + myvar) }}"
  vars:
    variablename: hello
    myvar: ename

- name: Show default empty since i dont have 'variablnotename'
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.vars', 'variabl' + myvar, default='') }}"
  vars:
    variablename: hello
    myvar: notename

- name: Produce an error since i dont have 'variablnotename'
  ansible.builtin.debug: msg="{{ q('vars', 'variabl' + myvar) }}"
  ignore_errors: True
  vars:
    variablename: hello
    myvar: notename

- name: find several related variables
  ansible.builtin.debug: msg="{{ query('ansible.builtin.vars', 'ansible_play_hosts', 'ansible_play_batch', 'ansible_play_hosts_all') }}"

- name: show values from variables found via varnames (note "*" is used to dereference the list to a 'list of arguments')
  debug: msg="{{ q('vars', *q('varnames', 'ansible_play_.+')) }}"

- name: Access nested variables
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.vars', 'variabl' + myvar).sub_var }}"
  ignore_errors: True
  vars:
    variablename:
        sub_var: 12
    myvar: ename

- name: alternate way to find some 'prefixed vars' in loop
  ansible.builtin.debug: msg="{{ lookup('ansible.builtin.vars', 'ansible_play_' + item) }}"
  loop:
    - hosts
    - batch
    - hosts_all
```

---

## ansible.builtin.eq test – Same as a == b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/eq_test.html

**Contents:**
- ansible.builtin.eq test – Same as a == b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name eq. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.eq for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘eq’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.eq

---

## ansible.builtin.from_yaml filter – Convert YAML string into variable structure — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/from_yaml_filter.html

**Contents:**
- ansible.builtin.from_yaml filter – Convert YAML string into variable structure
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name from_yaml. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.from_yaml for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts a YAML string representation into an equivalent structured Ansible variable.

Ansible automatically converts YAML strings into variable structures in most contexts, use this plugin in contexts where automatic conversion does not happen.

This describes the input of the filter, the value before | ansible.builtin.from_yaml.

This filter functions as a wrapper to the Python pyyaml library‘s yaml.safe_load function.

The variable resulting from deserializing the YAML document.

**Examples:**

Example 1 (unknown):
```unknown
# variable from string variable containing a YAML document
{{ github_workflow | from_yaml }}

# variable from string JSON document
{{ '{"a": true, "b": 54, "c": [1,2,3]}' | from_yaml }}
```

---

## ansible.builtin.template module – Template a file out to a target host — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/template_module.html

**Contents:**
- ansible.builtin.template module – Template a file out to a target host
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name template even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.template for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Templates are processed by the Jinja2 templating language.

Documentation on the template formatting can be found in the Template Designer Documentation.

Additional variables listed below can be used in templates.

ansible_managed (configurable via the defaults section of ansible.cfg) contains a string which can be used to describe the template name, host, modification time of the template file and the owner uid.

template_host contains the node name of the template’s machine.

template_uid is the numeric user id of the owner.

template_path is the path of the template.

template_fullpath is the absolute path of the template.

template_destpath is the path of the template on the remote system (added in 2.8).

template_run_date is the date that the template was rendered.

This module has a corresponding action plugin.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

The string marking the end of a block.

The string marking the beginning of a block.

added in ansible-core 2.12

The string marking the end of a comment statement.

added in ansible-core 2.12

The string marking the beginning of a comment statement.

Location to render the template to on the remote machine.

Determine whether symbolic links should be followed.

When set to true symbolic links will be followed, if they exist.

When set to false symbolic links will not be followed.

Previous to Ansible 2.4, this was hardcoded as true.

Determine when the file is being transferred if the destination already exists.

When set to yes, replace the remote file when contents are different than the source.

When set to no, the file will only be transferred if the destination does not exist.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

Determine when leading spaces and tabs should be stripped.

When set to yes leading spaces and tabs are stripped from the start of a line to a block.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Specify the newline sequence to use for templating files.

Overrides the encoding used to write the template file defined by dest.

It defaults to utf-8, but any encoding supported by python can be used.

The source template file must always be encoded using utf-8, for homogeneity.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Path of a Jinja2 formatted template on the Ansible controller.

This can be a relative or an absolute path.

The file must be encoded with utf-8 but output_encoding can be used to control the encoding of the output template.

Determine when newlines should be removed from blocks.

When set to yes the first newline after a block is removed (block, not variable tag!).

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying the updated file into the final destination.

A temporary file path is used to validate, passed in through %s which must be present as in the examples below.

Also, the command is passed securely so shell features such as expansion and pipes will not work.

For an example on how to handle more complex validation than what this option provides, see handling complex validation.

The string marking the end of a print statement.

variable_start_string

The string marking the beginning of a print statement.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

For Windows you can use ansible.windows.win_template which uses \r\n as newline_sequence by default.

The jinja2_native setting has no effect. Native types are never used in the ansible.builtin.template module which is by design used for generating text files. For working with templates and utilizing Jinja2 native types see the jinja2_native parameter of the ansible.builtin.template lookup.

Including a string that uses a date in the template will result in the template being marked ‘changed’ each time.

Since Ansible 0.9, templates are loaded with trim_blocks=True.

Also, you can override jinja2 settings by adding a special header to template file. that is #jinja2:variable_start_string:'[%', variable_end_string:'%]', trim_blocks: False which changes the variable interpolation markers to [% var %] instead of {{ var }}. This is the best way to prevent evaluation of things that look like, but should not be Jinja2.

To find Byte Order Marks in files, use Format-Hex <file> -Count 16 on Windows, and use od -a -t x1 -N 16 <file> on Linux.

Copy files to remote locations.

The official documentation on the ansible.windows.win_copy module.

The official documentation on the ansible.windows.win_template module.

Common return values are documented here, the following are the fields unique to this module:

SHA1 checksum of the rendered file

Sample: "373296322247ab85d26d5d1257772757e7afd172"

Destination file/path, equal to the value passed to dest.

Sample: "/path/to/file.txt"

Numeric id representing the group of the owner

MD5 checksum of the rendered file

Sample: "d41d8cd98f00b204e9800998ecf8427e"

Unix permissions of the file in octal representation as a string

Size of the rendered file in bytes

Source file used for the copy on the target machine.

Sample: "/home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source"

Numeric id representing the file owner

**Examples:**

Example 1 (unknown):
```unknown
- name: Template a file to /etc/file.conf
  ansible.builtin.template:
    src: /mytemplates/foo.j2
    dest: /etc/file.conf
    owner: bin
    group: wheel
    mode: '0644'

- name: Template a file, using symbolic modes (equivalent to 0644)
  ansible.builtin.template:
    src: /mytemplates/foo.j2
    dest: /etc/file.conf
    owner: bin
    group: wheel
    mode: u=rw,g=r,o=r

- name: Copy a version of named.conf that is dependent on the OS. setype obtained by doing ls -Z /etc/named.conf on original file
  ansible.builtin.template:
    src: named.conf_{{ ansible_os_family }}.j2
    dest: /etc/named.conf
    group: named
    setype: named_conf_t
    mode: '0640'

- name: Create a DOS-style text file from a template
  ansible.builtin.template:
    src: config.ini.j2
    dest: /share/windows/config.ini
    newline_sequence: '\r\n'

- name: Copy a new sudoers file into place, after passing validation with visudo
  ansible.builtin.template:
    src: /mine/sudoers
    dest: /etc/sudoers
    validate: /usr/sbin/visudo -cf %s

- name: Update sshd configuration safely, avoid locking yourself out
  ansible.builtin.template:
    src: etc/ssh/sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: '0600'
    validate: /usr/sbin/sshd -t -f %s
    backup: yes
```

---

## ansible.builtin.normpath filter – Normalize a pathname — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/normpath_filter.html

**Contents:**
- ansible.builtin.normpath filter – Normalize a pathname
- Synopsis
- Input
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name normpath. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.normpath for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.15

Returns the normalized pathname by collapsing redundant separators and up-level references.

This describes the input of the filter, the value before | ansible.builtin.normpath.

get a path’s base name.

The normalized path from the path given.

**Examples:**

Example 1 (unknown):
```unknown
# To get a normalized path (for example - '/foo/bar') from the path (for example - '/foo//bar')
{{ path | normpath }}
```

---

## ansible.builtin.regex_search filter – extract regex match from string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/regex_search_filter.html

**Contents:**
- ansible.builtin.regex_search filter – extract regex match from string
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name regex_search. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.regex_search for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Search in a string to extract the part that matches the regular expression.

This describes the input of the filter, the value before | ansible.builtin.regex_search.

String to match against.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.regex_search(positional1, positional2, ...)

Regular expression string that defines the match.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.regex_search(key1=value1, key2=value2, ...)

Force the search to be case insensitive if True, case sensitive otherwise.

Search across line endings if True, do not if otherwise.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.regex_search(positional1, positional2, key1=value1, key2=value2)

Maps to Python’s re.search.

The substring matched by the group is accessible via the symbolic group name or the ``\{number}`` special sequence. See examples section.

Matched string or None if no match.

**Examples:**

Example 1 (javascript):
```javascript
# db => 'database42'
db: "{{ 'server1/database42' | regex_search('database[0-9]+') }}"

# Using inline regex flags instead of passing options to filter
# See https://docs.python.org/3/library/re.html for more information
# on inline regex flags
# server => 'sErver1'
db: "{{ 'sErver1/database42' | regex_search('(?i)server([0-9]+)') }}"

# drinkat => 'BAR'
drinkat: "{{ 'foo\nBAR' | regex_search('^bar', multiline=True, ignorecase=True) }}"

# Extracts server and database id from a string using number
# (the substring matched by the group is accessible via the \number special sequence)
db: "{{ 'server1/database42' | regex_search('server([0-9]+)/database([0-9]+)', '\\1', '\\2') }}"
# => ['1', '42']

# Extracts dividend and divisor from a division
# (the substring matched by the group is accessible via the symbolic group name)
db: "{{ '21/42' | regex_search('(?P<dividend>[0-9]+)/(?P<divisor>[0-9]+)', '\\g<dividend>', '\\g<divisor>') }}"
# => ['21', '42']
```

---

## ansible.builtin.exists test – does the path exist, follow symlinks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/exists_test.html

**Contents:**
- ansible.builtin.exists test – does the path exist, follow symlinks
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name exists. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.exists for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to an existing filesystem object on the controller (localhost).

Follows symlinks and checks the target of the symlink instead of the link itself, use the ansible.builtin.link or ansible.builtin.link_exists tests to check on the link.

This describes the input of the test, the value before is ansible.builtin.exists or is not ansible.builtin.exists.

Returns True if the path corresponds to an existing filesystem object on the controller (after following symlinks), False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
vars:
  my_etc_hosts_exists: "{{ '/etc/hosts' is exists }}"
  list_of_local_files_to_copy_to_remote: "{{ list_of_all_possible_files | select('exists') }}"
```

---

## ansible.builtin.lineinfile module – Manage lines in text files — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lineinfile_module.html

**Contents:**
- ansible.builtin.lineinfile module – Manage lines in text files
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name lineinfile even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lineinfile for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module ensures a particular line is in a file, or replace an existing line using a back-referenced regular expression.

This is primarily useful when you want to change a single line in a file only.

See the ansible.builtin.replace module if you want to change multiple, similar lines or check ansible.builtin.blockinfile if you want to insert/update/remove a block of lines in a file. For other cases, see the ansible.builtin.copy or ansible.builtin.template modules.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Used with state=present.

If set, line can contain backreferences (both positional and named) that will get populated if the regexp matches.

This parameter changes the operation of the module slightly; insertbefore and insertafter will be ignored, and if the regexp does not match anywhere in the file, the file will be left unchanged.

If the regexp does match, the last matching line will be replaced by the expanded line parameter.

Mutually exclusive with search_string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

Used with state=present.

If specified, the file will be created if it does not already exist.

By default it will fail if the file is missing.

Used with insertafter or insertbefore.

If set, insertafter and insertbefore will work with the first line that matches the given regular expression.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

Used with state=present.

If specified, the line will be inserted after the last match of specified regular expression.

If the first match is required, use(firstmatch=yes).

A special value is available; EOF for inserting the line at the end of the file.

If specified regular expression has no matches or no value is passed, EOF will be used instead.

If insertbefore is set, default value EOF will be ignored.

If regular expressions are passed to both regexp and insertafter, insertafter is only honored if no match for regexp is found.

May not be used with backrefs or insertbefore.

Used with state=present.

If specified, the line will be inserted before the last match of specified regular expression.

If the first match is required, use firstmatch=yes.

A value is available; BOF for inserting the line at the beginning of the file.

If specified regular expression has no matches, the line will be inserted at the end of the file.

If regular expressions are passed to both regexp and insertbefore, insertbefore is only honored if no match for regexp is found.

May not be used with backrefs or insertafter.

The line to insert/replace into the file.

Required for state=present.

If backrefs is set, may contain backreferences that will get expanded with the regexp capture groups if the regexp matches.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

aliases: dest, destfile, name

Before Ansible 2.3 this option was only usable as dest, destfile and name.

The regular expression to look for in every line of the file.

For state=present, the pattern to replace if found. Only the last line found will be replaced.

For state=absent, the pattern of the line(s) to remove.

If the regular expression is not matched, the line will be added to the file in keeping with insertbefore or insertafter settings.

When modifying a line the regexp should typically match both the initial state of the line as well as its state after replacement by line to ensure idempotence.

Uses Python regular expressions. See https://docs.python.org/3/library/re.html.

added in ansible-core 2.11

The literal string to look for in every line of the file. This does not have to match the entire line.

For state=present, the line to replace if the string is found in the file. Only the last line found will be replaced.

For state=absent, the line(s) to remove if the string is in the line.

If the literal expression is not matched, the line will be added to the file in keeping with insertbefore or insertafter settings.

Mutually exclusive with backrefs and regexp.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Whether the line should be there or not.

"present" ← (default)

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying the updated file into the final destination.

A temporary file path is used to validate, passed in through %s which must be present as in the examples below.

Also, the command is passed securely so shell features such as expansion and pipes will not work.

For an example on how to handle more complex validation than what this option provides, see handling complex validation.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

As of Ansible 2.3, the dest option has been changed to path as default, but dest still works as well.

Insert/update/remove a text block surrounded by marker lines.

Copy files to remote locations.

Manage files and file properties.

Replace all instances of a particular string in a file using a back-referenced regular expression.

Template a file out to a target host.

The official documentation on the community.windows.win_lineinfile module.

Daniel Hokka Zakrissoni (@dhozac)

Jose Angel Munoz (@imjoseangel)

**Examples:**

Example 1 (unknown):
```unknown
# NOTE: Before 2.3, option 'dest', 'destfile' or 'name' was used instead of 'path'
- name: Ensure SELinux is set to enforcing mode
  ansible.builtin.lineinfile:
    path: /etc/selinux/config
    regexp: '^SELINUX='
    line: SELINUX=enforcing

- name: Make sure group wheel is not in the sudoers configuration
  ansible.builtin.lineinfile:
    path: /etc/sudoers
    state: absent
    regexp: '^%wheel'

- name: Replace a localhost entry with our own
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: '^127\.0\.0\.1'
    line: 127.0.0.1 localhost
    owner: root
    group: root
    mode: '0644'

- name: Replace a localhost entry searching for a literal string to avoid escaping
  ansible.builtin.lineinfile:
    path: /etc/hosts
    search_string: '127.0.0.1'
    line: 127.0.0.1 localhost
    owner: root
    group: root
    mode: '0644'

- name: Ensure the default Apache port is 8080
  ansible.builtin.lineinfile:
    path: /etc/httpd/conf/httpd.conf
    regexp: '^Listen '
    insertafter: '^#Listen '
    line: Listen 8080

- name: Ensure php extension matches new pattern
  ansible.builtin.lineinfile:
    path: /etc/httpd/conf/httpd.conf
    search_string: '<FilesMatch ".php[45]?$">'
    insertafter: '^\t<Location \/>\n'
    line: '        <FilesMatch ".php[34]?$">'

- name: Ensure we have our own comment added to /etc/services
  ansible.builtin.lineinfile:
    path: /etc/services
    regexp: '^# port for http'
    insertbefore: '^www.*80/tcp'
    line: '# port for http by default'

- name: Add a line to a file if the file does not exist, without passing regexp
  ansible.builtin.lineinfile:
    path: /tmp/testfile
    line: 192.168.1.99 foo.lab.net foo
    create: yes

# NOTE: Yaml requires escaping backslashes in double quotes but not in single quotes
- name: Ensure the JBoss memory settings are exactly as needed
  ansible.builtin.lineinfile:
    path: /opt/jboss-as/bin/standalone.conf
    regexp: '^(.*)Xms(\d+)m(.*)$'
    line: '\1Xms${xms}m\3'
    backrefs: yes

# NOTE: Fully quoted because of the ': ' on the line. See the Gotchas in the YAML docs.
- name: Validate the sudoers file before saving
  ansible.builtin.lineinfile:
    path: /etc/sudoers
    state: present
    regexp: '^%ADMIN ALL='
    line: '%ADMIN ALL=(ALL) NOPASSWD: ALL'
    validate: /usr/sbin/visudo -cf %s

# See https://docs.python.org/3/library/re.html for further details on syntax
- name: Use backrefs with alternative group syntax to avoid conflicts with variable values
  ansible.builtin.lineinfile:
    path: /tmp/config
    regexp: ^(host=).*
    line: \g<1>{{ hostname }}
    backrefs: yes
```

---

## ansible.builtin.sh shell – POSIX shell (/bin/sh) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sh_shell.html

**Contents:**
- ansible.builtin.sh shell – POSIX shell (/bin/sh)
- Synopsis
- Parameters
  - Collection links

This shell plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name sh. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sh for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same shell plugin name.

This shell plugin is the one you want to use on most Unix systems, it is the most compatible and widely installed shell.

list / elements=string

list of users to be expected to have admin privileges. This is used by the controller to determine how to share temporary files between the remote user and the become user.

Default: ["root", "toor"]

Environment variable: ANSIBLE_ADMIN_USERS

Variable: ansible_admin_users

Directory in which ansible will keep async job information.

Default: "~/.ansible_async"

Environment variable: ANSIBLE_ASYNC_DIR

Variable: ansible_async_dir

added in ansible-base 2.10

Checked when Ansible needs to execute a module as a different user.

If setfacl and chown both fail and do not let the different user access the module’s files, they will be chgrp’d to this group.

In order for this to work, the remote_user and become_user must share a common group and this setting must be set to that group.

Environment variable: ANSIBLE_COMMON_REMOTE_GROUP

Variable: ansible_common_remote_group

Temporary directory to use on targets when executing tasks.

Default: "~/.ansible/tmp"

Environment variable: ANSIBLE_REMOTE_TEMP

Environment variable: ANSIBLE_REMOTE_TMP

Variable: ansible_remote_tmp

list / elements=string

List of valid system temporary directories on the managed machine for Ansible to validate remote_tmp against, when specific permissions are needed. These must be world readable, writable, and executable. This list should only contain directories which the system administrator has pre-created with the proper ownership and permissions otherwise security issues can arise.

When remote_tmp is required to be a system temp dir and it does not match any in the list, the first one from the list will be used instead.

Default: ["/var/tmp", "/tmp"]

Environment variable: ANSIBLE_SYSTEM_TMPDIRS

Variable: ansible_system_tmpdirs

added in ansible-base 2.10

This makes the temporary files created on the machine world-readable and will issue a warning instead of failing the task.

It is useful when becoming an unprivileged user.

Environment variable: ANSIBLE_SHELL_ALLOW_WORLD_READABLE_TEMP

Variable: ansible_shell_allow_world_readable_temp

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
admin_users = root, toor
```

Example 2 (unknown):
```unknown
[defaults]
async_dir = ~/.ansible_async
```

Example 3 (unknown):
```unknown
[defaults]
common_remote_group = VALUE
```

Example 4 (unknown):
```unknown
[defaults]
remote_tmp = ~/.ansible/tmp
```

---

## ansible.builtin.ping module – Try to connect to host, verify a usable python and return pong on success — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ping_module.html

**Contents:**
- ansible.builtin.ping module – Try to connect to host, verify a usable python and return pong on success
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name ping even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ping for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

A trivial test module, this module always returns pong on successful contact. It does not make sense in playbooks, but it is useful from /usr/bin/ansible to verify the ability to login and that a usable Python is configured.

This is NOT ICMP ping, this is just a trivial test module that requires Python on the remote-node.

For Windows targets, use the ansible.windows.win_ping module instead.

For Network targets, use the ansible.netcommon.net_ping module instead.

Data to return for the ping return value.

If this parameter is set to crash, the module will cause an exception.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

The official documentation on the ansible.netcommon.net_ping module.

The official documentation on the ansible.windows.win_ping module.

Common return values are documented here, the following are the fields unique to this module:

Value provided with the data parameter.

**Examples:**

Example 1 (unknown):
```unknown
# Test we can logon to 'webservers' and execute python with json lib.
# ansible webservers -m ansible.builtin.ping

- name: Example from an Ansible Playbook
  ansible.builtin.ping:

- name: Induce an exception to see what happens
  ansible.builtin.ping:
    data: crash
```

---

## ansible.builtin.sysvinit module – Manage SysV services. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/sysvinit_module.html

**Contents:**
- ansible.builtin.sysvinit module – Manage SysV services.
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name sysvinit even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.sysvinit for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Controls services on target hosts that use the SysV init system.

The below requirements are needed on the host that executes this module.

That the service managed has a corresponding init script.

Additional arguments provided on the command line that some init scripts accept.

Have the module daemonize as the service itself might not do so properly.

This is useful with badly written init scripts or daemons, which commonly manifests as the task hanging as it is still holding the tty or the service dying when the task is over as the connection closes the session.

Whether the service should start on boot. At least one of state and enabled are required.

A substring to look for as would be found in the output of the ps command as a stand-in for a status result.

If the string is found, the service will be assumed to be running.

This option is mainly for use with init scripts that don’t support the status option.

list / elements=string

The runlevels this script should be enabled/disabled from.

Use this to override the defaults set by the package or init script itself.

If the service is being restarted or reloaded then sleep this many seconds between the stop and start command. This helps to workaround badly behaving services.

started/stopped are idempotent actions that will not run commands unless necessary. Not all init scripts support restarted nor reloaded natively, so these will both trigger a stop and start as needed.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

One option other than name is required.

The service names might vary by specific OS/distribution.

Common return values are documented here, the following are the fields unique to this module:

results from actions taken

Status of the service

Sample: {"enabled": {"changed": true, "rc": 0, "stderr": "", "stdout": ""}, "stopped": {"changed": true, "rc": 0, "stderr": "", "stdout": "Stopping web server: apache2.\n"}}

**Examples:**

Example 1 (unknown):
```unknown
- name: Make sure apache2 is started
  ansible.builtin.sysvinit:
      name: apache2
      state: started
      enabled: yes

- name: Sleep for 5 seconds between stop and start command of badly behaving service
  ansible.builtin.sysvinit:
      name: apache2
      state: restarted
      sleep: 5

- name: Make sure apache2 is started on runlevels 3 and 5
  ansible.builtin.sysvinit:
      name: apache2
      state: started
      enabled: yes
      runlevels:
        - 3
        - 5
```

---

## ansible.builtin.rekey_on_member filter – Rekey a list of dicts into a dict using a member — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/rekey_on_member_filter.html

**Contents:**
- ansible.builtin.rekey_on_member filter – Rekey a list of dicts into a dict using a member
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name rekey_on_member. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.rekey_on_member for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

New in ansible-core 2.13

Positional parameters

Iterate over several iterables in parallel, producing tuples with an item from each one.

This describes the input of the filter, the value before | ansible.builtin.rekey_on_member.

dictionary / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.rekey_on_member(positional1, positional2, ...)

How to handle duplicates.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.rekey_on_member(key1=value1, key2=value2, ...)

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.rekey_on_member(positional1, positional2, key1=value1, key2=value2)

The resulting dictionary.

**Examples:**

Example 1 (javascript):
```javascript
# mydict => {'eigrp': {'state': 'enabled', 'proto': 'eigrp'}, 'ospf': {'state': 'enabled', 'proto': 'ospf'}}
 mydict: '{{ [{"proto": "eigrp", "state": "enabled"}, {"proto": "ospf", "state": "enabled"}] | rekey_on_member("proto") }}'
```

---

## ansible.builtin.env lookup – Read the value of environment variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/env_lookup.html

**Contents:**
- ansible.builtin.env lookup – Read the value of environment variables
- Synopsis
- Terms
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name env. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.env for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Allows you to query the environment variables available on the controller when you invoked Ansible.

Environment variable or list of them to lookup the values for.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.env', key1=value1, key2=value2, ...) and query('ansible.builtin.env', key1=value1, key2=value2, ...)

added in ansible-core 2.13

What return when the variable is undefined

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.env', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.env', term1, term2, key1=value1, key2=value2)

You can pass the Undefined object as default to force an undefined error

list / elements=string

Values from the environment variables.

Jan-Piet Mens (@jpmens) <jpmens(at)gmail.com>

**Examples:**

Example 1 (unknown):
```unknown
- name: Basic usage
  ansible.builtin.debug:
    msg: "'{{ lookup('ansible.builtin.env', 'HOME') }}' is the HOME environment variable."

- name: Before 2.13, how to set default value if the variable is not defined
  ansible.builtin.debug:
    msg: "Hello {{ lookup('ansible.builtin.env', 'UNDEFINED_VARIABLE') | default('World', True) }}"

- name: Example how to set default value if the variable is not defined
  ansible.builtin.debug:
    msg: "Hello {{ lookup('ansible.builtin.env', 'UNDEFINED_VARIABLE', default='World') }}"

- name: Fail if the variable is not defined by setting default value to 'undef()'
  ansible.builtin.debug:
    msg: "Hello {{ lookup('ansible.builtin.env', 'UNDEFINED_VARIABLE', default=undef()) }}"
```

---

## ansible.builtin.apt_key module – Add or remove an apt key — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/apt_key_module.html

**Contents:**
- ansible.builtin.apt_key module – Add or remove an apt key
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name apt_key even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.apt_key for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Add or remove an apt key, optionally downloading it.

The below requirements are needed on the host that executes this module.

The keyfile contents to add to the keyring.

The path to a keyfile on the remote server to add to the keyring.

The identifier of the key.

Including this allows check mode to correctly report the changed state.

If specifying a subkey’s id be aware that apt-key does not understand how to remove keys via a subkey id. Specify the primary key’s id instead.

This parameter is required when state is set to absent.

The full path to specific keyring file in /etc/apt/trusted.gpg.d/.

The keyserver to retrieve key from.

Ensures that the key is present (added) or absent (revoked).

"present" ← (default)

The URL to retrieve key from.

If false, SSL certificates for the target url will not be validated. This should only be used on personally controlled sites using self-signed certificates.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

The apt-key command used by this module has been deprecated. See the Debian wiki for details. This module is kept for backwards compatibility for systems that still use apt-key as the main way to manage apt repository keys.

As a sanity check, downloaded key id must match the one specified.

Use full fingerprint (40 characters) key ids to avoid key collisions. To generate a full-fingerprint imported key: apt-key adv --list-public-keys --with-fingerprint --with-colons.

If you specify both the key id and the url with state=present, the task can verify or add the key as needed.

Adding a new key requires an apt cache update (e.g. using the ansible.builtin.apt module’s update_cache option).

The apt-key utility has been deprecated and removed in modern debian versions, use ansible.builtin.deb822_repository as an alternative to ansible.builtin.apt_repository + apt_key combinations.

Add and remove deb822 formatted repositories.

Common return values are documented here, the following are the fields unique to this module:

list / elements=string

List of apt key ids or fingerprints after any modification

Sample: ["D8576A8BA88D21E9", "3B4FE6ACC0B21F32", "D94AA3F0EFE21092", "871920D1991BC93C"]

list / elements=string

List of apt key ids or fingprints before any modifications

Sample: ["3B4FE6ACC0B21F32", "D94AA3F0EFE21092", "871920D1991BC93C"]

Fingerprint of the key to import

Sample: "D8576A8BA88D21E9"

Sample: "36A1D7869245C8950F966E92D8576A8BA88D21E9"

calculated key id, it should be same as ‘id’, but can be different

Sample: "36A1D7869245C8950F966E92D8576A8BA88D21E9"

calculated short key id

Jayson Vantuyl (@jvantuyl)

**Examples:**

Example 1 (unknown):
```unknown
- name: One way to avoid apt_key once it is removed from your distro, armored keys should use .asc extension, binary should use .gpg
  block:
    - name: somerepo | no apt key
      ansible.builtin.get_url:
        url: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x36a1d7869245c8950f966e92d8576a8ba88d21e9
        dest: /etc/apt/keyrings/myrepo.asc
        checksum: sha256:bb42f0db45d46bab5f9ec619e1a47360b94c27142e57aa71f7050d08672309e0

    - name: somerepo | apt source
      ansible.builtin.apt_repository:
        repo: "deb [arch=amd64 signed-by=/etc/apt/keyrings/myrepo.asc] https://download.example.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present

- name: Add an apt key by id from a keyserver
  ansible.builtin.apt_key:
    keyserver: keyserver.ubuntu.com
    id: 36A1D7869245C8950F966E92D8576A8BA88D21E9

- name: Add an Apt signing key, uses whichever key is at the URL
  ansible.builtin.apt_key:
    url: https://ftp-master.debian.org/keys/archive-key-6.0.asc
    state: present

- name: Add an Apt signing key, will not download if present
  ansible.builtin.apt_key:
    id: 9FED2BCBDCD29CDF762678CBAED4B06F473041FA
    url: https://ftp-master.debian.org/keys/archive-key-6.0.asc
    state: present

- name: Remove a Apt specific signing key, leading 0x is valid
  ansible.builtin.apt_key:
    id: 0x9FED2BCBDCD29CDF762678CBAED4B06F473041FA
    state: absent

# Use armored file since utf-8 string is expected. Must be of "PGP PUBLIC KEY BLOCK" type.
- name: Add a key from a file on the Ansible server
  ansible.builtin.apt_key:
    data: "{{ lookup('ansible.builtin.file', 'apt.asc') }}"
    state: present

- name: Add an Apt signing key to a specific keyring file
  ansible.builtin.apt_key:
    id: 9FED2BCBDCD29CDF762678CBAED4B06F473041FA
    url: https://ftp-master.debian.org/keys/archive-key-6.0.asc
    keyring: /etc/apt/trusted.gpg.d/debian.gpg

- name: Add Apt signing key on remote server to keyring
  ansible.builtin.apt_key:
    id: 9FED2BCBDCD29CDF762678CBAED4B06F473041FA
    file: /tmp/apt.gpg
    state: present
```

---

## ansible.builtin.selectattr filter – Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/selectattr_filter.html

**Contents:**
- ansible.builtin.selectattr filter – Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name selectattr. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.selectattr for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.

This is the Jinja builtin filter plugin ‘selectattr’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.selectattr

---

## ansible.builtin.d filter – If the value is undefined it will return the passed default value, otherwise the value of the variable. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/d_filter.html

**Contents:**
- ansible.builtin.d filter – If the value is undefined it will return the passed default value, otherwise the value of the variable.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name d. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.d for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

If the value is undefined it will return the passed default value, otherwise the value of the variable.

This is the Jinja builtin filter plugin ‘d’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.d

---

## ansible.builtin.comment filter – comment out a string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/comment_filter.html

**Contents:**
- ansible.builtin.comment filter – comment out a string
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name comment. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.comment for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Use programming language conventions to turn the input string into an embeddable comment.

This describes the input of the filter, the value before | ansible.builtin.comment.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.comment(positional1, positional2, ...)

Comment style to use.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.comment(key1=value1, key2=value2, ...)

Indicator of the start of a comment block, only available for styles that support multiline comments.

Indicator for comment or intermediate comment depending on the style.

Indicator the end of a comment block, only available for styles that support multiline comments.

Indicator of comment end of line, only available for styles that support multiline comments.

Indicator of the end of each line inside a comment block, only available for styles that support multiline comments.

Number of times to add a postfix at the end of a line, when a prefix exists and is usable.

Token to start each line inside a comment block, only available for styles that support multiline comments.

Number of times to add a prefix at the start of a line, when a prefix exists and is usable.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.comment(positional1, positional2, key1=value1, key2=value2)

The ‘commented out’ string.

**Examples:**

Example 1 (javascript):
```javascript
# commented =>  #
#               # Plain style (default)
#               #
commented: "{{ 'Plain style (default)' | comment }}"

# not going to show that here ...
verycustom: "{{ "Custom style" | comment('plain', prefix='#######\n#', postfix='#\n#######\n   ###\n    #') }}"
```

---

## ansible.builtin.select filter – Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/select_filter.html

**Contents:**
- ansible.builtin.select filter – Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name select. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.select for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.

This is the Jinja builtin filter plugin ‘select’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.select

---

## ansible.builtin.vaulted_file test – Is this file an encrypted vault — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/vaulted_file_test.html

**Contents:**
- ansible.builtin.vaulted_file test – Is this file an encrypted vault
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name vaulted_file. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.vaulted_file for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

New in ansible-core 2.18

Verifies if the input path is an Ansible vault file.

This describes the input of the test, the value before is ansible.builtin.vaulted_file or is not ansible.builtin.vaulted_file.

The path to the possible vault.

Returns True if the path is a valid ansible vault, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
thisisfalse: '{{ "/etc/hosts" is vaulted_file}}'
thisistrue: '{{ "/path/to/vaulted/file" is vaulted_file}}'
```

---

## ansible.builtin.dnf5 module – Manages packages with the dnf5 package manager — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dnf5_module.html

**Contents:**
- ansible.builtin.dnf5 module – Manages packages with the dnf5 package manager
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name dnf5 even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dnf5 for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

New in ansible-core 2.15

Installs, upgrade, removes, and lists packages and groups with the dnf5 package manager.

WARNING: The dnf5 package manager is still under development and not all features that the existing ansible.builtin.dnf module provides are implemented in ansible.builtin.dnf5, please consult specific options for more information.

The below requirements are needed on the host that executes this module.

Specify if the named package and version is allowed to downgrade a maybe already installed higher version of that package. Note that setting allow_downgrade=true can make this module behave in a non-idempotent way. The task could end up with a set of packages that does not match the complete list of specified packages to install (because dependencies between the downgraded package and others can cause changes to the packages which were in the earlier transaction).

Since this feature is not provided by dnf5 itself but by ansible.builtin.dnf5 module, using this in combination with wildcard characters in name may result in an unexpected results.

If true it allows erasing of installed packages to resolve dependencies.

auto_install_module_deps

added in ansible-core 2.19

Automatically install dependencies required to run this module.

If true, removes all “leaf” packages from the system that were originally installed as dependencies of user-installed packages but which are no longer required by any such package. Should be used alone or when state=absent.

added in ansible-core 2.17

When set to true, either use a package with the highest version available or fail.

When set to false, if the latest version cannot be installed go with the lower version.

Default is set by the operating system distribution.

If set to true, and state=latest then only installs updates that have been marked bugfix related.

Note that, similar to dnf upgrade-minimal, this filter applies to dependencies as well.

Tells dnf to run entirely from system cache; does not download or update metadata.

The remote dnf configuration file to use for the transaction.

Disable the excludes defined in DNF config files.

If set to all, disables all excludes.

If set to main, disable excludes defined in [main] in dnf.conf.

If set to repoid, disable excludes defined for given repo id.

Whether to disable the GPG checking of signatures of packages being installed. Has an effect only if state is present or latest.

This setting affects packages installed from a repository as well as “local” packages installed from the filesystem or a URL.

list / elements=string

Plugin name to disable for the install/update operation. The disabled plugins will not persist beyond the transaction.

disable_plugin takes precedence in case a plugin is listed in both enable_plugin and disable_plugin.

Requires python3-libdnf5 5.2.0.0+.

list / elements=string

Repoid of repositories to disable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a ,.

Specifies an alternate directory to store packages.

Has an effect only if download_only is specified.

Only download the packages, do not install them.

list / elements=string

Plugin name to enable for the install/update operation. The enabled plugin will not persist beyond the transaction.

disable_plugin takes precedence in case a plugin is listed in both enable_plugin and disable_plugin.

Requires python3-libdnf5 5.2.0.0+.

list / elements=string

Repoid of repositories to enable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a ,.

list / elements=string

Package name(s) to exclude when state=present or state=latest. This can be a list or a comma separated string.

This is effectively a no-op in DNF as it is not needed with DNF.

This option is deprecated and will be removed in ansible-core 2.20.

Will also install all packages linked by a weak dependency relation.

Specifies an alternative installroot, relative to which all packages will be installed.

Various (non-idempotent) commands for usage with /usr/bin/ansible and not playbooks. Use ansible.builtin.package_facts instead of the list argument as a best practice.

This is currently a no-op as dnf5 does not provide an option to configure it.

Amount of time to wait for the dnf lockfile to be freed.

list / elements=string

A package name or package specifier with version, like name-1.0. When using state=latest, this can be * which means run: dnf -y update. You can also pass a url or a local path to an rpm file. To operate on several packages this can accept a comma separated string of packages or a list of packages.

Comparison operators for package version are valid here >, <, >=, <=. Example - name >= 1.0. Spaces around the operator are required.

You can also pass an absolute path for a binary which is provided by the package to install. See examples for more information.

This is the opposite of the best option kept for backwards compatibility.

Since ansible-core 2.17 the default value is set by the operating system distribution.

Specifies an alternative release from which all packages will be installed.

If set to true, and state=latest then only installs updates that have been marked security related.

Note that, similar to dnf upgrade-minimal, this filter applies to dependencies as well.

Skip all unavailable packages or packages with broken dependencies without raising an error. Equivalent to passing the --skip-broken option.

Disables SSL validation of the repository server for this transaction.

This should be set to false if one of the configured repositories is using an untrusted or self-signed certificate.

Whether to install (present, latest), or remove (absent) a package.

Default is None, however in effect the default action is present unless the autoremove=true, then absent is inferred.

aliases: expire-cache

Force dnf to check if cache is out of date and redownload if needed. Has an effect only if state=present or state=latest.

When using latest, only update installed packages. Do not install packages.

Has an effect only if state=present or state=latest.

This is effectively a no-op in the dnf5 module as dnf5 itself handles downloading a https url as the source of the rpm, but is an accepted parameter for feature parity/compatibility with the ansible.builtin.dnf module.

dnf5 has 2 action plugins that use it under the hood, ansible.builtin.dnf and ansible.builtin.package.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

If the interpreter can’t import python3-libdnf5 the module will check for it in system-owned interpreters as well. If the dependency can’t be found, depending on the value of auto_install_module_deps the module will attempt to install it. If the dependency is found or installed, the module will be respawned under the correct interpreter.

Common return values are documented here, the following are the fields unique to this module:

list / elements=string

A list of the dnf transaction failures

Sample: ["Argument 'lsof' matches only excluded packages."]

Additional information about the result

Sample: "Nothing to do"

For compatibility, 0 for success, 1 for failure

list / elements=string

A list of the dnf transaction results

Sample: ["Installed: lsof-4.94.0-4.fc37.x86_64"]

**Examples:**

Example 1 (unknown):
```unknown
- name: Install the latest version of Apache
  ansible.builtin.dnf5:
    name: httpd
    state: latest

- name: Install Apache >= 2.4
  ansible.builtin.dnf5:
    name: httpd >= 2.4
    state: present

- name: Install the latest version of Apache and MariaDB
  ansible.builtin.dnf5:
    name:
      - httpd
      - mariadb-server
    state: latest

- name: Remove the Apache package
  ansible.builtin.dnf5:
    name: httpd
    state: absent

- name: Install the latest version of Apache from the testing repo
  ansible.builtin.dnf5:
    name: httpd
    enablerepo: testing
    state: present

- name: Upgrade all packages
  ansible.builtin.dnf5:
    name: "*"
    state: latest

- name: Update the webserver, depending on which is installed on the system. Do not install the other one
  ansible.builtin.dnf5:
    name:
      - httpd
      - nginx
    state: latest
    update_only: yes

- name: Install the nginx rpm from a remote repo
  ansible.builtin.dnf5:
    name: 'http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm'
    state: present

- name: Install nginx rpm from a local file
  ansible.builtin.dnf5:
    name: /usr/local/src/nginx-release-centos-6-0.el6.ngx.noarch.rpm
    state: present

- name: Install Package based upon the file it provides
  ansible.builtin.dnf5:
    name: /usr/bin/cowsay
    state: present

- name: Install the 'Development tools' package group
  ansible.builtin.dnf5:
    name: '@Development tools'
    state: present

- name: Autoremove unneeded packages installed as dependencies
  ansible.builtin.dnf5:
    autoremove: yes

- name: Uninstall httpd but keep its dependencies
  ansible.builtin.dnf5:
    name: httpd
    state: absent
    autoremove: no
```

---

## ansible.builtin.bool filter – coerce some well-known truthy/falsy values to a boolean — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/bool_filter.html

**Contents:**
- ansible.builtin.bool filter – coerce some well-known truthy/falsy values to a boolean
- Synopsis
- Input
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name bool. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.bool for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Attempt to convert the input value into a boolean (True or False) from a common set of well-known values.

Valid true values are (True, ‘yes’, ‘on’, ‘1’, ‘true’, 1).

Valid false values are (False, ‘no’, ‘off’, ‘0’, ‘false’, 0).

A deprecation warning will result if an invalid value is supplied.

For more permissive boolean conversion, consider the ansible.builtin.truthy or ansible.builtin.falsy tests.

String comparisons are case-insensitive.

Aliases: formerly_core_filter, formerly_core_masked_filter

This describes the input of the filter, the value before | ansible.builtin.bool.

The boolean result of coercing the input expression to a True or False value.

**Examples:**

Example 1 (unknown):
```unknown
# in vars
vars:
  isbool: "{{ (a == b) | bool }} "
  otherbool: "{{ anothervar | bool }} "

# in a task
...
when: some_string_value | bool
```

---

## ansible.builtin.from_json filter – Convert JSON string into variable structure — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/from_json_filter.html

**Contents:**
- ansible.builtin.from_json filter – Convert JSON string into variable structure
- Synopsis
- Input
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name from_json. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.from_json for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Converts a JSON string representation into an equivalent structured Ansible variable.

Ansible automatically converts JSON strings into variable structures in most contexts, use this plugin in contexts where automatic conversion does not happen.

This describes the input of the filter, the value before | ansible.builtin.from_json.

This filter functions as a wrapper to the Python json.loads function.

The variable resulting from deserialization of the JSON document.

**Examples:**

Example 1 (unknown):
```unknown
# variable from string variable containing a JSON document
{{ docker_config | from_json }}

# variable from string JSON document
{{ '{"a": true, "b": 54, "c": [1,2,3]}' | from_json }}
```

---

## ansible.builtin.indexed_items lookup – rewrites lists to return ‘indexed items’ — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/indexed_items_lookup.html

**Contents:**
- ansible.builtin.indexed_items lookup – rewrites lists to return ‘indexed items’
- Synopsis
- Terms
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name indexed_items. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.indexed_items for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

use this lookup if you want to loop over an array and also get the numeric index of where you are in the array as you go

any list given will be transformed with each resulting element having the it’s previous position in item.0 and its value in item.1

list with each item.0 giving you the position and item.1 the value

**Examples:**

Example 1 (unknown):
```unknown
- name: indexed loop demo
  ansible.builtin.debug:
    msg: "at array position {{ item.0 }} there is a value {{ item.1 }}"
  with_indexed_items:
    - "{{ some_list }}"
```

---

## ansible.builtin.import_tasks module – Import a task list — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/import_tasks_module.html

**Contents:**
- ansible.builtin.import_tasks module – Import a task list
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name import_tasks even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.import_tasks for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Imports a list of tasks to be added to the current playbook for subsequent execution.

Specifies the name of the file that lists tasks to add to the current playbook.

Specifies the name of the imported file directly without any other option - import_tasks: file.yml.

Most keywords, including loops and conditionals, only apply to the imported tasks, not to this statement itself.

If you need any of those to apply, use ansible.builtin.include_tasks instead.

While this action executes locally on the controller it is not governed by an action plugin

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Is usable alongside become keywords

While the import can be host specific and runs per host it is not dealing with all available host variables, use an include instead for those cases

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

The task itself is not looped, but the loop is applied to each imported task

These tasks ignore the loop and with_ keywords

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Uses the target’s configured connection information to execute code on it

This is a ‘core engine’ feature and is not implemented like most task actions, so it is not overridable in any way via the plugin system.

Since there are no connection nor facts, there is no sense in delegating imports

Can be used in conjunction with delegate_to and related keywords

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

While the action itself will ignore the conditional, it will be inherited by the imported tasks themselves

The action is not subject to conditional execution so it will ignore the when: keyword

Target OS/families that can be operated against

Tags are not interpreted for this action, they are applied to the imported tasks

Allows for the ‘tags’ keyword to control the selection of this action for execution

Denotes if this action obeys until/retry/poll keywords

This is a core feature of Ansible, rather than a module, and cannot be overridden like a module

Import a role into a play.

Load and execute a role.

Dynamically include a task list.

More information related to including and importing playbooks, roles and tasks.

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: task1

    - name: Include task list in play
      ansible.builtin.import_tasks:
        file: stuff.yaml

    - ansible.builtin.debug:
        msg: task10

- hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: task1

    - name: Apply conditional to all imported tasks
      ansible.builtin.import_tasks: stuff.yaml
      when: hostvar is defined
```

---

## ansible.builtin.yum_repository module – Add or remove YUM repositories — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/yum_repository_module.html

**Contents:**
- ansible.builtin.yum_repository module – Add or remove YUM repositories
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name yum_repository even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.yum_repository for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Add or remove YUM repositories in RPM-based Linux distributions.

If you wish to update an existing repository definition use community.general.ini_file instead.

If set to true Yum will download packages and metadata from this repo in parallel, if possible.

In ansible-core 2.11, 2.12, and 2.13 the default value is true.

This option has been removed in RHEL 8. If you’re using one of the versions listed above, you can set this option to null to avoid passing an unknown configuration option.

This parameter is deprecated as it has been removed on systems supported by ansible-core and will be removed in ansible-core 2.22.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Maximum available network bandwidth in bytes/second. Used with the throttle option.

If throttle is a percentage and bandwidth is 0 then bandwidth throttling will be disabled. If throttle is expressed as a data rate (bytes/sec) then this option is ignored. Default is 0 (no bandwidth throttling).

list / elements=string

URL to the directory where the yum repository’s ‘repodata’ directory lives.

It can also be a list of multiple URLs.

This, the metalink or mirrorlist parameters are required if state is set to present.

Relative cost of accessing this repository. Useful for weighing one repo’s packages as greater/less than any other.

added in ansible-core 2.18

Whether a special flag should be added to a randomly chosen metalink/mirrorlist query each week. This allows the repository owner to estimate the number of systems consuming it.

deltarpm_metadata_percentage

When the relative size of deltarpm metadata vs pkgs is larger than this, deltarpm metadata is not downloaded from the repo. Note that you can give values over 100, so 200 means that the metadata is required to be half the size of the packages. Use 0 to turn off this check, and always download metadata.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

When the relative size of delta vs pkg is larger than this, delta is not used. Use 0 to turn off delta rpm processing. Local repositories (with file://baseurl) have delta rpms turned off by default.

A human-readable string describing the repository. This option corresponds to the name property in the repo file.

This parameter is only required if state=present.

This tells yum whether or not use this repository.

Yum default value is true.

Determines whether yum will allow the use of package groups for this repository.

Yum default value is true.

list / elements=string

List of packages to exclude from updates or installs. This should be a space separated list. Shell globs using wildcards (for example * and ?) are allowed.

The list can also be a regular YAML array.

excludepkgs alias was added in ansible-core 2.18.

roundrobin randomly selects a URL out of the list of URLs to start with and proceeds through each of them as it encounters a failure contacting the host.

priority starts from the first baseurl listed and reads through them sequentially.

File name without the .repo extension to save the repo in. Defaults to the value of name.

A URL pointing to the ASCII-armored CA key file for the repository.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Tells yum whether or not it should perform a GPG signature check on packages.

No default setting. If the value is not set, the system setting from /etc/yum.conf or system default of false will be used.

list / elements=string

A URL pointing to the ASCII-armored GPG key file for the repository.

It can also be a list of multiple URLs.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

Determines how upstream HTTP caches are instructed to handle any HTTP downloads that Yum does.

all means that all HTTP downloads should be cached.

packages means that only RPM package downloads should be cached (but not repository metadata downloads).

none means that no HTTP downloads should be cached.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Include external configuration file. Both, local path and URL is supported. Configuration file will be inserted at the position of the include= line. Included files may contain further include lines. Yum will abort with an error if an inclusion loop is detected.

list / elements=string

List of packages you want to only use from a repository. This should be a space separated list. Shell globs using wildcards (for example * and ?) are allowed. Substitution variables (for example $releasever) are honored here.

The list can also be a regular YAML array.

Determines how yum resolves host names.

4 or IPv4 - resolve to IPv4 addresses only.

6 or IPv6 - resolve to IPv6 addresses only.

This tells yum whether or not HTTP/1.1 keepalive should be used with this repository. This can improve transfer speeds by using one connection when downloading multiple files from a repository.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Either 1 or 0. Determines whether or not yum keeps the cache of headers and packages after successful installation.

This parameter is deprecated as it is only valid in the main configuration and will be removed in ansible-core 2.20.

Time (in seconds) after which the metadata will expire.

Default value is 6 hours.

metadata_expire_filter

Filter the metadata_expire time, allowing a trade of speed for accuracy if a command doesn’t require it. Each yum command can specify that it requires a certain level of timeliness quality from the remote repos. from “I’m about to install/upgrade, so this better be current” to “Anything that’s available is good enough”.

never - Nothing is filtered, always obey metadata_expire.

read-only:past - Commands that only care about past information are filtered from metadata expiring. Eg. yum history info (if history needs to lookup anything about a previous transaction, then by definition the remote package was available in the past).

read-only:present - Commands that are balanced between past and future. Eg. yum list yum.

read-only:future - Commands that are likely to result in running other commands which will require the latest metadata. Eg. yum check-update.

Note that this option does not override yum clean expire-cache.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Specifies a URL to a metalink file for the repomd.xml, a list of mirrors for the entire repository are generated by converting the mirrors for the repomd.xml file to a baseurl.

This, the baseurl or mirrorlist parameters are required if state is set to present.

Specifies a URL to a file containing a list of baseurls.

This, the baseurl or metalink parameters are required if state is set to present.

Time (in seconds) after which the mirrorlist locally cached will expire.

Default value is 6 hours.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

added in ansible-core 2.11

Disable module RPM filtering and make all RPMs from the repository available. The default is null.

Unique repository ID. This option builds the section name of the repository in the repo file.

This parameter is only required if state is set to present or absent.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

Password to use with the username for basic authentication.

Enforce ordered protection of repositories. The value is an integer from 1 to 99.

This option only works if the YUM Priorities plugin is installed.

Protect packages from updates from other repositories.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

URL to the proxy server that yum should use. Set to _none_ to disable the global proxy setting.

Password for this proxy.

Username to use for proxy.

This tells yum whether or not it should perform a GPG signature check on the repodata from this repository.

Directory where the .repo files will be stored.

Default: "/etc/yum.repos.d"

Set the number of times any attempt to retrieve a file should retry before returning an error. Setting this to 0 makes yum try forever.

Enables support for S3 repositories.

This option only works if the YUM S3 plugin is installed.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

If set to true yum will continue running if this repository cannot be contacted for any reason. This should be set carefully as all repos are consulted for any given command.

ssl_check_cert_permissions

Whether yum should check the permissions on the paths for the certificates on the repository (both remote and local).

If we can’t read any of the files then yum will force skip_if_unavailable to be true. This is most useful for non-root processes which use yum on repos that have client cert files which are readable only by root.

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Path to the directory containing the databases of the certificate authorities yum should use to verify SSL certificates.

Path to the SSL client certificate yum should use to connect to repos/remote sites.

Path to the SSL client key yum should use to connect to repos/remote sites.

aliases: validate_certs

Defines whether yum should verify SSL certificates/hosts at all.

State of the repo file.

"present" ← (default)

Enable bandwidth throttling for downloads.

This option can be expressed as a absolute data rate in bytes/sec. An SI prefix (k, M or G) may be appended to the bandwidth value.

Number of seconds to wait for a connection before timing out.

When a repository id is displayed, append these yum variables to the string if they are used in the baseurl/etc. Variables are appended in the order listed (and found).

This parameter is deprecated as it has no effect with dnf as an underlying package manager and will be removed in ansible-core 2.22.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

Username to use for basic authentication to a repo or really any url.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

All comments will be removed if modifying an existing repo file.

Section order is preserved in an existing repo file.

Parameters in a section are ordered alphabetically in an existing repo file.

The repo file will be automatically deleted if it contains no repository.

When removing a repository, beware that the metadata cache may still remain on disk until you run yum clean all. Use a notification handler for this.

The params parameter was removed in Ansible 2.5 due to circumventing Ansible’s parameter handling

Common return values are documented here, the following are the fields unique to this module:

state of the target, after execution

**Examples:**

Example 1 (unknown):
```unknown
- name: Add repository
  ansible.builtin.yum_repository:
    name: epel
    description: EPEL YUM repo
    baseurl: https://download.fedoraproject.org/pub/epel/$releasever/$basearch/

- name: Add multiple repositories into the same file (1/2)
  ansible.builtin.yum_repository:
    name: epel
    description: EPEL YUM repo
    file: external_repos
    baseurl: https://download.fedoraproject.org/pub/epel/$releasever/$basearch/
    gpgcheck: no

- name: Add multiple repositories into the same file (2/2)
  ansible.builtin.yum_repository:
    name: rpmforge
    description: RPMforge YUM repo
    file: external_repos
    baseurl: http://apt.sw.be/redhat/el7/en/$basearch/rpmforge
    mirrorlist: http://mirrorlist.repoforge.org/el7/mirrors-rpmforge
    enabled: no

# Handler showing how to clean yum metadata cache
- name: yum-clean-metadata
  ansible.builtin.command: yum clean metadata

# Example removing a repository and cleaning up metadata cache
- name: Remove repository (and clean up left-over metadata)
  ansible.builtin.yum_repository:
    name: epel
    state: absent
  notify: yum-clean-metadata

- name: Remove repository from a specific repo file
  ansible.builtin.yum_repository:
    name: epel
    file: external_repos
    state: absent
```

---

## ansible.builtin.log filter – log of (math operation) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/log_filter.html

**Contents:**
- ansible.builtin.log filter – log of (math operation)
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name log. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.log for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Math operation that returns the logarithm to base N of the input number.

By default, computes the natural logarithm.

This describes the input of the filter, the value before | ansible.builtin.log.

Number to operate on.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.log(positional1, positional2, ...)

Which base to use. Defaults to Euler’s number.

Default: 2.718281828459045

This is a passthrough to Python’s math.log.

**Examples:**

Example 1 (unknown):
```unknown
# 1.2920296742201791
eightlogfive: "{{ 8 | log(5) }}"

# 0.9030899869919435
eightlog10: "{{ 8 | log() }}"
```

---

## ansible.builtin.combine filter – combine two dictionaries — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/combine_filter.html

**Contents:**
- ansible.builtin.combine filter – combine two dictionaries
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name combine. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.combine for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Create a dictionary (hash/associative array) as a result of merging existing dictionaries.

This describes the input of the filter, the value before | ansible.builtin.combine.

dictionary / required

First dictionary to combine.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.combine(positional1, positional2, ...)

list / elements=dictionary / required

The list of dictionaries to combine.

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.combine(key1=value1, key2=value2, ...)

Behavior when encountering list elements.

"append": append newer entries to the older ones

"append_rp": append newer entries to the older ones, overwrite duplicates

"keep": discard newer entries

"prepend": insert newer entries in front of the older ones

"prepend_rp": insert newer entries in front of the older ones, discard duplicates

"replace" (default): overwrite older entries with newer ones

If True, merge elements recursively.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.combine(positional1, positional2, key1=value1, key2=value2)

Resulting merge of supplied dictionaries.

**Examples:**

Example 1 (javascript):
```javascript
# ab => {'a':1, 'b':3, 'c': 4}
ab: {{ {'a':1, 'b':2} | ansible.builtin.combine({'b':3, 'c':4}) }}

many: "{{ dict1 | ansible.builtin.combine(dict2, dict3, dict4) }}"

# defaults => {'a':{'b':3, 'c':4}, 'd': 5}
# customization => {'a':{'c':20}}
# final => {'a':{'b':3, 'c':20}, 'd': 5}
final: "{{ defaults | ansible.builtin.combine(customization, recursive=true) }}"
```

---

## ansible.builtin.shell module – Execute shell commands on targets — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/shell_module.html

**Contents:**
- ansible.builtin.shell module – Execute shell commands on targets
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name shell even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.shell for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.shell module takes the command name followed by a list of space-delimited arguments.

Either a free form command or cmd parameter is required, see the examples.

It is almost exactly like the ansible.builtin.command module but runs the command through a shell (/bin/sh) on the remote node.

For Windows targets, use the ansible.windows.win_shell module instead.

This module has a corresponding action plugin.

Change into this directory before running the command.

The command to run followed by optional arguments.

A filename, when it already exists, this step will not be run.

Change the shell used to execute the command.

This expects an absolute path to the executable.

The shell module takes a free form command to run, as a string.

There is no actual parameter named ‘free form’.

See the examples on how to use this module.

A filename, when it does not exist, this step will not be run.

Set the stdin of the command directly to the specified value.

Whether to append a newline to stdin data.

while the command itself is arbitrary and cannot be subject to the check mode semantics it adds creates/removes options as a workaround

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Indicates if an action takes a ‘raw’ or ‘free form’ string as an option and has it’s own special parsing of it

If you want to execute a command securely and predictably, it may be better to use the ansible.builtin.command module instead. Best practices when writing playbooks will follow the trend of using ansible.builtin.command unless the ansible.builtin.shell module is explicitly required. When running ad-hoc commands, use your best judgement.

To sanitize any variables passed to the shell module, you should use {{ var | quote }} instead of just {{ var }} to make sure they do not include evil things like semicolons.

An alternative to using inline shell scripts with this module is to use the ansible.builtin.script module possibly together with the ansible.builtin.template module.

For rebooting systems, use the ansible.builtin.reboot or ansible.windows.win_reboot module.

If the command returns non UTF-8 data, it must be encoded to avoid issues. One option is to pipe the output through base64.

Execute commands on targets.

Executes a low-down and dirty command.

Runs a local script on a remote node after transferring it.

The official documentation on the ansible.windows.win_shell module.

Common return values are documented here, the following are the fields unique to this module:

The command executed by the task.

Sample: "rabbitmqctl join_cluster rabbit@master"

The command execution delta time.

Sample: "0:00:00.325771"

The command execution end time.

Sample: "2016-02-25 09:18:26.755339"

The command return code (0 means success).

The command execution start time.

Sample: "2016-02-25 09:18:26.429568"

The command standard error.

Sample: "ls: cannot access foo: No such file or directory"

list / elements=string

The command standard error split in lines.

Sample: [{"u'ls cannot access foo": "No such file or directory'"}, "u'ls \u2026'"]

The command standard output.

Sample: "Clustering node rabbit@slave1 with rabbit@master \u2026"

list / elements=string

The command standard output split in lines.

Sample: ["u'Clustering node rabbit@slave1 with rabbit@master \u2026'"]

**Examples:**

Example 1 (unknown):
```unknown
- name: Execute the command in remote shell; stdout goes to the specified file on the remote
  ansible.builtin.shell: somescript.sh >> somelog.txt

- name: Change the working directory to somedir/ before executing the command
  ansible.builtin.shell: somescript.sh >> somelog.txt
  args:
    chdir: somedir/

# You can also use the 'args' form to provide the options.
- name: This command will change the working directory to somedir/ and will only run when somedir/somelog.txt doesn't exist
  ansible.builtin.shell: somescript.sh >> somelog.txt
  args:
    chdir: somedir/
    creates: somelog.txt

# You can also use the 'cmd' parameter instead of free form format.
- name: This command will change the working directory to somedir/
  ansible.builtin.shell:
    cmd: ls -l | grep log
    chdir: somedir/

- name: Run a command that uses non-posix shell-isms (in this example /bin/sh doesn't handle redirection and wildcards together but bash does)
  ansible.builtin.shell: cat < /tmp/*txt
  args:
    executable: /bin/bash

- name: Run a command using a templated variable (always use quote filter to avoid injection)
  ansible.builtin.shell: cat {{ myfile|quote }}

# You can use shell to run other executables to perform actions inline
- name: Run expect to wait for a successful PXE boot via out-of-band CIMC
  ansible.builtin.shell: |
    set timeout 300
    spawn ssh admin@{{ cimc_host }}

    expect "password:"
    send "{{ cimc_password }}\n"

    expect "\n{{ cimc_name }}"
    send "connect host\n"

    expect "pxeboot.n12"
    send "\n"

    exit 0
  args:
    executable: /usr/bin/expect
  delegate_to: localhost
```

---

## ansible.builtin.zip_longest filter – combine list elements, with filler — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/zip_longest_filter.html

**Contents:**
- ansible.builtin.zip_longest filter – combine list elements, with filler
- Synopsis
- Input
- Positional parameters
- Keyword parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name zip_longest. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.zip_longest for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Make an iterator that aggregates elements from each of the iterables. If the iterables are of uneven length, missing values are filled-in with fillvalue. Iteration continues until the longest iterable is exhausted.

This describes the input of the filter, the value before | ansible.builtin.zip_longest.

list / elements=any / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.zip_longest(positional1, positional2, ...)

list / elements=any / required

This describes keyword parameters of the filter. These are the values key1=value1, key2=value2 and so on in the following example: input | ansible.builtin.zip_longest(key1=value1, key2=value2, ...)

Filler value to add to output when one of the lists does not contain enough elements to match the others.

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: input | ansible.builtin.zip_longest(positional1, positional2, key1=value1, key2=value2)

This is mostly a passthrough to Python’s itertools.zip_longest function

List of lists made of elements matching the positions of the input lists.

**Examples:**

Example 1 (javascript):
```javascript
# X_fill => [[1, "a", 21], [2, "b", 22], [3, "c", 23], ["X", "d", "X"], ["X", "e", "X"], ["X", "f", "X"]]
X_fill: "{{ [1,2,3] | zip_longest(['a','b','c','d','e','f'], [21, 22, 23], fillvalue='X') }}"
```

---

## ansible.builtin.mount_facts module – Retrieve mount information. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/mount_facts_module.html

**Contents:**
- ansible.builtin.mount_facts module – Retrieve mount information.
- Synopsis
- Parameters
- Attributes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name mount_facts even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.mount_facts for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

New in ansible-core 2.18

Retrieve information about mounts from preferred sources and filter the results based on the filesystem type and device.

list / elements=string

A list of fnmatch patterns to filter mounts by the special device or remote file system.

list / elements=string

A list of fnmatch patterns to filter mounts by the type of the file system.

include_aggregate_mounts

Whether or not the module should return the aggregate_mounts list in ansible_facts.

When this is null, a warning will be emitted if multiple mounts for the same mount point are found.

The mount_binary is used if sources contain the value “mount”, or if sources contains a dynamic source, and none were found (as can be expected on BSD or AIX hosts).

Set to null to stop after no dynamic file source is found instead.

The action to take when gathering mount information exceeds timeout.

list / elements=string

A list of sources used to determine the mounts. Missing file sources (or empty files) are skipped. Repeat sources, including symlinks, are skipped.

The mount_points return value contains the first definition found for a mount point.

Additional mounts to the same mount point are available from aggregate_mounts (if enabled).

By default, mounts are retrieved from all of the standard locations, which have the predefined aliases all/static/dynamic.

all contains dynamic and static.

dynamic contains /etc/mtab, /proc/mounts, /etc/mnttab, and the value of mount_binary if it is not None. This allows platforms like BSD or AIX, which don’t have an equivalent to /proc/mounts, to collect the current mounts by default. See the mount_binary option to disable the fall back or configure a different executable.

static contains /etc/fstab, /etc/vfstab, and /etc/filesystems. Note that /etc/filesystems is specific to AIX. The Linux file by this name has a different format/purpose and is ignored.

The value of mount_binary can be configured as a source, which will cause it to always execute. Depending on the other sources configured, this could be inefficient/redundant. For example, if /proc/mounts and mount are listed as sources, Linux hosts will retrieve the same mounts twice.

This is the maximum number of seconds to wait for each mount to complete. When this is null, wait indefinitely.

Configure in conjunction with on_timeout to skip unresponsive mounts.

This timeout also applies to the mount_binary command to list mounts.

If the module is configured to run during the play’s fact gathering stage, set a timeout using module_defaults to prevent a hang (see example).

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Sloane Hertel (@s-hertel)

**Examples:**

Example 1 (unknown):
```unknown
- name: Get non-local devices
  mount_facts:
    devices: "[!/]*"

- name: Get FUSE subtype mounts
  mount_facts:
    fstypes:
      - "fuse.*"

- name: Get NFS mounts during gather_facts with timeout
  hosts: all
  gather_facts: true
  vars:
    ansible_facts_modules:
      - ansible.builtin.mount_facts
  module_default:
    ansible.builtin.mount_facts:
      timeout: 10
      fstypes:
        - nfs
        - nfs4

- name: Get mounts from a non-default location
  mount_facts:
    sources:
      - /usr/etc/fstab

- name: Get mounts from the mount binary
  mount_facts:
    sources:
      - mount
    mount_binary: /sbin/mount
```

---

## ansible.builtin.join filter – Return a string which is the concatenation of the strings in the sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/join_filter.html

**Contents:**
- ansible.builtin.join filter – Return a string which is the concatenation of the strings in the sequence.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name join. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.join for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a string which is the concatenation of the strings in the sequence.

This is the Jinja builtin filter plugin ‘join’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.join

---

## ansible.builtin.host_group_vars vars – In charge of loading group_vars and host_vars — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/host_group_vars_vars.html

**Contents:**
- ansible.builtin.host_group_vars vars – In charge of loading group_vars and host_vars
- Synopsis
- Requirements
- Parameters
  - Collection links

This vars plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name host_group_vars. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.host_group_vars for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same vars plugin name.

Loads YAML vars into corresponding groups/hosts in group_vars/ and host_vars/ directories.

Files are restricted by extension to one of .yaml, .json, .yml or no extension.

Hidden (starting with ‘.’) and backup (ending with ‘~’) files and directories are ignored.

Only applies to inventory sources that are existing paths.

Starting in 2.10, this plugin requires enabling and is enabled by default.

The below requirements are needed on the local controller node that executes this vars.

Enabled in configuration

list / elements=string

Check all of these extensions when looking for ‘variable’ files which should be YAML or JSON or vaulted versions of these.

This affects vars_files, include_vars, inventory and vars plugins among others.

Default: [".yml", ".yaml", ".json"]

Environment variable: ANSIBLE_YAML_FILENAME_EXT

added in ansible-base 2.10

Control when this vars plugin may be executed.

Setting this option to all will run the vars plugin after importing inventory and whenever it is demanded by a task.

Setting this option to task will only run the vars plugin whenever it is demanded by a task.

Setting this option to inventory will only run the vars plugin after parsing inventory.

If this option is omitted, the global RUN_VARS_PLUGINS configuration is used to determine when to execute the vars plugin.

Environment variable: ANSIBLE_VARS_PLUGIN_STAGE

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
yaml_valid_extensions = .yml, .yaml, .json
```

Example 2 (unknown):
```unknown
[vars_host_group_vars]
stage = VALUE
```

---

## ansible.builtin.file lookup – read file contents — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/file_lookup.html

**Contents:**
- ansible.builtin.file lookup – read file contents
- Synopsis
- Terms
- Keyword parameters
- Notes
- See Also
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name file. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.file for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

This lookup returns the contents from a file on the Ansible controller’s file system.

path(s) of files to read

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.file', key1=value1, key2=value2, ...) and query('ansible.builtin.file', key1=value1, key2=value2, ...)

whether or not to remove whitespace from the beginning of the looked-up file

whether or not to remove whitespace from the ending of the looked-up file

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.file', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.file', term1, term2, key1=value1, key2=value2)

this lookup does not understand ‘globbing’, use the fileglob lookup instead.

Search paths used for relative files.

list / elements=string

Daniel Hokka Zakrisson

**Examples:**

Example 1 (unknown):
```unknown
- ansible.builtin.debug:
    msg: "the value of foo.txt is {{ lookup('ansible.builtin.file', '/etc/foo.txt') }}"

- name: display multiple file contents
  ansible.builtin.debug: var=item
  with_file:
    - "/path/to/foo.txt"
    - "bar.txt"  # will be looked in files/ dir relative to play or in role
    - "/path/to/biz.txt"
```

---

## ansible.builtin.started test – Was async task started — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/started_test.html

**Contents:**
- ansible.builtin.started test – Was async task started
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name started. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.started for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Used to check if an async task has started, will also work with non async tasks but will issue a warning.

This test checks for the existence of a started key in the input dictionary and that it is 1 if present

This describes the input of the test, the value before is ansible.builtin.started or is not ansible.builtin.started.

dictionary / required

registered result from an Ansible task

Returns True if the task has started, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ (asynctaskpoll is started}}
```

---

## ansible.builtin.lines lookup – read lines from command — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lines_lookup.html

**Contents:**
- ansible.builtin.lines lookup – read lines from command
- Synopsis
- Terms
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name lines. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lines for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Run one or more commands and split the output into lines, returning them as a list

The given commands are passed to a shell for execution, therefore all variables that are part of the commands and come from a remote/untrusted source MUST be sanitized using the ansible.builtin.quote filter to avoid shell injection vulnerabilities. See the example section.

Like all lookups, this runs on the Ansible controller and is unaffected by other keywords such as ‘become’. If you need to use different permissions, you must change the command or run Ansible as another user.

Alternatively, you can use a shell/command task that runs against localhost and registers the result.

The directory of the play is used as the current working directory.

list / elements=string

lines of stdout from command

Daniel Hokka Zakrisson

**Examples:**

Example 1 (unknown):
```unknown
- name: We could read the file directly, but this shows output from command
  ansible.builtin.debug: msg="{{ item }} is an output line from running cat on /etc/motd"
  with_lines: cat /etc/motd

- name: Always use quote filter to make sure your variables are safe to use with shell
  ansible.builtin.debug: msg="{{ item }} is an output line from running given command"
  with_lines: "cat {{ file_name | quote }}"

- name: More useful example of looping over a command result
  ansible.builtin.shell: "/usr/bin/frobnicate {{ item }}"
  with_lines:
    - "/usr/bin/frobnications_per_host --param {{ inventory_hostname }}"
```

---

## ansible.builtin.command module – Execute commands on targets — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/command_module.html

**Contents:**
- ansible.builtin.command module – Execute commands on targets
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name command even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.command for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

The ansible.builtin.command module takes the command name followed by a list of space-delimited arguments.

The given command will be executed on all selected nodes.

The command(s) will not be processed through the shell, so operations like "*", "<", ">", "|", ";" and "&" will not work. Also, environment variables are resolved via Python, not shell, see expand_argument_vars and are left unchanged if not matched. Use the ansible.builtin.shell module if you need these features.

To create command tasks that are easier to read than the ones using space-delimited arguments, pass parameters using the args task keyword or use cmd parameter.

Either a free form command or cmd parameter is required, see the examples.

For Windows targets, use the ansible.windows.win_command module instead.

This module has a corresponding action plugin.

list / elements=string

Passes the command as a list rather than a string.

Use argv to avoid quoting values that would otherwise be interpreted incorrectly (for example “user name”).

Only the string (free form) or the list (argv) form can be provided, not both. One or the other must be provided.

Change into this directory before running the command.

A filename or (since 2.0) glob pattern. If a matching file already exists, this step will not be run.

This is checked before removes is checked.

added in ansible-core 2.16

Expands the arguments that are variables, for example $HOME will be expanded before being passed to the command to run.

If a variable is not matched, it is left unchanged, unlike shell substitution which would remove it.

Set to false to disable expansion and treat the value as a literal argument.

The command module takes a free form string as a command to run.

There is no actual parameter named free_form.

A filename or (since 2.0) glob pattern. If a matching file exists, this step will be run.

This is checked after creates is checked.

Set the stdin of the command directly to the specified value.

If set to true, append a newline to stdin data.

Strip empty lines from the end of stdout/stderr in result.

while the command itself is arbitrary and cannot be subject to the check mode semantics it adds creates/removes options as a workaround

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Indicates if an action takes a ‘raw’ or ‘free form’ string as an option and has it’s own special parsing of it

If you want to run a command through the shell (say you are using <, >, |, and so on), you actually want the ansible.builtin.shell module instead. Parsing shell metacharacters can lead to unexpected commands being executed if quoting is not done correctly so it is more secure to use the ansible.builtin.command module when possible.

creates, removes, and chdir can be specified after the command. For instance, if you only want to run a command if a certain file does not exist, use this.

Check mode is supported when passing creates or removes. If running in check mode and either of these are specified, the module will check for the existence of the file and report the correct changed status. If these are not supplied, the task will be skipped.

The executable parameter is removed since version 2.4. If you have a need for this parameter, use the ansible.builtin.shell module instead.

For Windows targets, use the ansible.windows.win_command module instead.

For rebooting systems, use the ansible.builtin.reboot or ansible.windows.win_reboot module.

If the command returns non UTF-8 data, it must be encoded to avoid issues. This may necessitate using ansible.builtin.shell so the output can be piped through base64.

Executes a low-down and dirty command.

Runs a local script on a remote node after transferring it.

Execute shell commands on targets.

The official documentation on the ansible.windows.win_command module.

Common return values are documented here, the following are the fields unique to this module:

list / elements=string

The command executed by the task.

Sample: ["echo", "hello"]

The command execution delta time.

Sample: "0:00:00.001529"

The command execution end time.

Sample: "2017-09-29 22:03:48.084657"

The command return code (0 means success).

The command execution start time.

Sample: "2017-09-29 22:03:48.083128"

The command standard error.

Sample: "ls cannot access foo: No such file or directory"

list / elements=string

The command standard error split in lines.

Sample: [{"u'ls cannot access foo": "No such file or directory'"}, "u'ls \u2026'"]

The command standard output.

Sample: "Clustering node rabbit@slave1 with rabbit@master \u2026"

list / elements=string

The command standard output split in lines.

Sample: ["u'Clustering node rabbit@slave1 with rabbit@master \u2026'"]

**Examples:**

Example 1 (unknown):
```unknown
- name: Return motd to registered var
  ansible.builtin.command: cat /etc/motd
  register: mymotd

# free-form (string) arguments, all arguments on one line
- name: Run command if /path/to/database does not exist (without 'args')
  ansible.builtin.command: /usr/bin/make_database.sh db_user db_name creates=/path/to/database

# free-form (string) arguments, some arguments on separate lines with the 'args' keyword
# 'args' is a task keyword, passed at the same level as the module
- name: Run command if /path/to/database does not exist (with 'args' keyword)
  ansible.builtin.command: /usr/bin/make_database.sh db_user db_name
  args:
    creates: /path/to/database

# 'cmd' is module parameter
- name: Run command if /path/to/database does not exist (with 'cmd' parameter)
  ansible.builtin.command:
    cmd: /usr/bin/make_database.sh db_user db_name
    creates: /path/to/database

- name: Change the working directory to somedir/ and run the command as db_owner if /path/to/database does not exist
  ansible.builtin.command: /usr/bin/make_database.sh db_user db_name
  become: yes
  become_user: db_owner
  args:
    chdir: somedir/
    creates: /path/to/database

# argv (list) arguments, each argument on a separate line, 'args' keyword not necessary
# 'argv' is a parameter, indented one level from the module
- name: Use 'argv' to send a command as a list - leave 'command' empty
  ansible.builtin.command:
    argv:
      - /usr/bin/make_database.sh
      - Username with whitespace
      - dbname with whitespace
    creates: /path/to/database

- name: Run command using argv with mixed argument formats
  ansible.builtin.command:
    argv:
      - /path/to/binary
      - -v
      - --debug
      - --longopt
      - value for longopt
      - --other-longopt=value for other longopt
      - positional

- name: Safely use templated variable to run command. Always use the quote filter to avoid injection issues
  ansible.builtin.command: cat {{ myfile|quote }}
  register: myoutput
```

---

## ansible.builtin.assemble module – Assemble configuration files from fragments — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/assemble_module.html

**Contents:**
- ansible.builtin.assemble module – Assemble configuration files from fragments
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name assemble even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.assemble for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Assembles a configuration file from fragments.

Often a particular program will take a single configuration file and does not support a conf.d style structure where it is easy to build up the configuration from multiple sources. ansible.builtin.assemble will take a directory of files that can be local or have already been transferred to the system, and concatenate them together to produce a destination file.

Files are assembled in string sorting order.

Puppet calls this idea fragments.

This module has a corresponding action plugin.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file (if true), including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

This option controls the auto-decryption of source files using vault.

A delimiter to separate the file contents.

A file to create using the concatenation of all of the source files.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

A boolean that controls if files that start with a . will be included or not.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

Assemble files only if the given regular expression matches the filename.

If not set, all files are assembled.

Every \ (backslash) must be escaped as \\ to comply to YAML syntax.

Uses Python regular expressions.

If false, it will search for src at originating/master machine.

If true, it will go to the remote/target machine for the src.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

An already existing directory full of source files.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

The validation command to run before copying into place.

The path to the file to validate is passed in by %s which must be present as in the sshd example below.

The command is passed securely so shell features like expansion and pipes won’t work.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Uses Ansible’s strict file operation functions to ensure proper permissions and avoid data corruption

Can automatically decrypt Ansible vaulted files

Copy files to remote locations.

Template a file out to a target host.

The official documentation on the ansible.windows.win_copy module.

Stephen Fromm (@sfromm)

**Examples:**

Example 1 (unknown):
```unknown
- name: Assemble from fragments from a directory
  ansible.builtin.assemble:
    src: /etc/someapp/fragments
    dest: /etc/someapp/someapp.conf

- name: Insert the provided delimiter between fragments
  ansible.builtin.assemble:
    src: /etc/someapp/fragments
    dest: /etc/someapp/someapp.conf
    delimiter: '### START FRAGMENT ###'

- name: Assemble a new "sshd_config" file into place, after passing validation with sshd
  ansible.builtin.assemble:
    src: /etc/ssh/conf.d/
    dest: /etc/ssh/sshd_config
    validate: /usr/sbin/sshd -t -f %s
```

---

## ansible.builtin.file test – does the path resolve to an existing file — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/file_test.html

**Contents:**
- ansible.builtin.file test – does the path resolve to an existing file
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name file. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.file for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Check if the provided path maps to an existing file on the controller’s filesystem (localhost)

This describes the input of the test, the value before is ansible.builtin.file or is not ansible.builtin.file.

Returns True if the path corresponds to an existing file on the filesystem on the controller, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
vars:
  my_etc_hosts_is_a_file: "{{ '/etc/hosts' is file }}"
  list_of_files: "{{ list_of_paths | select('file') }}"
```

---

## ansible.builtin.get_url module – Downloads files from HTTP, HTTPS, or FTP to node — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/get_url_module.html

**Contents:**
- ansible.builtin.get_url module – Downloads files from HTTP, HTTPS, or FTP to node
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name get_url even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.get_url for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Downloads files from HTTP, HTTPS, or FTP to the remote server. The remote server must have direct access to the remote resource.

By default, if an environment variable <protocol>_proxy is set on the target host, requests will be sent through that proxy. This behaviour can be overridden by setting a variable for this task (see setting the environment), or by using the use_proxy option.

HTTP redirects can redirect from HTTP to HTTPS so you should be sure that your proxy environment for both protocols is correct.

From Ansible 2.4 when run with --check, it will do a HEAD request to validate the URL but will not download the entire file or verify it against hashes and will report incorrect changed status.

For Windows targets, use the ansible.windows.win_get_url module instead.

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.

If a checksum is passed to this parameter, the digest of the destination file will be calculated after it is downloaded to ensure its integrity and verify that the transfer completed successfully. Format: <algorithm>:<checksum|url>, for example checksum="sha256:D98291AC[...]B6DC7B97", checksum="sha256:http://example.com/path/sha256sum.txt".

If you worry about portability, only the sha1 algorithm is available on all platforms and python versions.

The Python hashlib module is responsible for providing the available algorithms. The choices vary based on Python version and OpenSSL version.

On systems running in FIPS compliant mode, the md5 algorithm may be unavailable.

Additionally, if a checksum is passed to this parameter, and the file exist under the dest location, the destination_checksum would be calculated, and if checksum equals destination_checksum, the file download would be skipped (unless force=true). If the checksum does not equal destination_checksum, the destination file is deleted.

If the checksum URL requires username and password, url_username and url_password are used to download the checksum file.

list / elements=string

added in ansible-core 2.14

SSL/TLS Ciphers to use for the request.

When a list is provided, all ciphers are joined in order with :.

See the OpenSSL Cipher List Format for more details.

The available ciphers is dependent on the Python and OpenSSL/LibreSSL versions.

PEM formatted certificate chain file to be used for SSL client authentication.

This file can also include the key as well, and if the key is included, client_key is not required.

PEM formatted file that contains your private key to be used for SSL client authentication.

If client_cert contains both the certificate and key, this option is not required.

added in ansible-core 2.14

Whether to attempt to decompress gzip content-encoded responses.

Absolute path of where to download the file to.

If dest is a directory, either the server provided filename or, if none provided, the base name of the URL on the remote server will be used. If a directory, force has no effect.

If dest is a directory, the file will always be downloaded (regardless of the force and checksum option), but replaced only if the contents changed.

If true and dest is not a directory, will download the file every time and replace the file if the contents change. If false, the file will only be downloaded if the destination does not exist. Generally should be true only for small local files.

Prior to 0.6, this module behaved as if true was the default.

Force the sending of the Basic authentication header upon initial request.

httplib2, the library used by the uri module only sends authentication information when a webservice responds to an initial request with a 401 status. Since some basic auth services do not properly send a 401, logins will fail.

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

Add custom HTTP headers to a request in hash/dict format.

The hash/dict format was added in Ansible 2.6.

Previous versions used a "key:value,key:value" string format.

The "key:value,key:value" string format is deprecated and has been removed in version 2.10.

Header to identify as, generally appears in web server logs.

Default: "ansible-httpget"

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Timeout in seconds for URL request.

Absolute path of where temporary file is downloaded to.

When run on Ansible 2.5 or greater, path defaults to ansible’s remote_tmp setting.

When run on Ansible prior to 2.5, it defaults to TMPDIR, TEMP or TMP env variables or a platform specific value.

https://docs.python.org/3/library/tempfile.html#tempfile.tempdir.

list / elements=string

added in ansible-core 2.12

A list of header names that will not be sent on subsequent redirected requests. This list is case insensitive. By default all headers will be redirected. In some cases it may be beneficial to list headers such as Authorization here to avoid potential credential exposure.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

HTTP, HTTPS, or FTP URL in the form (http|https|ftp://[user[:pass]]@host.domain[:port]/path).

The password for use in HTTP basic authentication.

If the url_username parameter is not specified, the url_password parameter will not be used.

Since version 2.8 you can also use the password alias for this option.

The username for use in HTTP basic authentication.

This parameter can be used without url_password for sites that allow empty passwords.

Since version 2.8 you can also use the username alias for this option.

added in ansible-core 2.11

Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

Requires the Python library gssapi to be installed.

Credentials for GSSAPI can be specified with url_username/url_password or with the GSSAPI env var KRB5CCNAME that specified a custom Kerberos credential cache.

NTLM authentication is not supported even if the GSSAPI mech for NTLM has been installed.

added in ansible-core 2.14

Determining whether to use credentials from ~/.netrc file.

By default .netrc is used with Basic authentication headers.

When false, .netrc credentials are ignored.

if false, it will not use a proxy, even if one is defined in an environment variable on the target hosts.

If false, SSL certificates will not be validated.

This should only be used on personally controlled sites using self-signed certificates.

the changed status will reflect comparison to an empty source file

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

For Windows targets, use the ansible.windows.win_get_url module instead.

Interacts with webservices.

The official documentation on the ansible.windows.win_get_url module.

Common return values are documented here, the following are the fields unique to this module:

name of backup file created after download

Returned: changed and if backup=yes

Sample: "/path/to/file.txt.2015-02-12@22:09~"

sha1 checksum of the file after copy

Sample: "6e642bb8dd5c2e027bf21dd923337cbb4214f827"

sha1 checksum of the file

Sample: "6e642bb8dd5c2e027bf21dd923337cbb4214f827"

destination file/path

Sample: "/path/to/file.txt"

The number of seconds that elapsed while performing the download

md5 checksum of the file after download

Returned: when supported

Sample: "2a5aeecc61dc98c4d780b14b330e3282"

permissions of the target

the HTTP message from the request

Sample: "OK (unknown bytes)"

the SELinux security context of the file

Sample: "unconfined_u:object_r:user_tmp_t:s0"

source file used after download

Sample: "/tmp/tmpAdFLdV"

the HTTP status code from the request

owner id of the file, after execution

the actual URL used for the request

Sample: "https://www.ansible.com/"

Jan-Piet Mens (@jpmens)

**Examples:**

Example 1 (unknown):
```unknown
- name: Download foo.conf
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    mode: '0440'

- name: Download file and force basic auth
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    force_basic_auth: yes

- name: Download file with custom HTTP headers
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    headers:
      key1: one
      key2: two

- name: Download file with check (sha256)
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    checksum: sha256:b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c

- name: Download file with check (md5)
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    checksum: md5:66dffb5228a211e61d6d7ef4a86f5758

- name: Download file with checksum url (sha256)
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    checksum: sha256:http://example.com/path/sha256sum.txt

- name: Download file from a file path
  ansible.builtin.get_url:
    url: file:///tmp/a_file.txt
    dest: /tmp/afilecopy.txt

- name: < Fetch file that requires authentication.
        username/password only available since 2.8, in older versions you need to use url_username/url_password
  ansible.builtin.get_url:
    url: http://example.com/path/file.conf
    dest: /etc/foo.conf
    username: bar
    password: '{{ mysecret }}'
```

---

## ansible.builtin.upper filter – Convert a value to uppercase. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/upper_filter.html

**Contents:**
- ansible.builtin.upper filter – Convert a value to uppercase.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name upper. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.upper for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert a value to uppercase.

This is the Jinja builtin filter plugin ‘upper’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.upper

---

## ansible.builtin.deb822_repository module – Add and remove deb822 formatted repositories — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/deb822_repository_module.html

**Contents:**
- ansible.builtin.deb822_repository module – Add and remove deb822 formatted repositories
- Synopsis
- Requirements
- Parameters
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name deb822_repository even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.deb822_repository for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

New in ansible-core 2.15

Add and remove deb822 formatted repositories in Debian based distributions.

The below requirements are needed on the host that executes this module.

python3-debian / python-debian

allow_downgrade_to_insecure

Allow downgrading a package that was previously authenticated but is no longer authenticated.

Allow insecure repositories.

Allow repositories signed with a key using a weak digest algorithm.

list / elements=string

Architectures to search within repository.

Controls if APT should try to acquire indexes via a URI constructed from a hashsum of the expected file instead of using the well-known stable filename of the index.

Controls if APT should consider the machine’s time correct and hence perform time related checks, such as verifying that a Release file is not from the future.

Controls if APT should try to detect replay attacks.

list / elements=string

Components specify different sections of one distribution version present in a Suite.

Controls how far from the future a repository may be.

Tells APT whether the source is enabled or not.

Determines the path to the InRelease file, relative to the normal position of an InRelease file.

list / elements=string

Defines which languages information such as translated package descriptions should be downloaded.

The octal mode for newly created files in sources.list.d.

Name of the repo. Specifically used for X-Repolib-Name and in naming the repository and signing key files.

Controls if APT should try to use PDiffs to update old indexes instead of downloading the new indexes entirely.

Either a URL to a GPG key, absolute path to a keyring file, one or more fingerprints of keys either in the trusted.gpg keyring or in the keyrings in the trusted.gpg.d/ directory, or an ASCII armored GPG public key block.

A source string state.

"present" ← (default)

list / elements=string

Suite can specify an exact path in relation to the URI(s) provided, in which case the Components: must be omitted and suite must end with a slash (/). Alternatively, it may take the form of a distribution version (for example a version codename like disco or artful). If the suite does not specify a path, at least one component must be present.

list / elements=string

Defines which download targets apt will try to acquire from this source.

Decides if a source is considered trusted or if warnings should be raised before, for example packages are installed from this source.

list / elements=string

Which types of packages to look for from a given source; either binary deb or source code deb-src.

list / elements=string

The URIs must specify the base of the Debian distribution archive, from which APT finds the information it needs.

This module will not automatically update caches, call the ansible.builtin.apt module based on the changed state.

Common return values are documented here, the following are the fields unique to this module:

Path to the repository file

Sample: "/etc/apt/sources.list.d/focal-archive.sources"

Path to the signed_by key file

Sample: "/etc/apt/keyrings/debian.gpg"

A source string for the repository

Sample: "X-Repolib-Name: debian\nTypes: deb\nURIs: https://deb.debian.org\nSuites: stable\nComponents: main contrib non-free\nSigned-By:\n -----BEGIN PGP PUBLIC KEY BLOCK-----\n .\n mDMEYCQjIxYJKwYBBAHaRw8BAQdAD/P5Nvvnvk66SxBBHDbhRml9ORg1WV5CvzKY\n CuMfoIS0BmFiY2RlZoiQBBMWCgA4FiEErCIG1VhKWMWo2yfAREZd5NfO31cFAmAk\n IyMCGyMFCwkIBwMFFQoJCAsFFgIDAQACHgECF4AACgkQREZd5NfO31fbOwD6ArzS\n dM0Dkd5h2Ujy1b6KcAaVW9FOa5UNfJ9FFBtjLQEBAJ7UyWD3dZzhvlaAwunsk7DG\n 3bHcln8DMpIJVXht78sL\n =IE0r\n -----END PGP PUBLIC KEY BLOCK-----\n"

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- name: Add debian repo
  deb822_repository:
    name: debian
    types: deb
    uris: http://deb.debian.org/debian
    suites: stretch
    components:
      - main
      - contrib
      - non-free

- name: Add debian repo with key
  deb822_repository:
    name: debian
    types: deb
    uris: https://deb.debian.org
    suites: stable
    components:
      - main
      - contrib
      - non-free
    signed_by: |-
      -----BEGIN PGP PUBLIC KEY BLOCK-----

      mDMEYCQjIxYJKwYBBAHaRw8BAQdAD/P5Nvvnvk66SxBBHDbhRml9ORg1WV5CvzKY
      CuMfoIS0BmFiY2RlZoiQBBMWCgA4FiEErCIG1VhKWMWo2yfAREZd5NfO31cFAmAk
      IyMCGyMFCwkIBwMFFQoJCAsFFgIDAQACHgECF4AACgkQREZd5NfO31fbOwD6ArzS
      dM0Dkd5h2Ujy1b6KcAaVW9FOa5UNfJ9FFBtjLQEBAJ7UyWD3dZzhvlaAwunsk7DG
      3bHcln8DMpIJVXht78sL
      =IE0r
      -----END PGP PUBLIC KEY BLOCK-----

- name: Add repo using key from URL
  deb822_repository:
    name: example
    types: deb
    uris: https://download.example.com/linux/ubuntu
    suites: '{{ ansible_distribution_release }}'
    components: stable
    architectures: amd64
    signed_by: https://download.example.com/linux/ubuntu/gpg
```

---

## ansible.builtin.string filter – Convert an object to a string if it isn’t already. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/string_filter.html

**Contents:**
- ansible.builtin.string filter – Convert an object to a string if it isn’t already.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name string. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.string for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Convert an object to a string if it isn’t already.

This is the Jinja builtin filter plugin ‘string’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.string

---

## ansible.builtin.cron module – Manage cron.d and crontab entries — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/cron_module.html

**Contents:**
- ansible.builtin.cron module – Manage cron.d and crontab entries
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name cron even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.cron for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Use this module to manage crontab and environment variables entries. This module allows you to create environment variables and named crontab entries, update, or delete them.

When crontab jobs are managed: the module includes one line with the description of the crontab entry "#Ansible: <name>" corresponding to the name passed to the module, which is used by future ansible/module calls to find/check the state. The name parameter should be unique, and changing the name value will result in a new cron task being created (or a different one being removed).

When environment variables are managed, no comment line is added, but, when the module needs to find/check the state, it uses the name parameter to find the environment variable definition line.

When using symbols such as %, they must be properly escaped.

The below requirements are needed on the host that executes this module.

cron (any ‘vixie cron’ conformant variant, like cronie)

If set, create a backup of the crontab before it is modified. The location of the backup is returned in the backup_file variable by this module.

If specified, uses this file instead of an individual user’s crontab. The assumption is that this file is exclusively managed by the module, do not use if the file contains multiple entries, NEVER use for /etc/crontab.

If this is a relative path, it is interpreted with respect to /etc/cron.d.

Many Linux distros expect (and some require) the filename portion to consist solely of upper- and lower-case letters, digits, underscores, and hyphens.

Using this parameter requires you to specify the user as well, unless state=absent.

Either this parameter or name is required.

Day of the month the job should run (1-31, *, */2, and so on).

Cannot be combined with special_time.

If the job should be disabled (commented out) in the crontab.

Only has effect if state=present.

If set, manages a crontab’s environment variable.

New variables are added on top of crontab.

name and value parameters are the name and the value of environment variable.

Hour when the job should run (0-23, *, */2, and so on).

Cannot be combined with special_time.

Used with state=present and env.

If specified, the environment variable will be inserted after the declaration of specified environment variable.

Used with state=present and env.

If specified, the environment variable will be inserted before the declaration of specified environment variable.

The command to execute or, if env is set, the value of environment variable.

The command should not contain line breaks.

Required if state=present.

Minute when the job should run (0-59, *, */2, and so on).

Cannot be combined with special_time.

Month of the year the job should run (JAN-DEC or 1-12, *, */2, and so on).

Cannot be combined with special_time.

Description of a crontab entry or, if env is set, the name of environment variable.

This parameter is always required as of ansible-core 2.12.

Special time specification nickname.

Cannot be combined with minute, hour, day, month or weekday.

Whether to ensure the job or environment variable is present or absent.

"present" ← (default)

The specific user whose crontab should be modified.

When unset, this parameter defaults to the current user.

Day of the week that the job should run (SUN-SAT or 0-6, *, and so on).

Cannot be combined with special_time.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

If you are experiencing permissions issues with cron and MacOS, you should see the official MacOS documentation for further information.

Dane Summers (@dsummersl)

Mike Grozak (@rhaido)

Patrick Callahan (@dirtyharrycallahan)

Evan Kaufman (@EvanK)

Luca Berruti (@lberruti)

**Examples:**

Example 1 (unknown):
```unknown
- name: Ensure a job that runs at 2 and 5 exists. Creates an entry like "0 5,2 * * ls -alh > /dev/null"
  ansible.builtin.cron:
    name: "check dirs"
    minute: "0"
    hour: "5,2"
    job: "ls -alh > /dev/null"

- name: 'Ensure an old job is no longer present. Removes any job that is prefixed by "#Ansible: an old job" from the crontab'
  ansible.builtin.cron:
    name: "an old job"
    state: absent

- name: Creates an entry like "@reboot /some/job.sh"
  ansible.builtin.cron:
    name: "a job for reboot"
    special_time: reboot
    job: "/some/job.sh"

- name: Creates an entry like "PATH=/opt/bin" on top of crontab
  ansible.builtin.cron:
    name: PATH
    env: yes
    job: /opt/bin

- name: Creates an entry like "APP_HOME=/srv/app" and insert it after PATH declaration
  ansible.builtin.cron:
    name: APP_HOME
    env: yes
    job: /srv/app
    insertafter: PATH

- name: Creates a cron file under /etc/cron.d
  ansible.builtin.cron:
    name: yum autoupdate
    weekday: "2"
    minute: "0"
    hour: "12"
    user: root
    job: "YUMINTERACTIVE=0 /usr/sbin/yum-autoupdate"
    cron_file: ansible_yum-autoupdate

- name: Removes a cron file from under /etc/cron.d
  ansible.builtin.cron:
    name: "yum autoupdate"
    cron_file: ansible_yum-autoupdate
    state: absent

- name: Removes "APP_HOME" environment variable from crontab
  ansible.builtin.cron:
    name: APP_HOME
    env: yes
    state: absent
```

---

## ansible.builtin.failed test – did the task fail — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/failed_test.html

**Contents:**
- ansible.builtin.failed test – did the task fail
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name failed. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.failed for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Tests if task finished in failure, opposite of succeeded.

This test checks for the existence of a failed key in the input dictionary and that it is True if present.

Tasks that get skipped or not executed due to other failures (syntax, templating, unreachable host, etc) do not return a ‘failed’ status.

This describes the input of the test, the value before is ansible.builtin.failed or is not ansible.builtin.failed.

dictionary / required

registered result from an Ansible task

Returns True if the task was failed, False otherwise.

**Examples:**

Example 1 (unknown):
```unknown
# test 'status' to know how to respond
{{ taskresults is failed }}
```

---

## ansible.builtin.strftime filter – date formatting — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/strftime_filter.html

**Contents:**
- ansible.builtin.strftime filter – date formatting
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name strftime. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.strftime for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Using Python’s strftime function, take a data formatting string and a date/time to create a formatted date.

This describes the input of the filter, the value before | ansible.builtin.strftime.

A formatting string following stftime conventions.

See the Python documentation for a reference.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.strftime(positional1, positional2, ...)

Datetime in seconds from epoch to format, if not supplied gmttime/localtime will be used.

added in ansible-core 2.14

Whether time supplied is in UTC.

This is a passthrough to Python’s stftime, for a complete set of formatting options go to https://strftime.org/.

A formatted date/time string.

**Examples:**

Example 1 (javascript):
```javascript
# for a complete set of features go to  https://strftime.org/

# Display year-month-day
{{ '%Y-%m-%d' | strftime }}
# => "2021-03-19"

# Display hour:min:sec
{{ '%H:%M:%S' | strftime }}
# => "21:51:04"

# Use ansible_date_time.epoch fact
{{ '%Y-%m-%d %H:%M:%S' | strftime(ansible_date_time.epoch) }}
# => "2021-03-19 21:54:09"

# Use arbitrary epoch value
{{ '%Y-%m-%d' | strftime(0) }}          # => 1970-01-01
{{ '%Y-%m-%d' | strftime(seconds=1441357287, utc=true) }} # => 2015-09-04
```

---

## ansible.builtin.lessthan test – Same as a < b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lessthan_test.html

**Contents:**
- ansible.builtin.lessthan test – Same as a < b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name lessthan. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lessthan for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘lessthan’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.lessthan

---

## ansible.builtin.ssh connection – connect via SSH client binary — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ssh_connection.html

**Contents:**
- ansible.builtin.ssh connection – connect via SSH client binary
- Synopsis
- Parameters
- Notes
  - Authors
  - Collection links

This connection plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ssh. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ssh for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same connection plugin name.

This connection plugin allows Ansible to communicate to the target machines through normal SSH command line.

Ansible does not expose a channel to allow communication between the user and the SSH process to accept a password manually to decrypt an SSH key when using this connection plugin (which is the default). The use of ssh-agent is highly recommended.

This is the location to save SSH’s ControlPath sockets, it uses SSH’s variable substitution.

Since 2.3, if null (default), ansible will generate a unique hash. Use ``%(directory)s`` to indicate where to use the control dir path setting.

Before 2.3 it defaulted to ``control_path=%(directory)s/ansible-ssh-%%h-%%p-%%r``.

Be aware that this setting is ignored if -o ControlPath is set in ssh args.

Environment variable: ANSIBLE_SSH_CONTROL_PATH

Variable: ansible_control_path

This sets the directory to use for ssh control path if the control path setting is null.

Also, provides the ``%(directory)s`` variable for the control path setting.

Default: "~/.ansible/cp"

Environment variable: ANSIBLE_SSH_CONTROL_PATH_DIR

Variable: ansible_control_path_dir

Hostname/IP to connect to.

Default: "inventory_hostname"

Variable: inventory_hostname

Variable: ansible_host

Variable: ansible_ssh_host

Variable: delegated_vars[‘ansible_host’]

Variable: delegated_vars[‘ansible_ssh_host’]

Determines if SSH should reject or not a connection after checking host keys.

Environment variable: ANSIBLE_HOST_KEY_CHECKING

Environment variable: ANSIBLE_SSH_HOST_KEY_CHECKING

Variable: ansible_host_key_checking

Variable: ansible_ssh_host_key_checking

Authentication password for the remote_user. Can be supplied as CLI option.

Variable: ansible_password

Variable: ansible_ssh_pass

Variable: ansible_ssh_password

added in ansible-core 2.19

Mechanism to use for handling ssh password prompt

"ssh_askpass" ← (default)

Environment variable: ANSIBLE_SSH_PASSWORD_MECHANISM

Variable: ansible_ssh_password_mechanism

Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

This can result in a very significant performance improvement when enabled.

However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable requiretty in the sudoers file for the target hosts, which is why this feature is disabled by default.

Environment variable: ANSIBLE_PIPELINING

Environment variable: ANSIBLE_SSH_PIPELINING

Variable: ansible_pipelining

Variable: ansible_ssh_pipelining

added in ansible-core 2.12

PKCS11 SmartCard provider such as opensc, example: /usr/local/lib/opensc-pkcs11.so

Environment variable: ANSIBLE_PKCS11_PROVIDER

Variable: ansible_ssh_pkcs11_provider

Remote port to connect to.

Environment variable: ANSIBLE_REMOTE_PORT

Variable: ansible_port

Variable: ansible_ssh_port

added in ansible-core 2.19

Private key contents in PEM format. Requires the SSH_AGENT configuration to be enabled.

Environment variable: ANSIBLE_PRIVATE_KEY

Variable: ansible_private_key

Variable: ansible_ssh_private_key

Path to private key file to use for authentication.

Environment variable: ANSIBLE_PRIVATE_KEY_FILE

CLI argument: --private-key

Variable: ansible_private_key_file

Variable: ansible_ssh_private_key_file

private_key_passphrase

added in ansible-core 2.19

Private key passphrase, dependent on private_key.

This does NOT have any effect when used with private_key_file.

Environment variable: ANSIBLE_PRIVATE_KEY_PASSPHRASE

Variable: ansible_private_key_passphrase

Variable: ansible_ssh_private_key_passphrase

Number of attempts to connect.

Ansible retries connections only if it gets an SSH error with a return code of 255.

Any errors with return codes other than 255 indicate an issue with program execution.

Environment variable: ANSIBLE_SSH_RETRIES

Variable: ansible_ssh_retries

User name with which to login to the remote server, normally set by the remote_user keyword.

If no user is supplied, Ansible will let the SSH client binary choose the user as it normally.

Environment variable: ANSIBLE_REMOTE_USER

Variable: ansible_user

Variable: ansible_ssh_user

This defines the location of the scp binary. It defaults to scp which will use the first binary available in $PATH.

Environment variable: ANSIBLE_SCP_EXECUTABLE

Variable: ansible_scp_executable

Extra exclusive to the scp CLI

Environment variable: ANSIBLE_SCP_EXTRA_ARGS

CLI argument: --scp-extra-args

Variable: ansible_scp_extra_args

When set to True, sftp will be run in batch mode, allowing detection of transfer errors.

When set to False, sftp will not be run in batch mode, preventing detection of transfer errors.

Environment variable: ANSIBLE_SFTP_BATCH_MODE

Variable: ansible_sftp_batch_mode

This defines the location of the sftp binary. It defaults to sftp which will use the first binary available in $PATH.

Environment variable: ANSIBLE_SFTP_EXECUTABLE

Variable: ansible_sftp_executable

Extra exclusive to the sftp CLI

Environment variable: ANSIBLE_SFTP_EXTRA_ARGS

CLI argument: --sftp-extra-args

Variable: ansible_sftp_extra_args

Arguments to pass to all SSH CLI tools.

Default: "-C -o ControlMaster=auto -o ControlPersist=60s"

Environment variable: ANSIBLE_SSH_ARGS

Variable: ansible_ssh_args

Common extra args for all SSH CLI tools.

Environment variable: ANSIBLE_SSH_COMMON_ARGS

CLI argument: --ssh-common-args

Variable: ansible_ssh_common_args

This defines the location of the SSH binary. It defaults to ssh which will use the first SSH binary available in $PATH.

This option is usually not required, it might be useful when access to system SSH is restricted, or when using SSH wrappers to connect to remote hosts.

Environment variable: ANSIBLE_SSH_EXECUTABLE

Variable: ansible_ssh_executable

Extra exclusive to the SSH CLI.

Environment variable: ANSIBLE_SSH_EXTRA_ARGS

CLI argument: --ssh-extra-args

Variable: ansible_ssh_extra_args

Preferred method to use when transferring files over ssh

"piped": Creates an SSH pipe with dd on either side to copy the data.

"scp": Deprecated in OpenSSH. For OpenSSH >=9.0 you must add an additional option to enable scp scp_extra_args="-O".

"sftp": This is the most reliable way to copy things with SSH.

"smart" (default): Tries each method in order (sftp > scp > piped), until one succeeds or they all fail.

Environment variable: ANSIBLE_SSH_TRANSFER_METHOD

Variable: ansible_ssh_transfer_method

added in ansible-core 2.12

added in ansible-base 2.10

Password prompt that sshpass/SSH_ASKPASS should search for.

Supported by sshpass 1.06 and up when password_mechanism set to sshpass.

Defaults to Enter PIN for when pkcs11_provider is set.

Defaults to assword when password_mechanism set to ssh_askpass.

Environment variable: ANSIBLE_SSHPASS_PROMPT

Variable: ansible_sshpass_prompt

This is the default amount of time we will wait while establishing an SSH connection.

It also controls how long we can wait to access reading the connection once established (select on the socket).

added in ansible-core 2.11

Environment variable: ANSIBLE_TIMEOUT

Environment variable: ANSIBLE_SSH_TIMEOUT

added in ansible-core 2.11

CLI argument: --timeout

Variable: ansible_ssh_timeout

added in ansible-core 2.11

add -tt to ssh commands to force tty allocation.

Environment variable: ANSIBLE_SSH_USETTY

Variable: ansible_ssh_use_tty

added in ansible-core 2.19

Requested verbosity level for the SSH CLI.

Environment variable: ANSIBLE_SSH_VERBOSITY

Variable: ansible_ssh_verbosity

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

This plugin is mostly a wrapper to the ``ssh`` CLI utility and the exact behavior of the options depends on this tool. This means that the documentation provided here is subject to be overridden by the CLI tool itself.

Many options default to None here but that only means we do not override the SSH tool’s defaults and/or configuration. For example, if you specify the port in this plugin it will override any Port entry in your .ssh/config.

The ssh CLI tool uses return code 255 as a ‘connection error’, this can conflict with commands/tools that also return 255 as an error code and will look like an ‘unreachable’ condition or ‘connection error’ to this plugin.

**Examples:**

Example 1 (unknown):
```unknown
[ssh_connection]
control_path = VALUE
```

Example 2 (unknown):
```unknown
[ssh_connection]
control_path_dir = ~/.ansible/cp
```

Example 3 (unknown):
```unknown
[defaults]
host_key_checking = true
```

Example 4 (unknown):
```unknown
[ssh_connection]
host_key_checking = true
```

---

## ansible.builtin.pow filter – power of (math operation) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/pow_filter.html

**Contents:**
- ansible.builtin.pow filter – power of (math operation)
- Synopsis
- Input
- Positional parameters
- Notes
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name pow. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.pow for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

Math operation that returns the Nth power of inputted number, X ^ N.

This describes the input of the filter, the value before | ansible.builtin.pow.

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.pow(positional1, positional2, ...)

Which power (exponent) to use.

This is a passthrough to Python’s math.pow.

**Examples:**

Example 1 (javascript):
```javascript
# => 32768
eight_power_five: "{{ 8 | pow(5) }}"

# 4
square_of_2: "{{ 2 | pow(2) }}"

# me ^ 3
cube_me: "{{ me | pow(3) }}"
```

---

## ansible.builtin.truncate filter – Return a truncated copy of the string. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/truncate_filter.html

**Contents:**
- ansible.builtin.truncate filter – Return a truncated copy of the string.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name truncate. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.truncate for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return a truncated copy of the string.

This is the Jinja builtin filter plugin ‘truncate’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.truncate

---

## ansible.builtin.dpkg_selections module – Dpkg package selection selections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/dpkg_selections_module.html

**Contents:**
- ansible.builtin.dpkg_selections module – Dpkg package selection selections
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name dpkg_selections even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.dpkg_selections for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Change dpkg package selection state via --get-selections and --set-selections.

The selection state to set the package to.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

This module will not cause any packages to be installed/removed/purged, use the ansible.builtin.apt module for that.

Brian Brazil (@brian-brazil)

**Examples:**

Example 1 (unknown):
```unknown
- name: Prevent python from being upgraded
  ansible.builtin.dpkg_selections:
    name: python
    selection: hold

- name: Allow python to be upgraded
  ansible.builtin.dpkg_selections:
    name: python
    selection: install
```

---

## ansible.builtin.min filter – Return the smallest item from the sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/min_filter.html

**Contents:**
- ansible.builtin.min filter – Return the smallest item from the sequence.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name min. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.min for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the smallest item from the sequence.

This is the Jinja builtin filter plugin ‘min’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.min

---

## ansible.builtin.file module – Manage files and file properties — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/file_module.html

**Contents:**
- ansible.builtin.file module – Manage files and file properties
- Synopsis
- Parameters
- Attributes
- See Also
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name file even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.file for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Set attributes of files, directories, or symlinks and their targets.

Alternatively, remove files, symlinks or directories.

Many other modules support the same options as the ansible.builtin.file module - including ansible.builtin.copy, ansible.builtin.template, and ansible.builtin.assemble.

For Windows targets, use the ansible.windows.win_file module instead.

This parameter indicates the time the file’s access time should be set to.

Should be preserve when no modification is required, YYYYMMDDHHMM.SS when using default time format, or now.

Default is None meaning that preserve is the default for state=[file,directory,link,hard] and now is default for state=touch.

When used with access_time, indicates the time format that must be used.

Based on default Python format (see time.strftime doc).

Default: "%Y%m%d%H%M.%S"

The attributes the resulting filesystem object should have.

To get supported flags look at the man page for chattr on the target system.

This string should contain the attributes in the same order as the one displayed by lsattr.

The = operator is assumed as default, otherwise + or - operators need to be included in the string.

This flag indicates that filesystem links, if they exist, should be followed.

follow=yes and state=link can modify src when combined with parameters such as mode.

Previous to Ansible 2.5, this was false by default.

While creating a symlink with a non-existent destination, set follow=false to avoid a warning message related to permission issues. The warning message is added to notify the user that we can not set permissions to the non-existent destination.

Force the creation of the links in two cases: if the link type is symbolic and the source file does not exist (but will appear later); the destination exists and is a file (so, we need to unlink the path file and create a link to the src file in place of it).

Name of the group that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current group of the current user unless you are root, in which case it can preserve the previous ownership.

The permissions the resulting filesystem object should have.

For those used to /usr/bin/chmod remember that modes are actually octal numbers. You must give Ansible enough information to parse them correctly. For consistent results, quote octal numbers (for example, '644' or '1777') so Ansible receives a string and can do its own conversion from string into number. Adding a leading zero (for example, 0755) works sometimes, but can fail in loops and some other circumstances.

Giving Ansible a number without following either of these rules will end up with a decimal number which will have unexpected results.

As of Ansible 1.8, the mode may be specified as a symbolic mode (for example, u+rwx or u=rw,g=r,o=r).

If mode is not specified and the destination filesystem object does not exist, the default umask on the system will be used when setting the mode for the newly created filesystem object.

If mode is not specified and the destination filesystem object does exist, the mode of the existing filesystem object will be used.

Specifying mode is the best way to ensure filesystem objects are created with the correct permissions. See CVE-2020-1736 for further details.

This parameter indicates the time the file’s modification time should be set to.

Should be preserve when no modification is required, YYYYMMDDHHMM.SS when using default time format, or now.

Default is None meaning that preserve is the default for state=[file,directory,link,hard] and now is default for state=touch.

modification_time_format

When used with modification_time, indicates the time format that must be used.

Based on default Python format (see time.strftime doc).

Default: "%Y%m%d%H%M.%S"

Name of the user that should own the filesystem object, as would be fed to chown.

When left unspecified, it uses the current user unless you are root, in which case it can preserve the previous ownership.

Specifying a numeric username will be assumed to be a user ID and not a username. Avoid numeric usernames to avoid this confusion.

Path to the file being managed.

Recursively set the specified file attributes on directory contents.

This applies only when state is set to directory.

The level part of the SELinux filesystem object context.

This is the MLS/MCS attribute, sometimes known as the range.

When set to _default, it will use the level portion of the policy if available.

The role part of the SELinux filesystem object context.

When set to _default, it will use the role portion of the policy if available.

The type part of the SELinux filesystem object context.

When set to _default, it will use the type portion of the policy if available.

The user part of the SELinux filesystem object context.

By default it uses the system policy, where applicable.

When set to _default, it will use the user portion of the policy if available.

Path of the file to link to.

This applies only to state=link and state=hard.

For state=link, this will also accept a non-existing path.

Relative paths are relative to the file being created (path) which is how the Unix command ln -s SRC DEST treats relative paths.

If absent, directories will be recursively deleted, and files or symlinks will be unlinked. In the case of a directory, if diff is declared, you will see the files and folders deleted listed under path_contents. Note that absent will not cause ansible.builtin.file to fail if the path does not exist as the state did not change.

If directory, all intermediate subdirectories will be created if they do not exist. Since Ansible 1.7 they will be created with the supplied permissions.

If file, with no other options, returns the current state of path.

If file, even with other options (such as mode), the file will be modified if it exists but will NOT be created if it does not exist. Set to touch or use the ansible.builtin.copy or ansible.builtin.template module if you want to create the file if it does not exist.

If hard, the hard link will be created or changed.

If link, the symbolic link will be created or changed.

If touch (new in 1.4), an empty file will be created if the file does not exist, while an existing file or directory will receive updated file access and modification times (similar to the way touch works from the command line).

Default is the current state of the file if it exists, directory if recurse=yes, or file otherwise.

Influence when to use atomic operation to prevent data corruption or inconsistent reads from the target filesystem object.

By default this module uses atomic operations to prevent data corruption or inconsistent reads from the target filesystem objects, but sometimes systems are configured or just broken in ways that prevent this. One example is docker mounted filesystem objects, which cannot be updated atomically from inside the container and can only be written in an unsafe manner.

This option allows Ansible to fall back to unsafe methods of updating filesystem objects when atomic operations fail (however, it doesn’t force Ansible to perform unsafe writes).

IMPORTANT! Unsafe writes are subject to race conditions and can lead to data corruption.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

permissions and ownership will be shown but file contents on absent/touch will not.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Assemble configuration files from fragments.

Copy files to remote locations.

Retrieve file or file system status.

Template a file out to a target host.

The official documentation on the ansible.windows.win_file module.

Common return values are documented here, the following are the fields unique to this module:

Destination file/path, equal to the value passed to path.

Returned: state=touch, state=hard, state=link

Sample: "/path/to/file.txt"

Destination file/path, equal to the value passed to path.

Returned: state=absent, state=directory, state=file

Sample: "/path/to/file.txt"

**Examples:**

Example 1 (unknown):
```unknown
- name: Change file ownership, group and permissions
  ansible.builtin.file:
    path: /etc/foo.conf
    owner: foo
    group: foo
    mode: '0644'

- name: Give insecure permissions to an existing file
  ansible.builtin.file:
    path: /work
    owner: root
    group: root
    mode: '1777'

- name: Create a symbolic link
  ansible.builtin.file:
    src: /file/to/link/to
    dest: /path/to/symlink
    owner: foo
    group: foo
    state: link

- name: Create two hard links
  ansible.builtin.file:
    src: '/tmp/{{ item.src }}'
    dest: '{{ item.dest }}'
    state: hard
  loop:
    - { src: x, dest: y }
    - { src: z, dest: k }

- name: Touch a file, using symbolic modes to set the permissions (equivalent to 0644)
  ansible.builtin.file:
    path: /etc/foo.conf
    state: touch
    mode: u=rw,g=r,o=r

- name: Touch the same file, but add/remove some permissions
  ansible.builtin.file:
    path: /etc/foo.conf
    state: touch
    mode: u+rw,g-wx,o-rwx

- name: Touch again the same file, but do not change times this makes the task idempotent
  ansible.builtin.file:
    path: /etc/foo.conf
    state: touch
    mode: u+rw,g-wx,o-rwx
    modification_time: preserve
    access_time: preserve

- name: Create a directory if it does not exist
  ansible.builtin.file:
    path: /etc/some_directory
    state: directory
    mode: '0755'

- name: Update modification and access time of given file
  ansible.builtin.file:
    path: /etc/some_file
    state: file
    modification_time: now
    access_time: now

- name: Set access time based on seconds from epoch value
  ansible.builtin.file:
    path: /etc/another_file
    state: file
    access_time: '{{ "%Y%m%d%H%M.%S" | strftime(stat_var.stat.atime) }}'

- name: Recursively change ownership of a directory
  ansible.builtin.file:
    path: /etc/foo
    state: directory
    recurse: yes
    owner: foo
    group: foo

- name: Remove file (delete file)
  ansible.builtin.file:
    path: /etc/foo.txt
    state: absent

- name: Recursively remove directory
  ansible.builtin.file:
    path: /etc/foo
    state: absent
```

---

## ansible.builtin.nan test – is this not a number (NaN) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/nan_test.html

**Contents:**
- ansible.builtin.nan test – is this not a number (NaN)
- Synopsis
- Input
- Examples
- Return Value
  - Authors
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name nan. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.nan for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

Whether the input is a special floating point number called not a number.

Aliases: is_file, isnan

This describes the input of the test, the value before is ansible.builtin.nan or is not ansible.builtin.nan.

Possible number representation or string that can be converted into one.

Returns True if the input is NaN, False if otherwise.

**Examples:**

Example 1 (unknown):
```unknown
isnan: "{{ '42' is nan }}"
```

---

## ansible.builtin.url lookup – return contents from URL — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/url_lookup.html

**Contents:**
- ansible.builtin.url lookup – return contents from URL
- Synopsis
- Terms
- Keyword parameters
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name url. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.url for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

Returns the content of the URL requested to be used as data in play.

This describes keyword parameters of the lookup. These are the values key1=value1, key2=value2 and so on in the following examples: lookup('ansible.builtin.url', key1=value1, key2=value2, ...) and query('ansible.builtin.url', key1=value1, key2=value2, ...)

added in ansible-base 2.10

String of file system path to CA cert bundle to use

Environment variable: ANSIBLE_LOOKUP_URL_CA_PATH

Variable: ansible_lookup_url_ca_path

list / elements=string

added in ansible-core 2.14

SSL/TLS Ciphers to use for the request

When a list is provided, all ciphers are joined in order with :

See the OpenSSL Cipher List Format for more details.

The available ciphers is dependent on the Python and OpenSSL/LibreSSL versions

Environment variable: ANSIBLE_LOOKUP_URL_CIPHERS

Variable: ansible_lookup_url_ciphers

added in ansible-base 2.10

Whether or not the URI module should follow redirects.

"all": Will follow all redirects.

"no": (DEPRECATED, removed in 2.22) alias of none.

"none": Will not follow any redirects.

"safe": Only redirects doing GET or HEAD requests will be followed.

"urllib2" (default): Defer to urllib2 behavior (As of writing this follows HTTP redirects).

"yes": (DEPRECATED, removed in 2.22) alias of all.

Environment variable: ANSIBLE_LOOKUP_URL_FOLLOW_REDIRECTS

Variable: ansible_lookup_url_follow_redirects

added in ansible-base 2.10

Whether or not to set “cache-control” header with value “no-cache”

Environment variable: ANSIBLE_LOOKUP_URL_FORCE

Variable: ansible_lookup_url_force

added in ansible-base 2.10

Force basic authentication

Environment variable: ANSIBLE_LOOKUP_URL_FORCE_BASIC_AUTH

Variable: ansible_lookup_url_force_basic_auth

added in ansible-base 2.10

User-Agent to use in the request. The default was changed in 2.11 to ansible-httpget.

Default: "ansible-httpget"

Environment variable: ANSIBLE_LOOKUP_URL_AGENT

Variable: ansible_lookup_url_agent

Password to use for HTTP authentication.

Flag to control if content is returned as a list of lines or as a single text blob

added in ansible-base 2.10

How long to wait for the server to send data before giving up

Environment variable: ANSIBLE_LOOKUP_URL_TIMEOUT

Variable: ansible_lookup_url_timeout

added in ansible-base 2.10

String of file system path to unix socket file to use when establishing connection to the provided url

Environment variable: ANSIBLE_LOOKUP_URL_UNIX_SOCKET

Variable: ansible_lookup_url_unix_socket

list / elements=string

added in ansible-base 2.10

A list of headers to not attach on a redirected request

Environment variable: ANSIBLE_LOOKUP_URL_UNREDIR_HEADERS

Variable: ansible_lookup_url_unredir_headers

added in ansible-base 2.10

Use GSSAPI handler of requests

As of Ansible 2.11, GSSAPI credentials can be specified with username and password.

Environment variable: ANSIBLE_LOOKUP_URL_USE_GSSAPI

Variable: ansible_lookup_url_use_gssapi

added in ansible-core 2.14

Determining whether to use credentials from ``~/.netrc`` file

By default .netrc is used with Basic authentication headers

When set to False, .netrc credentials are ignored

Environment variable: ANSIBLE_LOOKUP_URL_USE_NETRC

Variable: ansible_lookup_url_use_netrc

Flag to control if the lookup will observe HTTP proxy environment variables when present.

Username to use for HTTP authentication.

Flag to control SSL certificate validation

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters: lookup('ansible.builtin.url', term1, term2, key1=value1, key2=value2) and query('ansible.builtin.url', term1, term2, key1=value1, key2=value2)

list / elements=string

list of list of lines or content of url(s)

**Examples:**

Example 1 (unknown):
```unknown
[url_lookup]
ca_path = VALUE
```

Example 2 (unknown):
```unknown
[url_lookup]
ciphers = VALUE
```

Example 3 (unknown):
```unknown
[url_lookup]
follow_redirects = urllib2
```

Example 4 (unknown):
```unknown
[url_lookup]
force = false
```

---

## ansible.builtin.subelements filter – returns a product of a list and its elements — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/subelements_filter.html

**Contents:**
- ansible.builtin.subelements filter – returns a product of a list and its elements
- Synopsis
- Input
- Positional parameters
- Examples
- Return Value
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name subelements. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.subelements for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Positional parameters

This produces a product of an object and the subelement values of that object, similar to the subelements lookup. This lets you specify individual subelements to use in a template _input.

This describes the input of the filter, the value before | ansible.builtin.subelements.

list / elements=any / required

This describes positional parameters of the filter. These are the values positional1, positional2 and so on in the following example: input | ansible.builtin.subelements(positional1, positional2, ...)

Label of property to extract from original list items.

If True, ignore missing subelements, otherwise missing subelements generate an error.

List made of original list and product of the subelement list.

**Examples:**

Example 1 (javascript):
```javascript
# data
users:
  - groups: [1,2,3]
    name: lola
  - name: fernando
    groups: [2,3,4]

# user_w_groups =>[ { "groups": [ 1, 2, 3 ], "name": "lola" }, 1 ], [ { "groups": [ 1, 2, 3 ], "name": "lola" }, 2 ], [ { "groups": [ 1, 2, 3 ], "name": "lola" }, 3 ], [ { "groups": [ 2, 3, 4 ], "name": "fernando" }, 2 ], [ { "groups": [ 2, 3, 4 ], "name": "fernando" }, 3 ], [ { "groups": [ 2, 3, 4 ], "name": "fernando" }, 4 ] ]
users_w_groups: {{ users | subelements('groups', skip_missing=True) }}
```

---

## Listing collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_listing.html

**Contents:**
- Listing collections

To list installed collections, run ansible-galaxy collection list. This shows all of the installed collections found in the configured collections search paths. It will also show collections under development that contain a galaxy.yml file instead of a MANIFEST.json. The path where the collections are located is displayed as well as version information. If no version information is available, a * is displayed for the version number.

Run with -vvv to display more detailed information. You may see additional collections here that were added as dependencies of your installed collections. Only use collections in your playbooks that you have directly installed.

To list a specific collection, pass a valid fully qualified collection name (FQCN) to the command ansible-galaxy collection list. All instances of the collection will be listed.

To search other paths for collections, use the -p option. Specify multiple search paths by separating them with a :. The list of paths specified on the command line will be added to the beginning of the configured collections search paths.

**Examples:**

Example 1 (unknown):
```unknown
# /home/astark/.ansible/collections/ansible_collections
Collection                 Version
-------------------------- -------
cisco.aci                  0.0.5
cisco.mso                  0.0.4
sandwiches.ham             *
splunk.es                  0.0.5

# /usr/share/ansible/collections/ansible_collections
Collection        Version
----------------- -------
fortinet.fortios  1.0.6
pureport.pureport 0.0.8
sensu.sensu_go    1.3.0
```

Example 2 (unknown):
```unknown
> ansible-galaxy collection list fortinet.fortios

# /home/astark/.ansible/collections/ansible_collections
Collection       Version
---------------- -------
fortinet.fortios 1.0.1

# /usr/share/ansible/collections/ansible_collections
Collection       Version
---------------- -------
fortinet.fortios 1.0.6
```

Example 3 (unknown):
```unknown
> ansible-galaxy collection list -p '/opt/ansible/collections:/etc/ansible/collections'

# /opt/ansible/collections/ansible_collections
Collection      Version
--------------- -------
sandwiches.club 1.7.2

# /etc/ansible/collections/ansible_collections
Collection     Version
-------------- -------
sandwiches.pbj 1.2.0

# /home/astark/.ansible/collections/ansible_collections
Collection                 Version
-------------------------- -------
cisco.aci                  0.0.5
cisco.mso                  0.0.4
fortinet.fortios           1.0.1
sandwiches.ham             *
splunk.es                  0.0.5

# /usr/share/ansible/collections/ansible_collections
Collection        Version
----------------- -------
fortinet.fortios  1.0.6
pureport.pureport 0.0.8
sensu.sensu_go    1.3.0
```

---

## Creating collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_creating.html

**Contents:**
- Creating collections
- Naming your collection
- Creating a new collection
- Creating a collection from a custom template
- Creating collections with ansible-creator

To create a collection:

Create a new collection, optionally using a custom collection template, with the ansible-galaxy collection init command.

Add modules and other content to the collection.

Build the collection into a collection artifact with ansible-galaxy collection build.

Publish the collection artifact to Galaxy with ansible-galaxy collection publish.

A user can then install your collection on their systems.

Naming your collection

Creating a new collection

Creating a collection from a custom template

Creating collections with ansible-creator

Collection names consist of a namespace and a name, separated by a period (.). Both namespace and name should be valid Python identifiers. This means that they should consist of ASCII letters, digits, and underscores.

Usually namespaces and names use lower-case letters, digits, and underscores, but no upper-case letters.

You should make sure that the namespace you use is not registered by someone else by checking on Ansible Galaxy’s namespace list. If you chose a namespace or even a full collection name that collides with another collection on Galaxy, it can happen that if you or someone else runs ansible-galaxy collection install with your collection name, you end up with another collection. Even if the namespace currently does not exist, it could be created later by someone else.

If you want to request a new namespace on Ansible Galaxy, create an issue on github.com/ansible/galaxy.

There are a few special namespaces:

The ansible namespace is owned by Red Hat and reserved for official Ansible collections. Two special members are the synthetic ansible.builtin and ansible.legacy collections. These cannot be found on Ansible Galaxy, but are built-in into ansible-core.

The community namespace is owned by the Ansible community. Collections from this namespace generally live in the GitHub ansible-collection organization. If you want to create a collection in this namespace, request it on the forum.

The local namespace does not contain any collection on Ansible Galaxy, and the intention is that this will never change. You can use the local namespace for collections that are locally on your machine or locally in your Git repositories, without having to fear collisions with actually existing collections on Ansible Galaxy.

Create your collection skeleton in a path that includes ansible_collections, for example collections/ansible_collections/.

To start a new collection, run the following command in your collections directory:

Both the namespace and collection names use the same strict set of requirements. Both are limited to alphanumeric characters and underscores, must have a minimum length of two characters, and cannot start with an underscore.

It will create the structure [my_namespace]/[my_collection]/[collection skeleton].

If Git is used for version control, the corresponding repository should be initialized in the collection directory.

Once the collection exists, you can populate the directories with the content you want inside the collection. See ansible-collections GitHub Org to get a better idea of what you can place inside a collection.

Reference: the ansible-galaxy collection command

Currently the ansible-galaxy collection command implements the following sub commands:

init: Create a basic collection based on the default template included with Ansible or your own template.

build: Create a collection artifact that can be uploaded to Galaxy or your own repository.

publish: Publish a built collection artifact to Galaxy.

install: Install one or more collections.

To learn more about the ansible-galaxy command-line tool, see the ansible-galaxy man page.

The built-in collection template is a simple example of a collection that works with ansible-core, but if you want to simplify your development process you may want to create a custom collection template to pass to ansible-galaxy collection init.

A collection skeleton is a directory that looks like a collection directory but any .j2 files (excluding those in templates/ and roles/*/templates/) will be templated by ansible-galaxy collection init. The skeleton’s galaxy.yml.j2 file should use the variables namespace and collection_name which are derived from ansible-galaxy init namespace.collection_name, and will populate the metadata in the initialized collection’s galaxy.yml file. There are a few additional variables available by default (for example, version is 1.0.0), and these can be supplemented/overridden using --extra-vars.

An example galaxy.yml.j2 file that accepts an optional dictionary variable dependencies could look like this:

To initialize a collection using the new template, pass the path to the skeleton with ansible-galaxy collection init:

Before ansible-core 2.17, collection skeleton templating is limited to the few hardcoded variables including namespace, collection_name, and version.

The default collection skeleton uses an internal filter comment_ify that isn’t accessibly to --collection-skeleton. Use ansible-doc -t filter|test --list to see available plugins.

ansible-creator is designed to quickly scaffold an Ansible collection project.

The Ansible Development Tools package offers a convenient way to install ansible-creator along with a curated set of tools for developing automation content.

After installing ansible-creator you can initialize a project in one of the following ways:

Use the init subcommand.

Use ansible-creator with the Ansible extension in Visual Studio Code.

Learn how to install and use collections.

Directories and files included in the collection skeleton

Python package of tools to create and test Ansible content.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
ansible_collections#> ansible-galaxy collection init my_namespace.my_collection
```

Example 2 (unknown):
```unknown
namespace: {{ namespace }}
name: {{ collection_name }}
version: {{ (version|quote) is version('0.0.0', operator='gt', version_type='semver')|ternary(version, undef('version must be a valid semantic version greater than 0.0.0')) }}
dependencies: {{ dependencies | default({}, true) }}
```

Example 3 (unknown):
```unknown
ansible_collections#> ansible-galaxy collection init --collection-skeleton /path/to/my/namespace/skeleton --extra-vars "@my_vars_file.json" my_namespace.my_collection
```

---

## ansible.builtin.last filter – Return the last item of a sequence. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/last_filter.html

**Contents:**
- ansible.builtin.last filter – Return the last item of a sequence.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name last. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.last for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Return the last item of a sequence.

This is the Jinja builtin filter plugin ‘last’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.last

---

## ansible.builtin.lt test – Same as a < b. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/lt_test.html

**Contents:**
- ansible.builtin.lt test – Same as a < b.
- Synopsis
  - Collection links

This test plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name lt. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.lt for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same test plugin name.

This is the Jinja builtin test plugin ‘lt’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-tests.lt

---

## ansible.builtin.service module – Manage services — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/service_module.html

**Contents:**
- ansible.builtin.service module – Manage services
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name service even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.service for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Controls services on remote hosts. Supported init systems include BSD init, OpenRC, SysV, Solaris SMF, systemd, upstart.

This module acts as a proxy to the underlying service manager module. While all arguments will be passed to the underlying module, not all modules support the same arguments. This documentation only covers the minimum intersection of module arguments that all service manager modules support.

This module is a proxy for multiple more specific service manager modules (such as ansible.builtin.systemd and ansible.builtin.sysvinit). This allows management of a heterogeneous environment of machines without creating a specific task for each service manager. The module to be executed is determined by the use option, which defaults to the service manager discovered by ansible.builtin.setup. If ansible.builtin.setup was not yet run, this module may run it.

For Windows targets, use the ansible.windows.win_service module instead.

This module has a corresponding action plugin.

Additional arguments provided on the command line.

While using remote hosts with systemd this setting will be ignored.

Whether the service should start on boot.

At least one of state and enabled are required.

If the service does not respond to the status command, name a substring to look for as would be found in the output of the ps command as a stand-in for a status result.

If the string is found, the service will be assumed to be started.

While using remote hosts with systemd this setting will be ignored.

For OpenRC init scripts (e.g. Gentoo) only.

The runlevel that this service belongs to.

While using remote hosts with systemd this setting will be ignored.

If the service is being restarted then sleep this many seconds between the stop and start command.

This helps to work around badly-behaving init scripts that exit immediately after signaling a process to stop.

Not all service managers support sleep, i.e when using systemd this setting will be ignored.

started/stopped are idempotent actions that will not run commands unless necessary.

restarted will always bounce the service.

reloaded will always reload.

At least one of state and enabled are required.

Note that reloaded will start the service if it is not already started, even if your chosen init system wouldn’t normally.

The service module actually uses system specific modules, normally through auto detection, this setting can force a specific module.

Normally it uses the value of the ansible_service_mgr fact and falls back to the ansible.legacy.service module when none matching is found.

The ‘old service module’ still uses autodetection and in no way does it correspond to the service command.

Indicates this has a corresponding action plugin so some parts of the options can be executed on the controller

Supports being used with the async keyword

Forces a ‘global’ task that does not execute per host, this bypasses per host templating and serial, throttle and other loop considerations

Conditionals will work as if run_once is being used, variables used will be from the first available host

This action will not work normally outside of lockstep strategies

support depends on the underlying plugin invoked

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

support depends on the underlying plugin invoked

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

The support depends on the availability for the specific plugin for each platform and if fact gathering is able to detect it

Target OS/families that can be operated against

For AIX, group subsystem names can be used.

The service command line utility is not part of any service manager system but a convenience. It does not have a standard implementation across systems, and this action cannot use it directly. Though it might be used if found in certain circumstances, the detected system service manager is normally preferred.

The official documentation on the ansible.windows.win_service module.

**Examples:**

Example 1 (unknown):
```unknown
- name: Start service httpd, if not started
  ansible.builtin.service:
    name: httpd
    state: started

- name: Stop service httpd, if started
  ansible.builtin.service:
    name: httpd
    state: stopped

- name: Restart service httpd, in all cases
  ansible.builtin.service:
    name: httpd
    state: restarted

- name: Reload service httpd, in all cases
  ansible.builtin.service:
    name: httpd
    state: reloaded

- name: Enable service httpd, and not touch the state
  ansible.builtin.service:
    name: httpd
    enabled: yes

- name: Start service foo, based on running process /usr/bin/foo
  ansible.builtin.service:
    name: foo
    pattern: /usr/bin/foo
    state: started

- name: Restart network service for interface eth0
  ansible.builtin.service:
    name: network
    state: restarted
    args: eth0
```

---

## ansible.builtin.attr filter – Get an attribute of an object. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/attr_filter.html

**Contents:**
- ansible.builtin.attr filter – Get an attribute of an object.
- Synopsis
  - Collection links

This filter plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name attr. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.attr for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same filter plugin name.

Get an attribute of an object.

This is the Jinja builtin filter plugin ‘attr’.

See: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.attr

---

## ansible.builtin.apt module – Manages apt-packages — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/apt_module.html

**Contents:**
- ansible.builtin.apt module – Manages apt-packages
- Synopsis
- Requirements
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name apt even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.apt for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Manages apt packages (such as for Debian/Ubuntu).

The below requirements are needed on the host that executes this module.

aptitude (before 2.4)

allow_change_held_packages

added in ansible-core 2.13

Allows changing the version of a package which is on the apt hold list.

aliases: allow-downgrade, allow_downgrades, allow-downgrades

added in ansible-core 2.12

Corresponds to the --allow-downgrades option for apt.

This option enables the named package and version to replace an already installed higher version of that package.

Note that setting allow_downgrade=true can make this module behave in a non-idempotent way.

(The task could end up with a set of packages that does not match the complete list of specified packages to install).

allow_downgrade is only supported by apt and will be ignored if aptitude is detected or specified.

allow_unauthenticated

aliases: allow-unauthenticated

Ignore if packages cannot be authenticated. This is useful for bootstrapping environments that manage their own apt-key setup.

allow_unauthenticated is only supported with state: install/present.

auto_install_module_deps

added in ansible-core 2.19

Automatically install dependencies required to run this module.

If true, cleans the local repository of retrieved package files that can no longer be downloaded.

If true, remove unused dependency packages for all module states except build-dep. It can also be used as the only option.

Previous to version 2.4, autoclean was also an alias for autoremove, now it is its own separate command. See documentation for further information.

Update the apt cache if it is older than the cache_valid_time. This option is set in seconds.

As of Ansible 2.4, if explicitly set, this sets update_cache=yes.

added in ansible-core 2.13

Run the equivalent of apt-get clean to clear out the local repository of retrieved package files. It removes everything but the lock file from /var/cache/apt/archives/ and /var/cache/apt/archives/partial/.

Can be run as part of the package installation (clean runs before install) or as a separate step.

Path to a .deb package on the remote machine.

If :// in the path, ansible will attempt to download deb before installing. (Version added 2.1)

Requires the xz-utils package to extract the control file of the deb package to install.

aliases: default-release

Corresponds to the -t option for apt and sets pin priorities.

Add dpkg options to apt command. Defaults to -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold".

Options should be supplied as comma separated list.

Default: "force-confdef,force-confold"

added in ansible-core 2.11

Corresponds to the --no-remove option for apt.

If true, it is ensured that no packages will be removed or the task will fail.

fail_on_autoremove is only supported with state except absent.

fail_on_autoremove is only supported by apt and will be ignored if aptitude is detected or specified.

Corresponds to the --force-yes to apt-get and implies allow_unauthenticated=yes and allow_downgrade=yes.

This option will disable checking both the packages’ signatures and the certificates of the web servers they are downloaded from.

This option *is not* the equivalent of passing the -f flag to apt-get on the command line.

**This is a destructive operation with the potential to destroy your system, and it should almost never be used.** Please also see man apt-get for more information.

Force usage of apt-get instead of aptitude.

aliases: install-recommends

Corresponds to the --no-install-recommends option for apt. true installs recommended packages. false does not install recommended packages. By default, Ansible will use the same defaults as the operating system. Suggested packages are never installed.

added in ansible-core 2.12

How many seconds will this action wait to acquire a lock on the apt db.

Sometimes there is a transitory lock and this will retry at least until timeout is hit.

aliases: package, pkg

list / elements=string

A list of package names, like foo, or package specifier with version, like foo=1.0 or foo>=1.0. Name wildcards (fnmatch) like apt* and version wildcards like foo=1.0* are also supported.

Do not use single or double quotes around the version when referring to the package name with a specific version, such as foo=1.0 or foo>=1.0.

Only upgrade a package if it is already installed.

Force the exit code of /usr/sbin/policy-rc.d.

For example, if policy_rc_d=101 the installed package will not trigger a service start.

If /usr/sbin/policy-rc.d already exists, it is backed up and restored after the package installation.

If null, the /usr/sbin/policy-rc.d is not created/changed.

Will force purging of configuration files if state=absent or autoremove=yes.

Indicates the desired package state. latest ensures that the latest version is installed. build-dep ensures the package build dependencies are installed. fixed attempt to correct a system with broken dependencies in place.

"present" ← (default)

aliases: update-cache

Run the equivalent of apt-get update before the operation. Can be run as part of the package installation or as a separate step.

Default is not to update the cache.

added in ansible-base 2.10

Amount of retries if the cache update fails. Also see update_cache_retry_max_delay.

update_cache_retry_max_delay

added in ansible-base 2.10

Use an exponential backoff delay for each retry (see update_cache_retries) up to this max delay in seconds.

If yes or safe, performs an aptitude safe-upgrade.

If full, performs an aptitude full-upgrade.

If dist, performs an apt-get dist-upgrade.

Note: This does not upgrade a specific package, use state=latest for that.

Note: Since 2.4, apt-get is used as a fall-back if aptitude is not present.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Target OS/families that can be operated against

Three of the upgrade modes (full, safe and its alias true) required aptitude up to 2.3, since 2.4 apt-get is used as a fall-back.

In most cases, packages installed with apt will start newly installed services by default. Most distributions have mechanisms to avoid this. For example when installing Postgresql-9.5 in Debian 9, creating an executable shell script (/usr/sbin/policy-rc.d) that throws a return code of 101 will stop Postgresql 9.5 starting up after install. Remove the file or its execute permission afterward.

The apt-get commandline supports implicit regex matches here but we do not because it can let typos through easier (If you typo foo as fo apt-get would install packages that have “fo” in their name with a warning and a prompt for the user. Since there are no warnings and prompts before installing, we disallow this. Use an explicit fnmatch pattern if you want wildcarding).

When used with a loop: each package will be processed individually, it is much more efficient to pass the list directly to the name option.

When default_release is used, an implicit priority of 990 is used. This is the same behavior as apt-get -t.

When an exact version is specified, an implicit priority of 1001 is used.

If the interpreter can’t import python3-apt the module will check for it in system-owned interpreters as well. If the dependency can’t be found, depending on the value of auto_install_module_deps the module will attempt to install it. If the dependency is found or installed, the module will be respawned under the correct interpreter.

Common return values are documented here, the following are the fields unique to this module:

time of the last cache update (0 if unknown)

Returned: success, in some cases

Sample: 1425828348000

if the cache was updated or not

Returned: success, in some cases

error output from apt

Returned: success, when needed

Sample: "AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to ..."

Returned: success, when needed

Sample: "Reading package lists...\nBuilding dependency tree...\nReading state information...\nThe following extra packages will be installed:\n apache2-bin ..."

Matthew Williams (@mgwilliams)

**Examples:**

Example 1 (unknown):
```unknown
- name: Install apache httpd (state=present is optional)
  ansible.builtin.apt:
    name: apache2
    state: present

- name: Update repositories cache and install "foo" package
  ansible.builtin.apt:
    name: foo
    update_cache: yes

- name: Remove "foo" package
  ansible.builtin.apt:
    name: foo
    state: absent

- name: Install the package "foo"
  ansible.builtin.apt:
    name: foo

- name: Install a list of packages
  ansible.builtin.apt:
    pkg:
    - foo
    - foo-tools

- name: Install the version '1.00' of package "foo"
  ansible.builtin.apt:
    name: foo=1.00

- name: Update the repository cache and update package "nginx" to latest version using default release squeeze-backport
  ansible.builtin.apt:
    name: nginx
    state: latest
    default_release: squeeze-backports
    update_cache: yes

- name: Install the version '1.18.0' of package "nginx" and allow potential downgrades
  ansible.builtin.apt:
    name: nginx=1.18.0
    state: present
    allow_downgrade: yes

- name: Install zfsutils-linux with ensuring conflicted packages (e.g. zfs-fuse) will not be removed.
  ansible.builtin.apt:
    name: zfsutils-linux
    state: latest
    fail_on_autoremove: yes

- name: Install latest version of "openjdk-6-jdk" ignoring "install-recommends"
  ansible.builtin.apt:
    name: openjdk-6-jdk
    state: latest
    install_recommends: no

- name: Update all packages to their latest version
  ansible.builtin.apt:
    name: "*"
    state: latest

- name: Upgrade the OS (apt-get dist-upgrade)
  ansible.builtin.apt:
    upgrade: dist

- name: Run the equivalent of "apt-get update" as a separate step
  ansible.builtin.apt:
    update_cache: yes

- name: Only run "update_cache=yes" if the last one is more than 3600 seconds ago
  ansible.builtin.apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Pass options to dpkg on run
  ansible.builtin.apt:
    upgrade: dist
    update_cache: yes
    dpkg_options: 'force-confold,force-confdef'

- name: Install a .deb package
  ansible.builtin.apt:
    deb: /tmp/mypackage.deb

- name: Install the build dependencies for package "foo"
  ansible.builtin.apt:
    pkg: foo
    state: build-dep

- name: Install a .deb package from the internet
  ansible.builtin.apt:
    deb: https://example.com/python-ppq_0.1-1_all.deb

- name: Remove useless packages from the cache
  ansible.builtin.apt:
    autoclean: yes

- name: Remove dependencies that are no longer required
  ansible.builtin.apt:
    autoremove: yes

- name: Remove dependencies that are no longer required and purge their configuration files
  ansible.builtin.apt:
    autoremove: yes
    purge: true

- name: Run the equivalent of "apt-get clean" as a separate step
  ansible.builtin.apt:
    clean: yes
```

---
