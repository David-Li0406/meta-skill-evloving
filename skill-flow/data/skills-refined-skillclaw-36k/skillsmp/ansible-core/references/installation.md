# Ansible-Core - Installation

**Pages:** 5

---

## Installing Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/installation_guide/intro_installation.html

**Contents:**
- Installing Ansible
- Control node requirements
- Managed node requirements
- Node requirement summary
- Selecting an Ansible package and version to install
- Installing and upgrading Ansible with pipx
  - Installing Ansible
  - Upgrading Ansible
  - Installing Extra Python Dependencies
- Installing and upgrading Ansible with pip

Ansible is an agentless automation tool that you install on a single host (referred to as the control node).

From the control node, Ansible can manage an entire fleet of machines and other devices (referred to as managed nodes) remotely with SSH, Powershell remoting, and numerous other transports, all from a simple command-line interface with no databases or daemons required.

Control node requirements

Managed node requirements

Node requirement summary

Selecting an Ansible package and version to install

Installing and upgrading Ansible with pipx

Installing Extra Python Dependencies

Installing and upgrading Ansible with pip

Ensuring pip is available

Installing Ansible to containers

Installing for development

Installing devel from GitHub with pip

Running the devel branch from a clone

Confirming your installation

Adding Ansible command shell completion

Installing argcomplete

Configuring argcomplete

Per command configuration

Using argcomplete with zsh or tcsh

For your control node (the machine that runs Ansible), you can use nearly any UNIX-like machine with Python installed. This includes Red Hat, Debian, Ubuntu, macOS, BSDs, and Windows under a Windows Subsystem for Linux (WSL) distribution. Windows without WSL is not natively supported as a control node; see Matt Davis’ blog post for more information.

The managed node (the machine that Ansible is managing) does not require Ansible to be installed, but requires Python to run Ansible-generated Python code. The managed node also needs a user account that can connect through SSH to the node with an interactive POSIX shell.

There can be exceptions in module requirements. For example, network modules do not require Python on the managed device. See documentation for the modules you use.

You can find details about control and managed node requirements, including Python versions, for each Ansible version in the ansible-core control node Python support and ansible-core support matrix sections.

Ansible’s community packages are distributed in two ways:

ansible-core: a minimalist language and runtime package containing a set of built-in modules and plugins.

ansible: a much larger “batteries included” package, which adds a community-curated selection of Ansible Collections for automating a wide variety of devices.

Choose the package that fits your needs. The following instructions use ansible as a package name, but you can substitute ansible-core if you prefer to start with the minimal package and separately install only the Ansible Collections you require.

The ansible or ansible-core packages may be available in your operating systems package manager, and you are free to install these packages with your preferred method. For more information, see the Installing Ansible on specific operating systems guide. These installation instructions only cover the officially supported means of installing the python packages with pip.

See the Ansible package release status table for the ansible-core version included in the package.

On some systems, it may not be possible to install Ansible with pip, due to decisions made by the operating system developers. In such cases, pipx is a widely available alternative.

These instructions will not go over the steps to install pipx; if those instructions are needed, please continue to the pipx installation instructions for more information.

Use pipx in your environment to install the full Ansible package:

You can install the minimal ansible-core package:

Alternately, you can install a specific version of ansible-core:

To upgrade an existing Ansible installation to the latest released version:

To install additional python dependencies that may be needed, with the example of installing the argcomplete python package as described below:

Include the --include-apps option to make apps in the additional python dependency available on your PATH. This allows you to execute commands for those apps from the shell.

If you need to install dependencies from a requirements file, for example when installing the Azure collection, you can use runpip.

Locate and remember the path to the Python interpreter you wish to use to run Ansible. The following instructions refer to this Python as python3. For example, if you have determined that you want the Python at /usr/bin/python3.9 to be the one that you will install Ansible under, specify that instead of python3.

To verify whether pip is already installed for your preferred Python:

If all is well, you should see something like the following:

If so, pip is available, and you can move on to the next step.

If you see an error like No module named pip, you will need to install pip under your chosen Python interpreter before proceeding. This may mean installing an additional OS package (for example, python3-pip), or installing the latest pip directly from the Python Packaging Authority by running the following:

You may need to perform some additional configuration before you are able to run Ansible. See the Python documentation on installing to the user site for more information.

Use pip in your selected Python environment to install the full Ansible package for the current user:

You can install the minimal ansible-core package for the current user:

Alternately, you can install a specific version of ansible-core:

To upgrade an existing Ansible installation in this Python environment to the latest released version, simply add --upgrade to the command above:

Instead of installing Ansible content manually, you can simply build an execution environment container image or use one of the available community images as your control node. See Getting started with Execution Environments for details.

If you are testing new features, fixing bugs, or otherwise working with the development team on changes to the core code, you can install and run the source from GitHub.

You should only install and run the devel branch if you are modifying ansible-core or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

For more information on getting involved in the Ansible project, see the Ansible Community Guide.

For more information on creating Ansible modules and Collections, see the Developer Guide.

You can install the devel branch of ansible-core directly from GitHub with pip:

You can replace devel in the URL mentioned above, with any other branch or tag on GitHub to install older versions of Ansible, tagged alpha or beta versions, and release candidates.

ansible-core is easy to run from source. You do not need root permissions to use it and there is no software to actually install. No daemons or database setup are required.

Clone the ansible-core repository

Setup the Ansible environment

To suppress spurious warnings/errors, use -q

Install Python dependencies

Update the devel branch of ansible-core on your local machine

Use pull-with-rebase so any local changes are replayed.

You can test that Ansible is installed correctly by checking the version:

The version displayed by this command is for the associated ansible-core package that has been installed.

To check the version of the ansible package that has been installed:

You can add shell completion of the Ansible command line utilities by installing an optional dependency called argcomplete. It supports bash, and has limited support for zsh and tcsh.

For more information about installation and configuration, see the argcomplete documentation.

If you chose the pipx installation instructions:

If you chose the pip installation instructions:

There are 2 ways to configure argcomplete to allow shell completion of the Ansible command line utilities: globally or per command.

Global completion requires bash 4.2.

This will write a bash completion file to a user location. Use --dest to change the location or sudo to set up the completion globally.

If you do not have bash 4.2, you must register each script independently.

You should place the above commands into your shell’s profile file such as ~/.profile or ~/.bash_profile.

See the argcomplete documentation.

Examples of basic commands

Learning ansible’s configuration management language

Ansible Installation related to FAQs

Join the Ansible community forum to get help and share insights

How to join Ansible chat channels

**Examples:**

Example 1 (unknown):
```unknown
$ pipx install --include-deps ansible
```

Example 2 (unknown):
```unknown
$ pipx install ansible-core
```

Example 3 (unknown):
```unknown
$ pipx install ansible-core==2.12.3
```

Example 4 (unknown):
```unknown
$ pipx upgrade --include-injected ansible
```

---

## ansible.builtin.setup module – Gathers facts about remote hosts — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/setup_module.html

**Contents:**
- ansible.builtin.setup module – Gathers facts about remote hosts
- Synopsis
- Parameters
- Attributes
- Notes
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name setup even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.setup for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

This module is automatically called by playbooks to gather useful variables about remote hosts that can be used in playbooks. It can also be executed directly by /usr/bin/ansible to check what variables are available to a host. Ansible provides many facts about the system, automatically.

This module is also supported for Windows targets.

Path used for local ansible facts (*.fact) - files in this dir will be run (if executable) and their results be added to ansible_local facts. If a file is not executable it is read instead. File/results format can be JSON or INI-format. The default fact_path can be specified in ansible.cfg for when setup is automatically called as part of gather_facts. NOTE - For windows clients, the results will be added to a variable named after the local file (without extension suffix), rather than ansible_local.

Since Ansible 2.1, Windows hosts can use fact_path. Make sure that this path exists on the target host. Files in this path MUST be PowerShell scripts .ps1 which outputs an object. This object will be formatted by Ansible as json so the script should be outputting a raw hashtable, array, or other primitive object.

Default: "/etc/ansible/facts.d"

list / elements=string

If supplied, only return facts that match one of the shell-style (fnmatch) pattern. An empty list basically means ‘no filter’. As of Ansible 2.11, the type has changed from string to list and the default has became an empty list. A simple string is still accepted and works as a single pattern. The behaviour prior to Ansible 2.11 remains.

list / elements=string

If supplied, restrict the additional facts collected to the given subset. Possible values: all, all_ipv4_addresses, all_ipv6_addresses, apparmor, architecture, caps, chroot,cmdline, date_time, default_ipv4, default_ipv6, devices, distribution, distribution_major_version, distribution_release, distribution_version, dns, effective_group_ids, effective_user_id, env, facter, fips, hardware, interfaces, is_chroot, iscsi, kernel, local, lsb, machine, machine_id, mounts, network, ohai, os_family, pkg_mgr, platform, processor, processor_cores, processor_count, python, python_version, real_user_id, selinux, service_mgr, ssh_host_key_dsa_public, ssh_host_key_ecdsa_public, ssh_host_key_ed25519_public, ssh_host_key_rsa_public, ssh_host_pub_keys, ssh_pub_keys, system, system_capabilities, system_capabilities_enforced, systemd, user, user_dir, user_gecos, user_gid, user_id, user_shell, user_uid, virtual, virtualization_role, virtualization_type. Can specify a list of values to specify a larger subset. Values can also be used with an initial ! to specify that that specific subset should not be collected. For instance: !hardware,!network,!virtual,!ohai,!facter. If !all is specified then only the min subset is collected. To avoid collecting even the min subset, specify !all,!min. To collect only specific facts, use !all,!min, and specify the particular fact subsets. Use the filter parameter if you do not want to display some collected facts.

Set the default timeout in seconds for individual fact gathering.

Can run in check_mode and return changed status prediction without modifying target, if not supported the action will be skipped.

Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode

Action returns an ansible_facts dictionary that will update existing host facts

Platforms: posix, windows

Target OS/families that can be operated against

More ansible facts will be added with successive releases. If facter or ohai are installed, variables from these programs will also be snapshotted into the JSON file for usage in templating. These variables are prefixed with facter_ and ohai_ so it’s easy to tell their source. All variables are bubbled up to the caller. Using the ansible facts and choosing to not install facter and ohai means you can avoid Ruby-dependencies on your remote systems. (See also community.general.facter and community.general.ohai.)

The filter option filters only the first level subkey below ansible_facts.

If the target host is Windows, you will not currently have the ability to use filter as this is provided by a simpler implementation of the module.

This module should be run with elevated privileges on BSD systems to gather facts like ansible_product_version.

For more information about delegated facts, please check https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#delegating-facts.

**Examples:**

Example 1 (unknown):
```unknown
# Display facts from all hosts and store them indexed by `hostname` at `/tmp/facts`.
# ansible all -m ansible.builtin.setup --tree /tmp/facts

# Display only facts regarding memory found by ansible on all hosts and output them.
# ansible all -m ansible.builtin.setup -a 'filter=ansible_*_mb'

# Display only facts returned by facter.
# ansible all -m ansible.builtin.setup -a 'filter=facter_*'

# Collect only facts returned by facter.
# ansible all -m ansible.builtin.setup -a 'gather_subset=!all,facter'

- name: Collect only facts returned by facter
  ansible.builtin.setup:
    gather_subset:
      - '!all'
      - '!<any valid subset>'
      - facter

- name: Filter and return only selected facts
  ansible.builtin.setup:
    filter:
      - 'ansible_distribution'
      - 'ansible_machine_id'
      - 'ansible_*_mb'

# Display only facts about certain interfaces.
# ansible all -m ansible.builtin.setup -a 'filter=ansible_eth[0-2]'

# Restrict additional gathered facts to network and virtual (includes default minimum facts)
# ansible all -m ansible.builtin.setup -a 'gather_subset=network,virtual'

# Collect only network and virtual (excludes default minimum facts)
# ansible all -m ansible.builtin.setup -a 'gather_subset=!all,network,virtual'

# Do not call puppet facter or ohai even if present.
# ansible all -m ansible.builtin.setup -a 'gather_subset=!facter,!ohai'

# Only collect the default minimum amount of facts:
# ansible all -m ansible.builtin.setup -a 'gather_subset=!all'

# Collect no facts, even the default minimum subset of facts:
# ansible all -m ansible.builtin.setup -a 'gather_subset=!all,!min'

# Display facts from Windows hosts with custom facts stored in C:\custom_facts.
# ansible windows -m ansible.builtin.setup -a "fact_path='c:\custom_facts'"

# Gathers facts for the machines in the dbservers group (a.k.a Delegating facts)
- hosts: app_servers
  tasks:
    - name: Gather facts from db servers
      ansible.builtin.setup:
      delegate_to: "{{ item }}"
      delegate_facts: true
      loop: "{{ groups['dbservers'] }}"
```

---

## Sample Ansible setup — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/tips_tricks/sample_setup.html

**Contents:**
- Sample Ansible setup
- Sample directory layout
- Alternative directory layout
- Sample group and host variables
- Sample playbooks organized by function
- Sample task and handler files in a function-based role
- What the sample setup enables
- Organizing for deployment or configuration
- Using local Ansible modules

You have learned about playbooks, inventory, roles, and variables. This section combines all those elements and outlines a sample setup for automating a web service.

The sample setup organizes playbooks, roles, inventory, and files with variables by function. Tags at the play and task level provide greater granularity and control. This is a powerful and flexible approach, but there are other ways to organize Ansible content. Your usage of Ansible should fit your needs, so feel free to modify this approach and organize your content accordingly.

Sample directory layout

Alternative directory layout

Sample group and host variables

Sample playbooks organized by function

Sample task and handler files in a function-based role

What the sample setup enables

Organizing for deployment or configuration

Using local Ansible modules

This layout organizes most tasks in roles, with a single inventory file for each environment and a few playbooks in the top-level directory:

By default, Ansible assumes your playbooks are stored in one directory with roles stored in a sub-directory called roles/. With more tasks to automate, you can consider moving your playbooks into a sub-directory called playbooks/. If you do this, you must configure the path to your roles/ directory using the roles_path setting in the ansible.cfg file.

You can also put each inventory file with its group_vars/host_vars in a separate directory. This is particularly useful if your group_vars/host_vars do not have that much in common in different environments. The layout could look like this example:

This layout gives you more flexibility for larger environments, as well as a total separation of inventory variables between different environments. However, this approach is harder to maintain, because there are more files. For more information on organizing group and host variables, see Organizing host and group variables.

These sample group and host files with variables contain the values that apply to each machine or a group of machines. For example, the data center in Atlanta has its own NTP servers. As a result, when setting up the ntp.conf file, you could use similar code as in this example:

Similarly, hosts in the webservers group have some configuration that does not apply to the database servers:

Default values, or values that are universally true, belong in a file called group_vars/all:

If necessary, you can define specific hardware variance in systems in the host_vars directory:

If you use dynamic inventory, Ansible creates many dynamic groups automatically. As a result, a tag like class:webserver will load in variables from the file group_vars/ec2_tag_class_webserver automatically.

You can access host variables with a special variable called hostvars. See Special Variables for a list of these variables. The hostvars variable can access only host-specific variables, not group variables.

With this setup, a single playbook can define the entire infrastructure. The site.yml playbook imports two other playbooks. One for the webservers and one for the database servers:

The webservers.yml playbook, also at the top level, maps the configuration of the webservers group to the roles related to the webservers group:

With this setup, you can configure your entire infrastructure by running site.yml. Alternatively, to configure just a portion of your infrastructure, run webservers.yml. This is similar to the Ansible --limit parameter but a little more explicit:

Ansible loads any file called main.yml in a role sub-directory. This sample tasks/main.yml file configures NTP:

Here is an example handlers file. Handlers are only triggered when certain tasks report changes. Handlers run at the end of each play:

See Roles for more information.

The basic organizational structure described above enables a lot of different automation options. To reconfigure your entire infrastructure:

To reconfigure NTP on everything:

To reconfigure only the webservers:

To reconfigure only the webservers in Boston:

To reconfigure only the first 10 webservers in Boston, and then the next 10:

The sample setup also supports basic ad hoc commands:

To discover what tasks would run or what hostnames would be affected by a particular Ansible command:

The sample setup illustrates a typical configuration topology. When you do multi-tier deployments, you will likely need some additional playbooks that hop between tiers to roll out an application. In this case, you can augment site.yml with playbooks like deploy_exampledotcom.yml. However, the general concepts still apply. With Ansible you can deploy and configure using the same utility. Therefore, you will probably reuse groups and keep the OS configuration in separate playbooks or roles from the application deployment.

Consider “playbooks” as a sports metaphor – you can have one set of plays to use against all your infrastructure. Then you have situational plays that you use at different times and for different purposes.

If a playbook has a ./library directory relative to its YAML file, you can use this directory to add Ansible modules automatically to the module path. This organizes modules with playbooks. For example, see the directory structure at the start of this section.

Learn about YAML syntax

Review the basic playbook features

Browse existing collections, modules, and plugins

Learn how to extend Ansible by writing your own modules

Learn about how to select hosts

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1.yml             # here we assign variables to particular groups
   group2.yml
host_vars/
   hostname1.yml          # here we assign variables to particular systems
   hostname2.yml

library/                  # if any custom modules, put them here (optional)
module_utils/             # if any custom module_utils to support modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # main playbook
webservers.yml            # playbook for webserver tier
dbservers.yml             # playbook for dbserver tier
tasks/                    # task files included from playbooks
    webservers-extra.yml  # <-- avoids confusing playbook with task files
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
            main.yml      #  <-- role dependencies and optional Galaxy info
        library/          # roles can also include custom modules
        module_utils/     # roles can also include custom module_utils
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""
```

Example 3 (unknown):
```unknown
inventories/
   production/
      hosts               # inventory file for production servers
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         hostname1.yml    # here we assign variables to particular systems
         hostname2.yml

   staging/
      hosts               # inventory file for staging environment
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         stagehost1.yml   # here we assign variables to particular systems
         stagehost2.yml

library/
module_utils/
filter_plugins/

site.yml
webservers.yml
dbservers.yml

roles/
    common/
    webtier/
    monitoring/
    fooapp/
```

Example 4 (unknown):
```unknown
---
# file: group_vars/atlanta
ntp: ntp-atlanta.example.com
backup: backup-atlanta.example.com
```

---

## Installing Ansible on specific operating systems — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/installation_guide/installation_distros.html

**Contents:**
- Installing Ansible on specific operating systems
- Requirements for adding new distributions
- Installing Ansible on Fedora Linux
- Installing Ansible from EPEL
- Installing Ansible on OpenSUSE Tumbleweed/Leap
- Installing Ansible on Ubuntu
- Installing Ansible on Debian
- Installing Ansible on Arch Linux
- Installing Ansible on Windows

These instructions come from their respective communities. If you encounter bugs or issues, file them with that community to update these instructions. Ansible maintains only the pip install instructions.

You can always install the ansible package from PyPI using pip on most systems. The community also packages and maintains Ansible for various Linux distributions.

This guide shows you how to install Ansible from different distribution package repositories.

Package maintainers who want to add instructions for another distribution to this guide must meet the following requirements:

Ensure the distribution provides a reasonably up-to-date version of ansible.

Keep ansible-core and ansible versions synchronized to the extent that the build system allows.

Provide a way to contact the distribution maintainers as part of the instructions.

Distribution maintainers are also encouraged to join and monitor the Ansible Packaging Matrix room.

Fedora Linux provides both the full Ansible package and the minimal ansible-core package through the standard repositories.

Install the full ansible package:

Install the minimal ansible-core package:

Fedora repositories include several Ansible collections as standalone packages that you can install alongside ansible-core. For example, install the community.general collection:

See the Fedora Packages index for a complete list of Ansible collections packaged in Fedora.

Contact the package maintainers by filing a bug against the Fedora product in Red Hat Bugzilla.

If you use CentOS Stream, Almalinux, Rocky Linux, or related distributions, you can install ansible or Ansible collections from the community-maintained EPEL (Extra Packages for Enterprise Linux) repository:

Enable the EPEL repository.

Use the same dnf commands as for Fedora Linux.

Contact the package maintainers by filing a bug against the Fedora EPEL product in Red Hat Bugzilla.

OpenSUSE provides Ansible packages through the standard package manager.

See the OpenSUSE Support Portal for additional help with Ansible on OpenSUSE.

Ubuntu provides Ansible packages through a Personal Package Archive (PPA) that contains more recent versions than the standard repositories.

Ubuntu builds are available in a PPA here.

Configure the PPA on your system and install Ansible:

On older Ubuntu distributions, “software-properties-common” is called “python-software-properties”. You may want to use apt-get rather than apt in older versions. Also, only newer distributions (18.04, 18.10, and later) have a -u or --update flag. Adjust your script as needed.

File any issues in the PPA’s issue tracker.

Debian users can choose between the standard repository or the Ubuntu PPA for more recent versions.

While Ansible is available from the main Debian repository, this version can be outdated.

For a more recent version, Debian users can use the Ubuntu PPA according to the following table:

Ubuntu 18.04 (Bionic)

The following example assumes that you already have wget and gpg installed.

Add the repository and install Ansible. Set UBUNTU_CODENAME=... based on the table above (we use jammy in this example):

Use double quotes around the keyserver URL and in the “echo deb” command like in the example above.

These commands download the signing key and add an entry to apt’s sources pointing to the PPA.

Previously, you may have used apt-key add. The apt-key add approach is now deprecated for security reasons (on Debian, Ubuntu, and elsewhere).

As such, we do NOT add the key to /etc/apt/trusted.gpg.d/ or to /etc/apt/trusted.gpg where the key would be allowed to sign releases from ANY repository.

Arch Linux provides both the full Ansible package and ansible-core through the standard package repositories.

Install the full ansible package:

Install the minimal ansible-core package:

Arch Linux repositories include several Ansible ecosystem packages as standalone packages that you can install alongside ansible-core. See the Arch Linux Packages index for a complete list of Ansible packages in Arch Linux.

Contact the package maintainers by opening an issue in the related package GitLab repository.

You cannot use a Windows system for the Ansible control node. See Using Windows as the control node

Distro-specific installation on Arch Linux

Distro-specific installation on Clear Linux

**Examples:**

Example 1 (unknown):
```unknown
$ sudo dnf install ansible
```

Example 2 (unknown):
```unknown
$ sudo dnf install ansible-core
```

Example 3 (unknown):
```unknown
$ sudo dnf install ansible-collection-community-general
```

Example 4 (unknown):
```unknown
$ sudo zypper install ansible
```

---

## Configuring Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/installation_guide/intro_configuration.html

**Contents:**
- Configuring Ansible
- Configuration file
  - Getting the latest configuration
- Environmental configuration
- Command line options

Getting the latest configuration

Environmental configuration

This topic describes how to control Ansible settings.

Certain settings in Ansible are adjustable with a configuration file (ansible.cfg). The stock configuration should be sufficient for most users, but there may be reasons you would want to change them.

Paths where the configuration file is searched are listed in reference documentation.

If installing Ansible from a package manager, the latest ansible.cfg file should be present in /etc/ansible, possibly as a .rpmnew file (or other) as appropriate in the case of updates.

If you installed Ansible from pip or from the source, you may want to create this file to override default settings in Ansible.

You can generate an Ansible configuration file, ansible.cfg, that lists all default settings as follows:

Include available plugins to create a more complete Ansible configuration as follows:

For more details and a full listing of available configurations go to configuration_settings.

You can use the ansible-config command-line utility to list your available options and inspect the current values.

For in-depth details, see Ansible Configuration Settings.

Ansible also allows configuring settings using environment variables.

If these environment variables are set, they will override any associated settings loaded from the configuration file. You can get a full listing of available environment variables from:

Ansible Configuration Settings: for configuring core functionality

Index of all Collection Environment Variables: for configuring plugins in collections

Not all configuration options are present in the command line, just the ones deemed most useful or common. Settings in the command line will override those passed through the configuration file and the environment.

The full list of options available is in ansible-playbook and ansible.

**Examples:**

Example 1 (unknown):
```unknown
$ ansible-config init --disabled > ansible.cfg
```

Example 2 (unknown):
```unknown
$ ansible-config init --disabled -t all > ansible.cfg
```

---
