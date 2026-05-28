# Ansible-Core - Commands

**Pages:** 6

---

## ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible.html

**Contents:**
- ansible
- Synopsis
- Description
- Common Options
- Environment
- Files
- Author
- License
- See also

Define and run a single task ‘playbook’ against a set of hosts

is an extra-simple tool/framework/API for doing ‘remote things’. this command allows you to define and run a single task ‘playbook’ against a set of hosts

privilege escalation method to use (default=sudo), use ansible-doc -t become -l to list valid choices.

run operations as this user (default=root)

Connection password file

clear the fact cache for every host in inventory

outputs a list of matching hosts; does not execute anything else

Since this tool does not use playbooks, use this as a substitute playbook directory. This sets the relative path for many features including roles/ group_vars/ etc.

use this file to authenticate the connection

specify extra arguments to pass to scp only (e.g. -l)

specify extra arguments to pass to sftp only (e.g. -f, -l)

specify common arguments to pass to sftp/scp/ssh (e.g. ProxyCommand)

specify extra arguments to pass to ssh only (e.g. -R)

set task timeout limit in seconds, must be positive integer.

the vault identity to use. This argument may be specified multiple times.

show program’s version number, config file location, configured module search path, module location, executable location and exit

run asynchronously, failing after X seconds (default=N/A)

don’t make any changes; instead, try to predict some of the changes that may occur

when changing (small) files and templates, show the differences in those files; works great with –check

ask for vault password

ask for privilege escalation password

prepend colon-separated path(s) to module library (default={{ ANSIBLE_HOME ~ “/plugins/modules:/usr/share/ansible/plugins/modules” }}). This argument may be specified multiple times.

set the poll interval if using -B (default=15)

override the connection timeout in seconds (default depends on connection)

The action’s options in space separated k=v format: -a ‘opt1=val1 opt2=val2’ or a json string: -a ‘{“opt1”: “val1”, “opt2”: “val2”}’

run operations with become (does not imply password prompting)

connection type to use (default=ssh)

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

specify number of parallel processes to use (default=5)

show this help message and exit

specify inventory host path or comma separated host list. This argument may be specified multiple times.

ask for connection password

further limit selected hosts to an additional pattern

Name of the action to execute (default=command)

log output to this directory

connect as this user (default=None)

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

The following environment variables may be specified.

ANSIBLE_INVENTORY – Override the default ansible inventory file

ANSIBLE_LIBRARY – Override the default ansible module library path

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/hosts – Default inventory file

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible-config(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible [-h] [--version] [-v] [-b] [--become-method BECOME_METHOD]
            [--become-user BECOME_USER]
            [-K | --become-password-file BECOME_PASSWORD_FILE]
            [-i INVENTORY] [--list-hosts] [-l SUBSET] [--flush-cache]
            [-P POLL_INTERVAL] [-B SECONDS] [-o] [-t TREE]
            [--private-key PRIVATE_KEY_FILE] [-u REMOTE_USER]
            [-c CONNECTION] [-T TIMEOUT]
            [--ssh-common-args SSH_COMMON_ARGS]
            [--sftp-extra-args SFTP_EXTRA_ARGS]
            [--scp-extra-args SCP_EXTRA_ARGS]
            [--ssh-extra-args SSH_EXTRA_ARGS]
            [-k | --connection-password-file CONNECTION_PASSWORD_FILE] [-C]
            [-D] [-e EXTRA_VARS] [--vault-id VAULT_IDS]
            [-J | --vault-password-file VAULT_PASSWORD_FILES] [-f FORKS]
            [-M MODULE_PATH] [--playbook-dir BASEDIR]
            [--task-timeout TASK_TIMEOUT] [-a MODULE_ARGS] [-m MODULE_NAME]
            pattern
```

---

## Ansible CLI cheatsheet — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/command_guide/cheatsheet.html

**Contents:**
- Ansible CLI cheatsheet
- ansible-playbook
- ansible-galaxy
  - Installing collections
  - Installing roles
- ansible
  - Running ad-hoc commands
- ansible-doc

This page shows one or more examples of each Ansible command line utility with some common flags added and a link to the full documentation for the command. This page offers a quick reminder of some common use cases only - it may be out of date or incomplete or both. For canonical documentation, follow the links to the CLI pages.

Installing collections

Running ad-hoc commands

-i - uses my_inventory_file in the path provided for inventory to match the pattern.

-u - connects over SSH as my_connection_user.

-k - asks for password which is then provided to SSH authentication.

-f - allocates 3 forks.

-T - sets a 30-second timeout.

-t - runs only tasks marked with the tag my_tag.

-M - loads local modules from /path/to/my/modules.

-b - executes with elevated privileges (uses become).

-K - prompts the user for the become password.

See ansible-playbook for detailed documentation.

Install a single collection:

Downloads mynamespace.mycollection from the configured Galaxy server (galaxy.ansible.com by default).

Install a list of collections:

Downloads the list of collections specified in the requirements.yml file.

List all installed collections:

Install a role named example.role:

List all installed roles:

See ansible-galaxy for detailed documentation.

Runs ansible localhost- on your local system. - name=apache2 state=present - installs the apache2 package on a Debian-based system. - -b - uses become to execute with elevated privileges. - -m - specifies a module name. - -K - prompts for the privilege escalation password.

Show plugin names and their source files:

Show available plugins:

**Examples:**

Example 1 (unknown):
```unknown
ansible-playbook -i /path/to/my_inventory_file -u my_connection_user -k -f 3 -T 30 -t my_tag -M /path/to/my_modules -b -K my_playbook.yml
```

Example 2 (unknown):
```unknown
ansible-galaxy collection install mynamespace.mycollection
```

Example 3 (unknown):
```unknown
ansible-galaxy collection install -r requirements.yml
```

Example 4 (unknown):
```unknown
ansible-galaxy collection list
```

---

## Working with command line tools — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/command_guide/command_line_tools.html

**Contents:**
- Working with command line tools

Most users are familiar with ansible and ansible-playbook, but those are not the only utilities Ansible provides. Below is a complete list of Ansible utilities. Each page contains a description of the utility and a listing of supported parameters.

You should not run most Ansible CLI tools in parallel against the same targets.

---

## ansible-console — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-console.html

**Contents:**
- ansible-console
- Synopsis
- Description
- Common Options
- ARGUMENTS
- Environment
- Files
- Author
- License
- See also

REPL console for executing Ansible tasks.

A REPL that allows for running ad-hoc tasks against a chosen inventory from a nice shell with built-in tab completion (based on dominis’ ansible-shell).

It supports several commands, and you can modify its configuration at runtime:

cd [pattern]: change host/group (you can use host patterns eg.: app*.dc*:!app01*)

list: list available hosts in the current path

list groups: list groups included in the current path

become: toggle the become flag

!: forces shell module instead of the ansible module (!yum update -y)

verbosity [num]: set the verbosity level

forks [num]: set the number of forks

become_user [user]: set the become_user

remote_user [user]: set the remote_user

become_method [method]: set the privilege escalation method

check [bool]: toggle check mode

diff [bool]: toggle diff mode

timeout [integer]: set the timeout of tasks in seconds (0 to disable)

help [command/module]: display documentation for the command or module

exit: exit ansible-console

privilege escalation method to use (default=sudo), use ansible-doc -t become -l to list valid choices.

run operations as this user (default=root)

Connection password file

clear the fact cache for every host in inventory

outputs a list of matching hosts; does not execute anything else

Since this tool does not use playbooks, use this as a substitute playbook directory. This sets the relative path for many features including roles/ group_vars/ etc.

use this file to authenticate the connection

specify extra arguments to pass to scp only (e.g. -l)

specify extra arguments to pass to sftp only (e.g. -f, -l)

specify common arguments to pass to sftp/scp/ssh (e.g. ProxyCommand)

specify extra arguments to pass to ssh only (e.g. -R)

one-step-at-a-time: confirm each task before running

set task timeout limit in seconds, must be positive integer.

the vault identity to use. This argument may be specified multiple times.

show program’s version number, config file location, configured module search path, module location, executable location and exit

don’t make any changes; instead, try to predict some of the changes that may occur

when changing (small) files and templates, show the differences in those files; works great with –check

ask for vault password

ask for privilege escalation password

prepend colon-separated path(s) to module library (default={{ ANSIBLE_HOME ~ “/plugins/modules:/usr/share/ansible/plugins/modules” }}). This argument may be specified multiple times.

override the connection timeout in seconds (default depends on connection)

run operations with become (does not imply password prompting)

connection type to use (default=ssh)

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

specify number of parallel processes to use (default=5)

show this help message and exit

specify inventory host path or comma separated host list. This argument may be specified multiple times.

ask for connection password

further limit selected hosts to an additional pattern

connect as this user (default=None)

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

A name of a group in the inventory, a shell-like glob selecting hosts in inventory or any combination of the two separated by commas.

The following environment variables may be specified.

ANSIBLE_INVENTORY – Override the default ansible inventory file

ANSIBLE_LIBRARY – Override the default ansible module library path

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/hosts – Default inventory file

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-config(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-console [-h] [--version] [-v] [-b]
                    [--become-method BECOME_METHOD]
                    [--become-user BECOME_USER]
                    [-K | --become-password-file BECOME_PASSWORD_FILE]
                    [-i INVENTORY] [--list-hosts] [-l SUBSET]
                    [--flush-cache] [--private-key PRIVATE_KEY_FILE]
                    [-u REMOTE_USER] [-c CONNECTION] [-T TIMEOUT]
                    [--ssh-common-args SSH_COMMON_ARGS]
                    [--sftp-extra-args SFTP_EXTRA_ARGS]
                    [--scp-extra-args SCP_EXTRA_ARGS]
                    [--ssh-extra-args SSH_EXTRA_ARGS]
                    [-k | --connection-password-file CONNECTION_PASSWORD_FILE]
                    [-C] [-D] [--vault-id VAULT_IDS]
                    [-J | --vault-password-file VAULT_PASSWORD_FILES]
                    [-f FORKS] [-M MODULE_PATH] [--playbook-dir BASEDIR]
                    [-e EXTRA_VARS] [--task-timeout TASK_TIMEOUT] [--step]
                    [pattern]
```

---

## ansible-config — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-config.html

**Contents:**
- ansible-config
- Synopsis
- Description
- Common Options
- Actions
  - list
  - dump
  - view
  - init
  - validate

View ansible configuration.

Config command line class

show program’s version number, config file location, configured module search path, module location, executable location and exit

show this help message and exit

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

list and output available configs

Output format for list

path to configuration file, defaults to first file found in precedence.

Filter down to a specific plugin type.

Shows the current settings, merges ansible.cfg if specified

Output format for dump

Only show configurations that have changed from the default

path to configuration file, defaults to first file found in precedence.

Filter down to a specific plugin type.

Displays the current config file

path to configuration file, defaults to first file found in precedence.

Filter down to a specific plugin type.

Create initial configuration

Prefixes all entries with a comment character to disable them

Output format for init

path to configuration file, defaults to first file found in precedence.

Filter down to a specific plugin type.

Output format for init

path to configuration file, defaults to first file found in precedence.

Filter down to a specific plugin type.

The following environment variables may be specified.

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-config [-h] [--version] [-v] {list,dump,view,init,validate} ...
```

---

## ansible-galaxy — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-galaxy.html

**Contents:**
- ansible-galaxy
- Synopsis
- Description
- Common Options
- Actions
  - collection
    - collection download
    - collection init
    - collection build
    - collection publish

Perform various Role and Collection related operations.

Command to manage Ansible roles and collections.

None of the CLI tools are designed to run concurrently with themselves. Use an external scheduler and/or locking to ensure there are no clashing operations.

show program’s version number, config file location, configured module search path, module location, executable location and exit

show this help message and exit

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

Perform the action on an Ansible Galaxy collection. Must be combined with a further action like init/install as listed below.

Download collections and their dependencies as a tarball for an offline install.

Clear the existing server response cache.

Do not use the server response cache.

Include pre-release versions. Semantic versioning pre-releases are ignored by default

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

Don’t download collection(s) listed as dependencies.

The directory to download the collections to.

A file containing a list of collections to be downloaded.

The Galaxy API server URL

Creates the skeleton framework of a role or collection that complies with the Galaxy metadata format. Requires a role or collection name. The collection name must be in the format <namespace>.<collection>.

The path to a collection skeleton that the new collection should be based upon.

The path in which the skeleton collection will be created. The default is the current working directory.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

Force overwriting an existing role or collection

The Galaxy API server URL

Build an Ansible Galaxy collection artifact that can be stored in a central repository like Ansible Galaxy. By default, this command builds from the current working directory. You can optionally pass in the collection input path (where the galaxy.yml file is).

The path in which the collection is built to. The default is the current working directory.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

Force overwriting an existing role or collection

The Galaxy API server URL

Publish a collection into Ansible Galaxy. Requires the path to the collection tarball to publish.

The time to wait for the collection import process to finish.

Don’t wait for import validation results.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The Galaxy API server URL

Install one or more roles(ansible-galaxy role install), or one or more collections(ansible-galaxy collection install). You can pass in a list (roles or collections) or use the file option listed below (these are mutually exclusive). If you pass in a list, it can be a name (which will be downloaded via the galaxy API and github), or it can be a local tar archive file.

Clear the existing server response cache.

Disable GPG signature verification when installing collections from a Galaxy server

Force overwriting an existing collection and its dependencies.

==SUPPRESS==. This argument may be specified multiple times.

A space separated list of status codes to ignore during signature verification (for example, NO_PUBKEY FAILURE). Descriptions for the choices can be seen at L(https://github.com/gpg/gnupg/blob/master/doc/DETAILS#general-status-codes).Note: specify these after positional arguments or use – to separate them. This argument may be specified multiple times.

The keyring used during signature verification

Do not use the server response cache.

Install collection artifacts (tarballs) without contacting any distribution servers. This does not apply to collections in remote Git repositories or URLs to remote tarballs.

Include pre-release versions. Semantic versioning pre-releases are ignored by default

The number of signatures that must successfully verify the collection. This should be a positive integer or -1 to signify that all signatures must be used to verify the collection. Prepend the value with + to fail if no valid signatures are found for the collection (e.g. +all).

An additional signature source to verify the authenticity of the MANIFEST.json before installing the collection from a Galaxy server. Use in conjunction with a positional collection name (mutually exclusive with –requirements-file). This argument may be specified multiple times.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Upgrade installed collection artifacts. This will also update dependencies unless –no-deps is provided

Ignore SSL certificate validation errors.

Force overwriting an existing role or collection

Ignore errors during installation and continue with the next specified collection. This will not ignore dependency conflict errors.

Don’t download collections listed as dependencies.

The path to the directory containing your collections.

A file containing a list of collections to be installed.

The Galaxy API server URL

List installed collections or roles

Format to display the list of collections in.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

One or more directories to search for collections in addition to the default COLLECTIONS_PATHS. Separate multiple paths with ‘:’. This argument may be specified multiple times.

The Galaxy API server URL

Compare checksums with the collection(s) found on the server and the installed copy. This does not verify dependencies.

==SUPPRESS==. This argument may be specified multiple times.

A space separated list of status codes to ignore during signature verification (for example, NO_PUBKEY FAILURE). Descriptions for the choices can be seen at L(https://github.com/gpg/gnupg/blob/master/doc/DETAILS#general-status-codes).Note: specify these after positional arguments or use – to separate them. This argument may be specified multiple times.

The keyring used during signature verification

Validate collection integrity locally without contacting server for canonical manifest hash.

The number of signatures that must successfully verify the collection. This should be a positive integer or all to signify that all signatures must be used to verify the collection. Prepend the value with + to fail if no valid signatures are found for the collection (e.g. +all).

An additional signature source to verify the authenticity of the MANIFEST.json before using it to verify the rest of the contents of a collection from a Galaxy server. Use in conjunction with a positional collection name (mutually exclusive with –requirements-file). This argument may be specified multiple times.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

Ignore errors during verification and continue with the next specified collection.

One or more directories to search for collections in addition to the default COLLECTIONS_PATHS. Separate multiple paths with ‘:’. This argument may be specified multiple times.

A file containing a list of collections to be verified.

The Galaxy API server URL

Perform the action on an Ansible Galaxy role. Must be combined with a further action like delete/install/init as listed below.

Creates the skeleton framework of a role or collection that complies with the Galaxy metadata format. Requires a role or collection name. The collection name must be in the format <namespace>.<collection>.

The path in which the skeleton role will be created. The default is the current working directory.

Don’t query the galaxy API when creating roles

The path to a role skeleton that the new role should be based upon.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Initialize using an alternate role type. Valid types include: ‘container’, ‘apb’ and ‘network’.

Ignore SSL certificate validation errors.

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

Force overwriting an existing role or collection

The Galaxy API server URL

removes the list of roles passed as arguments from the local system.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The path to the directory containing your roles. The default is the first writable one configured via DEFAULT_ROLES_PATH: {{ ANSIBLE_HOME ~ “/roles:/usr/share/ansible/roles:/etc/ansible/roles” }} . This argument may be specified multiple times.

The Galaxy API server URL

Delete a role from Ansible Galaxy.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The Galaxy API server URL

List installed collections or roles

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The path to the directory containing your roles. The default is the first writable one configured via DEFAULT_ROLES_PATH: {{ ANSIBLE_HOME ~ “/roles:/usr/share/ansible/roles:/etc/ansible/roles” }} . This argument may be specified multiple times.

The Galaxy API server URL

searches for roles on the Ansible Galaxy server

list of galaxy tags to filter by

list of OS platforms to filter by

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The Galaxy API server URL

used to import a role into Ansible Galaxy

The name of a branch to import. Defaults to the repository’s default branch (usually master)

Don’t wait for import results.

The name the role should have, if different than the repo name

Check the status of the most recent import request for given github_user/github_repo.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The Galaxy API server URL

Setup an integration from Github or Travis for Ansible Galaxy roles

List all of your integrations.

Remove the integration matching the provided ID value. Use –list to see ID values.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The path to the directory containing your roles. The default is the first writable one configured via DEFAULT_ROLES_PATH: {{ ANSIBLE_HOME ~ “/roles:/usr/share/ansible/roles:/etc/ansible/roles” }} . This argument may be specified multiple times.

The Galaxy API server URL

prints out detailed information about an installed role as well as info available from the galaxy API.

Don’t query the galaxy API when creating roles

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

The path to the directory containing your roles. The default is the first writable one configured via DEFAULT_ROLES_PATH: {{ ANSIBLE_HOME ~ “/roles:/usr/share/ansible/roles:/etc/ansible/roles” }} . This argument may be specified multiple times.

The Galaxy API server URL

Install one or more roles(ansible-galaxy role install), or one or more collections(ansible-galaxy collection install). You can pass in a list (roles or collections) or use the file option listed below (these are mutually exclusive). If you pass in a list, it can be a name (which will be downloaded via the galaxy API and github), or it can be a local tar archive file.

Force overwriting an existing role and its dependencies.

The time to wait for operations against the galaxy server, defaults to 60s.

The Ansible Galaxy API key which can be found at https://galaxy.ansible.com/me/preferences.

Ignore SSL certificate validation errors.

Force overwriting an existing role or collection

Use tar instead of the scm archive option when packaging the role.

Ignore errors and continue with the next specified role.

Don’t download roles listed as dependencies.

The path to the directory containing your roles. The default is the first writable one configured via DEFAULT_ROLES_PATH: {{ ANSIBLE_HOME ~ “/roles:/usr/share/ansible/roles:/etc/ansible/roles” }} . This argument may be specified multiple times.

A file containing a list of roles to be installed.

The Galaxy API server URL

The following environment variables may be specified.

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-config(1), ansible-console(1), ansible-doc(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-galaxy [-h] [--version] [-v] TYPE ...
```

---
