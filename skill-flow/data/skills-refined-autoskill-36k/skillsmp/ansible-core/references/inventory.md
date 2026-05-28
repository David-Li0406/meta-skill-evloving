# Ansible-Core - Inventory

**Pages:** 19

---

## ansible.builtin.ini inventory – Uses an Ansible INI file as inventory source. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/ini_inventory.html

**Contents:**
- ansible.builtin.ini inventory – Uses an Ansible INI file as inventory source.
- Synopsis
- Notes
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name ini. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.ini for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

INI file based inventory, sections are groups or group related with special :modifiers.

Entries in sections [group_1] are hosts, members of the group.

Hosts can have variables defined inline as key/value pairs separated by =.

The children modifier indicates that the section contains groups.

The vars modifier indicates that the section contains variables assigned to members of the group.

Anything found outside a section is considered an ‘ungrouped’ host.

Values passed in the INI format using the key=value syntax are interpreted differently depending on where they are declared within your inventory.

When declared inline with the host, INI values are processed by Python’s ast.literal_eval function (https://docs.python.org/3/library/ast.html#ast.literal_eval) and interpreted as Python literal structures (strings, numbers, tuples, lists, dicts, booleans, None). If you want a number to be treated as a string, you must quote it. Host lines accept multiple key=value parameters per line. Therefore they need a way to indicate that a space is part of a value rather than a separator.

When declared in a :vars section, INI values are interpreted as strings. For example var=FALSE would create a string equal to FALSE. Unlike host lines, :vars sections accept only a single entry per line, so everything after the = must be the value for the entry.

Do not rely on types set during definition, always make sure you specify type with a filter when needed when consuming the variable.

See the Examples for proper quoting to prevent changes to variable type.

Enabled in configuration by default.

Consider switching to YAML format for inventory sources to avoid confusion on the actual type of a variable. The YAML inventory plugin processes variable values consistently and correctly.

**Examples:**

Example 1 (unknown):
```unknown
# fmt: ini
# Example 1
[web]
host1
host2 ansible_port=222 # defined inline, interpreted as an integer

[web:vars]
http_port=8080 # all members of 'web' will inherit these
myvar=23 # defined in a :vars section, interpreted as a string

[web:children] # child groups will automatically add their hosts to parent group
apache
nginx

[apache]
tomcat1
tomcat2 myvar=34 # host specific vars override group vars
tomcat3 mysecret="'03#pa33w0rd'" # proper quoting to prevent value changes

[nginx]
jenkins1

[nginx:vars]
has_java = True # vars in child groups override same in parent

[all:vars]
has_java = False # 'all' is 'top' parent

# Example 2
host1 # this is 'ungrouped'

# both hosts have same IP but diff ports, also 'ungrouped'
host2 ansible_host=127.0.0.1 ansible_port=44
host3 ansible_host=127.0.0.1 ansible_port=45

[g1]
host4

[g2]
host4 # same host as above, but member of 2 groups, will inherit vars from both
      # inventory hostnames are unique
```

---

## Patterns: targeting hosts and groups — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/inventory_guide/intro_patterns.html

**Contents:**
- Patterns: targeting hosts and groups
- Using patterns
- Common patterns
- Limitations of patterns
- Pattern processing order
- Advanced pattern options
  - Using variables in patterns
  - Using group position in patterns
    - Slicing at specific items
    - Slicing with start and end points

When you execute Ansible through an ad hoc command or by running a playbook, you must choose which managed nodes or groups you want to execute against. Patterns let you run commands and playbooks against specific hosts and/or groups in your inventory. An Ansible pattern can refer to a single host, an IP address, an inventory group, a set of groups, or all hosts in your inventory. Patterns are highly flexible - you can exclude or require subsets of hosts, use wildcards or regular expressions, and more. Ansible executes on all inventory hosts included in the pattern.

Limitations of patterns

Pattern processing order

Advanced pattern options

Using variables in patterns

Using group position in patterns

Slicing at specific items

Slicing with start and end points

Using regexes in patterns

Patterns and ad-hoc commands

Patterns and ansible-playbook flags

You use a pattern almost any time you execute an ad hoc command or a playbook. The pattern is the only element of an ad hoc command that has no flag. It is usually the second element:

In a playbook, the pattern is the content of the hosts: line for each play:

Since you often want to run a command or playbook against multiple hosts at once, patterns often refer to inventory groups. Both the ad hoc command and the playbook above will execute against all machines in the webservers group.

This table lists common patterns for targeting inventory hosts and groups.

host1:host2 (or host1,host2)

all hosts in webservers plus all hosts in dbservers

all hosts in webservers except those in atlanta

Intersection of groups

any hosts in webservers that are also in staging

You can use either a comma (,) or a colon (:) to separate a list of hosts. The comma is preferred when dealing with ranges and IPv6 addresses.

Once you know the basic patterns, you can combine them. This example:

targets all machines in the groups ‘webservers’ and ‘dbservers’ that are also in the group ‘staging’, except for any machines in the group ‘phoenix’.

You can use wildcard patterns with FQDNs or IP addresses, as long as the hosts are named in your inventory by FQDN or IP address:

You can mix wildcard patterns and groups at the same time:

Patterns depend on inventory. If a host or group is not listed in your inventory, you cannot use a pattern to target it. If your pattern includes an IP address or hostname that does not appear in your inventory, you will see an error like this:

Your pattern must match your inventory syntax. If you define a host as an alias:

you must use the alias in your pattern. In the example above, you must use host1 in your pattern. If you use the IP address, you will once again get the error:

The processing is a bit special and happens in the following order:

This positioning only accounts for processing order inside each operation: a:b:&c:!d:!e == &c:a:!d:b:!e == !d:a:!e:&c:b

All of these result in the following:

Host in/is (a or b) AND host in/is all(c) AND host NOT in/is all(d, e).

Now a:b:!e:!d:&c is a slight change as the !e gets processed before the !d, though this doesn’t make much of a difference:

Host in/is (a or b) AND host in/is all(c) AND host NOT in/is all(e, d).

The common patterns described above will meet most of your needs, but Ansible offers several other ways to define the hosts and groups you want to target.

You can use variables to enable passing group specifiers with the -e argument to ansible-playbook:

You can define a host or subset of hosts by its position in a group. For example, given the following group:

you can use subscripts to select individual hosts or ranges within the webservers group.

Result: i-th item of s where the indexing origin is 0

If i is negative, the index is relative to the end of sequence s: len(s) + i is substituted. However -0 is 0.

Result: slice of s from i to j

The slice of s from i to j is defined as the sequence of items with index k such that i <= k <= j. If i is omitted, use 0. If j is omitted, use len(s). The slice omitting both i and j, results in an invalid host pattern. If i is greater than j, the slice is empty. If i is equal to j, the s[i] is substituted.

You can specify a pattern as a regular expression by starting the pattern with ~:

You can change the behavior of the patterns defined in ad-hoc commands using command-line options. You can also limit the hosts you target on a particular run with the --limit flag.

Limit to multiple hosts

Negated limit. Note that single quotes MUST be used to prevent bash interpolation.

You can change the behavior of the patterns defined in playbooks using command-line options. For example, you can run a playbook that defines hosts: all on a single host by specifying -i 127.0.0.2, (note the trailing comma). This works even if the host you target is not defined in your inventory, but this method will NOT read your inventory for variables tied to this host and any variables required by the playbook will need to be specified manually at the command line. You can also limit the hosts you target on a particular run with the --limit flag, which will reference your inventory:

Finally, you can use --limit to read the list of hosts from a file by prefixing the file name with @:

If RETRY_FILES_ENABLED is set to True, a .retry file will be created after the ansible-playbook run containing a list of failed hosts from all plays. This file is overwritten each time ansible-playbook finishes running.

To apply your knowledge of patterns with Ansible commands and playbooks, read Introduction to ad hoc commands and Ansible playbooks.

Examples of basic commands

Learning the Ansible configuration management language

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
ansible <pattern> -m <module_name> -a "<module options>"
```

Example 2 (unknown):
```unknown
ansible webservers -m service -a "name=httpd state=restarted"
```

Example 3 (unknown):
```unknown
- name: <play_name>
  hosts: <pattern>
```

Example 4 (unknown):
```unknown
- name: restart webservers
  hosts: webservers
```

---

## ansible.builtin.add_host module – Add a host (and alternatively a group) to the ansible-playbook in-memory inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/add_host_module.html

**Contents:**
- ansible.builtin.add_host module – Add a host (and alternatively a group) to the ansible-playbook in-memory inventory
- Synopsis
- Parameters
- Attributes
- Notes
- See Also
- Examples
  - Authors
  - Collection links

This module is part of ansible-core and included in all Ansible installations. In most cases, you can use the short module name add_host even without specifying the collections keyword. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.add_host for easy linking to the module documentation and to avoid conflicting with other collections that may have the same module name.

Use variables to create new hosts and groups in inventory for use in later plays of the same playbook.

Takes variables so you can define the new hosts more fully.

This module is also supported for Windows targets.

This module has a corresponding action plugin.

aliases: group, groupname

list / elements=string

The groups to add the hostname to.

aliases: host, hostname

The hostname/ip of the host to add to the inventory, can include a colon and a port number.

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

The alias host of the parameter name is only available on Ansible 2.4 and newer.

Since Ansible 2.4, the inventory_dir variable is now set to None instead of the ‘global inventory source’, because you can now have multiple sources. An example was added that shows how to partially restore the previous behaviour.

Though this module does not change the remote host, we do provide changed status as it can be useful for those trying to track inventory changes.

The hosts added will not bypass the --limit from the command line, so both of those need to be in agreement to make them available as play targets. They are still available from hostvars and for delegation as a normal part of the inventory.

Create Ansible groups based on facts.

Seth Vidal (@skvidal)

**Examples:**

Example 1 (unknown):
```unknown
- name: Add host to group 'just_created' with variable foo=42
  ansible.builtin.add_host:
    name: '{{ ip_from_ec2 }}'
    groups: just_created
    foo: 42

- name: Add host to multiple groups
  ansible.builtin.add_host:
    hostname: '{{ new_ip }}'
    groups:
    - group1
    - group2

- name: Add a host with a non-standard port local to your machines
  ansible.builtin.add_host:
    name: '{{ new_ip }}:{{ new_port }}'

- name: Add a host alias that we reach through a tunnel (Ansible 1.9 and older)
  ansible.builtin.add_host:
    hostname: '{{ new_ip }}'
    ansible_ssh_host: '{{ inventory_hostname }}'
    ansible_ssh_port: '{{ new_port }}'

- name: Add a host alias that we reach through a tunnel (Ansible 2.0 and newer)
  ansible.builtin.add_host:
    hostname: '{{ new_ip }}'
    ansible_host: '{{ inventory_hostname }}'
    ansible_port: '{{ new_port }}'

- name: Ensure inventory vars are set to the same value as the inventory_hostname has (close to pre Ansible 2.4 behaviour)
  ansible.builtin.add_host:
    hostname: charlie
    inventory_dir: '{{ inventory_dir }}'

- name: Add all hosts running this playbook to the done group
  ansible.builtin.add_host:
    name: '{{ item }}'
    groups: done
  loop: "{{ ansible_play_hosts }}"
```

---

## ansible.builtin.constructed inventory – Uses Jinja2 to construct vars and groups based on existing inventory. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/constructed_inventory.html

**Contents:**
- ansible.builtin.constructed inventory – Uses Jinja2 to construct vars and groups based on existing inventory.
- Synopsis
- Parameters
- Notes
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name constructed. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.constructed for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

Uses a YAML configuration file with a valid YAML or .config extension to define var expressions and group conditionals

The Jinja2 conditionals that qualify a host for membership.

The Jinja2 expressions are calculated and assigned to the variables

Only variables already available from previous inventories or the fact cache can be used for templating.

When strict is False, failed expressions will be ignored (assumes vars were missing).

Create vars from jinja2 expressions.

Add hosts to group based on Jinja2 conditionals.

list / elements=dictionary

Add hosts to group based on the values of a variable.

added in ansible-core 2.12

The default value when the host variable’s value is None or an empty string.

This option is mutually exclusive with keyed_groups[].trailing_separator.

The key from input dictionary used to generate groups.

parent group for keyed group.

A keyed group name will start with this prefix.

separator used to build the keyed group name.

added in ansible-core 2.12

Set this option to false to omit the keyed_groups[].separator after the host variable when the value is None or an empty string.

This option is mutually exclusive with keyed_groups[].default_value.

added in ansible-core 2.11

Use in conjunction with keyed_groups.

By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

This is because the default prefix is "" and the default separator is "_".

Set this option to false to omit the leading underscore (or other separator) if no prefix is given.

If the group name is derived from a mapping the separator is still used to concatenate the items.

To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.

token that ensures this is a source file for the ‘constructed’ plugin.

"ansible.builtin.constructed"

If yes make invalid entries a fatal error, otherwise skip and continue.

Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.

added in ansible-core 2.11

Merge extra vars into the available variables for composition (highest precedence).

Environment variable: ANSIBLE_INVENTORY_USE_EXTRA_VARS

added in ansible-core 2.11

Normally, for performance reasons, vars plugins get executed after the inventory sources complete the base inventory, this option allows for getting vars related to hosts/groups from those plugins.

The host_group_vars (enabled by default) ‘vars plugin’ is the one responsible for reading host_vars/ and group_vars/ directories.

This will execute all vars plugins, even those that are not supposed to execute at the ‘inventory’ stage. See vars plugins docs for details on ‘stage’.

Implicit groups, such as ‘all’ or ‘ungrouped’, need to be explicitly defined in any previous inventory to apply the corresponding group_vars

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

Inventories are not finalized at this stage, so the auto populated all and ungrouped groups will only reflect what previous inventory sources explicitly added to them.

Runtime ‘magic variables’ are not available during inventory construction. For example, groups and hostvars do not exist yet.

**Examples:**

Example 1 (unknown):
```unknown
[inventory_plugins]
use_extra_vars = false
```

Example 2 (unknown):
```unknown
# inventory.config file in YAML format
plugin: ansible.builtin.constructed
strict: False
compose:
    var_sum: var1 + var2

    # this variable will only be set if I have a persistent fact cache enabled (and have non expired facts)
    # `strict: False` will skip this instead of producing an error if it is missing facts.
    server_type: "ansible_hostname | regex_replace ('(.{6})(.{2}).*', '\\2')"
groups:
    # simple name matching
    webservers: inventory_hostname.startswith('web')

    # using ec2 'tags' (assumes aws inventory)
    development: "'devel' in (ec2_tags|list)"

    # using other host properties populated in inventory
    private_only: not (public_dns_name is defined or ip_address is defined)

    # complex group membership
    multi_group: (group_names | intersect(['alpha', 'beta', 'omega'])) | length >= 2

keyed_groups:
    # this creates a group per distro (distro_CentOS, distro_Debian) and assigns the hosts that have matching values to it,
    # using the default separator "_"
    - prefix: distro
      key: ansible_distribution

    # the following examples assume the first inventory is from the `aws_ec2` plugin
    # this creates a group per ec2 architecture and assign hosts to the matching ones (arch_x86_64, arch_sparc, etc)
    - prefix: arch
      key: architecture

    # this creates a group per ec2 region like "us_west_1"
    - prefix: ""
      separator: ""
      key: placement.region

    # this creates a common parent group for all ec2 availability zones
    - key: placement.availability_zone
      parent_group: all_ec2_zones
```

---

## ansible.builtin.advanced_host_list inventory – Parses a ‘host list’ with ranges — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/advanced_host_list_inventory.html

**Contents:**
- ansible.builtin.advanced_host_list inventory – Parses a ‘host list’ with ranges
- Synopsis
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name advanced_host_list. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.advanced_host_list for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

Parses a host list string as a comma separated values of hosts and supports host ranges.

This plugin only applies to inventory sources that are not paths and contain at least one comma.

**Examples:**

Example 1 (unknown):
```unknown
# simple range
# ansible -i 'host[1:10],' -m ping

# still supports w/o ranges also
# ansible-playbook -i 'localhost,' play.yml
```

---

## How to build your inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/inventory_guide/intro_inventory.html

**Contents:**
- How to build your inventory
- Inventory basics: formats, hosts, and groups
  - Default groups
  - Hosts in multiple groups
  - Grouping groups: parent/child group relationships
  - Adding ranges of hosts
- Passing multiple inventory sources
- Organizing inventory in a directory
  - Managing inventory load order
- Adding variables to inventory

Ansible automates tasks on managed nodes or “hosts” in your infrastructure by using a list or group of lists known as inventory. Ansible composes its inventory from one or more ‘inventory sources’. While one of these sources can be the list of host names you pass at the command line, most Ansible users create inventory files. Your inventory defines the managed nodes you automate and the variables associated with those hosts. You can also specify groups. Groups allow you to reference multiple associated hosts to target for your automation or to define variables in bulk. Once you define your inventory, you use patterns to select the hosts or groups you want Ansible to run against.

The simplest inventory is a single file that contains a list of hosts and groups. The default location for this file is /etc/ansible/hosts. You can specify a different inventory source or sources at the command line by using the -i <path or expression> option or by using the configuration system.

Ansible Inventory plugins supports a range of formats and sources, which makes your inventory flexible and customizable. As your inventory expands, you might need more than a single file to organize your hosts and groups. You have the following common options beyond the /etc/ansible/hosts file:

You can generate an inventory dynamically. For example, you can use an inventory plugin to list resources in one or more cloud providers or other sources. See Working with dynamic inventory.

You can use multiple sources for inventory, including both dynamic inventory and static files. See Passing multiple inventory sources.

You can create a directory with multiple inventory sources, static or dynamic. See Organizing inventory in a directory.

Inventory basics: formats, hosts, and groups

Hosts in multiple groups

Grouping groups: parent/child group relationships

Adding ranges of hosts

Passing multiple inventory sources

Organizing inventory in a directory

Managing inventory load order

Adding variables to inventory

Assigning a variable to one machine: host variables

Defining variables in INI format

Assigning a variable to many machines: group variables

Inheriting variable values: group variables for groups of groups

Organizing host and group variables

How variables are merged

Managing inventory variable load order

Connecting to hosts: behavioral inventory parameters

Non-SSH connection types

Inventory setup examples

Example: One inventory per environment

Example: Group by function

Example: Group by location

The following YAML snippets include an ellipsis (…) to indicate that the snippets are part of a larger YAML file. You can find out more about YAML syntax at YAML Basics.

You can create your inventory file in one of many formats, depending on the inventory plugins you have. The most common formats are INI and YAML because Ansible includes built-in support for them. This introduction focuses on these two formats, but many other formats and sources are possible.

A basic INI /etc/ansible/hosts might look like this:

The headings in brackets are group names. You can use group names to classify hosts and to decide which hosts you are controlling at what times and for what purpose. Group names should follow the same guidelines as Creating valid variable names.

Here’s the same basic inventory file in YAML format:

Even if you do not define any groups in your inventory, Ansible creates two default groups: all and ungrouped. The all group contains every host. The ungrouped group contains all hosts that do not belong to any other group. Every host always belongs to at least two groups (all and ungrouped, or all and another group). For example, in the basic inventory above, the host mail.example.com belongs to the all and ungrouped groups. The host two.example.com belongs to the all and dbservers groups. Although all and ungrouped are always present, they can be implicit and might not appear in group listings like group_names.

You can put a host in more than one group. For example, you can include a production web server in a data center in Atlanta in the [prod], [atlanta], and [webservers] groups. You can create groups that track the following criteria:

What - An application, stack, or microservice (for example, database servers, web servers, and so on).

Where - A datacenter or region, to talk to local DNS, storage, and so on (for example, east, west).

When - The development stage, to avoid testing on production resources (for example, prod, test).

The following example extends the previous YAML inventory to include what, when, and where:

As the example shows, one.example.com exists in the dbservers, east, and prod groups.

You can create parent/child relationships among groups. Parent groups are also known as nested groups or groups of groups. For example, if all your production hosts are already in groups such as atlanta_prod and denver_prod, you can create a production group that includes those smaller groups. This approach reduces maintenance because you add or remove hosts from the parent group by editing the child groups.

To create parent/child relationships for groups, use one of the following methods:

In INI format, use the :children suffix.

In YAML format, use the children: entry.

The following example shows the same inventory as above, simplified with parent groups for the prod and test groups:

Note the following properties of child groups:

Any host that is a member of a child group is automatically a member of the parent group.

A group can have multiple parents and children, but not circular relationships.

A host can be in multiple groups, but Ansible processes only one instance of the host at runtime. Ansible merges the data from multiple groups.

Hosts and groups are always ‘global’. If you define a host or group more than once under different ‘branches’ or ‘instances’, the host or group remains the same entity. Defining a host or group more than once either adds new information to it or overwrites any conflicting information with the latest definition.

Some plugins, like YAML and INI, support adding ranges of hosts. If you have many hosts with a similar pattern, you can add the hosts as a range rather than listing each hostname separately:

You can specify a stride (increments between sequence numbers) when you define a numeric range of hosts:

The example above matches the subdomains www01, www03, www05, …, www49, but not www00, www02, www50, and so on, because the stride (increment) is 2 units for each step.

For numeric patterns, you can include or remove leading zeros as desired. Ranges are inclusive. You can also define alphabetic ranges:

You can target multiple inventory sources (static files, directories, dynamic inventory scripts or anything supported by inventory plugins) at the same time. To do this, specify multiple inventory sources from the command line (see below) or by configuration, either by setting ANSIBLE_INVENTORY or in ansible.cfg (DEFAULT_HOST_LIST). This capability can be useful when you want to target normally separate environments, like staging and production, at the same time for a specific action.

To target two inventory sources from the command line:

You can consolidate multiple inventory sources in a single directory. The simplest version of this approach is a directory with multiple files instead of a single inventory file. Maintaining a single file becomes difficult when the file gets too long. If you have multiple teams and multiple automation projects, creating one inventory file per team or project lets everyone easily find the hosts and groups that matter to them. You can also still use the files individually or in subsets, depending on how you configure or call Ansible.

These files can use all formats or plugin configurations (for example, YAML or INI). In this case, your directory becomes your ‘single’ inventory source, and Ansible aggregates the multiple sources it finds in that directory. By default, Ansible ignores some directories and extensions, but you can change this behavior in the configuration (INVENTORY_IGNORE_PATTERNS and INVENTORY_IGNORE_EXTS).

You can also combine multiple inventory source types in an inventory directory. This method can be useful for combining static and dynamic hosts and managing them as one inventory. The following inventory directory combines an inventory plugin source, a dynamic inventory script, and a file with static hosts:

You can target this inventory directory as follows:

You can also configure the inventory directory in your ansible.cfg file. See Configuring Ansible for more details.

Ansible reads and loads files from the top directory down in alphabetically sorted order.

Ansible loads inventory sources in the order you supply them. It defines hosts, groups, and variables as it encounters them in the source files, adding the all and ungrouped groups at the end if needed.

Depending on the inventory plugin or plugins you use, you might need to rearrange the order of sources to ensure that parent/child-defined groups or hosts exist as the plugins expect. Otherwise, you might encounter a parsing error. For example, the YAML and INI inventory plugins discard empty groups (groups with no associated hosts) when they finish processing each source.

If you define a variable multiple times, Ansible overwrites the previous value. The last definition wins.

You can define variables that relate to a specific host or group in your inventory. A simple way to start is by adding variables directly to the hosts and groups in a YAML or INI inventory source.

This guide documents how to add variables in the inventory source for simplicity. However, you can also use Vars plugins to add variables from many other sources. By default, Ansible ships with the host_group_vars plugin, which allows you to define variables in separate host and group variable files. Using separate files is a more robust approach to describing your system policy than defining variables in the inventory source. See Organizing host and group variables for guidelines on how to store variable values in individual files in the ‘host_vars’ and ‘group_vars’ directories.

You can easily assign a variable to a single host and then use that variable later in playbooks. You can do this directly in your inventory file.

Unique values like non-standard SSH ports work well as host variables. You can add them to your Ansible inventory by adding the port number after the hostname with a colon:

You can use host variables to define ‘Connection variables’. Connection variables configure connection, shell, and become plugins to enable task execution on the host. For example:

The inventory_hostname is the unique identifier for a host in Ansible. This identifier can be an IP address or a hostname, but it can also be just an ‘alias’ or short name for the host.

In this example, running Ansible against the host alias “jumper” connects to 192.0.2.50 on port 5555. See behavioral inventory parameters to further customize the connection to hosts.

This feature is also useful for targeting the same host more than once, but remember that tasks can run in parallel:

Ansible interprets values that you pass in the INI format by using the key=value syntax differently depending on where you declare them:

When you declare a value inline with the host, Ansible interprets the INI value as a Python literal structure (for example, a string, number, tuple, list, dict, boolean, or None). Host lines accept multiple key=value parameters per line. Therefore, you need a way to indicate that a space is part of a value rather than a separator. You can quote values that contain whitespace (using single or double quotes). See the Python shlex parsing rules for details.

When you declare a value in a :vars section, Ansible interprets the INI value as a string. For example, var=FALSE creates a string with the value ‘FALSE’. Unlike host lines, :vars sections accept only a single entry per line, so everything after the = becomes the value for the entry.

If you need a variable from an INI inventory to have a certain type (for example, a string or a boolean), always specify the type with a filter in your task. Do not rely on types that you set in INI inventories when you consume variables.

Consider using the YAML format for inventory sources to avoid confusion about the actual type of a variable. The YAML inventory plugin processes variable values consistently and correctly.

If all hosts in a group share a variable value, you can apply that variable to an entire group at once.

Group variables are a convenient way to apply variables to multiple hosts at once. Before executing, however, Ansible always flattens variables, including inventory variables, to the host level. If a host is a member of multiple groups, Ansible reads variable values from all of those groups. If you assign different values to the same variable in different groups, Ansible chooses which value to use based on internal rules for merging.

You can apply variables to parent groups (nested groups or groups of groups) as well as to child groups. The syntax is the same: :vars for INI format and vars: for YAML format:

A child group’s variables have higher precedence (they override) than a parent group’s variables.

Although you can define variables in the inventory source, you can also use Vars plugins to define alternate sources for your variables.

The default vars plugin that Ansible ships with, host_group_vars, lets you use separate host and group variable files. This method helps you organize your variable values more easily. You can also use lists and hash data in these files, which you cannot do in your main inventory file.

For the host_group_vars plugin, your host and group variable files must use YAML syntax. Valid file extensions are ‘.yml’, ‘.yaml’, ‘.json’, or no file extension. See YAML Syntax if you are new to YAML.

The host_group_vars plugin loads host and group variable files by searching paths relative to the inventory source or the playbook file. If your inventory file at /etc/ansible/hosts contains a host named ‘foosball’ that belongs to the raleigh and webservers groups, that host will use variables from the YAML files in the following locations:

For example, if you group hosts in your inventory by datacenter, and each datacenter uses its own NTP server and database server, you can create a file named /etc/ansible/group_vars/raleigh to store the variables for the raleigh group:

You can also create directories named after your groups or hosts. Ansible reads all the files in these directories in lexicographical order. Here is an example with the ‘raleigh’ group:

All hosts in the ‘raleigh’ group have the variables that you define in these files available to them. This method is very useful for keeping your variables organized when a single file gets too big, or when you want to use Ansible Vault on some group variables.

Ansible’s host_group_vars vars plugin can also add group_vars/ and host_vars/ directories to your playbook directory when you use ansible-playbook. However, not all Ansible commands have a playbook (for example, ansible or ansible-console). For those commands, you can use the --playbook-dir option to provide the directory on the command line. If you have sources for the vars plugins relative to both the playbook directory and the inventory directory, the variables that Ansible sources relative to the playbook override the variables that it sources relative to the inventory source.

To track changes to your inventory and variable definitions, keep your inventory sources and their relative variable directories and files in a Git repository or other version control system.

Ansible merges variables from different sources and applies precedence to some variables over others according to a set of rules. For example, variables that occur higher in an inventory can override variables that occur lower in the inventory. See Variable precedence: where should I put a variable? for more information.

Before it runs a play, Ansible merges and flattens variables to the specific host. This process keeps Ansible focused on the Host and Task, so groups do not survive outside of inventory and host matching. By default, Ansible overwrites variables, including the ones that you define for a group or host (see DEFAULT_HASH_BEHAVIOUR). The order/precedence for inventory entities is (from lowest to highest):

The following list shows the order of precedence for inventory entities, from lowest to highest:

all group (because it is the ‘parent’ of all other groups)

By default, Ansible merges groups at the same parent/child level in alphabetical order. Variables from the last group that Ansible loads overwrite variables from the previous groups. For example, Ansible merges an a_group with a b_group, and matching variables from b_group overwrite the variables in a_group.

You can fine-tune this merge behavior by setting the group variable ansible_group_priority. This variable overrides the alphabetical sorting for the merge order for groups of the same level (after Ansible resolves the parent/child order). The larger the number, the later Ansible merges the group, giving it higher priority. This variable defaults to 1 if you do not set it. For example:

In this example, if both groups have the same priority, the result would normally be testvar == b. However, because we give a_group a higher priority, the result is testvar == a.

You can set ansible_group_priority only in an inventory source, not in group_vars/. Ansible uses this variable when it loads the group_vars/ directory.

This section describes how to control variable precedence by managing the load order of inventory sources. You can pass sources in a specific order at the command line or use prefixes in the filenames of sources within a directory.

When you use multiple inventory sources, remember that Ansible resolves any variable conflicts according to the rules described in How variables are merged and Variable precedence: where should I put a variable?. You can control the merging order of variables in inventory sources to get the variable value you need.

When you pass multiple inventory sources at the command line, Ansible merges variables in the order you pass those parameters. If the [all:vars] section in the staging inventory defines myvar = 1 and the production inventory defines myvar = 2, then the following outcomes are true:

If you pass -i staging -i production, Ansible runs the playbook with myvar = 2.

If you pass -i production -i staging, Ansible runs the playbook with myvar = 1.

When you put multiple inventory sources in a directory, Ansible merges the sources in alphabetical order according to their filenames. You can control the load order by adding prefixes to the files:

If 01-openstack.yml defines myvar = 1 for the group all, 02-dynamic-inventory.py defines myvar = 2, and 03-static-inventory defines myvar = 3, Ansible runs the playbook with myvar = 3.

For more details on inventory plugins and dynamic inventory scripts see Inventory plugins and Working with dynamic inventory.

As described above, you can set the following variables to control how Ansible interacts with remote hosts.

Ansible does not expose a channel to allow communication between the user and the ssh process to accept a password manually to decrypt an ssh key when using the ssh connection plugin (which is the default). The use of ssh-agent is highly recommended.

Specifies the connection type to the host. This can be the name of any Ansible connection plugin. SSH protocol types are ssh or paramiko. The default is ssh.

General for all connections:

Specifies the resolvable name or IP of the host to connect to, if it is different from the alias you wish to give to it. Never set it to depend on inventory_hostname. If you really need something like that, use inventory_hostname_short so it can work with delegation.

The connection port number, if not the default (22 for ssh).

The username to use when connecting (logging in) to the host.

The password to use to authenticate to the host. (Never store this variable in plain text. Always use a vault. See Keep vaulted variables safely visible.)

Specific to the SSH connection plugin:

Private key file used by SSH. This is useful if you use multiple keys and you do not want to use SSH agent.

Ansible always appends this setting to the default command line for sftp, scp, and ssh. This is useful for configuring a ProxyCommand for a certain host or group.

Ansible always appends this setting to the default sftp command line.

Ansible always appends this setting to the default scp command line.

Ansible always appends this setting to the default ssh command line.

Specifies whether to use SSH pipelining. This can override the pipelining setting in ansible.cfg.

This setting overrides the default behavior to use the system ssh. It can override the ssh_executable setting in the ssh_connection section of ansible.cfg.

Privilege escalation (see Ansible Privilege Escalation for further details):

Equivalent to ansible_sudo or ansible_su; allows you to force privilege escalation.

Allows you to set the privilege escalation method to a matching become plugin.

Equivalent to ansible_sudo_user or ansible_su_user; allows you to set the user you become through privilege escalation.

Equivalent to ansible_sudo_password or ansible_su_password; allows you to set the privilege escalation password. (Never store this variable in plain text. Always use a vault. See Keep vaulted variables safely visible.)

Equivalent to ansible_sudo_exe or ansible_su_exe; allows you to set the executable for the escalation method you selected.

Equivalent to ansible_sudo_flags or ansible_su_flags; allows you to set the flags passed to the selected escalation method. You can also set this globally in ansible.cfg in the become_flags option under privilege_escalation.

Remote host environment parameters:

Specifies the shell type of the target system. You should not use this setting unless you have set the ansible_shell_executable to a non-Bourne (sh) compatible shell. By default, Ansible formats commands using sh-style syntax. If you set this to csh or fish, commands that Ansible executes on target systems follow those shell’s syntax instead.

Specifies the target host Python path. This is useful for systems with more than one Python or for systems where Python is not located at /usr/bin/python, such as *BSD, or where /usr/bin/python is not a 2.X series Python. We do not use the /usr/bin/env mechanism because that requires the remote user’s path to be set correctly and also assumes the python executable is named python, where the executable might be named something like python2.6.

Works for any language, such as Ruby or Perl, and works just like ansible_python_interpreter. This variable replaces the shebang of modules that will run on that host.

This setting sets the shell the Ansible control node will use on the target machine. It overrides executable in ansible.cfg, which defaults to /bin/sh. You should only change this value if it is not possible to use /bin/sh (in other words, if /bin/sh is not installed on the target machine or cannot be run from sudo.).

Examples from an Ansible-INI host file:

As stated in the previous section, Ansible executes playbooks over SSH by default, but it is not limited to this connection type. You can change the connection type with the host-specific parameter ansible_connection=<connection plugin name>. For a full list of available plugins and examples, see Plugin list.

See also Sample Ansible setup, which shows inventory along with playbooks and other Ansible artifacts.

If you need to manage multiple environments, consider defining only the hosts of a single environment in each inventory. This way, it is harder to, for example, accidentally change the state of nodes inside the “test” environment when you wanted to update some “staging” servers.

For the example mentioned above, you could have an inventory_test file:

That file only includes hosts that are part of the “test” environment. You can define the “staging” machines in another file called inventory_staging:

To apply a playbook called site.yml to all the app servers in the test environment, use the following command:

In the previous section, you already saw an example of using groups to cluster hosts that have the same function. This approach allows you, for example, to define firewall rules inside a playbook or role that affect only database servers:

Other tasks might focus on where a certain host is located. Let’s say that db01.test.example.com and app01.test.example.com are located in DC1, while db02.test.example.com is in DC2:

In practice, you might end up mixing all these setups. For example, you might need to update all nodes in a specific data center on one day, while on another day, you might need to update all the application servers no matter their location.

Pulling inventory from dynamic or static sources

Pulling inventory from dynamic sources, such as cloud providers

Examples of basic commands

Learning Ansible’s configuration, deployment, and orchestration language.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
mail.example.com

[webservers]
foo.example.com
bar.example.com

[dbservers]
one.example.com
two.example.com
three.example.com
```

Example 2 (unknown):
```unknown
ungrouped:
  hosts:
    mail.example.com:
webservers:
  hosts:
    foo.example.com:
    bar.example.com:
dbservers:
  hosts:
    one.example.com:
    two.example.com:
    three.example.com:
```

Example 3 (unknown):
```unknown
ungrouped:
  hosts:
    mail.example.com:
webservers:
  hosts:
    foo.example.com:
    bar.example.com:
dbservers:
  hosts:
    one.example.com:
    two.example.com:
    three.example.com:
east:
  hosts:
    foo.example.com:
    one.example.com:
    two.example.com:
west:
  hosts:
    bar.example.com:
    three.example.com:
prod:
  hosts:
    foo.example.com:
    one.example.com:
    two.example.com:
test:
  hosts:
    bar.example.com:
    three.example.com:
```

Example 4 (unknown):
```unknown
ungrouped:
  hosts:
    mail.example.com:
webservers:
  hosts:
    foo.example.com:
    bar.example.com:
dbservers:
  hosts:
    one.example.com:
    two.example.com:
    three.example.com:
east:
  hosts:
    foo.example.com:
    one.example.com:
    two.example.com:
west:
  hosts:
    bar.example.com:
    three.example.com:
prod:
  children:
    east:
test:
  children:
    west:
```

---

## ansible.builtin.inventory_hostnames lookup – list of inventory hosts matching a host pattern — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/inventory_hostnames_lookup.html

**Contents:**
- ansible.builtin.inventory_hostnames lookup – list of inventory hosts matching a host pattern
- Synopsis
- Notes
- Examples
- Return Value
  - Authors
  - Collection links

This lookup plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name inventory_hostnames. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.inventory_hostnames for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same lookup plugin name.

This lookup understands ‘host patterns’ as used by the hosts: keyword in plays and can return a list of matching hosts from inventory

this is only worth for ‘hostname patterns’ it is easier to loop over the group/group_names variables otherwise.

list / elements=string

list of hostnames that matched the host pattern in inventory

**Examples:**

Example 1 (unknown):
```unknown
- name: show all the hosts matching the pattern, i.e. all but the group www
  ansible.builtin.debug:
    msg: "{{ item }}"
  with_inventory_hostnames:
    - all:!www
```

---

## Developing dynamic inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_inventory.html

**Contents:**
- Developing dynamic inventory
- Inventory sources
- Inventory plugins
  - Developing an inventory plugin
    - verify_file method
    - parse method
    - inventory object
    - inventory cache
    - constructed features
  - Common format for inventory sources

Ansible can pull inventory information from dynamic sources, including cloud sources, by using the supplied inventory plugins. For details about how to pull inventory information, see Working with dynamic inventory. If the source you want is not currently covered by existing plugins, you can create your own inventory plugin as with any other plugin type.

In previous versions, you had to create a script or program that could output JSON in the correct format when invoked with the proper arguments. You can still use and write inventory scripts, as we ensured backwards compatibility through the script inventory plugin and there is no restriction on the programming language used. If you choose to write a script, however, you will need to implement some features yourself such as caching, configuration management, dynamic variable and group composition, and so on. If you use inventory plugins instead, you can use the Ansible codebase and add these common features automatically.

Developing an inventory plugin

Common format for inventory sources

Inventory script conventions

Tuning the external inventory script

Inventory sources are the input strings that inventory plugins work with. An inventory source can be a path to a file or to a script, or it can be raw data that the plugin can interpret.

The table below shows some examples of inventory plugins and the source types that you can pass to them with -i on the command line.

A comma-separated list of hosts

Path to a YAML format data file

Path to a YAML configuration file

Path to an INI formatted data file

Path to a YAML configuration file

Path to an executable that outputs JSON

Like most plugin types (except modules), inventory plugins must be developed in Python. They execute on the control node and should therefore adhere to the Control node requirements.

Most of the documentation in Developing plugins also applies here. You should read that document first for a general understanding and then come back to this document for specifics on inventory plugins.

Normally, inventory plugins are executed at the start of a run, and before the playbooks, plays, or roles are loaded. However, you can use the meta: refresh_inventory task to clear the current inventory and execute the inventory plugins again, and this task will generate a new inventory.

If you use the persistent cache, inventory plugins can also use the configured cache plugin to store and retrieve data. Caching inventory avoids making repeated and costly external calls.

The first thing you want to do is use the base class:

If the inventory plugin is in a collection, the NAME should be in the ‘namespace.collection_name.myplugin’ format. The base class has a couple of methods that each plugin should implement and a few helpers for parsing the inventory source and updating the inventory.

After you have the basic plugin working, you can incorporate other features by adding more base classes:

For the bulk of the work in a plugin, we mostly want to deal with 2 methods verify_file and parse.

Ansible uses this method to quickly determine if the inventory source is usable by the plugin. The determination does not need to be 100% accurate, as there might be an overlap in what plugins can handle and by default Ansible will try the enabled plugins as per their sequence.

In the above example, from the virtualbox inventory plugin, we screen for specific file name patterns to avoid attempting to consume any valid YAML file. You can add any type of condition here, but the most common one is ‘extension matching’. If you implement extension matching for YAML configuration files, the path suffix <plugin_name>.<yml|yaml> should be accepted. All valid extensions should be documented in the plugin description.

The following is another example that does not use a ‘file’ but the inventory source string itself, from the host list plugin:

This method is just to expedite the inventory process and avoid unnecessary parsing of sources that are easy to filter out before causing a parse error.

This method does the bulk of the work in the plugin. It takes the following parameters:

inventory: inventory object with existing data and the methods to add hosts/groups/variables to inventory

loader: Ansible’s DataLoader. The DataLoader can read files, auto load JSON/YAML and decrypt vaulted data, and cache read files.

path: string with inventory source (this is usually a path, but is not required)

cache: indicates whether the plugin should use or avoid caches (cache plugin and/or loader)

The base class does some minimal assignment for reuse in other methods.

It is up to the plugin now to parse the provided inventory source and translate it into Ansible inventory. To facilitate this, the example below uses a few helper functions:

The specifics will vary depending on API and structure returned. Remember that if you get an inventory source error or any other issue, you should raise AnsibleParserError to let Ansible know that the source was invalid or the process failed.

For examples on how to implement an inventory plugin, see the source code here: lib/ansible/plugins/inventory.

The inventory object passed to parse has helpful methods for populating inventory.

add_group adds a group to inventory if it doesn’t already exist. It takes the group name as the only positional argument.

add_child adds a group or host that exists in inventory to a parent group in inventory. It takes two positional arguments, the name of the parent group and the name of the child group or host.

add_host adds a host to inventory if it doesn’t already exist, optionally to a specific group. It takes the host name as the first argument and accepts two optional keyword arguments, group and port. group is the name of a group in inventory, and port is an integer.

set_variable adds a variable to a group or host in inventory. It takes three positional arguments: the name of the group or host, the name of the variable, and the value of the variable.

To create groups and variables using Jinja2 expressions, see the section on implementing constructed features below.

To see other inventory object methods, see the source code here: lib/ansible/inventory/data.py.

To cache the inventory, extend the inventory plugin documentation with the inventory_cache documentation fragment and use the Cacheable base class.

Next, load the cache plugin specified by the user to read from and update the cache. If your inventory plugin uses YAML-based configuration files and the _read_config_data method, the cache plugin is loaded within that method. If your inventory plugin does not use _read_config_data, you must load the cache explicitly with load_cache_plugin.

Before using the cache plugin, you must retrieve a unique cache key by using the get_cache_key method. This task needs to be done by all inventory modules using the cache, so that you don’t use/overwrite other parts of the cache.

Now that you’ve enabled caching, loaded the correct plugin, and retrieved a unique cache key, you can set up the flow of data between the cache and your inventory using the cache parameter of the parse method. This value comes from the inventory manager and indicates whether the inventory is being refreshed (such as by the --flush-cache or the meta task refresh_inventory). Although the cache shouldn’t be used to populate the inventory when being refreshed, the cache should be updated with the new inventory if the user has enabled caching. You can use self._cache like a dictionary. The following pattern allows refreshing the inventory to work in conjunction with caching.

After the parse method is complete, the contents of self._cache is used to set the cache plugin if the contents of the cache have changed.

set_cache_plugin forces the cache plugin to be set with the contents of self._cache, before the parse method completes

update_cache_if_changed sets the cache plugin only if self._cache has been modified, before the parse method completes

clear_cache flushes the cache, ultimately by calling the cache plugin’s flush() method, whose implementation is dependent upon the particular cache plugin in use. Note that if the user is using the same cache backend for facts and inventory, both will get flushed. To avoid this, the user can specify a distinct cache backend in their inventory plugin configuration.

Inventory plugins can create host variables and groups from Jinja2 expressions and variables by using features from the constructed inventory plugin. To do this, use the Constructable base class and extend the inventory plugin’s documentation with the constructed documentation fragment.

There are three main options in the constructed documentation fragment:

compose creates variables using Jinja2 expressions. This is implemented by calling the _set_composite_vars method. keyed_groups creates groups of hosts based on variable values. This is implemented by calling the _add_host_to_keyed_groups method. groups creates groups based on Jinja2 conditionals. This is implemented by calling the _add_host_to_composed_groups method.

Each method should be called for every host added to inventory. Three positional arguments are required: the constructed option, a dictionary of variables, and a host name. Calling the method _set_composite_vars first will allow keyed_groups and groups to use the composed variables.

By default, undefined variables are ignored. This is permitted by default for compose so you can make the variable definitions depend on variables that will be populated later in a play from other sources. For groups, it allows using variables that are not always present without having to use the default filter. To support configuring undefined variables to be an error, pass the constructed option strict to each of the methods as a keyword argument.

keyed_groups and groups use any variables already associated with the host (for example, from an earlier inventory source). _add_host_to_keyed_groups and add_host_to_composed_groups can turn this off by passing the keyword argument fetch_hostvars.

Here is an example using all three methods:

By default, group names created with _add_host_to_composed_groups() and _add_host_to_keyed_groups() are valid Python identifiers. Invalid characters are replaced with an underscore _. A plugin can change the sanitization used for the constructed features by setting self._sanitize_group_name to a new function. The core engine also does sanitization, so if the custom function is less strict it should be used in conjunction with the configuration setting TRANSFORM_INVALID_GROUP_CHARS.

To simplify development, most plugins use a standard YAML-based configuration file as the inventory source. The file has only one required field plugin, which should contain the name of the plugin that is expected to consume the file. Depending on other common features used, you might need other fields, and you can add custom options in each plugin as required. For example, if you use the integrated caching, cache_plugin, cache_timeout and other cache-related fields could be present.

From Ansible 2.5 onwards, we include the auto inventory plugin and enable it by default. If the plugin field in your standard configuration file matches the name of your inventory plugin, the auto inventory plugin will load your plugin. The ‘auto’ plugin makes it easier to use your plugin without having to update configurations.

Even though we now have inventory plugins, we still support inventory scripts, not only for backwards compatibility but also to allow users to use other programming languages.

Inventory scripts must accept the --list and --host <hostname> arguments. Although other arguments are allowed, Ansible will not use them. Such arguments might still be useful for executing the scripts directly.

When the script is called with the single argument --list, the script must output to stdout a JSON object that contains all the groups to be managed. Each group’s value should be either an object containing a list of each host, any child groups, and potential group variables, or simply a list of hosts:

If any of the elements of a group are empty, they may be omitted from the output.

When called with the argument --host <hostname> (where <hostname> is a host from above), the script must print a JSON object, either empty or containing variables to make them available to templates and playbooks. For example:

Printing variables is optional. If the script does not print variables, it should print an empty JSON object.

The stock inventory script system mentioned above works for all versions of Ansible, but calling --host for every host can be rather inefficient, especially if it involves API calls to a remote subsystem.

To avoid this inefficiency, if the inventory script returns a top-level element called “_meta”, it is possible to return all the host variables in a single script execution. When this meta element contains a value for “hostvars”, the inventory script will not be invoked with --host for each host. This behavior results in a significant performance increase for large numbers of hosts.

The data to be added to the top-level JSON object looks like this:

To satisfy the requirements of using _meta, to prevent ansible from calling your inventory with --host you must at least populate _meta with an empty hostvars object. For example:

If you intend to replace an existing static inventory file with an inventory script, it must return a JSON object which contains an ‘all’ group that includes every host in the inventory as a member and every group in the inventory as a child. It should also include an ‘ungrouped’ group which contains all hosts which are not members of any other group. A skeleton example of this JSON object is:

An easy way to see how this should look is using ansible-inventory, which also supports --list and --host parameters like an inventory script would.

Python API to Playbooks and Ad Hoc Task Execution

Get started with developing a module

How to develop plugins

REST API endpoint and GUI for Ansible, syncs with dynamic inventory

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (python):
```python
from ansible.plugins.inventory import BaseInventoryPlugin

class InventoryModule(BaseInventoryPlugin):

    NAME = 'myplugin'  # used internally by Ansible, it should match the file name but not required
```

Example 2 (python):
```python
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'myplugin'
```

Example 3 (python):
```python
def verify_file(self, path):
    ''' return true/false if this is possibly a valid file for this plugin to consume '''
    valid = False
    if super(InventoryModule, self).verify_file(path):
        # base class verifies that file exists and is readable by current user
        if path.endswith(('virtualbox.yaml', 'virtualbox.yml', 'vbox.yaml', 'vbox.yml')):
            valid = True
    return valid
```

Example 4 (python):
```python
def verify_file(self, path):
    ''' don't call base class as we don't expect a path, but a host list '''
    host_list = path
    valid = False
    b_path = to_bytes(host_list, errors='surrogate_or_strict')
    if not os.path.exists(b_path) and ',' in host_list:
        # the path does NOT exist and there is a comma to indicate this is a 'host list'
        valid = True
    return valid
```

---

## ansible-inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-inventory.html

**Contents:**
- ansible-inventory
- Synopsis
- Description
- Common Options
- ARGUMENTS
- Environment
- Files
- Author
- License
- See also

Show Ansible inventory information, by default it uses the inventory script JSON format

used to display or dump the configured inventory as Ansible sees it

When doing –list, represent in a way that is optimized for export,not as an accurate representation of how Ansible has processed it

clear the fact cache for every host in inventory

create inventory graph, if supplying pattern it must be a valid group name. It will ignore limit

Output specific host info, works as inventory script. It will ignore limit

Output all hosts info, works as inventory script

When doing –list, send the inventory to a file instead of to the screen

Since this tool does not use playbooks, use this as a substitute playbook directory. This sets the relative path for many features including roles/ group_vars/ etc.

Use TOML format instead of default JSON, ignored for –graph

Add vars to graph display, ignored unless used with –graph

the vault identity to use. This argument may be specified multiple times.

show program’s version number, config file location, configured module search path, module location, executable location and exit

ask for vault password

set additional variables as key=value or YAML/JSON, if filename prepend with @. This argument may be specified multiple times.

show this help message and exit

specify inventory host path or comma separated host list. This argument may be specified multiple times.

further limit selected hosts to an additional pattern

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

Use YAML format instead of default JSON, ignored for –graph

The name of a group in the inventory, relevant when using –graph

The following environment variables may be specified.

ANSIBLE_INVENTORY – Override the default ansible inventory file

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/hosts – Default inventory file

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-config(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-inventory [-h] [--version] [-v] [-i INVENTORY] [-l SUBSET]
                      [--flush-cache] [--vault-id VAULT_IDS]
                      [-J | --vault-password-file VAULT_PASSWORD_FILES]
                      [--playbook-dir BASEDIR] [-e EXTRA_VARS] [--list]
                      [--host HOST] [--graph] [-y] [--toml] [--vars]
                      [--export] [--output OUTPUT_FILE]
                      [group]
```

---

## Inventory plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/inventory.html

**Contents:**
- Inventory plugins
- Enabling inventory plugins
- Using inventory plugins
- Plugin list

Enabling inventory plugins

Using inventory plugins

Inventory plugins allow users to point at data sources to compile the inventory of hosts that Ansible uses to target tasks, either using the -i /path/to/file and/or -i 'host1, host2' command line parameters or from other configuration sources. If necessary, you can create custom inventory plugins.

Most inventory plugins shipped with Ansible are enabled by default or can be used with the auto plugin.

In some circumstances, for example, if the inventory plugin does not use a YAML configuration file, you may need to enable the specific plugin. You can do this by setting enable_plugins in your ansible.cfg file in the [inventory] section. Modifying this will override the default list of enabled plugins. Here is the default list of enabled plugins that ships with Ansible:

If the plugin is in a collection and is not being picked up by the auto statement, you can append the fully qualified name:

Or, if it is a local plugin, perhaps stored in the path set by DEFAULT_INVENTORY_PLUGIN_PATH, you could reference it as follows:

If you use a plugin that supports a YAML configuration source, make sure that the name matches the name provided in the plugin entry of the inventory source file. For other plugins you must either save it in one of the directory sources configured in ansible.cfg and enable it or add to a collection and then reference it by FQCN.

To use an inventory plugin, you must provide an inventory source. Most of the time this is a file containing host information or a YAML configuration file with options for the plugin. You can use the -i flag to provide inventory sources or configure a default inventory path.

To start using an inventory plugin with a YAML configuration source, create a file with the accepted file name schema documented for the plugin in question, then add plugin: plugin_name. Use the fully qualified name if the plugin is in a collection.

Inventory plugins have required name patterns to which they must conform, for example:

An inventory that includes the kubevirt.core.kubevirt inventory plugin must use the *.kubevirt.yml filename pattern. An inventory that includes the servicenow.servicenow.now inventory plugin must use the *.servicenow.yml filename pattern.

Each plugin should document any naming restrictions. In addition, the YAML config file must end with the extension yml or yaml to be enabled by default with the auto plugin (otherwise, see the section above on enabling plugins).

After providing any required options, you can view the populated inventory with ansible-inventory -i demo.aws_ec2.yml --graph:

If you are using an inventory plugin in a playbook-adjacent collection and want to test your setup with ansible-inventory, use the --playbook-dir flag.

Your inventory source might be a directory of inventory configuration files. The constructed inventory plugin only operates on those hosts already in inventory, so you may want the constructed inventory configuration parsed at a particular point (such as last). Ansible parses the directory recursively, alphabetically. You cannot configure the parsing approach, so name your files to make it work predictably. Inventory plugins that extend constructed features directly can work around that restriction by adding constructed options in addition to the inventory plugin options. Otherwise, you can use -i with multiple sources to impose a specific order, for example -i demo.aws_ec2.yml -i clouds.yml -i constructed.yml.

You can create dynamic groups using host variables with the constructed keyed_groups option. The option groups can also be used to create groups and compose creates and modifies host variables. Here is an aws_ec2 example utilizing constructed features:

Now the output of ansible-inventory -i demo.aws_ec2.yml --graph:

If a host does not have the variables in the configuration above (in other words, tags.Name, tags, private_ip_address), the host will not be added to groups other than those that the inventory plugin creates and the ansible_host host variable will not be modified.

Inventory plugins that support caching can use the general settings for the fact cache defined in the ansible.cfg file’s [defaults] section or define inventory-specific settings in the [inventory] section. Individual plugins can define plugin-specific cache settings in their config file:

Here is an example of setting inventory caching with some fact caching defaults for the cache plugin used and the timeout in an ansible.cfg file:

You can use ansible-doc -t inventory -l to see the list of available plugins. Use ansible-doc -t inventory <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
```

Example 2 (unknown):
```unknown
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml, namespace.collection_name.inventory_plugin_name
```

Example 3 (unknown):
```unknown
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml, my_plugin
```

Example 4 (unknown):
```unknown
ansible hostname -i inventory_source -m ansible.builtin.ping
```

---

## ansible.builtin.yaml inventory – Uses a specific YAML file as an inventory source. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/yaml_inventory.html

**Contents:**
- ansible.builtin.yaml inventory – Uses a specific YAML file as an inventory source.
- Synopsis
- Parameters
- Notes
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name yaml. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.yaml for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

YAML-based inventory, should start with the all group and contain hosts/vars/children entries.

Host entries can have sub-entries defined, which will be treated as variables.

Vars entries are normal group vars.

Children are ‘child groups’, which can also have their own vars/hosts/children and so on.

File MUST have a valid extension, defined in configuration.

list / elements=string

list of ‘valid’ extensions for files containing YAML

Default: [".yaml", ".yml", ".json"]

Environment variable: ANSIBLE_YAML_FILENAME_EXT

Environment variable: ANSIBLE_INVENTORY_PLUGIN_EXTS

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

If you want to set vars for the all group inside the inventory file, the all group must be the first entry in the file.

Enabled in configuration by default.

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
yaml_valid_extensions = .yaml, .yml, .json
```

Example 2 (unknown):
```unknown
[inventory_plugin_yaml]
yaml_valid_extensions = .yaml, .yml, .json
```

Example 3 (unknown):
```unknown
all: # keys must be unique, i.e. only one 'hosts' per group
    hosts:
        test1:
        test2:
            host_var: value
    vars:
        group_all_var: value
    children:   # key order does not matter, indentation does
        other_group:
            children:
                group_x:
                    hosts:
                        test5   # Note that one machine will work without a colon
                #group_x:
                #    hosts:
                #        test5  # But this won't
                #        test7  #
                group_y:
                    hosts:
                        test6:  # So always use a colon
            vars:
                g2_var2: value3
            hosts:
                test4:
                    ansible_host: 127.0.0.1
        last_group:
            hosts:
                test1 # same host as above, additional group membership
            vars:
                group_last_var: value
```

---

## Working with dynamic inventory — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/inventory_guide/intro_dynamic_inventory.html

**Contents:**
- Working with dynamic inventory
- Inventory script example: Cobbler
- Other inventory scripts
- Using inventory directories and multiple inventory sources
- Static groups of dynamic groups

Inventory script example: Cobbler

Other inventory scripts

Using inventory directories and multiple inventory sources

Static groups of dynamic groups

If your Ansible inventory fluctuates over time, with hosts spinning up and shutting down in response to business demands, the static inventory solutions described in How to build your inventory will not serve your needs. You may need to track hosts from multiple sources: cloud providers, LDAP, Cobbler, and/or enterprise CMDB systems.

Ansible integrates all of these options through a dynamic external inventory system. Ansible supports two ways to connect with external inventory: Inventory plugins and inventory scripts.

Inventory plugins take advantage of the most recent updates to the Ansible Core code. We recommend plugins over scripts for dynamic inventory. You can write your own plugin to connect to additional dynamic inventory sources.

You can still use inventory scripts if you choose. When we implemented inventory plugins, we ensured backwards compatibility through the script inventory plugin. The examples below illustrate how to use inventory scripts.

If you prefer a GUI for handling dynamic inventory, the inventory database on AWX or Red Hat Ansible Automation Platform syncs with all your dynamic inventory sources, provides web and REST access to the results, and offers a graphical inventory editor. With a database record of all of your hosts, you can correlate past event history and see which hosts have had failures on their last playbook runs.

Ansible integrates seamlessly with Cobbler, a Linux installation server originally written by Michael DeHaan and now led by James Cammarata, who works for Ansible.

While primarily used to kickoff OS installations and manage DHCP and DNS, Cobbler has a generic layer that can represent data for multiple configuration management systems (even at the same time) and serve as a ‘lightweight CMDB’.

To tie your Ansible inventory to Cobbler, copy this script to /etc/ansible and chmod +x the file. Run cobblerd any time you use Ansible and use the -i command line option (for example, -i /etc/ansible/cobbler.py) to communicate with Cobbler using Cobbler’s XMLRPC API.

Add a cobbler.ini file in /etc/ansible so Ansible knows where the Cobbler server is and some cache improvements can be used. For example:

First test the script by running /etc/ansible/cobbler.py directly. You should see some JSON data output, but it may not have anything in it just yet.

Let’s explore what this does. In Cobbler, assume a scenario somewhat like the following:

In the example above, the system ‘foo.example.com’ is addressable by ansible directly, but is also addressable when using the group names ‘webserver’ or ‘atlanta’. Since Ansible uses SSH, it contacts system foo over ‘foo.example.com’, only, never just ‘foo’. Similarly, if you tried “ansible foo”, it would not find the system… but “ansible ‘foo*’” would do, because the system DNS name starts with ‘foo’.

The script provides more than host and group info. In addition, as a bonus, when the ‘setup’ module is run (which happens automatically when using playbooks), the variables ‘a’, ‘b’, and ‘c’ will all be auto-populated in the templates:

Which could be executed just like this:

The name ‘webserver’ came from Cobbler, as did the variables for the config file. You can still pass in your own variables like normal in Ansible, but variables from the external inventory script will override any that have the same name.

So, with the template above (motd.j2), this results in the following data being written to /etc/motd for system ‘foo’:

And on system ‘bar’ (bar.example.com):

And technically, though there is no major good reason to do it, this also works:

So, in other words, you can use those variables in arguments/actions as well.

In Ansible 2.10 and later, inventory scripts moved to their associated collections. Many are now in the ansible-community/contrib-scripts repository. We recommend you use Inventory plugins instead.

If the location given to -i in Ansible is a directory (or as so configured in ansible.cfg), Ansible can use multiple inventory sources at the same time. When doing so, it is possible to mix both dynamic and statically managed inventory sources in the same ansible run. Instant hybrid cloud!

In an inventory directory, executable files are treated as dynamic inventory sources and most other files as static sources. Files which end with any of the following are ignored:

You can replace this list with your own selection by configuring an inventory_ignore_extensions list in ansible.cfg, or setting the ANSIBLE_INVENTORY_IGNORE environment variable. The value in either case must be a comma-separated list of patterns, as shown above.

Any group_vars and host_vars subdirectories in an inventory directory are interpreted as expected, making inventory directories a powerful way to organize different sets of configurations. See Passing multiple inventory sources for more information.

When defining groups of groups in the static inventory file, the child groups must also be defined in the static inventory file, otherwise ansible returns an error. If you want to define a static group of dynamic child groups, define the dynamic groups as empty in the static inventory file. For example:

All about static inventory files

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
[cobbler]

# Set Cobbler's hostname or IP address
host = http://127.0.0.1/cobbler_api

# API calls to Cobbler can be slow. For this reason, we cache the results of an API
# call. Set this to the path you want cache files to be written to. Two files
# will be written to this directory:
#   - ansible-cobbler.cache
#   - ansible-cobbler.index

cache_path = /tmp

# The number of seconds a cache file is considered valid. After this many
# seconds, a new API call will be made, and the cache file will be updated.

cache_max_age = 900
```

Example 2 (unknown):
```unknown
cobbler profile add --name=webserver --distro=CentOS6-x86_64
cobbler profile edit --name=webserver --mgmt-classes="webserver" --ksmeta="a=2 b=3"
cobbler system edit --name=foo --dns-name="foo.example.com" --mgmt-classes="atlanta" --ksmeta="c=4"
cobbler system edit --name=bar --dns-name="bar.example.com" --mgmt-classes="atlanta" --ksmeta="c=5"
```

Example 3 (unknown):
```unknown
# file: /srv/motd.j2
Welcome, I am templated with a value of a={{ a }}, b={{ b }}, and c={{ c }}
```

Example 4 (unknown):
```unknown
ansible webserver -m setup
ansible webserver -m template -a "src=/tmp/motd.j2 dest=/etc/motd"
```

---

## ansible.builtin.auto inventory – Loads and executes an inventory plugin specified in a YAML config — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/auto_inventory.html

**Contents:**
- ansible.builtin.auto inventory – Loads and executes an inventory plugin specified in a YAML config
- Synopsis
- Examples
  - Authors
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name auto. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.auto for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

By enabling the auto inventory plugin, any YAML inventory config file with a plugin key at its root will automatically cause the named plugin to be loaded and executed with that config. This effectively provides automatic enabling of all installed/accessible inventory plugins.

To disable this behavior, remove auto from the INVENTORY_ENABLED config element.

Matt Davis (@nitzmahone)

**Examples:**

Example 1 (unknown):
```unknown
# This plugin is not intended for direct use; it is a fallback mechanism for automatic enabling of
# all installed inventory plugins.
```

---

## ansible.builtin.host_list inventory – Parses a ‘host list’ string — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/host_list_inventory.html

**Contents:**
- ansible.builtin.host_list inventory – Parses a ‘host list’ string
- Synopsis
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name host_list. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.host_list for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

Parses a host list string as a comma separated values of hosts

This plugin only applies to inventory strings that are not paths and contain a comma.

**Examples:**

Example 1 (unknown):
```unknown
# define 2 hosts in command line
# ansible -i '10.10.2.6, 10.10.2.4' -m ping all

# DNS resolvable names
# ansible -i 'host1.example.com, host2' -m user -a 'name=me state=absent' all

# just use localhost
# ansible-playbook -i 'localhost,' play.yml -c local
```

---

## ansible.builtin.generator inventory – Uses Jinja2 to construct hosts and groups from patterns — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/generator_inventory.html

**Contents:**
- ansible.builtin.generator inventory – Uses Jinja2 to construct hosts and groups from patterns
- Synopsis
- Parameters
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name generator. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.generator for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

Uses a YAML configuration file with a valid YAML or .config extension to define var expressions and group conditionals

Create a template pattern that describes each host, and then use independent configuration layers

Every element of every layer is combined to create a host for every layer combination

Parent groups can be defined with reference to hosts and other groups using the same template variables

The name key is a template used to generate hostnames based on the layers option. Each variable in the name is expanded to create a cartesian product of all possible layer combinations.

The parents are a list of parent groups that the host belongs to. Each parent item contains a name key, again expanded from the template, and an optional parents key that lists its parents.

Parents can also contain vars, which is a dictionary of vars that is then always set for that variable. This can provide easy access to the group name. E.g set an application variable that is set to the value of the application layer name.

A dictionary of layers, with the key being the layer name, used as a variable name in the host name and parents keys. Each layer value is a list of possible values for that layer.

token that ensures this is a source file for the ‘generator’ plugin.

"ansible.builtin.generator"

**Examples:**

Example 1 (unknown):
```unknown
# inventory.config file in YAML format
# remember to enable this inventory plugin in the ansible.cfg before using
# View the output using `ansible-inventory -i inventory.config --list`
plugin: ansible.builtin.generator
hosts:
    name: "{{ operation }}_{{ application }}_{{ environment }}_runner"
    parents:
      - name: "{{ operation }}_{{ application }}_{{ environment }}"
        parents:
          - name: "{{ operation }}_{{ application }}"
            parents:
              - name: "{{ operation }}"
              - name: "{{ application }}"
          - name: "{{ application }}_{{ environment }}"
            parents:
              - name: "{{ application }}"
                vars:
                  application: "{{ application }}"
              - name: "{{ environment }}"
                vars:
                  environment: "{{ environment }}"
      - name: runner
layers:
    operation:
        - build
        - launch
    environment:
        - dev
        - test
        - prod
    application:
        - web
        - api
```

---

## ansible.builtin.toml inventory – Uses a specific TOML file as an inventory source. — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/toml_inventory.html

**Contents:**
- ansible.builtin.toml inventory – Uses a specific TOML file as an inventory source.
- Synopsis
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name toml. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.toml for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

TOML based inventory format

File MUST have a valid ‘.toml’ file extension

**Examples:**

Example 1 (unknown):
```unknown
# fmt: toml
# Example 1
[all.vars]
has_java = false

[web]
children = [
    "apache",
    "nginx"
]
vars = { http_port = 8080, myvar = 23 }

[web.hosts]
host1 = {}
host2 = { ansible_port = 222 }

[apache.hosts]
tomcat1 = {}
tomcat2 = { myvar = 34 }
tomcat3 = { mysecret = "03#pa33w0rd" }

[nginx.hosts]
jenkins1 = {}

[nginx.vars]
has_java = true

# Example 2
[all.vars]
has_java = false

[web]
children = [
    "apache",
    "nginx"
]

[web.vars]
http_port = 8080
myvar = 23

[web.hosts.host1]
[web.hosts.host2]
ansible_port = 222

[apache.hosts.tomcat1]

[apache.hosts.tomcat2]
myvar = 34

[apache.hosts.tomcat3]
mysecret = "03#pa33w0rd"

[nginx.hosts.jenkins1]

[nginx.vars]
has_java = true

# Example 3
[ungrouped.hosts]
host1 = {}
host2 = { ansible_host = "127.0.0.1", ansible_port = 44 }
host3 = { ansible_host = "127.0.0.1", ansible_port = 45 }

[g1.hosts]
host4 = {}

[g2.hosts]
host4 = {}
```

---

## ansible.builtin.script inventory – Executes an inventory script that returns JSON — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/ansible/builtin/script_inventory.html

**Contents:**
- ansible.builtin.script inventory – Executes an inventory script that returns JSON
- Synopsis
- Parameters
- Notes
- Examples
  - Collection links

This inventory plugin is part of ansible-core and included in all Ansible installations. In most cases, you can use the short plugin name script. However, we recommend you use the Fully Qualified Collection Name (FQCN) ansible.builtin.script for easy linking to the plugin documentation and to avoid conflicting with other collections that may have the same inventory plugin name.

The source provided must be an executable that returns Ansible inventory JSON

The source must accept --list and --host <hostname> as arguments. --host will only be used if no _meta key is present. This is a performance optimization as the script would be called one additional time per host otherwise.

Toggle display of stderr even when script was successful

Environment variable: ANSIBLE_INVENTORY_PLUGIN_SCRIPT_STDERR

Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up. The entry types are also ordered by precedence from low to high priority order. For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

Enabled in configuration by default.

The plugin does not cache results because external inventory scripts are responsible for their own caching.

To write your own inventory script see (Developing dynamic inventory from the documentation site.

To find the scripts that used to be part of the code release, go to https://github.com/ansible-community/contrib-scripts/.

Since 2.19 using a directory as an inventory source will no longer ignore .ini files by default, but you can still update the configuration to do so.

**Examples:**

Example 1 (unknown):
```unknown
[inventory_plugin_script]
always_show_stderr = true
```

Example 2 (python):
```python
# fmt: code

### simple bash script

   #!/usr/bin/env bash

   if [ "$1" == "--list" ]; then
   cat<<EOF
   {
     "bash_hosts": {
       "hosts": [
         "myhost.domain.com",
         "myhost2.domain.com"
       ],
       "vars": {
         "host_test": "test-value"
       }
     },
     "_meta": {
       "hostvars": {
         "myhost.domain.com": {
           "host_specific_test_var": "test-value"
         }
       }
     }
   }
   EOF
   elif [ "$1" == "--host" ]; then
     # this should not normally be called by Ansible as we return _meta above
     if [ "$2" == "myhost.domain.com" ]; then
        echo '{"_meta": {hostvars": {"myhost.domain.com": {"host_specific-test_var": "test-value"}}}}'
     else
        echo '{"_meta": {hostvars": {}}}'
     fi
   else
     echo "Invalid option: use --list or --host <hostname>"
     exit 1
   fi


### python example with ini config

    #!/usr/bin/env python
    """
    # ansible_inventory.py
    """
    import argparse
    import json
    import os.path
    import sys
    from configparser import ConfigParser
    from inventories.custom import MyInventoryAPI

    def load_config() -> ConfigParser:
        cp = ConfigParser()
        config_file = os.path.expanduser("~/.config/ansible_inventory_script.cfg")
        cp.read(config_file)
        if not cp.has_option('DEFAULT', 'namespace'):
            raise ValueError("Missing configuration option: DEFAULT -> namespace")
        return cp


    def get_api_data(namespace: str, pretty=False) -> str:
        """
        :param namespace: parameter for our custom api
        :param pretty: Human readable JSON vs machine readable
        :return: JSON string
        """
        found_data = list(MyInventoryAPI(namespace))
        hostvars = {}
        data = { '_meta': { 'hostvars': {}},}

        groups = found_data['groups'].keys()
        for group in groups:
            groups[group]['hosts'] = found_data[groups].get('host_list', [])
            if group not in data:
                data[group] = {}
            data[group]['hosts'] = found_data[groups].get('host_list', [])
            data[group]['vars'] = found_data[groups].get('info', [])
            data[group]['children'] = found_data[group].get('subgroups', [])

        for host_data in found_data['hosts']:
            for name in host_data.items():
                # turn info into vars
                data['_meta'][name] = found_data[name].get('info', {})
                # set ansible_host if possible
                if 'address' in found_data[name]:
                    data[name]['_meta']['ansible_host'] = found_data[name]['address']
        data['_meta']['hostvars'] = hostvars

        return json.dumps(data, indent=pretty)

    if __name__ == '__main__':

        arg_parser = argparse.ArgumentParser( description=__doc__, prog=__file__)
        arg_parser.add_argument('--pretty', action='store_true', default=False, help="Pretty JSON")
        mandatory_options = arg_parser.add_mutually_exclusive_group()
        mandatory_options.add_argument('--list', action='store', nargs="*", help="Get inventory JSON from our API")
        mandatory_options.add_argument('--host', action='store',
                                       help="Get variables for specific host, not used but kept for compatibility")

        try:
            config = load_config()
            namespace = config.get('DEFAULT', 'namespace')

            args = arg_parser.parse_args()
            if args.host:
                print('{"_meta":{}}')
                sys.stderr.write('This script already provides _meta via --list, so this option is really ignored')
            elif len(args.list) >= 0:
                print(get_api_data(namespace, args.pretty))
            else:
                raise ValueError("Valid options are --list or --host <HOSTNAME>")

        except ValueError:
            raise
```

---

## Connection methods and details — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/inventory_guide/connection_details.html

**Contents:**
- Connection methods and details
- ControlPersist and paramiko
- Setting a remote user
- Setting up SSH keys
- Running against localhost
- Managing host key checking
- Other connection methods

This section shows you how to expand and refine the connection methods Ansible uses for your inventory.

By default, Ansible uses native OpenSSH, because it supports ControlPersist (a performance feature), Kerberos, and options in ~/.ssh/config such as Jump Host setup. If your control machine uses an older version of OpenSSH that does not support ControlPersist, Ansible will fall back to a Python implementation of OpenSSH called ‘paramiko’.

By default, Ansible connects to all remote devices with the username you are using on the control node. If that username does not exist on a remote device, you can set a different username for the connection. If you just need to do some tasks as a different user, look at Understanding privilege escalation: become. You can set the connection user in a playbook:

as a host variable in inventory:

or as a group variable in inventory:

Details on the remote_user keyword and ansible_user variable.

Details on Ansible precedence rules.

By default, Ansible assumes you are using SSH keys to connect to remote machines. SSH keys are encouraged, but you can use password authentication if needed with the --ask-pass option. If you need to provide a password for privilege escalation (sudo, pbrun, and so on), use --ask-become-pass.

Ansible does not expose a channel to allow communication between the user and the ssh process to accept a password manually to decrypt an ssh key when using the ssh connection plugin (which is the default). The use of ssh-agent is highly recommended.

To set up SSH agent to avoid retyping passwords, you can do:

Depending on your setup, you may wish to use Ansible’s --private-key command line option to specify a pem file instead. You can also add the private key file:

Another way to add private key files without using ssh-agent is using ansible_ssh_private_key_file in an inventory file as explained here: How to build your inventory.

You can run commands against the control node by using “localhost” or “127.0.0.1” for the server name:

You can specify localhost explicitly by adding this to your inventory file:

Ansible enables host key checking by default. Checking host keys guards against server spoofing and man-in-the-middle attacks, but it does require some maintenance.

If a host is reinstalled and has a different key in ‘known_hosts’, this will result in an error message until corrected. If a new host is not in ‘known_hosts’ your control node may prompt for confirmation of the key, which results in an interactive experience if using Ansible, from say, cron. You might not want this.

If you understand the implications and wish to disable this behavior, you can do so by editing /etc/ansible/ansible.cfg or ~/.ansible.cfg:

Alternatively, this can be set by the ANSIBLE_HOST_KEY_CHECKING environment variable:

Also note that host key checking in paramiko mode is reasonably slow, therefore switching to ‘ssh’ is also recommended when using this feature.

Ansible can use a variety of connection methods beyond SSH. You can select any connection plugin, including managing things locally and managing chroot, lxc, and jail containers. A mode called ‘ansible-pull’ can also invert the system and have systems ‘phone home’ with scheduled Git checkouts to pull configuration directives from a central repository.

**Examples:**

Example 1 (unknown):
```unknown
---
- name: update webservers
  hosts: webservers
  remote_user: admin

  tasks:
  - name: thing to do first in this playbook

  # ...
```

Example 2 (unknown):
```unknown
other1.example.com     ansible_connection=ssh        ansible_user=myuser
other2.example.com     ansible_connection=ssh        ansible_user=myotheruser
```

Example 3 (unknown):
```unknown
cloud:
  hosts:
    cloud1: my_backup.cloud.com
    cloud2: my_backup2.cloud.com
  vars:
    ansible_user: admin
```

Example 4 (unknown):
```unknown
$ ssh-agent bash
$ ssh-add ~/.ssh/id_rsa
```

---

## Index of all Inventory Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_inventory.html

**Contents:**
- Index of all Inventory Plugins
- ansible.builtin

ansible.builtin.advanced_host_list – Parses a ‘host list’ with ranges

ansible.builtin.auto – Loads and executes an inventory plugin specified in a YAML config

ansible.builtin.constructed – Uses Jinja2 to construct vars and groups based on existing inventory.

ansible.builtin.generator – Uses Jinja2 to construct hosts and groups from patterns

ansible.builtin.host_list – Parses a ‘host list’ string

ansible.builtin.ini – Uses an Ansible INI file as inventory source.

ansible.builtin.script – Executes an inventory script that returns JSON

ansible.builtin.toml – Uses a specific TOML file as an inventory source.

ansible.builtin.yaml – Uses a specific YAML file as an inventory source.

---
