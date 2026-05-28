# Ansible-Core - Playbooks

**Pages:** 72

---

## ansible-pull — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-pull.html

**Contents:**
- ansible-pull
- Synopsis
- Description
- Common Options
- ARGUMENTS
- Environment
- Files
- Author
- License
- See also

pulls playbooks from a VCS repo and executes them on target host

Used to pull a remote copy of ansible on each managed node, each set to run via cron and update playbook source via a source repository. This inverts the default push architecture of ansible into a pull architecture, which has near-limitless scaling potential.

None of the CLI tools are designed to run concurrently with themselves, you should use an external scheduler and/or locking to ensure there are no clashing operations.

The setup playbook can be tuned to change the cron frequency, logging locations, and parameters to ansible-pull. This is useful both for extreme scale-out and periodic remediation. Usage of the ‘fetch’ module to retrieve logs from ansible-pull runs would be an excellent way to gather and analyze remote logs from ansible-pull.

adds the hostkey for the repo url if not already added

don’t make any changes; instead, try to predict some of the changes that may occur

modified files in the working repository will be discarded

Connection password file

when changing (small) files and templates, show the differences in those files; works great with –check

clear the fact cache for every host in inventory

Do a full clone, instead of a shallow one.

outputs a list of matching hosts; does not execute anything else

use this file to authenticate the connection

purge checkout after playbook run

specify extra arguments to pass to scp only (e.g. -l)

specify extra arguments to pass to sftp only (e.g. -f, -l)

only run plays and tasks whose tags do not match these values. This argument may be specified multiple times.

specify common arguments to pass to sftp/scp/ssh (e.g. ProxyCommand)

specify extra arguments to pass to ssh only (e.g. -R)

submodules will track the latest changes. This is equivalent to specifying the –remote flag to git submodule update

the vault identity to use. This argument may be specified multiple times.

verify GPG signature of checked out commit, if it fails abort running the playbook. This needs the corresponding VCS module to support such an operation

show program’s version number, config file location, configured module search path, module location, executable location and exit

branch/tag/commit to checkout. Defaults to behavior of repository module.

ask for vault password

ask for privilege escalation password

prepend colon-separated path(s) to module library (default={{ ANSIBLE_HOME ~ “/plugins/modules:/usr/share/ansible/plugins/modules” }}). This argument may be specified multiple times.

override the connection timeout in seconds (default depends on connection)

URL of the playbook repository

connection type to use (default=ssh)

path to the directory to which Ansible will checkout the repository.

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

run the playbook even if the repository could not be updated

show this help message and exit

specify inventory host path or comma separated host list. This argument may be specified multiple times.

ask for connection password

further limit selected hosts to an additional pattern

Repository module name, which ansible will use to check out the repo. Choices are (‘git’, ‘subversion’, ‘hg’, ‘bzr’). Default is git.

only run the playbook if the repository has been updated

sleep for random interval (between 0 and n number of seconds) before starting. This is a useful way to disperse git requests

only run plays and tasks tagged with these values. This argument may be specified multiple times.

connect as this user (default=None)

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

The name of one the YAML format files to run as an Ansible playbook. This can be a relative path within the checkout. By default, Ansible will look for a playbook based on the host’s fully-qualified domain name, on the host hostname and finally a playbook named local.yml.

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

ansible(1), ansible-config(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-pull [-h] [--version] [-v] [--private-key PRIVATE_KEY_FILE]
                 [-u REMOTE_USER] [-c CONNECTION] [-T TIMEOUT]
                 [--ssh-common-args SSH_COMMON_ARGS]
                 [--sftp-extra-args SFTP_EXTRA_ARGS]
                 [--scp-extra-args SCP_EXTRA_ARGS]
                 [--ssh-extra-args SSH_EXTRA_ARGS]
                 [-k | --connection-password-file CONNECTION_PASSWORD_FILE]
                 [--vault-id VAULT_IDS]
                 [-J | --vault-password-file VAULT_PASSWORD_FILES]
                 [-e EXTRA_VARS] [-t TAGS] [--skip-tags SKIP_TAGS]
                 [-i INVENTORY] [--list-hosts] [-l SUBSET] [--flush-cache]
                 [-M MODULE_PATH]
                 [-K | --become-password-file BECOME_PASSWORD_FILE]
                 [--purge] [-o] [-s SLEEP] [-f] [-d DEST] [-U URL] [--full]
                 [-C CHECKOUT] [--accept-host-key] [-m MODULE_NAME]
                 [--verify-commit] [--clean] [--track-subs] [--check]
                 [--diff]
                 [playbook.yml ...]
```

---

## Connection plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/connection.html

**Contents:**
- Connection plugins
- ssh plugins
- Using connection plugins
- Plugin list

Using connection plugins

Connection plugins allow Ansible to connect to the target hosts so it can execute tasks on them. Ansible ships with many connection plugins, but only one can be used per host at a time.

By default, Ansible ships with several connection plugins. The most commonly used are the paramiko SSH, native ssh (just called ssh), and local connection types. All of these can be used in playbooks and with /usr/bin/ansible to decide how you want to talk to remote machines. If necessary, you can create custom connection plugins. To change the connection plugin for your tasks, you can use the connection keyword.

The basics of these connection types are covered in the getting started section.

Because SSH is the default protocol used in system administration and the protocol most used in Ansible, SSH options are included in the command line tools. See ansible-playbook for more details.

You can set the connection plugin globally with configuration, at the command line (-c, --connection), as a keyword in your play, or by setting a variable, most often in your inventory. For example, for Windows machines, you might want to set the winrm plugin as an inventory variable.

Most connection plugins can operate with minimal configuration. By default, they use the inventory hostname and defaults to find the target host.

Plugins are self-documenting. Each plugin should document its configuration options. The following are connection variables common to most connection plugins:

The name of the host to connect to, if different from the inventory hostname.

The ssh port number, for ssh and paramiko_ssh it defaults to 22.

The default username to use for log in. Most plugins default to the ‘current user running Ansible’.

Each plugin might also have a specific version of a variable that overrides the general version. For example, ansible_ssh_host for the ssh plugin.

You can use ansible-doc -t connection -l to see the list of available plugins. Use ansible-doc -t connection <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Ansible Core Documentation — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/

**Contents:**
- Ansible Core Documentation

Ansible Core, or ansible-core is the main building block and architecture for Ansible, and includes:

CLI tools such as ansible-playbook, ansible-doc. and others for driving and interacting with automation.

The Ansible language that uses YAML to create a set of rules for developing Ansible Playbooks and includes functions such as conditionals, blocks, includes, loops, and other Ansible imperatives.

An architectural framework that allows extensions through Ansible collections.

This documentation covers the version of ansible-core noted in the upper left corner of this page. We maintain multiple versions of ansible-core and of the documentation, so please be sure you are using the version of the documentation that covers the version of Ansible you’re using. For recent features, we note the version of Ansible where the feature was added.

ansible-core releases a new major release approximately twice a year. The core application evolves somewhat conservatively, valuing simplicity in language design and setup. Contributors develop and change modules and plugins, hosted in collections, much more quickly.

Ansible getting started

Installation, Upgrade & Configuration

Contributing to Ansible Core

Reference & Appendices

---

## Ansible-core 2.12 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.12.html

**Contents:**
- Ansible-core 2.12 Porting Guide
- Playbook
- Python Interpreter Discovery
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins

This section discusses the behavioral changes between ansible-core 2.11 and ansible-core 2.12.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.12 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.12 Porting Guide

Python Interpreter Discovery

Noteworthy module changes

Porting custom scripts

When calling tasks and setting async, setting ANSIBLE_ASYNC_DIR under environment: is no longer valid. Instead, use the shell configuration variable async_dir, for example by setting ansible_async_dir:

The undef() function is added to the templating environment for creating undefined variables directly in a template. Optionally, a hint may be provided for variables which are intended to be overridden.

The default value of INTERPRETER_PYTHON changed to auto. The list of Python interpreters in INTERPRETER_PYTHON_FALLBACK changed to prefer Python 3 over Python 2. The combination of these two changes means the new default behavior is to quietly prefer Python 3 over Python 2 on remote hosts. Previously a deprecation warning was issued in situations where interpreter discovery would have used Python 3 but the interpreter was set to /usr/bin/python.

INTERPRETER_PYTHON_FALLBACK can be changed from the default list of interpreters by setting the ansible_interpreter_python_fallback variable.

See interpreter discovery documentation for more details.

Python 3.8 on the controller node is a hard requirement for this release. The command line scripts will not function with a lower Python version.

ansible-vault no longer supports PyCrypto and requires cryptography.

Python 2.6 on the target node is deprecated in this release. ansible-core 2.13 will remove support for Python 2.6.

Bare variables in conditionals: when conditionals no longer automatically parse string booleans such as "true" and "false" into actual booleans. Any variable containing a non-empty string is considered true. This was previously configurable with the CONDITIONAL_BARE_VARS configuration option (and the ANSIBLE_CONDITIONAL_BARE_VARS environment variable). This setting no longer has any effect. Users can work around the issue by using the |bool filter:

The _remote_checksum() method in ActionBase is deprecated. Any action plugin using this method should use _execute_remote_stat() instead.

cron now requires name to be specified in all cases.

cron no longer allows a reboot parameter. Use special_time: reboot instead.

hostname - On FreeBSD, the before result will no longer be "temporarystub" if permanent hostname file does not exist. It will instead be "" (empty string) for consistency with other systems.

hostname - On OpenRC and Solaris based systems, the before result will no longer be "UNKNOWN" if the permanent hostname file does not exist. It will instead be "" (empty string) for consistency with other systems.

pip now uses the pip Python module installed for the Ansible module’s Python interpreter, if available, unless executable or virtualenv were specified.

The following modules no longer exist:

unique filter with Jinja2 < 2.10 is case-sensitive and now raise coherently an error if case_sensitive=False instead of when case_sensitive=True.

Set theory filters (intersect, difference, symmetric_difference and union) are now case-sensitive. Explicitly use case_sensitive=False to keep previous behavior. Note: with Jinja2 < 2.10, the filters were already case-sensitive by default.

password_hash now uses passlib defaults when an option is unspecified, for example bcrypt_sha256 now default to the “2b” format and if the “2a” format is required it must be specified.

**Examples:**

Example 1 (unknown):
```unknown
tasks:
  - dnf:
      name: '*'
      state: latest
    async: 300
    poll: 5
    vars:
      ansible_async_dir: /path/to/my/custom/dir
```

Example 2 (python):
```python
vars:
  old: "{{ undef }}"
  new: "{{ undef() }}"
  new_with_hint: "{{ undef(hint='You must override this variable') }}"
```

Example 3 (unknown):
```unknown
vars:
  teardown: 'false'

tasks:
  - include_tasks: teardown.yml
    when: teardown | bool

  - include_tasks: provision.yml
    when: not teardown | bool
```

---

## Modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/module.html

**Contents:**
- Modules
- Enabling modules
- Using modules

Modules are the main building blocks of Ansible playbooks. Although we do not generally speak of “module plugins”, a module is a type of plugin. For a developer-focused description of the differences between modules and other plugins, see Modules and plugins: what is the difference?.

You can enable a custom module by dropping it into one of these locations:

any directory added to the ANSIBLE_LIBRARY environment variable ($ANSIBLE_LIBRARY takes a colon-separated list like $PATH)

~/.ansible/plugins/modules/

/usr/share/ansible/plugins/modules/

For more information on using local custom modules, see Adding a module or plugin outside of a collection.

For information on using modules in ad hoc tasks, see Introduction to ad hoc commands. For information on using modules in playbooks, see Ansible playbooks.

An introduction to playbooks

An introduction to creating Ansible modules

A guide to creating Ansible collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Testing Strategies — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/test_strategies.html

**Contents:**
- Testing Strategies
- Integrating Testing With Ansible Playbooks
- The Right Level of Testing
- Check Mode As A Drift Test
- Modules That Are Useful for Testing
- Testing Lifecycle
- Integrating Testing With Rolling Updates
- Achieving Continuous Deployment
- Conclusion

Many times, people ask, “how can I best integrate testing with Ansible playbooks?” There are many options. Ansible is actually designed to be a “fail-fast” and ordered system, therefore it makes it easy to embed testing directly in Ansible playbooks. In this chapter, we’ll go into some patterns for integrating tests of infrastructure and discuss the right level of testing that may be appropriate.

This is a chapter about testing the application you are deploying, not the chapter on how to test Ansible modules during development. For that content, please hop over to the Development section.

By incorporating a degree of testing into your deployment workflow, there will be fewer surprises when code hits production and, in many cases, tests can be used in production to prevent failed updates from migrating across an entire installation. Since it is push-based, it is also very easy to run the steps on the localhost or testing servers. Ansible lets you insert as many checks and balances into your upgrade workflow as you would like to have.

Ansible resources are models of desired-state. As such, it should not be necessary to test that services are started, packages are installed, or other such things. Ansible is the system that will ensure these things are declaratively true. Instead, assert these things in your playbooks.

If you think the service may not be started, the best thing to do is request it to be started. If the service fails to start, Ansible will yell appropriately. (This should not be confused with whether the service is doing something functional, which we’ll show more about how to do later).

In the above setup, --check mode in Ansible can be used as a layer of testing as well. If running a deployment playbook against an existing system, using the --check flag to the ansible command will report if Ansible thinks it would have had to have made any changes to bring the system into a desired state.

This can let you know up front if there is any need to deploy onto the given system. Ordinarily, scripts and commands don’t run in check mode, so if you want certain steps to execute in normal mode even when the --check flag is used, such as calls to the script module, disable check mode for those tasks:

Certain playbook modules are particularly good for testing. Below is an example that ensures a port is open:

Here’s an example of using the URI module to make sure a web service returns:

It is easy to push an arbitrary script (in any language) on a remote host and the script will automatically fail if it has a non-zero return code:

If using roles (you should be, roles are great!), scripts pushed by the script module can live in the ‘files/’ directory of a role.

And the assert module makes it very easy to validate various kinds of truth:

Should you feel the need to test for the existence of files that are not declaratively set by your Ansible configuration, the ‘stat’ module is a great choice:

As mentioned above, there’s no need to check things like the return codes of commands. Ansible is checking them automatically. Rather than checking for a user to exist, consider using the user module to make it exist.

Ansible is a fail-fast system, so when there is an error creating that user, it will stop the playbook run. You do not have to check up behind it.

If writing some degree of basic validation of your application into your playbooks, they will run every time you deploy.

As such, deploying into a local development VM and a staging environment will both validate that things are according to plan ahead of your production deploy.

Your workflow may be something like this:

Something like an integration test battery should be written by your QA team if you are a production webservice. This would include things like Selenium tests or automated API tests and would usually not be something embedded into your Ansible playbooks.

However, it does make sense to include some basic health checks into your playbooks, and in some cases it may be possible to run a subset of the QA battery against remote nodes. This is what the next section covers.

If you have read into Controlling where tasks run: delegation and local actions it may quickly become apparent that the rolling update pattern can be extended, and you can use the success or failure of the playbook run to decide whether to add a machine into a load balancer or not.

This is the great culmination of embedded tests:

Of course in the above, the “take out of the pool” and “add back” steps would be replaced with a call to an Ansible load balancer module or appropriate shell command. You might also have steps that use a monitoring module to start and end an outage window for the machine.

However, what you can see from the above is that tests are used as a gate – if the “apply_testing_checks” step is not performed, the machine will not go back into the pool.

Read the delegation chapter about “max_fail_percentage” and you can also control how many failing tests will stop a rolling update from proceeding.

This above approach can also be modified to run a step from a testing machine remotely against a machine:

In the above example, a script is run from the testing server against a remote node prior to bringing it back into the pool.

In the event of a problem, fix the few servers that fail using Ansible’s automatically generated retry file to repeat the deploy on just those servers.

If desired, the above techniques may be extended to enable continuous deployment practices.

The workflow may look like this:

Some Ansible users use the above approach to deploy a half-dozen or dozen times an hour without taking all of their infrastructure offline. A culture of automated QA is vital if you wish to get to this level.

If you are still doing a large amount of manual QA, you should still make the decision on whether to deploy manually as well, but it can still help to work in the rolling update patterns of the previous section and incorporate some basic health checks using modules like ‘script’, ‘stat’, ‘uri’, and ‘assert’.

Ansible believes you should not need another framework to validate basic things of your infrastructure is true. This is the case because Ansible is an order-based system that will fail immediately on unhandled errors for a host, and prevent further configuration of that host. This forces errors to the top and shows them in a summary at the end of the Ansible run.

However, as Ansible is designed as a multi-tier orchestration system, it makes it very easy to incorporate tests into the end of a playbook run, either using loose tasks or roles. When used with rolling updates, testing steps can decide whether to put a machine back into a load balanced pool or not.

Finally, because Ansible errors propagate all the way up to the return code of the Ansible program itself, and Ansible by default runs in an easy push-based mode, Ansible is a great step to put into a build environment if you wish to use it to roll out systems as part of a Continuous Integration/Continuous Delivery pipeline, as is covered in sections above.

The focus should not be on infrastructure testing, but on application testing, so we strongly encourage getting together with your QA team and ask what sort of tests would make sense to run every time you deploy development VMs, and which sort of tests they would like to run against the staging environment on every deploy. Obviously at the development stage, unit tests are great too. But don’t unit test your playbook. Ansible describes states of resources declaratively, so you don’t have to. If there are cases where you want to be sure of something though, that’s great, and things like stat/assert are great go-to modules for that purpose.

In all, testing is a very organizational and site-specific thing. Everybody should be doing it, but what makes the most sense for your environment will vary with what you are deploying and who is using it – but everyone benefits from a more robust and reliable deployment system.

Browse existing collections, modules, and plugins

An introduction to playbooks

Delegation, useful for working with load balancers, clouds, and locally executed steps.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
tasks:
  - ansible.builtin.service:
      name: foo
      state: started
      enabled: true
```

Example 2 (unknown):
```unknown
roles:
  - webserver

tasks:
  - ansible.builtin.script: verify.sh
    check_mode: false
```

Example 3 (unknown):
```unknown
tasks:

  - ansible.builtin.wait_for:
      host: "{{ inventory_hostname }}"
      port: 22
    delegate_to: localhost
```

Example 4 (unknown):
```unknown
tasks:

  - action: uri url=https://www.example.com return_content=yes
    register: webpage

  - fail:
      msg: 'service is not happy'
    when: "'AWESOME' not in webpage.content"
```

---

## Frequently Asked Questions — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/faq.html

**Contents:**
- Frequently Asked Questions
- Where did all the modules go?
- Where did this specific module go?
- How can I speed up Ansible on systems with slow disks?
- How can I set the PATH or any other environment variable for a task or entire play?
- How do I handle different machines needing different user accounts or ports to log in with?
- How do I get ansible to reuse connections, enable Kerberized SSH, or have Ansible pay attention to my local SSH config file?
- How do I configure a jump host to access servers that I have no direct access to?
- How do I get Ansible to notice a dead target in a timely manner?
- How do I speed up run of ansible for servers from cloud providers (EC2, openstack,.. )?

Here are some commonly asked questions and their answers.

In July, 2019, we announced that collections would be the future of Ansible content delivery. A collection is a distribution format for Ansible content that can include playbooks, roles, modules, and plugins. In Ansible 2.9 we added support for collections. In Ansible 2.10 we extracted most modules from the main ansible/ansible repository and placed them in collections. Collections may be maintained by the Ansible team, by the Ansible community, or by Ansible partners. The ansible/ansible repository now contains the code for basic features and functions, such as copying module code to managed nodes. This code is also known as ansible-core (it was briefly called ansible-base for version 2.10).

To learn more about using collections, see Using Ansible collections.

To learn more about developing collections, see Developing collections.

To learn more about contributing to existing collections, see the individual collection repository for guidelines, or see Contributing to Ansible-maintained Collections to contribute to one of the Ansible-maintained collections.

IF you are searching for a specific module, you can check the runtime.yml file, which lists the first destination for each module that we extracted from the main ansible/ansible repository. Some modules have moved again since then. You can also search on Ansible Galaxy or ask on one of our chat channels.

Ansible may feel sluggish on systems with slow disks, such as Raspberry PI. See Ansible might be running slow if libyaml is not available for hints on how to improve this.

Setting environment variables can be done with the environment keyword. It can be used at the task or other levels in the play.

starting in 2.0.1 the setup task from gather_facts also inherits the environment directive from the play, you might need to use the |default filter to avoid errors if setting this at play level.

Setting inventory variables in the inventory file is the easiest way.

For example, suppose these hosts have different usernames and ports:

You can also dictate the connection type to be used, if you want:

You may also wish to keep these in group variables instead, or file them in a group_vars/<groupname> file. See the rest of the documentation for more information about how to organize variables.

Switch your default connection type in the configuration file to ssh, or use -c ssh to use Native OpenSSH for connections instead of the python paramiko library. In Ansible 1.2.1 and later, ssh will be used by default if OpenSSH is new enough to support ControlPersist as an option.

Paramiko is great for starting out, but the OpenSSH type offers many advanced options. You will want to run Ansible from a machine new enough to support ControlPersist, if you are using this connection type. You can still manage older clients. If you are using RHEL 6, CentOS 6, SLES 10 or SLES 11 the version of OpenSSH is still a bit old, so consider managing from a Fedora or openSUSE client even though you are managing older nodes, or just use paramiko.

We keep paramiko as the default as if you are first installing Ansible on these enterprise operating systems, it offers a better experience for new users.

You can set a ProxyCommand in the ansible_ssh_common_args inventory variable. Any arguments specified in this variable are added to the sftp/scp/ssh command line when connecting to the relevant host(s). Consider the following inventory group:

You can create group_vars/gatewayed.yml with the following contents:

Ansible will append these arguments to the command line when trying to connect to any hosts in the group gatewayed. (These arguments are used in addition to any ssh_args from ansible.cfg, so you do not need to repeat global ControlPersist settings in ansible_ssh_common_args.)

Note that ssh -W is available only with OpenSSH 5.4 or later. With older versions, it is necessary to execute nc %h:%p or some equivalent command on the bastion host.

With earlier versions of Ansible, it was necessary to configure a suitable ProxyCommand for one or more hosts in ~/.ssh/config, or globally by setting ssh_args in ansible.cfg.

You can add -o ServerAliveInterval=NumberOfSeconds with the ssh_args parameter in SSH connection plugin. Without this option, SSH and therefore Ansible will wait until the TCP connection times out. Another solution is to add ServerAliveInterval into your global SSH configuration. A good value for ServerAliveInterval is up to you to decide; keep in mind that ServerAliveCountMax=3 is the SSH default so any value you set will be tripled before terminating the SSH session.

Don’t try to manage a fleet of machines of a cloud provider from your laptop. Rather connect to a management node inside this cloud provider first and run Ansible from there.

While you can write Ansible modules in any language, most Ansible modules are written in Python, including the ones central to letting Ansible work.

By default, Ansible assumes it can find a /usr/bin/python on your remote system that is either Python2, version 2.6 or higher or Python3, 3.5 or higher.

Setting the inventory variable ansible_python_interpreter on any host will tell Ansible to auto-replace the Python interpreter with that value instead. Thus, you can point to any Python you want on the system if /usr/bin/python on your system does not point to a compatible Python interpreter.

Some platforms may only have Python 3 installed by default. If it is not installed as /usr/bin/python, you will need to configure the path to the interpreter through ansible_python_interpreter. Although most core modules will work with Python 3, there may be some special purpose ones which do not or you may encounter a bug in an edge case. As a temporary workaround you can install Python 2 on the managed host and configure Ansible to use that Python through ansible_python_interpreter. If there’s no mention in the module’s documentation that the module requires Python 2, you can also report a bug on our bug tracker so that the incompatibility can be fixed in a future release.

Do not replace the shebang lines of your python modules. Ansible will do this for you automatically at deploy time.

Also, this works for ANY interpreter, for example ruby: ansible_ruby_interpreter, perl: ansible_perl_interpreter, and so on, so you can use this for custom modules written in any scripting language and control the interpreter location.

Keep in mind that if you put env in your module shebang line (#!/usr/bin/env <other>), this won’t work and will be evaluated as one string (including the space between env and <other> space). Arguments are neither intended nor supported.

While installing Ansible, sometimes you may encounter errors such as No package ‘libffi’ found or fatal error: Python.h: No such file or directory These errors are generally caused by the missing packages, which are dependencies of the packages required by Ansible. For example, libffi package is dependency of pynacl and paramiko (Ansible -> paramiko -> pynacl -> libffi).

In order to solve these kinds of dependency issues, you might need to install required packages using the OS native package managers, such as yum, dnf, or apt, or as mentioned in the package installation guide.

Refer to the documentation of the respective package for such dependencies and their installation methods.

You can install Ansible into a virtualenv on the control node quite simply:

If you want to run under Python 3 instead of Python 2 you may want to change that slightly:

If you need to use any libraries which are not available through pip (for example, SELinux Python bindings on systems such as Red Hat Enterprise Linux or Fedora that have SELinux enabled), then you need to install them into the virtualenv. There are two methods:

When you create the virtualenv, specify --system-site-packages to make use of any libraries installed in the system’s Python:

Copy those files in manually from the system. For example, for SELinux bindings you might do:

When executing Ansible on a system with macOS as a control node machine one might encounter the following error:

+[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug. ERROR! A worker was found in a dead state

In general the recommended workaround is to set the following environment variable in your shell:

When managing a system with macOS Monterey 12, macOS Ventura 13 or above over SSH, the following error can occur:

“eDSPermissionError” DS Error: -14120 (eDSPermissionError)

This is a good indication that Allow full disk access for remote users has not been enabled.

For more details, check out the official Apple user guide article.

Managing BSD hosts with Ansible

By default, Solaris 10 and earlier run a non-POSIX shell which does not correctly expand the default tmp directory Ansible uses ( ~/.ansible/tmp). If you see module failures on Solaris machines, this is likely the problem. There are several workarounds:

You can set remote_tmp to a path that will expand correctly with the shell you are using (see the plugin documentation for C shell, fish shell, and Powershell). For example, in the ansible config file you can set:

In Ansible 2.5 and later, you can also set it per-host in inventory like this:

You can set ansible_shell_executable to the path to a POSIX compatible shell. For instance, many Solaris hosts have a POSIX shell located at /usr/xpg4/bin/sh so you can set this in inventory like so:

(bash, ksh, and zsh should also be POSIX compatible if you have any of those installed).

Generally speaking, z/OS cannot be used as an Ansible control node. For more details, see Using z/OS as a control node.

When the path to the Python interpreter is not found in the default location on the target host, the following error may result:

/usr/bin/python: FSUM7351 not found

Ansible requires a Python interpreter to execute modules on the remote host, and checks for it at the ‘default’ path /usr/bin/python.

On z/OS, the Python 3 interpreter (from IBM Open Enterprise SDK for Python) is often installed to a different path, typically something like: /usr/lpp/cyp/v3r12/pyz.

The path to the python interpreter can be configured with the Ansible inventory variable ansible_python_interpreter. For example:

For more details, see: How do I handle not having a Python interpreter at /usr/bin/python on a remote machine?.

When ANSIBLE_PIPELINING is not enabled or when Ansible pipelining is enabled but the PYTHONSTDINENCODING property is not correctly set, the following error may result.

SyntaxError: Non-UTF-8 code starting with ‘\x81’ in file <stdin> on line 1, but no encoding declared; see https://peps.python.org/pep-0263/ for details

Note, the hex '\x81' below may vary depending source causing the error:

When Ansible pipelining is enabled, Ansible passes all module code to the remote target through Python’s stdin pipe and runs it all in a single call. For more details on pipelining, see: Pipelining.

Include the following in the environment for any tasks performed on z/OS managed nodes.

Certain language environment (LE) configurations enable automatic conversion and automatic file tagging functionality required by Python on z/OS systems (IBM Open Enterprise SDK for Python ).

Include the following configurations when setting the remote environment for any z/OS managed nodes:

Ansible can be configured with remote environment variables in these options:

inventory - inventory.yml, group_vars/all.yml, or host_vars/all.yml

playbook - environment variable at top of playbook.

block or task - environment key word.

For more details, see Setting the remote environment.

Managing z/OS UNIX hosts with Ansible

Some issues arise as fakeroot does not create a full nor POSIX compliant system by default. It is known that it will not correctly expand the default tmp directory Ansible uses (~/.ansible/tmp). If you see module failures, this is likely the problem. The simple workaround is to set remote_tmp to a path that will expand correctly (see documentation of the shell plugin you are using for specifics).

For example, in the ansible config file (or through environment variable) you can set:

If you have not done so already, read all about “Roles” in the playbooks documentation. This helps you make playbook content self-contained, and works well with things like Git submodules for sharing content with others.

If some of these plugin types look strange to you, see the API documentation for more details about ways Ansible can be extended.

See Configuring Ansible.

If cowsay is installed, Ansible takes it upon itself to make your day happier when running playbooks. If you decide that you would like to work in a professional cow-free environment, you can either uninstall cowsay, set nocows=1 in ansible.cfg, or set the ANSIBLE_NOCOWS environment variable:

Ansible by default gathers “facts” about the machines under management, and these facts can be accessed in playbooks and in templates. To see a list of all of the facts that are available about a machine, you can run the setup module as an ad hoc action:

This will print out a dictionary of all of the facts that are available for that particular host. You might want to pipe the output to a pager.This does NOT include inventory variables or internal ‘magic’ variables. See the next question if you need more than just ‘facts’.

By running the following command, you can see inventory variables for a host:

To see all host specific variables, which might include facts and other sources:

Unless you are using a fact cache, you normally need to use a play that gathers facts first, for facts included in the task above.

A pretty common pattern is to iterate over a list of hosts inside of a host group, perhaps to populate a template configuration file with a list of servers. To do this, you can just access the “$groups” dictionary in your template, like this:

If you need to access facts about these hosts, for example, the IP address of each hostname, you need to make sure that the facts have been populated. For example, make sure you have a play that talks to db_servers:

Then you can use the facts inside your template, like this:

An example may come up where we need to get the ipv4 address of an arbitrary interface, where the interface to be used may be supplied through a role parameter or other input. Variable names can be built by adding strings together using “~”, like so:

The trick about going through hostvars is necessary because it is a dictionary of the entire namespace of variables. inventory_hostname is a magic variable that indicates the current host you are looping over in the host loop.

In the example above, if your interface names have dashes, you must replace them with underscores:

Also see dynamic_variables.

Technically, you don’t, Ansible does not really use groups directly. Groups are labels for host selection and a way to bulk assign variables, they are not a first class entity, Ansible only cares about Hosts and Tasks.

That said, you could just access the variable by selecting a host that is part of that group, see first_host_in_a_group below for an example.

What happens if we want the ip address of the first webserver in the webservers group? Well, we can do that too. Note that if we are using dynamic inventory, which host is the ‘first’ may not be consistent, so you wouldn’t want to do this unless your inventory is static and predictable. (If you are using AWX or the Red Hat Ansible Automation Platform, it will use database order, so this isn’t a problem even if you are using cloud based inventory scripts).

Anyway, here’s the trick:

Notice how we’re pulling out the hostname of the first machine of the webservers group. If you are doing this in a template, you could use the Jinja2 ‘#set’ directive to simplify this, or in a playbook, you could also use set_fact:

Notice how we interchanged the bracket syntax for dots – that can be done anywhere.

The copy module has a recursive parameter. However, take a look at the synchronize module if you want to do something more efficient for a large number of files. The synchronize module wraps rsync. See the module index for info on both of these modules.

On control node machine : Access existing variables from control node use the env lookup plugin. For example, to access the value of the HOME environment variable on the management machine:

On target machines : Environment variables are available through facts in the ansible_env variable:

If you need to set environment variables for TASK execution, see Setting the remote environment in the Advanced Playbooks section. There are several ways to set environment variables on your target machines. You can use the template, replace, or lineinfile modules to introduce environment variables into files. The exact files to edit vary depending on your OS and distribution and local configuration.

Ansible ad hoc command is the easiest option:

The mkpasswd utility that is available on most Linux systems is also a great option:

If this utility is not installed on your system (for example, you are using macOS) then you can still easily generate these passwords using Python. First, ensure that the Passlib password hashing library is installed:

Once the library is ready, SHA512 password values can then be generated as follows:

Use the integrated Hashing and encrypting strings and passwords to generate a hashed version of a password. You shouldn’t put plaintext passwords in your playbook or host_vars; instead, use Using encrypted variables and files to encrypt sensitive data.

In OpenBSD, a similar option is available in the base system called encrypt (1)

The dot notation comes from Jinja and works fine for variables without special characters. If your variable contains dots (.), colons (:), or dashes (-), if a key begins and ends with two underscores, or if a key uses any of the known public attributes, it is safer to use the array notation. See Using variables for a list of the known public attributes.

Also array notation allows for dynamic variable composition, see dynamic_variables.

Another problem with ‘dot notation’ is that some keys can cause problems because they collide with attributes and methods of python dictionaries.

Example of incorrect syntax when item is a dictionary:

This variant causes a syntax error because update() is a Python method for dictionaries.

Example of correct syntax:

You can set all of a task’s arguments from a dictionary-typed variable. This technique can be useful in some dynamic execution scenarios. However, it introduces a security risk. We do not recommend it, so Ansible issues a warning when you do something like this:

This particular example is safe. However, constructing tasks like this is risky because the parameters and values passed to usermod_args could be overwritten by malicious values in the host facts on a compromised target machine. To mitigate this risk:

set bulk variables at a level of precedence greater than host facts in the order of precedence found in Variable precedence: where should I put a variable? (the example above is safe because play vars take precedence over facts)

disable the INJECT_FACTS_AS_VARS configuration setting to prevent fact values from colliding with variables (this will also disable the original warning)

Yes! See our services page for information on our services and training offerings. Email info@ansible.com for further details.

We also offer free web-based training classes on a regular basis. See our webinar page for more info on upcoming webinars.

Yes! The open-source web interface is Ansible AWX. The supported Red Hat product that makes Ansible even more powerful and easy to use is Red Hat Ansible Automation Platform.

If you would like to keep secret data in your Ansible content and still share it publicly or keep things in source control, see Using encrypted variables and files.

If you have a task that you don’t want to show the results or command given to it when using -v (verbose) mode, the following task or playbook attribute can be useful:

This can be used to keep verbose output but hide sensitive information from others who would otherwise like to be able to see the output.

The no_log attribute can also apply to an entire play:

Though this will make the play somewhat difficult to debug. It is recommended that this be applied to single tasks only, once a playbook is completed. Note that the use of the no_log attribute does not prevent data from being shown when debugging Ansible itself through the ANSIBLE_DEBUG environment variable.

A steadfast rule is ‘always use {{ }} except when when:’. Conditionals are always run through Jinja2 as to resolve the expression, so when:, failed_when: and changed_when: are always templated and you should avoid adding {{ }}.

In most other cases you should always use the brackets, even if previously you could use variables without specifying (like loop or with_ clauses), as this made it hard to distinguish between an undefined variable and a string.

Another rule is ‘moustaches don’t stack’. We often see this:

The above DOES NOT WORK as you expect, if you need to use a dynamic variable use the following as appropriate:

For ‘non host vars’ you can use the vars lookup plugin:

To determine if a keyword requires {{ }} or even supports templating, use ansible-doc -t keyword <name>, this will return documentation on the keyword including a template field with the values explicit (requires {{ }}), implicit (assumes {{ }}, so no needed) or static (no templating supported, all characters will be interpreted literally)

As the documentation states, connection variables are taken from the delegate_to host so ansible_host is overwritten, but you can still access the original through hostvars:

This works for all overridden connection variables, like ansible_user, ansible_port, and so on.

Since release 7.9p1 of OpenSSH there is a bug in the SCP client that can trigger this error on the Ansible control node when using SCP as the file transfer mechanism:

failed to transfer file to /tmp/ansible/file.txtrnprotocol error: file name does not match request

In these releases, SCP tries to validate that the path of the file to fetch matches the requested path. The validation fails if the remote file name requires quotes to escape spaces or non-ascii characters in its path. To avoid this error:

Rely on the default setting, which is smart — this works if ssh_transfer_method is not explicitly set anywhere

Set a host variable or group variable in inventory: ansible_ssh_transfer_method: smart

Set an environment variable on your control node: export ANSIBLE_SSH_TRANSFER_METHOD=smart

Pass an environment variable when you run Ansible: ANSIBLE_SSH_TRANSFER_METHOD=smart ansible-playbook

Modify your ansible.cfg file: add ssh_transfer_method=smart to the [ssh_connection] section. The smart setting attempts to use sftp for the transfer, then falls back to scp and then dd. If you want the transfer to fail if SFTP is not available, add ssh_transfer_method=sftp to the [ssh_connection] section.

Set a host variable or group variable: ansible_scp_extra_args=-T,

Export or pass an environment variable: ANSIBLE_SCP_EXTRA_ARGS=-T

Modify your ansible.cfg file: add scp_extra_args=-T to the [ssh_connection] section

If you see an invalid argument error when using -T, then your SCP client is not performing file name validation and will not trigger this error.

No, Ansible is designed to execute multiple tasks against multiple targets, minimizing user interaction. As with most automation tools, it is not compatible with interactive security systems designed to handle human interaction. Most of these systems require a secondary prompt per target, which prevents scaling to thousands of targets. They also tend to have very short expiration periods so it requires frequent reauthorization, also an issue with many hosts and/or a long set of tasks.

In such environments we recommend securing around Ansible’s execution but still allowing it to use an ‘automation user’ that does not require such measures. With AWX or the Red Hat Ansible Automation Platform, administrators can set up RBAC access to inventory, along with managing credentials and job execution.

Many Ansible modules that create or update files have a validate option that allows you to abort the update if the validation command fails. This uses the temporary file Ansible creates before doing the final update. In many cases this does not work since the validation tools for the specific application require either specific names, multiple files or some other factor that is not present in this simple feature.

For these cases you have to handle the validation and restoration yourself. The following is a simple example of how to do this with block/rescue and backups, which most file based modules also support:

Documentation for Ansible is kept in the ansible/ansible-documentation project Git repository. See Contributing to the Ansible Documentation for details.

Neither is a real collection. They are virtually constructed by the core engine (synthetic collections).

The ansible.builtin collection only refers to plugins that ship with ansible-core.

The ansible.legacy collection is a superset of ansible.builtin (you can reference the plugins from builtin through ansible.legacy). You also get the ability to add ‘custom’ plugins in the configured paths and adjacent directories, with the ability to override the builtin plugins that have the same name.

Also, ansible.legacy is what you get by default when you do not specify an FQCN. So this:

Is really equivalent to:

Though, if you do not override the shell module, you can also just write it as ansible.builtin.shell, since legacy will resolve to the builtin collection.

If you have not found an answer to your questions, ask the community! Visit the Ansible communication guide for details.

An introduction to playbooks

Tips and tricks for playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
shell:
  cmd: date
environment:
  LANG=fr_FR.UTF-8
```

Example 2 (unknown):
```unknown
hosts: servers
environment:
  PATH: "{{ ansible_env.PATH }}:/thingy/bin"
  SOME: value
```

Example 3 (unknown):
```unknown
[webservers]
asdf.example.com  ansible_port=5000   ansible_user=alice
jkl.example.com   ansible_port=5001   ansible_user=bob
```

Example 4 (unknown):
```unknown
[testcluster]
localhost           ansible_connection=local
/path/to/chroot1    ansible_connection=chroot
foo.example.com     ansible_connection=paramiko
```

---

## Debugging tasks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_debugger.html

**Contents:**
- Debugging tasks
- Enabling the debugger
  - Enabling the debugger with the debugger keyword
    - Examples of using the debugger keyword
  - Enabling the debugger in configuration or an environment variable
  - Enabling the debugger as a strategy
- Resolving errors in the debugger
- Available debug commands
  - Print command
  - Update args command

Ansible offers a task debugger so you can fix errors during execution instead of editing your playbook and running it again to see if your change worked. You have access to all of the features of the debugger in the context of the task. You can check or set the value of variables, update module arguments, and re-run the task with the new variables and arguments. The debugger lets you resolve the cause of the failure and continue with playbook execution.

Enabling the debugger

Enabling the debugger with the debugger keyword

Examples of using the debugger keyword

Enabling the debugger in configuration or an environment variable

Enabling the debugger as a strategy

Resolving errors in the debugger

Available debug commands

How the debugger interacts with the free strategy

The debugger is not enabled by default. If you want to invoke the debugger during playbook execution, you must enable it first.

Use one of these three methods to enable the debugger:

with the debugger keyword

in configuration or an environment variable, or

You can use the debugger keyword to enable (or disable) the debugger for a specific play, role, block, or task. This option is especially useful when developing or extending playbooks, plays, and roles. You can enable the debugger on new or updated tasks. If they fail, you can fix the errors efficiently. The debugger keyword accepts five values:

Always invoke the debugger, regardless of the outcome

Never invoke the debugger, regardless of the outcome

Only invoke the debugger if a task fails

Only invoke the debugger if a host is unreachable

Only invoke the debugger if the task is skipped

When you use the debugger keyword, the value you specify overrides any global configuration to enable or disable the debugger. If you define debugger at multiple levels, such as in a role and in a task, Ansible honors the most granular definition. The definition at the play or role level applies to all blocks and tasks within that play or role unless they specify a different value. A definition at the block level overrides a definition at the play or role level and applies to all tasks within that block unless they specify a different value. A definition at the task level always applies to the task; it overrides definitions at the block, play, or role level.

Example of setting the debugger keyword on a task:

Example of setting the debugger keyword on a play:

Example of setting the debugger keyword at multiple levels:

In this example, the debugger is set to never at the play level and to on_failed at the task level. If the task fails, Ansible invokes the debugger, because the task’s definition overrides that of its parent play.

You can enable the task debugger globally with a setting in ansible.cfg or with an environment variable. The only options are True or False. If you set the configuration option or environment variable to True, Ansible runs the debugger on failed tasks by default.

To enable the task debugger from ansible.cfg, add this setting to the [defaults] section:

To enable the task debugger with an environment variable, pass the variable when you run your playbook:

When you enable the debugger globally, every failed task invokes the debugger, unless the role, play, block, or task explicitly disables the debugger. If you need more granular control over what conditions trigger the debugger, use the debugger keyword.

If you are running legacy playbooks or roles, you may see the debugger enabled as a strategy. You can do this at the play level, in ansible.cfg, or with the environment variable ANSIBLE_STRATEGY=debug. For example:

This backwards-compatible method, which matches Ansible versions before 2.5, may be removed in a future release.

After Ansible invokes the debugger, you can use the seven debugger commands to resolve the error that Ansible encountered. Consider this example playbook, which defines the var1 variable but uses the undefined wrong_var variable in a task by mistake.

If you run this playbook, Ansible invokes the debugger when the task fails. From the debug prompt, you can change the module arguments or the variables and run the task again.

Changing the task arguments in the debugger to use var1 instead of wrong_var makes the task run successfully.

You can use these seven commands at the debug prompt:

Print information about the task

task.args[key] = value

Update module arguments

task_vars[key] = value

Update task variables (you must update_task next)

Recreate a task with updated task variables

Continue executing, starting with the next task

For more details, see the individual descriptions and examples below.

print *task/task.args/task_vars/host/result* prints information about the task.

task.args[*key*] = *value* updates a module argument. This sample playbook has an invalid package name.

When you run the playbook, the invalid package name triggers an error, and Ansible invokes the debugger. You can fix the package name by viewing, and then updating the module argument.

After you update the module argument, use redo to run the task again with the new args.

task_vars[*key*] = *value* updates the task_vars. You could fix the playbook above by viewing and then updating the task variables instead of the module args.

After you update the task variables, you must use update_task to load the new variables before using redo to run the task again.

In 2.5 this was updated from vars to task_vars to avoid conflicts with the vars() python function.

u or update_task recreates the task from the original task data structure and templates with updated task variables. See the entry Update vars command for an example of use.

r or redo runs the task again.

c or continue continues executing, starting with the next task.

q or quit quits the debugger. The playbook execution is aborted.

With the default linear strategy enabled, Ansible halts execution while the debugger is active, and runs the debugged task immediately after you enter the redo command. With the free strategy enabled, however, Ansible does not wait for all hosts and may queue later tasks on one host before a task fails on another host. With the free strategy, Ansible does not queue or execute any tasks while the debugger is active. However, all queued tasks remain in the queue and run as soon as you exit the debugger. If you use redo to reschedule a task from the debugger, other queued tasks may execute before your rescheduled task. For more information about strategies, see Controlling playbook execution: strategies and more.

Running playbooks while debugging or testing

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- name: Execute a command
  ansible.builtin.command: "false"
  debugger: on_failed
```

Example 2 (unknown):
```unknown
- name: My play
  hosts: all
  debugger: on_skipped
  tasks:
    - name: Execute a command
      ansible.builtin.command: "true"
      when: False
```

Example 3 (unknown):
```unknown
- name: Play
  hosts: all
  debugger: never
  tasks:
    - name: Execute a command
      ansible.builtin.command: "false"
      debugger: on_failed
```

Example 4 (unknown):
```unknown
[defaults]
enable_task_debugger = True
```

---

## Manipulating data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/complex_data_manipulation.html

**Contents:**
- Manipulating data
- Loops and list comprehensions
  - Extract keys from a dictionary matching elements from a list
  - Find mount point
  - Combine values from same list of dicts
  - Custom Fileglob Based on a Variable
- Complex Type transformations
  - Create dictionary from list

In many cases, you will need to perform complex operations with your variables. While Ansible is not recommended as a data processing/manipulation tool, you can use the existing Jinja2 templating in conjunction with the many added Ansible filters, lookups and tests to perform some very complex transformations.

lookups: Mainly used to query ‘external data’, in Ansible these were the primary part of loops using the with_<lookup> construct, but they can be used independently to return data for processing. They normally return a list due to their primary function in loops as mentioned previously. Used with the lookup or query Jinja2 operators.

filters: used to change/transform data, used with the | Jinja2 operator.

tests: used to validate data, used with the is Jinja2 operator.

Most programming languages have loops (for, while, and so on) and list comprehensions to do transformations on lists including lists of objects. Jinja2 has a few filters that provide this functionality: map, select, reject, selectattr, rejectattr.

map: this is a basic for loop that just allows you to change every item in a list, using the ‘attribute’ keyword you can do the transformation based on attributes of the list elements.

select/reject: this is a for loop with a condition, that allows you to create a subset of a list that matches (or not) based on the result of the condition.

selectattr/rejectattr: very similar to the above but it uses a specific attribute of the list elements for the conditional statement.

Use a loop to create exponential backoff.

The Python equivalent code would be:

There are several ways to do it in Ansible, this is just one example:

In this case, we want to find the mount point for a given path across our machines, since we already collect mount facts, we can use the following:

Combining positive and negative filters from the examples above, you can get a ‘value when it exists’ and a ‘fallback’ when it doesn’t.

This example uses Python argument list unpacking to create a custom list of fileglobs based on a variable.

Jinja provides filters for simple data type transformations (int, bool, and so on), but when you want to transform data structures things are not as easy. You can use loops and list comprehensions as shown above to help, also other filters and lookups can be chained and used to achieve more complex transformations.

In most languages, it is easy to create a dictionary (also known as map/associative array/hash and so on) from a list of pairs. In Ansible there are a couple of ways to do it, and the best one for you might depend on the source of your data.

These example produces {"a": "b", "c": "d"}

Both end up being the same thing, with zip_longest transforming single_list to a list_of_pairs generator.

A bit more complex, using set_fact and a loop to create/update a dictionary with key value pairs from 2 lists:

This results in {"foo": "a", "var": "b", "bar": "c"}.

You can even combine these simple examples with other filters and lookups to create a dictionary dynamically by matching patterns to variable names:

A quick explanation, since there is a lot to unpack from these two lines:

The varnames lookup returns a list of variables that match “begin with xyz_”.

Then feeding the list from the previous step into the vars lookup to get the list of values. The * is used to ‘dereference the list’ (a pythonism that works in Jinja), otherwise it would take the list as a single argument.

Both lists get passed to the zip filter to pair them off into a unified list (key, value, key2, value2, …).

The dict function then takes this ‘list of pairs’ to create the dictionary.

An example of how to use facts to find a host’s data that meets condition X:

An example to show a host uptime in days/hours/minutes/seconds (assuming facts were gathered).

Jinja2 filters included with Ansible

Jinja2 tests included with Ansible

Jinja2 documentation, includes lists for core filters and tests

**Examples:**

Example 1 (unknown):
```unknown
- name: try wait_for_connection up to 10 times with exponential delay
  ansible.builtin.wait_for_connection:
    delay: '{{ item | int }}'
    timeout: 1
  loop: '{{ range(1, 11) | map("pow", 2) }}'
  loop_control:
    extended: true
  ignore_errors: "{{ not ansible_loop.last }}"
  register: result
  when: result is not defined or result is failed
```

Example 2 (unknown):
```unknown
chains = [1, 2]
for chain in chains:
    for config in chains_config[chain]['configs']:
        print(config['type'])
```

Example 3 (unknown):
```unknown
tasks:
   - name: Show extracted list of keys from a list of dictionaries
     ansible.builtin.debug:
       msg: "{{ chains | map('extract', chains_config) | map(attribute='configs') | flatten | map(attribute='type') | flatten }}"
     vars:
       chains: [1, 2]
       chains_config:
           1:
               foo: bar
               configs:
                   - type: routed
                     version: 0.1
                   - type: bridged
                     version: 0.2
           2:
               foo: baz
               configs:
                   - type: routed
                     version: 1.0
                   - type: bridged
                     version: 1.1
```

Example 4 (javascript):
```javascript
ok: [localhost] => {
       "msg": [
           "routed",
           "bridged",
           "routed",
           "bridged"
       ]
   }
```

---

## Galaxy User Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/galaxy/user_guide.html

**Contents:**
- Galaxy User Guide
- Finding collections on Galaxy
- Finding roles on Galaxy
  - Get more information about a role
- Installing roles from Galaxy
  - Installing roles
    - Setting where to install roles
  - Installing a specific version of a role
  - Installing multiple roles from a file
  - Installing roles and collections from the same requirements.yml file

Ansible Galaxy refers to the Galaxy website, a free site for finding, downloading, and sharing community developed collections and roles.

Use Galaxy to jump-start your automation project with great content from the Ansible community. Galaxy provides pre-packaged units of work such as roles, and collections. The collection format provides a comprehensive package of automation that may include multiple playbooks, roles, modules, and plugins. See the Galaxy documentation for full details on Galaxy.

Finding collections on Galaxy

Finding roles on Galaxy

Get more information about a role

Installing roles from Galaxy

Installing a specific version of a role

Installing multiple roles from a file

Installing roles and collections from the same requirements.yml file

Installing multiple roles from multiple files

Remove an installed role

To find collections on Galaxy:

Click Collections > Collections in the left-hand navigation.

Type in your search term. You can filter by keyword, tags, and namespaces.

Galaxy presents a list of collections that match your search criteria.

See Using Ansible collections for complete details on installing and using collections.

To find standalone roles (that is roles that are not part of a collection):

Click Roles > Roles in the left-hand navigation.

Type in your search term. You can filter by keyword, tags, and namespaces.

Galaxy presents a list of roles that match your search criteria.

You can optionally search the Galaxy database by tags, platforms, author and multiple keywords using the ansible-galaxy CLI command.

The search command will return a list of the first 1000 results matching your search:

Use the info command to view more detail about a specific role:

This returns everything found in Galaxy for the role:

The ansible-galaxy command comes bundled with Ansible, and you can use it to install roles from Galaxy or directly from a Git based SCM. You can also use it to create a new role, remove roles, or perform tasks on the Galaxy website.

The command line tool by default communicates with the Galaxy website API using the server address https://galaxy.ansible.com. If you run your own internal Galaxy server and want to use it instead of the default one, pass the --server option followed by the address of this galaxy server. You can set this option permanently by setting the Galaxy server value in your ansible.cfg file. See GALAXY_SERVER for details on setting the value in ansible.cfg .

Use the ansible-galaxy command to download roles from the Galaxy website

By default, Ansible downloads roles to the first writable directory in the default list of paths ~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles. This installs roles in the home directory of the user running ansible-galaxy.

You can override this with one of the following options:

Set the environment variable ANSIBLE_ROLES_PATH in your session.

Use the --roles-path option for the ansible-galaxy command.

Define roles_path in an ansible.cfg file.

The following provides an example of using --roles-path to install the role into the current working directory:

All about configuration files

When the Galaxy server imports a role, it imports any Git tags matching the Semantic Version format as versions. In turn, you can download a specific version of a role by specifying one of the imported tags.

To see the available versions for a role:

Locate the role on the Galaxy search page.

Click on the name to view more details, including the available versions.

To install a specific version of a role from Galaxy, append a comma and the value of a GitHub release tag. For example:

It is also possible to point directly to the Git repository and specify a branch name or commit hash as the version. For example, the following will install a specific commit:

You can install multiple roles by including the roles in a requirements.yml file. The format of the file is YAML, and the file extension must be either .yml or .yaml.

Use the following command to install roles included in requirements.yml:

Again, the extension is important. If the .yml extension is left off, the ansible-galaxy CLI assumes the file is in an older, now deprecated, “basic” format.

Each role in the file will have one or more of the following attributes:

The source of the role. Use the format namespace.role_name, if downloading from Galaxy; otherwise, provide a URL pointing to a repository within a Git based SCM. See the examples below. This is a required attribute.

Specify the SCM. As of this writing only git or hg are allowed. See the examples below. Defaults to git.

The version of the role to download. Provide a release tag value, commit hash, or branch name. Defaults to the branch set as a default in the repository, otherwise defaults to the master.

Download the role to a specific name. Defaults to the Galaxy name when downloading from Galaxy, otherwise it defaults to the name of the repository.

Use the following example as a guide for specifying roles in requirements.yml:

Embedding credentials into a SCM URL is not secure. Make sure to use safe auth options for security reasons. For example, use SSH, netrc or http.extraHeader/url.<base>.pushInsteadOf in Git config to prevent your credentials from being exposed in logs.

You can install roles and collections from the same requirements files

For large projects, the include directive in a requirements.yml file provides the ability to split a large file into multiple smaller files.

For example, a project may have a requirements.yml file, and a webserver.yml file.

Below are the contents of the webserver.yml file:

The following shows the contents of the requirements.yml file that now includes the webserver.yml file:

To install all the roles from both files, pass the root file, in this case requirements.yml on the command line, as follows:

Roles can also be dependent on other roles, and when you install a role that has dependencies, those dependencies will automatically be installed to the roles_path.

There are two ways to define the dependencies of a role:

using meta/requirements.yml

You can create the file meta/requirements.yml and define dependencies in the same format used for requirements.yml described in the Installing multiple roles from a file section.

From there, you can import or include the specified roles in your tasks.

Alternatively, you can specify role dependencies in the meta/main.yml file by providing a list of roles under the dependencies section. If the source of a role is Galaxy, you can simply specify the role in the format namespace.role_name. You can also use the more complex format in requirements.yml, allowing you to provide src, scm, version, and name.

Dependencies installed that way, depending on other factors described below, will also be executed before this role is executed during play execution. To better understand how dependencies are handled during play execution, see Roles.

The following shows an example meta/main.yml file with dependent roles:

Tags are inherited down the dependency chain. In order for tags to be applied to a role and all its dependencies, the tag should be applied to the role, not to all the tasks within a role.

Roles listed as dependencies are subject to conditionals and tag filtering, and may not execute fully depending on what tags and conditionals are applied.

If the source of a role is Galaxy, specify the role in the format namespace.role_name:

Alternately, you can specify the role dependencies in the complex form used in requirements.yml as follows:

Galaxy expects all role dependencies to exist in Galaxy, and therefore dependencies to be specified in the namespace.role_name format. If you import a role with a dependency where the src value is a URL, the import process will fail.

Use list to show the name and version of each role installed in the roles_path.

Use remove to delete a role from roles_path:

Shareable collections of modules, playbooks and roles

Reusable tasks, handlers, and other files in a known directory structure

Perform other related operations

**Examples:**

Example 1 (unknown):
```unknown
$ ansible-galaxy role search elasticsearch --author geerlingguy
```

Example 2 (unknown):
```unknown
Found 6 roles matching your search:

 Name                             Description
 ----                             -----------
geerlingguy.elasticsearch         Elasticsearch for Linux.
geerlingguy.elasticsearch-curator Elasticsearch curator for Linux.
geerlingguy.filebeat              Filebeat for Linux.
geerlingguy.fluentd               Fluentd for Linux.
geerlingguy.kibana                Kibana for Linux.
```

Example 3 (unknown):
```unknown
$ ansible-galaxy role info username.role_name
```

Example 4 (unknown):
```unknown
Role: username.role_name
    description: Installs and configures a thing, a distributed, highly available NoSQL thing.
    active: True
    commit: c01947b7bc89ebc0b8a2e298b87ab416aed9dd57
    commit_message: Adding travis
    commit_url: https://github.com/username/repo_name/commit/c01947b7bc89ebc0b8a2e298b87ab
    company: My Company, Inc.
    created: 2015-12-08T14:17:52.773Z
    download_count: 1
    forks_count: 0
    github_branch: main
    github_repo: repo_name
    github_user: username
    id: 6381
    is_valid: True
    issue_tracker_url:
    license: Apache
    min_ansible_version: 2.15
    modified: YYYY-MM-DDTHH:MM:SS.000Z
    namespace: username
    open_issues_count: 0
    path: /Users/username/projects/roles
    role_type: ANS
    stargazers_count: 0
    travis_status_url: https://travis-ci.org/username/repo_name.svg?branch=main
```

---

## Advanced playbook syntax — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_advanced_syntax.html

**Contents:**
- Advanced playbook syntax
- Unsafe or raw strings
- YAML anchors and aliases: sharing variable values

The advanced YAML syntax examples on this page give you more control over the data placed in YAML files used by Ansible. You can find additional information about Python-specific YAML in the official PyYAML Documentation.

When handling values returned by lookup plugins, Ansible uses a data type called unsafe to block templating. Marking data as unsafe prevents malicious users from abusing Jinja2 templates to execute arbitrary code on target machines. The Ansible implementation ensures that unsafe values are never templated. It is more comprehensive than escaping Jinja2 with {% raw %} ... {% endraw %} tags.

You can use the same unsafe data type in variables you define, to prevent templating errors and information disclosure. You can mark values supplied by vars_prompts as unsafe. You can also use unsafe in playbooks. The most common use cases include passwords that allow special characters like { or %, and JSON arguments that look like templates but should not be templated. For example:

For complex variables such as hashes or arrays, use !unsafe on the individual elements:

YAML anchors and aliases help you define, maintain, and flexibly use shared variable values. You define an anchor with &, then refer to it using an alias, denoted with *. Here’s an example that sets three values with an anchor, uses two of those values with an alias, and overrides the third value:

Here, app1 and app2 share the values for opts and port using the anchor &jvm_opts and the alias *jvm_opts. The value for path is merged by << or merge operator.

Anchors and aliases also let you share complex sets of variable values, including nested variables. If you have one variable value that includes another variable value, you can define them separately:

This is inefficient and, at scale, means more maintenance. To incorporate the version value in the name, you can use an anchor in app_version and an alias in custom_name:

Now, you can reuse the value of app_version within the value of custom_name and use the output in a template:

You’ve anchored the value of version with the &my_version anchor and reused it with the *my_version alias. Anchors and aliases let you access nested values inside dictionaries.

Doing complex data manipulation in Ansible

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
---
mypassword: !unsafe 234%234{435lkj{{lkjsdf
```

Example 2 (unknown):
```unknown
---
hosts: all
vars:
  my_unsafe_variable: !unsafe 'unsafe % value'
tasks:
    ...
```

Example 3 (unknown):
```unknown
---
my_unsafe_array:
  - !unsafe 'unsafe element'
  - 'safe element'

my_unsafe_hash:
  unsafe_key: !unsafe 'unsafe value'
```

Example 4 (unknown):
```unknown
---
# ...
vars:
  app1:
    jvm: &jvm_opts
      opts: '-Xms1G -Xmx2G'
      port: 1000
      path: /usr/lib/app1
  app2:
    jvm:
      <<: *jvm_opts
      path: /usr/lib/app2
# ...
```

---

## ansible.builtin.pause module – Pause playbook execution — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/pause_module.html

**Contents:**
- ansible.builtin.pause module – Pause playbook execution
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
- Return Values
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name pause even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.pause for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Pauses playbook execution for a set amount of time, or until a prompt is acknowledged. All parameters are optional. The default behavior is to pause with a prompt.

To pause/wait/sleep per host, use the ansible.builtin.wait_for module.

You can use ctrl+c if you wish to advance a pause earlier than it is set to expire or if you need to abort a playbook run entirely. To continue early press ctrl+c and then c. To abort a playbook press ctrl+c and then a.

Prompting for a set amount of time is not supported. Pausing playbook execution is interruptible but does not return user input.

The pause module integrates into async/parallelized playbooks without any special considerations (see Rolling Updates). When using pauses with the serial playbook parameter (as in rolling updates) you are only prompted once for the current group of hosts.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

Controls whether or not keyboard input is shown when typing.

Only has effect if neither seconds nor minutes are set.

A positive number of minutes to pause for.

Optional text to use for the prompt message.

User input is only returned if seconds and minutes are both not specified, otherwise this is just a custom message before playbook execution is paused.

A positive number of seconds to pause for.

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

Starting in 2.2, if you specify 0 or negative for minutes or seconds, it will wait for 1 second, previously it would wait indefinitely.

User input is not captured or echoed, regardless of echo setting, when minutes or seconds is specified.

Common return values are documented here, the following are the fields unique to this module:

Time paused in seconds

Value of echo setting

Time when started pausing

Sample: "2017-02-23 14:35:07.298862"

Output of pause module

Sample: "Paused for 0.04 minutes"

Time when ended pausing

Sample: "2017-02-23 14:35:09.552594"

User input from interactive console

Returned: if no waiting time set

Sample: "Example user input"

Tim Bielawa (@tbielawa)

**Examples:**

Example 1 (unknown):
```unknown
- name: Pause for 5 minutes to build app cache
  ansible.builtin.pause:
    minutes: 5

- name: Pause until you can verify updates to an application were successful
  ansible.builtin.pause:

- name: A helpful reminder of what to look out for post-update
  ansible.builtin.pause:
    prompt: "Make sure org.foo.FooOverload exception is not present"

- name: Pause to get some sensitive input
  ansible.builtin.pause:
    prompt: "Enter a secret"
    echo: no
```

---

## Ansible-core 2.14 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.14.html

**Contents:**
- Ansible-core 2.14 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins
- Porting custom scripts

This section discusses the behavioral changes between ansible-core 2.13 and ansible-core 2.14.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.14 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.14 Porting Guide

Noteworthy module changes

Porting custom scripts

Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.14.12, conditional expressions with embedded template blocks can fail with the message “Conditional is marked as unsafe, and cannot be evaluated.” when an embedded template consults data from untrusted sources like module results or vars marked !unsafe. Conditionals with embedded templates can be a source of malicious template injection when referencing untrusted data, and can nearly always be rewritten without embedded templates. Playbook task conditional keywords such as when and until have long displayed warnings discouraging use of embedded templates in conditionals; this warning has been expanded to non-task conditionals as well, such as the assert action.

Variables are now evaluated lazily; only when they are actually used. For example, in ansible-core 2.14 an expression {{ defined_variable or undefined_variable }} does not fail on undefined_variable if the first part of or is evaluated to True as it is not needed to evaluate the second part. One particular case of a change in behavior to note is the task below which uses the undefined test. Prior to version 2.14 this would result in a fatal error trying to access the undefined value in the dictionary. In 2.14 the assertion passes as the dictionary is evaluated as undefined through one of its undefined values:

Python 3.9 on the controller node is a hard requirement for this release.

At startup the filesystem encoding and locale are checked to verify they are UTF-8. If not, the process exits with an error reporting the errant encoding. If you were previously using the C or POSIX locale, you may be able to use C.UTF-8. If you were previously using a locale such as en_US.ISO-8859-1, you may be able to use en_US.UTF-8. For simplicity it may be easiest to export the appropriate locale using the LC_ALL environment variable. An alternative to modifying your system locale is to run Python in UTF-8 mode; See the Python documentation for more information.

The following modules no longer exist:

**Examples:**

Example 1 (unknown):
```unknown
- name: task with a module result (always untrusted by Ansible)
  shell: echo "hi mom"
  register: untrusted_result

# don't do it this way...
# - name: insecure conditional with embedded template consulting untrusted data
#   assert:
#     that: '"hi mom" is in {{ untrusted_result.stdout }}'

- name: securely access untrusted values directly as Jinja variables instead
  assert:
    that: '"hi mom" is in untrusted_result.stdout'
```

Example 2 (unknown):
```unknown
- assert:
    that:
      - some_defined_dict_with_undefined_values is undefined
  vars:
    dict_value: 1
    some_defined_dict_with_undefined_values:
      key1: value1
      key2: '{{ dict_value }}'
      key3: '{{ undefined_dict_value }}'
```

---

## ansible-playbook — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-playbook.html

**Contents:**
- ansible-playbook
- Synopsis
- Description
- Common Options
- Environment
- Files
- Author
- License
- See also

Runs Ansible playbooks, executing the defined tasks on the targeted hosts.

the tool to run Ansible playbooks, which are a configuration and multinode deployment system. See the project home page (https://docs.ansible.com) for more information.

privilege escalation method to use (default=sudo), use ansible-doc -t become -l to list valid choices.

run operations as this user (default=root)

Connection password file

clear the fact cache for every host in inventory

run handlers even if a task fails

outputs a list of matching hosts; does not execute anything else

list all available tags

list all tasks that would be executed

use this file to authenticate the connection

specify extra arguments to pass to scp only (e.g. -l)

specify extra arguments to pass to sftp only (e.g. -f, -l)

only run plays and tasks whose tags do not match these values. This argument may be specified multiple times.

specify common arguments to pass to sftp/scp/ssh (e.g. ProxyCommand)

specify extra arguments to pass to ssh only (e.g. -R)

start the playbook at the task matching this name

one-step-at-a-time: confirm each task before running

perform a syntax check on the playbook, but do not execute it

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

only run plays and tasks tagged with these values. This argument may be specified multiple times.

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

ansible(1), ansible-config(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-playbook [-h] [--version] [-v] [--private-key PRIVATE_KEY_FILE]
                     [-u REMOTE_USER] [-c CONNECTION] [-T TIMEOUT]
                     [--ssh-common-args SSH_COMMON_ARGS]
                     [--sftp-extra-args SFTP_EXTRA_ARGS]
                     [--scp-extra-args SCP_EXTRA_ARGS]
                     [--ssh-extra-args SSH_EXTRA_ARGS]
                     [-k | --connection-password-file CONNECTION_PASSWORD_FILE]
                     [--force-handlers] [-b]
                     [--become-method BECOME_METHOD]
                     [--become-user BECOME_USER]
                     [-K | --become-password-file BECOME_PASSWORD_FILE]
                     [-t TAGS] [--skip-tags SKIP_TAGS] [-C] [-D]
                     [-i INVENTORY] [--list-hosts] [-l SUBSET]
                     [--flush-cache] [-e EXTRA_VARS] [--vault-id VAULT_IDS]
                     [-J | --vault-password-file VAULT_PASSWORD_FILES]
                     [-f FORKS] [-M MODULE_PATH] [--syntax-check]
                     [--list-tasks] [--list-tags] [--step]
                     [--start-at-task START_AT_TASK]
                     playbook [playbook ...]
```

---

## Controlling playbook execution: strategies and more — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_strategies.html

**Contents:**
- Controlling playbook execution: strategies and more
- Selecting a strategy
- Setting the number of forks
- Using keywords to control execution
  - Setting the batch size with serial
  - Restricting execution with throttle
  - Ordering execution based on inventory
  - Running on a single machine with run_once

By default, Ansible runs each task on all hosts affected by a play before starting the next task on any host, using 5 forks. If you want to change this default behavior, you can use a different strategy plugin, change the number of forks, or apply one of several keywords like serial.

Setting the number of forks

Using keywords to control execution

Setting the batch size with serial

Restricting execution with throttle

Ordering execution based on inventory

Running on a single machine with run_once

The default behavior described above is the linear strategy. Ansible offers other strategies, including the debug strategy (see also Debugging tasks) and the free strategy, which allows each host to run until the end of the play as fast as it can:

You can select a different strategy for each play as shown above, or set your preferred strategy globally in ansible.cfg, under the defaults stanza:

All strategies are implemented as strategy plugins. Please review the documentation for each strategy plugin for details on how it works.

If you have the processing power available and want to use more forks, you can set the number in ansible.cfg:

or pass it on the command line: ansible-playbook -f 30 my_playbook.yml.

In addition to strategies, several keywords also affect play execution. You can set a number, a percentage, or a list of numbers of hosts you want to manage at a time with serial. Ansible completes the play on the specified number or percentage of hosts before starting the next batch of hosts. You can restrict the number of workers allotted to a block or task with throttle. You can control how Ansible selects the next host in a group to execute against with order. You can run a task on a single host with run_once. These keywords are not strategies. They are directives or options applied to a play, block, or task.

Other keywords that affect play execution include ignore_errors, ignore_unreachable, and any_errors_fatal. These options are documented in Error handling in playbooks.

By default, Ansible runs in parallel against all the hosts in the pattern you set in the hosts: field of each play. If you want to manage only a few machines at a time, for example during a rolling update, you can define how many hosts Ansible should manage at a single time using the serial keyword:

In the above example, if we had 6 hosts in the group ‘webservers’, Ansible would execute the play completely (both tasks) on 3 of the hosts before moving on to the next 3 hosts:

Setting the batch size with serial changes the scope of the Ansible failures to the batch size, not the entire host list. You can use ignore_unreachable or max_fail_percentage to modify this behavior.

You can also specify a percentage with the serial keyword. Ansible applies the percentage to the total number of hosts in a play to determine the number of hosts per pass:

If the number of hosts does not divide equally into the number of passes, the final pass contains the remainder. In this example, if you had 20 hosts in the webservers group, the first batch would contain 6 hosts, the second batch would contain 6 hosts, the third batch would contain 6 hosts, and the last batch would contain 2 hosts.

You can also specify batch sizes as a list. For example:

In the above example, the first batch would contain a single host, the next would contain 5 hosts, and (if there are any hosts left), every following batch would contain either 10 hosts or all the remaining hosts, if fewer than 10 hosts remained.

You can list multiple batch sizes as percentages:

You can also mix and match the values:

No matter how small the percentage, the number of hosts per pass will always be 1 or greater.

The throttle keyword limits the number of workers for a particular task. It can be set at the block and task level. Use throttle to restrict tasks that may be CPU-intensive or interact with a rate-limiting API:

If you have already restricted the number of forks or the number of machines to execute against in parallel, you can reduce the number of workers with throttle, but you cannot increase it. In other words, to have an effect, your throttle setting must be lower than your forks or serial setting if you are using them together.

The order keyword controls the order in which hosts are run. Possible values for order are:

(default) The order provided by the inventory for the selection requested (see note below)

The same as above, but reversing the returned list

Sorted alphabetically sorted by name

Sorted by name in reverse alphabetical order

Randomly ordered on each run

the ‘inventory’ order does not equate to the order in which hosts/groups are defined in the inventory source file, but the ‘order in which a selection is returned from the compiled inventory’. This is a backwards compatible option and while reproducible it is not normally predictable. Due to the nature of inventory, host patterns, limits, inventory plugins and the ability to allow multiple sources, it is almost impossible to return such an order. For simple cases, this might happen to match the file definition order, but that is not guaranteed.

If you want a task to run only on the first host in your batch of hosts, set run_once to true on that task:

Ansible executes this task on the first host in the current batch and applies all results and facts to all the hosts in the same batch. This approach is similar to applying a conditional to a task such as:

However, with run_once, the results are applied to all the hosts. To run the task on a specific host, instead of the first host in the batch, delegate the task:

As always with delegation, the action will be executed on the delegated host, but the information is still that of the original host in the task.

When used together with serial, tasks marked as run_once will be run on one host in each serial batch. If the task must run only once regardless of serial mode, use when: inventory_hostname == ansible_play_hosts_all[0] construct.

Any conditional (in other words, when:) will use the variables of the ‘first host’ to decide if the task runs or not, no other hosts will be tested.

If you want to avoid the default behavior of setting the fact for all hosts, set delegate_facts: True for the specific task or block.

An introduction to playbooks

Running tasks on or assigning facts to specific machines

Playbook organization by roles

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- hosts: all
  strategy: free
  tasks:
  # ...
```

Example 2 (unknown):
```unknown
[defaults]
strategy = free
```

Example 3 (unknown):
```unknown
[defaults]
forks = 30
```

Example 4 (unknown):
```unknown
---
- name: test play
  hosts: webservers
  serial: 3
  gather_facts: False

  tasks:
    - name: first task
      command: hostname
    - name: second task
      command: hostname
```

---

## Distributing collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_distributing.html

**Contents:**
- Distributing collections
- Initial configuration of your distribution server or servers
  - Creating a namespace
  - Getting your API token
  - Specifying your API token and distribution server
    - Specifying the token and distribution server in configuration
    - Specifying the token at the command line
- Building your collection tarball
  - Ignoring files and folders
    - Include all, with explicit ignores

A collection is a distribution format for Ansible content. A typical collection contains modules and other plugins that address a set of related use cases. For example, a collection might automate administering a particular database. A collection can also contain roles and playbooks.

Before distributing your collection, ensure you have updated the galaxy.yml file. See Collection structure for details.

To distribute your collection and allow others to use it, you can publish your collection on one or more distribution server. Distribution servers include:

All collections, supports signed collections

Red Hat Automation Hub

Only collections certified by Red Hat, supports signed collections

Privately hosted Automation Hub

Collections authorized by the owners

Distributing collections involves four major steps:

Initial configuration of your distribution server or servers

Building your collection tarball

Preparing to publish your collection

Publishing your collection

Initial configuration of your distribution server or servers

Getting your API token

Specifying your API token and distribution server

Building your collection tarball

Ignoring files and folders

Preparing to publish your collection

Installing your collection locally

Reviewing your collection

Understanding collection versioning

Publishing your collection

Publishing a collection from the command line

Publishing a collection from the website

Configure a connection to one or more distribution servers so you can publish collections there. You only need to configure each distribution server once. You must repeat the other steps (building your collection tarball, preparing to publish, and publishing your collection) every time you publish a new collection or a new version of an existing collection.

Create a namespace on each distribution server you want to use.

Get an API token for each distribution server you want to use.

Specify the API token for each distribution server you want to use.

You must upload your collection into a namespace on each distribution server. If you have a login for Ansible Galaxy, your Ansible Galaxy username is usually also an Ansible Galaxy namespace.

Namespaces on Ansible Galaxy cannot include hyphens. If you have a login for Ansible Galaxy that includes a hyphen, your Galaxy username is not also a Galaxy namespace. For example, awesome-user is a valid username for Ansible Galaxy, but it is not a valid namespace.

You can create additional namespaces on Ansible Galaxy if you choose. For Red Hat Automation Hub and private Automation Hub you must create a namespace before you can upload your collection. To create a namespace:

To create a namespace on Galaxy, see Galaxy namespaces on the Galaxy docsite for details.

To create a namespace on Red Hat Automation Hub, see the Red Hat automation content documentation.

Specify the namespace in the galaxy.yml file for each collection. For more information on the galaxy.yml file, see Collection Galaxy metadata structure.

An API token authenticates your connection to each distribution server. You need a separate API token for each distribution server. Use the correct API token to connect to each distribution server securely and protect your content.

To get your API token:

To get an API token for Galaxy, see the Galaxy documentation.

To get an API token for Automation Hub, see the Red Hat automation content documentation.

Each time you publish a collection, you must specify the API token and the distribution server to create a secure connection. You have two options for specifying the token and distribution server:

You can configure the token in configuration, as part of a galaxy_server_list entry in your ansible.cfg file. Using configuration is the most secure option.

You can pass the token at the command line as an argument to the ansible-galaxy command. If you pass the token at the command line, you can specify the server at the command line, by using the default setting, or by setting the server in configuration. Passing the token at the command line is insecure, because typing secrets at the command line may expose them to other users on the system.

By default, Ansible Galaxy is configured as the only distribution server. You can add other distribution servers and specify your API token or tokens in configuration by editing the galaxy_server_list section of your ansible.cfg file. This is the most secure way to manage authentication for distribution servers. Specify a URL and token for each server. For example:

You cannot use apt-key with any servers defined in your galaxy_server_list. See Configuring the ansible-galaxy client for complete details.

You can specify the API token at the command line using the --token argument of the ansible-galaxy command. There are three ways to specify the distribution server when passing the token at the command line:

using the --server argument of the ansible-galaxy command

relying on the default (https://galaxy.ansible.com)

setting a server in configuration by creating a GALAXY_SERVER setting in your ansible.cfg file

Using the --token argument is insecure. Passing secrets at the command line may expose them to others on the system.

After configuring one or more distribution servers, build a collection tarball. The collection tarball is the published artifact, the object that you upload and other users download to install your collection. To build a collection tarball:

Review all settings in your galaxy.yml file. See Collection Galaxy metadata structure for details. Ensure you have updated the version number. Each time you publish your collection, it must have a new version number. You cannot make changes to existing versions of your collection on a distribution server. If you try to upload the same collection version more than once, the distribution server returns the error Code: conflict.collection_exists. Collections follow semantic versioning rules. For more information on versions, see Understanding collection versioning. For more information on the galaxy.yml file, see Collection Galaxy metadata structure.

Run ansible-galaxy collection build from inside the top-level directory of the collection. For example:

This command builds a tarball of the collection in the current directory, which you can upload to your selected distribution server:

To reduce the size of collections, certain files and folders are excluded from the collection tarball by default. See Ignoring files and folders if your collection directory contains other files you want to exclude.

The current Galaxy maximum tarball size is 2 MB.

You can upload your tarball to one or more distribution servers. You can also distribute your collection locally by copying the tarball to install your collection directly on target systems.

You can exclude files from your collection with either build_ignore or Manifest Directives. For more information on the galaxy.yml file, see Collection Galaxy metadata structure.

By default, the build step includes all the files in the collection directory in the tarball except for the following:

previously built tarballs in the root directory

various version control directories such as .git/

To exclude other files and folders from your collection tarball, set a list of file glob-like patterns in the build_ignore key in the collection’s galaxy.yml file. These patterns use the following special characters for wildcard matching:

*: Matches everything

?: Matches any single character

[seq]: Matches any character in sequence

[!seq]:Matches any character not in sequence

For example, to exclude the sensitive folder within the playbooks folder as well any .tar.gz archives, set the following in your galaxy.yml file:

The build_ignore feature is only supported with ansible-galaxy collection build in Ansible 2.10 or newer.

The galaxy.yml file supports manifest directives that are historically used in Python packaging, as described in MANIFEST.in commands.

The use of manifest requires installing the optional distlib Python dependency.

The manifest feature is only supported with ansible-galaxy collection build in ansible-core 2.14 or newer, and is mutually exclusive with build_ignore.

For example, to exclude the sensitive folder within the playbooks folder as well as any .tar.gz archives, set the following in your galaxy.yml file:

By default, the MANIFEST.in style directives would exclude all files by default, but there are default directives in place. Those default directives are described below. To see the directives in use during build, pass -vvv with the ansible-galaxy collection build command.

<namespace>-<name>-*.tar.gz is expanded with the actual namespace and name.

The manifest.directives supplied in galaxy.yml are inserted after the default includes and before the default excludes.

To enable the use of manifest directives without supplying your own, insert either manifest: {} or manifest: null in the galaxy.yml file and remove any use of build_ignore.

If the default manifest directives do not meet your needs, you can set manifest.omit_default_directives to a value of true in galaxy.yml. You then must specify a full compliment of manifest directives in galaxy.yml. The defaults documented above are a good starting point.

Below is an example where the default directives are not included.

You can include a GnuPG signature with your collection on a Pulp 3 Galaxy server. See Enabling collection signing for details.

You can manually generate detached signatures for a collection using the gpg CLI using the following step. This step assume you have generated a GPG private key, but do not cover this process.

Each time you publish your collection, you must create a new version on the distribution server. After you publish a version of a collection, you cannot delete or modify that version. To avoid unnecessary extra versions, check your collection for bugs, typos, and other issues locally before publishing:

Install the collection locally.

Review the locally installed collection before publishing a new version.

You have two options for installing your collection locally:

Install your collection locally from the tarball.

Install your collection locally from your Git repository.

To install your collection locally from the tarball, run ansible-galaxy collection install and specify the collection tarball. You can optionally specify a location using the -p flag. For example:

Install the tarball into a directory configured in COLLECTIONS_PATHS so Ansible can easily find and load the collection. If you do not specify a path value, ansible-galaxy collection install installs the collection in the first path defined in COLLECTIONS_PATHS.

To install your collection locally from a Git repository, specify the repository and the branch you want to install:

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

Review the collection:

Run a playbook that uses the modules and plugins in your collection. Verify that new features and functionality work as expected. For examples and more details see Using collections.

Check the documentation for typos.

Check that the version number of your tarball is higher than the latest published version on the distribution server or servers.

If you find any issues, fix them and rebuild the collection tarball.

The only way to change a collection is to release a new version. The latest version of a collection (by highest version number) is the version displayed everywhere in Galaxy and Automation Hub. Users can still download older versions.

Follow semantic versioning when setting the version for your collection. In summary:

Increment the major version number, x of x.y.z, for an incompatible API change.

Increment the minor version number, y of x.y.z, for new functionality in a backwards compatible manner (for example new modules/plugins, parameters, return values).

Increment the patch version number, z of x.y.z, for backwards compatible bug fixes.

Read the official Semantic Versioning documentation for details and examples.

The last step in distributing your collection is publishing the tarball to Ansible Galaxy, Red Hat Automation Hub, or a privately hosted Automation Hub instance. You can publish your collection in two ways:

from the command line using the ansible-galaxy collection publish command

from the website of the distribution server (Galaxy, Automation Hub) itself

To upload the collection tarball from the command line using ansible-galaxy:

This ansible-galaxy command assumes you have retrieved and stored your API token in configuration. See Specifying your API token and distribution server for details.

The ansible-galaxy collection publish command triggers an import process, just as if you uploaded the collection through the Galaxy website. The command waits until the import process completes before reporting the status back. If you want to continue without waiting for the import result, use the --no-wait argument and manually look at the import progress in your My Imports page.

See the Galaxy documentation to learn how to publish your collection directly on the Galaxy website.

Learn how to install and use collections.

Table of fields used in the galaxy.yml file

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
[galaxy]
server_list = release_galaxy

[galaxy_server.release_galaxy]
url=https://galaxy.ansible.com/
token=abcdefghijklmnopqrtuvwxyz
```

Example 2 (unknown):
```unknown
ansible-galaxy collection publish path/to/my_namespace-my_collection-1.0.0.tar.gz --token abcdefghijklmnopqrtuvwxyz
```

Example 3 (unknown):
```unknown
collection_dir#> ansible-galaxy collection build
```

Example 4 (unknown):
```unknown
my_collection/
├── galaxy.yml
├── ...
├── my_namespace-my_collection-1.0.0.tar.gz
└── ...
```

---

## Handlers: running operations on change — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_handlers.html

**Contents:**
- Handlers: running operations on change
- Handler example
- Notifying handlers
- Notifying and loops
- Naming handlers
- Handler insertion order into the play
- Controlling when handlers run
- Defining when tasks change
- Using variables with handlers
- Handlers in roles

Sometimes you want a task to run only when a change is made on a machine. For example, you may want to restart a service if a task updates the configuration of that service, but not if the configuration is unchanged. Ansible uses handlers to address this use case. Handlers are tasks that only run when notified.

Handler insertion order into the play

Controlling when handlers run

Defining when tasks change

Using variables with handlers

Includes and imports in handlers

Meta tasks as handlers

This playbook, verify-apache.yml, contains a single play with a handler.

In this example playbook, the Apache server is restarted by the handler after all tasks are completed in the play.

Tasks can instruct one or more handlers to execute using the notify keyword. The notify keyword can be applied to a task and accepts a list of handler names that are notified on a task change. Alternatively, a string containing a single handler name can be supplied as well. The following example demonstrates how multiple handlers can be notified by a single task:

In the above example, the handlers are executed on task change in the following order: Restart memcached, Restart apache. Handlers are executed in the order they are defined in the handlers section, not in the order listed in the notify statement. Notifying the same handler multiple times will result in executing the handler only once regardless of how many tasks notify it. For example, if multiple tasks update a configuration file and notify a handler to restart Apache, Ansible only bounces Apache once to avoid unnecessary restarts.

Tasks can use loops to notify handlers. This is particularly useful when combined with variables to trigger multiple dynamic notifications.

Note that the handlers are triggered if the task as a whole is changed. When a loop is used the changed state is set if any of the loop items are changed. That is, any change triggers all of the handlers.

In the above example both memcached and apache will be restarted if either template file is changed, neither will be restarted if no file changes.

Handlers must be named in order for tasks to be able to notify them using the notify keyword.

Alternatively, handlers can utilize the listen keyword. Using this handler keyword, handlers can listen on topics that can group multiple handlers as follows:

Notifying the restart web services topic results in executing all handlers listening to that topic regardless of how those handlers are named.

This use makes it much easier to trigger multiple handlers. It also decouples handlers from their names, making it easier to share handlers among playbooks and roles (especially when using third-party roles from a shared source such as Ansible Galaxy).

Each handler should have a globally unique name. If multiple handlers are defined with the same name, only the last one loaded into the play (see handlers_insertion_order) can be notified and executed, effectively shadowing all of the previous handlers with the same name.

There is only one global, play-level scope for handlers regardless of where the handlers are defined, either in the handlers: section or in roles. The order in which handlers are added into the play is as follows:

Handlers from roles in the roles: section.

Handlers from the handlers: section.

Handlers from roles statically imported via import_role tasks.

Handlers from roles dynamically included via include_role tasks (available at runtime only after the include_role task executed).

In case handlers having the same name the last one loaded into the play, as per the above order, can be notified and executed.

By default, handlers run after all the tasks in a particular play have been completed. Notified handlers are executed automatically after each of the following sections, in the following order: pre_tasks, roles/tasks and post_tasks. This approach is efficient, because the handler only runs once, regardless of how many tasks notify it. For example, if multiple tasks update a configuration file and notify a handler to restart Apache, Ansible only bounces Apache once to avoid unnecessary restarts.

If you need handlers to run before the end of the play, add a task to flush them using the meta module, which executes Ansible actions:

The meta: flush_handlers task triggers any handlers that have been notified at that point in the play.

Once handlers are executed, either automatically after each mentioned section or manually by the flush_handlers meta task, they can be notified and run again in later sections of the play.

You can control when handlers are notified about task changes using the changed_when keyword.

In the following example, the handler restarts the service each time the configuration file is copied:

See Defining “changed” for more about changed_when.

You may want your Ansible handlers to use variables. For example, if the name of a service varies slightly by distribution, you want your output to show the exact name of the restarted service for each target machine. Avoid placing variables in the name of the handler. Since handler names are templated early on, Ansible may not have a value available for a handler name like this:

If the variable used in the handler name is not available, the entire play fails. Changing that variable mid-play will not result in newly created handler.

Instead, place variables in the task parameters of your handler. You can load the values using include_vars like this:

While handler names can contain a template, listen topics cannot.

Handlers from roles are not just contained in their roles but rather inserted into the global scope with all other handlers from a play. As such they can be used outside of the role they are defined in. It also means that their name can conflict with handlers from outside the role. To ensure that a handler from a role is notified as opposed to one from outside the role with the same name, notify the handler by using its name in the following form: role_name : handler_name.

Handlers notified within the roles section are automatically flushed at the end of the tasks section.

Notifying a dynamic include such as include_task as a handler results in executing all tasks from within the include. It is not possible to notify a handler defined inside a dynamic include.

Having a static include such as import_task as a handler results in that handler being effectively rewritten by handlers from within that import before the play execution. A static include itself cannot be notified; the tasks from within that include, on the other hand, can be notified individually.

Since Ansible 2.14 meta tasks are allowed to be used and notified as handlers. Note that however flush_handlers cannot be used as a handler to prevent unexpected behavior.

A handler cannot run import_role nor include_role. Handlers ignore tags.

**Examples:**

Example 1 (unknown):
```unknown
---
- name: Verify apache installation
  hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
    - name: Ensure apache is at the latest version
      ansible.builtin.yum:
        name: httpd
        state: latest

    - name: Write the apache config file
      ansible.builtin.template:
        src: /srv/httpd.j2
        dest: /etc/httpd.conf
      notify:
        - Restart apache

    - name: Ensure apache is running
      ansible.builtin.service:
        name: httpd
        state: started

  handlers:
    - name: Restart apache
      ansible.builtin.service:
        name: httpd
        state: restarted
```

Example 2 (unknown):
```unknown
tasks:
- name: Template configuration file
  ansible.builtin.template:
    src: template.j2
    dest: /etc/foo.conf
  notify:
    - Restart apache
    - Restart memcached

handlers:
  - name: Restart memcached
    ansible.builtin.service:
      name: memcached
      state: restarted

  - name: Restart apache
    ansible.builtin.service:
      name: apache
      state: restarted
```

Example 3 (unknown):
```unknown
tasks:
- name: Template services
  ansible.builtin.template:
    src: "{{ item }}.j2"
    dest: /etc/systemd/system/{{ item }}.service
  # Note: if *any* loop iteration triggers a change, *all* handlers are run
  notify: Restart {{ item }}
  loop:
    - memcached
    - apache

handlers:
  - name: Restart memcached
    ansible.builtin.service:
      name: memcached
      state: restarted

  - name: Restart apache
    ansible.builtin.service:
      name: apache
      state: restarted
```

Example 4 (unknown):
```unknown
tasks:
  - name: Restart everything
    command: echo "this task will restart the web services"
    notify: "restart web services"

handlers:
  - name: Restart memcached
    service:
      name: memcached
      state: restarted
    listen: "restart web services"

  - name: Restart apache
    service:
      name: apache
      state: restarted
    listen: "restart web services"
```

---

## The undef function: add hint for undefined variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_templating_undef.html

**Contents:**
- The undef function: add hint for undefined variables

The Jinja2 undef() function returns a Python AnsibleUndefined object, derived from jinja2.StrictUndefined. Use undef() to undefine variables of lesser precedence. For example, a host variable can be overridden for a block of tasks:

The undef function accepts one optional argument:

Give a custom hint about the undefined variable if DEFAULT_UNDEFINED_VAR_BEHAVIOR is configured to give an error.

**Examples:**

Example 1 (unknown):
```unknown
---
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ns.col.auth: "{{ vaulted_credentials | default({}) }}"
  tasks:
    - ns.col.module1:
    - ns.col.module2:

    - name: override host variable
      vars:
        vaulted_credentials: "{{ undef() }}"
      block:
        - ns.col.module1:
```

---

## Roles — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_reuse_roles.html

**Contents:**
- Roles
- Role directory structure
- Storing and finding roles
- Using roles
  - Using roles at the play level
  - Including roles: dynamic reuse
  - Importing roles: static reuse
- Role argument validation
  - Specification format
  - Sample specification

Roles let you automatically load related vars, files, tasks, handlers, and other Ansible artifacts based on a known file structure. After you group your content into roles, you can easily reuse them and share them with other users.

Role directory structure

Storing and finding roles

Using roles at the play level

Including roles: dynamic reuse

Importing roles: static reuse

Role argument validation

Running a role multiple times in one play

Passing different parameters

Using allow_duplicates: true

Using role dependencies

Running role dependencies multiple times in one play

Embedding modules and plugins in roles

Sharing roles: Ansible Galaxy

An Ansible role has a defined directory structure with seven main standard directories. You must include at least one of these directories in each role. You can omit any directories the role does not use. For example:

By default, Ansible will look in most role directories for a main.yml file for relevant content (also main.yaml and main):

tasks/main.yml - A list of tasks that the role provides to the play for execution.

handlers/main.yml - handlers that are imported into the parent play for use by the role or other roles and tasks in the play.

defaults/main.yml - very low precedence values for variables provided by the role (see Using variables for more information). A role’s own defaults will take priority over other role’s defaults, but any/all other variable sources will override this.

vars/main.yml - high precedence variables provided by the role to the play (see Using variables for more information).

files/stuff.txt - one or more files that are available for the role and it’s children.

templates/something.j2 - templates to use in the role or child roles.

meta/main.yml - metadata for the role, including role dependencies and optional Galaxy metadata such as platforms supported. This is required for uploading into galaxy as a standalone role, but not for using the role in your play.

None of the files above are required for a role. For example, you can just provide files/something.txt or vars/for_import.yml and it will still be a valid role.

On stand alone roles you can also include custom modules and/or plugins, for example library/my_module.py, which may be used within this role (see Embedding modules and plugins in roles for more information).

A ‘stand alone’ role refers to role that is not part of a collection but as individually installable content.

Variables from vars/ and defaults/ are imported into play scope unless you disable it via the public option in import_role/include_role.

You can add other YAML files in some directories, but they won’t be used by default. They can be included/imported directly or specified when using include_role/import_role. For example, you can place platform-specific tasks in separate files and refer to them in the tasks/main.yml file:

Or call those tasks directly when loading the role, which bypasses the main.yml files:

Directories defaults and vars may also include nested directories. If your variables file is a directory, Ansible reads all variables files and directories inside in alphabetical order. If a nested directory contains variables files as well as directories, Ansible reads the directories first. Below is an example of a vars/main directory:

By default, Ansible looks for roles in the following locations:

in collections, if you are using them

in a directory called roles/, relative to the playbook file

in the configured roles_path. The default search path is ~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles.

in the directory where the playbook file is located

If you store your roles in a different location, set the roles_path configuration option so Ansible can find your roles. Checking shared roles into a single location makes them easier to use in multiple playbooks. See Configuring Ansible for details about managing settings in ansible.cfg.

Alternatively, you can call a role with a fully qualified path:

You can use roles in the following ways:

at the play level with the roles option: This is the classic way of using roles in a play.

at the tasks level with include_role: You can reuse roles dynamically anywhere in the tasks section of a play using include_role.

at the tasks level with import_role: You can reuse roles statically anywhere in the tasks section of a play using import_role.

as a dependency of another role (see the dependencies keyword in meta/main.yml in this same page).

The classic (original) way to use roles is with the roles option for a given play:

When you use the roles option at the play level, each role ‘x’ looks for a main.yml (also main.yaml and main) in the following directories:

Any copy, script, template or include tasks (in the role) can reference files in roles/x/{files,templates,tasks}/ (dir depends on task) without having to path them relatively or absolutely.

vars and defaults can also match to a directory of the same name and Ansible will process all the files contained in that directory. See Role directory structure for more details.

If you use include_role/import_role, you can specify a custom file name instead of main. The meta directory is an exception because it does not allow for customization.

When you use the roles option at the play level, Ansible treats the roles as static imports and processes them during playbook parsing. Ansible executes each play in this order:

Any pre_tasks defined in the play.

Any handlers triggered by pre_tasks.

Each role listed in roles:, in the order listed. Any role dependencies defined in the role’s meta/main.yml run first, subject to tag filtering and conditionals. See Using role dependencies for more details.

Any tasks defined in the play.

Any handlers triggered by the roles or tasks.

Any post_tasks defined in the play.

Any handlers triggered by post_tasks.

If using tags with tasks in a role, be sure to also tag your pre_tasks, post_tasks, and role dependencies and pass those along as well, especially if the pre/post tasks and role dependencies are used for monitoring outage window control or load balancing. See Tags for details on adding and using tags.

You can pass other keywords to the roles option:

When you add a tag to the role option, Ansible applies the tag to ALL tasks within the role.

Prior to ansible-core 2.15, vars: within the roles: section of a playbook are added to the play variables, making them available to all tasks within the play before and after the role. This behavior can be changed by DEFAULT_PRIVATE_ROLE_VARS. On more recent versions, vars: do not leak into the play’s variable scope.

You can reuse roles dynamically anywhere in the tasks section of a play using include_role. While roles added in a roles section run before any other tasks in a play, included roles run in the order they are defined. If there are other tasks before an include_role task, the other tasks will run first.

You can pass other keywords, including variables and tags, when including roles:

When you add a tag to an include_role task, Ansible applies the tag only to the include itself. This means you can pass --tags to run only selected tasks from the role, if those tasks themselves have the same tag as the include statement. See Selectively running tagged tasks in reusable files for details.

You can conditionally include a role:

You can reuse roles statically anywhere in the tasks section of a play using import_role. The behavior is the same as using the roles keyword. For example:

You can pass other keywords, including variables and tags when importing roles:

When you add a tag to an import_role statement, Ansible applies the tag to all tasks within the role. See Tag inheritance: adding tags to multiple tasks for details.

Beginning with version 2.11, you may choose to enable role argument validation based on an argument specification. This specification is defined in the meta/argument_specs.yml file (or with the .yaml file extension). When this argument specification is defined, a new task is inserted at the beginning of role execution that will validate the parameters supplied for the role against the specification. If the parameters fail validation, the role will fail execution.

Ansible also supports role specifications defined in the role meta/main.yml file, as well. However, any role that defines the specs within this file will not work on versions below 2.11. For this reason, we recommend using the meta/argument_specs.yml file to maintain backward compatibility.

When role argument validation is used on a role that has defined dependencies, then validation on those dependencies will run before the dependent role, even if argument validation fails for the dependent role.

Ansible tags the inserted role argument validation task with always. If the role is statically imported this task runs unless you use the --skip-tags flag.

The role argument specification must be defined in a top-level argument_specs block within the role meta/argument_specs.yml file. All fields are lowercase.

The name of the role entry point.

This should be main in the case of an unspecified entry point.

This will be the base name of the tasks file to execute, with no .yml or .yaml file extension.

A short, one-line description of the entry point. Ideally, it is a phrase and not a sentence.

The short_description is displayed by ansible-doc -t role -l.

It also becomes part of the title for the role page in the documentation.

The short description should always be a string and never a list, and should not end in a period.

You can use Ansible markup in this field.

A longer description that may contain multiple lines.

element is a new paragraph.

You can use Ansible markup in this field.

The version of the role when the entrypoint was added.

This is a string, and not a float, for example, version_added: '2.1'.

In collections, this must be the collection version the entrypoint was added to. For example, version_added: 1.0.0.

Name of the entry point authors.

This can be a single string or a list of strings. Use one list entry per author. If there is only a single author, use a string or a one-element list.

Options are often called “parameters” or “arguments”. This section defines those options.

For each role option (argument), you may include:

The name of the option/argument.

Detailed explanation of what this option does. It should be written in full sentences.

This can be a single string or a list of strings. In case this is a list of strings, every list element is a new paragraph.

You can use Ansible markup in this field.

Only needed if this option was added after the initial role/entry point release. In other words, this is greater than the top level version_added field.

This is a string, and not a float, for example, version_added: '2.1'.

In collections, this must be the collection version the option was added to. For example, version_added: 1.0.0.

The data type of the option. See Argument spec for allowed values for type. The default is str.

If an option is of type list, elements should be specified.

If missing, the option is not required.

If required is false/missing, default may be specified (assumed null if missing).

Ensure that the default value in the docs matches the default value in the code. The actual default for the role variable will always come from the role defaults (as defined in Role directory structure).

The default field must not be listed as part of the description unless it requires additional information or conditions.

If the option is a boolean value, you should use true/false if you want to be compatible with ansible-lint.

List of option values.

Should be absent if empty.

Specifies the data type for list elements when the type is list.

If this option takes a dict or list of dicts, you can define the structure here.

Ansible only executes each role once in a play, even if you define it multiple times unless the parameters defined on the role are different for each definition. For example, Ansible only runs the role foo once in a play like this:

You have two options to force Ansible to run a role more than once.

If you pass different parameters in each role definition, Ansible runs the role more than once. Providing different variable values is not the same as passing different role parameters. You must use the roles keyword for this behavior, since import_role and include_role do not accept role parameters.

This play runs the foo role twice:

This syntax also runs the foo role twice;

In these examples, Ansible runs foo twice because each role definition has different parameters.

Add allow_duplicates: true to the meta/main.yml file for the role:

In this example, Ansible runs foo twice because we have explicitly enabled it to do so.

Role dependencies let you automatically pull in other roles when using a role.

Role dependencies are prerequisites, not true dependencies. The roles do not have a parent/child relationship. Ansible loads all listed roles, runs the roles listed under dependencies first, then runs the role that lists them. The play object is the parent of all roles, including roles called by a dependencies list.

Role dependencies are stored in the meta/main.yml file within the role directory. This file should contain a list of roles and parameters to insert before the specified role. For example:

Ansible always executes roles listed in dependencies before the role that lists them. Ansible executes this pattern recursively when you use the roles keyword. For example, if you list role foo under roles:, role foo lists role bar under dependencies in its meta/main.yml file, and role bar lists role baz under dependencies in its meta/main.yml, Ansible executes baz, then bar, then foo.

Ansible treats duplicate role dependencies like duplicate roles listed under roles:: Ansible only executes role dependencies once, even if defined multiple times, unless the parameters, tags, or when clause defined on the role are different for each definition. If two roles in a play both list a third role as a dependency, Ansible only runs that role dependency once, unless you pass different parameters, tags, when clause, or use allow_duplicates: true in the role you want to run multiple times. See Galaxy role dependencies for more details.

Role deduplication does not consult the invocation signature of parent roles. Additionally, when using vars: instead of role params, there is a side effect of changing variable scoping. Using vars: results in those variables being scoped at the play level. In the below example, using vars: would cause n to be defined as 4 throughout the entire play, including roles called before it.

In addition to the above, users should be aware that role de-duplication occurs before variable evaluation. This means that Lazy Evaluation may make seemingly different role invocations equivalently the same, preventing the role from running more than once.

For example, a role named car depends on a role named wheel as follows:

And the wheel role depends on two roles: tire and brake. The meta/main.yml for wheel would then contain the following:

And the meta/main.yml for tire and brake would contain the following:

The resulting order of execution would be as follows:

To use allow_duplicates: true with role dependencies, you must specify it for the role listed under dependencies, not for the role that lists it. In the example above, allow_duplicates: true appears in the meta/main.yml of the tire and brake roles. The wheel role does not require allow_duplicates: true, because each instance defined by car uses different parameter values.

See Using variables for details on how Ansible chooses among variable values defined in different places (variable inheritance and scope). Also, deduplication happens ONLY at the play level, so multiple plays in the same playbook may rerun the roles.

This applies only to standalone roles. Roles in collections do not support plugin embedding; they must use the collection’s plugins structure to distribute plugins.

If you write a custom module (see Should you develop a module?) or a plugin (see Developing plugins), you might wish to distribute it as part of a role. For example, if you write a module that helps configure your company’s internal software, and you want other people in your organization to use this module, but do not want to tell everyone how to configure their Ansible library path, you can include the module in your internal_config role.

To add a module or a plugin to a role: Alongside the ‘tasks’ and ‘handlers’ structure of a role, add a directory named ‘library’ and then include the module directly inside the ‘library’ directory.

Assuming you had this:

The module will be usable in the role itself, as well as any roles that are called after this role, as follows:

If necessary, you can also embed a module in a role to modify a module in Ansible’s core distribution. For example, you can use the development version of a particular module before it is released in production releases by copying the module and embedding the copy in a role. Use this approach with caution, as API signatures may change in core components, and this workaround is not guaranteed to work.

The same mechanism can be used to embed and distribute plugins in a role, using the same schema. For example, for a filter plugin:

These filters can then be used in a Jinja template in any role called after ‘my_custom_filter’.

Ansible Galaxy is a free site for finding, downloading, rating, and reviewing all kinds of community-developed Ansible roles and can be a great way to get a jumpstart on your automation projects.

The client ansible-galaxy is included in Ansible. The Galaxy client allows you to download roles from Ansible Galaxy and provides an excellent default framework for creating your own roles.

Read the Ansible Galaxy documentation page for more information.

How to create new roles, share roles on Galaxy, role management

Learn about YAML syntax

Review the basic Playbook language features

Tips and tricks for playbooks

Variables in playbooks

Conditionals in playbooks

Using tags to select or skip roles/tasks in long playbooks

Browse existing collections, modules, and plugins

Extending Ansible by writing your own modules

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
# playbooks
site.yml
webservers.yml
fooservers.yml
```

Example 2 (unknown):
```unknown
roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies
        library/          # roles can also include custom modules
        module_utils/     # roles can also include custom module_utils
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""
```

Example 3 (unknown):
```unknown
# roles/example/tasks/main.yml
- name: Install the correct web server for RHEL
  import_tasks: redhat.yml
  when: ansible_facts['os_family']|lower == 'redhat'

- name: Install the correct web server for Debian
  import_tasks: debian.yml
  when: ansible_facts['os_family']|lower == 'debian'

# roles/example/tasks/redhat.yml
- name: Install web server
  ansible.builtin.yum:
    name: "httpd"
    state: present

# roles/example/tasks/debian.yml
- name: Install web server
  ansible.builtin.apt:
    name: "apache2"
    state: present
```

Example 4 (unknown):
```unknown
- name: include apt tasks
  include_role:
      name: package_manager_bootstrap
      tasks_from: apt.yml
  when: ansible_facts['os_family'] == 'Debian'
```

---

## Playbook Keywords — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/playbooks_keywords.html

**Contents:**
- Playbook Keywords
- Play
- Role
- Block
- Task

These are the keywords available on common playbook objects. Keywords are one of several sources for configuring Ansible behavior. See Controlling how Ansible behaves: precedence rules for details on the relative precedence of each source.

Aliases for the directives are not reflected here, nor are mutable ones. For example, action in task can be substituted by the name of any Ansible module.

The keywords do not have version_added information at this time

Some keywords set defaults for the objects inside of them rather than for the objects themselves

Force any un-handled task errors on any host to propagate to all hosts and end the play.

Boolean that controls if privilege escalation is used or not on Task execution. Implemented by the become plugin. See Become plugins.

Path to the executable used to elevate privileges. Implemented by the become plugin. See Become plugins.

A string of flag(s) to pass to the privilege escalation program when become is True.

Which method of privilege escalation to use (such as sudo or su).

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

A boolean that controls if a task is run normally or avoids changes to the target and tries to report what it would have done (check mode/dry run). See Validating tasks: check mode and diff mode.

List of collection namespaces to search for modules, plugins, and roles. See Using collections in a playbook

Tasks within a role do not inherit the value of collections from the play. To have a role search a list of collections, use the collections keyword in meta/main.yml within a role.

Allows you to change the connection plugin used for tasks to execute on the target. See Using connection plugins.

Enable debugging tasks based on the state of the task result. See Debugging tasks.

Toggle to make tasks return ‘diff’ information or not.

A dictionary that gets converted into environment vars to be provided for the task upon execution. This can ONLY be used with modules. This is not supported for any other type of plugins nor Ansible itself nor its configuration, it just sets the variables for the code responsible for executing the task. This is not a recommended way to pass in confidential data.

Set the fact path option for the fact gathering plugin controlled by gather_facts.

Will force notified handler execution for hosts even if they failed during the play. Will not trigger if the play itself fails.

A boolean that controls if the play will automatically run the ‘setup’ task to gather facts for the hosts.

Allows you to pass subset options to the fact gathering plugin controlled by gather_facts.

Allows you to set the timeout for the fact gathering plugin controlled by gather_facts.

A section with tasks that are treated as handlers, these won’t get executed normally, only when notified after each section of tasks is complete. A handler’s listen field is not templatable.

A list of groups, hosts or host pattern that translates into a list of hosts that are the play’s target.

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

Boolean that allows you to ignore task failures due to an unreachable host and continue with the play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

can be used to abort the run after a given percentage of hosts in the current batch has failed. This only works on linear or linear-derived strategies.

Specifies default parameter values for modules.

Identifier. Can be used for documentation, or in tasks/handlers.

Boolean that controls information disclosure.

Controls the sorting of hosts as they are used for executing the play. Possible values are inventory (default), sorted, reverse_sorted, reverse_inventory and shuffle.

Used to override the default port used in a connection.

A list of tasks to execute after the tasks section.

A list of tasks to execute before roles.

User used to log into the target via the connection plugin.

List of roles to be imported into the play

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterward apply any results and facts to all active hosts in the same batch.

Explicitly define how Ansible batches the execution of the current play on the play’s target. See Setting the batch size with serial.

Allows you to choose the strategy plugin to use for the play. See Strategy plugins.

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

Main list of tasks to execute in the play, they run after roles and before post_tasks.

Limit the number of concurrent task runs on task, block and playbook level. This is independent of the forks and serial settings, but cannot be set higher than those limits. For example, if forks is set to 10 and the throttle is set to 15, at most 10 hosts will be operated on in parallel.

Time limit for the task action to execute in, if exceeded, Ansible will interrupt the process. Timeout does not include templating or looping.

Dictionary/map of variables

List of files that contain vars to include in the play.

list of variables to prompt for.

Force any un-handled task errors on any host to propagate to all hosts and end the play.

Boolean that controls if privilege escalation is used or not on Task execution. Implemented by the become plugin. See Become plugins.

Path to the executable used to elevate privileges. Implemented by the become plugin. See Become plugins.

A string of flag(s) to pass to the privilege escalation program when become is True.

Which method of privilege escalation to use (such as sudo or su).

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

A boolean that controls if a task is run normally or avoids changes to the target and tries to report what it would have done (check mode/dry run). See Validating tasks: check mode and diff mode.

List of collection namespaces to search for modules, plugins, and roles. See Using collections in a playbook

Tasks within a role do not inherit the value of collections from the play. To have a role search a list of collections, use the collections keyword in meta/main.yml within a role.

Allows you to change the connection plugin used for tasks to execute on the target. See Using connection plugins.

Enable debugging tasks based on the state of the task result. See Debugging tasks.

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

Toggle to make tasks return ‘diff’ information or not.

A dictionary that gets converted into environment vars to be provided for the task upon execution. This can ONLY be used with modules. This is not supported for any other type of plugins nor Ansible itself nor its configuration, it just sets the variables for the code responsible for executing the task. This is not a recommended way to pass in confidential data.

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

Boolean that allows you to ignore task failures due to an unreachable host and continue with the play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

Specifies default parameter values for modules.

Identifier. Can be used for documentation, or in tasks/handlers.

Boolean that controls information disclosure.

Used to override the default port used in a connection.

User used to log into the target via the connection plugin.

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterward apply any results and facts to all active hosts in the same batch.

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

Limit the number of concurrent task runs on task, block and playbook level. This is independent of the forks and serial settings, but cannot be set higher than those limits. For example, if forks is set to 10 and the throttle is set to 15, at most 10 hosts will be operated on in parallel.

Time limit for the task action to execute in, if exceeded, Ansible will interrupt the process. Timeout does not include templating or looping.

Dictionary/map of variables

Conditional expression, determines if an iteration of a task is run or not.

List of tasks, in a block, that execute no matter if there is an error in the block or not.

Force any un-handled task errors on any host to propagate to all hosts and end the play.

Boolean that controls if privilege escalation is used or not on Task execution. Implemented by the become plugin. See Become plugins.

Path to the executable used to elevate privileges. Implemented by the become plugin. See Become plugins.

A string of flag(s) to pass to the privilege escalation program when become is True.

Which method of privilege escalation to use (such as sudo or su).

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

List of tasks in a block.

A boolean that controls if a task is run normally or avoids changes to the target and tries to report what it would have done (check mode/dry run). See Validating tasks: check mode and diff mode.

List of collection namespaces to search for modules, plugins, and roles. See Using collections in a playbook

Tasks within a role do not inherit the value of collections from the play. To have a role search a list of collections, use the collections keyword in meta/main.yml within a role.

Allows you to change the connection plugin used for tasks to execute on the target. See Using connection plugins.

Enable debugging tasks based on the state of the task result. See Debugging tasks.

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

Toggle to make tasks return ‘diff’ information or not.

A dictionary that gets converted into environment vars to be provided for the task upon execution. This can ONLY be used with modules. This is not supported for any other type of plugins nor Ansible itself nor its configuration, it just sets the variables for the code responsible for executing the task. This is not a recommended way to pass in confidential data.

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

Boolean that allows you to ignore task failures due to an unreachable host and continue with the play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

Specifies default parameter values for modules.

Identifier. Can be used for documentation, or in tasks/handlers.

Boolean that controls information disclosure.

List of handlers to notify when the task returns a ‘changed=True’ status.

Used to override the default port used in a connection.

User used to log into the target via the connection plugin.

List of tasks in a block that run if there is a task error in the main block list.

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterward apply any results and facts to all active hosts in the same batch.

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

Limit the number of concurrent task runs on task, block and playbook level. This is independent of the forks and serial settings, but cannot be set higher than those limits. For example, if forks is set to 10 and the throttle is set to 15, at most 10 hosts will be operated on in parallel.

Time limit for the task action to execute in, if exceeded, Ansible will interrupt the process. Timeout does not include templating or looping.

Dictionary/map of variables

Conditional expression, determines if an iteration of a task is run or not.

The ‘action’ to execute for a task, it normally translates into a C(module) or action plugin.

Force any un-handled task errors on any host to propagate to all hosts and end the play.

A secondary way to add arguments into a task. Takes a dictionary in which keys map to options and values.

Run a task asynchronously if the C(action) supports this; the value is the maximum runtime in seconds.

Boolean that controls if privilege escalation is used or not on Task execution. Implemented by the become plugin. See Become plugins.

Path to the executable used to elevate privileges. Implemented by the become plugin. See Become plugins.

A string of flag(s) to pass to the privilege escalation program when become is True.

Which method of privilege escalation to use (such as sudo or su).

User that you ‘become’ after using privilege escalation. The remote/login user must have permissions to become this user.

Conditional expression that overrides the task’s normal ‘changed’ status.

A boolean that controls if a task is run normally or avoids changes to the target and tries to report what it would have done (check mode/dry run). See Validating tasks: check mode and diff mode.

List of collection namespaces to search for modules, plugins, and roles. See Using collections in a playbook

Tasks within a role do not inherit the value of collections from the play. To have a role search a list of collections, use the collections keyword in meta/main.yml within a role.

Allows you to change the connection plugin used for tasks to execute on the target. See Using connection plugins.

Enable debugging tasks based on the state of the task result. See Debugging tasks.

Number of seconds to delay between retries. This setting is only used in combination with until.

Boolean that allows you to apply facts to a delegated host instead of inventory_hostname.

Host to execute task instead of the target (inventory_hostname). Connection vars from the delegated host will also be used for the task.

Toggle to make tasks return ‘diff’ information or not.

A dictionary that gets converted into environment vars to be provided for the task upon execution. This can ONLY be used with modules. This is not supported for any other type of plugins nor Ansible itself nor its configuration, it just sets the variables for the code responsible for executing the task. This is not a recommended way to pass in confidential data.

Conditional expression that overrides the task’s normal ‘failed’ status.

Boolean that allows you to ignore task failures and continue with play. It does not affect connection errors.

Boolean that allows you to ignore task failures due to an unreachable host and continue with the play. This does not affect other task errors (see ignore_errors) but is useful for groups of volatile/ephemeral hosts.

Same as action but also implies delegate_to: localhost

Takes a list for the task to iterate over, saving each list element into the item variable (configurable via loop_control)

Several keys here allow you to modify/set loop behavior in a task. See Adding controls to loops.

Specifies default parameter values for modules.

Identifier. Can be used for documentation, or in tasks/handlers.

Boolean that controls information disclosure.

List of handlers to notify when the task returns a ‘changed=True’ status.

Sets the polling interval in seconds for async tasks (default 10s).

Used to override the default port used in a connection.

Name of variable that will contain task status and module return data.

User used to log into the target via the connection plugin.

Number of retries before giving up in a until loop. This setting is only used in combination with until.

Boolean that will bypass the host loop, forcing the task to attempt to execute on the first host available and afterward apply any results and facts to all active hosts in the same batch.

Tags applied to the task or included tasks, this allows selecting subsets of tasks from the command line.

Limit the number of concurrent task runs on task, block and playbook level. This is independent of the forks and serial settings, but cannot be set higher than those limits. For example, if forks is set to 10 and the throttle is set to 15, at most 10 hosts will be operated on in parallel.

Time limit for the task action to execute in, if exceeded, Ansible will interrupt the process. Timeout does not include templating or looping.

This keyword implies a ‘retries loop’ that will go on until the condition supplied here is met or we hit the retries limit.

Dictionary/map of variables

Conditional expression, determines if an iteration of a task is run or not.

The same as loop but magically adds the output of any lookup plugin to generate the item list.

---

## Blocks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_blocks.html

**Contents:**
- Blocks
- Grouping tasks with blocks
- Handling errors with blocks

Blocks create logical groups of tasks. Blocks also offer ways to handle task errors, similar to exception handling in many programming languages.

Grouping tasks with blocks

Handling errors with blocks

All tasks in a block inherit directives applied at the block level. Most of what you can apply to a single task (with the exception of loops) can be applied at the block level, so blocks make it much easier to set data or directives common to the tasks. The directive does not affect the block itself, it is only inherited by the tasks enclosed by a block. For example, a when statement is applied to the tasks within a block, not to the block itself.

In the example above, the ‘when’ condition will be evaluated before Ansible runs each of the three tasks in the block. All three tasks also inherit the privilege escalation directives, running as the root user. Finally, ignore_errors: true ensures that Ansible continues to execute the playbook even if some of the tasks fail.

All tasks in a block, including the ones included through include_role, inherit directives applied at the block level.

Names for blocks have been available since Ansible 2.3. We recommend using names in all tasks, within blocks or elsewhere, for better visibility into the tasks being executed when you run the playbook.

You can control how Ansible responds to task errors using blocks with rescue and always sections.

Errors caused by invalid task definitions and unreachable hosts do not trigger the rescue or always sections of a block.

Rescue blocks specify tasks to run when an earlier task in a block fails. This approach is similar to exception handling in many programming languages. Ansible only runs rescue blocks after a task returns a ‘failed’ state.

You can also add an always section to a block. Tasks in the always section run no matter what the task status of the previous block is.

Together, these elements offer complex error handling.

The tasks in the block execute normally. If any tasks in the block return failed, the rescue section executes tasks to recover from the error. The always section runs regardless of the results of the block and rescue sections.

If an error occurs in the block and the rescue task succeeds, Ansible reverts the failed status of the original task for the run and continues to run the play as if the original task had succeeded. The rescued task is considered successful and does not trigger max_fail_percentage or any_errors_fatal configurations. However, Ansible still reports a failure in the playbook statistics.

You can use blocks with flush_handlers in a rescue task to ensure that all handlers run even if an error occurs:

Ansible provides a couple of variables for tasks in the rescue portion of a block:

The task that returned ‘failed’ and triggered the rescue. For example, to get the name use ansible_failed_task.name.

The captured return result of the failed task that triggered the rescue. This would equate to having used this var in the register keyword.

These can be inspected in the rescue section:

In ansible-core 2.14 or later, both variables are propagated from an inner block to an outer rescue portion of a block when nesting blocks.

An introduction to playbooks

Playbook organization by roles

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
tasks:
   - name: Install, configure, and start Apache
     when: ansible_facts['distribution'] == 'CentOS'
     block:
       - name: Install httpd and memcached
         ansible.builtin.yum:
           name:
           - httpd
           - memcached
           state: present

       - name: Apply the foo config template
         ansible.builtin.template:
           src: templates/src.j2
           dest: /etc/foo.conf

       - name: Start service bar and enable it
         ansible.builtin.service:
           name: bar
           state: started
           enabled: True
     become: true
     become_user: root
     ignore_errors: true
```

Example 2 (unknown):
```unknown
tasks:
   - name: Handle the error
     block:
       - name: Print a message
         ansible.builtin.debug:
           msg: 'I execute normally'

       - name: Force a failure
         ansible.builtin.command: /bin/false

       - name: Never print this
         ansible.builtin.debug:
           msg: 'I never execute, due to the above task failing, :-('
     rescue:
       - name: Print when errors
         ansible.builtin.debug:
           msg: 'I caught an error, can do stuff here to fix it, :-)'
```

Example 3 (unknown):
```unknown
tasks:
   - name: Always do X
     block:
       - name: Print a message
         ansible.builtin.debug:
           msg: 'I execute normally'

       - name: Force a failure
         ansible.builtin.command: /bin/false

       - name: Never print this
         ansible.builtin.debug:
           msg: 'I never execute :-('
     always:
       - name: Always do this
         ansible.builtin.debug:
           msg: "This always executes, :-)"
```

Example 4 (unknown):
```unknown
tasks:
   - name: Attempt and graceful roll back demo
     block:
       - name: Print a message
         ansible.builtin.debug:
           msg: 'I execute normally'

       - name: Force a failure
         ansible.builtin.command: /bin/false

       - name: Never print this
         ansible.builtin.debug:
           msg: 'I never execute, due to the above task failing, :-('
     rescue:
       - name: Print when errors
         ansible.builtin.debug:
           msg: 'I caught an error'

       - name: Force a failure in middle of recovery! >:-)
         ansible.builtin.command: /bin/false

       - name: Never print this
         ansible.builtin.debug:
           msg: 'I also never execute :-('
     always:
       - name: Always do this
         ansible.builtin.debug:
           msg: "This always executes"
```

---

## Setting the remote environment — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_environment.html

**Contents:**
- Setting the remote environment
- Setting the remote environment in a task
- Working with language-specific version managers

You can use the environment keyword at the play, block, or task level to set an environment variable for an action on a remote host. With this keyword, you can enable using a proxy for a task that does http requests, set the required environment variables for language-specific version managers, and more.

When you set a value with environment: at the play or block level, it is available only to tasks within the play or block that are executed by the same user. The environment: keyword does not affect Ansible itself, Ansible configuration settings, the environment for other users, or the execution of other plugins like lookups and filters. Variables set with environment: do not automatically become Ansible facts, even when you set them at the play level. You must include an explicit gather_facts task in your playbook and set the environment keyword on that task to turn these values into Ansible facts.

Setting the remote environment in a task

You can set the environment directly at the task level.

You can reuse environment settings by defining them as variables in your play and accessing them in a task as you would access any stored Ansible variable.

You can store environment settings for reuse in multiple playbooks by defining them in a group_vars file.

You can set the remote environment at the play level.

These examples show proxy settings, but you can provide any number of settings this way.

Some language-specific version managers (such as rbenv and nvm) require you to set environment variables while these tools are in use. When using these tools manually, you usually source some environment variables from a script or lines added to your shell configuration file. In Ansible, you can do this with the environment keyword at the play level.

The example above uses ansible_env as part of the PATH. Basing variables on ansible_env is risky. Ansible populates ansible_env values by gathering facts, so the value of the variables depends on the remote_user or become_user Ansible used when gathering those facts. If you change remote_user/become_user the values in ansible_env may not be the ones you expect.

Environment variables are normally passed in clear text (shell plugin dependent) so they are not a recommended way of passing secrets to the module being executed.

You can also specify the environment at the task level.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- hosts: all
  remote_user: root

  tasks:

    - name: Install cobbler
      ansible.builtin.package:
        name: cobbler
        state: present
      environment:
        http_proxy: http://proxy.example.com:8080
```

Example 2 (unknown):
```unknown
- hosts: all
  remote_user: root

  # create a variable named "proxy_env" that is a dictionary
  vars:
    proxy_env:
      http_proxy: http://proxy.example.com:8080

  tasks:

    - name: Install cobbler
      ansible.builtin.package:
        name: cobbler
        state: present
      environment: "{{ proxy_env }}"
```

Example 3 (unknown):
```unknown
---
# file: group_vars/boston

ntp_server: ntp.bos.example.com
backup: bak.bos.example.com
proxy_env:
  http_proxy: http://proxy.bos.example.com:8080
  https_proxy: http://proxy.bos.example.com:8080
```

Example 4 (unknown):
```unknown
- hosts: testing

  roles:
     - php
     - nginx

  environment:
    http_proxy: http://proxy.example.com:8080
```

---

## Ansible-core 2.17 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.17.html

**Contents:**
- Ansible-core 2.17 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins
- Porting custom scripts

This section discusses the behavioral changes between ansible-core 2.16 and ansible-core 2.17.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.17 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.17 Porting Guide

Noteworthy module changes

Porting custom scripts

Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.16.1, conditional expressions with embedded template blocks can fail with the message “Conditional is marked as unsafe, and cannot be evaluated.” when an embedded template consults data from untrusted sources like module results or vars marked !unsafe. Conditionals with embedded templates can be a source of malicious template injection when referencing untrusted data, and can nearly always be rewritten without embedded templates. Playbook task conditional keywords such as when and until have long displayed warnings discouraging use of embedded templates in conditionals; this warning has been expanded to non-task conditionals as well, such as the assert action.

any_errors_fatal - when a task in a block with a rescue section fails on a host, the rescue section is executed on all hosts. This occurs because any_errors_fatal automatically fails all hosts.

Python 2.7 and Python 3.6 are no longer supported remote versions. Python 3.7+ is now required for target execution.

The following modules no longer exist:

**Examples:**

Example 1 (unknown):
```unknown
- name: task with a module result (always untrusted by Ansible)
  shell: echo "hi mom"
  register: untrusted_result

# don't do it this way...
# - name: insecure conditional with embedded template consulting untrusted data
#   assert:
#     that: '"hi mom" is in {{ untrusted_result.stdout }}'

- name: securely access untrusted values directly as Jinja variables instead
  assert:
    that: '"hi mom" is in untrusted_result.stdout'
```

---

## Ansible playbooks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_intro.html

**Contents:**
- Ansible playbooks
- Playbook syntax
- Playbook execution
  - Task execution
  - Desired state and idempotency
  - Running playbooks
  - Running playbooks in check mode
- Ansible-Pull
- Verifying playbooks
  - ansible-lint

Ansible Playbooks provide a repeatable, reusable, simple configuration management and multimachine deployment system that is well suited to deploying complex applications. If you need to execute a task with Ansible more than once, you can write a playbook and put the playbook under source control. You can then use the playbook to push new configurations or confirm the configuration of remote systems.

Playbooks allow you to perform the following actions:

Declare configurations.

Orchestrate steps of any manual ordered process on multiple sets of machines in a defined order.

Launch tasks synchronously or asynchronously.

Desired state and idempotency

Running playbooks in check mode

You express playbooks in YAML format with a minimum of syntax. If you are not familiar with YAML, review the YAML Syntax overview and consider installing an add-on for your text editor (see Other Tools and Programs) to help you write clean YAML syntax in your playbooks.

A playbook consists of one or more ‘plays’ in an ordered list. The terms ‘playbook’ and ‘play’ are sports analogies. Each play executes part of the overall goal of the playbook, running one or more tasks. Each task calls an Ansible module.

A playbook runs in order from top to bottom. Within each play, tasks also run in order from top to bottom. Playbooks with multiple plays can orchestrate multimachine deployments, running one play on your webservers, another play on your database servers, and a third play on your network infrastructure. At a minimum, each play defines two things:

The managed nodes to target, using a pattern.

At least one task to execute.

For Ansible 2.10 and later, you should use the fully-qualified collection name (FQCN) in your playbooks. Using the FQCN ensures that you have selected the correct module, because multiple collections can contain modules with the same name. For example, user. See Using collections in a playbook.

In the following example, the first play targets the web servers and the second play targets the database servers.

Your playbook can include more than just a hosts line and tasks. For example, the playbook above sets a remote_user for each play. The remote_user is the user account for the SSH connection. You can add other Playbook Keywords at the playbook, play, or task level to influence how Ansible behaves. Playbook keywords can control the connection plugin, whether to use privilege escalation, how to handle errors, and more. To support a variety of environments, you can set many of these parameters as command-line flags in your Ansible configuration, or in your inventory. Learning the precedence rules for these sources of data helps you as you expand your Ansible ecosystem.

By default, Ansible executes each task in order, one at a time, against all machines matched by the host pattern. Each task executes a module with specific arguments. After a task has executed on all target machines, Ansible moves to the next task. You can use strategies to change this default behavior. Within each play, Ansible applies the same task directives to all hosts. If a task fails on a host, Ansible removes that host from the rotation for the rest of the playbook.

When you run a playbook, Ansible returns information about connections, the name lines of all your plays and tasks, whether each task has succeeded or failed on each machine, and whether each task has made a change on each machine. At the bottom of the playbook execution, Ansible provides a summary of the nodes that were targeted and how they performed. General failures and fatal “unreachable” communication attempts are kept separate in the counts.

Most Ansible modules check whether the desired final state has already been achieved and exit without performing any actions if that state has been achieved. Repeating the task does not change the final state. Modules that behave this way are ‘idempotent’. Whether you run a playbook once or multiple times, the outcome should be the same. However, not all playbooks and not all modules behave this way. If you are unsure, test your playbooks in a sandbox environment before running them multiple times in production.

To run your playbook, use the ansible-playbook command.

Use the --verbose flag when running your playbook to see detailed output from successful and unsuccessful tasks.

The Ansible check mode allows you to execute a playbook without applying any alterations to your systems. You can use check mode to test playbooks before you implement them in a production environment.

To run a playbook in check mode, pass the -C or --check flag to the ansible-playbook command:

Executing this command runs the playbook normally. Instead of implementing any modifications, Ansible provides a report on the changes it would have made. This report includes details such as file modifications, command execution, and module calls.

Check mode offers a safe and practical approach to examine the functionality of your playbooks without risking unintended changes to your systems. Check mode is also a valuable tool for troubleshooting playbooks that are not functioning as expected.

You can invert the Ansible architecture so that nodes check in to a central location instead of you pushing configuration out to them.

The ansible-pull command is a small script that checks out a repo of configuration instructions from git and then runs ansible-playbook against that content.

If you load balance your checkout location, ansible-pull scales infinitely.

Run ansible-pull --help for details.

You may want to verify your playbooks to catch syntax errors and other problems before you run them. The ansible-playbook command offers several options for verification, including --check, --diff, --list-hosts, --list-tasks, and --syntax-check. The Tools for validating playbooks topic describes other tools for validating and testing playbooks.

You can use ansible-lint for detailed, Ansible-specific feedback on your playbooks before you execute them. For example, if you run ansible-lint on the playbook called verify-apache.yml near the top of this page, you should get the following results:

The ansible-lint default rules page describes each error.

Learn how to test Ansible Playbooks syntax

Learn about YAML syntax

Tips for managing playbooks in the real world

Browse existing collections, modules, and plugins

Learn to extend Ansible by writing your own modules

Learn about how to select hosts

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
---
- name: Update web servers
  hosts: webservers
  remote_user: root

  tasks:
  - name: Ensure apache is at the latest version
    ansible.builtin.yum:
      name: httpd
      state: latest

  - name: Write the apache config file
    ansible.builtin.template:
      src: /srv/httpd.j2
      dest: /etc/httpd.conf

- name: Update db servers
  hosts: databases
  remote_user: root

  tasks:
  - name: Ensure postgresql is at the latest version
    ansible.builtin.yum:
      name: postgresql
      state: latest

  - name: Ensure that postgresql is started
    ansible.builtin.service:
      name: postgresql
      state: started
```

Example 2 (unknown):
```unknown
ansible-playbook playbook.yml -f 10
```

Example 3 (unknown):
```unknown
ansible-playbook --check playbook.yaml
```

Example 4 (unknown):
```unknown
$ ansible-lint verify-apache.yml
[403] Package installs should not use latest
verify-apache.yml:8
Task/Handler: ensure apache is at the latest version
```

---

## Conditionals — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_conditionals.html

**Contents:**
- Conditionals
- Basic conditionals with when
  - Conditionals based on ansible_facts
  - Conditions based on registered variables
  - Conditionals based on variables
  - Using conditionals in loops
  - Loading custom facts
  - Conditionals with reuse
    - Conditionals with imports
    - Conditionals with includes

In a playbook, you may want to execute different tasks or have different goals, depending on the value of a fact (data about the remote system), a variable, or the result of a previous task. You may want the value of some variables to depend on the value of other variables. Or you may want to create additional groups of hosts based on whether the hosts match other criteria. You can do all of these things with conditionals.

Ansible uses Jinja2 tests and filters in conditionals. Ansible supports all the standard tests and filters and adds some unique ones as well.

There are many options to control execution flow in Ansible. You can find more examples of supported conditionals at https://jinja.palletsprojects.com/en/latest/templates/#comparisons.

Basic conditionals with when

Conditionals based on ansible_facts

Conditions based on registered variables

Conditionals based on variables

Using conditionals in loops

Conditionals with reuse

Conditionals with imports

Conditionals with includes

Conditionals with roles

Selecting variables, files, or templates based on facts

Selecting variables files based on facts

Selecting files and templates based on facts

Debugging conditionals

ansible_facts[‘distribution’]

ansible_facts[‘distribution_major_version’]

ansible_facts[‘os_family’]

The simplest conditional statement applies to a single task. Create the task, then add a when statement that applies a test. The when clause is a raw Jinja2 expression without double curly braces (see Referencing simple variables). When you run the task or playbook, Ansible evaluates the test for all hosts. On any host where the test passes (returns a value of True), Ansible runs that task. For example, if you are installing mysql on multiple machines, some of which have SELinux enabled, you might have a task to configure SELinux to allow mysql to run. You would only want that task to run on machines that have SELinux enabled:

Often you want to execute or skip a task based on facts. Facts are attributes of individual hosts, including IP address, operating system, the status of a filesystem, and many more. With conditionals based on facts:

You can install a certain package only when the operating system is a particular version.

You can skip configuring a firewall on hosts with internal IP addresses.

You can perform cleanup tasks only when a filesystem is getting full.

See Commonly-used facts for a list of facts that frequently appear in conditional statements. Not all facts exist for all hosts. For example, the ‘lsb_major_release’ fact used in the example below only exists when the lsb_release package is installed on the target host. To see what facts are available on your systems, add a debug task to your playbook:

Here is a sample conditional based on a fact:

If you have multiple conditions, you can group them with parentheses:

You can use logical operators to combine conditions. When you have multiple conditions that all need to be true (that is, a logical and), you can specify them as a list:

If a fact or variable is a string, and you need to run a mathematical comparison on it, use a filter to ensure that Ansible reads the value as an integer:

You can store Ansible facts as variables to use for conditional logic, as in the following example:

Often in a playbook, you want to execute or skip a task based on the outcome of an earlier task. For example, you might want to configure a service after it is upgraded by an earlier task. To create a conditional based on a registered variable:

Register the outcome of the earlier task as a variable.

Create a conditional test based on the registered variable.

You create the name of the registered variable using the register keyword. A registered variable always contains the status of the task that created it as well as any output that the task generated. You can use registered variables in templates and action lines as well as in conditional when statements. You can access the string contents of the registered variable using variable.stdout. For example:

You can use registered results in the loop of a task if the variable is a list. If the variable is not a list, you can convert it into a list, with either stdout_lines or with variable.stdout.split(). You can also split the lines by other fields:

The string content of a registered variable can be empty. If you want to run another task only on hosts where the stdout of your registered variable is empty, check the registered variable’s string contents for emptiness:

Ansible always registers something in a registered variable for every host, even on hosts where a task fails or Ansible skips a task because a condition is not met. To run a follow-up task on these hosts, query the registered variable for is skipped (not for “undefined” or “default”). See Registering variables for more information. Here are sample conditionals based on the success or failure of a task. Remember to ignore errors if you want Ansible to continue executing on a host when a failure occurs:

Older versions of Ansible used success and fail, but succeeded and failed use the correct tense. All of these options are now valid.

You can also create conditionals based on variables defined in the playbooks or inventory. Because conditionals require boolean input (a test must evaluate as True to trigger the condition), you must apply the | bool filter to non-boolean variables, such as string variables with content like ‘yes’, ‘on’, ‘1’, or ‘true’. You can define variables like this:

With the variables above, Ansible would run one of these tasks and skip the other:

If a required variable has not been set, you can skip or fail using Jinja2’s defined test. For example:

This is especially useful in combination with the conditional import of vars files (see below). As the examples show, you do not need to use {{ }} to use variables inside conditionals, as these are already implied.

If you combine a when statement with a loop, Ansible processes the condition separately for each item. This is by design, so you can execute the task on some items in the loop and skip it on other items. For example:

If you need to skip the whole task when the loop variable is undefined, use the |default filter to provide an empty iterator. For example, when looping over a list:

You can do the same thing when looping over a dict:

You can provide your own facts, as described in Should you develop a module?. To run them, just make a call to your own custom fact gathering module at the top of your list of tasks, and the variables returned there will be accessible for future tasks:

You can use conditionals with reusable tasks files, playbooks, or roles. Ansible executes these conditional statements differently for dynamic reuse (includes) and static reuse (imports). See Reusing Ansible artifacts for more information on reuse in Ansible.

When you add a conditional to an import statement, Ansible applies the condition to all tasks within the imported file. This behavior is the equivalent of Tag inheritance: adding tags to multiple tasks. Ansible applies the condition to every task and evaluates each task separately. For example, if you want to define and then display a variable that was not previously defined, you might have a playbook called main.yml and a tasks file called other_tasks.yml:

Ansible expands this at execution time to the equivalent of:

If x is initially defined, both tasks are skipped as intended. But if x is initially undefined, the debug task will be skipped since the conditional is evaluated for every imported task. The conditional will evaluate to true for the set_fact task, which will define the variable and cause the debug conditional to evaluate to false.

If this is not the behavior you want, use an include_* statement to apply a condition only to that statement itself.

Now if x is initially undefined, the debug task will not be skipped because the conditional is evaluated at the time of the include and does not apply to the individual tasks.

You can apply conditions to import_playbook as well as to the other import_* statements. When you use this approach, Ansible returns a ‘skipped’ message for every task on every host that does not match the criteria, creating repetitive output. In many cases the group_by module can be a more streamlined way to accomplish the same objective; see Handling OS and distro differences.

When you use a conditional on an include_* statement, the condition is applied only to the include task itself and not to any other tasks within the included file(s). To contrast with the example used for conditionals on imports above, look at the same playbook and tasks file, but using an include instead of an import:

Ansible expands this at execution time to the equivalent of:

By using include_tasks instead of import_tasks, both tasks from other_tasks.yml will be executed as expected. For more information on the differences between include v import see Reusing Ansible artifacts.

There are three ways to apply conditions to roles:

Add the same condition or conditions to all tasks in the role by placing your when statement under the roles keyword. See the example in this section.

Add the same condition or conditions to all tasks in the role by placing your when statement on a static import_role in your playbook.

Add a condition or conditions to individual tasks or blocks within the role itself. This is the only approach that allows you to select or skip some tasks within the role based on your when statement. To select or skip tasks within the role, you must have conditions set on individual tasks or blocks, use the dynamic include_role in your playbook, and add the condition or conditions to the include. When you use this approach, Ansible applies the condition to the include itself plus any tasks in the role that also have that when statement.

When you incorporate a role in your playbook statically with the roles keyword, Ansible adds the conditions you define to all the tasks in the role. For example:

Sometimes the facts about a host determine the values you want to use for certain variables or even the file or template you want to select for that host. For example, the names of packages are different on CentOS and Debian. The configuration files for common services are also different on different OS flavors and versions. To load different variables files, templates, or other files based on a fact about the hosts:

name your vars files, templates, or files to match the Ansible fact that differentiates them

select the correct vars file, template, or file for each host with a variable based on that Ansible fact

Ansible separates variables from tasks, keeping your playbooks from turning into arbitrary code with nested conditionals. This approach results in more streamlined and auditable configuration rules because there are fewer decision points to track.

You can create a playbook that works on multiple platforms and OS versions with a minimum of syntax by placing your variable values in vars files and conditionally importing them. If you want to install Apache on some CentOS and some Debian servers, create variables files with YAML keys and values. For example:

Then import those variables files based on the facts you gather on the hosts in your playbook:

Ansible gathers facts on the hosts in the webservers group, then interpolates the variable “ansible_facts[‘os_family’]” into a list of file names. If you have hosts with Red Hat operating systems (CentOS, for example), Ansible looks for ‘vars/RedHat.yml’. If that file does not exist, Ansible attempts to load ‘vars/os_defaults.yml’. For Debian hosts, Ansible first looks for ‘vars/Debian.yml’, before falling back on ‘vars/os_defaults.yml’. If no files in the list are found, Ansible raises an error.

You can use the same approach when different OS flavors or versions require different configuration files or templates. Select the appropriate file or template based on the variables assigned to each host. This approach is often much cleaner than putting a lot of conditionals into a single template to cover multiple OS or package versions.

For example, you can template out a configuration file that is very different between, say, CentOS and Debian:

If your conditional when statement is not behaving as you intended, you can add a debug statement to determine if the condition evaluates to true or false. A common cause of unexpected behavior in conditionals is testing an integer as a string or a string as an integer. To debug a conditional statement, add the entire statement as the var: value in a debug task. Ansible then shows the test and how the statement evaluates. For example, here is a set of tasks and sample output:

The following Ansible facts are frequently used in conditionals.

Possible values (sample, not complete list):

The major version of the operating system. For example, the value is 16 for Ubuntu 16.04.

Possible values (sample, not complete list):

An introduction to playbooks

Playbook organization by roles

Tips and tricks for playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
tasks:
  - name: Configure SELinux to start mysql on any port
    ansible.posix.seboolean:
      name: mysql_connect_any
      state: true
      persistent: true
    when: ansible_selinux.status == "enabled"
    # all variables can be used directly in conditionals without double curly braces
```

Example 2 (unknown):
```unknown
- name: Show facts available on the system
  ansible.builtin.debug:
    var: ansible_facts
```

Example 3 (unknown):
```unknown
tasks:
  - name: Shut down Debian flavored systems
    ansible.builtin.command: /sbin/shutdown -t now
    when: ansible_facts['os_family'] == "Debian"
```

Example 4 (unknown):
```unknown
tasks:
  - name: Shut down CentOS 6 and Debian 7 systems
    ansible.builtin.command: /sbin/shutdown -t now
    when: (ansible_facts['distribution'] == "CentOS" and ansible_facts['distribution_major_version'] == "6") or
          (ansible_facts['distribution'] == "Debian" and ansible_facts['distribution_major_version'] == "7")
```

---

## Reusing Ansible artifacts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_reuse.html

**Contents:**
- Reusing Ansible artifacts
- Creating reusable files and roles
- Reusing playbooks
- When to turn a playbook into a role
- Reusing files and roles
  - Includes: dynamic reuse
  - Imports: static reuse
  - Comparing includes and imports: dynamic and static reuse
- Reusing tasks as handlers
  - Triggering included (dynamic) handlers

You can write a simple playbook in one very large file, and most users learn the one-file approach first. However, breaking your automation work up into smaller files is an excellent way to organize complex sets of tasks and reuse them. Smaller, more distributed artifacts let you reuse the same variables, tasks, and plays in multiple playbooks to address different use cases. You can use distributed artifacts across multiple parent playbooks or even multiple times within one playbook. For example, you might want to update your customer database as part of several different playbooks. If you put all the tasks related to updating your database in a tasks file or a role, you can reuse them in many playbooks while only maintaining them in one place.

Creating reusable files and roles

When to turn a playbook into a role

Reusing files and roles

Includes: dynamic reuse

Imports: static reuse

Comparing includes and imports: dynamic and static reuse

Reusing tasks as handlers

Triggering included (dynamic) handlers

Triggering imported (static) handlers

Ansible offers four distributed, reusable artifacts: variables files, task files, playbooks, and roles.

A variables file contains only variables.

A task file contains only tasks.

A playbook contains at least one play, and may contain variables, tasks, and other content. You can reuse tightly focused playbooks, but you can only reuse them statically, not dynamically.

A role contains a set of related tasks, variables, defaults, handlers, and even modules or other plugins in a defined file-tree. Unlike variables files, task files, or playbooks, roles can be easily uploaded and shared through Ansible Galaxy. See Roles for details about creating and using roles.

You can incorporate multiple playbooks into a main playbook. However, you can only use imports to reuse playbooks. For example:

Importing incorporates playbooks in other playbooks statically. Ansible runs the plays and tasks in each imported playbook in the order they are listed, just as if they had been defined directly in the main playbook.

You can select which playbook you want to import at runtime by defining your imported playbook file name with a variable, then passing the variable with either --extra-vars or the vars keyword. For example:

If you run this playbook with ansible-playbook my_playbook -e import_from_extra_var=other_playbook.yml, Ansible imports both one_playbook.yml and other_playbook.yml.

For some use cases, simple playbooks work well. However, starting at a certain level of complexity, roles work better than playbooks. A role lets you store your defaults, handlers, variables, and tasks in separate directories, instead of in a single long document. Roles are easy to share on Ansible Galaxy. For complex use cases, most users find roles easier to read, understand, and maintain than all-in-one playbooks.

Ansible offers two ways to reuse files and roles in a playbook: dynamic and static.

For dynamic reuse, add an include_* task in the tasks section of a play:

For static reuse, add an import_* task in the tasks section of a play:

Task include and import statements can be used at arbitrary depth.

You can still use the bare roles keyword at the play level to incorporate a role in a playbook statically. However, the bare include keyword, once used for both task files and playbook-level includes, is now deprecated.

Including roles, tasks, or variables adds them to a playbook dynamically. Ansible processes included files and roles as they come up in a playbook, so included tasks can be affected by the results of earlier tasks within the top-level playbook. Included roles and tasks are similar to handlers - they may or may not run, depending on the results of other tasks in the top-level playbook.

The primary advantage of using include_* statements is looping. When a loop is used with an include, the included tasks or roles will be executed once for each item in the loop.

The file names for included roles, tasks, and vars are templated before inclusion.

You can pass variables into includes. See Variable precedence: where should I put a variable? for more details on variable inheritance and precedence.

Importing roles, tasks, or playbooks adds them to a playbook statically. Ansible pre-processes imported files and roles before it runs any tasks in a playbook, so imported content is never affected by other tasks within the top-level playbook.

The file names for imported roles and tasks support templating, but the variables must be available when Ansible is pre-processing the imports. This can be done with the vars keyword or by using --extra-vars.

You can pass variables to imports. You must pass variables if you want to run an imported file more than once in a playbook. For example:

See Variable precedence: where should I put a variable? for more details on variable inheritance and precedence.

Each approach to reusing distributed Ansible artifacts has advantages and limitations. You may choose dynamic reuse for some playbooks and static reuse for others. Although you can use both dynamic and static reuse in a single playbook, it is best to select one approach per playbook. Mixing static and dynamic reuse can introduce difficult-to-diagnose bugs into your playbooks. This table summarizes the main differences so you can choose the best approach for each playbook you create.

At runtime, when encountered

Pre-processed during playbook parsing

All includes are tasks

import_playbook cannot be a task

Apply only to include task itself

Apply to all child tasks in import

Executed once for each loop item

Cannot be used in a loop

Tags within includes not listed

All tags appear with --list-tags

Tasks within includes not listed

All tasks appear with --list-tasks

Cannot trigger handlers within includes

Can trigger individual imported handlers

Using --start-at-task

Cannot start at tasks within includes

Can start at imported tasks

Using inventory variables

Can include_*: {{ inventory_var }}

Cannot import_*: {{ inventory_var }}

Can import full playbooks

Can include variables files

Use vars_files: to import variables

There are also big differences in resource consumption and performance, imports are quite lean and fast, while includes require a lot of management and accounting.

You can also use includes and imports in the Handlers: running operations on change section of a playbook. For example, if you want to define how to restart Apache, you only have to do that once for all of your playbooks. You might make a restarts.yml file that looks like:

You can trigger handlers from either an import or an include, but the procedure is different for each method of reuse. If you include the file, you must notify the include itself, which triggers all the tasks in restarts.yml. If you import the file, you must notify the individual task(s) within restarts.yml. You can mix direct tasks and handlers with included or imported tasks and handlers.

Includes are executed at run-time, so the name of the include exists during play execution, but the included tasks do not exist until the include itself is triggered. To use the Restart apache task with dynamic reuse, refer to the name of the include itself. This approach triggers all tasks in the included file as handlers. For example, with the task file shown above:

Imports are processed before the play begins, so the name of the import no longer exists during play execution, but the names of the individual imported tasks do exist. To use the Restart apache task with static reuse, refer to the name of each task or tasks within the imported file. For example, with the task file shown above:

Documentation of the include* and import* modules discussed here.

Review the basic Playbook language features

All about variables in playbooks

Conditionals in playbooks

Tips and tricks for playbooks

How to share roles on galaxy, role management

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- import_playbook: webservers.yml
- import_playbook: databases.yml
```

Example 2 (unknown):
```unknown
- import_playbook: "/path/to/{{ import_from_extra_var }}"
- import_playbook: "{{ import_from_vars }}"
  vars:
    import_from_vars: /path/to/one_playbook.yml
```

Example 3 (unknown):
```unknown
tasks:
- import_tasks: wordpress.yml
  vars:
    wp_user: timmy

- import_tasks: wordpress.yml
  vars:
    wp_user: alice

- import_tasks: wordpress.yml
  vars:
    wp_user: bob
```

Example 4 (unknown):
```unknown
# restarts.yml
- name: Restart apache
  ansible.builtin.service:
    name: apache
    state: restarted

- name: Restart mysql
  ansible.builtin.service:
    name: mysql
    state: restarted
```

---

## Ansible-core 2.15 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.15.html

**Contents:**
- Ansible-core 2.15 Porting Guide
- Playbook
  - Handlers
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins

This section discusses the behavioral changes between ansible-core 2.14 and ansible-core 2.15.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.15 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.15 Porting Guide

Noteworthy module changes

Porting custom scripts

Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.15.7, conditional expressions with embedded template blocks can fail with the message “Conditional is marked as unsafe, and cannot be evaluated.” when an embedded template consults data from untrusted sources like module results or vars marked !unsafe. Conditionals with embedded templates can be a source of malicious template injection when referencing untrusted data, and can nearly always be rewritten without embedded templates. Playbook task conditional keywords such as when and until have long displayed warnings discouraging use of embedded templates in conditionals; this warning has been expanded to non-task conditionals as well, such as the assert action.

As documented, if multiple handlers of a specific name have been defined, the last one added into the play is the one that is executed when being notified. Prior to ansible-core 2.15, this was not the case for handlers included dynamically into the play with the include_role task. This issue has been addressed in ansible-core 2.15, and users relying on the ansible-core 2.14 and older behavior may need to adjust their playbooks accordingly.

As an example of the behavior change, consider the following:

The example assumes there is a task within the role foo that notifies a handler named foo_handler within the role foo.

The fact that different variables and/or their values are attached to include_role tasks including the same role makes them distinct roles.

The second invocation of the include_role task results in including tasks and handlers from the role regardless of the when conditional evaluation result. The when conditional is attached to the block wrapping the include_role task and as such the when conditional is applied to all tasks and handlers from the role after they are included into the play.

By the time the flush_handlers task runs, all hosts notified foo_handler within the first invocation of include_role. Additionally the host bar (due to when restricting all other hosts) notified foo_handler again during the second invocation of include_role.

On ansible-core 2.15, the last handler named foo_handler added into the play is from the second include_role invocation and therefore has when: inventory_hostname == "bar" attached to it, resulting in the handler being actually run only on the host bar and skipped on all other hosts. Consequently the notifications from the host bar have been de-duplicated.

On ansible-core 2.14 and older, foo_handler from the first invocation runs on all hosts. Additionally, foo_handler from the second invocation is run on the host bar again.

The return code of ansible-galaxy search is now 0 instead of 1 and the stdout is empty when results are empty to align with other ansible-galaxy commands.

Providing a list of dictionaries to vars: is deprecated in favor of supplying a dictionary.

The following modules no longer exist:

**Examples:**

Example 1 (unknown):
```unknown
- name: task with a module result (always untrusted by Ansible)
  shell: echo "hi mom"
  register: untrusted_result

# don't do it this way...
# - name: insecure conditional with embedded template consulting untrusted data
#   assert:
#     that: '"hi mom" is in {{ untrusted_result.stdout }}'

- name: securely access untrusted values directly as Jinja variables instead
  assert:
    that: '"hi mom" is in untrusted_result.stdout'
```

Example 2 (unknown):
```unknown
- include_role:
    name: foo
  vars:
    invocation: 1

- block:
   - include_role:
       name: foo
     vars:
       invocation: 2
  when: inventory_hostname == "bar"

- meta: flush_handlers
```

Example 3 (unknown):
```unknown
vars:
  - var1: foo
  - var2: bar
```

Example 4 (unknown):
```unknown
vars:
  var1: foo
  var2: bar
```

---

## Module defaults — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_module_defaults.html

**Contents:**
- Module defaults
- Module defaults groups

If you frequently call the same module with the same arguments, it can be useful to define default arguments for that particular module using the module_defaults keyword.

Here is a basic example:

The module_defaults keyword can be used at the play, block, and task level. Any module arguments explicitly specified in a task will override any established default for that module argument.

You can remove any previously established defaults for a module by specifying an empty dict.

Any module defaults set at the play level (and block/task level when using include_role or import_role) will apply to any roles used, which may cause unexpected behavior in the role.

Here are some more realistic use cases for this feature.

Interacting with an API that requires auth.

Setting a default AWS region for specific EC2-related modules.

Module default groups allow to provide common parameters to groups of modules that belong together. Collections can define such groups in their meta/runtime.yml file.

module_defaults does not take the collections keyword into account, so the fully qualified group name must be used for new groups in module_defaults.

Here is an example runtime.yml file for the ns.coll collection. This file defines an action group named ns.coll.my_group and places the sample_module from ns.coll and another_module from another.collection into the group.

This group can now be used in a playbook like this:

For historical reasons and backwards compatibility, there are some special groups:

Extended module group

amazon.aws.aws and community.aws.aws

azure.azcollection.azure

community.kubernetes.k8s, community.general.k8s, community.kubevirt.k8s, community.okd.k8s, and kubernetes.core.k8s

community.crypto.acme

community.general.docker and community.docker.docker

ovirt.ovirt.ovirt and community.general.ovirt

community.vmware.vmware

Check out the documentation for the collection or its meta/runtime.yml to see which action plugins and modules are included in the group.

Use the groups with module_defaults by prefixing the group name with group/ - for example group/aws.

In a playbook, you can set module defaults for whole groups of modules, such as setting a common AWS region.

More information on meta/runtime.yml, including the complete format for action_groups, can be found in runtime.yml.

**Examples:**

Example 1 (unknown):
```unknown
- hosts: localhost
  module_defaults:
    ansible.builtin.file:
      owner: root
      group: root
      mode: 0755
  tasks:
    - name: Create file1
      ansible.builtin.file:
        state: touch
        path: /tmp/file1

    - name: Create file2
      ansible.builtin.file:
        state: touch
        path: /tmp/file2

    - name: Create file3
      ansible.builtin.file:
        state: touch
        path: /tmp/file3
```

Example 2 (unknown):
```unknown
- block:
    - name: Print a message
      ansible.builtin.debug:
        msg: "Different message"
  module_defaults:
    ansible.builtin.debug:
      msg: "Default message"
```

Example 3 (unknown):
```unknown
- name: Create file1
  ansible.builtin.file:
    state: touch
    path: /tmp/file1
  module_defaults:
    file: {}
```

Example 4 (unknown):
```unknown
- hosts: localhost
  module_defaults:
    ansible.builtin.uri:
      force_basic_auth: true
      user: some_user
      password: some_password
  tasks:
    - name: Interact with a web service
      ansible.builtin.uri:
        url: http://some.api.host/v1/whatever1

    - name: Interact with a web service
      ansible.builtin.uri:
        url: http://some.api.host/v1/whatever2

    - name: Interact with a web service
      ansible.builtin.uri:
        url: http://some.api.host/v1/whatever3
```

---

## Developing collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections.html

**Contents:**
- Developing collections

Collections are a distribution format for Ansible content. You can package and distribute playbooks, roles, modules, and plugins using collections. A typical collection addresses a set of related use cases. For example, the cisco.ios collection automates management of Cisco IOS devices.

You can create a collection and publish it to Ansible Galaxy or to a private Automation Hub instance. You can publish certified collections to the Red Hat Automation Hub, part of the Red Hat Ansible Automation Platform.

Examine the Ansible collection creator path to understand how to go from creating a collection to having it included in the Ansible package distribution.

Developing new collections

Working with existing collections

Collections references

For instructions on developing modules, see Developing modules.

Learn how to install and use collections in playbooks and roles

Guidelines for contributing to selected collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Using filters to manipulate data — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_filters.html

**Contents:**
- Using filters to manipulate data
- Handling undefined variables
  - Providing default values
  - Making variables optional
  - Defining mandatory values
- Defining different values for true/false/null (ternary)
- Managing data types
  - Discovering the data type
  - Transforming strings into lists
  - Transforming dictionaries into lists

Filters let you transform JSON data into YAML data, split a URL to extract the hostname, get the SHA1 hash of a string, add or multiply integers, and much more. You can use the Ansible-specific filters documented here to manipulate your data, or use any of the standard filters shipped with Jinja2 - see the list of built-in filters in the official Jinja2 template documentation. You can also use Python methods to transform data. You can create custom Ansible filters as plugins, though we generally welcome new filters into the ansible-core repo so everyone can use them.

Because templating happens on the Ansible control node, not on the target host, filters execute on the control node and transform data locally.

Handling undefined variables

Providing default values

Making variables optional

Defining mandatory values

Defining different values for true/false/null (ternary)

Discovering the data type

Transforming strings into lists

Transforming dictionaries into lists

Transforming lists into dictionaries

Forcing the data type

Formatting data: YAML and JSON

Filter to_json and Unicode support

Combining and selecting data

Combining items from multiple lists: zip and zip_longest

Combining objects and subelements

Combining hashes/dictionaries

Selecting values from arrays or hashtables

Selecting JSON data: JSON queries

Random items or numbers

Managing list variables

Selecting from sets or lists (set theory)

Calculating numbers (math)

Managing network interactions

Hashing and encrypting strings and passwords

Adding comments to files

Searching strings with regular expressions

Managing file names and path names

Handling dates and times

Getting Kubernetes resource names

Filters can help you manage missing or undefined variables by providing defaults or making some variables optional. If you configure Ansible to ignore most undefined variables, you can mark some variables as requiring values with the mandatory filter.

You can provide default values for variables directly in your templates using the Jinja2 ‘default’ filter. This is often a better approach than failing if a variable is not defined:

In the above example, if the variable ‘some_variable’ is not defined, Ansible uses the default value 5, rather than raising an “undefined variable” error and failing. If you are working within a role, you can also add role defaults to define the default values for variables in your role. To learn more about role defaults see Role directory structure.

Beginning in version 2.8, attempting to access an attribute of an Undefined value in Jinja will return another Undefined value, rather than throwing an error immediately. This means that you can now simply use a default with a value in a nested data structure (in other words, {{ foo.bar.baz | default('DEFAULT') }}) when you do not know if the intermediate values are defined.

If you want to use the default value when variables evaluate to false or an empty string you have to set the second parameter to true:

By default, Ansible requires values for all variables in a templated expression. However, you can make specific module variables optional. For example, you might want to use a system default for some items and control the value for others. To make a module variable optional, set the default value to the special variable omit:

In this example, the default mode for the files /tmp/foo and /tmp/bar is determined by the umask of the system. Ansible does not send a value for mode. Only the third file, /tmp/baz, receives the mode=0444 option.

If you are “chaining” additional filters after the default(omit) filter, you should instead do something like this: "{{ foo | default(None) | some_filter or omit }}". In this example, the default None (Python null) value will cause the later filters to fail, which will trigger the or omit portion of the logic. Using omit in this manner is very specific to the later filters you are chaining though, so be prepared for some trial and error if you do this.

If you configure Ansible to ignore undefined variables, you may want to define some values as mandatory. By default, Ansible fails if a variable in your playbook or command is undefined. You can configure Ansible to allow undefined variables by setting DEFAULT_UNDEFINED_VAR_BEHAVIOR to false. In that case, you may want to require some variables to be defined. You can do this with:

The variable value will be used as is, but the template evaluation will raise an error if it is undefined.

A convenient way of requiring a variable to be overridden is to give it an undefined value using the undef() function.

You can create a test, then define one value to use when the test returns true and another when the test returns false (new in version 1.9):

In addition, you can define one value to use on true, one value on false and a third value on null (new in version 2.8):

You might need to know, change, or set the data type on a variable. For example, a registered variable might contain a dictionary when your next task needs a list, or a user prompt might return a string when your playbook needs a boolean value. Use the ansible.builtin.type_debug, ansible.builtin.dict2items, and ansible.builtin.items2dict filters to manage data types. You can also use the data type itself to cast a value as a specific data type.

If you are unsure of the underlying Python type of a variable, you can use the ansible.builtin.type_debug filter to display it. This is useful in debugging when you need a particular type of variable:

You should note that, while this may seem like a useful filter for checking that you have the right type of data in a variable, you should often prefer type tests, which will allow you to test for specific data types.

Use the ansible.builtin.split filter to transform a character/string delimited string into a list of items suitable for looping. For example, if you want to split a string variable fruits by commas, you can use:

String data (before applying the ansible.builtin.split filter):

List data (after applying the ansible.builtin.split filter):

Use the ansible.builtin.dict2items filter to transform a dictionary into a list of items suitable for looping:

Dictionary data (before applying the ansible.builtin.dict2items filter):

List data (after applying the ansible.builtin.dict2items filter):

The ansible.builtin.dict2items filter is the reverse of the ansible.builtin.items2dict filter.

If you want to configure the names of the keys, the ansible.builtin.dict2items filter accepts 2 keyword arguments. Pass the key_name and value_name arguments to configure the names of the keys in the list output:

Dictionary data (before applying the ansible.builtin.dict2items filter):

List data (after applying the ansible.builtin.dict2items filter):

Use the ansible.builtin.items2dict filter to transform a list into a dictionary, mapping the content into key: value pairs:

List data (before applying the ansible.builtin.items2dict filter):

Dictionary data (after applying the ansible.builtin.items2dict filter):

The ansible.builtin.items2dict filter is the reverse of the ansible.builtin.dict2items filter.

Not all lists use key to designate keys and value to designate values. For example:

In this example, you must pass the key_name and value_name arguments to configure the transformation. For example:

If you do not pass these arguments, or do not pass the correct values for your list, you will see KeyError: key or KeyError: my_typo.

You can cast values as certain types. For example, if you expect the input “True” from a vars_prompt and you want Ansible to recognize it as a boolean value instead of a string:

If you want to perform a mathematical comparison on a fact and you want Ansible to recognize it as an integer instead of a string:

You can switch a data structure in a template from or to JSON or YAML format, with options for formatting, indenting, and loading data. The basic filters are occasionally useful for debugging:

See ansible.builtin.to_json and ansible.builtin.to_yaml for documentation on these filters.

For human readable output, you can use:

See ansible.builtin.to_nice_json and ansible.builtin.to_nice_yaml for documentation on these filters.

You can change the indentation of either format:

The ansible.builtin.to_yaml and ansible.builtin.to_nice_yaml filters use the PyYAML library which has a default 80 symbol string length limit. That causes an unexpected line break after 80th symbol (if there is a space after 80th symbol) To avoid such behavior and generate long lines, use the width option. You must use a hardcoded number to define the width, instead of a construction like float("inf"), because the filter does not support proxying Python functions. For example:

The filter does support passing through other YAML parameters. For a full list, see the PyYAML documentation for dump().

If you are reading in some already formatted data:

By default ansible.builtin.to_json and ansible.builtin.to_nice_json will convert data received to ASCII, so:

To keep Unicode characters, pass the parameter ensure_ascii=False to the filter:

To parse multi-document YAML strings, the ansible.builtin.from_yaml_all filter is provided. The ansible.builtin.from_yaml_all filter will return a generator of parsed YAML documents.

You can combine data from multiple sources and types, and select values from large data structures, giving you precise control over complex data.

To get a list combining the elements of other lists use ansible.builtin.zip:

To always exhaust all lists use ansible.builtin.zip_longest:

Similarly to the output of the ansible.builtin.items2dict filter mentioned above, these filters can be used to construct a dict:

List data (before applying the ansible.builtin.zip filter):

Dictionary data (after applying the ansible.builtin.zip filter):

The ansible.builtin.subelements filter produces a product of an object and the subelement values of that object, similar to the ansible.builtin.subelements lookup. This lets you specify individual subelements to use in a template. For example, this expression:

Data before applying the ansible.builtin.subelements filter:

Data after applying the ansible.builtin.subelements filter:

You can use the transformed data with loop to iterate over the same subelement for multiple objects:

The ansible.builtin.combine filter allows hashes to be merged. For example, the following would override keys in one hash:

The resulting hash would be:

The filter can also take multiple arguments to merge:

In this case, keys in d would override those in c, which would override those in b, and so on.

The filter also accepts two optional parameters: recursive and list_merge.

Is a boolean, default to False. Should the ansible.builtin.combine recursively merge nested hashes. Note: It does not depend on the value of the hash_behaviour setting in ansible.cfg.

Is a string, its possible values are replace (default), keep, append, prepend, append_rp or prepend_rp. It modifies the behavior of ansible.builtin.combine when the hashes to merge contain arrays/lists.

If recursive=False (the default), nested hash aren’t merged:

This would result in:

If recursive=True, recurse into a nested hash and merge their keys:

This would result in:

If list_merge='replace' (the default), arrays from the right hash will “replace” the ones in the left hash:

This would result in:

If list_merge='keep', arrays from the left hash will be kept:

This would result in:

If list_merge='append', arrays from the right hash will be appended to the ones in the left hash:

This would result in:

If list_merge='prepend', arrays from the right hash will be prepended to the ones in the left hash:

This would result in:

If list_merge='append_rp', arrays from the right hash will be appended to the ones in the left hash. Elements of arrays in the left hash that are also in the corresponding array of the right hash will be removed (“rp” stands for “remove present”). Duplicate elements that aren’t in both hashes are kept:

This would result in:

If list_merge='prepend_rp', the behavior is similar to the one for append_rp, but elements of arrays in the right hash are prepended:

This would result in:

recursive and list_merge can be used together:

This would result in:

The extract filter is used to map from a list of indices to a list of values from a container (hash or array):

The results of the above expressions would be:

The filter can take another argument:

This takes the list of hosts in group ‘x’, looks them up in hostvars, and then looks up the ec2_ip_address of the result. The final result is a list of IP addresses for the hosts in group ‘x’.

The third argument to the filter can also be a list, for a recursive lookup inside the container:

This would return a list containing the value of b[‘a’][‘x’][‘y’].

This set of filters returns a list of combined lists.

To get permutations of a list:

Combinations always require a set size:

Also see the zip and zip_longest filters

The product filter returns the cartesian product of the input iterables. This is roughly equivalent to nested for-loops in a generator expression.

For example Generate multiple hostnames:

To select a single element or a data subset from a complex data structure in JSON format (for example, Ansible facts), use the community.general.json_query filter. The community.general.json_query filter lets you query a complex JSON structure and iterate over it using a loop structure.

This filter has migrated to the community.general collection. Follow the installation instructions to install that collection.

You must manually install the jmespath dependency on the Ansible control node before using this filter. This filter is built upon jmespath, and you can use the same syntax. For examples, see jmespath examples.

Consider this data structure:

To extract all clusters from this structure, you can use the following query:

To extract all server names:

To extract ports from cluster1:

You can use a variable to make the query more readable.

To print out the ports from cluster1 in a comma-separated string:

In the example above, quoting literals using backticks avoids escaping quotes and maintains readability.

You can use YAML single quote escaping:

Escaping single quotes within single quotes in YAML is done by doubling the single quote.

To get a hash map with all ports and names of a cluster:

To extract ports from all clusters with the name starting with ‘server1’:

To extract ports from all clusters with the name containing ‘server1’:

while using starts_with and contains, you have to use `` to_json | from_json `` filter for correct parsing of data structure.

When you need a randomly generated value, use one of these filters.

This filter can be used to generate a random MAC address from a string prefix.

This filter has migrated to the community.general collection. Follow the installation instructions to install that collection.

To get a random MAC address from a string prefix starting with ‘52:54:00’:

Note that if anything is wrong with the prefix string, the filter will issue an error.

As of Ansible version 2.9, you can also initialize the random number generator from a seed to create random-but-idempotent MAC addresses:

The ansible.builtin.random filter in Ansible is an extension of the default Jinja2 random filter, and can be used to return a random item from a sequence of items or to generate a random number based on a range.

To get a random item from a list:

To get a random number between 0 (inclusive) and a specified integer (exclusive):

To get a random number from 0 to 100 but in steps of 10:

To get a random number from 1 to 100 but in steps of 10:

You can initialize the random number generator from a seed to create random-but-idempotent numbers:

The ansible.builtin.shuffle filter randomizes an existing list, giving a different order for every invocation.

To get a random list from an existing list:

You can initialize the shuffle generator from a seed to generate a random-but-idempotent order:

The shuffle filter returns a list whenever possible. If you use it with a non ‘listable’ item, the filter does nothing.

You can search for the minimum or maximum value in a list, or flatten a multi-level list.

To get the minimum value from the list of numbers:

To get the minimum value in a list of objects:

To get the maximum value from a list of numbers:

To get the maximum value in a list of objects:

Flatten a list (same thing the flatten lookup does):

Flatten only the first level of a list (akin to the items lookup):

Preserve nulls in a list (flatten removes them by default):

Create a list from a list repeated N times:

You can select or combine items from sets or lists. Note, multisets are currently not supported and all of the following filters imply uniqueness. That means that duplicate elements are removed from the result.

To get a unique set from a list:

To get a union (with duplicate elements removed) of two lists:

To get the intersection of 2 lists (unique list of all items in both):

To get the difference of 2 lists (items in 1 that don’t exist in 2):

To get the symmetric difference of 2 lists (items exclusive to each list):

You can calculate logs, powers, and roots of numbers with Ansible filters. Jinja2 provides other mathematical functions like abs() and round().

Get the logarithm (default is e):

Get the base 10 logarithm:

Give me the power of 2! (or 5):

Square root, or the 5th:

These filters help you with common network tasks.

These filters have migrated to the ansible.utils collection. Follow the installation instructions to install that collection.

To test if a string is a valid IP address:

You can also require a specific IP protocol version:

IP address filter can also be used to extract specific information from an IP address. For example, to get the IP address itself from a CIDR, you can use:

More information about ansible.utils.ipaddr filter and complete usage guide can be found in Ansible.Utils.

To convert the output of a network device CLI command into structured JSON output, use the ansible.netcommon.parse_cli filter:

The ansible.netcommon.parse_cli filter will load the spec file and pass the command output through it, returning JSON output. The YAML spec file defines how to parse the CLI output.

The spec file should be valid formatted YAML. It defines how to parse the CLI output and return JSON data. Below is an example of a valid spec file that will parse the output from the show vlan command.

The spec file above will return a JSON data structure that is a list of hashes with the parsed VLAN information.

The same command could be parsed into a hash by using the key and values directives. Here is an example of how to parse the output into a hash value using the same show vlan command.

Another common use case for parsing CLI commands is to break a large command into blocks that can be parsed. This can be done using the start_block and end_block directives to break the command into blocks that can be parsed.

The example above will parse the output of show interface into a list of hashes.

The network filters also support parsing the output of a CLI command using the TextFSM library. To parse the CLI output with TextFSM use the following filter:

Use of the TextFSM filter requires the TextFSM library to be installed.

To convert the XML output of a network device command into structured JSON output, use the ansible.netcommon.parse_xml filter:

The ansible.netcommon.parse_xml filter will load the spec file and pass the command output through formatted as JSON.

The spec file should be valid formatted YAML. It defines how to parse the XML output and return JSON data.

Below is an example of a valid spec file that will parse the output from the show vlan | display xml command.

The spec file above will return a JSON data structure that is a list of hashes with the parsed VLAN information.

The same command could be parsed into a hash by using the key and values directives. Here is an example of how to parse the output into a hash value using the same show vlan | display xml command.

The value of top is the XPath relative to the XML root node. In the example, XML output given below, the value of top is configuration/vlans/vlan, which is an XPath expression relative to the root node (<rpc-reply>). configuration in the value of top is the outermost container node, and vlan is the innermost container node.

items is a dictionary of key-value pairs that map user-defined names to XPath expressions that select elements. The Xpath expression is relative to the value of the XPath value contained in top. For example, the vlan_id in the spec file is a user-defined name and its value vlan-id is the relative to the value of XPath in top

Attributes of XML tags can be extracted using XPath expressions. The value of state in the spec is an XPath expression used to get the attributes of the vlan tag in output XML.:

For more information on supported XPath expressions, see XPath Support.

Use the ansible.netcommon.vlan_parser filter to transform an unsorted list of VLAN integers into a sorted string list of integers according to IOS-like VLAN list rules. This list has the following properties:

Vlans are listed in ascending order.

Three or more consecutive VLANs are listed with a dash.

The first line of the list can be first_line_len characters long.

Subsequent list lines can be other_line_len characters.

This example renders the following sorted list:

Another example Jinja template:

This allows for the dynamic generation of VLAN lists on a Cisco IOS tagged interface. You can store an exhaustive raw list of the exact VLANs required for an interface and then compare that to the parsed IOS output that would actually be generated for the configuration.

To get the sha1 hash of a string:

To get the md5 hash of a string:

Get a string checksum:

Other hashes (platform dependent):

To get a sha512 password hash (random salt):

To get a sha256 password hash with a specific salt:

An idempotent method to generate unique hashes per system is to use a salt that is consistent between runs:

Hash types available depend on the control system running Ansible, ansible.builtin.hash depends on hashlib, ansible.builtin.password_hash depends on passlib. The crypt is used as a fallback if passlib is not installed.

Some hash types allow providing a rounds parameter:

The filter password_hash produces different results depending on whether you installed passlib or not.

To ensure idempotency, specify rounds to be neither crypt’s nor passlib’s default, which is 5000 for crypt and a variable value (535000 for sha256, 656000 for sha512) for passlib:

Hash type ‘blowfish’ (BCrypt) provides the facility to specify the version of the BCrypt algorithm.

The parameter is only available for blowfish (BCrypt). Other hash types will simply ignore this parameter. Valid values for this parameter are: [‘2’, ‘2a’, ‘2y’, ‘2b’]

You can also use the Ansible ansible.builtin.vault filter to encrypt data:

And then decrypt it using the unvault filter:

Several filters work with text, including URLs, file names, and path names.

The ansible.builtin.comment filter lets you create comments in a file from text in a template, with a variety of comment styles. By default, Ansible uses # to start a comment line and adds a blank comment line above and below your comment text. For example the following:

produces this output:

Ansible offers styles for comments in C (//...), C block (/*...*/), Erlang (%...) and XML (<!--...-->):

You can define a custom comment character. This filter:

You can fully customize the comment style:

That creates the following output:

The urlencode filter quotes data for use in a URL path or query using UTF-8:

The ansible.builtin.urlsplit filter extracts the fragment, hostname, netloc, password, path, port, query, scheme, and username from an URL. With no arguments, returns a dictionary of all the fields:

To search in a string or extract parts of a string with a regular expression, use the ansible.builtin.regex_search filter:

To extract all occurrences of regex matches in a string, use the ansible.builtin.regex_findall filter:

To replace text in a string with regex, use the ansible.builtin.regex_replace filter:

If you want to match the whole string and you are using * make sure to always wraparound your regular expression with the start/end anchors. For example ^(.*)$ will always match only one result, while (.*) on some Python versions will match the whole string and an empty string at the end, which means it will make two replacements:

Prior to ansible 2.0, if ansible.builtin.regex_replace filter was used with variables inside YAML arguments (as opposed to simpler ‘key=value’ arguments), then you needed to escape backreferences (for example, \\1) with 4 backslashes (\\\\) instead of 2 (\\).

To escape special characters within a standard Python regex, use the ansible.builtin.regex_escape filter (using the default re_type='python' option):

To escape special characters within a POSIX basic regex, use the ansible.builtin.regex_escape filter with the re_type='posix_basic' option:

To get the last name of a file path, like ‘foo.txt’ out of ‘/etc/asdf/foo.txt’:

To get the last name of a Windows style file path (new in version 2.0):

To separate the Windows drive letter from the rest of a file path (new in version 2.0):

To get only the Windows drive letter:

To get the rest of the path without the drive letter:

To get the directory from a path:

To get the directory from a Windows path (new version 2.0):

To expand a path containing a tilde (~) character (new in version 1.5):

To expand a path containing environment variables:

expandvars expands local variables; using it on remote paths can lead to errors.

To get the real path of a link (new in version 1.8):

To get the relative path of a link, from a start point (new in version 1.7):

To get the root and extension of a path or file name (new in version 2.0):

The ansible.builtin.splitext filter always returns a pair of strings. The individual components can be accessed by using the first and last filters:

To join one or more path components:

To add quotes for shell usage:

(Documentation: ansible.builtin.quote)

To concatenate a list into a string:

To split a string into a list:

To work with Base64 encoded strings:

(Documentation: ansible.builtin.b64encode)

As of version 2.6, you can define the type of encoding to use, the default is utf-8:

(Documentation: ansible.builtin.b64decode)

The string filter is only required for Python 2 and ensures that the text to encode is a unicode string. Without that filter before b64encode the wrong value will be encoded.

The return value of b64decode is a string. If you decrypt a binary blob using b64decode and then try to use it (for example by using copy to write it to a file) you will most likely find that your binary has been corrupted. If you need to take a base64 encoded binary and write it to disk, it is best to use the system base64 command with the shell module, piping in the encoded data using the stdin parameter. For example: shell: cmd="base64 --decode > myfile.bin" stdin="{{ encoded }}"

To create a namespaced UUIDv5:

To create a namespaced UUIDv5 using the default Ansible namespace ‘361E6D51-FAEC-444A-9079-341386DA8E2E’:

To make use of one attribute from each item in a list of complex variables, use the Jinja2 map filter:

To get a date object from a string use the to_datetime filter:

For a full list of format codes for working with Python date format strings, see the python datetime documentation.

To format a date using a string (like with the shell date command), use the “strftime” filter:

strftime takes an optional utc argument, defaulting to False, meaning times are in the local timezone:

To get all string possibilities, check https://docs.python.org/3/library/time.html#time.strftime

These filters have migrated to the kubernetes.core collection. Follow the installation instructions to install that collection.

Use the “k8s_config_resource_name” filter to obtain the name of a Kubernetes ConfigMap or Secret, including its hash:

This can then be used to reference hashes in Pod specifications:

An introduction to playbooks

Conditional statements in playbooks

Playbook organization by roles

Tips and tricks for playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

How to use inline regular expression flags

**Examples:**

Example 1 (unknown):
```unknown
{{ some_variable | default(5) }}
```

Example 2 (unknown):
```unknown
{{ lookup('env', 'MY_USER') | default('admin', true) }}
```

Example 3 (unknown):
```unknown
- name: Touch files with an optional mode
  ansible.builtin.file:
    dest: "{{ item.path }}"
    state: touch
    mode: "{{ item.mode | default(omit) }}"
  loop:
    - path: /tmp/foo
    - path: /tmp/bar
    - path: /tmp/baz
      mode: "0444"
```

Example 4 (unknown):
```unknown
{{ variable | mandatory }}
```

---

## Loops — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_loops.html

**Contents:**
- Loops
- Comparing loops
- Using loops
  - Iterating over a simple list
  - Iterating over a list of hashes
  - Iterating over a dictionary
  - Registering variables with a loop
  - Retrying a task until a condition is met
  - Looping over inventory
- Ensuring list input for loop: using query rather than lookup

Ansible offers the loop, with_<lookup>, and until keywords to execute a task multiple times. Examples of commonly-used loops include changing ownership on several files and/or directories with the file module, creating multiple users with the user module, and repeating a polling step until a certain result is reached.

We added loop in Ansible 2.5. as a simpler way to do loops, but we recommend it for most use cases.

We have not deprecated the use of with_<lookup> - that syntax will still be valid for the foreseeable future.

loop and with_<lookup> are mutually exclusive. While it is possible to nest them under until, this affects each loop iteration.

Iterating over a simple list

Iterating over a list of hashes

Iterating over a dictionary

Registering variables with a loop

Retrying a task until a condition is met

Looping over inventory

Ensuring list input for loop: using query rather than lookup

Adding controls to loops

Limiting loop output with label

Pausing within a loop

Breaking out of a loop

Tracking progress through a loop with index_var

Extended loop variables

Accessing the name of your loop_var

Iterating over nested lists

Stacking loops via include_tasks

Migrating from with_X to loop

with_nested/with_cartesian

The normal use case for until has to do with tasks that are likely to fail, while loop and with_<lookup> are meant for repeating tasks with slight variations.

The loop and with_<lookup> will run the task once per item in the list used as input, while until will rerun the task until a condition is met. For programmers the former are “for loops” and the latter is a “while/until loop”.

The with_<lookup> keywords rely on Lookup plugins - even items is a lookup.

The loop keyword is equivalent to with_list, and is the best choice for simple loops.

The loop keyword will not accept a string as input, see Ensuring list input for loop: using query rather than lookup.

The until keyword accepts an ‘end conditional’ (expression that returns True or False) that is “implicitly templated” (no need for {{ }}), commonly based on the variable you register for the task.

loop_control affects both loop and with_<lookup>, but not until, which has its own companion keywords: retries and delay.

Generally speaking, any use of with_* covered in Migrating from with_X to loop can be updated to use loop.

Be careful when changing with_items to loop, as with_items performs implicit single-level flattening. You may need to use | flatten(1) with loop to match the exact outcome. For example, to get the same output as:

Any with_* statement that requires using lookup within a loop should not be converted to use the loop keyword. For example, instead of doing:

it is cleaner to keep

Repeated tasks can be written as standard loops over a simple list of strings. You can define the list directly in the task.

You can define the list in a variables file, or in the ‘vars’ section of your play, then refer to the name of the list in the task.

Either of these examples would be the equivalent of

You can pass a list directly to a parameter for some plugins. Most of the packaging modules, like yum and apt, have this capability. When available, passing the list to a parameter is better than looping over the task. For example

Check the module documentation to see if you can pass a list to any particular module’s parameter(s).

If you have a list of hashes, you can reference subkeys in a loop. For example:

When combining conditionals with a loop, the when: statement is processed separately for each item. See Basic conditionals with when for examples.

To loop over a dict, use the dict2items:

Here, we are iterating over server_configs and printing the key and selected nested fields.

If the values in the dictionary are themselves dictionaries (for example, each group maps to a dict containing a gid), remember that after applying dict2items each loop item has two attributes: item.key and item.value. Access nested fields via item.value.<field>.

You can register the output of a loop as a variable. For example

When you use register with a loop, the data structure placed in the variable will contain a results attribute that is a list of all responses from the module. This differs from the data structure returned when using register without a loop. The changed/failed/skipped attribute that’s beside the results will represent the overall state. changed/failed will be true if at least one of the iterations triggered a change/failed, while skipped will be true only if all iterations were skipped.

Subsequent loops over the registered variable to inspect the results may look like

During iteration, the result of the current item will be placed in the variable.

You can use the until keyword to retry a task until a certain condition is met. Here’s an example:

This task runs up to 5 times with a delay of 10 seconds between each attempt. If the result of any attempt has “all systems go” in its stdout, the task succeeds. The default value for “retries” is 3 and “delay” is 5.

To see the results of individual retries, run the play with -vv.

When you run a task with until and register the result as a variable, the registered variable will include a key called “attempts”, which records the number of retries for the task.

If until is not specified, the task will retry until the task succeeds but at most retries times (New in version 2.16).

You can combine the until keyword with loop or with_<lookup>. The result of the task for each element of the loop is registered in the variable and can be used in the until condition. Here is an example:

When you use the timeout keyword in a loop, it applies to each attempt of the task action. See TASK_TIMEOUT for more details.

Normally the play itself is a loop over your inventory, but sometimes you need a task to do the same over a different set of hosts. To loop over your inventory, or just a subset of it, you can use a regular loop with the ansible_play_batch or groups variables.

There is also a specific lookup plugin inventory_hostnames that can be used like this

More information on the patterns can be found in Patterns: targeting hosts and groups.

The loop keyword requires a list as input, but the lookup keyword returns a string of comma-separated values by default. Ansible 2.5 introduced a new Jinja2 function named query that always returns a list, offering a simpler interface and more predictable output from lookup plugins when using the loop keyword.

You can force lookup to return a list to loop by using wantlist=True, or you can use query instead.

The following two examples do the same thing.

The loop_control keyword lets you manage your loops in useful ways.

When looping over complex data structures, the console output of your task can be enormous. To limit the displayed output, use the label directive with loop_control.

The output of this task will display just the name field for each item instead of the entire contents of the multi-line {{ item }} variable.

This is for making console output more readable, not protecting sensitive data. If there is sensitive data in loop, set no_log: true on the task to prevent disclosure.

To control the time (in seconds) between the execution of each item in a task loop, use the pause directive with loop_control.

Use the break_when directive with loop_control to exit a loop after any item, based on Jinja2 expressions.

To keep track of where you are in a loop, use the index_var directive with loop_control. This directive specifies a variable name to contain the current loop index.

index_var is 0 indexed.

As of Ansible 2.8, you can get extended loop information using the extended option to loop control. This option will expose the following information.

ansible_loop.allitems

The list of all items in the loop

The current iteration of the loop. (1 indexed)

The current iteration of the loop. (0 indexed)

ansible_loop.revindex

The number of iterations from the end of the loop (1 indexed)

ansible_loop.revindex0

The number of iterations from the end of the loop (0 indexed)

True if first iteration

True if last iteration

The number of items in the loop

ansible_loop.previtem

The item from the previous iteration of the loop. Undefined during the first iteration.

ansible_loop.nextitem

The item from the following iteration of the loop. Undefined during the last iteration.

When using loop_control.extended more memory will be utilized on the control node. This is a result of ansible_loop.allitems containing a reference to the full loop data for every loop. When serializing the results for display in callback plugins within the main ansible process, these references may be dereferenced causing memory usage to increase.

To disable the ansible_loop.allitems item, to reduce memory consumption, set loop_control.extended_allitems: false.

As of Ansible 2.8, you can get the name of the value provided to loop_control.loop_var using the ansible_loop_var variable

For role authors, writing roles that allow loops, instead of dictating the required loop_var value, you can gather the value through the following

While we are using loop in these examples, the same applies to with_<lookup>.

The simplest way to ‘nest’ loops is to avoid nesting loops, just format the data to achieve the same result. You can use Jinja2 expressions to iterate over complex lists. For example, a loop can combine nested lists, which simulates a nested loop.

You can nest two looping tasks using include_tasks. However, by default, Ansible sets the loop variable item for each loop. This means the inner, nested loop will overwrite the value of item from the outer loop. To avoid this, you can specify the name of the variable for each loop using loop_var with loop_control.

If Ansible detects that the current loop is using a variable that has already been defined, it will raise an error to fail the task.

The until condition will apply per item of the loop:

This will make Ansible retry the first 2 items twice, then fail the item on the 3rd attempt, then succeed at the first attempt on the 3rd item, in the end failing the task as a whole.

In most cases, loops work best with the loop keyword instead of with_X style loops. The loop syntax is usually best expressed using filters instead of more complex use of query or lookup.

These examples show how to convert many common with_ style loops to loop and filters.

with_list is directly replaced by loop.

with_items is replaced by loop and the flatten filter.

with_indexed_items is replaced by loop, the flatten filter and loop_control.index_var.

with_flattened is replaced by loop and the flatten filter.

with_together is replaced by loop and the zip filter.

Another example with complex data

with_dict can be substituted by loop and either the dictsort or dict2items filters.

with_sequence is replaced by loop and the range function, and potentially the format filter.

The range of the loop is exclusive of the end point.

with_subelements is replaced by loop and the subelements filter.

with_nested and with_cartesian are replaced by loop and the product filter.

with_random_choice is replaced by just use of the random filter, without need of loop.

An introduction to playbooks

Playbook organization by roles

Tips and tricks for playbooks

Conditional statements in playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
with_items:
  - 1
  - [2,3]
  - 4
```

Example 2 (unknown):
```unknown
loop: "{{ [1, [2, 3], 4] | flatten(1) }}"
```

Example 3 (unknown):
```unknown
loop: "{{ lookup('fileglob', '*.txt', wantlist=True) }}"
```

Example 4 (unknown):
```unknown
with_fileglob: '*.txt'
```

---

## Galaxy Developer Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/galaxy/dev_guide.html

**Contents:**
- Galaxy Developer Guide
- Creating collections for Galaxy
- Creating roles for Galaxy
  - Force
  - Container enabled
  - Using a custom role skeleton
  - Authenticate with Galaxy
  - Import a role
  - Delete a role
  - Travis integrations

You can host collections and roles on Galaxy to share with the Ansible community. Galaxy content is formatted in pre-packaged units of work such as roles, and collections. You can create roles for provisioning infrastructure, deploying applications, and all of the tasks you do everyday. Taking this a step further, you can create collections which provide a comprehensive package of automation that may include multiple playbooks, roles, modules, and plugins.

Creating collections for Galaxy

Creating roles for Galaxy

Using a custom role skeleton

Authenticate with Galaxy

Collections are a distribution format for Ansible content. You can use collections to package and distribute playbooks, roles, modules, and plugins. You can publish and use collections through Ansible Galaxy.

See Developing collections for details on how to create collections.

Use the init command to initialize the base structure of a new role, saving time on creating the various directories and main.yml files a role requires

The above will create the following directory structure in the current working directory:

If you want to create a repository for the role, the repository root should be role_name.

If a directory matching the name of the role already exists in the current working directory, the init command will result in an error. To ignore the error use the --force option. Force will create the above subdirectories and files, replacing anything that matches.

If you are creating a Container Enabled role, pass --type container to ansible-galaxy init. This will create the same directory structure as above, but populate it with default files appropriate for a Container Enabled role. For example, the README.md has a slightly different structure, the .travis.yml file tests the role using Ansible Container, and the meta directory includes a container.yml file.

A custom role skeleton directory can be supplied as follows:

When a skeleton is provided, init will:

copy all files and directories from the skeleton to the new role

any .j2 files found outside of a templates folder will be rendered as templates. The only useful variable at the moment is role_name

The .git folder and any .git_keep files will not be copied

Alternatively, the role_skeleton and ignoring of files can be configured with ansible.cfg

Using the import, delete and setup commands to manage your roles on the Galaxy website requires authentication in the form of an API key, you must create an account on the Galaxy website.

To create an authentication token:

Click Collections > API Token.

Click Load Token and then copy it.

Save your token in the path set in the GALAXY_TOKEN_PATH.

The import``command requires that you authenticate with the API token. You can include it in your ``ansible.cfg file or use the --token command option. You are only allowed to remove roles where you have access to the repository in GitHub.

To import a new role:

By default, the command will wait for Galaxy to complete the import process, displaying the results as the import progresses:

See ansible-galaxy for other command options.

The delete command requires that you authenticate with the API token. You can include it in your ansible.cfg file or use the --token command option. You are only allowed to remove roles where you have access to the repository in GitHub.

Use the following to delete a role:

This only removes the role from Galaxy. It does not remove or alter the actual GitHub repository.

You can create an integration or connection between a role in Galaxy and Travis. Once the connection is established, a build in Travis will automatically trigger an import in Galaxy, updating the search index with the latest information about the role.

You create the integration using the setup command with your API token. You will also need an account in Travis, and your Travis token. Once you’re ready, use the following command to create the integration:

The setup command requires your Travis token, however the token is not stored in Galaxy. It is used along with the GitHub username and repo to create a hash as described in the Travis documentation. The hash is stored in Galaxy and used to verify notifications received from Travis.

The setup command enables Galaxy to respond to notifications. To configure Travis to run a build on your repository and send a notification, follow the Travis getting started guide.

To instruct Travis to notify Galaxy when a build completes, add the following to your .travis.yml file:

Use the --list option to display your Travis integrations:

Use the --remove option to disable and remove a Travis integration:

Provide the ID of the integration to be disabled. You can find the ID by using the --list option.

Shareable collections of modules, playbooks and roles

All about ansible roles

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
$ ansible-galaxy role init role_name
```

Example 2 (unknown):
```unknown
role_name/
    README.md
    defaults/
        main.yml
    files/
    handlers/
        main.yml
    meta/
        main.yml
    tasks/
        main.yml
    templates/
    tests/
        inventory
        test.yml
    vars/
        main.yml
```

Example 3 (unknown):
```unknown
$ ansible-galaxy init --role-skeleton=/path/to/skeleton role_name
```

Example 4 (unknown):
```unknown
[galaxy]
role_skeleton = /path/to/skeleton
role_skeleton_ignore = ^.git$,^.*/.git_keep$
```

---

## Ansible-core 2.16 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.16.html

**Contents:**
- Ansible-core 2.16 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins
- Porting custom scripts

This section discusses the behavioral changes between ansible-core 2.15 and ansible-core 2.16.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.16 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.16 Porting Guide

Noteworthy module changes

Porting custom scripts

Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.16.1, conditional expressions with embedded template blocks can fail with the message “Conditional is marked as unsafe, and cannot be evaluated.” when an embedded template consults data from untrusted sources like module results or vars marked !unsafe. Conditionals with embedded templates can be a source of malicious template injection when referencing untrusted data, and can nearly always be rewritten without embedded templates. Playbook task conditional keywords such as when and until have long displayed warnings discouraging use of embedded templates in conditionals; this warning has been expanded to non-task conditionals as well, such as the assert action.

**Examples:**

Example 1 (unknown):
```unknown
- name: task with a module result (always untrusted by Ansible)
  shell: echo "hi mom"
  register: untrusted_result

# don't do it this way...
# - name: insecure conditional with embedded template consulting untrusted data
#   assert:
#     that: '"hi mom" is in {{ untrusted_result.stdout }}'

- name: securely access untrusted values directly as Jinja variables instead
  assert:
    that: '"hi mom" is in untrusted_result.stdout'
```

---

## Templating (Jinja2) — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_templating.html

**Contents:**
- Templating (Jinja2)
- Jinja2 Example

Ansible uses Jinja2 templating to enable dynamic expressions and access to variables and facts. You can use templating with the template module. For example, you can create a template for a configuration file, then deploy that configuration file to multiple environments and supply the correct data (IP address, hostname, version) for each environment. You can also use templating in playbooks directly, by templating task names and more. You can use all the standard filters and tests included in Jinja2. Ansible includes additional specialized filters for selecting and transforming data, tests for evaluating template expressions, and Lookup plugins for retrieving data from external sources such as files, APIs, and databases for use in templating.

All templating happens on the Ansible control node before the task is sent and executed on the target machine. This approach minimizes the package requirements on the target (jinja2 is only required on the control node). It also limits the amount of data Ansible passes to the target machine. Ansible parses templates on the control node and passes only the information needed for each task to the target machine, instead of passing all the data on the control node and parsing it on the target.

Files and data used by the template module must be utf-8 encoded.

In this example, we want to write the server hostname to its /tmp/hostname.

Our directory looks like this:

An introduction to playbooks

Tips and tricks for playbooks

Jinja2 documentation, includes the syntax and semantics of the templates

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
├── hostname.yml
├── templates
    └── test.j2
```

Example 2 (unknown):
```unknown
---
- name: Write hostname
  hosts: all
  tasks:
  - name: write hostname using jinja2
    ansible.builtin.template:
       src: templates/test.j2
       dest: /tmp/hostname
```

Example 3 (unknown):
```unknown
My name is {{ ansible_facts['hostname'] }}
```

---

## Test plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/test.html

**Contents:**
- Test plugins
- Enabling test plugins
- Using test plugins
  - Using test plugins with lists
- Plugin list

Enabling test plugins

Using test plugins with lists

Test plugins evaluate template expressions and return True or False. With test plugins you can create conditionals to implement the logic of your tasks, blocks, plays, playbooks, and roles. Ansible uses the standard tests shipped as part of Jinja and adds some specialized test plugins. You can create custom Ansible test plugins.

You can add a custom test plugin by dropping it into a test_plugins directory adjacent to your play, inside a role, or by putting it in one of the test plugin directory sources configured in ansible.cfg.

You can use tests anywhere you can use templating in Ansible: in a play, in a variables file, or in a Jinja2 template for the template module. For more information on using test plugins, see Tests.

Tests always return True or False, they are always a boolean, if you need a different return type, you should be looking at filters.

You can recognize test plugins by the use of the is statement in a template, they can also be used as part of the select family of filters.

Tests will always have an _input and this is normally what is on the left side of is. Tests can also take additional parameters as you would to most programming functions. These parameters can be either positional (passed in order) or named (passed as key=value pairs). When passing both types, positional arguments should go first.

As mentioned above, one way to use tests is with the select family of filters (select, reject, selectattr, rejectattr).

You can use ansible-doc -t test -l to see the list of available plugins. Use ansible-doc -t test <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Using conditional statements

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
vars:
  is_ready: '{{ task_result is success }}'

tasks:
- name: conditionals are always in 'template' context
  action: dostuff
  when: task_result is failed
```

Example 2 (unknown):
```unknown
tasks:
- name: pass a positional parameter to match test
  action: dostuff
  when: myurl is match("https://example.com/users/.*/resources")

- name: pass named parameter to truthy test
  action: dostuff
  when: myvariable is truthy(convert_bool=True)

- name: pass both types to 'version' test
  action: dostuff
  when: sample_semver_var is version('2.0.0-rc.1+build.123', 'lt', version_type='semver')
```

Example 3 (unknown):
```unknown
# give me only defined variables from a list of variables, using 'defined' test
good_vars: "{{ all_vars|select('defined') }}"

# this uses the 'equalto' test to filter out non 'fixed' type of addresses from a list
only_fixed_addresses:  "{{ all_addresses|selectattr('type', 'equalto', 'fixed') }}"

# this does the opposite of the previous one
only_fixed_addresses:  "{{ all_addresses|rejectattr('type', 'equalto', 'fixed') }}"
```

---

## Tests — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_tests.html

**Contents:**
- Tests
- Test syntax
- Testing strings
- Vault
- Testing truthiness
- Comparing versions
- Set theory tests
- Testing if a list contains a value
- Testing if a list value is True
- Testing paths

Tests in Jinja are a way of evaluating template expressions and returning True or False. Jinja ships with many of these. See builtin tests in the official Jinja template documentation.

The main difference between tests and filters are that Jinja tests are used for comparisons, whereas filters are used for data manipulation, and have different applications in jinja. Tests can also be used in list processing filters, like map() and select() to choose items in the list.

Like all templating, tests always execute on the Ansible control node, not on the target of a task, as they test local data.

In addition to those Jinja2 tests, Ansible supplies a few more and users can easily create their own.

Testing if a list contains a value

Testing if a list value is True

Test syntax varies from filter syntax (variable | filter). Historically Ansible has registered tests as both jinja tests and jinja filters, allowing for them to be referenced using filter syntax.

As of Ansible 2.5, using a jinja test as a filter will generate a deprecation warning. As of Ansible 2.9+ using jinja test syntax is required.

The syntax for using a jinja test is as follows

To match strings against a substring or a regular expression, use the match, search or regex tests

match succeeds if it finds the pattern at the beginning of the string, while search succeeds if it finds the pattern anywhere within string. By default, regex works like search, but regex can be configured to perform other tests as well, by passing the match_type keyword argument. In particular, match_type determines the re method that gets used to perform the search. The full list can be found in the relevant Python documentation here.

All of the string tests also take optional ignorecase and multiline arguments. These correspond to re.I and re.M from Python’s re library, respectively.

You can test whether a variable is an inline single vault encrypted value using the vault_encrypted test.

As of Ansible 2.10, you can now perform Python like truthy and falsy checks.

Additionally, the truthy and falsy tests accept an optional parameter called convert_bool that will attempt to convert boolean indicators to actual booleans.

In 2.5 version_compare was renamed to version

To compare a version number, such as checking if the ansible_facts['distribution_version'] version is greater than or equal to ‘12.04’, you can use the version test.

The version test can also be used to evaluate the ansible_facts['distribution_version']

If ansible_facts['distribution_version'] is greater than or equal to 12.04, this test returns True, otherwise False.

The version test accepts the following operators

This test also accepts a 3rd parameter, strict which defines if strict version parsing as defined by ansible.module_utils.compat.version.StrictVersion should be used. The default is False (using ansible.module_utils.compat.version.LooseVersion), True enables strict version parsing

As of Ansible 2.11 the version test accepts a version_type parameter which is mutually exclusive with strict, and accepts the following values

This type corresponds to the Python distutils.version.LooseVersion class. All version formats are valid for this type. The rules for comparison are simple and predictable, but may not always give the expected results.

This type corresponds to the Python distutils.version.StrictVersion class. A version number consists of two or three dot-separated numeric components, with an optional “pre-release” tag on the end. The pre-release tag consists of a single letter ‘a’ or ‘b’ followed by a number. If the numeric components of two version numbers are equal, then one with a pre-release tag will always be deemed earlier (lesser) than one without.

This type implements the Semantic Version scheme for version comparison.

This type implements the Python PEP-440 versioning rules for version comparison. Added in version 2.14.

Using version_type to compare a semantic version would be achieved like the following

In Ansible 2.14, the pep440 option for version_type was added, and the rules of this type are defined in PEP-440. The following example showcases how this type can differentiate pre-releases as being less than a general release.

When using version in a playbook or role, don’t use {{ }} as described in the FAQ

In 2.5 issubset and issuperset were renamed to subset and superset

To see if a list includes or is included by another list, you can use ‘subset’ and ‘superset’

Ansible includes a contains test which operates similarly, but in reverse of the Jinja2 provided in test. The contains test is designed to work with the select, reject, selectattr, and rejectattr filters

You can use any and all to check if any or all elements in a list are true or not

In 2.5 the following tests were renamed to remove the is_ prefix

The following tests can provide information about a path on the control node

The human_readable and human_to_bytes functions let you test your playbooks to make sure you are using the right size format in your tasks, and that you provide Byte format to computers and human-readable format to people.

Asserts whether the given string is human-readable or not.

Returns the given string in the Bytes format.

The following tasks are illustrative of the tests meant to check the status of tasks

From 2.1, you can also use success, failure, change, and skip so that the grammar matches, for those who need to be strict about it.

When looking to determine types, it may be tempting to use the type_debug filter and compare that to the string name of that type, however, you should instead use type test comparisons, such as:

An introduction to playbooks

Conditional statements in playbooks

Playbook organization by roles

Tips and tricks for playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
variable is test_name
```

Example 2 (unknown):
```unknown
result is failed
```

Example 3 (unknown):
```unknown
vars:
  url: "https://example.com/users/foo/resources/bar"

tasks:
    - debug:
        msg: "matched pattern 1"
      when: url is match("https://example.com/users/.*/resources")

    - debug:
        msg: "matched pattern 2"
      when: url is search("users/.*/resources/.*")

    - debug:
        msg: "matched pattern 3"
      when: url is search("users")

    - debug:
        msg: "matched pattern 4"
      when: url is regex("example\.com/\w+/foo")
```

Example 4 (unknown):
```unknown
vars:
  variable: !vault |
    $ANSIBLE_VAULT;1.2;AES256;dev
    61323931353866666336306139373937316366366138656131323863373866376666353364373761
    3539633234313836346435323766306164626134376564330a373530313635343535343133316133
    36643666306434616266376434363239346433643238336464643566386135356334303736353136
    6565633133366366360a326566323363363936613664616364623437336130623133343530333739
    3039

tasks:
  - debug:
      msg: '{{ (variable is vault_encrypted) | ternary("Vault encrypted", "Not vault encrypted") }}'
```

---

## Tags — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_tags.html

**Contents:**
- Tags
- Adding tags with the tags keyword
  - Adding tags to individual tasks
    - Adding tags to handlers
    - Adding tags to blocks
    - Adding tags to plays
    - Adding tags to roles
    - Adding tags to includes
    - Adding tags to imports
    - Tag inheritance for includes: blocks and the apply keyword

If you have a large playbook, it may be useful to run only specific parts of it instead of running the entire playbook. You can do this with Ansible tags. Using tags to execute or skip selected tasks is a two-step process:

Add tags to your tasks, either individually or with tag inheritance from a block, play, role, or import.

Select or skip tags when you run your playbook.

The tags keyword is part of ‘pre processing’ the playbook and has high precedence when deciding what tasks are available to consider for execution.

Adding tags with the tags keyword

Adding tags to individual tasks

Adding tags to handlers

Adding tags to blocks

Adding tags to includes

Adding tags to imports

Tag inheritance for includes: blocks and the apply keyword

Selecting or skipping tags when you run a playbook

Previewing the results of using tags

Selectively running tagged tasks in reusable files

Tag inheritance: adding tags to multiple tasks

Configuring tags globally

You can add tags to a single task or include. You can also add tags to multiple tasks by defining them at the level of a block, play, role, or import. The keyword tags addresses all these use cases. The tags keyword always defines tags and adds them to tasks; it does not select or skip tasks for execution. You can only select or skip tasks based on tags at the command line when you run a playbook. See Selecting or skipping tags when you run a playbook for more details.

At the simplest level, you can apply one or more tags to an individual task. You can add tags to tasks in playbooks, in task files, or within a role. Here is an example that tags two tasks with different tags:

You can apply the same tag to more than one individual task. This example tags several tasks with the same tag, “ntp”:

If you ran these four tasks in a playbook with --tags ntp, Ansible would run the three tasks tagged ntp and skip the one task that does not have that tag.

Handlers are a special case of tasks that only execute when notified, as such they ignore all tags and cannot be selected for nor against.

If you want to apply a tag to many, but not all, of the tasks in your play, use a block and define the tags at that level. For example, we could edit the NTP example shown above to use a block:

Be mindful that tag selection supersedes most other logic, including block error handling. Setting a tag on a task in a block but not in the rescue or always section will prevent those from triggering if your tags selection does not cover the tasks in those sections.

This example runs all 3 tasks if called without specifying --tags but only runs the first task if you run with --tags example.

If all the tasks in a play should get the same tag, you can add the tag at the level of the play. For example, if you had a play with only the NTP tasks, you could tag the entire play:

The tasks tagged will include all implicit tasks (like fact gathering) of the play, including those added via roles.

There are three ways to add tags to roles:

Add the same tag or tags to all tasks in the role by setting tags under roles. See examples in this section.

Add the same tag or tags to all tasks in the role by setting tags on a static import_role in your playbook. See examples in Adding tags to imports.

Add a tag or tags to individual tasks or blocks within the role itself. This is the only approach that allows you to select or skip some tasks within the role. To select or skip tasks within the role, you must have tags set on individual tasks or blocks, use the dynamic include_role in your playbook, and add the same tag or tags to the include. When you use this approach, and then run your playbook with --tags foo, Ansible runs the include itself plus any tasks in the role that also have the tag foo. See Adding tags to includes for details.

When you incorporate a role in your playbook statically with the roles keyword, Ansible adds any tags you define to all the tasks in the role. For example:

When adding a tag at the role level, not only are all tasks tagged, but the role’s dependencies also have their tasks tagged. See the tag inheritance section for details.

You can apply tags to dynamic includes in a playbook. As with tags on an individual task, tags on an include_* task apply only to the include itself, not to any tasks within the included file or role. If you add mytag to a dynamic include, then run that playbook with --tags mytag, Ansible runs the include itself, runs any tasks within the included file or role tagged with mytag, and skips any tasks within the included file or role without that tag. See Selectively running tagged tasks in reusable files for more details.

You add tags to includes the same way you add tags to any other task:

You can add a tag only to the dynamic include of a role. In this example, the foo tag will not apply to tasks inside the bar role:

You can also apply a tag or tags to all the tasks imported by the static import_role and import_tasks statements:

By default, Ansible does not apply tag inheritance to dynamic reuse with include_role and include_tasks. If you add tags to an include, they apply only to the include itself, not to any tasks in the included file or role. This allows you to execute selected tasks within a role or task file - see Selectively running tagged tasks in reusable files when you run your playbook.

If you want tag inheritance, you probably want to use imports. However, using both includes and imports in a single playbook can lead to difficult-to-diagnose bugs. For this reason, if your playbook uses include_* to reuse roles or tasks, and you need tag inheritance on one include, Ansible offers two workarounds. You can use the apply keyword:

Or you can use a block:

Ansible reserves several tag names for special behavior: always, never, tagged, untagged and all. Both always and never are mostly for use in tagging the tasks themselves, the other three are used when selecting which tags to run or skip.

Ansible reserves several tag names for special behavior, two of which are always and never. If you assign the always tag to a task or play, Ansible will always run that task or play, unless you specifically skip it (--skip-tags always) or another tag defined on that task.

The internal fact gathering task is tagged with ‘always’ by default. But it can be skipped if you apply a tag to the play and you skip it directly (--skip-tags) or indirectly when you use --tags and omit it.

The role argument specification validation task is tagged with ‘always’ by default. This validation will be skipped if you use --skip-tags always.

If you assign the never tag to a task or play, Ansible skips that task or play unless you specifically request it (--tags never) or another tag defined for that task.

The rarely-used debug task in the example above only runs when you specifically request the debug or never tags.

Once you have added tags to your tasks, includes, blocks, plays, roles, and imports, you can selectively execute or skip tasks based on their tags when you run ansible-playbook. Ansible runs or skips all tasks with tags that match the tags you pass at the command line. If you have added a tag at the block or play level, with roles, or with an import, that tag applies to every task within the block, play, role, or imported role or file. If you have a role with several tags and you want to call subsets of the role at different times, either use it with dynamic includes, or split the role into multiple roles.

ansible-playbook offers five tag-related command-line options:

--tags all - run all tasks, tagged and untagged except if never (default behavior).

--tags tag1,tag2 - run only tasks with either the tag tag1 or the tag tag2 (also those tagged always).

--skip-tags tag3,tag4 - run all tasks except those with either the tag tag3 or the tag tag4 or never.

--tags tagged - run only tasks with at least one tag (never overrides).

--tags untagged - run only tasks with no tags (always overrides).

For example, to run only tasks and blocks tagged either configuration or packages in a very long playbook:

To run all tasks except those tagged packages:

To run all tasks, even those excluded because are tagged never:

Run tasks with tag1 or tag3 but skip tasks that also have tag4:

Skipping always takes precedence over explicit tags, for example, if you specify both --tags and --skip-tags the latter has precedence. For example --tags tag1,tag3,tag4 --skip-tags tag3 will only run tasks tagged with tag1 or tag4, but not with tag3, even if the task has one of the other tags.

When you run a role or playbook, you might not know or remember which tasks have which tags, or which tags exist at all. Ansible offers two command-line flags for ansible-playbook that help you manage tagged playbooks:

--list-tags - generate a list of available tags

--list-tasks - when used with --tags tagname or --skip-tags tagname, generate a preview of tagged tasks

For example, if you do not know whether the tag for configuration tasks is config or conf in a playbook, role, or tasks file, you can display all available tags without running any tasks:

If you do not know which tasks have the tags configuration and packages, you can pass those tags and add --list-tasks. Ansible lists the tasks but does not execute any of them.

These command-line flags have one limitation: they cannot show tags or tasks within dynamically included files or roles. See Comparing includes and imports: dynamic and static reuse for more information on differences between static imports and dynamic includes.

If you have a role or a tasks file with tags defined at the task or block level, you can selectively run or skip those tagged tasks in a playbook if you use a dynamic include instead of a static import. You must use the same tag on the included tasks and on the include statement itself. For example, you might create a file with some tagged and some untagged tasks:

And you might include the tasks file above in a playbook:

When you run the playbook with ansible-playbook -i hosts myplaybook.yml --tags "mytag", Ansible skips the task with no tags, runs the tagged individual task, and runs the two tasks in the block. Also it could run fact gathering (implicit task) as it is tagged with always.

If you want to apply the same tag or tags to multiple tasks without adding a tags line to every task, you can define the tags at the level of your play or block, or when you add a role or import a file. Ansible applies the tags down the dependency chain to all child tasks. With roles and imports, Ansible appends the tags set by the roles section or import to any tags set on individual tasks or blocks within the role or imported file. This is called tag inheritance. Tag inheritance is convenient because you do not have to tag every task. However, the tags still apply to the tasks individually.

With plays, blocks, the role keyword, and static imports, Ansible applies tag inheritance, adding the tags you define to every task inside the play, block, role, or imported file. However, tag inheritance does not apply to dynamic reuse with include_role and include_tasks. With dynamic reuse (includes), the tags you define apply only to the include itself. If you need tag inheritance, use a static import. If you cannot use an import because the rest of your playbook uses includes, see Tag inheritance for includes: blocks and the apply keyword for ways to work around this behavior.

You can apply tags to dynamic includes in a playbook. As with tags on an individual task, tags on an include_* task apply only to the include itself, not to any tasks within the included file or role. If you add mytag to a dynamic include, then run that playbook with --tags mytag, Ansible runs the include itself, runs any tasks within the included file or role tagged with mytag, and skips any tasks within the included file or role without that tag. See Selectively running tagged tasks in reusable files for more details.

If you run or skip certain tags by default, you can use the TAGS_RUN and TAGS_SKIP options in Ansible configuration to set those defaults.

An introduction to playbooks

Playbook organization by roles

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
tasks:
- name: Install the servers
  ansible.builtin.yum:
    name:
    - httpd
    - memcached
    state: present
  tags:
  - packages
  - webservers

- name: Configure the service
  ansible.builtin.template:
    src: templates/src.j2
    dest: /etc/foo.conf
  tags:
  - configuration
```

Example 2 (unknown):
```unknown
---
# file: roles/common/tasks/main.yml

- name: Install ntp
  ansible.builtin.yum:
    name: ntp
    state: present
  tags: ntp

- name: Configure ntp
  ansible.builtin.template:
    src: ntp.conf.j2
    dest: /etc/ntp.conf
  notify:
  - restart ntpd
  tags: ntp

- name: Enable and run ntpd
  ansible.builtin.service:
    name: ntpd
    state: started
    enabled: true
  tags: ntp

- name: Install NFS utils
  ansible.builtin.yum:
    name:
    - nfs-utils
    - nfs-util-lib
    state: present
  tags: filesharing
```

Example 3 (unknown):
```unknown
# myrole/tasks/main.yml
- name: ntp tasks
  tags: ntp
  block:
  - name: Install ntp
    ansible.builtin.yum:
      name: ntp
      state: present

  - name: Configure ntp
    ansible.builtin.template:
      src: ntp.conf.j2
      dest: /etc/ntp.conf
    notify:
    - restart ntpd

  - name: Enable and run ntpd
    ansible.builtin.service:
      name: ntpd
      state: started
      enabled: true

- name: Install NFS utils
  ansible.builtin.yum:
    name:
    - nfs-utils
    - nfs-util-lib
    state: present
  tags: filesharing
```

Example 4 (unknown):
```unknown
- block:
  - debug: msg=run with tag, but always fail
    failed_when: true
    tags: example

  rescue:
  - debug: msg=I always run because the block always fails, except if you select to only run 'example' tag

  always:
  - debug: msg=I always run, except if you select to only run 'example' tag
```

---

## Search paths in Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbook_pathing.html

**Contents:**
- Search paths in Ansible
- Config paths
- Task paths
  - Resolving local relative paths
    - Troubleshooting search paths

You can control the paths Ansible searches to find resources on your control node (including configuration, modules, roles, ssh keys, and more) as well as resources on the remote nodes you are managing. Use absolute paths to tell Ansible where to find resources whenever you can. However, absolute paths are not always practical. This page covers how Ansible interprets relative search paths, along with ways to troubleshoot when Ansible cannot find the resource you need.

Resolving local relative paths

Troubleshooting search paths

By default, these should be relative to the config file. Some are specifically relative to the current working directory or the playbook and should have this noted in their description. Things like SSH keys are left to use the current working directory because it mirrors how the underlying tools would use it.

Relative paths used in a task typically refer to remote files and directories on the managed nodes. However, paths passed to lookup plugins and some paths used in action plugins such as the “src” path for the template and copy modules refer to local files and directories on the control node.

When you specify a relative path for a local file, Ansible will try to find that file first in the current task’s role, then in other roles that included or depend on the current role, then relative to the file in which the task is defined, and finally relative to the current play. It will take the first matching file that it finds. This way, if multiple files with the same file name exist, Ansible will find the file that is closest to the current task and that is most likely to be file you wanted.

Specifically, Ansible tries to find the file in the following order:

In its appropriate subdirectory: “files”, “vars”, “templates”, or “tasks”; depending on the kind of file Ansible is searching for.

Directly in its directory.

Like 1, in the parent role that called into this current role with include_role, import_role, or with a role dependency. If the parent role has its own parent role, Ansible will repeat this step with that role.

Like 1, in the current task file’s directory.

Like 1, in the current play file’s directory.

Ansible does not search for local files in the current working directory; in other words, the directory from which you execute Ansible.

The current working directory might vary depending on the connection plugin and if the action is local or remote. For the remote it is normally the directory on which the login shell puts the user. For local it is either the directory you executed Ansible from or in some cases the playbook directory.

Search path context is additive, meaning that Ansible uses a “stack” of contexts when resolving file paths. When resolving local relative paths for files in tasks, the context of the role that includes tasks with an include_role or import_role statement gets highest precedence in the stack. If you import the tasks with include_task, or import_task statements, Ansible uses the context of the importing file.

When you execute Ansible, the variable ansible_search_path will contain the paths searched, in the order they were searched in but without listing their subdirectories. If you run Ansible in verbosity level 5 by passing the -vvvvv argument, Ansible will report each directory as it searches, except when it searches for a tasks file.

---

## Ansible Core Porting Guides — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/core_porting_guides.html

**Contents:**
- Ansible Core Porting Guides

This section lists porting guides that can help you in updating playbooks, plugins and other parts of your Ansible infrastructure from one version of ansible-core to the next.

Please note that this is not a complete list. If you believe any extra information would be useful in these pages, you can edit by clicking Edit on GitHub on the top right, or raising an issue.

---

## Advanced playbooks features — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_special_topics.html

**Contents:**
- Advanced playbooks features

This page is obsolete. Refer to the main User Guide index page for links to all playbook-related topics. Please update any links you may have made directly to this page.

---

## Ansible-core 2.11 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.11.html

**Contents:**
- Ansible-core 2.11 Porting Guide
- Playbook
- Command Line
- Deprecated
- Breaking Changes
  - Changes to AnsibleModule
  - Changes to ansible.module_utils.common.parameters
- Other
- Modules
  - Modules removed

This section discusses the behavioral changes between ansible-base 2.10 and ansible-core 2.11.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they work with this version of ansible-core.

We suggest you read this page along with the ansible-core Changelog for 2.11 to understand what updates you may need to make.

ansible-core is mainly of interest for developers and users who only want to use a small, controlled subset of the available collections. Regular users should install Ansible.

The complete list of porting guides can be found at porting guides.

Ansible-core 2.11 Porting Guide

Changes to AnsibleModule

Changes to ansible.module_utils.common.parameters

Noteworthy module changes

Porting custom scripts

The jinja2_native setting now does not affect the template module which implicitly returns strings. For the template lookup there is a new argument jinja2_native (off by default) to control that functionality. The rest of the Jinja2 expressions still operate based on the jinja2_native setting.

The ansible-galaxy login command has been removed, as the underlying API it used for GitHub auth has been shut down. Publishing roles or collections to Galaxy with ansible-galaxy now requires that a Galaxy API token be passed to the CLI using a token file (default location ~/.ansible/galaxy_token) or (insecurely) with the --token argument to ansible-galaxy.

The constant ansible.module_utils.basic._CHECK_ARGUMENT_TYPES_DISPATCHER is deprecated. Use ansible.module_utils.common.parameters.DEFAULT_TYPE_VALIDATORS instead.

With the move to ArgumentSpecValidator for performing argument spec validation, the following private methods in AnsibleModule have been removed:

_check_argument_types()

_check_argument_values()

_check_mutually_exclusive() –> ansible.module_utils.common.validation.check_mutually_exclusive()

_check_required_arguments() –> ansible.module_utils.common.validation.check_required_arguments()

_check_required_by() –> ansible.module_utils.common.validation.check_required_by()

_check_required_if() –> ansible.module_utils.common.validation.check_required_if()

_check_required_one_of() –> ansible.module_utils.common.validation.check_required_one_of()

_check_required_together() –> ansible.module_utils.common.validation.check_required_together()

_check_type_bits() –> ansible.module_utils.common.validation.check_type_bits()

_check_type_bool() –> ansible.module_utils.common.validation.check_type_bool()

_check_type_bytes() –> ansible.module_utils.common.validation.check_type_bytes()

_check_type_dict() –> ansible.module_utils.common.validation.check_type_dict()

_check_type_float() –> ansible.module_utils.common.validation.check_type_float()

_check_type_int() –> ansible.module_utils.common.validation.check_type_int()

_check_type_jsonarg() –> ansible.module_utils.common.validation.check_type_jsonarg()

_check_type_list() –> ansible.module_utils.common.validation.check_type_list()

_check_type_path() –> ansible.module_utils.common.validation.check_type_path()

_check_type_raw() –> ansible.module_utils.common.validation.check_type_raw()

_check_type_str() –> ansible.module_utils.common.validation.check_type_str()

_count_terms() –> ansible.module_utils.common.validation.count_terms()

_handle_no_log_values()

Modules or plugins using these private methods should use the public functions in ansible.module_utils.common.validation or ArgumentSpecValidator.validate() if no public function was listed above.

The following functions in ansible.module_utils.common.parameters are now private and should not be used directly. Use ArgumentSpecValidator.validate() instead.

Upgrading: If upgrading from ansible < 2.10 or from ansible-base and using pip, you must pip uninstall ansible or pip uninstall ansible-base before installing ansible-core to avoid conflicts.

Python 3.8 on the controller node is a soft requirement for this release. ansible-core 2.11 still works with the same versions of Python that ansible-base 2.10 worked with, however 2.11 emits a warning when running on a controller node with a Python version less than 3.8. This warning can be disabled by setting ANSIBLE_CONTROLLER_PYTHON_WARNING=False in your environment. ansible-core 2.12 will require Python 3.8 or greater.

The configuration system now validates the choices field, so any settings that violate it and were ignored in 2.10 cause an error in 2.11. For example, ANSIBLE_COLLECTIONS_ON_ANSIBLE_VERSION_MISMATCH=0 now causes an error (valid choices are ignore, warn or error).

The ansible-galaxy command now uses resolvelib for resolving dependencies. In most cases this should not make a user-facing difference beyond being more performant, but we note it here for posterity and completeness.

If you import Python module_utils into any modules you maintain, you may now mark the import as optional during the module payload build by wrapping the import statement in a try or if block. This allows modules to use module_utils that may not be present in all versions of Ansible or a collection, and to perform arbitrary recovery or fallback actions during module runtime.

The apt_key module has explicitly defined file as mutually exclusive with data, keyserver and url. They cannot be used together anymore.

The meta module now supports tags for user-defined tasks. Set the task’s tags to ‘always’ to maintain the previous behavior. Internal meta tasks continue to always run.

The following modules no longer exist:

facts - On NetBSD, ansible_virtualization_type now tries to report a more accurate result than xen when virtualized and not running on Xen.

facts - Virtualization facts now include virtualization_tech_guest and virtualization_tech_host keys. These are lists of virtualization technologies that a guest is a part of, or that a host provides, respectively. As an example, if you set up a host to provide both KVM and VirtualBox, both values are included in virtualization_tech_host. Similarly, a podman container running on a VM powered by KVM has a virtualization_tech_guest of ["kvm", "podman", "container"].

The parameter filter type is changed from string to list in the setup module in order to use more than one filter. Previous behavior (using a string) still remains and works as a single filter.

inventory plugins - CachePluginAdjudicator.flush() now calls the underlying cache plugin’s flush() instead of only deleting keys that it knows about. Inventory plugins should use delete() to remove any specific keys. As a user, this means that when an inventory plugin calls its clear_cache() method, facts could also be flushed from the cache. To work around this, users can configure inventory plugins to use a cache backend that is independent of the facts cache.

callback plugins - meta task execution is now sent to v2_playbook_on_task_start like any other task. By default, only explicit meta tasks are sent there. Callback plugins can opt-in to receiving internal, implicitly created tasks to act on those as well, as noted in the plugin development documentation.

The choices are now validated, so plugins that were using incorrect or incomplete choices issue an error in 2.11 if the value provided does not match. This has a simple fix: update the entries in choices to match reality.

---

## Controlling where tasks run: delegation and local actions — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_delegation.html

**Contents:**
- Controlling where tasks run: delegation and local actions
- Tasks that cannot be delegated
- Delegating tasks
- Templating in delegation context
- Delegation and parallel execution
- Delegating facts
- Local playbooks

By default, Ansible gathers facts and executes all tasks on the machines that match the hosts line of your playbook. This page shows you how to delegate tasks to a different machine or group, delegate facts to specific machines or groups, or run an entire playbook locally. Using these approaches, you can manage inter-related environments precisely and efficiently. For example, when updating your webservers, you might need to remove them from a load-balanced pool temporarily. You cannot perform this task on the webservers themselves. By delegating the task to localhost, you keep all the tasks within the same play.

Tasks that cannot be delegated

Templating in delegation context

Delegation and parallel execution

Some tasks always executed on the control node. These tasks, including include, add_host, and debug, cannot be delegated. You can determine if an action can be delegated from the connection attribute documentation. If the connection attribute indicates support is False or None, then the action does not use a connection and cannot be delegated.

If you want to perform a task on one host with the reference to other hosts, use the delegate_to keyword on a task. This is ideal for managing nodes in a load-balanced pool or for controlling outage windows. You can use delegation with the serial keyword to control the number of hosts executing at one time:

The first and third tasks in this play run on 127.0.0.1, which is the machine running Ansible. There is also a shorthand syntax that you can use on a per-task basis: local_action. Here is the same playbook as above, but using the shorthand syntax for delegating to 127.0.0.1:

You can use a local action to call ‘rsync’ to recursively copy files to the managed servers:

Note that you must have passphrase-less SSH keys or an ssh-agent configured for this to work, otherwise rsync asks for a passphrase.

To specify more arguments, use the following syntax:

The ansible_host variable and other connection variables, if present, reflects information about the host a task is delegated to, not the inventory_hostname.

The host to which a task is delegated does not inherit variables from the host that is delegating the task.

Although you can delegate_to a host that does not exist in inventory (by adding an IP address, DNS name or whatever requirement the connection plugin has), doing so does not add the host to your inventory and might cause issues. Hosts delegated to in this way do inherit variables from the “all” group (assuming VARIABLE_PRECEDENCE includes all_inventory). If you must delegate_to a non-inventory host, use the add host module.

Be advised that under delegation, the execution interpreter (normally Python), connection, become, and shell plugin options will now be templated using values from the delegated to host. All variables except inventory_hostname will now be consumed from this host and not the original task host. If you need variables from the original task host for those options, you must use hostvars[inventory_hostname]['varname'], even inventory_hostname_short refers to the delegated host.

By default, Ansible tasks are executed in parallel. Delegating a task does not change this and does not handle concurrency issues (multiple forks writing to the same file). Most commonly, users are affected by this when updating a single file on a single delegated to host for all hosts (using the copy, template, or lineinfile modules, for example). They will still operate in parallel forks (default 5) and overwrite each other.

This can be handled in several ways:

By using an intermediate play with serial: 1 or using throttle: 1 at the task level, for more detail see Controlling playbook execution: strategies and more

Delegating Ansible tasks is like delegating tasks in the real world - your groceries belong to you, even if someone else delivers them to your home. Similarly, any facts gathered by a delegated task are assigned by default to the inventory_hostname (the current host), not to the host that produced the facts (the delegated to host). To assign gathered facts to the delegated host instead of the current host, set delegate_facts to true:

This task gathers facts for the machines in the dbservers group and assigns the facts to those machines, even though the play targets the app_servers group. This way you can lookup hostvars[‘dbhost1’][‘ansible_default_ipv4’][‘address’] even though dbservers were not part of the play, or left out by using --limit.

It may be useful to use a playbook locally on a remote host, rather than by connecting over SSH. This can be useful for assuring the configuration of a system by putting a playbook in a crontab. This may also be used to run a playbook inside an OS installer, such as an Anaconda kickstart.

To run an entire playbook locally, just set the hosts: line to hosts: 127.0.0.1 and then run the playbook like so:

Alternatively, a local connection can be used in a single playbook play, even if other plays in the playbook use the default remote connection type:

If you set the connection to local and there is no ansible_python_interpreter set, modules will run under /usr/bin/python and not under {{ ansible_playbook_python }}. Be sure to set ansible_python_interpreter: “{{ ansible_playbook_python }}” in host_vars/localhost.yml, for example. You can avoid this issue by using local_action or delegate_to: localhost instead.

An introduction to playbooks

More ways to control how and where Ansible executes

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
---
- hosts: webservers
  serial: 5

  tasks:
    - name: Take out of load balancer pool
      ansible.builtin.command: /usr/bin/take_out_of_pool {{ inventory_hostname }}
      delegate_to: 127.0.0.1

    - name: Actual steps would go here
      ansible.builtin.yum:
        name: acme-web-stack
        state: latest

    - name: Add back to load balancer pool
      ansible.builtin.command: /usr/bin/add_back_to_pool {{ inventory_hostname }}
      delegate_to: 127.0.0.1
```

Example 2 (unknown):
```unknown
---
# ...

  tasks:
    - name: Take out of load balancer pool
      local_action: ansible.builtin.command /usr/bin/take_out_of_pool {{ inventory_hostname }}

# ...

    - name: Add back to load balancer pool
      local_action: ansible.builtin.command /usr/bin/add_back_to_pool {{ inventory_hostname }}
```

Example 3 (unknown):
```unknown
---
# ...

  tasks:
    - name: Recursively copy files from management server to target
      local_action: ansible.builtin.command rsync -a /path/to/files {{ inventory_hostname }}:/path/to/target/
```

Example 4 (unknown):
```unknown
---
# ...

  tasks:
    - name: Send summary mail
      local_action:
        module: community.general.mail
        subject: "Summary Mail"
        to: "{{ mail_recipient }}"
        body: "{{ mail_body }}"
      run_once: True
```

---

## Validating tasks: check mode and diff mode — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_checkmode.html

**Contents:**
- Validating tasks: check mode and diff mode
- Using check mode
  - Enforcing or preventing check mode on tasks
  - Skipping tasks or ignoring errors in check mode
- Using diff mode
  - Enforcing or preventing diff mode on tasks

Ansible provides two modes of execution that validate tasks: check mode and diff mode. These modes can be used separately or together. They are useful when you are creating or editing a playbook or role and you want to know what it will do. In check mode, Ansible runs without making any changes on remote systems. Modules that support check mode report the changes they would have made. Modules that do not support check mode report nothing and do nothing. In diff mode, Ansible provides before-and-after comparisons. Modules that support diff mode display detailed information. You can combine check mode and diff mode for detailed validation of your playbook or role.

Enforcing or preventing check mode on tasks

Skipping tasks or ignoring errors in check mode

Enforcing or preventing diff mode on tasks

Check mode is just a simulation. It will not generate output for tasks that use conditionals based on registered variables (results of prior tasks). However, it is great for validating configuration management playbooks that run on one node at a time. To run a playbook in check mode:

If you want certain tasks to run in check mode always, or never, regardless of whether you run the playbook with or without --check, you can add the check_mode option to those tasks:

To force a task to run in check mode, even when the playbook is called without --check, set check_mode: true.

To force a task to run in normal mode and make changes to the system, even when the playbook is called with --check, set check_mode: false.

Running single tasks with check_mode: true can be useful for testing Ansible modules, either to test the module itself or to test the conditions under which a module would make changes. You can register variables (see Conditionals) on these tasks for even more detail on the potential changes.

Prior to version 2.2 only the equivalent of check_mode: false existed. The notation for that was always_run: true.

If you want to skip a task or ignore errors on a task when you run Ansible in check mode, you can use a boolean magic variable ansible_check_mode, which is set to True when Ansible runs in check mode. For example:

The --diff option for ansible-playbook can be used alone or with --check. When you run in diff mode, any module that supports diff mode reports the changes made or, if used with --check, the changes that would have been made. Diff mode is most common in modules that manipulate files (for example, the template module) but other modules might also show ‘before and after’ information (for example, the user module).

Diff mode produces a large amount of output, so it is best used when checking a single host at a time. For example:

Because the --diff option can reveal sensitive information, you can disable it for a task by specifying diff: false. For example:

**Examples:**

Example 1 (unknown):
```unknown
ansible-playbook foo.yml --check
```

Example 2 (unknown):
```unknown
tasks:
  - name: This task will always make changes to the system
    ansible.builtin.command: /something/to/run --even-in-check-mode
    check_mode: false

  - name: This task will never make changes to the system
    ansible.builtin.lineinfile:
      line: "important config"
      dest: /path/to/myconfig.conf
      state: present
    check_mode: true
    register: changes_to_important_config
```

Example 3 (unknown):
```unknown
tasks:

  - name: This task will be skipped in check mode
    ansible.builtin.git:
      repo: ssh://[email protected]/mylogin/hello.git
      dest: /home/mylogin/hello
    when: not ansible_check_mode

  - name: This task will ignore errors in check mode
    ansible.builtin.git:
      repo: ssh://[email protected]/mylogin/hello.git
      dest: /home/mylogin/hello
    ignore_errors: "{{ ansible_check_mode }}"
```

Example 4 (unknown):
```unknown
ansible-playbook foo.yml --check --diff --limit foo.example.com
```

---

## Executing playbooks for troubleshooting — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_startnstep.html

**Contents:**
- Executing playbooks for troubleshooting
- start-at-task
- Step mode

When you are testing new plays or debugging playbooks, you may need to run the same play multiple times. To make this more efficient, Ansible offers two alternative ways to execute a playbook: start-at-task and step mode.

To start executing your playbook at a particular task (usually the task that failed on the previous run), use the --start-at-task option.

In this example, Ansible starts executing your playbook at a task named “install packages”. This feature does not work with tasks inside dynamically reused roles or tasks (include_*), see Comparing includes and imports: dynamic and static reuse.

To execute a playbook interactively, use --step.

With this option, Ansible stops on each task and asks if it should execute that task. For example, if you have a task called “configure ssh”, the playbook run will stop and ask.

Answer “y” to execute the task, answer “n” to skip the task, and answer “c” to exit step mode, executing all remaining tasks without asking.

An introduction to playbooks

Using the Ansible debugger

**Examples:**

Example 1 (unknown):
```unknown
ansible-playbook playbook.yml --start-at-task="install packages"
```

Example 2 (unknown):
```unknown
ansible-playbook playbook.yml --step
```

Example 3 (unknown):
```unknown
Perform task: configure ssh (y/n/c):
```

---

## ansible.builtin.import_playbook module – Import a playbook — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/import_playbook_module.html

**Contents:**
- ansible.builtin.import_playbook module – Import a playbook
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name import_playbook even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.import_playbook for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Includes a file with a list of plays to be executed.

Files with a list of plays can only be included at the top level.

You cannot use this action inside a play.

The name of the imported playbook is specified directly without any other option.

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

This is a core feature of Ansible, rather than a module, and cannot be overridden like a module.

Import a role into a play.

Load and execute a role.

Dynamically include a task list.

More information related to including and importing playbooks, roles and tasks.

Ansible Core Team (@ansible)

**Examples:**

Example 1 (unknown):
```unknown
- hosts: localhost
  tasks:
    - ansible.builtin.debug:
        msg: play1

- name: Include a play after another play
  ansible.builtin.import_playbook: otherplays.yaml

- name: Set variables on an imported playbook
  ansible.builtin.import_playbook: otherplays.yml
  vars:
    service: httpd

- name: Include a playbook from a collection
  ansible.builtin.import_playbook: my_namespace.my_collection.my_playbook

- name: This DOES NOT WORK
  hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: task1

    - name: This fails because I'm inside a play already
      ansible.builtin.import_playbook: stuff.yaml
```

---

## Lookup plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/lookup.html

**Contents:**
- Lookup plugins
- Enabling lookup plugins
- Using lookup plugins
- Forcing lookups to return lists: query and wantlist=True
- Plugin list

Enabling lookup plugins

Forcing lookups to return lists: query and wantlist=True

Lookup plugins are an Ansible-specific extension to the Jinja2 templating language. You can use lookup plugins to access data from outside sources (files, databases, key/value stores, APIs, and other services) within your playbooks. Like all templating, lookups execute and are evaluated on the Ansible control machine. Ansible makes the data returned by a lookup plugin available using the standard templating system. You can use lookup plugins to load variables or templates with information from external sources. You can create custom lookup plugins.

Lookups are executed with a working directory relative to the role or play, as opposed to local tasks, which are executed relative to the executed script.

Pass wantlist=True to lookups to use in Jinja2 template “for” loops.

By default, lookup return values are marked as unsafe for security reasons. If you trust the outside source for your lookup accesses, pass allow_unsafe=True to allow Jinja2 templates to evaluate lookup values.

Some lookups pass arguments to a shell. When using variables from a remote/untrusted source, use the |quote filter to ensure safe usage.

Ansible enables all lookup plugins it can find. You can activate a custom lookup by either dropping it into a lookup_plugins directory adjacent to your play, inside the plugins/lookup/ directory of a collection you have installed, inside a standalone role, or in one of the lookup directory sources configured in ansible.cfg.

You can use lookup plugins anywhere you can use templating in Ansible: in a play, in variables file, or a Jinja2 template for the template module. For more information on using lookup plugins, see Lookups.

Lookups are an integral part of loops. Wherever you see with_, the part after the underscore is the name of a lookup. For this reason, lookups are expected to output lists; for example, with_items uses the items lookup:

You can combine lookups with filters, tests and even each other to do some complex data generation and manipulation. For example:

You can control how errors behave in all lookup plugins by setting errors to ignore, warn, or strict. The default setting is strict, which causes the task to fail if the lookup returns an error. For example:

To ignore lookup errors:

To get a warning instead of a failure:

To get a fatal error (the default):

In Ansible 2.5, a new Jinja2 function called query was added for invoking lookup plugins. The difference between lookup and query is largely that query will always return a list. The default behavior of lookup is to return a string of comma-separated values. lookup can be explicitly configured to return a list using wantlist=True.

This feature provides an easier and more consistent interface for interacting with the new loop keyword while maintaining backward compatibility with other uses of lookup.

The following examples are equivalent:

As demonstrated above, the behavior of wantlist=True is implicit when using query.

Additionally, q was introduced as a short form of query:

You can use ansible-doc -t lookup -l to see the list of available plugins. Use ansible-doc -t lookup <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Ansible inventory plugins

Ansible callback plugins

Jinja2 filter plugins

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
vars:
  file_contents: "{{ lookup('file', 'path/to/file.txt') }}"
```

Example 2 (unknown):
```unknown
tasks:
  - name: count to 3
    debug: msg={{ item }}
    with_items: [1, 2, 3]
```

Example 3 (unknown):
```unknown
tasks:
  - name: Complicated chained lookups and filters
    debug: msg="find the answer here:\n{{ lookup('url', 'https://google.com/search/?q=' + item|urlencode)|join(' ') }}"
    with_nested:
      - "{{ lookup('consul_kv', 'bcs/' + lookup('file', '/the/question') + ', host=localhost, port=2000')|shuffle }}"
      - "{{ lookup('sequence', 'end=42 start=2 step=2')|map('log', 4)|list) }}"
      - ['a', 'c', 'd', 'c']
```

Example 4 (unknown):
```unknown
- name: if this file does not exist, I do not care .. file plugin itself warns anyway ...
  debug: msg="{{ lookup('file', '/nosuchfile', errors='ignore') }}"
```

---

## YAML Syntax — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/YAMLSyntax.html

**Contents:**
- YAML Syntax
- YAML Basics
- Gotchas

This page provides a basic overview of correct YAML syntax, which is how Ansible playbooks (our configuration management language) are expressed.

We use YAML because it is easier for humans to read and write than other common data formats like XML or JSON. Further, there are libraries available in most programming languages for working with YAML.

You may also wish to read Working with playbooks at the same time to see how this is used in practice.

For Ansible, nearly every YAML file starts with a list. Each item in the list is a list of key/value pairs, commonly called a “hash” or a “dictionary”. So, we need to know how to write lists and dictionaries in YAML.

There’s another small quirk to YAML. All YAML files (regardless of their association with Ansible or not) can optionally begin with --- and end with .... This is part of the YAML format and indicates the start and end of a document.

All members of a list are lines beginning at the same indentation level starting with a "- " (a dash and a space):

A dictionary is represented in a simple key: value form (the colon must be followed by a space):

More complicated data structures are possible, such as lists of dictionaries, dictionaries whose values are lists or a mix of both:

Dictionaries and lists can also be represented in an abbreviated form if you really want to:

These are called “Flow collections”.

Ansible doesn’t really use these too much, but you can also specify a boolean value (true/false) in several forms:

Use lowercase ‘true’ or ‘false’ for boolean values in dictionaries if you want to be compatible with default yamllint options.

Values can span multiple lines using | or >. Spanning multiple lines using a “Literal Block Scalar” | will include the newlines and any trailing spaces. Using a “Folded Block Scalar” > will fold newlines to spaces; it is used to make what would otherwise be a very long line easier to read and edit. In either case the indentation will be ignored. Examples are:

While in the above > example all newlines are folded into spaces, there are two ways to enforce a newline to be kept:

Alternatively, it can be enforced by including newline \n characters:

Let’s combine what we learned so far in an arbitrary YAML example. This really has nothing to do with Ansible, but will give you a feel for the format:

That’s all you really need to know about YAML to start writing Ansible playbooks.

While you can put just about anything into an unquoted scalar, there are some exceptions. A colon followed by a space (or newline) ": " is an indicator for a mapping. A space followed by the pound sign " #" starts a comment.

Because of this, the following is going to result in a YAML syntax error:

You will want to quote hash values using colons followed by a space or the end of the line:

…and then the colon will be preserved.

Alternatively, you can use double quotes:

The difference between single quotes and double quotes is that in double quotes you can use escapes:

The list of allowed escapes can be found in the YAML Specification under “Escape Sequences” (YAML 1.1) or “Escape Characters” (YAML 1.2).

The following is invalid YAML:

Further, Ansible uses “{{ var }}” for variables. If a value after a colon starts with a “{”, YAML will think it is a dictionary, so you must quote it, like so:

If your value starts with a quote the entire value must be quoted, not just part of it. Here are some additional examples of how to properly quote things:

In addition to ' and " there are a number of characters that are special (or reserved) and cannot be used as the first character of an unquoted scalar: [] {} > | * & ! % # ` @ ,.

You should also be aware of ? : -. In YAML, they are allowed at the beginning of a string if a non-space character follows, but YAML processor implementations differ, so it is better to use quotes.

In Flow Collections, the rules are a bit more strict:

Boolean conversion is helpful, but this can be a problem when you want a literal yes or other boolean values as a string. In these cases just use quotes:

YAML converts certain strings into floating-point values, such as the string 1.0. If you need to specify a version number (in a requirements.yml file, for example), you will need to quote the value if it looks like a floating-point value:

Learn what playbooks can do and how to write/run them.

YAML Lint (online) helps you debug YAML syntax if you are having problems

A good guide to YAML syntax

The Specification for YAML 1.1, which PyYAML and libyaml are currently implementing

For completeness, YAML 1.2 is the successor of 1.1

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
---
# A list of tasty fruits
- Apple
- Orange
- Strawberry
- Mango
...
```

Example 2 (unknown):
```unknown
# An employee record
martin:
  name: Martin D'vloper
  job: Developer
  skill: Elite
```

Example 3 (unknown):
```unknown
# Employee records
- martin:
    name: Martin D'vloper
    job: Developer
    skills:
      - python
      - perl
      - pascal
- tabitha:
    name: Tabitha Bitumen
    job: Developer
    skills:
      - lisp
      - fortran
      - erlang
```

Example 4 (unknown):
```unknown
---
martin: {name: Martin D'vloper, job: Developer, skill: Elite}
fruits: ['Apple', 'Orange', 'Strawberry', 'Mango']
```

---

## Playbook Example: Continuous Delivery and Rolling Upgrades — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/guide_rolling_upgrade.html

**Contents:**
- Playbook Example: Continuous Delivery and Rolling Upgrades
- What is continuous delivery?
- Site deployment
- Reusable content: roles
- Configuration: group variables
- The rolling upgrade
- Managing other load balancers
- Continuous delivery end-to-end

What is continuous delivery?

Reusable content: roles

Configuration: group variables

Managing other load balancers

Continuous delivery end-to-end

Continuous delivery (CD) means frequently delivering updates to your software application.

The idea is that by updating more often, you do not have to wait for a specific timed period, and your organization gets better at the process of responding to change.

Some Ansible users are deploying updates to their end users on an hourly or even more frequent basis – sometimes every time there is an approved code change. To achieve this, you need tools to be able to quickly apply those updates in a zero-downtime way.

This document describes in detail how to achieve this goal, using one of Ansible’s most complete example playbooks as a template: lamp_haproxy. This example uses a lot of Ansible features: roles, templates, and group variables, and it also comes with an orchestration playbook that can do zero-downtime rolling upgrades of the web application stack.

The playbooks deploy Apache, PHP, MySQL, Nagios, and HAProxy to a CentOS-based set of servers.

We’re not going to cover how to run these playbooks here. Read the included README in the GitHub project along with the example for that information. Instead, we’re going to take a close look at every part of the playbook and describe what it does.

Let’s start with site.yml. This is our site-wide deployment playbook. It can be used to initially deploy the site, as well as push updates to all of the servers:

If you’re not familiar with terms like playbooks and plays, you should review Working with playbooks.

In this playbook we have 5 plays. The first one targets all hosts and applies the common role to all of the hosts. This is for site-wide things like yum repository configuration, firewall configuration, and anything else that needs to apply to all of the servers.

The next four plays run against specific host groups and apply specific roles to those servers. Along with the roles for Nagios monitoring, the database, and the web application, we’ve implemented a base-apache role that installs and configures a basic Apache setup. This is used by both the sample web application and the Nagios hosts.

By now you should have a bit of understanding about roles and how they work in Ansible. Roles are a way to organize content: tasks, handlers, templates, and files, into reusable components.

This example has six roles: common, base-apache, db, haproxy, nagios, and web. How you organize your roles is up to you and your application, but most sites will have one or more common roles that are applied to all systems, and then a series of application-specific roles that install and configure particular parts of the site.

Roles can have variables and dependencies, and you can pass in parameters to roles to modify their behavior. You can read more about roles in the Roles section.

Group variables are variables that are applied to groups of servers. They can be used in templates and in playbooks to customize behavior and to provide easily-changed settings and parameters. They are stored in a directory called group_vars in the same location as your inventory. Here is lamp_haproxy’s group_vars/all file. As you might expect, these variables are applied to all of the machines in your inventory:

This is a YAML file, and you can create lists and dictionaries for more complex variable structures. In this case, we are just setting two variables, one for the port for the web server, and one for the NTP server that our machines should use for time synchronization.

Here’s another group variables file. This is group_vars/dbservers which applies to the hosts in the dbservers group:

If you look in the example, there are group variables for the webservers group and the lbservers group, similarly.

These variables are used in a variety of places. You can use them in playbooks, like this, in roles/db/tasks/main.yml:

You can also use these variables in templates, like this, in roles/common/templates/ntp.conf.j2:

You can see that the variable substitution syntax of {{ and }} is the same for both templates and variables. The syntax inside the curly braces is Jinja2, and you can do all sorts of operations and apply different filters to the data inside. In templates, you can also use for loops and if statements to handle more complex situations, like this, in roles/common/templates/iptables.j2:

This is testing to see if the inventory name of the machine we’re currently operating on (inventory_hostname) exists in the inventory group dbservers. If so, that machine will get an iptables ACCEPT line for port 3306.

Here’s another example, from the same template:

This loops over all of the hosts in the group called monitoring, and adds an ACCEPT line for each monitoring hosts’ default IPv4 address to the current machine’s iptables configuration, so that Nagios can monitor those hosts.

You can learn a lot more about Jinja2 and its capabilities here, and you can read more about Ansible variables in general in the Using variables section.

Now you have a fully-deployed site with web servers, a load balancer, and monitoring. How do you update it? This is where Ansible’s orchestration features come into play. While some applications use the term ‘orchestration’ to mean basic ordering or command-blasting, Ansible refers to orchestration as ‘conducting machines like an orchestra’, and has a pretty sophisticated engine for it.

Ansible has the capability to do operations on multi-tier applications in a coordinated way, making it easy to orchestrate a sophisticated zero-downtime rolling upgrade of our web application. This is implemented in a separate playbook, called rolling_update.yml.

Looking at the playbook, you can see it is made up of two plays. The first play is very simple and looks like this:

What’s going on here, and why are there no tasks? You might know that Ansible gathers “facts” from the servers before operating upon them. These facts are useful for all sorts of things: networking information, OS/distribution versions, and so on. In our case, we need to know something about all of the monitoring servers in our environment before we perform the update, so this simple play forces a fact-gathering step on our monitoring servers. You will see this pattern sometimes, and it is a useful trick to know.

The next part is the update play. The first part looks like this:

This is just a normal play definition, operating on the webservers group. The serial keyword tells Ansible how many servers to operate on at once. If it is not specified, Ansible will parallelize these operations up to the default “forks” limit specified in the configuration file. But for a zero-downtime rolling upgrade, you may not want to operate on that many hosts at once. If you had just a handful of webservers, you may want to set serial to 1, for one host at a time. If you have 100, maybe you could set serial to 10, for ten at a time.

Here is the next part of the update play:

The serial keyword forces the play to be executed in ‘batches’. Each batch counts as a full play with a subselection of hosts. This has some consequences on play behavior. For example, if all hosts in a batch fails, the play fails, which in turn fails the entire run. You should consider this when combining with max_fail_percentage.

The pre_tasks keyword just lets you list tasks to run before the roles are called. This will make more sense in a minute. If you look at the names of these tasks, you can see that we are disabling Nagios alerts and then removing the webserver that we are currently updating from the HAProxy load balancing pool.

The delegate_to and loop arguments, used together, cause Ansible to loop over each monitoring server and load balancer, and perform that operation (delegate that operation) on the monitoring or load balancing server, “on behalf” of the webserver. In programming terms, the outer loop is the list of web servers, and the inner loop is the list of monitoring servers.

Note that the HAProxy step looks a little complicated. We’re using HAProxy in this example because it is freely available, though if you have (for example) an F5 or Netscaler in your infrastructure (or maybe you have an AWS Elastic IP setup?), you can use Ansible modules to communicate with them instead. You might also wish to use other monitoring modules instead of nagios, but this just shows the main goal of the ‘pre tasks’ section – take the server out of monitoring, and take it out of rotation.

The next step simply re-applies the proper roles to the web servers. This will cause any configuration management declarations in web and base-apache roles to be applied to the web servers, including an update of the web application code itself. We don’t have to do it this way–we could instead just purely update the web application, but this is a good example of how roles can be used to reuse tasks:

Finally, in the post_tasks section, we reverse the changes to the Nagios configuration and put the web server back in the load balancing pool:

Again, if you were using a Netscaler or F5 or Elastic Load Balancer, you would just substitute in the appropriate modules instead.

In this example, we use the simple HAProxy load balancer to front-end the web servers. It is easy to configure and easy to manage. As we have mentioned, Ansible has support for a variety of other load balancers like Citrix NetScaler, F5 BigIP, Amazon Elastic Load Balancers, and more.

For other load balancers, you may need to send shell commands to them (like we do for HAProxy above), or call an API, if your load balancer exposes one. For the load balancers for which Ansible has modules, you may want to run them as a local_action if they contact an API. You can read more about local actions in the Controlling where tasks run: delegation and local actions section. Should you develop anything interesting for some hardware where there is not a module, it might make for a good contribution!

Now that you have an automated way to deploy updates to your application, how do you tie it all together? A lot of organizations use a continuous integration tool like Jenkins or Atlassian Bamboo to tie the development, test, release, and deploy steps together. You may also want to use a tool like Gerrit to add a code review step to commits to either the application code itself, or to your Ansible playbooks, or both.

Depending on your environment, you might be deploying continuously to a test environment, running an integration test battery against that environment, and then deploying automatically into production. Or you could keep it simple and just use the rolling-update for on-demand deployment into test or production specifically. This is all up to you.

For integration with Continuous Integration systems, you can easily trigger playbook runs using the ansible-playbook command line tool, or, if you’re using AWX, the tower-cli command or the built-in REST API. (The tower-cli command ‘joblaunch’ will spawn a remote job over the REST API and is pretty slick).

This should give you a good idea of how to structure a multi-tier application with Ansible and orchestrate operations upon that app, with the eventual goal of continuous delivery to your customers. You could extend the idea of the rolling upgrade to several different parts of the app; maybe add front-end web servers along with application servers, or replace the SQL database with NoSQL database. Ansible gives you the capability to easily manage complicated environments and automate common operations.

An introduction to playbooks

An introduction to playbook roles

An introduction to Ansible variables

An introduction to Continuous Delivery with Ansible

**Examples:**

Example 1 (unknown):
```unknown
---
# This playbook deploys the whole application stack in this site.

# Apply common configuration to all hosts
- hosts: all

  roles:
  - common

# Configure and deploy database servers.
- hosts: dbservers

  roles:
  - db

# Configure and deploy the web servers. Note that we include two roles
# here, the 'base-apache' role which simply sets up Apache, and 'web'
# which includes our example web application.

- hosts: webservers

  roles:
  - base-apache
  - web

# Configure and deploy the load balancer(s).
- hosts: lbservers

  roles:
  - haproxy

# Configure and deploy the Nagios monitoring node(s).
- hosts: monitoring

  roles:
  - base-apache
  - nagios
```

Example 2 (unknown):
```unknown
---
httpd_port: 80
ntpserver: 192.0.2.23
```

Example 3 (unknown):
```unknown
---
mysqlservice: mysqld
mysql_port: 3306
dbuser: root
dbname: foodb
upassword: usersecret
```

Example 4 (unknown):
```unknown
- name: Create Application Database
  mysql_db:
    name: "{{ dbname }}"
    state: present

- name: Create Application DB User
  mysql_user:
    name: "{{ dbuser }}"
    password: "{{ upassword }}"
    priv: "*.*:ALL"
    host: '%'
    state: present
```

---

## Working with playbooks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks.html

**Contents:**
- Working with playbooks

Playbooks record and execute Ansible’s configuration, deployment, and orchestration functions. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT process.

If Ansible modules are the tools in your workshop, playbooks are your instruction manuals, and your inventory of hosts is your raw material.

At a basic level, playbooks can be used to manage configurations of and deployments to remote machines. At a more advanced level, they can sequence multi-tier rollouts involving rolling updates and can delegate actions to other hosts, interacting with monitoring servers and load balancers along the way.

Playbooks are designed to be human-readable and are developed in a basic text language. There are multiple ways to organize playbooks and the files they include, and we’ll offer up some suggestions on that and making the most out of Ansible.

---

## Ansible-core 2.18 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.18.html

**Contents:**
- Ansible-core 2.18 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
- Plugins
- Porting custom scripts

This section discusses the behavioral changes between ansible-core 2.17 and ansible-core 2.18.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.18 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.18 Porting Guide

Noteworthy module changes

Porting custom scripts

Python 3.10 is a no longer supported control node version. Python 3.11+ is now required for running Ansible.

Python 3.7 is a no longer supported remote version. Python 3.8+ is now required for target execution.

The following modules no longer exist:

The ssh connection plugin now officially supports targeting Windows hosts. A breaking change that has been made as part of this official support is the low level command execution done by plugins like ansible.builtin.raw and action plugins calling _low_level_execute_command is no longer wrapped with a powershell.exe wrapped invocation. These commands will now be executed directly on the target host using the default shell configuration set on the Windows host. This change is done to simplify the configuration required on the Ansible side, make module execution more efficient, and to remove the need to decode stderr CLIXML output. A consequence of this change is that ansible.builtin.raw commands are no longer guaranteed to be run through a PowerShell shell and with the output encoding of UTF-8. To run a command through PowerShell and with UTF-8 output support, use the ansible.windows.win_shell or ansible.windows.win_powershell module instead.

**Examples:**

Example 1 (unknown):
```unknown
- name: Run with win_shell
  ansible.windows.win_shell: Write-Host "Hello, Café"

- name: Run with win_powershell
  ansible.windows.win_powershell:
    script: Write-Host "Hello, Café"
```

---

## Asynchronous actions and polling — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_async.html

**Contents:**
- Asynchronous actions and polling
- Asynchronous ad hoc tasks
- Asynchronous playbook tasks
  - Avoid connection timeouts: poll > 0
  - Run tasks concurrently: poll = 0

By default, Ansible runs tasks synchronously, holding the connection to the remote node open until the action is completed. This means that, within a playbook, each task blocks the next task by default, and subsequent tasks will not run until the current task is completed. This behavior can create challenges. For example, a task may take longer to complete than the SSH session allows for, causing a timeout. Or you may want a long-running process to execute in the background while you perform other tasks concurrently. Asynchronous mode lets you control how long-running tasks are executed.

Asynchronous ad hoc tasks

Asynchronous playbook tasks

Avoid connection timeouts: poll > 0

Run tasks concurrently: poll = 0

You can execute long-running operations in the background with ad hoc tasks. For example, to execute long_running_operation asynchronously in the background, with a timeout (-B) of 3600 seconds, and without polling (-P):

To check on the job status later, use the async_status module, passing it the job ID that was returned when you ran the original job in the background:

Ansible can also check on the status of your long-running job automatically with polling. In most cases, Ansible will keep the connection to your remote node open between polls. To run for 30 minutes and poll for status every 60 seconds:

Poll mode is smart so all jobs will be started before polling begins on any machine. Be sure to use a high enough --forks value if you want to get all of your jobs started very quickly. After the time limit (in seconds) runs out (-B), the process on the remote nodes will be terminated.

Asynchronous mode is best suited to long-running shell commands or software upgrades. Running the copy module asynchronously, for example, does not do a background file transfer.

Playbooks also support asynchronous mode and polling, with a simplified syntax. You can use asynchronous mode in playbooks to avoid connection timeouts or to avoid blocking subsequent tasks. The behavior of asynchronous mode in a playbook depends on the value of poll.

If you want to set a longer timeout limit for a certain task in your playbook, use async with poll set to a positive value. Ansible will still block the next task in your playbook, waiting until the async task either completes, fails or times out. However, the task will only time out if it exceeds the timeout limit you set with the async parameter.

To avoid timeouts on a task, specify its maximum runtime and how frequently you would like to poll for status:

The default poll value is set by the DEFAULT_POLL_INTERVAL setting. There is no default for the async time limit. If you leave off the ‘async’ keyword, the task runs synchronously, which is Ansible’s default.

As of Ansible 2.3, async does not support check mode and will fail the task when run in check mode. See Validating tasks: check mode and diff mode on how to skip a task in check mode.

When an async task completes with polling enabled, the temporary async job cache file (by default in ~/.ansible_async/) is automatically removed.

If you want to run multiple tasks in a playbook concurrently, use async with poll set to 0. When you set poll: 0, Ansible starts the task and immediately moves on to the next task without waiting for a result. Each async task runs until it either completes, fails or times out (runs longer than its async value). The playbook run ends without checking back on async tasks.

To run a playbook task asynchronously:

Do not specify a poll value of 0 with operations that require exclusive locks (such as yum transactions) if you expect to run other commands later in the playbook against those same resources.

Using a higher value for --forks will result in kicking off asynchronous tasks even faster. This also increases the efficiency of polling.

When running with poll: 0, Ansible will not automatically clean up the async job cache file. You will need to manually clean this up with the async_status module with mode: cleanup.

If you need a synchronization point with an async task, you can register it to obtain its job ID and use the async_status module to observe it in a later task. For example:

If the value of async: is not high enough, this will cause the “check on it later” task to fail because the temporary status file that the async_status: is looking for will not have been written or no longer exist

Asynchronous playbook tasks always return changed. If the task is using a module that requires the user to annotate changes with changed_when, creates, and so on, then those should be added to the following async_status task.

To run multiple asynchronous tasks while limiting the number of tasks running concurrently:

Options for controlling playbook execution

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
$ ansible all -B 3600 -P 0 -a "/usr/bin/long_running_operation --do-stuff"
```

Example 2 (unknown):
```unknown
$ ansible web1.example.com -m async_status -a "jid=488359678239.2844"
```

Example 3 (unknown):
```unknown
$ ansible all -B 1800 -P 60 -a "/usr/bin/long_running_operation --do-stuff"
```

Example 4 (unknown):
```unknown
---

- hosts: all
  remote_user: root

  tasks:

  - name: Simulate long running op (15 sec), wait for up to 45 sec, poll every 5 sec
    ansible.builtin.command: /bin/sleep 15
    async: 45
    poll: 5
```

---

## Integration tests — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_integration.html

**Contents:**
- Integration tests
- Quick Start
- Configuration
  - ansible-test command
  - integration_config.yml
- Prerequisites
- Non-destructive Tests
- Destructive Tests
- Windows Tests
- Tests in containers

integration_config.yml

Non-destructive Tests

Running Integration Tests

Other configuration for Cloud Tests

Other Definitions required

Where to find out more

The Ansible integration Test system.

Tests for playbooks, by playbooks.

Some tests may require credentials. Credentials may be specified with credentials.yml.

Some tests may require root.

Every new module and plugin should have integration tests, even if the tests cannot be run on Ansible CI infrastructure. In this case, the tests should be marked with the unsupported alias in aliases file.

It is highly recommended that you install and activate the argcomplete Python package. It provides tab completion in bash for the ansible-test test runner.

The example below assumes bin/ is in your $PATH. An easy way to achieve that is to initialize your environment with the env-setup command:

You can also call ansible-test with the full path:

Making your own version of integration_config.yml can allow for setting some tunable parameters to help run the tests better in your environment. Some tests (for example, cloud tests) will only run when access credentials are provided. For more information about supported credentials, refer to the various cloud-config-*.template files in the tests/integration/ directory.

Some tests assume things like hg, svn, and git are installed, and in path. Some tests (such as those for Amazon Web Services) need separate definitions, which will be covered later in this document.

(Complete list pending)

These tests will modify files in subdirectories, but will not do things that install or remove packages or things outside of those test subdirectories. They will also not reconfigure or bounce system services.

Running integration tests within containers

To protect your system from any potential changes caused by integration tests, and to ensure a sensible set of dependencies are available we recommend that you always run integration tests with the --docker option, for example --docker ubuntu2204. Get the list of supported container images by running ansible-test integration --help. You can find them in the target docker images section of the output. The default image is used for sanity and unit tests, as well as for platform independent integration tests such as those for cloud modules.

Run as follows for all POSIX platform tests executed by our CI system in a Fedora 34 container:

You can exclude a specific test as well, such as for individual modules:

You can target a specific test as well, such as for individual modules:

You can use the -v option to make the output more verbose:

Use the following command to list all the available targets:

If you use bash with argcomplete, obtain a full list by doing: ansible-test integration <tab><tab>

These tests are allowed to install and remove some trivial packages. You will likely want to devote these to a virtual environment, such as Docker. They won’t reformat your filesystem:

These tests exercise the winrm connection plugin and Windows modules. You’ll need to define an inventory with a remote Windows Server to use for testing, and enable PowerShell Remoting to continue.

Running these tests may result in changes to your Windows host, so don’t run them against a production/critical Windows environment.

Enable PowerShell Remoting (run on the Windows host by a Remote Desktop):

Define Windows inventory:

Run the Windows tests executed by our CI system:

If you have a Linux system with Docker or Podman installed, running integration tests using the same containers used by the Ansible continuous integration (CI) system is recommended.

By default, Podman will only be used if the Docker CLI is not installed. If you have Docker installed but want to use Podman, you can change this behavior by setting the environment variable ANSIBLE_TEST_PREFER_PODMAN.

Using Docker Engine to run Docker on a non-Linux host (such as macOS) is not recommended. Some tests may fail, depending on the image used for testing. Using the --docker-privileged option when running integration (not network-integration or windows-integration) may resolve the issue.

To run all CI integration test targets for POSIX platforms in a Ubuntu 18.04 container:

You can also run specific tests or select a different Linux distribution. For example, to run tests for the ping module on a Ubuntu 18.04 container:

Container images are updated regularly. To see the current list of container images:

The list is under the target docker images and supported python version heading.

To run some tests, you must provide access credentials in a file named cloud-config-aws.yml or cloud-config-cs.ini in the tests/integration directory. Corresponding .template files are available for syntax help. The newer AWS tests now use the file tests/integration/cloud-config-aws.yml.

Ansible needs fairly wide ranging powers to run the tests in an AWS account. These rights can be provided to a dedicated user. These need to be configured before running the test.

The GitHub repository mattclay/aws-terminator contains two sets of policies used for all existing AWS module integration tests. The hacking/aws_config/setup_iam.yml playbook can be used to setup two groups:

ansible-integration-ci will have the policies applied necessary to run any integration tests not marked as unsupported and are designed to mirror those used by Ansible’s CI.

ansible-integration-unsupported will have the additional policies applied necessary to run the integration tests marked as unsupported including tests for managing IAM roles, users and groups.

Once the groups have been created, you’ll need to create a user and make the user a member of these groups. The policies are designed to minimize the rights of that user. Please note that while this policy does limit the user to one region, this does not fully restrict the user (primarily due to the limitations of the Amazon ARN notation). The user will still have wide privileges for viewing account definitions, and will also be able to manage some resources that are not related to testing (for example, AWS lambdas with different names). Tests should not be run in a primary production account in any case.

Apart from installing the policy and giving it to the user identity running the tests, a lambda role ansible_integration_tests has to be created which has lambda basic execution privileges.

For guidance on writing network test see Resource module integration tests.

If you’d like to know more about the plans for improving testing Ansible, join the Ansible community forum

**Examples:**

Example 1 (unknown):
```unknown
source hacking/env-setup
ansible-test --help
```

Example 2 (unknown):
```unknown
bin/ansible-test --help
```

Example 3 (unknown):
```unknown
ansible-test integration shippable/ --docker fedora34
```

Example 4 (unknown):
```unknown
ansible-test integration --exclude git
```

---

## General tips — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/tips_tricks/ansible_tips_tricks.html

**Contents:**
- General tips
- Keep it simple
- Use version control
- Customize the CLI output
- Avoid configuration-dependent content
- Playbook tips
- Use whitespace
- Always name plays, tasks, and blocks
- Always mention the state
- Use comments

These concepts apply to all Ansible activities and artifacts.

Whenever you can, do things simply.

Use advanced features only when necessary, and select the feature that best matches your use case. For example, you will probably not need vars, vars_files, vars_prompt and --extra-vars all at once, while also using an external inventory file.

If something feels complicated, it probably is. Take the time to look for a simpler solution.

Keep your playbooks, roles, inventory, and variables files in git or another version control system and make commits with meaningful comments to the repository when you make changes. Version control gives you an audit trail describing when and why you changed the rules that automate your infrastructure.

You can change the output from Ansible CLI commands using Callback plugins.

To ensure that your automation project is easy to understand, modify, and share with others, you should avoid configuration-dependent content. For example, rather than referencing an ansible.cfg as the root of a project, you can use magic variables such as playbook_dir or role_name to determine paths relative to known locations within your project directory. This can help to keep automation content flexible, reusable, and easy to maintain. For more information, see special variables.

These tips help make playbooks and roles easier to read, maintain, and debug.

Generous use of whitespace, for example, a blank line before each block or task, makes a playbook easy to scan.

Play, task, and block - name:’s are optional, but extremely useful. In its output, Ansible shows you the name of each named entity it runs. Choose names that describe what each play, task, and block does and why.

For many modules, the state parameter is optional.

Different modules have different default settings for state, and some modules support several state settings. Explicitly setting state: present or state: absent makes playbooks and roles clearer.

Even with task names and explicit states, sometimes a part of a playbook or role (or inventory/variable file) needs more explanation. Adding a comment (any line starting with #) helps others (and possibly yourself in the future) understand what a play or task (or variable setting) does, how it does it, and why.

Use fully qualified collection names (FQCN) to avoid ambiguity in which collection to search for the correct module or plugin for each task.

For builtin modules and plugins, use the ansible.builtin collection name as a prefix, for example, ansible.builtin.copy.

These tips help keep your inventory well organized.

With cloud providers and other systems that maintain canonical lists of your infrastructure, use dynamic inventory to retrieve those lists instead of manually updating static inventory files. With cloud resources, you can use tags to differentiate production and staging environments.

A system can be in multiple groups. See How to build your inventory and Patterns: targeting hosts and groups. If you create groups named for the function of the nodes in the group, for example, webservers or dbservers, your playbooks can target machines based on function. You can assign function-specific variables using the group variable system, and design Ansible roles to handle function-specific use cases. See Roles.

You can keep your production environment separate from development, test, and staging environments by using separate inventory files or directories for each environment. This way you pick with -i what you are targeting. Keeping all your environments in one file can lead to surprises! For example, all vault passwords used in an inventory need to be available when using that inventory. If an inventory contains both production and development environments, developers using that inventory would be able to access production secrets.

You should encrypt sensitive or secret variables with Ansible Vault. However, encrypting the variable names as well as the variable values makes it hard to find the source of the values. To circumvent this, you can encrypt the variables individually using ansible-vault encrypt_string, or add the following layer of indirection to keep the names of your variables accessible (by grep, for example) without exposing any secrets:

Create a group_vars/ subdirectory named after the group.

Inside this subdirectory, create two files named vars and vault.

In the vars file, define all of the variables needed, including any sensitive ones.

Copy all of the sensitive variables over to the vault file and prefix these variables with vault_.

Adjust the variables in the vars file to point to the matching vault_ variables using jinja2 syntax: db_password: "{{ vault_db_password }}".

Encrypt the vault file to protect its contents.

Use the variable name from the vars file in your playbooks.

When running a playbook, Ansible finds the variables in the unencrypted file, which pulls the sensitive variable values from the encrypted file. There is no limit to the number of variable and vault files or their names.

Note that using this strategy in your inventory still requires all vault passwords to be available (for example for ansible-playbook or AWX/Ansible Tower) when run with that inventory.

These tips apply to using Ansible, rather than to Ansible artifacts.

Reduce complexity with portable container images known as Execution Environments.

Testing changes in a staging environment before rolling them out in production is always a great idea. Your environments need not be the same size, and you can use group variables to control the differences between environments. You can also check for any syntax errors in the staging environment using the flag --syntax-check such as in the following example:

Use the serial keyword to control how many machines you update at once in the batch. See Controlling where tasks run: delegation and local actions.

Group variables files and the group_by module work together to help Ansible execute across a range of operating systems and distributions that require different settings, packages, and tools. The group_by module creates a dynamic group of hosts that match certain criteria. This group does not need to be defined in the inventory file. This approach lets you execute different tasks on different operating systems or distributions.

For example, the following play categorizes all systems into dynamic groups based on the operating system name:

Subsequent plays can use these groups as patterns on the hosts line as follows:

You can also add group-specific settings in group vars files. In the following example, CentOS machines get the value of ‘42’ for asdf but other machines get ‘10’. You can also use group vars files to apply roles to systems as well as set variables.

All three names must match: the name created by the group_by task, the name of the pattern in subsequent plays, and the name of the group vars file.

You can use the same setup with include_vars when you only need OS-specific variables, not tasks:

This pulls in variables from the group_vars/os_CentOS.yml file.

Learn about YAML syntax

Review the basic playbook features

Browse existing collections, modules, and plugins

Learn how to extend Ansible by writing your own modules

Learn about how to select hosts

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
ansible-playbook --syntax-check
```

Example 2 (unknown):
```unknown
- name: Talk to all hosts just so we can learn about them
  hosts: all
  tasks:

    - name: Classify hosts depending on their OS distribution
      ansible.builtin.group_by:
        key: os_{{ ansible_facts['distribution'] }}
```

Example 3 (unknown):
```unknown
- hosts: os_CentOS
  gather_facts: False
  tasks:

    # Tasks for CentOS hosts only go in this play.
    - name: Ping my CentOS hosts
      ansible.builtin.ping:
```

Example 4 (unknown):
```unknown
---
# file: group_vars/all
asdf: 10

---
# file: group_vars/os_CentOS.yml
asdf: 42
```

---

## ansible.builtin.junit callback – write playbook output to a JUnit file. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/junit_callback.html

**Contents:**
- ansible.builtin.junit callback – write playbook output to a JUnit file.
- Callback plugin
- Synopsis
- Requirements
- Parameters
  - Collection links

This callback plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name junit. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.junit for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same callback plugin name.

This plugin is an aggregate callback. It adds additional console output next to the configured stdout callback. See Callback plugins for more information on callback plugins.

This callback writes playbook output to a JUnit formatted XML file.

Tasks show up in the report as follows: ‘ok’: pass ‘failed’ with ‘EXPECTED FAILURE’ in the task name: pass ‘failed’ with ‘TOGGLE RESULT’ in the task name: pass ‘ok’ with ‘TOGGLE RESULT’ in the task name: failure ‘failed’ due to an exception: error ‘failed’ for other reasons: failure ‘skipped’: skipped

The below requirements are needed on the local controller node that executes this callback.

enable in configuration

Consider any tasks reporting “changed” as a junit test failure

Environment variable: JUNIT_FAIL_ON_CHANGE

Consider failed tasks as a junit test failure even if ignore_on_error is set

Environment variable: JUNIT_FAIL_ON_IGNORE

Hide the arguments for a task

Environment variable: JUNIT_HIDE_TASK_ARGUMENTS

include_setup_tasks_in_report

Should the setup tasks be included in the final report

Environment variable: JUNIT_INCLUDE_SETUP_TASKS_IN_REPORT

Directory to write XML files to.

Default: "~/.ansible.log"

Environment variable: JUNIT_OUTPUT_DIR

replace_out_of_tree_path

added in ansible-core 2.12.3

Replace the directory portion of an out-of-tree relative task path with the given placeholder

Environment variable: JUNIT_REPLACE_OUT_OF_TREE_PATH

Configure the output to be one class per yaml file

Environment variable: JUNIT_TASK_CLASS

Configure the output to use relative paths to given directory

Environment variable: JUNIT_TASK_RELATIVE_PATH

Consider a task only as test case if it has this value as prefix. Additionally failing tasks are recorded as failed test cases.

Environment variable: JUNIT_TEST_CASE_PREFIX

---

## Executing playbooks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_execution.html

**Contents:**
- Executing playbooks

Ready to run your Ansible playbook?

Running complex playbooks requires some trial and error so learn about some of the abilities that Ansible gives you to ensure successful execution. You can validate your tasks with “dry run” playbooks, use the start-at-task and step mode options to efficiently troubleshoot playbooks. You can also use Ansible debugger to correct tasks during execution. Ansible also offers flexibility with asynchronous playbook execution and tags that let you run specific parts of your playbook.

---

## Discovering variables: facts and magic variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_vars_facts.html

**Contents:**
- Discovering variables: facts and magic variables
- Ansible facts
  - Package requirements for fact gathering
  - Caching facts
  - Disabling facts
  - Adding custom facts
    - facts.d or local facts
- Information about Ansible: magic variables
  - Ansible version

With Ansible you can retrieve or discover certain variables containing information about your remote systems or about Ansible itself. Variables related to remote systems are called facts. With facts, you can use the behavior or state of one system as a configuration on other systems. For example, you can use the IP address of one system as a configuration value on another system. Variables related to Ansible are called magic variables.

Package requirements for fact gathering

facts.d or local facts

Information about Ansible: magic variables

Ansible facts are data related to your remote systems, including operating systems, IP addresses, attached filesystems, and more. You can access this data in the ansible_facts variable. By default, you can also access some Ansible facts as top-level variables with the ansible_ prefix. You can disable this behavior using the INJECT_FACTS_AS_VARS setting. To see all available facts, add this task to a play:

If you have already created an inventory and configured working SSH credentials, you can see the ‘raw’ information for any host in your inventory by running this ad-hoc ansible command at the command line:

Facts include a large amount of variable data, which may look like this:

You can reference the model of the first disk in the facts shown above in a template or playbook as:

To reference the system hostname:

Note that ansible_ prefix shown in the setup module output is not used when addressing these variables.

You can use facts in conditionals (see Conditionals) and also in templates. You can also use facts to create dynamic groups of hosts that match particular criteria, see the group_by module documentation for details.

Because ansible_date_time is created and cached when Ansible gathers facts before each playbook run, it can get stale with long-running playbooks. If your playbook takes a long time to run, use the pipe filter (for example, lookup('pipe', 'date +%Y-%m-%d.%H:%M:%S')) or now() with a Jinja 2 template instead of ansible_date_time.

On some distros, you may see missing fact values or facts set to default values because the packages that support gathering those facts are not installed by default. You can install the necessary packages on your remote hosts using the OS package manager. Known dependencies include:

Linux Network fact gathering - Depends on the ip binary, commonly included in the iproute2 package.

Like registered variables, facts are stored in memory by default. However, unlike registered variables, facts can be gathered independently and cached for repeated use. With cached facts, you can refer to facts from one system when configuring a second system, even if Ansible executes the current play on the second system first. For example:

Caching is controlled by the cache plugins. By default, Ansible uses the memory cache plugin, which stores facts in memory for the duration of the current playbook run. To retain Ansible facts for repeated use, select a different cache plugin. See Cache plugins for details.

Fact caching can improve performance. If you manage thousands of hosts, you can configure fact caching to run nightly, and then manage configuration on a smaller set of servers periodically throughout the day. With cached facts, you have access to variables and information about all hosts even when you are only managing a small number of servers.

By default, Ansible gathers facts at the beginning of each play. If you do not need to gather facts (for example, if you know everything about your systems centrally), you can turn off fact gathering at the play level to improve scalability. Disabling facts may particularly improve performance in push mode with very large numbers of systems, or if you are using Ansible on experimental platforms. To disable fact gathering:

The setup module in Ansible automatically discovers a standard set of facts about each host. If you want to add custom values to your facts, you can write a custom facts module, set temporary facts with a ansible.builtin.set_fact task, or provide permanent custom facts using the facts.d directory.

You can add static custom facts by adding static files to facts.d, or add dynamic facts by adding executable scripts to facts.d. For example, you can add a list of all users on a host to your facts by creating and running a script in facts.d.

To use facts.d, create an /etc/ansible/facts.d directory on the remote host or hosts. If you prefer a different directory, create it and specify it using the fact_path play keyword. Add files to the directory to supply your custom facts. All file names must end with .fact. The files can be JSON, INI, or executable files returning JSON.

To add static facts, simply add a file with the .fact extension. For example, create /etc/ansible/facts.d/preferences.fact with this content:

Make sure the file is not executable as this will break the ansible.builtin.setup module.

The next time fact gathering runs, your facts will include a hash variable fact named general with asdf and bar as members. To validate this, run the following:

And you will see your custom fact added:

The ansible_local namespace separates custom facts created by facts.d from system facts or variables defined elsewhere in the playbook, so variables will not override each other. You can access this custom fact in a template or playbook as:

The key part in the key=value pairs will be converted into lowercase inside the ansible_local variable. Using the example above, if the ini file contained XYZ=3 in the [general] section, then you should expect to access it as: {{ ansible_local['preferences']['general']['xyz'] }} and not {{ ansible_local['preferences']['general']['XYZ'] }}. This is because Ansible uses Python’s ConfigParser which passes all option names through the optionxform method and this method’s default implementation converts option names to lowercase.

You can also use facts.d to execute a script on the remote host, generating dynamic custom facts to the ansible_local namespace. For example, you can generate a list of all users that exist on a remote host as a fact about that host. To generate dynamic custom facts using facts.d:

Write and test a script to generate the JSON data you want.

Save the script in your facts.d directory.

Make sure your script has the .fact file extension.

Make sure your script is executable by the Ansible connection user.

Gather facts to execute the script and add the JSON output to ansible_local.

By default, fact gathering runs once at the beginning of each play. If you create a custom fact using facts.d in a playbook, it will be available in the next play that gathers facts. If you want to use it in the same play where you created it, you must explicitly re-run the setup module. For example:

If you use this pattern frequently, a custom facts module would be more efficient than facts.d.

You can access information about Ansible operations, including the Python version being used, the hosts and groups in inventory, and the directories for playbooks and roles, using “magic” variables. Like connection variables, magic variables are Special Variables. Magic variable names are reserved - do not set variables with these names. The variable environment is also reserved.

The most commonly used magic variables are hostvars, groups, group_names, and inventory_hostname. With hostvars, you can access variables defined for any host in the play, at any point in a playbook. You can access Ansible facts using the hostvars variable too, but only after you have gathered (or cached) facts. Note that variables defined at play objects are not defined for specific hosts and therefore are not mapped to hostvars.

If you want to configure your database server using the value of a ‘fact’ from another node, or the value of an inventory variable assigned to another node, you can use hostvars in a template or on an action line:

With groups, a list of all the groups (and hosts) in the inventory, you can enumerate all hosts within a group. For example:

You can use groups and hostvars together to find all the IP addresses in a group.

You can use this approach to point a frontend proxy server to all the hosts in your app servers group, to set up the correct firewall rules between servers, and so on. You must either cache facts or gather facts for those hosts before the task that fills out the template.

With group_names, a list (array) of all the groups the current host is in, you can create templated files that vary based on the group membership (or role) of the host:

You can use the magic variable inventory_hostname, the name of the host as configured in your inventory, as an alternative to ansible_hostname when fact-gathering is disabled. If you have a long FQDN, you can use inventory_hostname_short, which contains the part up to the first period, without the rest of the domain.

Other useful magic variables refer to the current play or playbook. These vars may be useful for filling out templates with multiple hostnames or for injecting the list into the rules for a load balancer.

ansible_play_hosts is the list of all hosts still active in the current play.

ansible_play_batch is a list of hostnames that are in scope for the current ‘batch’ of the play.

The batch size is defined by serial, when not set it is equivalent to the whole play (making it the same as ansible_play_hosts).

ansible_playbook_python is the path to the Python executable used to invoke the Ansible command line tool.

inventory_dir is the pathname of the directory holding Ansible’s inventory host file.

inventory_file is the pathname and the file name pointing to the Ansible’s inventory host file.

playbook_dir contains the playbook base directory.

role_path contains the current role’s pathname and only works inside a role.

ansible_check_mode is a boolean, set to True if you run Ansible with --check.

To adapt playbook behavior to different versions of Ansible, you can use the variable ansible_version, which has the following structure:

**Examples:**

Example 1 (unknown):
```unknown
- name: Print all available facts
  ansible.builtin.debug:
    var: ansible_facts
```

Example 2 (unknown):
```unknown
ansible <hostname> -m ansible.builtin.setup
```

Example 3 (unknown):
```unknown
{
    "ansible_all_ipv4_addresses": [
        "REDACTED IP ADDRESS"
    ],
    "ansible_all_ipv6_addresses": [
        "REDACTED IPV6 ADDRESS"
    ],
    "ansible_apparmor": {
        "status": "disabled"
    },
    "ansible_architecture": "x86_64",
    "ansible_bios_date": "11/28/2013",
    "ansible_bios_version": "4.1.5",
    "ansible_cmdline": {
        "BOOT_IMAGE": "/boot/vmlinuz-3.10.0-862.14.4.el7.x86_64",
        "console": "ttyS0,115200",
        "no_timer_check": true,
        "nofb": true,
        "nomodeset": true,
        "ro": true,
        "root": "LABEL=cloudimg-rootfs",
        "vga": "normal"
    },
    "ansible_date_time": {
        "date": "2018-10-25",
        "day": "25",
        "epoch": "1540469324",
        "hour": "12",
        "iso8601": "2018-10-25T12:08:44Z",
        "iso8601_basic": "20181025T120844109754",
        "iso8601_basic_short": "20181025T120844",
        "iso8601_micro": "2018-10-25T12:08:44.109968Z",
        "minute": "08",
        "month": "10",
        "second": "44",
        "time": "12:08:44",
        "tz": "UTC",
        "tz_offset": "+0000",
        "weekday": "Thursday",
        "weekday_number": "4",
        "weeknumber": "43",
        "year": "2018"
    },
    "ansible_default_ipv4": {
        "address": "REDACTED",
        "alias": "eth0",
        "broadcast": "REDACTED",
        "gateway": "REDACTED",
        "interface": "eth0",
        "macaddress": "REDACTED",
        "mtu": 1500,
        "netmask": "255.255.255.0",
        "network": "REDACTED",
        "type": "ether"
    },
    "ansible_default_ipv6": {},
    "ansible_device_links": {
        "ids": {},
        "labels": {
            "xvda1": [
                "cloudimg-rootfs"
            ],
            "xvdd": [
                "config-2"
            ]
        },
        "masters": {},
        "uuids": {
            "xvda1": [
                "cac81d61-d0f8-4b47-84aa-b48798239164"
            ],
            "xvdd": [
                "2018-10-25-12-05-57-00"
            ]
        }
    },
    "ansible_devices": {
        "xvda": {
            "holders": [],
            "host": "",
            "links": {
                "ids": [],
                "labels": [],
                "masters": [],
                "uuids": []
            },
            "model": null,
            "partitions": {
                "xvda1": {
                    "holders": [],
                    "links": {
                        "ids": [],
                        "labels": [
                            "cloudimg-rootfs"
                        ],
                        "masters": [],
                        "uuids": [
                            "cac81d61-d0f8-4b47-84aa-b48798239164"
                        ]
                    },
                    "sectors": "83883999",
                    "sectorsize": 512,
                    "size": "40.00 GB",
                    "start": "2048",
                    "uuid": "cac81d61-d0f8-4b47-84aa-b48798239164"
                }
            },
            "removable": "0",
            "rotational": "0",
            "sas_address": null,
            "sas_device_handle": null,
            "scheduler_mode": "deadline",
            "sectors": "83886080",
            "sectorsize": "512",
            "size": "40.00 GB",
            "support_discard": "0",
            "vendor": null,
            "virtual": 1
        },
        "xvdd": {
            "holders": [],
            "host": "",
            "links": {
                "ids": [],
                "labels": [
                    "config-2"
                ],
                "masters": [],
                "uuids": [
                    "2018-10-25-12-05-57-00"
                ]
            },
            "model": null,
            "partitions": {},
            "removable": "0",
            "rotational": "0",
            "sas_address": null,
            "sas_device_handle": null,
            "scheduler_mode": "deadline",
            "sectors": "131072",
            "sectorsize": "512",
            "size": "64.00 MB",
            "support_discard": "0",
            "vendor": null,
            "virtual": 1
        },
        "xvde": {
            "holders": [],
            "host": "",
            "links": {
                "ids": [],
                "labels": [],
                "masters": [],
                "uuids": []
            },
            "model": null,
            "partitions": {
                "xvde1": {
                    "holders": [],
                    "links": {
                        "ids": [],
                        "labels": [],
                        "masters": [],
                        "uuids": []
                    },
                    "sectors": "167770112",
                    "sectorsize": 512,
                    "size": "80.00 GB",
                    "start": "2048",
                    "uuid": null
                }
            },
            "removable": "0",
            "rotational": "0",
            "sas_address": null,
            "sas_device_handle": null,
            "scheduler_mode": "deadline",
            "sectors": "167772160",
            "sectorsize": "512",
            "size": "80.00 GB",
            "support_discard": "0",
            "vendor": null,
            "virtual": 1
        }
    },
    "ansible_distribution": "CentOS",
    "ansible_distribution_file_parsed": true,
    "ansible_distribution_file_path": "/etc/redhat-release",
    "ansible_distribution_file_variety": "RedHat",
    "ansible_distribution_major_version": "7",
    "ansible_distribution_release": "Core",
    "ansible_distribution_version": "7.5.1804",
    "ansible_dns": {
        "nameservers": [
            "127.0.0.1"
        ]
    },
    "ansible_domain": "",
    "ansible_effective_group_id": 1000,
    "ansible_effective_user_id": 1000,
    "ansible_env": {
        "HOME": "/home/zuul",
        "LANG": "en_US.UTF-8",
        "LESSOPEN": "||/usr/bin/lesspipe.sh %s",
        "LOGNAME": "zuul",
        "MAIL": "/var/mail/zuul",
        "PATH": "/usr/local/bin:/usr/bin",
        "PWD": "/home/zuul",
        "SELINUX_LEVEL_REQUESTED": "",
        "SELINUX_ROLE_REQUESTED": "",
        "SELINUX_USE_CURRENT_RANGE": "",
        "SHELL": "/bin/bash",
        "SHLVL": "2",
        "SSH_CLIENT": "REDACTED 55672 22",
        "SSH_CONNECTION": "REDACTED 55672 REDACTED 22",
        "USER": "zuul",
        "XDG_RUNTIME_DIR": "/run/user/1000",
        "XDG_SESSION_ID": "1",
        "_": "/usr/bin/python2"
    },
    "ansible_eth0": {
        "active": true,
        "device": "eth0",
        "ipv4": {
            "address": "REDACTED",
            "broadcast": "REDACTED",
            "netmask": "255.255.255.0",
            "network": "REDACTED"
        },
        "ipv6": [
            {
                "address": "REDACTED",
                "prefix": "64",
                "scope": "link"
            }
        ],
        "macaddress": "REDACTED",
        "module": "xen_netfront",
        "mtu": 1500,
        "pciid": "vif-0",
        "promisc": false,
        "type": "ether"
    },
    "ansible_eth1": {
        "active": true,
        "device": "eth1",
        "ipv4": {
            "address": "REDACTED",
            "broadcast": "REDACTED",
            "netmask": "255.255.224.0",
            "network": "REDACTED"
        },
        "ipv6": [
            {
                "address": "REDACTED",
                "prefix": "64",
                "scope": "link"
            }
        ],
        "macaddress": "REDACTED",
        "module": "xen_netfront",
        "mtu": 1500,
        "pciid": "vif-1",
        "promisc": false,
        "type": "ether"
    },
    "ansible_fips": false,
    "ansible_form_factor": "Other",
    "ansible_fqdn": "centos-7-rax-dfw-0003427354",
    "ansible_hostname": "centos-7-rax-dfw-0003427354",
    "ansible_interfaces": [
        "lo",
        "eth1",
        "eth0"
    ],
    "ansible_is_chroot": false,
    "ansible_kernel": "3.10.0-862.14.4.el7.x86_64",
    "ansible_lo": {
        "active": true,
        "device": "lo",
        "ipv4": {
            "address": "127.0.0.1",
            "broadcast": "host",
            "netmask": "255.0.0.0",
            "network": "127.0.0.0"
        },
        "ipv6": [
            {
                "address": "::1",
                "prefix": "128",
                "scope": "host"
            }
        ],
        "mtu": 65536,
        "promisc": false,
        "type": "loopback"
    },
    "ansible_local": {},
    "ansible_lsb": {
        "codename": "Core",
        "description": "CentOS Linux release 7.5.1804 (Core)",
        "id": "CentOS",
        "major_release": "7",
        "release": "7.5.1804"
    },
    "ansible_machine": "x86_64",
    "ansible_machine_id": "2db133253c984c82aef2fafcce6f2bed",
    "ansible_memfree_mb": 7709,
    "ansible_memory_mb": {
        "nocache": {
            "free": 7804,
            "used": 173
        },
        "real": {
            "free": 7709,
            "total": 7977,
            "used": 268
        },
        "swap": {
            "cached": 0,
            "free": 0,
            "total": 0,
            "used": 0
        }
    },
    "ansible_memtotal_mb": 7977,
    "ansible_mounts": [
        {
            "block_available": 7220998,
            "block_size": 4096,
            "block_total": 9817227,
            "block_used": 2596229,
            "device": "/dev/xvda1",
            "fstype": "ext4",
            "inode_available": 10052341,
            "inode_total": 10419200,
            "inode_used": 366859,
            "mount": "/",
            "options": "rw,seclabel,relatime,data=ordered",
            "size_available": 29577207808,
            "size_total": 40211361792,
            "uuid": "cac81d61-d0f8-4b47-84aa-b48798239164"
        },
        {
            "block_available": 0,
            "block_size": 2048,
            "block_total": 252,
            "block_used": 252,
            "device": "/dev/xvdd",
            "fstype": "iso9660",
            "inode_available": 0,
            "inode_total": 0,
            "inode_used": 0,
            "mount": "/mnt/config",
            "options": "ro,relatime,mode=0700",
            "size_available": 0,
            "size_total": 516096,
            "uuid": "2018-10-25-12-05-57-00"
        }
    ],
    "ansible_nodename": "centos-7-rax-dfw-0003427354",
    "ansible_os_family": "RedHat",
    "ansible_pkg_mgr": "yum",
    "ansible_processor": [
        "0",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "1",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "2",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "3",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "4",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "5",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "6",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
        "7",
        "GenuineIntel",
        "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz"
    ],
    "ansible_processor_cores": 8,
    "ansible_processor_count": 8,
    "ansible_processor_nproc": 8,
    "ansible_processor_threads_per_core": 1,
    "ansible_processor_vcpus": 8,
    "ansible_product_name": "HVM domU",
    "ansible_product_serial": "REDACTED",
    "ansible_product_uuid": "REDACTED",
    "ansible_product_version": "4.1.5",
    "ansible_python": {
        "executable": "/usr/bin/python2",
        "has_sslcontext": true,
        "type": "CPython",
        "version": {
            "major": 2,
            "micro": 5,
            "minor": 7,
            "releaselevel": "final",
            "serial": 0
        },
        "version_info": [
            2,
            7,
            5,
            "final",
            0
        ]
    },
    "ansible_python_version": "2.7.5",
    "ansible_real_group_id": 1000,
    "ansible_real_user_id": 1000,
    "ansible_selinux": {
        "config_mode": "enforcing",
        "mode": "enforcing",
        "policyvers": 31,
        "status": "enabled",
        "type": "targeted"
    },
    "ansible_selinux_python_present": true,
    "ansible_service_mgr": "systemd",
    "ansible_ssh_host_key_ecdsa_public": "REDACTED KEY VALUE",
    "ansible_ssh_host_key_ed25519_public": "REDACTED KEY VALUE",
    "ansible_ssh_host_key_rsa_public": "REDACTED KEY VALUE",
    "ansible_swapfree_mb": 0,
    "ansible_swaptotal_mb": 0,
    "ansible_system": "Linux",
    "ansible_system_capabilities": [
        ""
    ],
    "ansible_system_capabilities_enforced": "True",
    "ansible_system_vendor": "Xen",
    "ansible_uptime_seconds": 151,
    "ansible_user_dir": "/home/zuul",
    "ansible_user_gecos": "",
    "ansible_user_gid": 1000,
    "ansible_user_id": "zuul",
    "ansible_user_shell": "/bin/bash",
    "ansible_user_uid": 1000,
    "ansible_userspace_architecture": "x86_64",
    "ansible_userspace_bits": "64",
    "ansible_virtualization_role": "guest",
    "ansible_virtualization_type": "xen",
    "gather_subset": [
        "all"
    ],
    "module_setup": true
}
```

Example 4 (unknown):
```unknown
{{ ansible_facts['devices']['xvda']['model'] }}
```

---

## Ansible-core 2.19 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.19.html

**Contents:**
- Ansible-core 2.19 Porting Guide
- Introduction
- Playbook
  - Broken Conditionals
    - Example - implicit boolean conversion
    - Example - unintentional truthy conditional
    - Example - expression syntax error
    - Example - Jinja order of operations
    - Example - dictionary as conditional
  - Multi-pass templating

This section discusses the behavioral changes between ansible-core 2.18 and ansible-core 2.19.

It is intended to assist in updating your playbooks, plugins, and other parts of your Ansible infrastructure so they will work with this version of Ansible.

Review this page and the ansible-core Changelog for 2.19 to understand necessary changes.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.19 Porting Guide

Example - implicit boolean conversion

Example - unintentional truthy conditional

Example - expression syntax error

Example - Jinja order of operations

Example - dictionary as conditional

Multi-pass templating

Example - unnecessary template in expression

Example - dynamic expression construction

Troubleshooting untrusted templates

Loops no longer leak omit placeholders

Example - missing default(omit)

Privilege escalation timeouts

Template trust model inversion

Native Jinja mode required

Example - unintentional string conversion

Example - unintentional None result

Consistent handling of range

Example - intentional list conversion

Example - unintentional string conversion

Contextual warnings and errors

Variable provenance tracking

Deprecation warnings on value access

Improved Ansible module error handling

Improved handling of undefined

Example - missing attribute

Displaying tracebacks

Applying template trust to individual values

Applying template trust in inventory and vars plugins

Overly-broad exception handling in Jinja plugins

Ansible custom data types

AnsibleVaultEncryptedUnicode replaced by EncryptedString

No implicit conversion of non-string dict keys

Noteworthy module changes

Noteworthy plugin changes

Porting custom scripts

This release includes an overhaul of the templating system and a new feature dubbed Data Tagging. These changes enable reporting of numerous problematic behaviors that went undetected in previous releases, with wide-ranging positive effects on security, performance, and user experience.

Backward compatibility has been preserved where practical, but some breaking changes were necessary. This guide describes some common problem scenarios with example content, error messages, and suggested solutions.

We recommend you test your playbooks and roles in a staging environment with this release to determine where you may need to make changes.

Broken conditionals occur when the input expression or template is not a string, or the result is not a boolean. Python and Jinja provide implicit “truthy” evaluation of most non-empty non-boolean values in conditional expressions. While sometimes desirable for brevity, truthy conditional evaluation often masks serious logic errors in playbooks that could not be reliably detected by previous versions of ansible-core.

Changes to templating in this release detects non-boolean conditionals during expression evaluation and reports an error by default. The error can be temporarily reduced to a warning with the ALLOW_BROKEN_CONDITIONALS config setting.

The following examples are derived from broken conditionals that masked logic errors in actual playbooks.

This expression relies on an implicit truthy evaluation of inventory_hostname. An explicit predicate with a boolean result, such as | length > 0 or is truthy, should be used instead.

The error reported is:

This can be resolved by using an explicit boolean conversion:

The second part of this conditional is erroneously quoted. The quoted part becomes the expression result (evaluated as truthy), so the expression can never be False.

The error reported is:

This can be resolved by removing the erroneous quotes:

Previous Ansible releases could mask some expression syntax errors as a truthy result.

The error reported is:

This can be resolved by removing the invalid comma after the expression.

This expression uses the ~ concatenation operator, which is evaluated after the contains test. The result is always a non-empty string, which is truthy.

The error reported is:

This can be resolved by inserting parentheses to resolve the concatenation operation before the contains test:

This conditional should have been quoted. In a YAML list element, an unquoted string with a space after a colon is interpreted by the YAML parser as a mapping. Non-empty mappings are always truthy.

The error reported is:

This can be resolved by quoting the entire assertion expression:

Embedding templates within other templates or expressions could previously result in untrusted templates being executed. The overhauled templating engine in this release no longer supports this insecure behavior.

This conditional references a variable using a template instead of using the variable directly in the expression.

The error reported is:

This can be resolved by referencing the variable without a template:

This conditional is dynamically created using a template, which is expected to be evaluated as an expression. Previously, the template was rendered by task argument templating, resulting in a plain string, which was later evaluated by the assert action.

The error reported is:

Dynamic expression construction from playbooks is insecure and unsupported.

By default, untrusted templates are silently ignored. Troubleshooting trust issues with templates can be aided by enabling warnings or errors for untrusted templates. The environment variable _ANSIBLE_TEMPLAR_UNTRUSTED_TEMPLATE_BEHAVIOR can be used to control this behavior.

warning - A warning will be issued when an untrusted template is encountered.

error - An error will be raised when an untrusted template is encountered.

ignore - Untrusted templates are silently ignored and used as-is. This is the default behavior.

This optional warning and failure behavior is experimental and subject to change in future versions.

Omit placeholders no longer leak between loop item templating and task templating.

Previously, omit placeholders could remain embedded in loop items after templating and be used as an omit for task templating. Now, values resolving to omit are dropped immediately when loop items are templated.

To turn missing values into an omit for task templating, use | default(omit). This solution is backward compatible with previous versions of ansible-core.

The following task tries to pass omit from a loop to the task, but the value is undefined since it was omitted:

This updated task uses default(omit) on the missing value to ensure it is omitted for the task:

Timeout waiting on privilege escalation (become) is now an unreachable error instead of a task error. Existing playbooks should be changed to replace ignore_errors with ignore_unreachable on tasks where timeout on become should be ignored.

Previously, ansible-core implicitly trusted all string values to be rendered as Jinja templates, but applied an “unsafe” wrapper object around strings obtained from untrusted sources (for example, module results). Unsafe-wrapped strings were silently ignored by the template engine, as many templating operations can execute arbitrary code on the control host as the user running ansible-core. This required any code that operated on strings to correctly propagate the wrapper object, which resulted in numerous CVE-worthy RCE (remote code execution) vulnerabilities.

This release inverts the previous trust model. Only strings marked as loaded from a trusted source are eligible to be rendered as templates. Untrusted values can (as before) be referenced by templates, but the template expression itself must always be trusted. While this change still requires consideration for propagation of trust markers when manipulating strings, failure to do so now results in a loss of templating ability instead of a potentially high-severity security issue.

Attempts to render a template appearing in an untrusted string will (as before) return the original string unmodified. By default, attempting to render an untrusted template fails silently, though such failures can be elevated to a warning or error via configuration.

Newly-created string results from template operations will never have trust automatically applied, though templates that return existing trusted string values unmodified will not strip their trust. It is also possible for plugins to explicitly apply trust.

Backward-compatible template trust behavior is applied automatically in most cases; for example, templates appearing in playbooks, roles, variable files, and most built-in inventory plugins will yield trusted template strings. Custom plugins that source template strings will be required to use new public APIs to apply trust where appropriate.

See Plugin API and Troubleshooting untrusted templates for additional information.

Previous versions supported templating in two different modes:

Jinja’s original string templating mode converted the result of each templating operation to a string.

Jinja’s native mode usually preserved variable types in template results.

In both modes, ansible-core evaluated the final template string results as Python literals, falling back to the original string if the evaluation resulted in an error. Selection of the templating mode was controlled by configuration, defaulting to Jinja’s original string templating.

Jinja’s native templating mode is now used exclusively. The configuration option for setting the templating mode is deprecated and no longer has any effect.

Preservation of native types in templating has been improved to correct gaps in the previous implementation, entirely eliminating the final literal evaluation pass (a frequent source of confusion, errors, and performance issues). In rare cases where playbooks relied on implicit object conversion from strings, an explicit conversion will be required.

Some existing templates may unintentionally convert non-strings to strings. In previous versions this conversion could be masked by the evaluation of strings as Python literals.

This expression erroneously passes a list to the replace filter, which operates only on strings. The filter silently converts the list input to a string. Due to some string results previously parsing as lists, this mistake often went undetected in earlier versions.

The result of this template becomes a string:

This can be resolved by using the map filter to apply the replace filter to each list element:

The result of the corrected template remains a list:

If a template evaluated to None, it was implicitly converted to an empty string in previous versions of ansible-core. This can now result in the template evaluating to the value None.

The following example shows a case where this happens:

This example can be fixed as follows:

This adjustment is backward-compatible with older ansible-core versions.

Since ansible-core 2.19.1, module options of type string accept None and convert it to an empty string. Before ansible-core 2.18, passing None to such options resulted in an error. This means that in most cases, expressions in roles and playbooks do not need to be adjusted because of unintentional None results.

Ansible’s interface with the Jinja templating engine has been heavily refined, yielding significant performance improvements for many complex templating operations. Previously, deeply-nested, recursive, or self-referential templating operations were always resolved to their full depth and breadth on every access, including repeated access to the same data within a single templating operation. This resulted in expensive and repetitive evaluation of the same templates within a single logical template operation, even for templates deep inside nested data structures that were never directly accessed. The new template engine lazily defers nearly all recursion and templating until values are accessed, or known to be exiting the template engine, and intermediate nested or indirected templated results are cached for the duration of the template operation, reducing repetitive templating. These changes have shown exponential performance improvements for many real-world complex templating scenarios.

The result of using the Jinja global function range() was heavily dependent on the context in which it was used and whether Jinja’s native mode was enabled. To preserve the ability to use very large ranges in filter chains the result is now always a range object, which means it cannot be returned from a template unless you convert it to a returnable type.

Ranges not embedded in containers would usually be converted to lists during template finalization. They will now result in this error:

This can be resolved by making the conversion explicit:

Ranges embedded in containers would usually be converted to string representations of the range object.

Attempting to do this will now result in an error; you can mimic the old behaviour by explicitly converting the container to a string, or convert the ranges to lists if you actually want to do something useful with them.

Changes to internal error handling in ansible-core will be visible in many situations that result in a warning or error. In most cases, the operational context (what was happening when the error or warning was generated) and data element(s) involved are captured and included in user-facing messages. Errors and warnings that occur during task execution are more consistently included in the task result, with the full details accessible to callbacks and (in the case of errors), a minimal error message in the msg field of the result. Due to the standardized nature of this error handling, seemingly redundant elements may appear in some error messages. These will improve over time as other error handling improvements are made but are currently necessary to ensure proper context is available in all error situations. Error message contents are not considered stable, so automation that relies on them should be avoided when possible.

The new Data Tagging feature expands provenance tracking on variables to nearly every source. This allows for much more descriptive error messaging, as the entire chain of execution can be consulted to include contextual information about what was happening when an error occurred. In most cases, this includes file path, source lines, and column markers. Non-file variable sources such as CLI arguments, inventory plugins and environment are also supported.

New features allow most ansible-core variables and values to be tagged as deprecated. Plugins and modules can apply these tags to augment deprecated elements of their return values with a description and help text to suggest alternatives, which will be displayed in a runtime warning when the tagged value is accessed by, for example, a playbook or template. This allows for easier evolution and removal of module and fact results, and obsolete core behaviors.

For example, accessing the deprecated play_hosts magic variable will trigger a deprecation warning that suggests the use of the ansible_play_batch variable instead.

Ansible modules implemented in Python now have exception handling provided by the AnsiballZ wrapper. In previous versions of ansible-core, unhandled exceptions in an Ansible module simply printed a traceback and exited without providing a standard module response, which caused the task result to contain a generic MODULE FAILURE message and any raw output text produced by the module.

To address this, modules often implemented unnecessary try/except blocks around most code where specific error handling was not possible, only to call AnsibleModule.fail_json with a generic failure message. This pattern is no longer necessary, as all unhandled exceptions in Ansible Python modules are now captured by the AnsiballZ wrapper and returned as a structured module result, with automatic inclusion of traceback information when enabled by the controller.

Undefined handling has been improved to avoid situations where a Jinja plugin silently ignores undefined values.

This commonly occurs when a Jinja plugin, such as a filter or test, checks the type of a variable without accounting for the possibility of an undefined value being present.

This task incorrectly references an undefined exists attribute from a stat result in a conditional. The undefined value was not detected in previous versions because it is passed to the false Jinja test plugin, which silently ignores undefined values. As a result, this conditional could never be True in earlier versions of ansible-core, and there was no indication that the failed_when expression was invalid.

In the current release the faulty expression is detected and results in an error.

This can be corrected by adding the missing stat attribute to the conditional:

In previous ansible-core versions, tracebacks from some controller-side errors were available by increasing verbosity with the -vvv option, but the availability and behavior was inconsistent. This feature was also limited to errors.

Handling of errors, warnings and deprecations throughout much of the ansible-core codebase has now been standardized. Tracebacks can be optionally collected and displayed for all exceptions, as well as at the call site of errors, warnings, or deprecations (even in module code) using the ANSIBLE_DISPLAY_TRACEBACK environment variable.

always - Tracebacks will always be displayed. This option takes precedence over others below.

never - Tracebacks will never be displayed. This option takes precedence over others below.

error - Tracebacks will be displayed for errors.

warning - Tracebacks will be displayed for warnings other than deprecation warnings.

deprecated - Tracebacks will be displayed for deprecation warnings.

Multiple options can be combined by separating them with commas.

Plugins and Python modules can tag returned values as deprecated with the new deprecate_value function from ansible.module_utils.datatag. A description of the deprecated feature, optional help text, and removal timeframes can be attached to the value, which will appear in a runtime warning if the deprecated value is referenced in an expression. The warning message will include information about the module/plugin that applied the deprecation tag and the location of the expression that accessed it.

When accessing the color_name from the module result, the following warning will be shown

String values are no longer trusted to be rendered as templates by default. Strings loaded from playbooks, vars files, and other built-in trusted sources are usually marked trusted by default. Plugins that create new string instances with embedded templates must use the new trust_as_template function from ansible.template to tag those values as originating from a trusted source to allow the templates to be rendered.

This section and the associated public API are currently incomplete.

Inventory plugins can set group and host variables. In most cases, these variables are static values from external sources and do not require trust. Values that can contain templates will require explicit trust via trust_as_template to be allowed to render, but trust should not be applied to variable values from external sources that could be maliciously altered to include templates.

This section and the associated public API are currently incomplete.

When raising exceptions in an exception handler, be sure to use raise ... from as appropriate. This supersedes the use of the AnsibleError arg orig_exc to represent the cause. Specifying orig_exc as the cause is still permitted for backward compatibility.

Failure to use raise ... from when orig_exc is set will result in a warning. Additionally, if the two cause exceptions do not match, a warning will be issued.

Jinja plugins with overly broad exception handling, such as except Exception, may behave incorrectly when accessing the contents of variables which are containers (dict, list). This can occur when a templated value from a variable is undefined, is an undecryptable vaulted value, or another value which triggers lazily reported fault conditions.

Jinja plugins should catch more specific exception types where possible, and do so around the smallest reasonable portion of code. Be especially careful to avoid broad exception handling around code which accesses the contents of container variables.

Many variable objects in ansible-core are represented by custom types. In previous versions these could be seen as types such as:

AnsibleUnicode (a subclass of str)

AnsibleSequence (a subclass of list)

AnsibleMapping (a subclass of dict)

These types, and more, now have new subclasses derived from their native Python types. In most cases these types behave indistinguishably from the types they extend, and existing code should function normally. However, some Python libraries do not handle builtin object subclasses properly. Custom plugins that interact with such libraries may require changes to convert and pass the native types.

This section and the associated public API are currently incomplete.

The AnsibleVaultEncryptedUnicode type has been replaced by EncryptedString.

Plugins which create AnsibleVaultEncryptedUnicode will now receive EncryptedString instances instead. This feature ensures backward compatibility with previous versions of ansible-core.

Plugins which perform isinstance checks, looking for AnsibleVaultEncryptedUnicode, will no longer encounter these types. Values formerly represented by that type will now appear as a tagged str instead. Special handling in plugins is no longer required to access the contents of these values.

In previous versions, ansible-core relied on Python’s json.dumps to implicitly convert int, float, bool and None dictionary keys to strings in various scenarios, including returning of module results. For example, a module was allowed to contain the following code:

Starting with this release, modules must explicitly convert any non-string keys to strings (for example, by using the str() Python function) before passing dictionaries to the AnsibleModule.exit_json() method of ansible-core. The above code must be changed as follows:

If you encounter "[ERROR]: Task failed: Module failed: Key of type '<NON-STRING>' is not JSON serializable by the 'module_legacy_m2c' profile., it indicates that the module that is used in the task does not perform the required key conversion.

With the changes to the templating system it is no longer possible to use the async_status module’s started and finished integer properties as values in conditionals as booleans are required. It is recommended to use started and finished test plugins instead, for example:

The following modules no longer exist:

The ssh connection plugin now supports using SSH_ASKPASS to supply passwords for authentication as an alternative to the sshpass program. The default is to use SSH_ASKPASS instead of sshpass. This is controlled by the password_mechanism configuration for the ssh connection plugin. To switch back to using sshpass make one of the following changes:

To your ansible.cfg file:

By exporting an environment variable:

By setting the following variable:

Coercing unrecognized input values in the bool filter is deprecated. The bool filter now returns only True or False, depending on the input:

True - Returned for True, 1 and case-insensitive matches on the strings: “yes”, “on”, “true”, “1”

False - Returned for False, 0 and case-insensitive matches on the strings: “no”, “off”, “false”, “0”

Any other input will result in a deprecation warning. This warning will become an error in ansible-core 2.23.

When a deprecation warning is issued, the return value is False unless the input equals 1, which can occur when the input is the float value of 1.0.

This filter now returns False instead of None when the input is None. The aforementioned deprecation warning is also issued in this case.

Passing nested non-scalars with embedded templates that may resolve to Undefined to Jinja2 filter plugins, such as default and mandatory, and test plugins including defined and undefined no longer evaluate as they did in previous versions because nested non-scalars with embedded templates are templated on use only. In 2.19, this assertion passes:

**Examples:**

Example 1 (unknown):
```unknown
- assert:
    that: inventory_hostname
```

Example 2 (unknown):
```unknown
Conditional result was 'localhost' of type 'str', which evaluates to True. Conditionals must have a boolean result.
```

Example 3 (unknown):
```unknown
- assert:
    that: inventory_hostname | length > 0
```

Example 4 (unknown):
```unknown
- assert:
    that: inventory_hostname is defined and 'inventory_hostname | length > 0'
```

---

## Understanding privilege escalation: become — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_privilege_escalation.html

**Contents:**
- Understanding privilege escalation: become
- Using become
  - Become directives
  - Become connection variables
  - Become command-line options
- Risks and limitations of become
  - Risks of becoming an unprivileged user
  - Not supported by all connection plugins
  - Only one method may be enabled per host
  - Privilege escalation must be general

Ansible uses existing privilege escalation systems to execute tasks with root privileges or with another user’s permissions. Because this feature allows you to ‘become’ another user, different from the user that logged into the machine (remote user), we call it become. The become keyword uses existing privilege escalation tools like sudo, su, pfexec, doas, pbrun, dzdo, ksu, runas, machinectl and others.

Become connection variables

Become command-line options

Risks and limitations of become

Risks of becoming an unprivileged user

Not supported by all connection plugins

Only one method may be enabled per host

Privilege escalation must be general

May not access environment variables populated by pamd_systemd

Resolving Temporary File Error Messages

Become and network automation

Setting enable mode for all tasks

Passwords for enable mode

authorize and auth_pass

Administrative rights

Local service accounts

Become without setting a password

Accounts without a password

Become flags for Windows

Limitations of become on Windows

You can control the use of become with play or task directives, connection variables, or at the command line. If you set privilege escalation properties in multiple ways, review the general precedence rules to understand which settings will be used.

A full list of all become plugins that are included in Ansible can be found in the Plugin List.

You can set the directives that control become at the play or task level. You can override these by setting connection variables, which often differ from one host to another. These variables and directives are independent. For example, setting become_user does not set become.

set to true to activate privilege escalation.

set to user with desired privileges — the user you become, NOT the user you login as. Does NOT imply become: true, to allow it to be set at the host level. The default value is root.

(at play or task level) overrides the default method set in ansible.cfg, set to use any of the Become plugins.

(at play or task level) permit the use of specific flags for the tasks or role. One common use is to change the user to nobody when the shell is set to nologin. Added in Ansible 2.2.

For example, to manage a system service (which requires root privileges) when connected as a non-root user, you can use the default value of become_user (root):

To run a command as the apache user:

To do something as the nobody user when the shell is nologin:

To specify a password for sudo, run ansible-playbook with --ask-become-pass (-K for short). If you run a playbook utilizing become and the playbook seems to hang, most likely it is stuck at the privilege escalation prompt. Stop it with CTRL-c, then execute the playbook with -K and the appropriate password.

You can define different become options for each managed node or group. You can define these variables in inventory or use them as normal variables.

overrides the become directive and decides if privilege escalation is used or not.

which privilege escalation method should be used

set the user you become through privilege escalation; does not imply ansible_become: true

set the privilege escalation password. See Using encrypted variables and files for details on how to avoid having secrets in plain text

determines if Ansible should try to chgrp its temporary files to a group if setfacl and chown both fail. See Risks of becoming an unprivileged user for more information. Added in version 2.10.

For example, if you want to run all tasks as root on a server named webserver, but you can only connect as the manager user, you could use an inventory entry like this:

The variables defined above are generic for all become plugins but plugin-specific ones can also be set instead. Please see the documentation for each plugin for a list of all options the plugin has and how they can be defined. A full list of become plugins in Ansible can be found at Become plugins.

ask for the privilege escalation password; does not imply become will be used. Note that this password will be used for all hosts.

run operations with become (no password implied)

privilege escalation method to use (default=sudo), valid choices: [ sudo | su | pbrun | pfexec | doas | dzdo | ksu | runas | machinectl ]

run operations as this user (default=root), does not imply --become/-b

Although privilege escalation is mostly intuitive, there are a few limitations on how it works. Users should be aware of these to avoid surprises.

Ansible modules are executed on the remote machine by first substituting the parameters into the module file, then copying the file to the remote machine, and finally executing it there.

Everything is fine if the module file is executed without using become, when the become_user is root, or when the connection to the remote machine is made as root. In these cases, Ansible creates the module file with permissions that only allow reading by the user and root, or only allow reading by the unprivileged user being switched to.

However, when both the connection user and the become_user are unprivileged, the module file is written as the user that Ansible connects as (the remote_user), but the file needs to be readable by the user Ansible is set to become. The details of how Ansible solves this can vary based on the platform. However, on POSIX systems, Ansible solves this problem in the following way:

First, if setfacl is installed and available in the remote PATH, and the temporary directory on the remote host is mounted with POSIX.1e filesystem ACL support, Ansible will use POSIX ACLs to share the module file with the second unprivileged user.

Next, if POSIX ACLs are not available or setfacl could not be run, Ansible will attempt to change ownership of the module file using chown for systems that support doing so as an unprivileged user.

New in Ansible 2.11, at this point, Ansible will try chmod +a which is a macOS-specific way of setting ACLs on files.

New in Ansible 2.10, if all of the above fails, Ansible will then check the value of the configuration setting ansible_common_remote_group. Many systems will allow a given user to change the group ownership of a file to a group the user is in. As a result, if the second unprivileged user (the become_user) has a UNIX group in common with the user Ansible is connected as (the remote_user), and if ansible_common_remote_group is defined to be that group, Ansible can try to change the group ownership of the module file to that group by using chgrp, thereby likely making it readable to the become_user.

At this point, if ansible_common_remote_group was defined and a chgrp was attempted and returned successfully, Ansible assumes (but, importantly, does not check) that the new group ownership is enough and does not fall back further. That is, Ansible does not check that the become_user does in fact share a group with the remote_user; so long as the command exits successfully, Ansible considers the result successful and does not proceed to check world_readable_temp per below.

If ansible_common_remote_group is not set and the chown above it failed, or if ansible_common_remote_group is set but the chgrp (or following group-permissions chmod) returned a non-successful exit code, Ansible will lastly check the world_readable_temp option. If this is set, Ansible will place the module file in a world-readable temporary directory, with world-readable permissions to allow the become_user (and incidentally any other user on the system) to read the contents of the file. If any of the parameters passed to the module are sensitive in nature, and you do not trust the remote machines, then this is a potential security risk.

Once the module is done executing, Ansible deletes the temporary file.

Several ways exist to avoid the above logic flow entirely:

Use pipelining. When pipelining is enabled, Ansible does not save the module to a temporary file on the client. Instead, it pipes the module to the remote Python interpreter’s stdin. Pipelining does not work for Python modules involving file transfer (for example: copy, fetch, template), or for non-Python modules.

Avoid becoming an unprivileged user. Temporary files are protected by UNIX file permissions when you become root or do not use become. In Ansible 2.1 and above, UNIX file permissions are also secure if you make the connection to the managed machine as root and then use become to access an unprivileged account.

Although the Solaris ZFS filesystem has filesystem ACLs, the ACLs are not POSIX.1e filesystem acls (they are NFSv4 ACLs instead). Ansible cannot use these ACLs to manage its temp file permissions so you may have to resort to the world_readable_temp option if the remote machines use ZFS.

Changed in version 2.1.

Ansible makes it hard to unknowingly use become insecurely. Starting in Ansible 2.1, Ansible defaults to issuing an error if it cannot execute securely with become. If you cannot use pipelining or POSIX ACLs, must connect as an unprivileged user, must use become to execute as a different unprivileged user, and decide that your managed nodes are secure enough for the modules you want to run there to be world readable, you can turn on the world_readable_temp option, which will change this from an error into a warning and allow the task to run as it did prior to 2.1.

Changed in version 2.10.

Ansible 2.10 introduces the above-mentioned ansible_common_remote_group fallback. As mentioned above, if enabled, it is used when remote_user and become_user are both unprivileged users. Refer to the text above for details on when this fallback happens.

As mentioned above, if ansible_common_remote_group and world_readable_temp are both enabled, it is unlikely that the world-readable fallback will ever trigger, and yet Ansible might still be unable to access the module file. This is because after the group ownership change is successful, Ansible does not fall back any further, and also does not do any checks to ensure that the become_user is actually a member of the “common group”. This is a design decision made by the fact that doing such a check would require another round-trip connection to the remote machine, which is a time-expensive operation. Ansible does, however, emit a warning in this case.

Privilege escalation methods must also be supported by the connection plugin used. Most connection plugins will warn if they do not support become. Some will just ignore it as they always run as root (jail, chroot, and so on).

Methods cannot be chained. You cannot use sudo /bin/su - to become a user, you need to have privileges to run the command as that user in sudo or be able to su directly to it (the same for pbrun, pfexec or other supported methods).

You cannot limit privilege escalation permissions to certain commands. Ansible does not always use a specific command to do something but runs modules (code) from a temporary file name which changes every time. If you have ‘/sbin/service’ or ‘/bin/chmod’ as the allowed commands this will fail with Ansible as those paths won’t match with the temporary file that Ansible creates to run the module. If you have security rules that constrain your sudo/pbrun/doas environment to run specific command paths only, use Ansible from a special account that does not have this constraint, or use AWX or the Red Hat Ansible Automation Platform to manage indirect access to SSH credentials.

For most Linux distributions using systemd as their init, the default methods used by become do not open a new “session”, in the sense of systemd. Because the pam_systemd module will not fully initialize a new session, you might have surprises compared to a normal session opened through ssh: some environment variables set by pam_systemd, most notably XDG_RUNTIME_DIR, are not populated for the new user and instead inherited or just emptied.

This might cause trouble when trying to invoke systemd commands that depend on XDG_RUNTIME_DIR to access the bus:

To force become to open a new systemd session that goes through pam_systemd, you can use become_method: machinectl.

For more information, see this systemd issue.

Failed to set permissions on the temporary files Ansible needs to create when becoming an unprivileged user”

This error can be resolved by installing the package that provides the setfacl command. (This is frequently the acl package but check your OS documentation.)

As of version 2.6, Ansible supports become for privilege escalation (entering enable mode or privileged EXEC mode) on all Ansible-maintained network platforms that support enable mode. Using become replaces the authorize and auth_pass options in a provider dictionary.

You must set the connection type to either connection: ansible.netcommon.network_cli or connection: ansible.netcommon.httpapi to use become for privilege escalation on network devices. Check the Platform Options documentation for details.

You can use escalated privileges on only the specific tasks that need them, on an entire play, or on all plays. Adding become: true and become_method: enable instructs Ansible to enter enable mode before executing the task, play, or playbook where those parameters are set.

If you see this error message, the task that generated it requires enable mode to succeed:

To set enable mode for a specific task, add become at the task level:

To set enable mode for all tasks in a single play, add become at the play level:

Often you wish for all tasks in all plays to run using privilege mode, which is best achieved by using group_vars:

If you need a password to enter enable mode, you can specify it in one of two ways:

providing the --ask-become-pass command line option

setting the ansible_become_password connection variable

As a reminder passwords should never be stored in plain text. For information on encrypting your passwords and other secrets with Ansible Vault, see Ansible Vault.

Ansible still supports enable mode with connection: local for legacy network playbooks. To enter enable mode with connection: local, use the module options authorize and auth_pass:

We recommend updating your playbooks to use become for network-device enable mode consistently. The use of authorize and provider dictionaries will be deprecated in the future. Check the Platform Options documentation for details.

Since Ansible 2.3, become can be used on Windows hosts through the runas method. Become on Windows uses the same inventory setup and invocation arguments as become on a non-Windows host, so the setup and variable names are the same as what is defined in this document except become_user. As there is no sensible default for become_user on Windows it is required when using become. See ansible.builtin.runas become plugin for details.

While become can be used to assume the identity of another user, there are other uses for it with Windows hosts. One important use is to bypass some of the limitations that are imposed when running on WinRM, such as constrained network delegation or accessing forbidden system calls like the WUA API. You can use become with the same user as ansible_user to bypass these limitations and run commands that are not normally accessible in a WinRM session.

On Windows, you cannot connect with an underprivileged account and use become to elevate your rights. Become can only be used if your connection account is already an Administrator of the target host.

Many tasks in Windows require administrative privileges to complete. When using the runas become method, Ansible will attempt to run the module with the full privileges that are available to the become user. If it fails to elevate the user token, it will continue to use the limited token during execution.

A user must have the SeDebugPrivilege to run a become process with elevated privileges. This privilege is assigned to Administrators by default. If the debug privilege is not available, the become process will run with a limited set of privileges and groups.

To determine the type of token that Ansible was able to get, run the following task:

The output will look something similar to the below:

Under the label key, the account_name entry determines whether the user has Administrative rights. Here are the labels that can be returned and what they represent:

Medium: Ansible failed to get an elevated token and ran under a limited token. Only a subset of the privileges assigned to the user are available during the module execution and the user does not have administrative rights.

High: An elevated token was used and all the privileges assigned to the user are available during the module execution.

System: The NT AUTHORITY\System account is used and has the highest level of privileges available.

The output will also show the list of privileges that have been granted to the user. When the privilege value is disabled, the privilege is assigned to the logon token but has not been enabled. In most scenarios, these privileges are automatically enabled when required.

If running on a version of Ansible that is older than 2.5 or the normal runas escalation process fails, an elevated token can be retrieved by:

Set the become_user to System which has full control over the operating system.

Grant SeTcbPrivilege to the user Ansible connects with on WinRM. SeTcbPrivilege is a high-level privilege that grants full control over the operating system. No user is given this privilege by default, and care should be taken if you grant this privilege to a user or group. For more information on this privilege, please see Act as part of the operating system. You can use the below task to set this privilege on a Windows host:

Turn UAC off on the host and reboot before trying to become the user. UAC is a security protocol that is designed to run accounts with the least privilege principle. You can turn UAC off by running the following tasks:

Granting the SeTcbPrivilege or turning UAC off can cause Windows security vulnerabilities and care should be given if these steps are taken.

Prior to Ansible version 2.5, become only worked on Windows with a local or domain user account. Local service accounts like System or NetworkService could not be used as become_user in these older versions. This restriction has been lifted since the 2.5 release of Ansible. The three service accounts that can be set under become_user are:

Because local service accounts do not have passwords, the ansible_become_password parameter is not required and is ignored if specified.

As of Ansible 2.8, become can be used to become a Windows local or domain account without requiring a password for that account. For this method to work, the following requirements must be met:

The connection user has the SeDebugPrivilege privilege assigned

The connection user is part of the BUILTIN\Administrators group

The become_user has either the SeBatchLogonRight or SeNetworkLogonRight user right

Using become without a password is achieved in one of two different methods:

Duplicating an existing logon session’s token if the account is already logged on

Using S4U to generate a logon token that is valid on the remote host only

In the first scenario, the become process is spawned from another logon of that user account. This could be an existing RDP logon, console logon, but this is not guaranteed to occur all the time. This is similar to the Run only when user is logged on option for a Scheduled Task.

In the case where another logon of the become account does not exist, S4U is used to create a new logon and run the module through that. This is similar to the Run whether user is logged on or not with the Do not store password option for a Scheduled Task. In this scenario, the become process will not be able to access any network resources like a normal WinRM process.

To make a distinction between using become with no password and becoming an account that has no password make sure to keep ansible_become_password as undefined or set ansible_become_password:.

Because there are no guarantees an existing token will exist for a user when Ansible runs, there’s a high chance the become process will only have access to local resources. Use become with a password if the task needs to access network resources

As a general security best practice, you should avoid allowing accounts without passwords.

Ansible can be used to become a Windows account that does not have a password (like the Guest account). To become an account without a password, set up the variables like normal but set ansible_become_password: ''.

Before become can work on an account like this, the local policy Accounts: Limit local account use of blank passwords to console logon only must be disabled. This can either be done through a Group Policy Object (GPO) or with this Ansible task:

This is only for accounts that do not have a password. You still need to set the account’s password under ansible_become_password if the become_user has a password.

Ansible 2.5 added the become_flags parameter to the runas become method. This parameter can be set using the become_flags task directive or set in Ansible’s configuration using ansible_become_flags. The two valid values that are initially supported for this parameter are logon_type and logon_flags.

These flags should only be set when becoming a normal user account, not a local service account like LocalSystem.

The key logon_type sets the type of logon operation to perform. The value can be set to one of the following:

interactive: The default logon type. The process will be run under a context that is the same as when running a process locally. This bypasses all WinRM restrictions and is the recommended method to use.

batch: Runs the process under a batch context that is similar to a scheduled task with a password set. This should bypass most WinRM restrictions and is useful if the become_user is not allowed to log on interactively.

new_credentials: Runs under the same credentials as the calling user, but outbound connections are run under the context of the become_user and become_password, similar to runas.exe /netonly. The logon_flags flag should also be set to netcredentials_only. Use this flag if the process needs to access a network resource (like an SMB share) using a different set of credentials.

network: Runs the process under a network context without any cached credentials. This results in the same type of logon session as running a normal WinRM process without credential delegation and operates under the same restrictions.

network_cleartext: Like the network logon type, but instead caches the credentials so it can access network resources. This is the same type of logon session as running a normal WinRM process with credential delegation.

For more information, see dwLogonType.

The logon_flags key specifies how Windows will log the user on when creating the new process. The value can be set to none or multiple of the following:

with_profile: The default logon flag set. The process will load the user’s profile in the HKEY_USERS registry key to HKEY_CURRENT_USER.

netcredentials_only: The process will use the same token as the caller but will use the become_user and become_password when accessing a remote resource. This is useful in inter-domain scenarios where there is no trust relationship, and should be used with the new_credentials logon_type.

By default, logon_flags=with_profile is set, if the profile should not be loaded set logon_flags= or if the profile should be loaded with netcredentials_only, set logon_flags=with_profile,netcredentials_only.

For more information, see dwLogonFlags.

Here are some examples of how to use become_flags with Windows tasks:

Running a task with async and become on Windows Server 2008, 2008 R2 and Windows 7 only works when using Ansible 2.7 or newer.

By default, the become user logs on with an interactive session, so it must have the right to do so on the Windows host. If it does not inherit the SeAllowLogOnLocally privilege or inherits the SeDenyLogOnLocally privilege, the become process will fail. Either add the privilege or set the logon_type flag to change the logon type used.

Prior to Ansible version 2.3, become only worked when ansible_winrm_transport was either basic or credssp. This restriction has been lifted since the 2.4 release of Ansible for all hosts except Windows Server 2008 (non R2 version).

The Secondary Logon service seclogon must be running to use ansible_become_method: runas

The connection user must already be an Administrator on the Windows host to use runas. The target become user does not need to be an Administrator though.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- name: Ensure the httpd service is running
  service:
    name: httpd
    state: started
  become: true
```

Example 2 (unknown):
```unknown
- name: Run a command as the apache user
  command: somecommand
  become: true
  become_user: apache
```

Example 3 (unknown):
```unknown
- name: Run a command as nobody
  command: somecommand
  become: true
  become_method: su
  become_user: nobody
  become_flags: '-s /bin/sh'
```

Example 4 (unknown):
```unknown
webserver ansible_user=manager ansible_become=true
```

---

## Python3 in templates — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_python_version.html

**Contents:**
- Python3 in templates
- Dictionary views
- dict.iteritems()

Ansible uses Jinja2 to take advantage of Python data types and standard functions in templates and variables. You can use these data types and standard functions to perform a rich set of operations on your data. However, if you use templates, you must be aware of the differences between Python versions.

These topics help you design templates that work on both Python2 and Python3. They might also help if you are upgrading from Python2 to Python3. Upgrading within Python2 or Python3 does not usually introduce changes that affect Jinja2 templates.

In Python2, the dict.keys(), dict.values(), and dict.items() methods return a list. Jinja2 returns that to Ansible using a string representation that Ansible can turn back into a list.

In Python3, those methods return a dictionary view object. The string representation that Jinja2 returns for dictionary views cannot be parsed back into a list by Ansible. It is, however, easy to make this portable by using the list filter whenever using dict.keys(), dict.values(), or dict.items().

Python2 dictionaries have iterkeys(), itervalues(), and iteritems() methods.

Python3 dictionaries do not have these methods. Use dict.keys(), dict.values(), and dict.items() to make your playbooks and templates compatible with both Python2 and Python3.

The Dictionary views entry for information on why the list filter is necessary here.

**Examples:**

Example 1 (unknown):
```unknown
vars:
  hosts:
    testhost1: 127.0.0.2
    testhost2: 127.0.0.3
tasks:
  - debug:
      msg: '{{ item }}'
    # Only works with Python 2
    #loop: "{{ hosts.keys() }}"
    # Works with both Python 2 and Python 3
    loop: "{{ hosts.keys() | list }}"
```

Example 2 (unknown):
```unknown
vars:
  hosts:
    testhost1: 127.0.0.2
    testhost2: 127.0.0.3
tasks:
  - debug:
      msg: '{{ item }}'
    # Only works with Python 2
    #loop: "{{ hosts.iteritems() }}"
    # Works with both Python 2 and Python 3
    loop: "{{ hosts.items() | list }}"
```

---

## Interactive input: prompts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_prompts.html

**Contents:**
- Interactive input: prompts
- Hashing values supplied by vars_prompt
- Allowing special characters in vars_prompt values

If you want your playbook to prompt the user for certain input, add a ‘vars_prompt’ section. Prompting the user for variables lets you avoid recording sensitive data like passwords. In addition to security, prompts support flexibility. For example, if you use one playbook across multiple software releases, you could prompt for the particular release version.

Hashing values supplied by vars_prompt

Allowing special characters in vars_prompt values

Here is a most basic example:

The user input is hidden by default but it can be made visible by setting private: false.

Prompts for individual vars_prompt variables will be skipped for any variable that is already defined through the command line --extra-vars option, or when running from a non-interactive session (such as cron or Ansible AWX). See Defining variables at runtime.

If you have a variable that changes infrequently, you can provide a default value that can be overridden.

You can hash the entered value so you can use it, for example, with the user module to define a password:

If you have Passlib installed, you can use any crypt scheme the library supports:

des_crypt - DES Crypt

bsdi_crypt - BSDi Crypt

md5_crypt - MD5 Crypt

sha1_crypt - SHA-1 Crypt

sun_md5_crypt - Sun MD5 Crypt

sha256_crypt - SHA-256 Crypt

sha512_crypt - SHA-512 Crypt

apr_md5_crypt - Apache’s MD5-Crypt variant

phpass - PHPass’ Portable Hash

pbkdf2_digest - Generic PBKDF2 Hashes

cta_pbkdf2_sha1 - Cryptacular’s PBKDF2 hash

dlitz_pbkdf2_sha1 - Dwayne Litzenberger’s PBKDF2 hash

bsd_nthash - FreeBSD’s MCF-compatible nthash encoding

The only parameters accepted are ‘salt’ or ‘salt_size’. You can use your own salt by defining ‘salt’, or have one generated automatically using ‘salt_size’. By default, Ansible generates a salt of size 8.

If you do not have Passlib installed, Ansible uses the crypt library as a fallback. Ansible supports at most four crypt schemes, depending on your platform at most the following crypt schemes are supported:

md5_crypt - MD5 Crypt

sha256_crypt - SHA-256 Crypt

sha512_crypt - SHA-512 Crypt

Some special characters, such as { and % can create templating errors. If you need to accept special characters, use the unsafe option:

An introduction to playbooks

Conditional statements in playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
---
- hosts: all
  vars_prompt:

    - name: username
      prompt: What is your username?
      private: false

    - name: password
      prompt: What is your password?

  tasks:

    - name: Print a message
      ansible.builtin.debug:
        msg: 'Logging in as {{ username }}'
```

Example 2 (unknown):
```unknown
vars_prompt:

  - name: release_version
    prompt: Product release version
    default: "1.0"
```

Example 3 (unknown):
```unknown
vars_prompt:

  - name: my_password2
    prompt: Enter password2
    private: true
    encrypt: sha512_crypt
    confirm: true
    salt_size: 7
```

Example 4 (unknown):
```unknown
vars_prompt:
  - name: my_password_with_weird_chars
    prompt: Enter password
    unsafe: true
    private: true
```

---

## Python API — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_api.html

**Contents:**
- Python API

The Ansible API is intended for internal Ansible use. Ansible may make changes to this API at any time that could break backward compatibility with older versions of the API. Because of this, external use is not supported by Ansible. If you want to use Python API only for executing playbooks or modules, consider ansible-runner first.

If you would like to use Ansible programmatically from a language other than Python, trigger events asynchronously, or have access control and logging demands, please see the AWX project.

Developing dynamic inventory integrations

Getting started on developing a module

How to develop plugins

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Lookups — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_lookups.html

**Contents:**
- Lookups
- The lookup function
- The query/q function

Lookup plugins retrieve data from outside sources such as files, databases, key/value stores, APIs, and other services. Like all templating, lookups execute and are evaluated on the Ansible control machine. Ansible makes the data returned by a lookup plugin available using the standard templating system. Before Ansible 2.5, lookups were mostly used indirectly in with_<lookup> constructs for looping. Starting with Ansible 2.5, lookups are used more explicitly as part of Jinja2 expressions fed into the loop keyword.

You can use the lookup function to populate variables dynamically. Ansible evaluates the value each time it is executed in a task (or template).

The first argument to the lookup function is required and specifies the name of the lookup plugin. If the lookup plugin is in a collection, the fully qualified name must be provided, since the collections keyword does not apply to lookup plugins.

The lookup function also accepts an optional boolean keyword wantlist, which defaults to False. When True, the result of the lookup is ensured to be a list.

Refer to the lookup plugin’s documentation to see plugin-specific arguments and keywords.

This function is shorthand for lookup(..., wantlist=True). These are equivalent:

For more details and a list of lookup plugins in ansible-core, see Working with plugins. You may also find lookup plugins in collections. You can review a list of lookup plugins installed on your control machine with the command ansible-doc -l -t lookup.

An introduction to playbooks

Conditional statements in playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
vars:
  motd_value: "{{ lookup('file', '/etc/motd') }}"
tasks:
  - debug:
      msg: "motd value is {{ motd_value }}"
```

Example 2 (unknown):
```unknown
block:
  - debug:
      msg: "{{ item }}"
    loop: "{{ lookup('ns.col.lookup_items', wantlist=True) }}"

  - debug:
      msg: "{{ item }}"
    loop: "{{ q('ns.col.lookup_items') }}"
```

---

## Using variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_variables.html

**Contents:**
- Using variables
- Creating valid variable names
- Simple variables
  - Defining simple variables
  - Referencing simple variables
- When to quote variables (a YAML gotcha)
- List variables
  - Defining variables as lists
  - Referencing list variables
- Dictionary variables

Ansible uses variables to manage differences between systems. With Ansible, you can execute tasks and playbooks on multiple systems with a single command. To represent the variations among those different systems, you can create variables with standard YAML syntax, including lists and dictionaries. You can define these variables in your playbooks, in your inventory, in reusable files or roles, or at the command line. You can also create variables during a playbook run by registering the return value of a task as a new variable.

After you create a variable, you can use it in module arguments, in conditional “when” statements, in templates, and in loops.

After you understand the concepts and examples on this page, read about Ansible facts, which are variables you retrieve from remote systems.

Creating valid variable names

Defining simple variables

Referencing simple variables

When to quote variables (a YAML gotcha)

Defining variables as lists

Referencing list variables

Defining variables as key-value dictionaries

Referencing key-value dictionary variables

Combining list variables

Combining dictionary variables

Using the merge_variables lookup

Registering variables

Referencing nested variables

Transforming variables with Jinja2 filters

Where to set variables

Defining variables in inventory

Defining variables in a play

Defining variables in included files and roles

Defining variables at runtime

Vars from a JSON or YAML file

Variable precedence: where should I put a variable?

Understanding variable precedence

Tips on where to set variables

Using advanced variable syntax

Not all strings are valid Ansible variable names. A variable name can only include letters, numbers, and underscores. Python keywords or playbook keywords are not valid variable names. A variable name cannot begin with a number.

Variable names can begin with an underscore. In many programming languages, variables that begin with an underscore are private. This is not true in Ansible. Ansible treats variables that begin with an underscore the same as any other variable. Do not rely on this convention for privacy or security.

This table gives examples of valid and invalid variable names:

*foo, Python keywords such as async and lambda

playbook keywords such as environment

foo-port, foo port, foo.port

Ansible defines certain variables internally. You cannot define these variables.

Avoid variable names that overwrite Jinja2 global functions listed in Working with playbooks, such as lookup, query, q, now, and undef.

Simple variables combine a variable name with a single value. You can use this syntax, and the syntax for lists and dictionaries shown below, in a variety of places. For details about setting variables in inventory, in playbooks, in reusable files, in roles, or at the command line, see Where to set variables.

You can define a simple variable using standard YAML syntax. For example:

After you define a variable, use Jinja2 syntax to reference it. Jinja2 variables use double curly braces. For example, the expression My amp goes to {{ max_amp_value }} demonstrates the most basic form of variable substitution. You can use Jinja2 syntax in playbooks. The following example shows a variable that defines the location of a file, which can vary from one system to another:

Ansible allows Jinja2 loops and conditionals in templates but not in playbooks. You cannot create a loop of tasks. Ansible playbooks are pure machine-parseable YAML.

If you start a value with {{ foo }}, you must quote the whole expression to create valid YAML syntax. If you do not quote the whole expression, the YAML parser cannot interpret the syntax. The parser cannot determine if it is a variable or the start of a YAML dictionary. For guidance on writing YAML, see the YAML Syntax documentation.

If you use a variable without quotes, like this:

You will see: ERROR! Syntax Error while loading YAML. If you add quotes, Ansible works correctly:

A list variable combines a variable name with multiple values. You can store the multiple values as an itemized list or in square brackets [], separated with commas.

You can define variables with multiple values using YAML lists. For example:

If you use a variable defined as a list (also called an array), you can use individual, specific items from that list. The first item in a list is item 0, the second item is item 1, and so on. For example:

The value of this expression would be “northeast”.

A dictionary stores data in key-value pairs. Usually, you use dictionaries to store related data, such as the information contained in an ID or a user profile.

You can define more complex variables using YAML dictionaries. A YAML dictionary maps keys to values. For example:

If you use a variable defined as a key-value dictionary (also called a hash), you can use individual, specific items from that dictionary using either bracket notation or dot notation:

Both of these examples reference the same value (“one”). Bracket notation always works. Dot notation can cause problems because some keys collide with attributes and methods of python dictionaries. Use bracket notation if you use keys that start and end with two underscores, which are reserved for special meanings in python, or are any of the known public attributes:

add, append, as_integer_ratio, bit_length, capitalize, center, clear, conjugate, copy, count, decode, denominator, difference, difference_update, discard, encode, endswith, expandtabs, extend, find, format, fromhex, fromkeys, get, has_key, hex, imag, index, insert, intersection, intersection_update, isalnum, isalpha, isdecimal, isdigit, isdisjoint, is_integer, islower, isnumeric, isspace, issubset, issuperset, istitle, isupper, items, iteritems, iterkeys, itervalues, join, keys, ljust, lower, lstrip, numerator, partition, pop, popitem, real, remove, replace, reverse, rfind, rindex, rjust, rpartition, rsplit, rstrip, setdefault, sort, split, splitlines, startswith, strip, swapcase, symmetric_difference, symmetric_difference_update, title, translate, union, update, upper, values, viewitems, viewkeys, viewvalues, zfill.

To merge variables that contain lists or dictionaries, you can use the following approaches.

You can use the set_fact module to combine lists into a new merged_list variable as follows:

To merge dictionaries, use the combine filter. For example:

For more details, see ansible.builtin.combine .

To merge variables that match the given prefixes, suffixes, or regular expressions, you can use the community.general.merge_variables lookup. For example:

For more details and example usage, refer to the community.general.merge_variables lookup documentation.

You can create a variable from the output of an Ansible task with the task keyword register. You can use the registered variable in any later task in your play. For example:

For more examples of using registered variables in conditions on later tasks, see Conditionals. Registered variables may be simple variables, list variables, dictionary variables, or complex nested data structures. The documentation for each module includes a RETURN section that describes the return values for that module. To see the values for a particular task, run your playbook with -v.

Registered variables are stored in memory. You cannot cache registered variables for use in future playbook runs. A registered variable is valid only on the host for the rest of the current playbook run, including subsequent plays within the same playbook run.

Registered variables are host-level variables. When you register a variable in a task with a loop, the registered variable contains a value for each item in the loop. The data structure placed in the variable during the loop contains a results attribute, which is a list of all responses from the module. For a more in-depth example of how this works, see the Loops section on using register with a loop.

If a task fails or is skipped, Ansible still registers a variable with a failure or skipped status, unless the task is skipped based on tags. See Tags for information on adding and using tags.

Many registered variables and facts are nested YAML or JSON data structures. You cannot access values from these nested data structures with the simple {{ foo }} syntax. You must use either bracket notation or dot notation. For example, to reference an IP address from your facts using bracket notation:

To reference an IP address from your facts using dot notation:

Jinja2 filters let you transform the value of a variable within a template expression. For example, the capitalize filter capitalizes any value passed to it; the to_yaml and to_json filters change the format of your variable values. Jinja2 includes many built-in filters, and Ansible supplies many more filters. To find more examples of filters, see Using filters to manipulate data.

You can define variables in a variety of places, such as in inventory, in playbooks, in reusable files, in roles, and at the command line. Ansible loads every possible variable it finds, then chooses the variable to apply based on variable precedence rules.

You can define different variables for each host individually, or set shared variables for a group of hosts in your inventory. For example, if all machines in the [boston] group use ‘boston.ntp.example.com’ as an NTP server, you can set a group variable. The How to build your inventory page has details on setting host variables and group variables in inventory.

You can define variables directly in a playbook play:

When you define variables in a play, they are visible only to tasks executed in that play.

You can define variables in reusable variables files or in reusable roles. If you define variables in reusable variable files, the sensitive variables are separated from playbooks. This separation enables you to store your playbooks in a source control software and even share the playbooks, without the risk of exposing passwords or other sensitive and personal data. For information about creating reusable files and roles, see Reusing Ansible artifacts.

This example shows how you can include variables defined in an external file:

The contents of each variables file is a simple YAML dictionary. For example:

You can keep per-host and per-group variables in similar files. To learn about organizing your variables, see Organizing host and group variables.

You can define variables when you run your playbook by passing variables at the command line using the --extra-vars (or -e) argument. You can also request user input with a vars_prompt (see Interactive input: prompts). If you pass variables at the command line, use a single quoted string that contains one or more variables in one of the formats below.

Values passed in using the key=value syntax are interpreted as strings. Use the JSON format if you need to pass non-string values such as Booleans, integers, floats, and lists.

When passing variables with --extra-vars, you must escape quotes and other special characters appropriately for both your markup (for example, JSON) and for your shell:

If you have a lot of special characters, use a JSON or YAML file containing the variable definitions. Prepend both JSON and YAML file names with @.

You can set multiple variables with the same name in many different places. If you do this, Ansible loads every possible variable it finds, and then chooses the variable to apply based on variable precedence. In other words, the different variables will override each other in a certain order.

Teams and projects that agree on guidelines for defining variables (where to define certain types of variables) usually avoid variable precedence concerns. You should define each variable in one place. Determine where to define a variable, and keep it simple. For examples, see Tips on where to set variables.

Some behavioral parameters that you can set in variables you can also set in Ansible configuration, as command-line options, and using playbook keywords. For example, you can define the user that Ansible uses to connect to remote devices as a variable with ansible_user, in a configuration file with DEFAULT_REMOTE_USER, as a command-line option with -u, and with the playbook keyword remote_user. If you define the same parameter in a variable and by another method, the variable overrides the other setting. This approach allows host-specific settings to override more general settings. For examples and more details on the precedence of these various settings, see Controlling how Ansible behaves: precedence rules.

Ansible does apply variable precedence, and you might have a use for it. Here is the order of precedence from least to greatest (the last listed variables override all other variables):

Command-line values (for example, -u my_user, these are not variables)

Role defaults (as defined in Role directory structure) [1]

Inventory file or script group vars [2]

Inventory group_vars/all [3]

Playbook group_vars/all [3]

Inventory group_vars/* [3]

Playbook group_vars/* [3]

Inventory file or script host vars [2]

Inventory host_vars/* [3]

Playbook host_vars/* [3]

Host facts and cached set_facts [4]

Role vars (as defined in Role directory structure)

Block vars (for tasks in block only)

Task vars (for the task only)

Registered vars and set_facts

Role (and include_role) params

Extra vars (for example, -e "user=my_user")(always win precedence)

In general, Ansible gives precedence to variables that were defined more recently, more actively, and with more explicit scope. Variables in the defaults folder inside a role are easily overridden. Anything in the vars directory of the role overrides previous versions of that variable in the namespace. Host or inventory variables override role defaults, but explicit includes such as the vars directory or an include_vars task override inventory variables.

Ansible merges different variables set in inventory so that more specific settings override more generic settings. For example, ansible_ssh_user specified as a group_var is overridden by ansible_user specified as a host_var. For details about the precedence of variables set in inventory, see How variables are merged.

Tasks in each role see their own role’s defaults. Tasks defined outside of a role see the last role’s defaults.

Variables defined in inventory file or provided by dynamic inventory.

Includes vars added by ‘vars plugins’ as well as host_vars and group_vars which are added by the default vars plugin shipped with Ansible.

When created with set_facts’s cacheable option, variables have the high precedence in the play, but are the same as a host facts precedence when they come from the cache.

Within any section, redefining a var overrides the previous instance. If multiple groups have the same variable, the last one loaded wins. If you define a variable twice in a play’s vars: section, the second one wins.

The previous text describes the default config hash_behavior=replace. Switch to merge to overwrite only partially.

You can decide where to set a variable based on the scope you want that value to have. Ansible has three main scopes:

Global: this is set by config, environment variables and the command line

Play: each play and contained structures, vars entries (vars; vars_files; vars_prompt), role defaults and vars.

Host: variables directly associated to a host, like inventory, include_vars, facts or registered task outputs

Inside a template, you automatically have access to all variables that are in scope for a host, plus any registered variables, facts, and magic variables.

You should choose where to define a variable based on the kind of control you might want over values.

Set variables in inventory that deal with geography or behavior. Since groups are frequently the entity that maps roles to hosts, you can often set variables on the group instead of defining them on a role. Remember that child groups override parent groups, and host variables override group variables. See Defining variables in inventory for details on setting host and group variables.

Set common defaults in a group_vars/all file. See Organizing host and group variables for details on how to organize host and group variables in your inventory. You generally place group variables alongside your inventory file, but they can also be returned by dynamic inventory (see Working with dynamic inventory) or defined in AWX or on the Red Hat Ansible Automation Platform from the UI or API:

Set location-specific variables in group_vars/my_location files. All groups are children of the all group, so variables set here override those set in group_vars/all:

If one host used a different NTP server, you could set that in a host_vars file, which would override the group variable:

Set defaults in roles to avoid undefined-variable errors. If you share your roles, other users can rely on the reasonable defaults you added in the roles/x/defaults/main.yml file, or they can easily override those values in inventory or at the command line. See Roles for more info. For example:

Set variables in roles to ensure a value is used in that role and is not overridden by inventory variables. If you are not sharing your role with others, you can define app-specific behaviors like ports this way, in roles/x/vars/main.yml. If you are sharing roles with others, putting variables here makes them harder to override, although they can still be overridden by passing a parameter to the role or setting a variable with -e:

Pass variables as parameters when you call roles for maximum clarity, flexibility, and visibility. This approach overrides any defaults that exist for a role. For example:

When you read this playbook, it is clear that you have chosen to set a variable or override a default. You can also pass multiple values, which allows you to run the same role multiple times. See Running a role multiple times in one play for more details. For example:

Variables set in one role are available to later roles. You can set variables in the role’s vars directory (as defined in Role directory structure) and use them in other roles and elsewhere in your playbook:

There are some protections in place to avoid the need to namespace variables. In this example, variables defined in ‘common_settings’ are available to ‘something’ and ‘something_else’ tasks, but tasks in ‘something’ have foo set at 12, even if ‘common_settings’ sets foo to 20.

Instead of worrying about variable precedence, we encourage you to think about how easily or how often you want to override a variable when deciding where to set it. If you are not sure what other variables are defined and you need a particular value, use --extra-vars (-e) to override all other variables.

For information about advanced YAML syntax used to declare variables and have more control over the data placed in YAML files used by Ansible, see Advanced playbook syntax.

An introduction to playbooks

Conditional statements in playbooks

Jinja2 filters and their uses

Playbook organization by roles

Tips and tricks for playbooks

List of special variables

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
remote_install_path: /opt/my_app_config
```

Example 2 (unknown):
```unknown
ansible.builtin.template:
  src: foo.cfg.j2
  dest: '{{ remote_install_path }}/foo.cfg'
```

Example 3 (unknown):
```unknown
- hosts: app_servers
  vars:
    app_path: {{ base_path }}/22
```

Example 4 (unknown):
```unknown
- hosts: app_servers
  vars:
    app_path: "{{ base_path }}/22"
```

---

## Ansible collection creator path — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_path.html

**Contents:**
- Ansible collection creator path
- Examine currently available solutions
- Create your content
- Put your content in a collection
- Write good user collection documentation
- Publish your collection source code
- Follow a versioning convention
- Understand and implement testing and CI
  - Add tests
  - Implement continuous integration

If you are unfamiliar with Ansible collections, first take a look at the Using Ansible collections guide.

Ansible collections are a distribution format for Ansible content that can include playbooks, roles, modules, and plugins. A typical collection addresses a set of related use cases. For example, the community.dns collection includes modules and plugins to work with DNS.

You can install collections made by others or share yours with the community through a distribution server such as Ansible Galaxy. Certified collections can be published to the Red Hat Automation Hub, a part of the Red Hat Ansible Automation Platform.

Creating and sharing collections is a great way of contributing to the Ansible project.

The Ansible community package consists of ansible-core, which, among other core components, includes the ansible.builtin collection maintained by the Core team, and a set of collections maintained by the community.

The purpose of this guide is to give you as a (potential) content creator a consistent overview of the Ansible collection creator journey from an idea for the first module/role to having your collection included in the Ansible community package. The Collection development guidelines section provides references to more detailed aspects of this journey. The overall journey consists of the following milestones:

Examine currently available solutions

Put your content in a collection

Write good user collection documentation

Publish your collection source code

Follow a versioning convention

Understand and implement testing and CI

Implement continuous integration

Provide good contributor & maintainer documentation

Publish your collection on distribution servers

Make your collection a part of Ansible community package

If you have an idea for a new role or module/plugin, there is no need to reinvent the wheel if there is already a sufficient solution that solves your automation issue.

Therefore, first examine the currently available content including:

Ansible builtin modules and plugins

Ansible package collection index

Ansible Automation Hub if you have the Ansible Automation Platform subscription

In case the solutions you found are not fully sufficient or have flaws, consider improving them rather than creating your own. Each collection includes information on where to create issues for that collection to propose your enhancement ideas.

If you already have your content written and used in your workflows, you can still consider integrating it to the existing solutions. However, if these options do not apply to your collection ideas, we encourage you to create and share your own.

You tried but have not found any sufficient solution for your automation issue.

Use one of the following guides:

Roles guide: if you want to create a role.

Developer guide: if you want to create a new Ansible module or plugin for your personal use.

You created new content.

Now it is time to create a reusable and sharable collection. Use the Developing collections guide to learn how.

We recommend you to use the collection_template repository as a basis for your collection.

Your collection README.md file should contain a quick-start installation and usage guides. You can use the community.general collection README file as an example.

If your collection contains modules or plugins, make sure their documentation is comprehensive. Use the Module format and documentation guide and Ansible documentation style guide to learn more.

Publish your collection on a platform for software development and version control such as GitHub.

It can be your personal repository or your organization’s one. You can also request a repository under the ansible-collections organization.

Make sure your collection contains exhaustive license information. Ansible is an open source project, so we encourage you to license it under one of open source licenses. If you plan to submit your collection for inclusion in the Ansible community package, your collection must satisfy the licensing requirements.

If you have used the collection_template repository we recommended earlier as a skeleton for your collection, it already contains the GNU GPL v3 license.

When releasing new versions of your collections, take the following recommended practices into consideration:

Follow a versioning convention. Using SemVer is highly recommended.

Base your releases on Git tags.

This section is applicable to collections containing modules and plugins.

For role testing, see the Ansible Molecule project.

Testing your collection ensures that your code works well and integrates with other components such as ansible-core.

Take a look at the following documents:

Testing Ansible guide: provides general information about testing.

Testing collections guide: contains collection-specific testing information.

Now make sure when pull requests are created in your collection repository they are automatically tested using a CI tool such as GitHub Actions or Azure Pipelines.

The collection_template repository contains GitHub Actions templates you can adjust and use to enable the workflows in your repository.

See the collection_template/README.md as an example.

To distribute your collection and allow others to conveniently use it, publish your collection on one or more distribution servers. See the Distributing collections guide to learn how.

Make you collection satisfy the Ansible community package collections requirements and submit it for inclusion. See the inclusion process description to learn how.

Maintain your collection. See the Ansible collection maintainer guidelines for details.

Engage with the community. Take a look at the Ansible communication guide to see available communication options.

A set of guidelines about collection development aspects

---

## The now function: get the current time — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_templating_now.html

**Contents:**
- The now function: get the current time

The now() Jinja2 function retrieves a Python datetime object or a string representation for the current time.

The now() function supports two arguments:

Specify True to get the current time in UTC. Defaults to False.

Accepts a strftime string that returns a formatted date time string.

For example: dtg: "Current time (UTC): {{ now(utc=true,fmt='%Y-%m-%d %H:%M:%S') }}"

---

## Ansible module architecture — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_program_flow_modules.html

**Contents:**
- Ansible module architecture
- Types of modules
  - Action plugins
  - New-style modules
    - Python
    - PowerShell
  - JSONARGS modules
  - Non-native want JSON modules
  - Binary modules
  - Old-style modules

If you are working on the ansible-core code, writing an Ansible module, or developing an action plugin, you may need to understand how Ansible’s program flow executes. If you are just using Ansible Modules in playbooks, you can skip this section.

Non-native want JSON modules

How modules are executed

Executor/task_executor

The normal action plugin

Executor/module_common.py

Module Replacer framework

_ansible_selinux_special_fs

_ansible_syslog_facility

_ansible_keep_remote_files

_ansible_shell_executable

Module return values & Unsafe strings

Special considerations

Why pass args over stdin?

Dependencies between module options

Declaring check mode support

Ansible supports several different types of modules in its code base. Some of these are for backwards compatibility and others are to enable flexibility.

Action plugins look like modules to anyone writing a playbook. Usage documentation for most action plugins lives inside a module of the same name. Some action plugins do all the work, with the module providing only documentation. Some action plugins execute modules. The normal action plugin executes modules that don’t have special action plugins. Action plugins always execute on the control node.

Some action plugins do all their work on the control node. For example, the debug action plugin (which prints text for the user to see) and the assert action plugin (which tests whether values in a playbook satisfy certain criteria) execute entirely on the control node.

Most action plugins set up some values on the control node, then invoke an actual module on the managed node that does something with these values. For example, the template action plugin takes values from the user to construct a file in a temporary location on the control node using variables from the playbook environment. It then transfers the temporary file to a temporary file on the remote system. After that, it invokes the copy module which operates on the remote system to move the file into its final location, sets file permissions, and so on.

All of the modules that ship with Ansible fall into this category. While you can write modules in any language, all official modules (shipped with Ansible) use either Python or PowerShell.

New-style modules have the arguments to the module embedded inside of them in some manner. Old-style modules must copy a separate file over to the managed node, which is less efficient as it requires two over-the-wire connections instead of only one.

New-style Python modules use the Ansiballz framework framework for constructing modules. These modules use imports from ansible.module_utils to pull in boilerplate module code, such as argument parsing, formatting of return values as JSON, and various file operations.

In Ansible, up to version 2.0.x, the official Python modules used the Module Replacer framework framework. For module authors, Ansiballz framework is largely a superset of Module Replacer framework functionality, so you usually do not need to understand the differences between them.

New-style PowerShell modules use the Module Replacer framework framework for constructing modules. These modules get a library of PowerShell code embedded in them before being sent to the managed node.

These modules are scripts that include the string <<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>> in their body. This string is replaced with the JSON-formatted argument string. These modules typically set a variable to that value like this:

Which is expanded as:

Ansible outputs a JSON string with bare quotes. Double quotes are used to quote string values, double quotes inside of string values are backslash escaped, and single quotes may appear unescaped inside of a string value. To use JSONARGS, your scripting language must have a way to handle this type of string. The example uses Python’s triple quoted strings to do this. Other scripting languages may have a similar quote character that won’t be confused by any quotes in the JSON or it may allow you to define your own start-of-quote and end-of-quote characters. If the language doesn’t give you any of these then you’ll need to write a non-native JSON module or Old-style module instead.

These modules typically parse the contents of json_arguments using a JSON library and then use them as native variables throughout the code.

If a module has the string WANT_JSON in it anywhere, Ansible treats it as a non-native module that accepts a file name as its only command-line parameter. The file name is for a temporary file containing a JSON string containing the module’s parameters. The module needs to open the file, read and parse the parameters, operate on the data, and print its return data as a JSON encoded dictionary to stdout before exiting.

These types of modules are self-contained entities. As of Ansible 2.1, Ansible only modifies them to change a shebang line if present.

Examples of Non-native modules written in ruby are in the Ansible for Rubyists repository.

From Ansible 2.2 onwards, modules may also be small binary programs. Ansible doesn’t perform any magic to make these portable to different systems so they may be specific to the system on which they were compiled or require other binary runtime dependencies. Despite these drawbacks, you may have to compile a custom module against a specific binary library if that’s the only way to get access to certain resources.

Binary modules take their arguments and return data to Ansible in the same way as want JSON modules.

One example of a binary module written in go.

Old-style modules are similar to want JSON modules, except that the file that they take contains key=value pairs for their parameters instead of JSON. Ansible decides that a module is old-style when it doesn’t have any of the markers that would show that it is one of the other types.

When a user uses ansible or ansible-playbook, they specify a task to execute. The task is usually the name of a module along with several parameters to be passed to the module. Ansible takes these values and processes them in various ways before they are finally executed on the remote machine.

The TaskExecutor receives the module name and parameters that were parsed from the playbook (or from the command-line in the case of /usr/bin/ansible). It uses the name to decide whether it is looking at a module or an Action Plugin. If it is a module, it loads the Normal Action Plugin and passes the name, variables, and other information about the task and play to that Action Plugin for further processing.

The normal action plugin executes the module on the remote host. It is the primary coordinator of much of the work to actually execute the module on the managed machine.

It loads the appropriate connection plugin for the task, which then transfers or executes as needed to create a connection to that host.

It adds any internal Ansible properties to the module’s parameters (for instance, the ones that pass along no_log to the module).

It works with other plugins (connection, shell, become, other action plugins) to create any temporary files on the remote machine and cleans up afterwards.

It pushes the module and module parameters to the remote host, although the module_common code described in the next section decides which format those will take.

It handles any special cases regarding modules (for example, async execution, or complications around Windows modules that must have the same names as Python modules, so that internal calling of modules from other Action Plugins work.)

Much of this functionality comes from the BaseAction class, which lives in plugins/action/__init__.py. It uses the Connection and Shell objects to do its work.

When tasks are run with the async: parameter, Ansible uses the async Action Plugin instead of the normal Action Plugin to invoke it. That program flow is currently not documented. Read the source for information on how that works.

Code in executor/module_common.py assembles the module to be shipped to the managed node. The module is first read in, then examined to determine its type:

PowerShell and JSON-args modules are passed through Module Replacer.

New-style Python modules are assembled by Ansiballz framework.

Non-native-want-JSON, Binary modules, and Old-Style modules aren’t touched by either of these and pass through unchanged.

After the assembling step, one final modification is made to all modules that have a shebang line. Ansible checks whether the interpreter in the shebang line has a specific path configured with an ansible_$X_interpreter inventory variable. If it does, Ansible substitutes that path for the interpreter path given in the module. After this, Ansible returns the complete module data and the module type to the Normal Action which continues execution of the module.

Ansible supports two assembler frameworks: Ansiballz and the older Module Replacer.

The Module Replacer framework is the original framework implementing new-style modules, and is still used for PowerShell modules. It is essentially a preprocessor (like the C Preprocessor for those familiar with that programming language). It does straight substitutions of specific substring patterns in the module file. There are two types of substitutions:

Replacements that only happen in the module file. These are public replacement strings that modules can utilize to get helpful boilerplate or access to arguments.

from ansible.module_utils.MOD_LIB_NAME import * is replaced with the contents of the ansible/module_utils/MOD_LIB_NAME.py These should only be used with new-style Python modules.

#<<INCLUDE_ANSIBLE_MODULE_COMMON>> is equivalent to from ansible.module_utils.basic import * and should also only apply to new-style Python modules.

# POWERSHELL_COMMON substitutes the contents of ansible/module_utils/powershell.ps1. It should only be used with new-style Powershell modules.

Replacements that are used by ansible.module_utils code. These are internal replacement patterns. They may be used internally, in the above public replacements, but shouldn’t be used directly by modules.

"<<ANSIBLE_VERSION>>" is substituted with the Ansible version. In new-style Python modules under the Ansiballz framework framework the proper way is to instead instantiate an AnsibleModule and then access the version from :attr:AnsibleModule.ansible_version.

"<<INCLUDE_ANSIBLE_MODULE_COMPLEX_ARGS>>" is substituted with a string which is the Python repr of the JSON encoded module parameters. Using repr on the JSON string makes it safe to embed in a Python file. In new-style Python modules under the Ansiballz framework this is better accessed by instantiating an AnsibleModule and then using AnsibleModule.params.

<<SELINUX_SPECIAL_FILESYSTEMS>> substitutes a string which is a comma-separated list of file systems which have a file system dependent security context in SELinux. In new-style Python modules, if you really need this you should instantiate an AnsibleModule and then use AnsibleModule._selinux_special_fs. The variable has also changed from a comma-separated string of file system names to an actual python list of file system names.

<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>> substitutes the module parameters as a JSON string. Care must be taken to properly quote the string as JSON data may contain quotes. This pattern is not substituted in new-style Python modules as they can get the module parameters another way.

The string syslog.LOG_USER is replaced wherever it occurs with the syslog_facility which was named in ansible.cfg or any ansible_syslog_facility inventory variable that applies to this host. In new-style Python modules this has changed slightly. If you really need to access it, you should instantiate an AnsibleModule and then use AnsibleModule._syslog_facility to access it. It is no longer the actual syslog facility and is now the name of the syslog facility. See the documentation on internal arguments for details.

The Ansiballz framework was adopted in Ansible 2.1 and is used for all new-style Python modules. Unlike the Module Replacer, Ansiballz uses real Python imports of things in ansible/module_utils instead of merely preprocessing the module. It does this by constructing a zipfile – which includes the module file, files in ansible/module_utils that are imported by the module, and some boilerplate to pass in the module’s parameters. The zipfile is then Base64 encoded and wrapped in a small Python script which decodes the Base64 encoding and places the zipfile into a temp directory on the managed node. It then extracts just the Ansible module script from the zip file and places that in the temporary directory as well. Then it sets the PYTHONPATH to find Python modules inside of the zip file and imports the Ansible module as the special name, __main__. Importing it as __main__ causes Python to think that it is executing a script rather than simply importing a module. This lets Ansible run both the wrapper script and the module code in a single copy of Python on the remote machine.

Ansible wraps the zipfile in the Python script for two reasons:

for compatibility with Python 2.6 which has a less functional version of Python’s -m command-line switch.

so that pipelining will function properly. Pipelining needs to pipe the Python module into the Python interpreter on the remote node. Python understands scripts on stdin but does not understand zip files.

Prior to Ansible 2.7, the module was executed by a second Python interpreter instead of being executed inside of the same process. This change was made once Python-2.4 support was dropped to speed up module execution.

In Ansiballz, any imports of Python modules from the ansible.module_utils package trigger inclusion of that Python file into the zipfile. Instances of #<<INCLUDE_ANSIBLE_MODULE_COMMON>> in the module are turned into from ansible.module_utils.basic import * and ansible/module-utils/basic.py is then included in the zipfile. Files that are included from module_utils are themselves scanned for imports of other Python modules from module_utils to be included in the zipfile as well.

Arguments are passed differently by the two frameworks:

In Module Replacer framework, module arguments are turned into a JSON-ified string and substituted into the combined module file.

In Ansiballz framework, the JSON-ified string is part of the script which wraps the zipfile. Just before the wrapper script imports the Ansible module as __main__, it monkey-patches the private, _ANSIBLE_ARGS variable in basic.py with the variable values. When a ansible.module_utils.basic.AnsibleModule is instantiated, it parses this string and places the args into AnsibleModule.params where it can be accessed by the module’s other code.

If you are writing modules, remember that the way we pass arguments is an internal implementation detail: it has changed in the past and will change again as soon as changes to the common module_utils code allow Ansible modules to forgo using ansible.module_utils.basic.AnsibleModule. Do not rely on the internal global _ANSIBLE_ARGS variable.

Very dynamic custom modules which need to parse arguments before they instantiate an AnsibleModule may use _load_params to retrieve those parameters. Although _load_params may change in breaking ways if necessary to support changes in the code, it is likely to be more stable than either the way we pass parameters or the internal global variable.

Prior to Ansible 2.7, the Ansible module was invoked in a second Python interpreter and the arguments were then passed to the script over the script’s stdin.

Both Module Replacer framework and Ansiballz framework send additional arguments to the Ansible module beyond those which the user specified in the playbook. These additional arguments are internal parameters that help implement global Ansible features. Modules often do not need to know about these explicitly because the features are implemented in ansible.module_utils.basic. However, certain features need support from modules and some knowledge of the internal arguments is useful.

The internal arguments in this section are global. If you need to add a local internal argument to a custom module, create an action plugin for that specific module. See _original_basename in the copy action plugin for an example.

Set to True whenever an argument in a task or play specifies no_log. Any module that calls the AnsibleModule.log() function handles this action automatically. If you have a module that implements its own logging then you need to check the value of _ansible_no_log. To access _ansible_no_log in a module, instantiate the AnsibleModule utility and then check the value of AnsibleModule.no_log.

no_log specified in a module’s argument_spec is handled by a different mechanism.

Operates verbose logging and logging of external commands that a module executes. If the module uses the AnsibleModule.debug() function rather than the AnsibleModule.log() function then the messages are only logged if you set the _ansible_debug argument to True. To access _ansible_debug in a module, instantiate the AnsibleModule utility and access AnsibleModule._debug. For more details, see DEFAULT_DEBUG.

With this parameter you can configure your module to show a unified diff of changes that will be applied to the templated files. To access _ansible_diff in a module, instantiate the AnsibleModule utility and access AnsibleModule._diff. You can also access this parameter using the diff keyword in your playbook, or the relevant environment variable. For more details, see Playbook Keywords and the DIFF_ALWAYS configuration option.

You can use this argument to control the level (0 for none) of verbosity in logging.

Type: list Elements: strings

This argument provides modules with the names of file systems which should have a special SELinux context. They are used by the AnsibleModule methods which operate on files (changing attributes, moving, and copying).

Most modules can use the built-in AnsibleModule methods to manipulate files. To access in a module that needs to know about these special context file systems, instantiate AnsibleModule and examine the list in AnsibleModule._selinux_special_fs.

This argument replaces ansible.module_utils.basic.SELINUX_SPECIAL_FS from Module Replacer framework. In the module replacer framework the argument was formatted as a comma-separated string of file system names. Under the Ansiballz framework it is a list. You can access _ansible_selinux_special_fs using the corresponding environment variable. For more details, see the DEFAULT_SELINUX_SPECIAL_FS configuration option.

This argument controls which syslog facility the module logs to. Most modules should just use the AnsibleModule.log() function which will then make use of this. If a module has to use this on its own, it should instantiate the AnsibleModule method and then retrieve the name of the syslog facility from AnsibleModule._syslog_facility. The Ansiballz code is less elegant than the Module Replacer framework code:

For more details, see the DEFAULT_SYSLOG_FACILITY configuration option.

This argument passes the version of Ansible to the module. To access it, a module should instantiate the AnsibleModule method and then retrieve the version from AnsibleModule.ansible_version. This replaces ansible.module_utils.basic.ANSIBLE_VERSION from Module Replacer framework.

This argument passes the information to modules about their name. For more details see, the configuration option DEFAULT_MODULE_NAME.

This argument provides instructions that modules must be ready if they need to keep the remote files. For more details, see the DEFAULT_KEEP_REMOTE_FILES configuration option.

This argument provides modules with a socket for persistent connections. The argument is created using the PERSISTENT_CONTROL_PATH_DIR configuration option.

This argument ensures that modules use the designated shell executable. For more details, see the ansible_shell_executable remote host environment parameter.

This argument provides instructions to modules that all commands must use the designated temporary directory, if created. The action plugin designs this temporary directory.

Modules can access this parameter by using the public tmpdir property. The tmpdir property will create a temporary directory if the action plugin did not set the parameter.

The directory name is generated randomly, and the the root of the directory is determined by one of these:

As a result, using the ansible.cfg configuration file to activate or customize this setting will not guarantee that you control the full value.

The module’s tmpdir property creates a randomized directory name in this directory if the action plugin did not set _ansible_tmpdir. For more details, see the remote_tmp parameter of the shell plugin.

At the end of a module’s execution, it formats the data that it wants to return as a JSON string and prints the string to its stdout. The normal action plugin receives the JSON string, parses it into a Python dictionary, and returns it to the executor.

If Ansible templated every string return value, it would be vulnerable to an attack from users with access to managed nodes. If an unscrupulous user disguised malicious code as Ansible return value strings, and if those strings were then templated on the control node, Ansible could execute arbitrary code. To prevent this scenario, Ansible marks all strings inside returned data as Unsafe, emitting any Jinja2 templates in the strings verbatim, not expanded by Jinja2.

Strings returned by invoking a module through ActionPlugin._execute_module() are automatically marked as Unsafe by the normal action plugin. If another action plugin retrieves information from a module through some other means, it must mark its return data as Unsafe on its own.

In case a poorly-coded action plugin fails to mark its results as “Unsafe,” Ansible audits the results again when they are returned to the executor, marking all strings as Unsafe. The normal action plugin protects itself and any other code that it calls with the result data as a parameter. The check inside the executor protects the output of all other action plugins, ensuring that subsequent tasks run by Ansible will not template anything from those results either.

Ansible can transfer a module to a remote machine in one of two ways:

it can write out the module to a temporary file on the remote host and then use a second connection to the remote host to execute it with the interpreter that the module needs

or it can use what’s known as pipelining to execute the module by piping it into the remote interpreter’s stdin.

Pipelining only works with modules written in Python at this time because Ansible only knows that Python supports this mode of operation. Supporting pipelining means that whatever format the module payload takes before being sent over the wire must be executable by Python through stdin.

Passing arguments through stdin was chosen for the following reasons:

When combined with ANSIBLE_PIPELINING, this keeps the module’s arguments from temporarily being saved onto disk on the remote machine. This makes it harder (but not impossible) for a malicious user on the remote machine to steal any sensitive information that may be present in the arguments.

Command line arguments would be insecure as most systems allow unprivileged users to read the full commandline of a process.

Environment variables are usually more secure than the commandline but some systems limit the total size of the environment. This could lead to truncation of the parameters if we hit that limit.

The argument_spec provided to AnsibleModule defines the supported arguments for a module, as well as their type, defaults and more.

Example argument_spec:

This section will discuss the behavioral attributes for arguments:

type allows you to define the type of the value accepted for the argument. The default value for type is str. Possible values are:

The raw type, performs no type validation or type casting, and maintains the type of the passed value.

elements works in combination with type when type='list'. elements can then be defined as elements='int' or any other type, indicating that each element of the specified list should be of that type.

The default option allows sets a default value for the argument for the scenario when the argument is not provided to the module. When not specified, the default value is None.

fallback accepts a tuple where the first argument is a callable (function) that will be used to perform the lookup, based on the second argument. The second argument is a list of values to be accepted by the callable.

The most common callable used is env_fallback which will allow an argument to optionally use an environment variable when the argument is not supplied.

choices accepts a list of choices that the argument will accept. The types of choices should match the type.

required accepts a boolean, either True or False that indicates that the argument is required. When not specified, required defaults to False. This should not be used in combination with default.

no_log accepts a boolean, either True or False, that indicates explicitly whether or not the argument value should be masked in logs and output.

In the absence of no_log, if the parameter name appears to indicate that the argument value is a password or passphrase (such as “admin_password”), a warning will be shown and the value will be masked in logs but not output. To disable the warning and masking for parameters that do not contain sensitive information, set no_log to False.

aliases accepts a list of alternative argument names for the argument, such as the case where the argument is name but the module accepts aliases=['pkg'] to allow pkg to be interchangeably with name. Use of aliases can make module interfaces confusing, so we recommend adding them only when necessary. If you are updating argument names to fix a typo or improve the interface, consider moving the old names to deprecated_aliases rather than keeping them around indefinitely.

options implements the ability to create a sub-argument_spec, where the sub options of the top level argument are also validated using the attributes discussed in this section. The example at the top of this section demonstrates use of options. type or elements should be dict is this case.

apply_defaults works alongside options and allows the default of the sub-options to be applied even when the top-level argument is not supplied.

In the example of the argument_spec at the top of this section, it would allow module.params['top_level']['second_level'] to be defined, even if the user does not provide top_level when calling the module.

removed_in_version indicates which version of ansible-core or a collection a deprecated argument will be removed in. Mutually exclusive with removed_at_date, and must be used with removed_from_collection.

removed_at_date indicates that a deprecated argument will be removed in a minor ansible-core release or major collection release after this date. Mutually exclusive with removed_in_version, and must be used with removed_from_collection.

Specifies which collection (or ansible-core) deprecates this deprecated argument. Specify ansible.builtin for ansible-core, or the collection’s name (format foo.bar). Must be used with removed_in_version or removed_at_date.

Deprecates aliases of this argument. Must contain a list or tuple of dictionaries having some the following keys:

The name of the alias to deprecate. (Required.)

The version of ansible-core or the collection this alias will be removed in. Either version or date must be specified.

The a date after which a minor release of ansible-core or a major collection release will no longer contain this alias.. Either version or date must be specified.

Specifies which collection (or ansible-core) deprecates this deprecated alias. Specify ansible.builtin for ansible-core, or the collection’s name (format foo.bar). Must be used with version or date.

If options is specified, mutually_exclusive refers to the sub-options described in options and behaves as in Dependencies between module options.

If options is specified, required_together refers to the sub-options described in options and behaves as in Dependencies between module options.

If options is specified, required_one_of refers to the sub-options described in options and behaves as in Dependencies between module options.

If options is specified, required_if refers to the sub-options described in options and behaves as in Dependencies between module options.

If options is specified, required_by refers to the sub-options described in options and behaves as in Dependencies between module options.

You can set the value of the context key to a dict of custom content. This allows you to provide additional context in the argument spec. The content provided is not validated or utilized by the core engine.

The following are optional arguments for AnsibleModule():

Must be a sequence (list or tuple) of sequences of strings. Every sequence of strings is a list of option names which are mutually exclusive. If more than one options of a list are specified together, Ansible will fail the module with an error.

In this example, the options path and content must not specified at the same time. Also the options repository_url and repository_filename must not be specified at the same time. But specifying path and repository_url is accepted.

To ensure that precisely one of two (or more) options is specified, combine mutually_exclusive with required_one_of.

Must be a sequence (list or tuple) of sequences of strings. Every sequence of strings is a list of option names which are must be specified together. If at least one of these options are specified, the other ones from the same sequence must all be present.

In this example, if one of the options file_path or file_hash is specified, Ansible will fail the module with an error if the other one is not specified.

Must be a sequence (list or tuple) of sequences of strings. Every sequence of strings is a list of option names from which at least one must be specified. If none one of these options are specified, Ansible will fail module execution.

In this example, at least one of path and content must be specified. If none are specified, execution will fail. Specifying both is explicitly allowed; to prevent this, combine required_one_of with mutually_exclusive.

Must be a sequence of sequences. Every inner sequence describes one conditional dependency. Every sequence must have three or four values. The first two values are the option’s name and the option’s value which describes the condition. The further elements of the sequence are only needed if the option of that name has precisely this value.

If you want that all options in a list of option names are specified if the condition is met, use one of the following forms:

If you want that at least one option of a list of option names is specified if the condition is met, use the following form:

In this example, if the user specifies state=present, at least one of the options path and content must be supplied (or both). To make sure that precisely one can be specified, combine required_if with mutually_exclusive.

On the other hand, if force (a boolean parameter) is set to true, yes and so on, both force_reason and force_code must be specified.

Must be a dictionary mapping option names to sequences of option names. If the option name in a dictionary key is specified, the option names it maps to must all also be specified. Note that instead of a sequence of option names, you can also specify one single option name.

In the example, if force is specified, force_reason must also be specified. Also, if path is specified, then three three options mode, owner and group also must be specified.

To declare that a module supports check mode, supply supports_check_mode=True to the AnsibleModule() call:

The module can determine whether it is called in check mode by checking the boolean value module.check_mode. If it evaluates to True, the module must take care not to do any modification.

If supports_check_mode=False is specified, which is the default value, the module will exit in check mode with skipped=True and message remote module (<insert module name here>) does not support check mode.

To declare that a module should add support for all common file options, supply add_file_common_args=True to the AnsibleModule() call:

You can find a list of all file options here. It is recommended that you make your DOCUMENTATION extend the doc fragment ansible.builtin.files (see Documentation fragments) in this case, to make sure that all these fields are correctly documented.

The helper functions module.load_file_common_arguments() and module.set_fs_attributes_if_different() can be used to handle these arguments for you:

**Examples:**

Example 1 (unknown):
```unknown
json_arguments = """<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>"""
```

Example 2 (unknown):
```unknown
json_arguments = """{"param1": "test's quotes", "param2": "\"To be or not to be\" - Hamlet"}"""
```

Example 3 (unknown):
```unknown
# Old module_replacer way
import syslog
syslog.openlog(NAME, 0, syslog.LOG_USER)

# New Ansiballz way
import syslog
facility_name = module._syslog_facility
facility = getattr(syslog, facility_name, syslog.LOG_USER)
syslog.openlog(NAME, 0, facility)
```

Example 4 (unknown):
```unknown
module = AnsibleModule(argument_spec=dict(
    top_level=dict(
        type='dict',
        options=dict(
            second_level=dict(
                default=True,
                type='bool',
            )
        )
    )
))
```

---

## Error handling in playbooks — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/playbook_guide/playbooks_error_handling.html

**Contents:**
- Error handling in playbooks
- Ignoring failed commands
- Ignoring unreachable host errors
- Resetting unreachable hosts
- Handlers and failure
- Defining failure
- Defining “changed”
- Ensuring success for command and shell
- Aborting a play on all hosts
  - Aborting on the first error: any_errors_fatal

When Ansible receives a non-zero return code from a command or a failure from a module, by default it stops executing on that host and continues on other hosts. However, in some circumstances, you may want different behavior. Sometimes a non-zero return code indicates success. Sometimes you want a failure on one host to stop execution on all hosts. Ansible provides tools and settings to handle these situations and help you get the behavior, output, and reporting you want.

Ignoring failed commands

Ignoring unreachable host errors

Resetting unreachable hosts

Ensuring success for command and shell

Aborting a play on all hosts

Aborting on the first error: any_errors_fatal

Setting a maximum failure percentage

Controlling errors in blocks

By default, Ansible stops executing tasks on a host when a task fails on that host. You can use ignore_errors to continue despite of the failure.

The ignore_errors directive only works when the task can run and returns a value of ‘failed’. It does not make Ansible ignore undefined variable errors, connection failures, execution issues (for example, missing packages), or syntax errors.

You can ignore a task failure due to the host instance being ‘UNREACHABLE’ with the ignore_unreachable keyword. Ansible ignores the task errors but continues to execute future tasks against the unreachable host. For example, at the task level:

And at the playbook level:

If Ansible cannot connect to a host, it marks that host as ‘UNREACHABLE’ and removes it from the list of active hosts for the run. You can use meta: clear_host_errors to reactivate all hosts, so subsequent tasks can try to reach them again.

Ansible runs handlers at the end of each play. If a task notifies a handler but another task fails later in the play, by default the handler does not run on that host, which may leave the host in an unexpected state. For example, a task could update a configuration file and notify a handler to restart some service. If a task later in the same play fails, the configuration file might be changed but the service will not be restarted.

You can change this behavior with the --force-handlers command-line option, by including force_handlers: True in a play, or by adding force_handlers = True to ansible.cfg. When handlers are forced, Ansible will run all notified handlers on all hosts, even hosts with failed tasks. (Note that certain errors could still prevent the handler from running, such as a host becoming unreachable.)

Ansible lets you define what “failure” means in each task using the failed_when conditional. As with all conditionals in Ansible, lists of multiple failed_when conditions are joined with an implicit and, meaning the task only fails when all conditions are met. If you want to trigger a failure when any of the conditions is met, you must define the conditions in a string with an explicit or operator.

You may check for failure by searching for a word or phrase in the output of a command

or based on the return code

You can also combine multiple conditions for failure. This task will fail if both conditions are true:

If you want the task to fail when only one condition is satisfied, change the failed_when definition to

If you have too many conditions to fit neatly into one line, you can split it into a multi-line YAML value with >.

Ansible lets you define when a particular task has “changed” a remote node using the changed_when conditional. This lets you determine, based on return codes or output, whether a change should be reported in Ansible statistics and whether a handler should be triggered or not. As with all conditionals in Ansible, lists of multiple changed_when conditions are joined with an implicit and, meaning the task only reports a change when all conditions are met. If you want to report a change when any of the conditions is met, you must define the conditions in a string with an explicit or operator. For example:

You can also combine multiple conditions to override “changed” result.

You can reference simple variables in conditionals to avoid repeating certain terms, as in the following example:

Notice the missing double curly braces {{ }} around the log_path variable in the changed_when statement.

Just like when these two conditionals do not require templating delimiters ({{ }}) because they are raw Jinja2 expressions.

If you still use them, ansible will raise a warning that conditional statements should not include jinja2 templating delimiters.

See Defining failure for more conditional syntax examples.

The command and shell modules care about return codes, so if you have a command whose successful exit code is not zero, you can do this:

Sometimes you want a failure on a single host, or failures on a certain percentage of hosts, to abort the entire play on all hosts. You can stop play execution after the first failure happens with any_errors_fatal. For finer-grained control, you can use max_fail_percentage to abort the run after a given percentage of hosts has failed.

If you set any_errors_fatal and a task returns an error, Ansible finishes the fatal task on all hosts in the current batch and then stops executing the play on all hosts. Subsequent tasks and plays are not executed. You can recover from fatal errors by adding a rescue section to the block. You can set any_errors_fatal at the play or block level.

You can use this feature when all tasks must be 100% successful to continue playbook execution. For example, if you run a service on machines in multiple data centers with load balancers to pass traffic from users to the service, you want all load balancers to be disabled before you stop the service for maintenance. To ensure that any failure in the task that disables the load balancers will stop all other tasks:

In this example, Ansible starts the software upgrade on the front ends only if all of the load balancers are successfully disabled.

By default, Ansible continues to execute tasks as long as there are hosts that have not yet failed. In some situations, such as when executing a rolling update, you may want to abort the play when a certain threshold of failures has been reached. To achieve this, you can set a maximum failure percentage on a play:

The max_fail_percentage setting applies to each batch when you use it with serial. In the example above, if more than 3 of the 10 servers in the first (or any) batch of servers failed, the rest of the play would be aborted.

The percentage set must be exceeded, not equaled. For example, if serial were set to 4 and you wanted the task to abort the play when 2 of the systems failed, set the max_fail_percentage at 49 rather than 50.

You can also use blocks to define responses to task errors. This approach is similar to exception handling in many programming languages. See Handling errors with blocks for details and examples.

An introduction to playbooks

Tips and tricks for playbooks

Conditional statements in playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- name: Do not count this as a failure
  ansible.builtin.command: /bin/false
  ignore_errors: true
```

Example 2 (unknown):
```unknown
- name: This executes, fails, and the failure is ignored
  ansible.builtin.command: /bin/true
  ignore_unreachable: true

- name: This executes, fails, and ends the play for this host
  ansible.builtin.command: /bin/true
```

Example 3 (unknown):
```unknown
- hosts: all
  ignore_unreachable: true
  tasks:
  - name: This executes, fails, and the failure is ignored
    ansible.builtin.command: /bin/true

  - name: This executes, fails, and ends the play for this host
    ansible.builtin.command: /bin/true
    ignore_unreachable: false
```

Example 4 (unknown):
```unknown
- name: Fail task when the command error output prints FAILED
  ansible.builtin.command: /usr/bin/example-command -x -y -z
  register: command_result
  failed_when: "'FAILED' in command_result.stderr"
```

---

## Ansible Automation Hub — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/automationhub.html

**Contents:**
- Ansible Automation Hub

Ansible Automation Hub is the official location to discover and download certified collections, included as part of an Ansible Automation Platform subscription. These content collections contain modules, plugins, roles, and playbooks in a downloadable package.

Ansible Automation Hub gives you direct access to trusted content collections from Red Hat and Certified Partners. You can find content by topic or Ansible Partner organizations.

Ansible Automation Hub is the downstream Red Hat supported product version of Ansible Galaxy. Find out more about Ansible Automation Hub features and how to access it at Ansible Automation Hub. Ansible Automation Hub is part of the Red Hat Ansible Automation Platform subscription, and comes bundled with support from Red Hat, Inc.

---

## Other Tools and Programs — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/other_tools_and_programs.html

**Contents:**
- Other Tools and Programs
- Popular editors
  - Text editors
  - Visual studio code
- Tools for validating playbooks
- Collection development tools
- Other tools

Tools for validating playbooks

Collection development tools

The Ansible community uses a range of tools for working with the Ansible project. This is a list of some of the most popular of these tools.

If you know of any other tools that should be added, open a PR against the Awesome Ansible repository.

There are popular open-source editors like Vim or Emacs that support YAML, Jinja, and specifically Ansible through corresponding plugins. Refer to Awesome Ansible Editors List for more information.

An open-source, free GUI text editor created and maintained by Microsoft. Useful Visual Studio Code plugins include:

Ansible extension by Red Hat - provides autocompletion, syntax highlighting, hover, diagnostics, goto support, and command to run ansible-playbook and ansible-navigator tool for both local and execution-environment setups.

YAML Support by Red Hat - provides YAML support through yaml-language-server with built-in Kubernetes and Kedge syntax support.

the Visual Studio Code Ansible extension is maintained by the Ansible community and Red Hat.

Ansible Lint - a highly configurable linter for Ansible playbooks.

Molecule - a testing framework for Ansible plays and roles.

yamllint - a command-line utility to check syntax validity including key repetition and indentation issues.

antsibull-changelog - a changelog generator for Ansible collections.

antsibull-docs - a docsite generator and documentation validator for Ansible collections.

Refer to Awesome Ansible Tools List, a community-curated list of awesome Ansible resources.

---

## Ansible Vault — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/vault_guide/vault.html

**Contents:**
- Ansible Vault

Ansible Vault encrypts variables and files so you can protect sensitive content such as passwords or keys rather than leaving it visible as plaintext in playbooks or roles. To use Ansible Vault you need one or more passwords to encrypt and decrypt content. If you store your vault passwords in a third-party tool such as a secret manager, you need a script to access them. Use the passwords with the ansible-vault command-line tool to create and view encrypted variables, create encrypted files, encrypt existing files, or edit, re-key, or decrypt files. You can then place encrypted content under source control and share it more safely.

Encryption with Ansible Vault ONLY protects ‘data at rest’. Once the content is decrypted (‘data in use’), play and plugin authors are responsible for avoiding any secret disclosure, see no_log for details on hiding output and Steps to secure your editor for security considerations on editors you use with Ansible Vault.

You can use encrypted variables and files in ad hoc commands and playbooks by supplying the passwords you used to encrypt them. You can modify your ansible.cfg file to specify the location of a password file or to always prompt for the password.

---

## Using collections in a playbook — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections_guide/collections_using_playbooks.html

**Contents:**
- Using collections in a playbook
- Simplifying module names with the collections keyword
- Using collections in roles
- Using collections in playbooks
- Using a playbook from a collection

Once installed, you can reference a collection content by its fully qualified collection name (FQCN):

This works for roles or any type of plugin distributed within the collection:

The collections keyword lets you define a list of collections that your role or playbook should search for unqualified module and action names. So you can use the collections keyword, then simply refer to modules and action plugins by their short-form names throughout that role or playbook.

If your playbook uses both the collections keyword and one or more roles, the roles do not inherit the collections set by the playbook. This is one of the reasons we recommend you always use FQCN. See below for roles details.

Within a role, you can control which collections Ansible searches for the tasks inside the role using the collections keyword in the role’s meta/main.yml. Ansible will use the collections list defined inside the role even if the playbook that calls the role defines different collections in a separate collections keyword entry. Roles defined inside a collection always implicitly search their own collection first, so you don’t need to use the collections keyword to access modules, actions, or other roles contained in the same collection.

In a playbook, you can control the collections Ansible searches for modules and action plugins to execute. However, any roles you call in your playbook define their own collections search order; they do not inherit the calling playbook’s settings. This is true even if the role does not define its own collections keyword.

The collections keyword merely creates an ordered ‘search path’ for non-namespaced plugins and role references. It does not install content or otherwise change Ansible’s behavior around the loading of plugins or roles. Note that an FQCN is still required for non-action or module plugins (for example, lookups, filters, and tests).

When using the collections keyword, it is not necessary to add in ansible.builtin as part of the search list. When left omitted, the following content is available by default:

Standard ansible modules and plugins available through ansible-base/ansible-core

Support for older 3rd party plugin paths

In general, it is preferable to use a module or plugin’s FQCN over the collections keyword.

You can also distribute playbooks in your collection and invoke them using the same semantics you use for plugins:

From inside a playbook:

A few recommendations when creating such playbooks, hosts: should be generic or at least have a variable input.

This will have an implied entry in the collections: keyword of my_namespace.my_collection just as with roles.

Playbook names, like other collection resources, have a restricted set of valid characters. Names can contain only lowercase alphanumeric characters, plus _ and must start with an alpha character. The dash - character is not valid for playbook names in collections. Playbooks whose names contain invalid characters are not addressable: this is a limitation of the Python importer that is used to load collection resources.

Playbooks in collections do not support ‘adjacent’ plugins, all plugins must be in the collection-specific directories.

**Examples:**

Example 1 (unknown):
```unknown
- name: Reference a collection content using its FQCN
  hosts: all
  tasks:

    - name: Call a module using FQCN
      my_namespace.my_collection.my_module:
        option1: value
```

Example 2 (unknown):
```unknown
- name: Reference collections contents using their FQCNs
  hosts: all
  tasks:

    - name: Import a role
      ansible.builtin.import_role:
        name: my_namespace.my_collection.role1

    - name: Call a module
      my_namespace.mycollection.my_module:
        option1: value

    - name: Call a debug task
      ansible.builtin.debug:
        msg: '{{ lookup("my_namespace.my_collection.lookup1", "param1") | my_namespace.my_collection.filter1 }}'
```

Example 3 (unknown):
```unknown
# myrole/meta/main.yml
collections:
  - my_namespace.first_collection
  - my_namespace.second_collection
  - other_namespace.other_collection
```

Example 4 (unknown):
```unknown
- name: Run a play using the collections keyword
  hosts: all
  collections:
    - my_namespace.my_collection

  tasks:

    - name: Import a role
      ansible.builtin.import_role:
        name: role1

    - name: Run a module not specifying FQCN
      my_module:
        option1: value

    - name: Run a debug task
      ansible.builtin.debug:
        msg: '{{ lookup("my_namespace.my_collection.lookup1", "param1")| my_namespace.my_collection.filter1 }}'
```

---

## Ansible-core 2.13 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_core_2.13.html

**Contents:**
- Ansible-core 2.13 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Modules removed
  - Deprecation notices
  - Noteworthy module changes
  - Breaking Changes
- Plugins

This section discusses the behavioral changes between ansible-core 2.12 and ansible-core 2.13.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with ansible-core Changelog for 2.13 to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

Ansible-core 2.13 Porting Guide

Noteworthy module changes

Porting custom scripts

Templating - You can no longer perform arithmetic and concatenation operations outside of the jinja template. The following statement will need to be rewritten to produce [1, 2]:

The return value of the __repr__ method of an undefined variable represented by the AnsibleUndefined object changed. {{ '%r'|format(undefined_variable) }} returns AnsibleUndefined(hint=None, obj=missing, name='undefined_variable') in 2.13 as opposed to just AnsibleUndefined in versions 2.12 and prior.

The finalize method is no longer exposed in the globals for use in templating. To convert None to an empty string the following expression can be used: {{ value if value is not none }}.

To use ansible-core 2.13 for module execution, you must use Python 2 version 2.7 or Python 3 version 3.5 or newer. Any code utilizing ansible.module_utils.basic will not function with lower Python versions.

The following modules no longer exist:

ansible.module_utils.urls.fetch_url will now return the captured HTTPError exception as r. HTTPError is a response like object that can offer more information to module authors. Modules should rely on info['status'] >= 400 to determine if there was a failure, instead of using r is None or catching AttributeError when attempting r.read().

**Examples:**

Example 1 (unknown):
```unknown
- name: Prior to 2.13
  debug:
    msg: '[1] + {{ [2] }}'

- name: 2.13 and forward
  debug:
    msg: '{{ [1] + [2] }}'
```

---
