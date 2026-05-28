# Ansible-Core - Getting Started

**Pages:** 9

---

## Start automating with Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/getting_started/get_started_ansible.html

**Contents:**
- Start automating with Ansible

Get started with Ansible by creating an automation project, building an inventory, and creating a “Hello World” playbook.

Create a project folder on your filesystem.

Using a single directory structure makes it easier to add to source control as well as to reuse and share automation content.

Continue getting started with Ansible by building an inventory.

Installation guide with instructions for installing Ansible on various operating systems

Demonstrations of different Ansible usecases

Labs to provide further knowledge on different topics

Questions? Help? Ideas? Ask the community

**Examples:**

Example 1 (unknown):
```unknown
pip install ansible
```

Example 2 (unknown):
```unknown
mkdir ansible_quickstart && cd ansible_quickstart
```

---

## Creating a playbook — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/getting_started/get_started_playbook.html

**Contents:**
- Creating a playbook

Playbooks are automation blueprints, in YAML format, that Ansible uses to deploy and configure managed nodes.

A list of plays that define the order in which Ansible performs operations, from top to bottom, to achieve an overall goal.

An ordered list of tasks that maps to managed nodes in an inventory.

A reference to a single module that defines the operations that Ansible performs.

A unit of code or binary that Ansible runs on managed nodes. Ansible modules are grouped in collections with a Fully Qualified Collection Name (FQCN) for each module.

Complete the following steps to create a playbook that pings your hosts and prints a “Hello world” message:

Create a file named playbook.yaml in your ansible_quickstart directory, that you created earlier, with the following content:

Ansible returns the following output:

In this output you can see:

The names that you give the play and each task. You should always use descriptive names that make it easy to verify and troubleshoot playbooks.

The “Gathering Facts” task runs implicitly. By default, Ansible gathers information about your inventory that it can use in the playbook.

The status of each task. Each task has a status of ok which means it ran successfully.

The play recap that summarizes results of all tasks in the playbook per host. In this example, there are three tasks so ok=3 indicates that each task ran successfully.

Congratulations, you have started using Ansible!

Start building playbooks for real world scenarios.

Go into more detail with Ansible playbooks.

Get tips and tricks for using playbooks.

Learn more about the gather_facts keyword in playbooks.

**Examples:**

Example 1 (unknown):
```unknown
- name: My first play
  hosts: myhosts
  tasks:
   - name: Ping my hosts
     ansible.builtin.ping:

   - name: Print message
     ansible.builtin.debug:
       msg: Hello world
```

Example 2 (unknown):
```unknown
ansible-playbook -i inventory.ini playbook.yaml
```

Example 3 (javascript):
```javascript
PLAY [My first play] ****************************************************************************

TASK [Gathering Facts] **************************************************************************
ok: [192.0.2.50]
ok: [192.0.2.51]
ok: [192.0.2.52]

TASK [Ping my hosts] ****************************************************************************
ok: [192.0.2.50]
ok: [192.0.2.51]
ok: [192.0.2.52]

TASK [Print message] ****************************************************************************
ok: [192.0.2.50] => {
    "msg": "Hello world"
}
ok: [192.0.2.51] => {
    "msg": "Hello world"
}
ok: [192.0.2.52] => {
    "msg": "Hello world"
}

PLAY RECAP **************************************************************************************
192.0.2.50: ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.0.2.51: ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.0.2.52: ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## Building an inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/getting_started/get_started_inventory.html

**Contents:**
- Building an inventory
- Inventories in INI or YAML format
- Tips for building inventories
  - Use metagroups
  - Create variables

Inventories organize managed nodes in centralized files that provide Ansible with system information and network locations. Using an inventory file, Ansible can manage a large number of hosts with a single command.

To complete the following steps, you will need the IP address or fully qualified domain name (FQDN) of at least one host system. For demonstration purposes, the host could be running locally in a container or a virtual machine. You must also ensure that your public SSH key is added to the authorized_keys file on each host.

Continue getting started with Ansible and build an inventory as follows:

Create a file named inventory.ini in the ansible_quickstart directory that you created in the preceding step.

Add a new [myhosts] group to the inventory.ini file and specify the IP address or fully qualified domain name (FQDN) of each host system.

Verify your inventory.

Ping the myhosts group in your inventory.

Pass the -u option with the ansible command if the username is different on the control node and the managed node(s).

Congratulations, you have successfully built an inventory. Continue getting started with Ansible by creating a playbook.

You can create inventories in either INI files or in YAML. In most cases, such as the example in the preceding steps, INI files are straightforward and easy to read for a small number of managed nodes.

Creating an inventory in YAML format becomes a sensible option as the number of managed nodes increases. For example, the following is an equivalent of the inventory.ini that declares unique names for managed nodes and uses the ansible_host field:

Ensure that group names are meaningful and unique. Group names are also case sensitive.

Avoid spaces, hyphens, and preceding numbers (use floor_19, not 19th_floor) in group names.

Group hosts in your inventory logically according to their What, Where, and When.

Group hosts according to the topology, for example: db, web, leaf, spine.

Group hosts by geographic location, for example: datacenter, region, floor, building.

Group hosts by stage, for example: development, test, staging, production.

Create a metagroup that organizes multiple groups in your inventory with the following syntax:

The following inventory illustrates a basic structure for a data center. This example inventory contains a network metagroup that includes all network devices and a datacenter metagroup that includes the network group and all webservers.

Variables set values for managed nodes, such as the IP address, FQDN, operating system, and SSH user, so you do not need to pass them when running Ansible commands.

Variables can apply to specific hosts.

Variables can also apply to all hosts in a group.

Learn more about inventories in YAML or INI format.

Find out more about inventory variables and their syntax.

Find out how to encrypt sensitive content in your inventory such as passwords and keys.

**Examples:**

Example 1 (unknown):
```unknown
[myhosts]
192.0.2.50
192.0.2.51
192.0.2.52
```

Example 2 (unknown):
```unknown
ansible-inventory -i inventory.ini --list
```

Example 3 (unknown):
```unknown
ansible myhosts -m ping -i inventory.ini
```

Example 4 (javascript):
```javascript
192.0.2.50 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.0.2.51 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.0.2.52 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

---

## Introduction to modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/module_plugin_guide/modules_intro.html

**Contents:**
- Introduction to modules
- Boolean variables

Modules (also referred to as “task plugins” or “library plugins”) are discrete units of code that can be used from the command line or in a playbook task. Ansible executes each module, usually on the remote managed node, and collects return values. In Ansible 2.10 and later, most modules are hosted in collections.

You can execute modules from the command line.

Each module supports arguments. Nearly all modules take key=value arguments, space delimited. Some modules take no arguments, and the command/shell modules simply take the string of the command you want to run.

From playbooks, Ansible modules are executed in a very similar way.

Another way to pass arguments to a module is using YAML syntax, also called ‘complex args’.

All modules return JSON format data. This means modules can be written in any programming language. Modules should be idempotent, and should avoid making any changes if they detect that the current state matches the desired final state. When used in an Ansible playbook, modules can trigger ‘change events’ in the form of notifying handlers to run additional tasks.

You can access the documentation for each module from the command line with the ansible-doc tool.

For a list of all available modules, see the Collection docs, or run the following at a command prompt.

Ansible accepts a broad range of values for bool in module arguments: true/false, 1/0, yes/no, True/False and so on. The matching of valid strings is case insensitive. While documentation examples focus on true/false to be compatible with ansible-lint default settings, you can use any of the following:

True , 'true' , 't' , 'yes' , 'y' , 'on' , '1' , 1 , 1.0

False , 'false' , 'f' , 'no' , 'n' , 'off' , '0' , 0 , 0.0

Examples of using modules in /usr/bin/ansible

Examples of using modules with /usr/bin/ansible-playbook

How to write your own modules

Examples of using modules with the Python API

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

All modules and plugins available

**Examples:**

Example 1 (unknown):
```unknown
ansible webservers -m service -a "name=httpd state=started"
ansible webservers -m ping
ansible webservers -m command -a "/sbin/reboot -t now"
```

Example 2 (unknown):
```unknown
- name: reboot the servers
  command: /sbin/reboot -t now
```

Example 3 (unknown):
```unknown
- name: restart webserver
  service:
    name: httpd
    state: restarted
```

Example 4 (unknown):
```unknown
ansible-doc yum
```

---

## Ansible concepts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/getting_started/basic_concepts.html

**Contents:**
- Ansible concepts
- Control node
- Managed nodes
- Inventory
- Playbooks
  - Plays
    - Roles
    - Tasks
    - Handlers
- Modules

These concepts are common to all uses of Ansible. You should understand them before using Ansible or reading the documentation.

The machine from which you run the Ansible CLI tools (ansible-playbook , ansible, ansible-vault and others). You can use any computer that meets the software requirements as a control node - laptops, shared desktops, and servers can all run Ansible. You can also run Ansible in containers known as Execution Environments.

Multiple control nodes are possible, but Ansible itself does not coordinate across them, see AAP for such features.

Also referred to as ‘hosts’, these are the target devices (servers, network appliances or any computer) you aim to manage with Ansible.

Ansible is not normally installed on managed nodes, unless you are using ansible-pull, but this is rare and not the recommended setup.

A list of managed nodes provided by one or more ‘inventory sources’. Your inventory can specify information specific to each node, like IP address. It is also used for assigning groups, that both allow for node selection in the Play and bulk variable assignment.

To learn more about inventory, see the Working with Inventory section. Sometimes an inventory source file is also referred to as a ‘hostfile’.

They contain Plays (which are the basic unit of Ansible execution). This is both an ‘execution concept’ and how we describe the files on which ansible-playbook operates.

Playbooks are written in YAML and are easy to read, write, share and understand. To learn more about playbooks, see Ansible playbooks.

The main context for Ansible execution, this playbook object maps managed nodes (hosts) to tasks. The Play contains variables, roles and an ordered lists of tasks and can be run repeatedly. It basically consists of an implicit loop over the mapped hosts and tasks and defines how to iterate over them.

A limited distribution of reusable Ansible content (tasks, handlers, variables, plugins, templates and files) for use inside of a Play.

To use any Role resource, the Role itself must be imported into the Play.

The definition of an ‘action’ to be applied to the managed host. You can execute a single task once with an ad hoc command using ansible or ansible-console (both create a virtual Play).

A special form of a Task, that only executes when notified by a previous task which resulted in a ‘changed’ status.

The code or binaries that Ansible copies to and executes on each managed node (when needed) to accomplish the action defined in each Task.

Each module has a particular use, from administering users on a specific type of database to managing VLAN interfaces on a specific type of network device.

You can invoke a single module with a task, or invoke several different modules in a playbook. Ansible modules are grouped in collections. For an idea of how many collections Ansible includes, see the Collection Index.

Pieces of code that expand Ansible’s core capabilities. Plugins can control how you connect to a managed node (connection plugins), manipulate data (filter plugins) and even control what is displayed in the console (callback plugins).

See Working with plugins for details.

A format in which Ansible content is distributed that can contain playbooks, roles, modules, and plugins. You can install and use collections through Ansible Galaxy.

To learn more about collections, see Using Ansible collections.

Collection resources can be used independently and discretely from each other.

---

## Introduction to Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/getting_started/introduction.html

**Contents:**
- Introduction to Ansible

Ansible provides open-source automation that reduces complexity and runs everywhere. Using Ansible lets you automate virtually any task. Here are some common use cases for Ansible:

Eliminate repetition and simplify workflows

Manage and maintain system configuration

Continuously deploy complex software

Perform zero-downtime rolling updates

Ansible uses simple, human-readable scripts called playbooks to automate your tasks. You declare the desired state of a local or remote system in your playbook. Ansible ensures that the system remains in that state.

As automation technology, Ansible is designed around the following principles:

Low maintenance overhead by avoiding the installation of additional software across IT infrastructure.

Automation playbooks use straightforward YAML syntax for code that reads like documentation. Ansible is also decentralized, using SSH with existing OS credentials to access to remote machines.

Easily and quickly scale the systems you automate through a modular design that supports a large range of operating systems, cloud platforms, and network devices.

When the system is in the state your playbook describes, Ansible does not change anything, even if the playbook runs multiple times.

Ready to start using Ansible? Get up and running in a few easy steps.

---

## Introduction to ad hoc commands — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/command_guide/intro_adhoc.html

**Contents:**
- Introduction to ad hoc commands
- Why use ad hoc commands?
- Use cases for ad hoc tasks
  - Rebooting servers
  - Managing files
  - Managing packages
  - Managing users and groups
  - Managing services
  - Gathering facts
  - Check mode

An Ansible ad hoc command uses the /usr/bin/ansible command-line tool to automate a single task on one or more managed nodes. ad hoc commands are quick and easy, but they are not reusable. So why learn about ad hoc commands? ad hoc commands demonstrate the simplicity and power of Ansible. The concepts you learn here will port over directly to the playbook language. Before reading and executing these examples, please read How to build your inventory.

Why use ad hoc commands?

Use cases for ad hoc tasks

Managing users and groups

Patterns and ad-hoc commands

ad hoc commands are great for tasks you repeat rarely. For example, if you want to power off all the machines in your lab for Christmas vacation, you could execute a quick one-liner in Ansible without writing a playbook. An ad hoc command looks like this:

The -a option accepts options either through the key=value syntax or a JSON string starting with { and ending with } for more complex option structure. You can learn more about patterns and modules on other pages.

ad hoc tasks can be used to reboot servers, copy files, manage packages and users, and much more. You can use any Ansible module in an ad hoc task. ad hoc tasks, like playbooks, use a declarative model, calculating and executing the actions required to reach a specified final state. They achieve a form of idempotence by checking the current state before they begin and doing nothing unless the current state is different from the specified final state.

The default module for the ansible command-line utility is the ansible.builtin.command module. You can use an ad hoc task to call the command module and reboot all web servers in Atlanta, 10 at a time. Before Ansible can do this, you must have all servers in Atlanta listed in a group called [atlanta] in your inventory, and you must have working SSH credentials for each machine in that group. To reboot all the servers in the [atlanta] group:

By default, Ansible uses only five simultaneous processes. If you have more hosts than the value set for the fork count, it can increase the time it takes for Ansible to communicate with the hosts. To reboot the [atlanta] servers with 10 parallel forks:

/usr/bin/ansible will default to running from your user account. To connect as a different user:

Rebooting probably requires privilege escalation. You can connect to the server as username and run the command as the root user by using the become keyword:

If you add --ask-become-pass or -K, Ansible prompts you for the password to use for privilege escalation (sudo/su/pfexec/doas/etc).

The command module does not support extended shell syntaxes like piping and redirects (although shell variables will always work). If your command requires shell-specific syntax, use the shell module instead.

So far all our examples have used the default ‘command’ module. To use a different module, pass -m for module name. For example, to use the ansible.builtin.shell module:

When running any command with the Ansible ad hoc CLI (as opposed to Playbooks), pay particular attention to shell quoting rules, so the local shell retains the variable and passes it to Ansible. For example, using double rather than single quotes in the above example would evaluate the variable on the box you were on.

An ad hoc task can harness the power of Ansible and SCP to transfer many files to multiple machines in parallel. To transfer a file directly to all servers in the [atlanta] group:

If you plan to repeat a task like this, use the ansible.builtin.template module in a playbook.

The ansible.builtin.file module allows changing ownership and permissions on files. These same options can be passed directly to the copy module as well:

The file module can also create directories, similar to mkdir -p:

As well as delete directories (recursively) and delete files:

You might also use an ad hoc task to install, update, or remove packages on managed nodes using a package management module such as yum. Package management modules support common functions to install, remove, and generally manage packages. Some specific functions for a package manager might not be present in the Ansible module since they are not part of general package management.

To ensure a package is installed without updating it:

To ensure a specific version of a package is installed:

To ensure a package is at the latest version:

To ensure a package is not installed:

Ansible has modules for managing packages under many platforms. If there is no module for your package manager, you can install packages using the command module or create a module for your package manager.

You can create, manage, and remove user accounts on your managed nodes with ad hoc tasks:

See the ansible.builtin.user module documentation for details on all of the available options, including how to manipulate groups and group membership.

Ensure a service is started on all webservers:

Alternatively, restart a service on all webservers:

Ensure a service is stopped:

Facts represent discovered variables about a system. You can use facts to implement conditional execution of tasks but also just to get ad hoc information about your systems. To see all facts:

You can also filter this output to display only certain facts, see the ansible.builtin.setup module documentation for details.

In check mode, Ansible does not make any changes to remote systems. Ansible prints the commands only. It does not run the commands.

Enabling check mode (-C or --check) in the above command means Ansible does not actually create or update the /root/bar.txt file on any remote systems.

See the patterns documentation for details on all of the available options, including how to limit using patterns in ad-hoc commands.

Now that you understand the basic elements of Ansible execution, you are ready to learn to automate repetitive tasks using Ansible Playbooks.

All about the Ansible config file

Browse existing collections, modules, and plugins

Using Ansible for configuration management & deployment

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
$ ansible [pattern] -m [module] -a "[module options]"
```

Example 2 (unknown):
```unknown
$ ansible atlanta -a "/sbin/reboot"
```

Example 3 (unknown):
```unknown
$ ansible atlanta -a "/sbin/reboot" -f 10
```

Example 4 (unknown):
```unknown
$ ansible atlanta -a "/sbin/reboot" -f 10 -u username
```

---

## Ansible architecture — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/overview_architecture.html

**Contents:**
- Ansible architecture
- Modules
- Module utilities
- Plugins
- Inventory
- Playbooks
- The Ansible search path

Ansible is a radically simple IT automation engine that automates cloud provisioning, configuration management, application deployment, intra-service orchestration, and many other IT needs.

Being designed for multi-tier deployments since day one, Ansible models your IT infrastructure by describing how all of your systems inter-relate, rather than just managing one system at a time.

It uses no agents and no additional custom security infrastructure, so it is easy to deploy - and most importantly, it uses a very simple language (YAML, in the form of Ansible Playbooks) that allows you to describe your automation jobs in a way that approaches plain English.

In this section, we’ll give you a really quick overview of how Ansible works so you can see how the pieces fit together.

The Ansible search path

Ansible works by connecting to your nodes and pushing out scripts called “Ansible modules” to them. Most modules accept parameters that describe the desired state of the system. Ansible then executes these modules (over SSH by default), and removes them when finished. Your library of modules can reside on any machine, and there are no servers, daemons, or databases required.

You can write your own modules, though you should first consider whether you should. Typically you’ll work with your favorite terminal program, a text editor, and probably a version control system to keep track of changes to your content. You may write specialized modules in any language that can return JSON (Ruby, Python, bash, and so on).

When multiple modules use the same code, Ansible stores those functions as module utilities to minimize duplication and maintenance. For example, the code that parses URLs is lib/ansible/module_utils/url.py. You can write your own module utilities as well. Module utilities may only be written in Python or in PowerShell.

Plugins augment Ansible’s core functionality. While modules execute on the target system in separate processes (usually that means on a remote system), plugins execute on the control node within the /usr/bin/ansible process. Plugins offer options and extensions for the core features of Ansible - transforming data, logging output, connecting to inventory, and more. Ansible ships with a number of handy plugins, and you can easily write your own. For example, you can write an inventory plugin to connect to any datasource that returns JSON. Plugins must be written in Python.

By default, Ansible represents the machines it manages in a file (INI, YAML, and so on) that puts all of your managed machines in groups of your own choosing.

To add new machines, there is no additional SSL signing server involved, so there’s never any hassle deciding why a particular machine didn’t get linked up due to obscure NTP or DNS issues.

If there’s another source of truth in your infrastructure, Ansible can also connect to that. Ansible can draw inventory, group, and variable information from sources like EC2, Rackspace, OpenStack, and more.

Here’s what a plain text inventory file looks like:

Once inventory hosts are listed, variables can be assigned to them in simple text files (in a subdirectory called ‘group_vars/’ or ‘host_vars/’) or directly in the inventory file.

Or, as already mentioned, use a dynamic inventory to pull your inventory from data sources like EC2, Rackspace, or OpenStack.

Playbooks can finely orchestrate multiple slices of your infrastructure topology, with very detailed control over how many machines to tackle at a time. This is where Ansible starts to get most interesting.

Ansible’s approach to orchestration is one of finely-tuned simplicity, as we believe your automation code should make perfect sense to you years down the road and there should be very little to remember about special syntax or features.

Here’s what a simple playbook looks like:

Modules, module utilities, plugins, playbooks, and roles can live in multiple locations. If you write your own code to extend Ansible’s core features, you may have multiple files with similar or the same names in different locations on your Ansible control node. The search path determines which of these files Ansible will discover and use on any given playbook run.

Ansible’s search path grows incrementally over a run. As Ansible finds each playbook and role included in a given run, it appends any directories related to that playbook or role to the search path. Those directories remain in scope for the duration of the run, even after the playbook or role has finished executing. Ansible loads modules, module utilities, and plugins in this order:

Directories adjacent to a playbook specified on the command line. If you run Ansible with ansible-playbook /path/to/play.yml, Ansible appends these directories if they exist:

Directories adjacent to a playbook that is statically imported by a playbook specified on the command line. If play.yml includes - import_playbook: /path/to/subdir/play1.yml, Ansible appends these directories if they exist:

Subdirectories of a role directory referenced by a playbook. If play.yml runs myrole, Ansible appends these directories if they exist:

Directories specified as default paths in ansible.cfg or by the related environment variables, including the paths for the various plugin types. See Ansible Configuration Settings for more information. Sample ansible.cfg fields:

Sample environment variables:

The standard directories that ship as part of the Ansible distribution.

Modules, module utilities, and plugins in user-specified directories will override the standard versions. This includes some files with generic names. For example, if you have a file named basic.py in a user-specified directory, it will override the standard ansible.module_utils.basic.

If you have more than one module, module utility, or plugin with the same name in different user-specified directories, the order of commands at the command line and the order of includes and roles in each play will affect which one is found and used on that particular play.

**Examples:**

Example 1 (unknown):
```unknown
[webservers]
www1.example.com
www2.example.com

[dbservers]
db0.example.com
db1.example.com
```

Example 2 (unknown):
```unknown
---
- hosts: webservers
  serial: 5 # update 5 machines at a time
  roles:
  - common
  - webapp

- hosts: content_servers
  roles:
  - common
  - content
```

Example 3 (unknown):
```unknown
/path/to/modules
/path/to/module_utils
/path/to/plugins
```

Example 4 (unknown):
```unknown
/path/to/subdir/modules
/path/to/subdir/module_utils
/path/to/subdir/plugins
```

---

## Getting started — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/getting_started.html

**Contents:**
- Getting started
- Other ways to get involved

Welcome and thank you for getting more involved with the Ansible community. Here are some ways you can get started.

Here are some other ways to connect with the Ansible community:

Visit the Ansible communication guide.

Find an Ansible Meetup near you.

Learn more about Ansible:

Review getting started guides.

Watch videos - includes Ansible Automates, AnsibleFest & webinar recordings.

---
