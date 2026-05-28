# Ansible-Core - Modules

**Pages:** 52

---

## Index of all Shell Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_shell.html

**Contents:**
- Index of all Shell Plugins
- ansible.builtin

ansible.builtin.cmd – Windows Command Prompt

ansible.builtin.powershell – Windows PowerShell

ansible.builtin.sh – POSIX shell (/bin/sh)

---

## Developing plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_plugins.html

**Contents:**
- Developing plugins
- Writing plugins in Python
- Raising errors
- String encoding
- Plugin configuration & documentation standards
  - General precedence rules
  - Accessing configuration settings
- Developing particular plugin types
  - Action plugins
  - Cache plugins

Writing plugins in Python

Plugin configuration & documentation standards

General precedence rules

Accessing configuration settings

Developing particular plugin types

Plugins augment Ansible’s core functionality with logic and features that are accessible to all modules. Ansible collections include a number of handy plugins, and you can easily write your own. All plugins must:

return strings in unicode

conform to Ansible’s configuration and documentation standards

Once you’ve reviewed these general guidelines, you can skip to the particular type of plugin you want to develop.

You must write your plugin in Python so it can be loaded by the PluginLoader and returned as a Python object that any module can use. Since your plugin will execute on the control node, you must write it in a compatible version of Python.

You should return errors encountered during plugin execution by raising AnsibleError() or a similar class with a message describing the error. When wrapping other exceptions into error messages, you should always use the to_native Ansible function to ensure proper string compatibility across Python versions:

Since Ansible evaluates variables only when they are needed, filter and test plugins should propagate the exceptions jinja2.exceptions.UndefinedError and AnsibleUndefinedVariable to ensure undefined variables are only fatal when necessary.

Check the different AnsibleError objects and see which one applies best to your situation. Check the section on the specific plugin type you’re developing for type-specific error handling details.

You must convert any strings returned by your plugin into Python’s unicode type. Converting to unicode ensures that these strings can run through Jinja2. To convert strings:

To define configurable options for your plugin, describe them in the DOCUMENTATION section of the python file. Callback and connection plugins have declared configuration requirements this way since Ansible version 2.4; most plugin types now do the same. This approach ensures that the documentation of your plugin’s options will always be correct and up-to-date. To add a configurable option to your plugin, define it in this format:

The supported configuration fields are:

List of environment variables that can be used to set this option. Each entry includes a name field specifying the environment variable name. The name should be in uppercase and should be prefixed with the collection name. Multiple environment variables can be listed for the same option. The last set environment variable in the list takes precedence if multiple are set. This is commonly used for plugins (especially inventory plugins) to allow configuration through environment variables. Examples: VMWARE_PORT, GRAFANA_PASSWORD

List of configuration file settings that can be used to set this option. Each entry includes a section field for the configuration file section and a key field for the configuration key. Both should be in lowercase and should be prefixed with the collection name. Multiple configuration settings can be listed for the same option. The last set configuration setting in the list takes precedence if multiple are set. This allows plugins to be configured with ansible.cfg. Example: grafana_password

List of Ansible variables that can be used to set this option. Each entry includes a name field specifying the variable name. The name should be in lowercase and should be prefixed with the collection name. Multiple variables can be listed for the same option. The last set variable in the list takes precedence if multiple are set. Variables follow Ansible’s variable precedence rules. This allows plugins to be configured with Ansible variables. Example: ansible_vmware_port

The precedence rules for configuration sources are listed below, starting with the highest precedence values:

Environment variables (env)

Values defined in ansible.cfg

Default value for the option, if present.

To access the configuration settings in your plugin, use self.get_option(<option_name>). Some plugin types handle this differently:

Become, callback, connection and shell plugins are guaranteed to have the engine call set_options().

Lookup plugins always require you to handle it in the run() method.

Inventory plugins are done automatically if you use the base _read_config_file() method. If not, you must use self.get_option(<option_name>).

Cache plugins do it on load.

Cliconf, httpapi and netconf plugins indirectly piggy back on connection plugins.

Vars plugin settings are populated when first accessed (using the self.get_option() or self.get_options() method.

If you need to populate settings explicitly, use a self.set_options() call.

Configuration sources follow the precedence rules for values in Ansible. When there are multiple values from the same category, the value defined last takes precedence. For example, in the above configuration block, if both name_of_ansible_var and name_of_second_var are defined, the value of the option_name option will be the value of name_of_second_var. Refer to Controlling how Ansible behaves: precedence rules for further information.

Plugins that support embedded documentation (see ansible-doc for the list) should include well-formed doc strings. If you inherit from a plugin, you must document the options it takes, either through a documentation fragment or as a copy. See Module format and documentation for more information on correct documentation. Thorough documentation is a good idea even if you’re developing a plugin for local use.

Define a Python file that includes inline documentation for each plugin.

Define a Python file for multiple plugins and create adjacent documentation files in YAML format.

Action plugins let you integrate local processing and local data with module functionality.

To create an action plugin, create a new class with the Base(ActionBase) class as the parent:

From there, execute the module using the _execute_module method to call the original module. After successful execution of the module, you can modify the module return data.

For example, if you wanted to check the time difference between your Ansible control node and your target machine(s), you could write an action plugin to check the local time and compare it to the return data from Ansible’s setup module:

This code checks the time on the control node, captures the date and time for the remote machine using the setup module, and calculates the difference between the captured time and the local time, returning the time delta in days, seconds and microseconds.

For practical examples of action plugins, see the source code for the action plugins included with Ansible Core

Cache plugins store gathered facts and data retrieved by inventory plugins.

Import cache plugins using the cache_loader so you can use self.set_options() and self.get_option(<option_name>). If you import a cache plugin directly in the code base, you can only access options by the ansible.constants, and you break the cache plugin’s ability to be used by an inventory plugin.

There are two base classes for cache plugins, BaseCacheModule for database-backed caches, and BaseCacheFileModule for file-backed caches.

To create a cache plugin, start by creating a new CacheModule class with the appropriate base class. If you’re creating a plugin using an __init__ method you should initialize the base class with any provided args and kwargs to be compatible with inventory plugin cache options. The base class calls self.set_options(direct=kwargs). After the base class __init__ method is called self.get_option(<option_name>) should be used to access cache options.

New cache plugins should take the options _uri, _prefix, and _timeout to be consistent with existing cache plugins.

If you use the BaseCacheModule, you must implement the methods get, contains, keys, set, delete, flush, and copy. The contains method should return a boolean that indicates if the key exists and has not expired. Unlike file-based caches, the get method does not raise a KeyError if the cache has expired.

If you use the BaseFileCacheModule, you must implement _load and _dump methods that will be called from the base class methods get and set.

If your cache plugin stores JSON, use AnsibleJSONEncoder in the _dump or set method and AnsibleJSONDecoder in the _load or get method.

For example cache plugins, see the source code for the cache plugins included with Ansible Core.

Callback plugins add new behaviors to Ansible when responding to events. By default, callback plugins control most of the output you see when running the command line programs.

To create a callback plugin, create a new class with the Base(Callbacks) class as the parent:

From there, override the specific methods from the CallbackBase that you want to provide a callback for. For plugins intended for use with Ansible version 2.0 and later, you should only override methods that start with v2. For a complete list of methods that you can override, please see __init__.py in the lib/ansible/plugins/callback directory.

The following is a modified example of how Ansible’s timer plugin is implemented, but with an extra option so you can see how configuration works in Ansible version 2.4 and later:

Note that the CALLBACK_VERSION and CALLBACK_NAME definitions are required for properly functioning plugins for Ansible version 2.0 and later. CALLBACK_TYPE is mostly needed to distinguish ‘stdout’ plugins from the rest, since you can only load one plugin that writes to stdout.

For example callback plugins, see the source code for the callback plugins included with Ansible Core

New in ansible-core 2.11, callback plugins are notified (by the v2_playbook_on_task_start) of meta tasks. By default, only explicit meta tasks that users list in their plays are sent to callbacks.

There are also some tasks which are generated internally and implicitly at various points in execution. Callback plugins can opt-in to receiving these implicit tasks as well, by setting self.wants_implicit_tasks = True. Any Task object received by a callback hook will have an .implicit attribute, which can be consulted to determine whether the Task originated from within Ansible, or explicitly by the user.

Connection plugins allow Ansible to connect to target hosts so it can execute tasks on them. Ansible ships with many connection plugins, but only one can be used per host at a time. The most commonly used connection plugins are native ssh, paramiko, and local. All of these can be used with ad-hoc tasks and in playbooks.

To create a new connection plugin (for example, to support SNMP, Message bus, or other transports), copy the format of one of the existing connection plugins and drop it into connection directory on your local plugin path.

Connection plugins can support common options (such as the --timeout flag) by defining an entry in the documentation for the attribute name (in this case timeout). If the common option has a non-null default, the plugin should define the same default since a different default would be ignored.

For example connection plugins, see the source code for the connection plugins included with Ansible Core.

Filter plugins manipulate data. They are a feature of Jinja2 and are also available in Jinja2 templates used by the template module. As with all plugins, they can be easily extended, but instead of having a file for each one you can have several per file. Most of the filter plugins shipped with Ansible reside in a core.py.

Filter plugins do not use the standard configuration system described above, but since ansible-core 2.14 can use it as plain documentation.

Since Ansible evaluates variables only when they are needed, filter plugins should propagate the exceptions jinja2.exceptions.UndefinedError and AnsibleUndefinedVariable to ensure undefined variables are only fatal when necessary.

For example filter plugins, see the source code for the filter plugins included with Ansible Core.

Inventory plugins parse inventory sources and form an in-memory representation of the inventory. Inventory plugins were added in Ansible version 2.4.

You can see the details for inventory plugins in the Developing dynamic inventory page.

Lookup plugins pull in data from external data stores. Lookup plugins can be used within playbooks both for looping — playbook language constructs like with_fileglob and with_items are implemented through lookup plugins — and to return values into a variable or parameter.

Lookup plugins are expected to return lists, even if just a single element.

Ansible includes many filters which can be used to manipulate the data returned by a lookup plugin. Sometimes it makes sense to do the filtering inside the lookup plugin, other times it is better to return results that can be filtered in the playbook. Keep in mind how the data will be referenced when determining the appropriate level of filtering to be done inside the lookup plugin.

Here’s a simple lookup plugin implementation — this lookup returns the contents of a text file as a variable:

The following is an example of how this lookup is called:

For example lookup plugins, see the source code for the lookup plugins included with Ansible Core.

For more usage examples of lookup plugins, see Using Lookups.

Test plugins verify data. They are a feature of Jinja2 and are also available in Jinja2 templates used by the template module. As with all plugins, they can be easily extended, but instead of having a file for each one you can have several per file. Most of the test plugins shipped with Ansible reside in a core.py. These are specially useful in conjunction with some filter plugins like map and select; they are also available for conditional directives like when:.

Test plugins do not use the standard configuration system described above. Since ansible-core 2.14 test plugins can use plain documentation.

Since Ansible evaluates variables only when they are needed, test plugins should propagate the exceptions jinja2.exceptions.UndefinedError and AnsibleUndefinedVariable to ensure undefined variables are only fatal when necessary.

For example test plugins, see the source code for the test plugins included with Ansible Core.

Vars plugins inject additional variable data into Ansible runs that did not come from an inventory source, playbook, or command line. Playbook constructs like ‘host_vars’ and ‘group_vars’ work using vars plugins.

Vars plugins were partially implemented in Ansible 2.0 and rewritten to be fully implemented starting with Ansible 2.4. Vars plugins are supported by collections starting with Ansible 2.10.

Older plugins used a run method as their main body/work:

Ansible 2.0 did not pass passwords to older plugins, so vaults were unavailable. Most of the work now happens in the get_vars method which is called from the VariableManager when needed.

loader: Ansible’s DataLoader. The DataLoader can read files, auto-load JSON/YAML and decrypt vaulted data, and cache read files.

path: this is ‘directory data’ for every inventory source and the current play’s playbook directory, so they can search for data in reference to them. get_vars will be called at least once per available path.

entities: these are host or group names that are pertinent to the variables needed. The plugin will get called once for hosts and again for groups.

This get_vars method just needs to return a dictionary structure with the variables.

Since Ansible version 2.4, vars plugins only execute as needed when preparing to execute a task. This avoids the costly ‘always execute’ behavior that occurred during inventory construction in older versions of Ansible. Since Ansible version 2.10, vars plugin execution can be toggled by the user to run when preparing to execute a task or after importing an inventory source.

The user must explicitly enable vars plugins that reside in a collection. See Enabling vars plugins for details.

Legacy vars plugins are always loaded and run by default. You can prevent them from automatically running by setting REQUIRES_ENABLED to True.

Include the vars_plugin_staging documentation fragment to allow users to determine when vars plugins run.

At times a value provided by a vars plugin will contain unsafe values. The utility function wrap_var provided by ansible.utils.unsafe_proxy should be used to ensure that Ansible handles the variable and value correctly. The use cases for unsafe data is covered in Unsafe or raw strings.

For example vars plugins, see the source code for the vars plugins included with Ansible Core.

Browse existing collections, modules, and plugins

Learn about the Python API for task execution

Learn about how to develop dynamic inventory sources

Learn about how to write Ansible modules

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

Alternate YAML files as documentation

**Examples:**

Example 1 (python):
```python
from ansible.module_utils.common.text.converters import to_native

try:
    cause_an_exception()
except Exception as e:
    raise AnsibleError('Something happened, this was original exception: %s' % to_native(e))
```

Example 2 (python):
```python
from ansible.module_utils.common.text.converters import to_text
result_string = to_text(result_string)
```

Example 3 (unknown):
```unknown
options:
  option_name:
    description: describe this config option
    default: default value for this config option
    env:
      - name: MYCOLLECTION_NAME_ENV_VAR_NAME
    ini:
      - section: mycollection_section_of_ansible.cfg_where_this_config_option_is_defined
        key: key_used_in_ansible.cfg
    vars:
      - name: mycollection_name_of_ansible_var
      - name: mycollection_name_of_second_var
        version_added: X.x
    required: True/False
    type: boolean/float/integer/list/none/path/pathlist/pathspec/string/tmppath
    version_added: X.x
```

Example 4 (python):
```python
from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):
    pass
```

---

## Debugging modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/debugging.html

**Contents:**
- Debugging modules
- Detailed debugging steps
- Simple debugging

Detailed debugging steps

Ansible modules are put together as a zip file consisting of the module file and the various Python module boilerplate inside of a wrapper script. To see what is actually happening in the module, you need to extract the file from the wrapper. The wrapper script provides helper methods that let you do that.

The following steps use localhost as the target host, but you can use the same steps to debug against remote hosts as well. For a simpler approach to debugging without using the temporary files, see simple debugging.

Set ANSIBLE_KEEP_REMOTE_FILES to 1 on the control host so Ansible will keep the remote module files instead of deleting them after the module finishes executing. Use the -vvv option to make Ansible more verbose. This will display the file name of the temporary module file.

Navigate to the temporary directory from the previous step. If the previous command was run against a remote host, connect to that host first before trying to navigate to the temporary directory.

Run the wrapper’s explode command to turn the string into some Python files that you can work with.

If you want to examine the wrapper file you can. It will show a small Python script with a large base64 encoded string. The string contains the module to execute.

When you look into the temporary directory you’ll see a structure like this:

AnsiballZ_ping.py is the Python script with the module code stored in a base64 encoded string. It contains various helper functions for executing the module.

ping.py is the code for the module itself. You can modify this code to see what effect it would have on your module, or for debugging purposes.

The args file contains a JSON string. The string is a dictionary containing the module arguments and other variables that Ansible passes into the module to change its behavior. Modify this file to change the parameters passed to the module.

The ansible directory contains the module code in modules as well as code from ansible.module_utils that is used by the module. Ansible includes files for any ansible.module_utils imports in the module but not any files from any other module. If your module uses ansible.module_utils.url Ansible will include it for you. But if your module includes requests, then you’ll have to make sure that the Python requests library is installed on the system before running the module.

You can modify files in this directory if you suspect that the module is having a problem in some of this boilerplate code rather than in the module code you have written.

Once you edit the code or arguments in the exploded tree, use the execute subcommand to run it:

This subcommand inserts the absolute path to debug_dir as the first item in sys.path and invokes the script using the arguments in the args file. You can continue to run the module like this until you understand the problem. Then you can copy the changes back into your real module file and test that the real module works by using the ansible or ansible-playbook.

The easiest way to run a debugger in a module, either local or remote, is to use madbg. Add import madbg; madbg.set_trace() in the module code on the control node at the desired break point. To connect to the debugger, run madbg connect. See the madbg documentation for how to specify the host and port. If connecting to a remote node, make sure to use a port that is allowed by any firewall between the control node and the remote node.

This technique should work with any remote debugger, but we do not guarantee any particular remote debugging tool will work.

The q library is another very useful debugging tool.

Since print() statements do not work inside modules, raising an exception is a good approach if you just want to see some specific data. Put raise Exception(some_value) somewhere in the module and run it normally. Ansible will handle this exception, pass the message back to the control node, and display it.

**Examples:**

Example 1 (javascript):
```javascript
$ ANSIBLE_KEEP_REMOTE_FILES=1 ansible localhost -m ping -a 'data=debugging_session' -vvv
<127.0.0.1> ESTABLISH LOCAL CONNECTION FOR USER: badger
<127.0.0.1> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo $HOME/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595 `" && echo "` echo $HOME/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595 `" )'
<127.0.0.1> PUT /var/tmp/tmpjdbJ1w TO /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/AnsiballZ_ping.py
<127.0.0.1> EXEC /bin/sh -c 'LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LC_MESSAGES=en_US.UTF-8 /usr/bin/python /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/AnsiballZ_ping.py && sleep 0'
localhost | SUCCESS => {
    "changed": false,
    "invocation": {
        "module_args": {
            "data": "debugging_session"
        },
        "module_name": "ping"
    },
    "ping": "debugging_session"
}
```

Example 2 (unknown):
```unknown
$ ssh remotehost  # only if not debugging against localhost
$ cd /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595
```

Example 3 (unknown):
```unknown
$ python AnsiballZ_ping.py explode
Module expanded into:
/home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/debug_dir
```

Example 4 (unknown):
```unknown
├── AnsiballZ_ping.py
└── debug_dir
    ├── ansible
    │   ├── __init__.py
    │   ├── module_utils
    │   │   ├── __init__.py
    │   │   ├── _text.py
    │   │   ├── basic.py
    │   │   ├── common
    │   │   ├── compat
    │   │   ├── distro
    │   │   ├── parsing
    │   │   ├── pycompat24.py
    │   │   └── six
    │   └── modules
    │       ├── __init__.py
    │       └── ping.py
    └── args
```

---

## Conventions, tips, and pitfalls — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_best_practices.html

**Contents:**
- Conventions, tips, and pitfalls
- Scoping your module(s)
- Designing module interfaces
- General guidelines & tips
- Functions and Methods
- Python tips
- Importing and using shared code
- Handling module failures
- Handling exceptions (bugs) gracefully
- Creating correct and informative module output

Scoping your module(s)

Designing module interfaces

General guidelines & tips

Functions and Methods

Importing and using shared code

Handling module failures

Handling exceptions (bugs) gracefully

Creating correct and informative module output

Following Ansible conventions

As you design and develop modules, follow these basic conventions and tips for clean, usable code:

Especially if you want to contribute your module(s) to an existing Ansible Collection, make sure each module includes enough logic and functionality, but not too much. If these guidelines seem confusing, consider whether you really need to write a module at all.

Each module should have a concise and well-defined functionality. Basically, follow the UNIX philosophy of doing one thing well.

Do not add get, list or info state options to an existing module - create a new _info or _facts module.

Modules should not require that a user know all the underlying options of an API/tool to be used. For example, if the legal values for a required module option cannot be documented, the module does not belong in Ansible Core.

Modules should encompass much of the logic for interacting with a resource. A lightweight wrapper around a complex API forces users to offload too much logic into their playbooks. If you want to connect Ansible to a complex API, create multiple modules that interact with smaller individual pieces of the API.

Avoid creating a module that does the work of other modules; this leads to code duplication and divergence, and makes things less uniform, unpredictable and harder to maintain. Modules should be the building blocks. If you are asking ‘how can I have a module execute other modules’ … you want to write a role.

If your module is addressing an object, the option for that object should be called name whenever possible, or accept name as an alias.

Modules accepting boolean status should accept yes, no, true, false, or anything else a user may likely throw at them. The AnsibleModule common code supports this with type='bool'.

Avoid action/command, they are imperative and not declarative, there are other ways to express the same thing.

Each module should be self-contained in one file, so it can be auto-transferred by ansible-core.

Module name MUST use underscores instead of hyphens or spaces as a word separator. Using hyphens and spaces will prevent ansible-core from importing your module.

Always use the hacking/test-module.py script when developing modules - it will warn you about common pitfalls.

If you have a local module that returns information specific to your installations, a good name for this module is site_info.

Eliminate or minimize dependencies. If your module has dependencies, document them at the top of the module file and raise JSON error messages when dependency import fails.

Don’t write to files directly; use a temporary file and then use the atomic_move function from ansible.module_utils.basic to move the updated temporary file into place. This prevents data corruption and ensures that the correct context for the file is kept.

Avoid creating caches. Ansible is designed without a central server or authority, so you cannot guarantee it will not run with different permissions, options or locations. If you need a central authority, have it on top of Ansible (for example, using bastion/cm/ci server, AWX, or the Red Hat Ansible Automation Platform); do not try to build it into modules.

If you package your module(s) in an RPM, install the modules on the control machine in /usr/share/ansible. Packaging modules in RPMs is optional.

Each function should be concise and should describe a meaningful amount of work.

“Don’t repeat yourself” is generally a good philosophy.

Function names should use underscores: my_function_name.

The name of each function should describe what the function does.

Each function should have a docstring.

If your code is too nested, that’s usually a sign the loop body could benefit from being a function. Parts of our existing code are not the best examples of this at times.

Include a main function that wraps the normal execution.

Call your main function from a conditional so you can import it into unit tests - for example:

Use shared code whenever possible - don’t reinvent the wheel. Ansible offers the AnsibleModule common Python code, plus utilities for many common use cases and patterns. You can also create documentation fragments for docs that apply to multiple modules.

Import ansible.module_utils code in the same place as you import other libraries.

Do NOT use wildcards (*) for importing other python modules; instead, list the function(s) you are importing (for example, from some.other_python_module.basic import otherFunction).

Import custom packages in try/except, capture any import errors, and handle them with fail_json() in main(). For example:

Then in main(), just after the argspec, do

And document the dependency in the requirements section of your module’s DOCUMENTATION block.

When your module fails, help users understand what went wrong. If you are using the AnsibleModule common Python code, the failed element will be included for you automatically when you call fail_json. For polite module failure behavior:

Include a key of failed along with a string explanation in msg. If you don’t do this, Ansible will use standard return codes: 0=success and non-zero=failure.

Don’t raise a traceback (stacktrace). Ansible can deal with stacktraces and automatically converts anything unparsable into a failed result, but raising a stacktrace on module failure is not user-friendly.

Do not use sys.exit(). Use fail_json() from the module object.

Validate upfront–fail fast and return useful and clear error messages.

Use defensive programming–use a simple design for your module, handle errors gracefully, and avoid direct stacktraces.

Fail predictably–if we must fail, do it in a way that is the most expected. Either mimic the underlying tool or the general way the system works.

Give out a useful message on what you were doing and add exception messages to that.

Avoid catchall exceptions, they are not very useful unless the underlying API gives very good error messages pertaining the attempted action.

Modules must output valid JSON only. Follow these guidelines for creating correct, useful module output:

Module return data must be encoded as strict UTF-8. Modules that cannot return UTF-8 encoded data should return the data encoded by something such as base64. Optionally modules can make the determination if they can encode as UTF-8 and utilize errors='replace' to replace non UTF-8 characters making the return values lossy.

Make your top-level return type a hash (dictionary).

Nest complex return values within the top-level hash.

Incorporate any lists or simple scalar values within the top-level return hash.

Do not send module output to standard error, because the system will merge standard out with standard error and prevent the JSON from parsing.

Capture standard error and return it as a variable in the JSON on standard out. This is how the command module is implemented.

Never do print("some status message") in a module, because it will not produce valid JSON output.

Always return useful data, even when there is no change.

Be consistent about returns (some modules are too random), unless it is detrimental to the state/action.

Make returns reusable–most of the time you don’t want to read it, but you do want to process it and re-purpose it.

Return diff if in diff mode. This is not required for all modules, as it won’t make sense for certain ones, but please include it when applicable.

Enable your return values to be serialized as JSON with Python’s standard JSON encoder and decoder library. Basic python types (strings, int, dicts, lists, and so on) are serializable.

Do not return an object using exit_json(). Instead, convert the fields you need from the object into the fields of a dictionary and return the dictionary.

Results from many hosts will be aggregated at once, so your module should return only relevant output. Returning the entire contents of a log file is generally bad form.

If a module returns stderr or otherwise fails to produce valid JSON, the actual output will still be shown in Ansible, but the command will not succeed.

Ansible conventions offer a predictable user interface across all modules, playbooks, and roles. To follow Ansible conventions in your module development:

Use consistent names across modules (yes, we have many legacy deviations - don’t make the problem worse!).

Use consistent options (arguments) within your module(s).

Do not use ‘message’ or ‘syslog_facility’ as an option name, because this is used internally by Ansible.

Normalize options with other modules - if Ansible and the API your module connects to use different names for the same option, add aliases to your options so the user can choose which names to use in tasks and playbooks.

Return facts from *_facts modules in the ansible_facts field of the result dictionary so other modules can access them.

Implement check_mode in all *_info and *_facts modules. Playbooks which conditionalize based on fact information will only conditionalize correctly in check_mode if the facts are returned in check_mode. Usually you can add supports_check_mode=True when instantiating AnsibleModule.

Use module-specific environment variables. For example, if you use the helpers in module_utils.api for basic authentication with module_utils.urls.fetch_url() and you fall back on environment variables for default values, use a module-specific environment variable like API_<MODULENAME>_USERNAME to avoid conflicts between modules.

Keep module options simple and focused - if you’re loading a lot of choices/states on an existing option, consider adding a new, simple option instead.

Keep options small when possible. Passing a large data structure to an option might save us a few tasks, but it adds a complex requirement that we cannot easily validate before passing on to the module.

If you want to pass complex data to an option, write an expert module that allows this, along with several smaller modules that provide a more ‘atomic’ operation against the underlying APIs and services. Complex operations require complex data. Let the user choose whether to reflect that complexity in tasks and plays or in vars files.

Implement declarative operations (not CRUD) so the user can ignore existing state and focus on final state. For example, use started/stopped, present/absent.

Strive for a consistent final state (aka idempotency). If running your module twice in a row against the same system would result in two different states, see if you can redesign or rewrite to achieve consistent final state. If you can’t, document the behavior and the reasons for it.

Provide consistent return values within the standard Ansible return structure, even if NA/None are used for keys normally returned under other options.

Avoid passing user input from the shell.

Always check return codes.

You must always use module.run_command, not subprocess or Popen or os.system.

Avoid using the shell unless absolutely necessary.

If you must use the shell, you must pass use_unsafe_shell=True to module.run_command.

If any variables in your module can come from user input with use_unsafe_shell=True, you must wrap them with pipes.quote(x).

When fetching URLs, use fetch_url or open_url from ansible.module_utils.urls. Do not use urllib2, which does not natively verify TLS certificates and so is insecure for https.

Sensitive values marked with no_log=True will automatically have that value stripped from module return values. If your module could return these sensitive values as part of a dictionary key name, you should call the ansible.module_utils.basic.sanitize_keys() function to strip the values from the keys. See the uri module for an example.

**Examples:**

Example 1 (unknown):
```unknown
if __name__ == '__main__':
    main()
```

Example 2 (python):
```python
import traceback

from ansible.module_utils.basic import missing_required_lib

LIB_IMP_ERR = None
try:
    import foo
    HAS_LIB = True
except:
    HAS_LIB = False
    LIB_IMP_ERR = traceback.format_exc()
```

Example 3 (unknown):
```unknown
if not HAS_LIB:
    module.fail_json(msg=missing_required_lib("foo"),
                     exception=LIB_IMP_ERR)
```

---

## Become plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/become.html

**Contents:**
- Become plugins
- Enabling Become Plugins
- Using Become Plugins
- Plugin List

Enabling Become Plugins

Become plugins work to ensure that Ansible can use certain privilege escalation systems when running the basic commands to work with the target machine as well as the modules required to execute the tasks specified in the play.

These utilities (sudo, su, doas, and so on) generally let you ‘become’ another user to execute a command with the permissions of that user.

The become plugins shipped with Ansible are already enabled. Custom plugins can be added by placing them into a become_plugins directory adjacent to your play, inside a role, or by placing them in one of the become plugin directory sources configured in ansible.cfg.

In addition to the default configuration settings in Ansible Configuration Settings or the --become-method command line option, you can use the become_method keyword in a play or, if you need to be ‘host specific’, the connection variable ansible_become_method to select the plugin to use.

You can further control the settings for each plugin with other configuration options detailed in the plugin themselves (linked below).

You can use ansible-doc -t become -l to see the list of available plugins. Use ansible-doc -t become <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Modules and plugins index — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/module_plugin_guide/modules_plugins_index.html

**Contents:**
- Modules and plugins index

You can find an index of modules and plugins at Indexes of all modules and plugins.

---

## Action plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/action.html

**Contents:**
- Action plugins
- Enabling action plugins
- Using action plugins
- Plugin list

Enabling action plugins

Action plugins act in conjunction with modules to execute the actions required by playbook tasks. They usually execute automatically in the background doing prerequisite work before modules execute.

The ‘normal’ action plugin is used for modules that do not already have an action plugin. If necessary, you can create custom action plugins.

You can enable a custom action plugin by either dropping it into the action_plugins directory adjacent to your play, inside a role, or by putting it in one of the action plugin directory sources configured in ansible.cfg.

Action plugins are executed by default when an associated module is used; no additional action is required.

You cannot list action plugins directly, they show up as their counterpart modules:

Use ansible-doc -l to see the list of available modules. Use ansible-doc <name> to see plugin-specific documentation and examples. This should note if the module has a corresponding action plugin.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Strategy plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/strategy.html

**Contents:**
- Strategy plugins
- Enabling strategy plugins
- Using strategy plugins
- Plugin list

Enabling strategy plugins

Using strategy plugins

Strategy plugins control the flow of play execution by handling task and host scheduling. For more information on using strategy plugins and other ways to control execution order, see Controlling playbook execution: strategies and more.

All strategy plugins shipped with Ansible are enabled by default. You can enable a custom strategy plugin by putting it in one of the lookup directory sources configured in ansible.cfg.

Only one strategy plugin can be used in a play, but you can use different ones for each play in a playbook or ansible run. By default, Ansible uses the linear plugin. You can change this default in Ansible configuration using an environment variable:

or in the ansible.cfg file:

You can also specify the strategy plugin in the play with the strategy keyword in a play:

You can use ansible-doc -t strategy -l to see the list of available plugins. Use ansible-doc -t strategy <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
export ANSIBLE_STRATEGY=free
```

Example 2 (unknown):
```unknown
[defaults]
strategy=linear
```

Example 3 (unknown):
```unknown
- hosts: all
  strategy: debug
  tasks:
    - copy:
        src: myhosts
        dest: /etc/hosts
      notify: restart_tomcat

    - package:
        name: tomcat
        state: present

  handlers:
    - name: restart_tomcat
      service:
        name: tomcat
        state: restarted
```

---

## Should you develop a module? — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules.html

**Contents:**
- Should you develop a module?

Developing Ansible modules is easy, but often it is not necessary. Before you start writing a new module, ask:

Does a similar module already exist?

An existing module may cover the functionality you want. Ansible collections include thousands of modules. Search our list of included collections or Ansible Galaxy to see if an existing module does what you need.

Should you use or develop an action plugin instead of a module?

An action plugin may be the best way to get the functionality you want. Action plugins run on the control node instead of on the managed node, and their functionality is available to all modules. For more information about developing plugins, read the developing plugins page.

Should you use a role instead of a module?

A combination of existing modules may cover the functionality you want. You can write a role for this type of use case. Check out the roles documentation.

Should you create a collection instead of a single module?

The functionality you want may be too large for a single module. If you want to connect Ansible to a new cloud provider, database, or network platform, you may need to develop a new collection.

Each module should have a concise and well defined functionality. Basically, follow the UNIX philosophy of doing one thing well.

A module should not require that a user know all the underlying options of an API/tool to be used. For example, if the legal values for a required module parameter cannot be documented, that’s a sign that the module would be rejected.

Modules should typically encompass much of the logic for interacting with a resource. A lightweight wrapper around an API that does not contain much logic would likely cause users to offload too much logic into a playbook, and for this reason the module would be rejected. Instead try creating multiple modules for interacting with smaller individual pieces of the API.

If your use case isn’t covered by an existing module, an action plugin, or a role, and you don’t need to create multiple modules, then you’re ready to start developing a new module. Choose from the topics below for next steps:

I want to get started on a new module.

I want to review tips and conventions for developing good modules.

I want to write a Windows module.

I want an overview of Ansible’s architecture.

I want to document my module.

I want to contribute my module to an existing Ansible collection.

I want to add unit and integration tests to my module.

I want to add Python 3 support to my module.

I want to write multiple modules.

Browse existing collections, modules, and plugins

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Index of all Stdout Callback Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/callback_index_stdout.html

**Contents:**
- Index of all Stdout Callback Plugins
- ansible.builtin

See Index of all Callback Plugins for the list of all callback plugins.

ansible.builtin.default – default Ansible screen output

ansible.builtin.minimal – minimal Ansible screen output

ansible.builtin.oneline – oneline Ansible screen output

---

## Ansible markup — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/ansible_markup.html

**Contents:**
- Ansible markup
- Semantic markup within module documentation
  - Rules for using O() and RV()
- Linking within module documentation
- Format macros within module documentation

Ansible markup allows you to format and structure documentation for Ansible modules, plugins, and roles. It lets you add basic formatting to text, such as bold, italics, code, and horizontal lines, as well as create various references, such as URLs, hyperlinks, Ansible module references, and RST references. The Ansible markup language was extended in 2023, starting with ansible-core 2.15. It now lets you apply semantic markup for values, module/plugin options, return values, environment variables, and for referencing plugins.

This page documents the currently supported Ansible markup.

Use the semantic markup to highlight option names, option values, and environment variables. The markup processor formats these highlighted terms in a uniform way. With semantic markup, we can modify how the output looks without changing underlying code.

The correct formats for semantic markup are as follows:

O() for option names, whether mentioned alone or with values. For example: Required if O(state=present). and Use with O(force) to require secure access.

V() for option values when mentioned alone. For example: Possible values include V(monospace) and V(pretty).

RV() for return value names, whether mentioned alone or with values. For example: The module returns RV(changed=true) in case of changes. and Use the RV(stdout) return value for standard output.

E() for environment variables. For example: If not set, the environment variable E(ACME_PASSWORD) will be used.

The parameters for these formatting functions can use escaping with backslashes: V(foo(bar="a\\b"\), baz) results in the formatted value foo(bar="a\b"), baz).

Rules for using O() and RV() are very strict. You must follow syntax rules so that documentation renderers can create hyperlinks for the options and return values, respectively.

The allowed syntaxes are as follows:

To reference an option for the current plugin/module, or the entrypoint of the current role (inside role entrypoint documentation), use O(option) and O(option=value).

To reference an option for another entrypoint entrypoint from inside role documentation, use O(entrypoint:option) and O(entrypoint:option=name). The entrypoint information can be ignored by the documentation renderer, turned into a link to that entrypoint, or even directly to the option of that entrypoint.

To reference an option for another plugin/module plugin.fqcn.name of type type, use O(plugin.fqcn.name#type:option) and O(plugin.fqcn.name#type:option=value). For modules, use type=module. The FQCN and plugin type can be ignored by the documentation renderer, turned into a link to that plugin, or even directly to the option of that plugin.

To reference an option for entrypoint entrypoint of another role role.fqcn.name, use O(role.fqcn.name#role:entrypoint:option) and O(role.fqcn.name#role:entrypoint:option=value). The FQCN and entrypoint information can be ignored by the documentation renderer, turned into a link to that entrypoint, or even directly to the option of that entrypoint.

To reference options that do not exist (for example, options that were removed in an earlier version), use O(ignore:option) and O(ignore:option=value). The ignore: part will not be shown to the user by documentation rendering.

Option names can refer to suboptions by listing the path to the option separated by dots. For example, if you have an option foo with suboption bar, then you must use O(foo.bar) to reference that suboption. You can add array indications like O(foo[].bar) or even O(foo[-1].bar) to indicate specific list elements. Everything between [ and ] pairs will be ignored to determine the real name of the option. For example, O(foo[foo | length - 1].bar[]) results in the same link as O(foo.bar), but the text foo[foo | length - 1].bar[] displays instead of foo.bar.

The same syntaxes can be used for RV(), except that these will refer to return value names instead of option names; for example RV(ansible.builtin.service_facts#module:ansible_facts.services) refers to the ansible_facts.services fact returned by the ansible.builtin.service_facts module.

You can link from your module documentation to other module docs, other resources on docs.ansible.com, and resources elsewhere on the internet with the help of some pre-defined macros. The correct formats for these macros are:

R() for cross-references with a heading (supported since Ansible 2.10). For example: See R(Cisco IOS Platform Guide,ios_platform_options). Use the RST anchor for the cross-reference. See Adding anchors for details.

For links outside of your collection, use R() if available. Otherwise, use U() or L() with full URLs (not relative links).

To refer to a group of modules in a collection, use R(). When a collection is not the right granularity, use C(..), for example:

Refer to the R(kubernetes.core collection, plugins_in_kubernetes.core) for information on managing kubernetes clusters.

The C(win_*) modules (spread across several collections) allow you to manage various aspects of windows hosts.

L() for links with a heading. For example: See L(Ansible Automation Platform,https://www.ansible.com/products/automation-platform). As of Ansible 2.10, do not use L() for relative links between Ansible documentation and collection documentation.

U() for URLs. For example: See U(https://www.ansible.com/products/automation-platform) for an overview.

M() for module names. For example: See also M(ansible.builtin.yum) or M(community.general.apt_rpm).

FQCNs MUST be used, short names will create broken links; use ansible.builtin for modules in ansible-core.

P() for plugin names (supported since ansible-core 2.15). For example: See also P(ansible.builtin.file#lookup) or P(community.general.json_query#filter).

This can also reference roles: P(community.sops.install#role).

FQCNs must be used, short names will create broken links; use ansible.builtin for plugins in ansible-core.

O() and RV() can also link, see the section on their syntax.

If you are creating your own documentation site, you will need to use the intersphinx extension to convert R(), M(), P(), O(), and RV() to the correct links.

While it is possible to use standard Ansible formatting macros to control the look of other terms in module documentation, you should do so sparingly.

Possible macros include the following:

C() for monospace (code) text. For example: This module functions like the unix command C(foo).

HORIZONTALLINE for a horizontal rule (the <hr> html tag) to separate long descriptions.

Note that C(), B(), and I() do not allow escaping, and thus cannot contain the value ) as it always ends the formatting sequence. If you need to use ) inside C(), we recommend to use V() instead; see the above section on semantic markup.

---

## Module maintenance and support — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/module_plugin_guide/modules_support.html

**Contents:**
- Module maintenance and support
- Maintenance
- Issue Reporting
- Support

If you are using a module and you discover a bug, you may want to know where to report that bug, who is responsible for fixing it, and how you can track changes to the module. If you are a Red Hat subscriber, you may want to know whether you can get support for the issue you are facing.

Starting in Ansible 2.10, most modules live in collections. The distribution method for each collection reflects the maintenance and support for the modules in that collection.

ansible/ansible repo on GitHub

distributed on Galaxy

various; follow repo link

community or partners

distributed on Automation Hub

various; follow repo link

content team or partners

If you find a bug that affects a plugin in the main Ansible repo, also known as ansible-core:

Confirm that you are running the latest stable version of Ansible or the devel branch.

Look at the issue tracker in the Ansible repo to see if an issue has already been filed.

Create an issue if one does not already exist. Include as much detail as you can about the behavior you discovered.

If you find a bug that affects a plugin in a Galaxy collection:

Find the collection on Galaxy.

Find the issue tracker for the collection.

Look there to see if an issue has already been filed.

Create an issue if one does not already exist. Include as much detail as you can about the behavior you discovered.

Some partner collections may be hosted in private repositories.

If you are not sure whether the behavior you see is a bug, if you have questions, if you want to discuss development-oriented topics, or if you just want to get in touch, visit the Ansible communication guide for information on how to join the community.

If you find a bug that affects a module in an Automation Hub collection:

If the collection offers an Issue Tracker link on Automation Hub, click there and open an issue on the collection repository. If it does not, follow the standard process for reporting issues on the Red Hat Customer Portal. You must have a subscription to the Red Hat Ansible Automation Platform to create an issue on the portal.

All plugins that remain in ansible-core and all collections hosted in Automation Hub are supported by Red Hat. No other plugins or collections are supported by Red Hat. If you have a subscription to the Red Hat Ansible Automation Platform, you can find more information and resources on the Red Hat Customer Portal.

Examples of using modules in /usr/bin/ansible

Examples of using modules with /usr/bin/ansible-playbook

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Netconf plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/netconf.html

**Contents:**
- Netconf plugins
- Adding netconf plugins
- Using netconf plugins
- Listing netconf plugins

Adding netconf plugins

Using netconf plugins

Listing netconf plugins

Netconf plugins are abstractions over the Netconf interface to network devices. They provide a standard interface for Ansible to execute tasks on those network devices.

These plugins generally correspond one-to-one to network device platforms. Ansible loads the appropriate netconf plugin automatically based on the ansible_network_os variable. If the platform supports standard Netconf implementation as defined in the Netconf RFC specification, Ansible loads the default netconf plugin. If the platform supports propriety Netconf RPCs, Ansible loads the platform-specific netconf plugin.

You can extend Ansible to support other network devices by dropping a custom plugin into the netconf_plugins directory.

The netconf plugin to use is determined automatically from the ansible_network_os variable. There should be no reason to override this functionality.

Most netconf plugins can operate without configuration. A few have additional options that can be set to affect how tasks are translated into netconf commands. A ncclient device-specific handler name can be set in the netconf plugin or else the value of default is used as per ncclient device handler.

Plugins are self-documenting. Each plugin should document its configuration options.

These plugins have migrated to collections on Ansible Galaxy. If you installed Ansible version 2.10 or later using pip, you have access to several netconf plugins. You can use ansible-doc -t netconf -l to see the list of available plugins. Use ansible-doc -t netconf <plugin name> to see plugin-specific documentation and examples.

An overview of using Ansible to automate networking devices.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Index of all Vars Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_vars.html

**Contents:**
- Index of all Vars Plugins
- ansible.builtin

ansible.builtin.host_group_vars – In charge of loading group_vars and host_vars

---

## Index of all Connection Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_connection.html

**Contents:**
- Index of all Connection Plugins
- ansible.builtin

ansible.builtin.local – execute on controller

ansible.builtin.paramiko_ssh – Run tasks via Python SSH (paramiko)

ansible.builtin.psrp – Run tasks over Microsoft PowerShell Remoting Protocol

ansible.builtin.ssh – connect via SSH client binary

ansible.builtin.winrm – Run tasks over Microsoft’s WinRM

---

## Module utilities — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/module_util.html

**Contents:**
- Module utilities
- Enabling module utilities
- Using module utilities

Enabling module utilities

Using module utilities

Module utilities contain shared code used by multiple plugins. You can write custom module utilities.

You can add a custom module utility by dropping it into a module_utils directory adjacent to your collection or role, just like any other plugin.

For information on using module utilities, see Using and developing module utilities.

An introduction to creating Ansible modules

A guide to creating Ansible collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Index of all Modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_module.html

**Contents:**
- Index of all Modules
- ansible.builtin

ansible.builtin.add_host – Add a host (and alternatively a group) to the ansible-playbook in-memory inventory

ansible.builtin.apt – Manages apt-packages

ansible.builtin.apt_key – Add or remove an apt key

ansible.builtin.apt_repository – Add and remove APT repositories

ansible.builtin.assemble – Assemble configuration files from fragments

ansible.builtin.assert – Asserts given expressions are true

ansible.builtin.async_status – Obtain status of asynchronous task

ansible.builtin.blockinfile – Insert/update/remove a text block surrounded by marker lines

ansible.builtin.command – Execute commands on targets

ansible.builtin.copy – Copy files to remote locations

ansible.builtin.cron – Manage cron.d and crontab entries

ansible.builtin.deb822_repository – Add and remove deb822 formatted repositories

ansible.builtin.debconf – Configure a .deb package

ansible.builtin.debug – Print statements during execution

ansible.builtin.dnf – Manages packages with the dnf package manager

ansible.builtin.dnf5 – Manages packages with the dnf5 package manager

ansible.builtin.dpkg_selections – Dpkg package selection selections

ansible.builtin.expect – Executes a command and responds to prompts

ansible.builtin.fail – Fail with custom message

ansible.builtin.fetch – Fetch files from remote nodes

ansible.builtin.file – Manage files and file properties

ansible.builtin.find – Return a list of files based on specific criteria

ansible.builtin.gather_facts – Gathers facts about remote hosts

ansible.builtin.get_url – Downloads files from HTTP, HTTPS, or FTP to node

ansible.builtin.getent – A wrapper to the unix getent utility

ansible.builtin.git – Deploy software (or files) from git checkouts

ansible.builtin.group – Add or remove groups

ansible.builtin.group_by – Create Ansible groups based on facts

ansible.builtin.hostname – Manage hostname

ansible.builtin.import_playbook – Import a playbook

ansible.builtin.import_role – Import a role into a play

ansible.builtin.import_tasks – Import a task list

ansible.builtin.include_role – Load and execute a role

ansible.builtin.include_tasks – Dynamically include a task list

ansible.builtin.include_vars – Load variables from files, dynamically within a task

ansible.builtin.iptables – Modify iptables rules

ansible.builtin.known_hosts – Add or remove a host from the known_hosts file

ansible.builtin.lineinfile – Manage lines in text files

ansible.builtin.meta – Execute Ansible ‘actions’

ansible.builtin.mount_facts – Retrieve mount information.

ansible.builtin.package – Generic OS package manager

ansible.builtin.package_facts – Package information as facts

ansible.builtin.pause – Pause playbook execution

ansible.builtin.ping – Try to connect to host, verify a usable python and return pong on success

ansible.builtin.pip – Manages Python library dependencies

ansible.builtin.raw – Executes a low-down and dirty command

ansible.builtin.reboot – Reboot a machine

ansible.builtin.replace – Replace all instances of a particular string in a file using a back-referenced regular expression

ansible.builtin.rpm_key – Adds or removes a gpg key from the rpm db

ansible.builtin.script – Runs a local script on a remote node after transferring it

ansible.builtin.service – Manage services

ansible.builtin.service_facts – Return service state information as fact data

ansible.builtin.set_fact – Set host variable(s) and fact(s).

ansible.builtin.set_stats – Define and display stats for the current ansible run

ansible.builtin.setup – Gathers facts about remote hosts

ansible.builtin.shell – Execute shell commands on targets

ansible.builtin.slurp – Slurps a file from remote nodes

ansible.builtin.stat – Retrieve file or file system status

ansible.builtin.subversion – Deploys a subversion repository

ansible.builtin.systemd_service – Manage systemd units

ansible.builtin.sysvinit – Manage SysV services.

ansible.builtin.tempfile – Creates temporary files and directories

ansible.builtin.template – Template a file out to a target host

ansible.builtin.unarchive – Unpacks an archive after (optionally) copying it from the local machine

ansible.builtin.uri – Interacts with webservices

ansible.builtin.user – Manage user accounts

ansible.builtin.validate_argument_spec – Validate role argument specs.

ansible.builtin.wait_for – Waits for a condition before continuing

ansible.builtin.wait_for_connection – Waits until remote system is reachable/usable

ansible.builtin.yum_repository – Add or remove YUM repositories

---

## Shell plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/shell.html

**Contents:**
- Shell plugins
- Enabling shell plugins
- Using shell plugins
- Plugin list

Enabling shell plugins

Shell plugins work to ensure that the basic commands Ansible runs are properly formatted to work with the target machine and allow the user to configure certain behaviors related to how Ansible executes tasks.

You can add a custom shell plugin by dropping it into a shell_plugins directory adjacent to your play, inside a role, or by putting it in one of the shell plugin directory sources configured in ansible.cfg.

You should not alter which plugin is used unless you have a setup in which the default /bin/sh is not a POSIX-compatible shell or is not available for execution.

In addition to the default configuration settings in Ansible Configuration Settings, you can use the connection variable ansible_shell_type to select the plugin to use. In this case, you will also want to update the ansible_shell_executable to match.

You can further control the settings for each plugin with other configuration options detailed in the plugin themselves. You can use ansible-doc -t shell -l to see the list of available plugins. Use ansible-doc -t shell <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Windows module development walkthrough — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_general_windows.html

**Contents:**
- Windows module development walkthrough
- Windows environment setup
- Create a Windows server in a VM
- Create an Ansible inventory
- Provisioning the environment
- Windows new module development
- Windows module utilities
  - Exposing shared module options
- Windows playbook module testing
- Windows debugging

In this section, we will walk through developing, testing, and debugging an Ansible Windows module.

Because Windows modules are written in Powershell and need to be run on a Windows host, this guide differs from the usual development walkthrough guide.

What’s covered in this section:

Windows environment setup

Create a Windows server in a VM

Create an Ansible inventory

Provisioning the environment

Windows new module development

Windows module utilities

Exposing shared module options

Windows playbook module testing

Windows integration testing

Windows communication and development support

Unlike Python module development which can be run on the host that runs Ansible, Windows modules need to be written and tested for Windows hosts. While evaluation editions of Windows can be downloaded from Microsoft, these images are usually not ready to be used by Ansible without further modification. The easiest way to set up a Windows host so that it is ready to by used by Ansible is to set up a virtual machine using Vagrant. Vagrant can be used to download existing OS images called boxes that are then deployed to a hypervisor like VirtualBox. These boxes can either be created and stored offline or they can be downloaded from a central repository called Vagrant Cloud.

This guide will use the Vagrant boxes created by the packer-windoze repository which have also been uploaded to Vagrant Cloud. To find out more info on how these images are created, please go to the GitHub repo and look at the README file.

Before you can get started, the following programs must be installed (please consult the Vagrant and VirtualBox documentation for installation instructions):

To create a single Windows Server 2016 instance, run the following:

This will download the Vagrant box from Vagrant Cloud and add it to the local boxes on your host and then start up that instance in VirtualBox. When starting for the first time, the Windows VM will run through the sysprep process and then create a HTTP and HTTPS WinRM listener automatically. Vagrant will finish its process once the listeners are online, after which the VM can be used by Ansible.

The following Ansible inventory file can be used to connect to the newly created Windows VM:

The port 55986 is automatically forwarded by Vagrant to the Windows host that was created, if this conflicts with an existing local port then Vagrant will automatically use another one at random and display show that in the output.

The OS that is created is based on the image set. The following images can be used:

jborean93/WindowsServer2012

jborean93/WindowsServer2012R2

jborean93/WindowsServer2016

jborean93/WindowsServer2019

jborean93/WindowsServer2022

When the host is online, it can accessible by RDP on 127.0.0.1:3389 but the port may differ depending if there was a conflict. To get rid of the host, run vagrant destroy --force and Vagrant will automatically remove the VM and any other files associated with that VM.

While this is useful when testing modules on a single Windows instance, these host won’t work without modification with domain based modules. The Vagrantfile at ansible-windows can be used to create a test domain environment to be used in Ansible. This repo contains three files which are used by both Ansible and Vagrant to create multiple Windows hosts in a domain environment. These files are:

Vagrantfile: The Vagrant file that reads the inventory setup of inventory.yml and provisions the hosts that are required

inventory.yml: Contains the hosts that are required and other connection information such as IP addresses and forwarded ports

main.yml: Ansible playbook called by Vagrant to provision the domain control node and join the child hosts to the domain

By default, these files will create the following environment:

A single AD domain controller running on Windows Server 2016

Five child hosts for each major Windows Server version joined to that domain

A domain with the DNS name domain.local

A local administrator account on each host with the username vagrant and password vagrant

A domain admin account vagrant-domain@domain.local with the password VagrantPass1

The domain name and accounts can be modified by changing the variables domain_* in the inventory.yml file if it is required. The inventory file can also be modified to provision more or less servers by changing the hosts that are defined under the domain_children key. The host variable ansible_host is the private IP that will be assigned to the VirtualBox host only network adapter while vagrant_box is the box that will be used to create the VM.

To provision the environment as is, run the following:

Vagrant provisions each host sequentially so this can take some time to complete. If any errors occur during the Ansible phase of setting up the domain, run vagrant provision to rerun just that step.

Unlike setting up a single Windows instance with Vagrant, these hosts can also be accessed using the IP address directly as well as through the forwarded ports. It is easier to access it over the host only network adapter as the normal protocol ports are used, for example RDP is still over 3389. In cases where the host cannot be resolved using the host only network IP, the following protocols can be access over 127.0.0.1 using these forwarded ports:

Replace xx with the entry number in the inventory file where the domain controller started with 00 and is incremented from there. For example, in the default inventory.yml file, WinRM over HTTPS for SERVER2012R2 is forwarded over port 29804 as it is the fourth entry in domain_children.

When creating a new module there are a few things to keep in mind:

Module code is in Powershell (.ps1) files while the documentation is contained in Python (.py) files of the same name

Avoid using Write-Host/Debug/Verbose/Error in the module and add what needs to be returned to the $module.Result variable

To fail a module, call $module.FailJson("failure message here"), an Exception or ErrorRecord can be set to the second argument for a more descriptive error message

You can pass in the exception or ErrorRecord as a second argument to FailJson("failure", $_) to get a more detailed output

Most new modules require check mode and integration tests before they are merged into the main Ansible codebase

Avoid using try/catch statements over a large code block, rather use them for individual calls so the error message can be more descriptive

Try and catch specific exceptions when using try/catch statements

Avoid using PSCustomObjects unless necessary

Look for common functions in ./lib/ansible/module_utils/powershell/ and use the code there instead of duplicating work. These can be imported by adding the line #Requires -Module * where * is the file name to import, and will be automatically included with the module code sent to the Windows target when run through Ansible

As well as PowerShell module utils, C# module utils are stored in ./lib/ansible/module_utils/csharp/ and are automatically imported in a module execution if the line #AnsibleRequires -CSharpUtil * is present

C# and PowerShell module utils achieve the same goal but C# allows a developer to implement low level tasks, such as calling the Win32 API, and can be faster in some cases

Ensure the code runs under Powershell v5.1 and higher on Windows Server 2016 and higher; if higher minimum Powershell or OS versions are required, ensure the documentation reflects this clearly

Ansible runs modules under strictmode version 2.0. Be sure to test with that enabled by putting Set-StrictMode -Version 2.0 at the top of your dev script

Favor native Powershell cmdlets over executable calls if possible

Use the full cmdlet name instead of aliases, for example Remove-Item over rm

Use named parameters with cmdlets, for example Remove-Item -Path C:\temp over Remove-Item C:\temp

A very basic Powershell module win_environment incorporates best practices for Powershell modules. It demonstrates how to implement check-mode and diff-support, and also shows a warning to the user when a specific condition is met.

A slightly more advanced module is win_uri which additionally shows how to use different parameter types (bool, str, int, list, dict, path) and a selection of choices for parameters, how to fail a module and how to handle exceptions.

As part of the new AnsibleModule wrapper, the input parameters are defined and validated based on an argument spec. The following options can be set at the root level of the argument spec:

mutually_exclusive: A list of lists, where the inner list contains module options that cannot be set together

no_log: Stops the module from emitting any logs to the Windows Event log

options: A dictionary where the key is the module option and the value is the spec for that option

required_by: A dictionary where the option(s) specified by the value must be set if the option specified by the key is also set

The first element is the module option to check the value against

The second element is the value of the option specified by the first element, if matched then the required if check is run

The third element is a list of required module options when the above is matched

An optional fourth element is a boolean that states whether all module options in the third elements are required (default: $false) or only one ($true)

required_one_of: A list of lists, where the inner list contains module options where at least one must be set

required_together: A list of lists, where the inner list contains module options that must be set together

supports_check_mode: Whether the module supports check mode, by default this is $false

The actual input options for a module are set within the options value as a dictionary. The keys of this dictionary are the module option names while the values are the spec of that module option. Each spec can have the following options set:

aliases: A list of aliases for the module option

choices: A list of valid values for the module option, if type=list then each list value is validated against the choices and not the list itself

default: The default value for the module option if not set

deprecated_aliases: A list of hashtables that define aliases that are deprecated and the versions they will be removed in. Each entry must contain the keys name and collection_name with either version or date

elements: When type=list, this sets the type of each list value, the values are the same as type

no_log: Will sanitize the input value before being returned in the module_invocation return value

removed_in_version: States when a deprecated module option is to be removed, a warning is displayed to the end user if set

removed_at_date: States the date (YYYY-MM-DD) when a deprecated module option will be removed, a warning is displayed to the end user if set

removed_from_collection: States from which collection the deprecated module option will be removed; must be specified if one of removed_in_version and removed_at_date is specified

required: Will fail when the module option is not set

bool: A boolean value

dict: A dictionary value, if the input is a JSON or key=value string then it is converted to dictionary

float: A float or Single value

json: A string where the value is converted to a JSON string if the input is a dictionary

list: A list of values, elements=<type> can convert the individual list value types if set. If elements=dict then options is defined, the values will be validated against the argument spec. When the input is a string then the string is split by , and any whitespace is trimmed

path: A string where values likes %TEMP% are expanded based on environment values. If the input value starts with \\?\ then no expansion is run

raw: No conversions occur on the value passed in by Ansible

sid: Will convert Windows security identifier values or Windows account names to a SecurityIdentifier value

str: The value is converted to a string

When type=dict, or type=list and elements=dict, the following keys can also be set for that module option:

apply_defaults: The value is based on the options spec defaults for that key if True and null if False. Only valid when the module option is not defined by the user and type=dict.

mutually_exclusive: Same as the root level mutually_exclusive but validated against the values in the sub dict

options: Same as the root level options but contains the valid options for the sub option

required_if: Same as the root level required_if but validated against the values in the sub dict

required_by: Same as the root level required_by but validated against the values in the sub dict

required_together: Same as the root level required_together but validated against the values in the sub dict

required_one_of: Same as the root level required_one_of but validated against the values in the sub dict

A module type can also be a delegate function that converts the value to whatever is required by the module option. For example the following snippet shows how to create a custom type that creates a UInt64 value:

When in doubt, look at some of the other core modules and see how things have been implemented there.

Sometimes there are multiple ways that Windows offers to complete a task; this is the order to favor when writing modules:

Native Powershell cmdlets like Remove-Item -Path C:\temp -Recurse

.NET classes like [System.IO.Path]::GetRandomFileName()

WMI objects through the New-CimInstance cmdlet

COM objects through New-Object -ComObject cmdlet

Calls to native executables like Secedit.exe

PowerShell modules support a small subset of the #Requires options built into PowerShell as well as some Ansible-specific requirements specified by #AnsibleRequires. These statements can be placed at any point in the script, but are most commonly near the top. They are used to make it easier to state the requirements of the module without writing any of the checks. Each requires statement must be on its own line, but there can be multiple requires statements in one script.

These are the checks that can be used within Ansible modules:

#Requires -Module Ansible.ModuleUtils.<module_util>: Added in Ansible 2.4, specifies a module_util to load in for the module execution.

#Requires -Version x.y: Added in Ansible 2.5, specifies the version of PowerShell that is required by the module. The module will fail if this requirement is not met.

#AnsibleRequires -PowerShell <module_util>: Added in Ansible 2.8, like #Requires -Module, this specifies a module_util to load in for module execution.

#AnsibleRequires -CSharpUtil <module_util>: Added in Ansible 2.8, specifies a C# module_util to load in for the module execution.

#AnsibleRequires -OSVersion x.y: Added in Ansible 2.5, specifies the OS build version that is required by the module and will fail if this requirement is not met. The actual OS version is derived from [Environment]::OSVersion.Version.

#AnsibleRequires -Become: Added in Ansible 2.5, forces the exec runner to run the module with become, which is primarily used to bypass WinRM restrictions. If ansible_become_user is not specified then the SYSTEM account is used instead.

The #AnsibleRequires -PowerShell and #AnsibleRequires -CSharpUtil support further features such as:

Importing a util contained in a collection (added in Ansible 2.9)

Importing a util by relative names (added in Ansible 2.10)

Specifying the util is optional by adding -Optional to the import declaration (added in Ansible 2.12).

See the below examples for more details:

For optional require statements, it is up to the module code to then verify whether the util has been imported before trying to use it. This can be done by checking if a function or type provided by the util exists or not.

While both #Requires -Module and #AnsibleRequires -PowerShell can be used to load a PowerShell module it is recommended to use #AnsibleRequires. This is because #AnsibleRequires supports collection module utils, imports by relative util names, and optional util imports.

C# module utils can reference other C# utils by adding the line using Ansible.<module_util>; to the top of the script with all the other using statements.

Like Python modules, PowerShell modules also provide a number of module utilities that provide helper functions within PowerShell. These module_utils can be imported by adding the following line to a PowerShell module:

This will import the module_util at ./lib/ansible/module_utils/powershell/Ansible.ModuleUtils.Legacy.psm1 and enable calling all of its functions. As of Ansible 2.8, Windows module utils can also be written in C# and stored at lib/ansible/module_utils/csharp. These module_utils can be imported by adding the following line to a PowerShell module:

This will import the module_util at ./lib/ansible/module_utils/csharp/Ansible.Basic.cs and automatically load the types in the executing process. C# module utils can reference each other and be loaded together by adding the following line to the using statements at the top of the util:

There are special comments that can be set in a C# file for controlling the compilation parameters. The following comments can be added to the script;

//AssemblyReference -Name <assembly dll> [-CLR [Core|Framework]]: The assembly DLL to reference during compilation, the optional -CLR flag can also be used to state whether to reference when running under .NET Core, Framework, or both (if omitted)

//NoWarn -Name <error id> [-CLR [Core|Framework]]: A compiler warning ID to ignore when compiling the code, the optional -CLR works the same as above. A list of warnings can be found at Compiler errors

As well as this, the following pre-processor symbols are defined;

CORECLR: This symbol is present when PowerShell is running through .NET Core

WINDOWS: This symbol is present when PowerShell is running on Windows

UNIX: This symbol is present when PowerShell is running on Unix

A combination of these flags help to make a module util interoperable on both .NET Framework and .NET Core, here is an example of them in action:

The following is a list of module_utils that are packaged with Ansible and a general description of what they do:

ArgvParser: Utility used to convert a list of arguments to an escaped string compliant with the Windows argument parsing rules.

CamelConversion: Utility used to convert camelCase strings/lists/dicts to snake_case.

CommandUtil: Utility used to execute a Windows process and return the stdout/stderr and rc as separate objects.

FileUtil: Utility that expands on the Get-ChildItem and Test-Path to work with special files like C:\pagefile.sys.

Legacy: General definitions and helper utilities for Ansible module.

LinkUtil: Utility to create, remove, and get information about symbolic links, junction points and hard inks.

SID: Utilities used to convert a user or group to a Windows SID and vice versa.

For more details on any specific module utility and their requirements, please see the Ansible module utilities source code.

PowerShell module utilities can be stored outside of the standard Ansible distribution for use with custom modules. Custom module_utils are placed in a folder called module_utils located in the root folder of the playbook or role directory.

C# module utilities can also be stored outside of the standard Ansible distribution for use with custom modules. Like PowerShell utils, these are stored in a folder called module_utils and the file name must end in the extension .cs, start with Ansible. and be named after the namespace defined in the util.

The below example is a role structure that contains two PowerShell custom module_utils called Ansible.ModuleUtils.ModuleUtil1, Ansible.ModuleUtils.ModuleUtil2, and a C# util containing the namespace Ansible.CustomUtil:

Each PowerShell module_util must contain at least one function that has been exported with Export-ModuleMember at the end of the file. For example

PowerShell module utils can easily expose common module options that a module can use when building its argument spec. This allows common features to be stored and maintained in one location and have those features used by multiple modules with minimal effort. Any new features or bugfixes added to one of these utils are then automatically used by the various modules that call that util.

An example of this would be to have a module util that handles authentication and communication against an API This util can be used by multiple modules to expose a common set of module options like the API endpoint, username, password, timeout, cert validation, and so on without having to add those options to each module spec.

The standard convention for a module util that has a shared argument spec would have

It is highly recommended to make this function name be unique to the module to avoid any conflicts with other utils that can be loaded

The format of the output spec is a Hashtable in the same format as the $spec used for normal modules

A function that takes in an AnsibleModule object called under the -Module parameter which it can use to get the shared options

Because these options can be shared across various module it is highly recommended to keep the module option names and aliases in the shared spec as specific as they can be. For example do not have a util option called password, rather you should prefix it with a unique name like acme_password.

Failure to have a unique option name or alias can prevent the util being used by module that also use those names or aliases for its own options.

The following is an example module util called ServiceAuth.psm1 in a collection that implements a common way for modules to authentication with a service.

For a module to take advantage of this common argument spec it can be set out like

Options defined in the module spec will always have precedence over a util spec. Any list values under the same key in a util spec will be appended to the module spec for that same key. Dictionary values will add any keys that are missing from the module spec and merge any values that are lists or dictionaries. This is similar to how the doc fragment plugins work when extending module documentation.

To document these shared util options for a module, create a doc fragment plugin that documents the options implemented by the module util and extend the module docs for every module that implements the util to include that fragment in its docs.

You can test a module with an Ansible playbook. For example:

Create a playbook in any directory touch testmodule.yml.

Create an inventory file in the same directory touch hosts.

Populate the inventory file with the variables required to connect to a Windows host(s).

Add the following to the new playbook file:

Run the playbook ansible-playbook -i hosts testmodule.yml

This can be useful for seeing how Ansible runs with the new module end to end. Other possible ways to test the module are shown below.

Debugging a module currently can only be done on a Windows host. This can be useful when developing a new module or implementing bug fixes. These are some steps that need to be followed to set this up:

Copy the module script to the Windows server

Copy the folders ./lib/ansible/module_utils/powershell and ./lib/ansible/module_utils/csharp to the same directory as the script above

Add an extra # to the start of any #Requires -Module lines in the module code, this is only required for any lines starting with #Requires -Module

Add the following to the start of the module script that was copied to the server:

You can add more args to $complex_args as required by the module or define the module options through a JSON file with the structure:

There are multiple IDEs that can be used to debug a Powershell script, two of the most popular ones are

To be able to view the arguments as passed by Ansible to the module follow these steps.

Prefix the Ansible command with ANSIBLE_KEEP_REMOTE_FILES=1 to specify that Ansible should keep the exec files on the server.

Log onto the Windows server using the same user account that Ansible used to execute the module.

Navigate to %TEMP%\... It should contain a folder starting with ansible-tmp-.

Inside this folder, open the PowerShell script for the module.

In this script is a raw JSON script under $json_raw which contains the module arguments under module_args. These args can be assigned manually to the $complex_args variable that is defined on your debug script or put in the args.json file.

Currently there is no mechanism to run unit tests for Powershell modules under Ansible CI.

Integration tests for Ansible modules are typically written as Ansible roles. These test roles are located in ./test/integration/targets. You must first set up your testing environment, and configure a test inventory for Ansible to connect to.

In this example we will set up a test inventory to connect to two hosts and run the integration tests for win_stat:

Run the command source ./hacking/env-setup to prepare environment.

Create a copy of ./test/integration/inventory.winrm.template and name it inventory.winrm.

Fill in entries under [windows] and set the required variables that are needed to connect to the host.

Install the required Python modules to support WinRM and a configured authentication method.

To execute the integration tests, run ansible-test windows-integration win_stat; you can replace win_stat with the role you want to test.

This will execute all the tests currently defined for that role. You can set the verbosity level using the -v argument just as you would with ansible-playbook.

When developing tests for a new module, it is recommended to test a scenario once in check mode and twice not in check mode. This ensures that check mode does not make any changes but reports a change, as well as that the second run is idempotent and does not report changes. For example:

Join the Ansible Forum and use the windows tag for discussions about Ansible development for Windows.

**Examples:**

Example 1 (unknown):
```unknown
vagrant init jborean93/WindowsServer2016
vagrant up
```

Example 2 (unknown):
```unknown
[windows]
WindowsServer  ansible_host=127.0.0.1

[windows:vars]
ansible_user=vagrant
ansible_password=vagrant
ansible_port=55986
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

Example 3 (unknown):
```unknown
git clone https://github.com/jborean93/ansible-windows.git
cd vagrant
vagrant up
```

Example 4 (unknown):
```unknown
$spec = @{
    uint64_type = @{ type = [Func[[Object], [UInt64]]]{ [System.UInt64]::Parse($args[0]) } }
}
$uint64_type = $module.Params.uint64_type
```

---

## Contributing your module to an existing Ansible collection — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_checklist.html

**Contents:**
- Contributing your module to an existing Ansible collection
- Contributing modules: objective requirements
- Contributing to Ansible: subjective requirements
- Other checklists

If you want to contribute a module to an existing collection, you must meet the community’s objective and subjective requirements. Please read the details below, and also review our tips for module development.

Modules accepted into certain collections are included in every Ansible release on PyPI. However, contributing to one of these collections is not the only way to distribute a module - you can create your own collection, embed modules in roles on Galaxy or simply share copies of your module code for local use.

To contribute a module to most Ansible collections, you must:

write your module in either Python or Powershell for Windows

use the AnsibleModule common code

support Python 2.6 and Python 3.5 - if your module cannot support Python 2.6, explain the required minimum Python version and rationale in the requirements section in DOCUMENTATION

use proper Python 3 syntax

follow PEP 8 Python style conventions - see pep8 for more information

license your module under the GPL license (GPLv3 or later)

understand the DCO agreement, which applies to contributions to the Ansible Core and Ansible Documentation repositories.

conform to Ansible’s formatting and documentation standards

include comprehensive tests for your module

minimize module dependencies

support check_mode if possible

ensure your code is readable

if a module is named <something>_facts, it should be because its main purpose is returning ansible_facts. Do not name modules that do not do this with _facts. Only use ansible_facts for information that is specific to the host machine, for example network interfaces and their configuration, which operating system and which programs are installed.

Modules that query/return general information (and not ansible_facts) should be named _info. General information is non-host specific information, for example information on online/cloud services (you can access different accounts for the same online service from the same host), or information on VMs and containers accessible from the machine.

Additional requirements may apply for certain collections. Review the individual collection repositories for more information.

Please make sure your module meets these requirements before you submit your PR/proposal. If you have questions, visit the Ansible communication guide for information on how to reach out to the community.

If your module meets these objective requirements, collection maintainers will review your code to see if they think it is clear, concise, secure, and maintainable. They will consider whether your module provides a good user experience, helpful error messages, reasonable defaults, and more. This process is subjective, with no exact standards for acceptance. For the best chance of getting your module accepted, follow our tips for module development.

Tips for module development.

Windows development checklist.

---

## Cache plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/cache.html

**Contents:**
- Cache plugins
- Enabling fact cache plugins
- Enabling inventory cache plugins
- Using cache plugins
- Plugin list

Enabling fact cache plugins

Enabling inventory cache plugins

Cache plugins allow Ansible to store gathered facts or inventory source data without the performance hit of retrieving them from the source.

The default cache plugin is the memory plugin, which only caches the data for the current execution of Ansible. Other plugins with persistent storage are available to allow caching of the data across runs. Some of these cache plugins write to files, and others write to databases.

You can use different cache plugins for inventory and facts. If you enable inventory caching without setting an inventory-specific cache plugin, Ansible uses the fact cache plugin for both facts and inventory. If necessary, you can create custom cache plugins.

Fact caching is always enabled. However, only one fact cache plugin can be active at a time. You can select the cache plugin to use for fact caching in the Ansible configuration, either with an environment variable:

or in the ansible.cfg file:

If the cache plugin is in a collection use the fully qualified name:

To enable a custom cache plugin, save it in one of the directory sources configured in ansible.cfg or in a collection and then reference it by FQCN.

You also need to configure other settings specific to each plugin. Consult the individual plugin documentation or the Ansible configuration for more details.

Inventory caching is disabled by default. To cache inventory data, you must enable inventory caching and then select the specific cache plugin you want to use. Not all inventory plugins support caching, so check the documentation for the inventory plugin(s) you want to use. You can enable inventory caching with an environment variable:

or in the ansible.cfg file:

or if the inventory plugin accepts a YAML configuration source, in the configuration file:

Only one inventory cache plugin can be active at a time. You can set it with an environment variable:

or in the ansible.cfg file:

or if the inventory plugin accepts a YAML configuration source, in the configuration file:

To cache inventory with a custom plugin in your plugin path, follow the developer guide on cache plugins.

To cache inventory with a cache plugin in a collection, use the FQCN:

If you enable caching for inventory plugins without selecting an inventory-specific cache plugin, Ansible falls back to caching inventory with the fact cache plugin you configured. Consult the individual inventory plugin documentation or the Ansible configuration for more details.

Cache plugins are used automatically once they are enabled.

You can use ansible-doc -t cache -l to see the list of available plugins. Use ansible-doc -t cache <plugin name> to see plugin-specific documentation and examples.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
export ANSIBLE_CACHE_PLUGIN=jsonfile
```

Example 2 (unknown):
```unknown
[defaults]
fact_caching=redis
```

Example 3 (unknown):
```unknown
[defaults]
fact_caching = namespace.collection_name.cache_plugin_name
```

Example 4 (unknown):
```unknown
export ANSIBLE_INVENTORY_CACHE=True
```

---

## Index of all Callback Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_callback.html

**Contents:**
- Index of all Callback Plugins
- ansible.builtin

List of callback plugins by callback type

ansible.builtin.default – default Ansible screen output

ansible.builtin.junit – write playbook output to a JUnit file.

ansible.builtin.minimal – minimal Ansible screen output

ansible.builtin.oneline – oneline Ansible screen output

ansible.builtin.tree – Save host events to files

---

## Rejecting modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/module_plugin_guide/plugin_filtering_config.html

**Contents:**
- Rejecting modules

If you want to avoid using certain modules, you can add them to a reject list to prevent Ansible from loading them. To reject plugins, create a yaml configuration file. The default location for this file is /etc/ansible/plugin_filters.yml. You can select a different path for the reject list using the PLUGIN_FILTERS_CFG setting in the defaults section of your ansible.cfg. Here is an example reject list:

The file contains two fields:

A file version so that you can update the format while keeping backward compatibility in the future. The present version should be the string, "1.0"

A list of modules to reject. Ansible will not load any module in this list when it searches for a module to invoke for a task.

The stat module is required for Ansible to run. Do not add this module to your reject list.

**Examples:**

Example 1 (unknown):
```unknown
---
filter_version: '1.0'
module_rejectlist:
  # Deprecated
  - docker
  # We only allow pip, not easy_install
  - easy_install
```

---

## Module format and documentation — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_documenting.html

**Contents:**
- Module format and documentation
- Non-Python modules documentation
- Python shebang & UTF-8 coding
- Copyright and license
- DOCUMENTATION block
  - Documentation fields
  - Documentation fragments
- EXAMPLES block
- RETURN block
- Python imports

In most cases if you want to contribute your module to an Ansible collection, you should write your module in Python and follow the standard format described below. If you are writing a Windows module, you should follow the Windows guidelines.

Before you open a pull request, in addition to following these guidelines, please also review and adhere to the practices outlined in the following sections:

testing before you open a pull request

Every Ansible module written in Python must begin with seven standard sections in a particular order, followed by the code. The sections in order are:

Non-Python modules documentation

Python shebang & UTF-8 coding

Copyright and license

Testing module documentation

If you are curious why imports are not located at the top of the file, see the Python imports section.

If you see any discrepancies in older Ansible modules, please open a pull request with modifications that satisfy these guidelines.

For modules written in languages other than Python, there are two approaches to handling documentation:

Option one: Create a .py file that contains the documentation-related sections described in this document.

Option two: Create a .yml file that has the same data structure in pure YAML.

With YAML files, the examples below are easy to use by removing Python quoting and substituting = for :, for example DOCUMENTATION = r''' ... ''' to DOCUMENTATION: ... and removing closing quotes. Refer to Adjacent YAML documentation files for details.

Begin your Ansible module with the #!/usr/bin/python shebang so that ansible_python_interpreter works.

If you develop the module using a different scripting language, adjust the interpreter accordingly (#!/usr/bin/<interpreter>) so ansible_<interpreter>_interpreter can work for that specific language.

Binary modules do NOT require a shebang or an interpreter.

Do NOT use #!/usr/bin/env because it makes env the interpreter and bypasses ansible_<interpreter>_interpreter logic.

Passing arguments to the interpreter in the shebang does not work; for example, #!/usr/bin/env python.

Follow the shebang immediately with # -*- coding: utf-8 -*- to clarify that the file is UTF-8 encoded.

After the shebang and UTF-8 encoding lines, add a copyright line with the original copyright holder and a license declaration.

The license declaration should be one line ONLY, not the full GPL prefix, as follows:

Additions to the module MUST NOT include additional copyright lines beyond the default statement, unless the default copyright statement is missing.

Any legal review will include the source control history, so an exhaustive copyright header is not necessary.

Please do NOT include a copyright year.

If the existing copyright statement includes a year, do NOT edit the existing copyright year.

Do NOT modify the existing copyright header without permission from the copyright author.

Before committing your module documentation, please test it at the command line and as HTML.

After the shebang, the UTF-8 encoding, the copyright line, and the license section comes the DOCUMENTATION block. Ansible’s online module documentation is generated from the DOCUMENTATION blocks in the source code of each module.

The DOCUMENTATION block must be valid YAML. To make it easier:

Start by copying our example documentation string.

Write the block in an editor with YAML syntax highlighting before you include it in your Python file.

If you run into syntax issues that are difficult to resolve, use the YAML Lint website to help validate the YAML.

When writing module documentation, take the following statements into consideration:

Module documentation should briefly and accurately define what each module and option does and how it works with others in the underlying system.

Module documentation should be written for a broad audience and be easily understood both by experts and non-experts.

Descriptions should always start with a capital letter and end with a full stop or period. Consistency always helps.

For password and secret arguments no_log=True should be set and any example passwords, secrets, or hashes should start with EXAMPLE to ensure no real passwords and so on are leaked.

For arguments that seem to contain sensitive information but do not contain secrets, such as “password_length”, set no_log=False to disable the warning message.

If an option is only required in certain conditions, describe those conditions; for example, “Required when I(state=present).”

If your module allows check_mode, reflect this fact in the documentation.

To create clear, concise, consistent, and useful documentation, follow the style guide.

Each documentation field is described below.

All fields in the DOCUMENTATION block are lower-case.

All fields are required unless specified otherwise.

The name of the module.

Must be the same as the file name, without the .py extension.

A short description which is displayed on the Collection Index page and ansible-doc -l.

The short_description is displayed by ansible-doc -l without any category grouping, so it needs enough detail to explain the module’s purpose without the context of the directory structure in which it lives.

Unlike description:, short_description MUST NOT have a trailing period/full stop.

You can use Ansible markup in this field.

A detailed description (generally two or more sentences).

Each sentence MUST be full: start with a capital letter and end with a period.

SHOULD NOT mention the module name.

Make use of multiple entries rather than using one long paragraph.

MUST NOT quote complete values unless it is required by YAML.

You can use Ansible markup in this field.

This is a string, not a float, and should be quoted to avoid errors.

For ansible.builtin.* modules (included in ansible-core), it is a version of ansible-core, for example, version_added: '2.18'

In collections, it MUST be a version of a collection (not the Ansible version) when the module was added, for example, version_added: '1.0.0'.

Name of the module author in the form First Last (@GitHubID).

Use a multi-line list if there is more than one author.

Do NOT use quotes unless it is required by YAML.

Marks modules that will be removed in future releases. See also The lifecycle of an Ansible module or plugin.

Options are often called “parameters” or “arguments”. Because the documentation field is called options, we will use that term.

If the module has no options (for example, it is a _facts module), all you need is one line: options: {}.

If your module has options (in other words, accepts arguments), document them thoroughly. For each module option, include:

Name it as a declarative operation (not CRUD) that focuses on the final state, for example online:, rather than is_online:.

Make the name consistent with the rest of the module, as well as other modules in the same category.

When in doubt, look for other modules to find option names that are used for the same purpose, we like to offer consistency to our users.

There is no explicit field option-name. This entry is about the key of the option in the options dictionary.

Detailed explanation of what this option does. Write it in full sentences that shart with a capital letter and end with a period.

The first entry is a description of the option itself; subsequent entries detail its use, dependencies, or format of possible values.

Do NOT list the possible values (that’s what the choices: field is for, though it should explain what the values do if they are not obvious).

If an option is only sometimes required, describe the conditions. For example, “Required when O(state=present).”

Mutually exclusive options MUST be documented as the final sentence on each of the options.

You can use Ansible markup in this field.

If missing, we assume the option is not required.

If required is either false or missing, default may be specified (assumed null if missing).

Ensure that the default value in the docs matches the default value in the code.

The default field MUST NOT be listed as part of the description, unless it requires additional information or conditions.

If the option is a boolean value, you can use any of the boolean values recognized by Ansible (such as true/false or yes/no). Document booleans as true/false for consistency and compatibility with ansible-lint.

List of option values.

Do NOT use it if empty.

Specifies the data type that option accepts, MUST match the argument_spec dictionary.

If an argument is type='bool', set it to type: bool and do NOT specify choices.

If an argument is type='list', specify elements.

Specifies the data type for list elements in case type='list'.

List of optional name aliases.

Generally not needed and not recommended to ensure consistency in the module usage.

Only needed if this option was added after initial module release; in other words, this is greater than the top (module) level version_added field.

This is a string, not a float, for example, for a module in ansible-core this could be version_added: '2.18'.

In collections, this MUST be the collection version the option was added to, not the Ansible version. For example, version_added: '1.0.0'.

If this option takes a dict or list of dicts, you can define the structure here.

See azure.azcollection.azure_rm_securitygroup, azure.azcollection.azure_rm_azurefirewall, and openstack.cloud.baremetal_node_action for examples.

List of requirements (if applicable).

Include minimum versions.

You can use Ansible markup in this field.

A list of references to other modules, documentation, or internet resources.

Because it is more prominent, use seealso for general references instead of notes or adding links to the module description.

References to modules MUST use the FQCN or ansible.builtin for modules in ansible-core.

Plugin references are supported since ansible-core 2.15.

You can use Ansible markup in the description and name fields.

A reference can be one of the following formats:

If you use ref: to link to an anchor that is not associated with a title, you MUST add a title to the ref for the link to work correctly.

A dictionary mapping attribute names to dictionaries describing that attribute.

Usually attributes are provided by documentation fragments, for example ansible.builtin.action_common_attributes and its sub-fragments. Modules and plugins use the appropriate docs fragments and fill in the support, details, and potential attribute-specific other fields.

A string or a list of strings. Each string is one paragraph.

Explanation of what this attribute does. It should be written in full sentences.

You can use Ansible markup in this field.

Generally optional, but must be provided if support is partial.

A string or a list of strings. Each string is one paragraph.

Describes how support might not work as expected by the user.

You can use Ansible markup in this field.

Must be one of full, none, partial, or N/A.

Indicates whether this attribute is supported by this module or plugin.

MUST ONLY be provided for the attribute action_group.

Lists the action groups this module or action is part of.

A string or a list of strings.

MUST ONLY be used for the attribute platform.

Lists the platforms the module or action supports.

A string or a list of strings.

Only needed if this attribute’s support was extended after the module/plugin was created, in other words, this is greater than the top (module) level version_added field.

This is a string, and not a float, for example, version_added: '2.3'.

In collections, this must be the collection version the attribute’s support was added to, not the Ansible version. For example, version_added: '1.0.0'.

Details of any important information that does not fit in one of the above sections.

Do NOT list check_mode or diff information under notes. Use the attributes field instead.

Because it stands out better, use seealso for general references over the use of notes.

You can use Ansible markup in this field.

If you are writing multiple related modules, they may share common documentation, such as options, authentication details, file mode settings, notes: or seealso: entries. Rather than duplicate that information in each module’s DOCUMENTATION block, you can save it once as a doc_fragment plugin and then include it in each module’s documentation.

In Ansible, shared documentation fragments are contained in a ModuleDocFragment class in lib/ansible/plugins/doc_fragments/ or in the plugins/doc_fragments directory in a collection. To include a documentation fragment, add extends_documentation_fragment: FRAGMENT_NAME in your module documentation. Use the fully qualified collection name for the FRAGMENT_NAME (for example, kubernetes.core.k8s_auth_options).

Modules should only use items from a doc fragment if the module will implement all of the interface documented there in a manner that behaves the same as the existing modules which import that fragment. The goal is that items imported from the doc fragment will behave identically when used in another module that imports the doc fragment.

By default, only the DOCUMENTATION property from a doc fragment is inserted into the module documentation. It is possible to define additional properties in the doc fragment in order to import only certain parts of a doc fragment or mix and match as appropriate. If a property is defined in both the doc fragment and the module, the module value overrides the doc fragment.

Here is an example doc fragment named example_fragment.py:

To insert the contents of OTHER in a module:

Since Ansible 2.8, you can have user-supplied doc_fragments by using a doc_fragments directory adjacent to play or role, just like any other plugin.

For example, all AWS modules should include:

Using documentation fragments in collections describes how to incorporate documentation fragments in a collection.

Immediately after the DOCUMENTATION block comes the EXAMPLES block. Here you show users how your module works with real-world examples in multi-line plain-text YAML format. The best examples are ready for the user to copy and paste into a playbook. Review and update your examples with every change to your module.

If the module has integration tests, add the example you want to add to the integration tests to make sure it works.

Each example should include a name: line:

The name: line should be capitalized and not include a trailing dot.

Use a fully qualified collection name (FQCN) as a part of the module’s name like in the example above.

For modules in ansible-core, use the ansible.builtin. identifier, for example ansible.builtin.debug.

If your examples use boolean options, use true/false values. Since the documentation generates boolean values as true/false, having the examples use these values as well makes the module documentation more consistent.

If your module returns facts that are often needed, consider adding an example of how to use them.

Right after the EXAMPLES block comes the RETURN block. This section documents the information the module returns for use by other modules.

If your module does not return anything (apart from the standard returns made by ansible-core), specify it as RETURN = r''' # ''' Otherwise, for each value returned, provide the following fields. All the fields are required unless specified otherwise:

Name of the returned field.

Detailed description of what this value represents. Capitalized and with a trailing dot. You can use Ansible markup in this field.

When this value is returned, such as always, changed or success. This is a string and can contain any human-readable content.

If type='list', specifies the data type of the list’s elements.

One or more examples.

Only needed if this return was extended after initial module release, in other words, this is greater than the top (module) level version_added field. This is a string, and not a float, for example, version_added: '2.3'.

Optional. To describe nested return values, set type: dict, or type: list/elements: dict, or if you really have to, type: complex, and repeat the elements above for each sub-field.

Here are two example RETURN sections, one with three simple fields and one with a complex nested field:

Immediately after the RETURN block, add the Python imports. All modules must use Python imports in the form:

The use of “wildcard” imports such as from module_utils.basic import * is no longer allowed.

Why don’t the imports go first?

Since the DOCUMENTATION, EXAMPLES, and RETURN blocks are essentially extra docstrings for the file and are not used by the module code itself, the import statements are placed after these special variables. Positioning the imports closer to the functional code helps consolidate related elements, improving readability, debugging, and overall comprehension.

Before committing your module documentation, please test it on the command line and as HTML as described on the Testing plugin documentation page.

To test documentation in collections, please see Build a docsite with antsibull-docs.

**Examples:**

Example 1 (unknown):
```unknown
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
```

Example 2 (unknown):
```unknown
# Copyright: Contributors to the Ansible project
```

Example 3 (unknown):
```unknown
seealso:

# Reference by module name
- module: cisco.aci.aci_tenant

# Reference by module name, including description
- module: cisco.aci.aci_tenant
  description: ACI module to create tenants on a Cisco ACI fabric.

# Reference by plugin name
- plugin: ansible.builtin.file
  plugin_type: lookup

# Reference by plugin name, including description
- plugin: ansible.builtin.file
  plugin_type: lookup
  description: You can use the ansible.builtin.file lookup to read files on the control node.

# Reference by rST documentation anchor
- ref: aci_guide
  description: Detailed information on how to manage your ACI infrastructure using Ansible.

# Reference by rST documentation anchor (with custom title)
- ref: The official Ansible ACI guide <aci_guide>
  description: Detailed information on how to manage your ACI infrastructure using Ansible.

# Reference by Internet resource
- name: APIC Management Information Model reference
  description: Complete reference of the APIC object model.
  link: https://developer.cisco.com/docs/apic-mim-ref/
```

Example 4 (unknown):
```unknown
class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
    options:
      # options here
    '''

    # Additional section
    OTHER = r'''
    options:
      # other options here
    '''
```

---

## Docs fragments — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/docs_fragment.html

**Contents:**
- Docs fragments
- Enabling docs fragments
- Using docs fragments

Enabling docs fragments

Docs fragments allow you to document common parameters of multiple plugins or modules in a single place.

You can add a custom docs fragment by dropping it into a doc_fragments directory adjacent to your collection or role, just like any other plugin.

Only collection developers and maintainers use docs fragments. For more information on using docs fragments, see Documentation fragments or Using documentation fragments in collections.

An introduction to creating Ansible modules

A guide to creating Ansible collections

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Vars plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/vars.html

**Contents:**
- Vars plugins
- Enabling vars plugins
- Using vars plugins
- Plugin list

Enabling vars plugins

Vars plugins inject additional variable data into Ansible runs that did not come from an inventory source, playbook, or command line. Playbook constructs like ‘host_vars’ and ‘group_vars’ work using vars plugins. For more details about variables in Ansible, see Using variables.

Vars plugins were partially implemented in Ansible 2.0 and rewritten to be fully implemented starting with Ansible 2.4.

The host_group_vars plugin shipped with Ansible enables reading variables from Assigning a variable to one machine: host variables and Assigning a variable to many machines: group variables.

You can activate a custom vars plugin by either dropping it into a vars_plugins directory adjacent to your play, inside a role, or by putting it in one of the directory sources configured in ansible.cfg. For a vars plugin to run during inventory build you cannot enable it in a play or role as these are not loaded until later. If they are only going to run at task execution, there are no limitations on where they are provided.

Most vars plugins are disabled by default. To enable a vars plugin, set vars_plugins_enabled in the defaults section of ansible.cfg or set the ANSIBLE_VARS_ENABLED environment variable to the list of vars plugins you want to execute. By default, the host_group_vars plugin shipped with Ansible is enabled.

Starting in Ansible 2.10, you can use vars plugins in collections. All vars plugins in collections must be explicitly enabled and must use the fully qualified collection name in the format namespace.collection_name.vars_plugin_name.

By default, vars plugins are used on demand automatically after they are enabled.

Starting in Ansible 2.10, vars plugins can be made to run at specific times. ansible-inventory does not use these settings, and always loads vars plugins.

The global setting RUN_VARS_PLUGINS can be set in ansible.cfg using run_vars_plugins in the defaults section or by the ANSIBLE_RUN_VARS_PLUGINS environment variable. The default option, demand, runs any enabled vars plugins relative to inventory sources whenever variables are demanded by tasks. You can use the option start to run any enabled vars plugins relative to inventory sources after importing that inventory source instead.

You can also control vars plugin execution on a per-plugin basis for vars plugins that support the stage option. To run the host_group_vars plugin after importing inventory you can add the following to ansible.cfg:

You can use ansible-doc -t vars -l to see the list of available vars plugins. Use ansible-doc -t vars <plugin name> to see plugin-specific documentation and examples.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
[defaults]
vars_plugins_enabled = host_group_vars,namespace.collection_name.vars_plugin_name
```

Example 2 (unknown):
```unknown
[vars_host_group_vars]
stage = inventory
```

---

## Creating a new collection — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_in_groups.html

**Contents:**
- Creating a new collection
- Before you start coding
- Naming conventions
- Speak to us
- Where to get support
- Required files
- New to Git or GitHub

Starting with Ansible 2.10, related modules should be developed in a collection. The Ansible Core team and community compiled these module development tips and tricks to help companies developing Ansible modules for their products and users developing Ansible modules for third-party products. See Developing collections for a more detailed description of the collections format and additional development guidelines.

Before you start coding

LICENSING REQUIREMENTS Ansible enforces the following licensing requirements:

A file in module_utils used only for a specific vendor’s hardware, provider, or service may be licensed under GPLv3+. Adding a new file under module_utils with GPLv3+ needs to be approved by the core team.

All other module_utils must be licensed under BSD, so GPL-licensed third-party and Galaxy modules can use them.

If there’s doubt about the appropriate license for a file in module_utils, the Ansible Core Team will decide during an Ansible Core Community Meeting.

All other files shipped with Ansible, including all modules, must be licensed under the GPL license (GPLv3 or later).

Existing license requirements still apply to content in ansible/ansible (ansible-core).

Content that was previously in ansible/ansible or a collection and has moved to a new collection must retain the license it had in its prior repository.

Copyright entries by previous committers must also be kept in any moved files.

This list of prerequisites is designed to help ensure that you develop high-quality modules that work well with ansible-core and provide a seamless user experience.

Read though all the pages linked off Developing modules; paying particular focus to the Contributing your module to an existing Ansible collection.

We encourage PEP 8 compliance. See pep8 for more information.

We encourage supporting Python 2.6+ and Python 3.5+.

Look at Ansible Galaxy and review the naming conventions in your functional area (such as cloud, networking, databases).

With great power comes great responsibility: Ansible collection maintainers have a duty to help keep content up to date and release collections they are responsible for regularly. As with all successful community projects, collection maintainers should keep a watchful eye for reported issues and contributions.

We strongly recommend unit and/or integration tests. Unit tests are especially valuable when external resources (such as cloud or network devices) are required. For more information see Testing Ansible.

Fully Qualified Collection Names (FQCNs) for plugins and modules include three elements:

the Galaxy namespace, which generally represents the company or group

the collection name, which generally represents the product or OS

words separated with an underscore (_) character

singular, rather than plural, for example, command not commands

For example, community.mongodb.mongodb_linux or cisco.meraki.meraki_device.

It is convenient if the organization and repository names on GitHub (or elsewhere) match your namespace and collection names on Ansible Galaxy, but it is not required. The plugin names you select, however, are always the same in your code repository and in your collection artifact on Galaxy.

Circulating your ideas before coding helps you adopt good practices and avoid common mistakes. After reading the “Before you start coding” section you should have a reasonable idea of the structure of your modules. Write a list of your proposed plugin and/or module names, with a short description of what each one does. Circulate that list on the Ansible Forum so the Ansible community can review your ideas for consistency and familiarity. Names and functionality that are consistent, predictable, and familiar make your collection easier to use.

Ansible has a thriving and knowledgeable community of module developers that is a great resource for getting your questions answered. Visit the Ansible communication guide for details.

Your collection should include the following files to be usable:

an __init__.py file - An empty file to initialize namespace and allow Python to import the files. Required

at least one plugin, for example, /plugins/modules/$your_first_module.py. Required

if needed, one or more /plugins/doc_fragments/$topic.py files - Code documentation, such as details regarding common arguments. Optional

if needed, one or more /plugins/module_utils/$topic.py files - Code shared between more than one module, such as common arguments. Optional

When you have these files ready, review the Contributing your module to an existing Ansible collection again. If you are creating a new collection, you are responsible for all procedures related to your repository, including setting rules for contributions, finding reviewers, and testing and maintaining the code in your collection.

We realize this may be your first use of Git or GitHub. The following guides may be of use:

How to create a fork of ansible/ansible

How to sync (update) your fork

How to create a Pull Request (PR)

---

## Callback plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/callback.html

**Contents:**
- Callback plugins
- Example callback plugins
- Enabling callback plugins
- Setting a callback plugin for ansible-playbook
- Setting a callback plugin for ad hoc commands
- Types of callback plugins
- Plugin list

Example callback plugins

Enabling callback plugins

Setting a callback plugin for ansible-playbook

Setting a callback plugin for ad hoc commands

Types of callback plugins

Callback plugins enable adding new behaviors to Ansible when responding to events. By default, callback plugins control most of the output you see when running the command line programs, but can also be used to add additional output, integrate with other tools and marshal the events to a storage backend. If necessary, you can create custom callback plugins.

The log_plays callback is an example of how to record playbook events to a log file, and the mail callback sends email on playbook failures.

The say callback responds with a computer-synthesized speech in relation to playbook events.

You can activate a custom callback, depending on it’s NEEDS_ENABLED property, by either dropping it into one of the callback directory sources configured in ansible.cfg or in a collection and referencing it in configuration by FQCN.

Plugins are loaded in alphanumeric order. For example, a plugin implemented in a file named 1_first.py would run before a plugin file named 2_second.py.

Most callbacks shipped with Ansible are disabled by default and need to be enabled in your ansible.cfg file in order to function. For example:

You can only have one plugin be the main manager of your console output. If you want to replace the default, you should define CALLBACK_TYPE = stdout in the subclass and then configure the stdout plugin in ansible.cfg. For example:

or for my custom callback:

This only affects ansible-playbook by default.

The ansible ad hoc command specifically uses a different callback plugin for stdout, so there is an extra setting in Ansible Configuration Settings you need to add to use the stdout callback defined above:

You can also set this as an environment variable:

There are three types of callback plugins:

These plugins handle the main console output. Only one can be active. They always get the event first; the rest of the callbacks get the event in the order they are configured.

Aggregate callbacks can add additional console output next to a stdout callback. This can be aggregate information at the end of a playbook run, additional per-task output, or anything else.

Notification callbacks inform other applications, services, or systems. This can be anything from logging to databases, informing on errors in Instant Messaging applications, or sending emails when a server is unreachable.

You can use ansible-doc -t callback -l to see the list of available plugins. Use ansible-doc -t callback <plugin name> to see plugin-specific documentation and examples.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
#callbacks_enabled = timer, mail, profile_roles, collection_namespace.collection_name.custom_callback
```

Example 2 (unknown):
```unknown
stdout_callback = dense
```

Example 3 (unknown):
```unknown
stdout_callback = mycallback
```

Example 4 (unknown):
```unknown
[defaults]
bin_ansible_callbacks=True
```

---

## Index of all Lookup Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_lookup.html

**Contents:**
- Index of all Lookup Plugins
- ansible.builtin

ansible.builtin.config – Display the ‘resolved’ Ansible option values.

ansible.builtin.csvfile – read data from a TSV or CSV file

ansible.builtin.dict – returns key/value pair items from dictionaries

ansible.builtin.env – Read the value of environment variables

ansible.builtin.file – read file contents

ansible.builtin.fileglob – list files matching a pattern

ansible.builtin.first_found – return first file found from list

ansible.builtin.indexed_items – rewrites lists to return ‘indexed items’

ansible.builtin.ini – read data from an ini file

ansible.builtin.inventory_hostnames – list of inventory hosts matching a host pattern

ansible.builtin.items – list of items

ansible.builtin.lines – read lines from command

ansible.builtin.list – simply returns what it is given.

ansible.builtin.nested – composes a list with nested elements of other lists

ansible.builtin.password – retrieve or generate a random password, stored in a file

ansible.builtin.pipe – read output from a command

ansible.builtin.random_choice – return random element from list

ansible.builtin.sequence – generate a list based on a number sequence

ansible.builtin.subelements – traverse nested key from a list of dictionaries

ansible.builtin.template – retrieve contents of file after templating with Jinja2

ansible.builtin.together – merges lists into synchronized list

ansible.builtin.unvault – read vaulted file(s) contents

ansible.builtin.url – return contents from URL

ansible.builtin.varnames – Lookup matching variable names

ansible.builtin.vars – Lookup templated value of variables

---

## The Ansible Development Cycle — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/development_process.html

**Contents:**
- The Ansible Development Cycle
- Macro development: ansible-core roadmaps, releases, and projects
- Micro development: the lifecycle of a PR
- Making your PR merge-worthy
  - Creating changelog fragments
    - Creating a changelog fragment
    - Changelog fragment entry format
    - Changelog fragment entry format for new playbooks
- Backporting merged PRs in ansible-core

Ansible developers (including community contributors) add new features, fix bugs, and update code in many different repositories. The ansible/ansible repository contains the code for basic features and functions, such as copying module code to managed nodes. This code is also known as ansible-core. Other repositories contain plugins and modules that enable Ansible to execute specific tasks, like adding a user to a particular database or configuring a particular network device. These repositories contain the source code for collections.

Development on ansible-core occurs on two levels. At the macro level, the ansible-core developers and maintainers plan releases and track progress with roadmaps and projects. At the micro level, each PR has its own lifecycle.

Development on collections also occurs at the macro and micro levels. Each collection has its own macro development cycle. For more information on the collections development cycle, see Contributing to Ansible-maintained Collections. The micro-level lifecycle of a PR is similar in collections and in ansible-core.

Macro development: ansible-core roadmaps, releases, and projects

Micro development: the lifecycle of a PR

Making your PR merge-worthy

Creating changelog fragments

Creating a changelog fragment

Changelog fragment entry format

Changelog fragment entry format for new playbooks

Backporting merged PRs in ansible-core

If you want to follow the conversation about what features will be added to ansible-core for upcoming releases and what bugs are being fixed, you can watch these resources:

the Ansible Release Schedule

the ansible-core project branches and tags

the 2.19 release project

If you want to contribute a feature or fix a bug in ansible-core or in a collection, you must open a pull request (“PR” for short). GitHub provides a great overview of how the pull request process works in general. The ultimate goal of any pull request is to get merged and become part of a collection or ansible-core. Here’s an overview of the PR lifecycle:

Contributor opens a PR (always against the devel branch)

ansible-core uses Ansibot to triage the PR. Some collection repositories use Ansibullbot to triage the PR. For most collections, this is done manually or by other means.

Azure Pipelines runs the test suite

Developers, maintainers, community review the PR

Contributor addresses any feedback from reviewers

Developers, maintainers, community re-review

PR backported to one or more stable-X.Y branches (optional, bugfixes only)

We do not merge every PR. Here are some tips for making your PR useful, attractive, and merge-worthy.

Changelogs help users and developers keep up with changes to ansible-core and Ansible collections. Ansible and many collections build changelogs for each release from fragments. For ansible-core and collections using this model, you must add a changelog fragment to any PR that changes functionality or fixes a bug.

You do not need a changelog fragment for PRs that:

add new modules and plugins, because Ansible tooling does that automatically;

contain only documentation changes.

Some collections require a changelog fragment for every pull request. They use the trivial: section for entries mentioned above that will be skipped when building a release changelog.

Every bugfix PR must have a changelog fragment. The only exception are fixes to a change that has not yet been included in a release.

Every feature PR must have a changelog fragment.

New modules and plugins (including jinja2 filter and test plugins) must have version_added entries set correctly in their documentation, and do not need a changelog fragment. The tooling detects new modules and plugins by their version_added values and announces them in the next release’s changelog automatically.

We build short summary changelogs for minor releases as well as for major releases. If you backport a bugfix, include a changelog fragment with the backport PR.

A basic changelog fragment is a .yaml or .yml file placed in the changelogs/fragments/ directory. Each file contains a yaml dict with keys like bugfixes or major_changes followed by a list of changelog entries of bugfixes or features. Each changelog entry is rst embedded inside of the yaml file which means that certain constructs would need to be escaped so they can be interpreted by rst and not by yaml (or escaped for both yaml and rst if you prefer). Each PR must use a new fragment file rather than adding to an existing one, so we can trace the change back to the PR that introduced it.

PRs which add a new module or plugin do not necessarily need a changelog fragment. See the previous section Creating changelog fragments. Also see the next section Changelog fragment entry format for the precise format changelog fragments should have.

To create a changelog entry, create a new file with a unique name in the changelogs/fragments/ directory of the corresponding repository. The file name should include the PR number and a description of the change. It must end with the file extension .yaml or .yml. For example: 40696-user-backup-shadow-file.yaml

A single changelog fragment may contain multiple sections but most will only contain one section. The toplevel keys (bugfixes, major_changes, and so on) are defined in the config file for our release note tool. Here are the valid sections and a description of each:

MUST include changes that break existing playbooks or roles. This includes any change to existing behavior that forces users to update tasks. Breaking changes means the user MUST make a change when they update. Breaking changes MUST only happen in a major release of the collection. Write in present tense and clearly describe the new behavior that the end user must now follow. Displayed in both the changelogs and the Porting Guides.

Major changes to ansible-core or a collection. SHOULD NOT include individual module or plugin changes. MUST include non-breaking changes that impact all or most of a collection (for example, updates to support a new SDK version across the collection). Major changes mean the user can CHOOSE to make a change when they update but do not have to. Could be used to announce an important upcoming EOL or breaking change in a future release. (ideally 6 months in advance, if known. See this example). Write in present tense and describe what is new. Optionally, include a ‘Previously…” sentence to help the user identify where old behavior should now change. Displayed in both the changelogs and the Porting Guides.

Minor changes to ansible-core, modules, or plugins. This includes new parameters added to modules, or non-breaking behavior changes to existing parameters, such as adding additional values to choices[]. Minor changes are enhancements, not bug fixes. Write in present tense.

Features that have been deprecated and are scheduled for removal in a future release. Use past tense and include an alternative, where available for what is being deprecated.. Displayed in both the changelogs and the Porting Guides.

Features that were previously deprecated and are now removed. Use past tense and include an alternative, where available for what is being deprecated. Displayed in both the changelogs and the Porting Guides.

Fixes that address CVEs or resolve security concerns. MUST use security_fixes for any CVEs. Use present tense. Include links to CVE information.

Fixes that resolve issues. SHOULD not be used for minor enhancements (use minor_change instead). Use past tense to describe the problem and present tense to describe the fix.

Known issues that are currently not fixed or will not be fixed. Use present tense and where available, use imperative tense for a workaround.

Each changelog entry must contain a link to its issue between parentheses at the end. If there is no corresponding issue, the entry must contain a link to the PR itself.

Most changelog entries are bugfixes or minor_changes. The changelog tool also supports trivial, which are not listed in the actual changelog output but are used by collections repositories that require a changelog fragment for each PR.

When writing a changelog entry, use the following format:

The scope is usually a module or plugin name or group of modules or plugins, for example, lookup plugins. While module names can (and should) be mentioned directly (foo_module), plugin names should always be followed by the type (foo inventory plugin).

For changes that are not really scoped (for example, which affect a whole collection), use the following format:

Here are some examples:

You can find more example changelog fragments in the changelog directory for the 2.19 release.

After you have written the changelog fragment for your PR, commit the file and include it with the pull request.

While new modules, plugins, and roles are mentioned automatically in the generated changelog, playbooks are not. To make sure they are mentioned, a changelog fragment in a specific format is needed:

All ansible-core PRs must be merged to the devel branch first. After a pull request has been accepted and merged to the devel branch, the following instructions will help you create a pull request to backport the change to a previous stable branch.

We do not backport features.

These instructions assume that:

stable-2.19 is the targeted release branch for the backport

https://github.com/ansible/ansible.git is configured as a git remote named upstream. If you do not use a git remote named upstream, adjust the instructions accordingly.

https://github.com/<yourgithubaccount>/ansible.git is configured as a git remote named origin. If you do not use a git remote named origin, adjust the instructions accordingly.

Prepare your devel, stable, and feature branches:

Cherry pick the relevant commit SHA from the devel branch into your feature branch, handling merge conflicts as necessary:

Add a changelog fragment for the change, and commit it.

Push your feature branch to your fork on GitHub:

Submit the pull request for backport/2.19/[PR_NUMBER_FROM_DEVEL] against the stable-2.19 branch

The Release Manager will decide whether to merge the backport PR before the next minor release. There isn’t any need to follow up. Just ensure that the automated tests (CI) are green.

The branch name backport/2.19/[PR_NUMBER_FROM_DEVEL] is somewhat arbitrary but conveys meaning about the purpose of the branch. This branch name format is not required, but it can be helpful, especially when making multiple backport PRs for multiple stable branches.

If you prefer, you can use CPython’s cherry-picker tool (pip install --user 'cherry-picker >= 1.3.2') to backport commits from devel to stable branches in Ansible. Take a look at the cherry-picker documentation for details on installing, configuring, and using it.

**Examples:**

Example 1 (unknown):
```unknown
breaking_changes:
  - ansible-test - automatic installation of requirements for cloud test plugins no longer occurs. The affected test plugins are ``aws``, ``azure``, ``cs``, ``hcloud``, ``nios``, ``opennebula``, ``openshift`` and ``vcenter``. Collections should instead use one of the supported integration test requirements files, such as the ``tests/integration/requirements.txt`` file (https://github.com/ansible/ansible/pull/75605).
```

Example 2 (unknown):
```unknown
major_changes:
  - ansible-test - all cloud plugins which use containers can now be used with all POSIX and Windows hosts. Previously the plugins did not work with Windows at all, and support for hosts created with the ``--remote`` option was inconsistent (https://github.com/ansible/ansible/pull/74216).
```

Example 3 (unknown):
```unknown
minor_changes:
  - lineinfile - add warning when using an empty regexp (https://github.com/ansible/ansible/issues/29443).
```

Example 4 (unknown):
```unknown
deprecated_features:
  - include action - is deprecated in favor of ``include_tasks``, ``import_tasks`` and ``import_playbook`` (https://github.com/ansible/ansible/pull/71262).
```

---

## Index of all Aggregate Callback Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/callback_index_aggregate.html

**Contents:**
- Index of all Aggregate Callback Plugins
- ansible.builtin

See Index of all Callback Plugins for the list of all callback plugins.

ansible.builtin.junit – write playbook output to a JUnit file.

---

## Httpapi plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/httpapi.html

**Contents:**
- Httpapi plugins
- Adding httpapi plugins
- Using httpapi plugins
- Viewing httpapi plugins

Adding httpapi plugins

Using httpapi plugins

Viewing httpapi plugins

Httpapi plugins tell Ansible how to interact with a remote device’s HTTP-based API and execute tasks on the device.

Each plugin represents a particular dialect of API. Some are platform-specific (Arista eAPI, Cisco NXAPI), while others might be usable on a variety of platforms (RESTCONF). Ansible loads the appropriate httpapi plugin automatically based on the ansible_network_os variable.

You can extend Ansible to support other APIs by dropping a custom plugin into the httpapi_plugins directory. See Developing httpapi plugins for details.

The httpapi plugin to use is determined automatically from the ansible_network_os variable.

Most httpapi plugins can operate without configuration. Additional options may be defined by each plugin.

Plugins are self-documenting. Each plugin should document its configuration options.

The following sample playbook shows the httpapi plugin for an Arista network device, assuming an inventory variable set as ansible_network_os=eos for the httpapi plugin to trigger off:

See the full working example on GitHub.

These plugins have migrated to collections on Ansible Galaxy. If you installed Ansible version 2.10 or later using pip, you have access to several httpapi plugins. You can use ansible-doc -t httpapi -l to see the list of available plugins. Use ansible-doc -t httpapi <plugin name> to see plugin-specific documentation and examples.

An overview of using Ansible to automate networking devices.

How to develop network modules.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
- hosts: leaf01
  connection: httpapi
  gather_facts: false
  tasks:

    - name: type a simple arista command
      eos_command:
        commands:
          - show version | json
      register: command_output

    - name: print command output to terminal window
      debug:
        var: command_output.stdout[0]["version"]
```

---

## Filter plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/filter.html

**Contents:**
- Filter plugins
- Enabling filter plugins
- Using filter plugins
- Plugin list

Enabling filter plugins

Filter plugins manipulate data. With the right filter, you can extract a particular value, transform data types and formats, perform mathematical calculations, split and concatenate strings, insert dates and times, and do much more. Ansible uses the standard filters shipped with Jinja2 and adds some specialized filter plugins. You can create custom Ansible filters as plugins.

You can add a custom filter plugin by dropping it into a filter_plugins directory adjacent to your play, inside a role, or by putting it in one of the filter plugin directory sources configured in ansible.cfg.

You can use filters anywhere you can use templating in Ansible: in a play, in variables file, or a Jinja2 template for the template module. For more information on using filter plugins, see Using filters to manipulate data. Filters can return any type of data, but if you want to always return a boolean, (true or false) you should be looking at a test instead.

Filters are the preferred way to manipulate data in Ansible, you can identify a filter because it is normally preceded by a |, with the expression on the left of it being the first input of the filter. Additional parameters may be passed into the filter itself as you would to most programming functions. These parameters can be either positional (passed in order) or named (passed as key=value pairs). When passing both types, positional arguments should go first.

In the documentation, filters will always have a C(_input) option that corresponds to the expression to the left of c(|). A C(positional:) field in the documentation will show which options are positional and in which order they are required.

You can use ansible-doc -t filter -l to see the list of available plugins. Use ansible-doc -t filter <plugin name> to see plugin-specific documentation and examples.

An introduction to playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
vars:
   yaml_string: "{{ some_variable|to_yaml }}"
```

Example 2 (unknown):
```unknown
passing_positional: "{{ (x == 32) | ternary('x is 32', 'x is not 32') }}"
passing_extra_named_parameters: "{{ some_variable | to_yaml(indent=8, width=1337) }}"
passing_both: "{{ some_variable | ternary('true value', 'false value', none_val='NULL') }}"
```

---

## Developing modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_modules_general.html

**Contents:**
- Developing modules
- Preparing an environment for developing Ansible modules
- Creating a standalone module
- Creating a module in a collection
- Creating an info or a facts module
- Verifying your module code
  - Verifying your module code locally
  - Verifying your module code in a playbook
- Testing your newly-created module
- Contributing back to Ansible

A module is a reusable, standalone script that Ansible runs on your behalf, either locally or remotely. Modules interact with your local machine, an API, or a remote system to perform specific tasks like changing a database password or spinning up a cloud instance. Each module can be used by the Ansible API, or by the ansible or ansible-playbook programs. A module provides a defined interface, accepts arguments, and returns information to Ansible by printing a JSON string to stdout before exiting.

If you need functionality that is not available in any of the thousands of Ansible modules found in collections, you can easily write your own custom module. When you write a module for local use, you can choose any programming language and follow your own rules. Use this topic to learn how to create an Ansible module in Python. After you create a module, you must add it locally to the appropriate directory so that Ansible can find and execute it. For details about adding a module locally, see Adding modules and plugins locally.

If you are developing a module in a collection, see those documents instead.

Preparing an environment for developing Ansible modules

Creating a standalone module

Creating a module in a collection

Creating an info or a facts module

Verifying your module code

Verifying your module code locally

Verifying your module code in a playbook

Testing your newly-created module

Contributing back to Ansible

Communication and development support

You just need ansible-core installed to test the module. Modules can be written in any language, but most of the following guide is assuming you are using Python. Modules for inclusion in Ansible itself must be Python or Powershell.

One advantage of using Python or Powershell for your custom modules is being able to use the module_utils common code that does a lot of the heavy lifting for argument processing, logging and response writing, among other things.

It is highly recommended that you use a venv or virtualenv for Python development.

To create a standalone module:

Create a library directory in your workspace. Your test play should live in the same directory.

Create your new module file: $ touch library/my_test.py. Or just open/create it with your editor of choice.

Paste the content below into your new module file. It includes the required Ansible format and documentation, a simple argument spec for declaring the module options, and some example code.

Modify and extend the code to do what you want your new module to do. See the programming tips and Python 3 compatibility pages for pointers on writing clean and concise module code.

To create a new module in an existing collection called my_namespace.my_collection:

Create your new module file: $ touch <PATH_TO_COLLECTION>/ansible_collections/my_namespace/my_collection/plugins/modules/my_test.py. Or just create it with your editor of choice.

Paste the content below into your new module file. It includes the required Ansible format and documentation, a simple argument spec for declaring the module options, and some example code.

Modify and extend the code to do what you want your new module to do. See the programming tips and Python 3 compatibility pages for pointers on writing clean and concise module code.

Ansible gathers information about the target machines using facts modules, and gathers information on other objects or files using info modules. If you find yourself trying to add state: info or state: list to an existing module, that is often a sign that a new dedicated _facts or _info module is needed.

In Ansible 2.8 and onwards, we have two type of information modules, they are *_info and *_facts.

If a module is named <something>_facts, it should be because its main purpose is returning ansible_facts. Do not name modules that do not do this with _facts. Only use ansible_facts for information that is specific to the host machine, for example network interfaces and their configuration, which operating system and which programs are installed.

Modules that query/return general information (and not ansible_facts) should be named _info. General information is non-host specific information, for example information on online/cloud services (you can access different accounts for the same online service from the same host), or information on VMs and containers accessible from the machine, or information on individual files or programs.

Info and facts modules, are just like any other Ansible Module, with a few minor requirements:

They MUST be named <something>_info or <something>_facts, where <something> is singular.

Info *_info modules MUST return in the form of the result dictionary so other modules can access them.

Fact *_facts modules MUST return in the ansible_facts field of the result dictionary so other modules can access them.

They MUST support check_mode.

They MUST NOT make any changes to the system.

They MUST document the return fields and examples.

You can add your facts into ansible_facts field of the result as follows:

The rest is just like creating a normal module.

After you modify the sample code above to do what you want, you can try out your module. Our debugging tips will help if you run into bugs as you verify your module code.

The simplest way is to use ansible adhoc command:

If your module does not need to target a remote host, you can quickly and easily exercise your code locally like this:

For a module developed in an existing collection called my_namespace.my_collection (as mentioned above):

If you use pdb, print(), or some other method of local debugging for faster iteration, you can avoid going through Ansible by creating an arguments file, which is a basic JSON config file that passes parameters to your module so that you can run it. Name the arguments file /tmp/args.json and add the following content:

Then the module can be tested locally and directly. This skips the packing steps and uses module_utils files directly:

You might also need to add your collection’s path to the Python path. This tells Python to look for additional module_utils code in the given path. You can run the module code, as in the following example:

It should return output like this:

You can easily run a full test by including it in a playbook, as long as the library directory is in the same directory as the play:

Create a playbook in any directory: $ touch testmod.yml

Add the following to the new playbook file:

Run the playbook and analyze the output: $ ansible-playbook ./testmod.yml

Review our testing section for more detailed information, including instructions for testing module documentation, adding integration tests, and more.

If contributing to Ansible, every new module and plugin should have integration tests, even if the tests cannot be run on Ansible CI infrastructure. In this case, the tests should be marked with the unsupported alias in aliases file.

If you would like to contribute to ansible-core by adding a new feature or fixing a bug, create a fork of the ansible/ansible repository and develop against a new feature branch using the devel branch as a starting point. When you have a good working code change, you can submit a pull request to the Ansible repository by selecting your feature branch as a source and the Ansible devel branch as a target.

If you want to contribute a module to an Ansible collection, review our submission checklist, programming tips, and strategy for maintaining Python 2 and Python 3 compatibility, as well as information about testing before you open a pull request.

The Community Guide covers how to open a pull request and what happens next.

Visit the Ansible communication guide for information on how to join the conversation.

Thank you to Thomas Stringer (@trstringer) for contributing source material for this topic.

**Examples:**

Example 1 (python):
```python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <[email protected]>
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
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

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

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
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

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```

Example 2 (unknown):
```unknown
module.exit_json(changed=False, ansible_facts=dict(my_new_fact=value_of_fact))
```

Example 3 (unknown):
```unknown
ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' remotehost
```

Example 4 (unknown):
```unknown
ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' localhost
```

---

## Index of all Become Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_become.html

**Contents:**
- Index of all Become Plugins
- ansible.builtin

ansible.builtin.runas – Run As user

ansible.builtin.su – Substitute User

ansible.builtin.sudo – Substitute User DO

---

## Adding modules and plugins locally — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_locally.html

**Contents:**
- Adding modules and plugins locally
- Modules and plugins: what is the difference?
- Adding modules and plugins in collections
- Adding a module or plugin outside of a collection
  - Adding standalone local modules for all playbooks and roles
  - Adding standalone local modules for selected playbooks or a single role
- Adding a non-module plugin locally outside of a collection
  - Adding local non-module plugins for all playbooks and roles
  - Adding standalone local plugins for selected playbooks or a single role
- Using ansible.legacy to access custom versions of an ansible.builtin module

You can extend Ansible by adding custom modules or plugins. You can create them from scratch or copy existing ones for local use. You can store a local module or plugin on your Ansible control node and share it with your team or organization. You can also share plugins and modules by including them in a collection, then publishing the collection on Ansible Galaxy.

If you are using a local module or plugin but Ansible cannot find it, this page is all you need.

If you want to create a plugin or a module, see Developing plugins, Developing modules and Developing collections.

Extending Ansible with local modules and plugins offers shortcuts such as:

You can copy other people’s modules and plugins.

When writing a new module, you can choose any programming language you like.

You do not have to clone any repositories.

You do not have to open a pull request.

You do not have to add tests (though we recommend that you do!).

Modules and plugins: what is the difference?

Adding modules and plugins in collections

Adding a module or plugin outside of a collection

Adding standalone local modules for all playbooks and roles

Adding standalone local modules for selected playbooks or a single role

Adding a non-module plugin locally outside of a collection

Adding local non-module plugins for all playbooks and roles

Adding standalone local plugins for selected playbooks or a single role

Using ansible.legacy to access custom versions of an ansible.builtin module

If you are looking to add functionality to Ansible, you might wonder whether you need a module or a plugin. Here is a quick overview to help you understand what you need:

Plugins extend Ansible’s core functionality. Most plugin types execute on the control node within the /usr/bin/ansible process. Plugins offer options and extensions for the core features of Ansible: transforming data, logging output, connecting to inventory, and more.

Modules are a type of plugin that execute automation tasks on a ‘target’ (usually a remote system). Modules work as standalone scripts that Ansible executes in their own process outside of the control node. Modules interface with Ansible mostly with JSON, accepting arguments and returning information by printing a JSON string to stdout before exiting. Unlike the other plugins (which must be written in Python), modules can be written in any language; although Ansible provides modules in Python and Powershell only.

You can add modules and plugins by creating a collection. With a collection, you can use custom modules and plugins in any playbook or role. You can share your collection easily at any time through Ansible Galaxy.

The rest of this page describes other methods of using local, standalone modules or plugins.

You can configure Ansible to load standalone local modules or plugins in specific locations and make them available to all playbooks and roles (using configured paths). Alternatively, you can make a non-collection local module or plugin available only to certain playbooks or roles (with adjacent paths).

To load standalone local modules automatically and make them available to all playbooks and roles, use the DEFAULT_MODULE_PATH configuration setting or the ANSIBLE_LIBRARY environment variable. The configuration setting and environment variable take a colon-separated list, similar to $PATH. You have two options:

Add your standalone local module to one of the default configured locations. See the DEFAULT_MODULE_PATH configuration setting for details. Default locations may change without notice.

the ANSIBLE_LIBRARY environment variable

the DEFAULT_MODULE_PATH configuration setting

To view your current configuration settings for modules:

After you save your module file in one of these locations, Ansible loads it and you can use it in any local task, playbook, or role.

To confirm that my_local_module is available:

type ansible localhost -m my_local_module to see the output for that module, or

type ansible-doc -t module my_local_module to see the documentation for that module

This applies to all plugin types but requires specific configuration and/or adjacent directories for each plugin type, see below.

The ansible-doc command can parse module documentation from modules written in Python or an adjacent YAML file. If you have a module written in a programming language other than Python, you should write the documentation in a Python or YAML file adjacent to the module file. Adjacent YAML documentation files

Ansible automatically loads all executable files from certain directories adjacent to your playbook or role as modules. Standalone modules in these locations are available only to the specific playbook, playbooks, or role in the parent directory.

To use a standalone module only in a selected playbook or playbooks, store the module in a subdirectory called library in the directory that contains the playbook or playbooks.

To use a standalone module only in a single role, store the module in a subdirectory called library within that role.

This applies to all plugin types but requires specific configuration and/or adjacent directories for each plugin type, see below.

Roles contained in collections cannot contain any modules or other plugins. All plugins in a collection must live in the collection plugins directory tree. All plugins in that tree are accessible to all roles in the collection. If you are developing new modules, we recommend distributing them in collections, not in roles.

You can configure Ansible to load standalone local plugins in a specified location or locations and make them available to all playbooks and roles. Alternatively, you can make a standalone local plugin available only to specific playbooks or roles.

Although modules are plugins, the naming patterns for directory names and environment variables that apply to other plugin types do not apply to modules. See Adding a module or plugin outside of a collection.

To load standalone local plugins automatically and make them available to all playbooks and roles, use the configuration setting or environment variable for the type of plugin you are adding. These configuration settings and environment variables take a colon-separated list, similar to $PATH. You have two options:

Add your local plugin to one of the default configured locations. See configuration settings for details on the correct configuration setting for the plugin type. Default locations may change without notice.

the relevant ANSIBLE_plugin_type_PLUGINS environment variable - for example, $ANSIBLE_INVENTORY_PLUGINS or $ANSIBLE_VARS_PLUGINS

the relevant plugin_type_PATH configuration setting, most of which begin with DEFAULT_ - for example, DEFAULT_CALLBACK_PLUGIN_PATH or DEFAULT_FILTER_PLUGIN_PATH or BECOME_PLUGIN_PATH

To view your current configuration settings for non-module plugins:

After your plugin file is added to one of these locations, Ansible loads it and you can use it in any local module, task, playbook, or role. For more information on environment variables and configuration settings, see Ansible Configuration Settings.

To confirm that plugins/plugin_type/my_local_plugin is available:

type ansible-doc -t <plugin_type> my_local_lookup_plugin to see the documentation for that plugin - for example, ansible-doc -t lookup my_local_lookup_plugin

The ansible-doc command works for most plugin types, but not for action, filter, or test plugins. See ansible-doc for more details.

Ansible automatically loads all plugins from certain directories adjacent to your playbook or role, loading each type of plugin separately from a directory named for the type of plugin. Standalone plugins in these locations are available only to the specific playbook, playbooks, or role in the parent directory.

To use a standalone plugin only in a selected playbook or playbooks, store the plugin in a subdirectory for the correct plugin_type (for example, callback_plugins or inventory_plugins) in the directory that contains the playbooks. These directories must use the _plugins suffix. For a full list of plugin types, see Working with plugins.

To use a standalone plugin only in a single role, store the plugin in a subdirectory for the correct plugin_type (for example, cache_plugins or strategy_plugins) within that role. When shipped as part of a role, the plugin is available as soon as the role is executed. These directories must use the _plugins suffix. For a full list of plugin types, see Working with plugins.

Roles contained in collections cannot contain any plugins. All plugins in a collection must live in the collection plugins directory tree. All plugins in that tree are accessible to all roles in the collection. If you are developing new plugins, we recommend distributing them in collections, not in roles.

Some plugin types are needed early during Ansible execution, such as callbacks, inventory, and cache. These plugin types cannot be loaded dynamically and must exist in configured paths or be referenced by FQCN in configuration.

If you need to override one of the ansible.builtin modules and are using FQCN, you need to use ansible.legacy as part of the fully-qualified collection name (FQCN). For example, if you had your own copy module, you would access it as ansible.legacy.copy. See Using ansible.legacy to access local custom modules from collections-based roles for details on how to use custom modules with roles within a collection.

**Examples:**

Example 1 (unknown):
```unknown
ansible-config dump |grep DEFAULT_MODULE_PATH
```

Example 2 (unknown):
```unknown
ansible-config dump |grep plugin_type_PATH
```

---

## Documenting collections — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_collections_documenting.html

**Contents:**
- Documenting collections
- Documenting modules and plugins
- Documenting roles
- Verifying your collection documentation
- Build a docsite with antsibull-docs

Documenting modules is thoroughly documented in Module format and documentation. Plugins can be documented the same way as modules, that is with DOCUMENTATION, EXAMPLES, and RETURN blocks.

To document a role, you have to add a role argument spec by creating a file meta/argument_specs.yml in your role. See Role argument validation for details. As an example, you can look at the argument specs file of the telekom_mms.icinga_director.ansible_icinga role on GitHub.

You can use antsibull-docs to lint your collection documentation. See Linting collection documentation. for details.

You can use antsibull-docs to build a Sphinx-based docsite for your collection:

Create your collection and make sure you can use it with ansible-core by adding it to your COLLECTIONS_PATHS.

Create a directory dest and run antsibull-docs sphinx-init --use-current --dest-dir dest namespace.name, where namespace.name is the name of your collection.

Go into dest and run pip install -r requirements.txt. You might want to create a venv and activate it first to avoid installing this globally.

Open build/html/index.html in a browser of your choice.

See antsibull-docs documentation for complete details.

If you want to add additional documentation to your collection next to the plugin, module, and role documentation, see docs directory.

---

## Ansible-base 2.10 Porting Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/porting_guides/porting_guide_base_2.10.html

**Contents:**
- Ansible-base 2.10 Porting Guide
- Playbook
- Command Line
- Deprecated
- Modules
  - Noteworthy module changes
- Plugins
  - Lookup plugin names case-sensitivity
  - Noteworthy plugin changes
  - Action plugins which execute modules should use fully-qualified module names

In preparation for the release of 2.10, many plugins and modules have migrated to Collections on Ansible Galaxy. For the current development status of Collections and FAQ see Ansible Collections Community Guide. We expect the 2.10 Porting Guide to change frequently up to the 2.10 release. Follow the conversations about collections on our various Communicating with the Ansible community channels for the latest information on the status of the devel branch.

This section discusses the behavioral changes between Ansible 2.9 and Ansible-base 2.10.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible-base.

We suggest you read this page along with the Ansible-base Changelog for 2.10 to understand what updates you may need to make.

Ansible-base is mainly of interest for developers and users who only want to use a small, controlled subset of the available collections. Regular users should install ansible.

The complete list of porting guides can be found at porting guides.

Ansible-base 2.10 Porting Guide

Noteworthy module changes

Lookup plugin names case-sensitivity

Noteworthy plugin changes

Action plugins which execute modules should use fully-qualified module names

Porting custom scripts

Fixed a bug on boolean keywords that made random strings return ‘False’, now they should return an error if they are not a proper boolean Example: diff: yes- was returning False.

A new fact, ansible_processor_nproc reflects the number of vcpus available to processes (falls back to the number of vcpus available to the scheduler).

The ansible-galaxy login command has been removed, as the underlying API it used for GitHub auth is being shut down. Publishing roles or collections to Galaxy through ansible-galaxy now requires that a Galaxy API token be passed to the CLI through a token file (default location ~/.ansible/galaxy_token) or (insecurely) through the --token argument to ansible-galaxy.

Windows Server 2008 and 2008 R2 will no longer be supported or tested in the next Ansible release, see Are Server 2008, 2008 R2 and Windows 7 supported?.

Links on this page may not point to the most recent versions of modules. We will update them when we can.

Version 2.10.0 of ansible-base changed the default mode of file-based tasks to 0o600 & ~umask when the user did not specify a mode parameter on file-based tasks. This was in response to a CVE report which we have reconsidered. As a result, the mode change has been reverted in 2.10.1, and mode will now default to 0o666 & ~umask as in previous versions of Ansible.

If you changed any tasks to specify less restrictive permissions while using 2.10.0, those changes will be unnecessary (but will do no harm) in 2.10.1.

To avoid the issue raised in CVE-2020-1736, specify a mode parameter in all file-based tasks that accept it.

dnf and yum - As of version 2.10.1, the dnf module (and yum action when it uses dnf) now correctly validates GPG signatures of packages (CVE-2020-14365). If you see an error such as Failed to validate GPG signature for [package name], please ensure that you have imported the correct GPG key for the DNF repository and/or package you are using. One way to do this is with the rpm_key module. Although we discourage it, in some cases it may be necessary to disable the GPG check. This can be done by explicitly adding disable_gpg_check: yes in your dnf or yum task.

Ansible modules created with add_file_common_args=True added a number of undocumented arguments which were mostly there to ease implementing certain action plugins. The undocumented arguments src, follow, force, content, backup, remote_src, regexp, delimiter, and directory_mode are now no longer added. Modules relying on these options to be added need to specify them by themselves.

Ansible no longer looks for Python modules in the current working directory (typically the remote_user’s home directory) when an Ansible module is run. This is to fix becoming an unprivileged user on OpenBSD and to mitigate any attack vector if the current working directory is writable by a malicious user. Install any Python modules needed to run the Ansible modules on the managed node in a system-wide location or in another directory which is in the remote_user’s $PYTHONPATH and readable by the become_user.

Prior to Ansible 2.10 lookup plugin names passed in as an argument to the lookup() function were treated as case-insensitive as opposed to lookups invoked through with_<lookup_name>. 2.10 brings consistency to lookup() and with_ to be both case-sensitive.

Cache plugins in collections can be used to cache data from inventory plugins. Previously, cache plugins in collections could only be used for fact caching.

Some undocumented arguments from FILE_COMMON_ARGUMENTS have been removed; plugins using these, in particular action plugins, need to be adjusted. The undocumented arguments which were removed are src, follow, force, content, backup, remote_src, regexp, delimiter, and directory_mode.

Action plugins that call modules should pass explicit, fully-qualified module names to _execute_module() whenever possible (eg, ansible.builtin.file rather than file). This ensures that the task’s collection search order is not consulted to resolve the module. Otherwise, a module from a collection earlier in the search path could be used when not intended.

---

## Cliconf plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/cliconf.html

**Contents:**
- Cliconf plugins
- Adding cliconf plugins
- Using cliconf plugins
- Viewing cliconf plugins

Adding cliconf plugins

Using cliconf plugins

Viewing cliconf plugins

Cliconf plugins are abstractions over the CLI interface to network devices. They provide a standard interface for Ansible to execute tasks on those network devices.

These plugins generally correspond one-to-one to network device platforms. Ansible loads the appropriate cliconf plugin automatically based on the ansible_network_os variable.

You can extend Ansible to support other network devices by dropping a custom plugin into the cliconf_plugins directory.

The cliconf plugin to use is determined automatically from the ansible_network_os variable. There should be no reason to override this functionality.

Most cliconf plugins can operate without configuration. A few have additional options that can be set to affect how tasks are translated into CLI commands.

Plugins are self-documenting. Each plugin should document its configuration options.

These plugins have migrated to collections on Ansible Galaxy. If you installed Ansible version 2.10 or later using pip, you have access to several cliconf plugins. You can use ansible-doc -t cliconf -l to see the list of available plugins. Use ansible-doc -t cliconf <plugin name> to see plugin-specific documentation and examples.

An overview of using Ansible to automate networking devices.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Unit Testing Ansible Modules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_units_modules.html

**Contents:**
- Unit Testing Ansible Modules
- Introduction
- What Are Unit Tests?
- Why Use Unit Tests?
- When To Use Unit Tests
  - Providing quick feedback
  - Ensuring correct use of external interfaces
  - Providing specific design tests
- How to unit test Ansible modules
  - Naming unit tests

Unit Testing Ansible Modules

When To Use Unit Tests

Providing quick feedback

Ensuring correct use of external interfaces

Providing specific design tests

How to unit test Ansible modules

Ensuring failure cases are visible with mock objects

Mocking of the actual module

API definition with unit test cases

Defining a module against an API specification

Defining a module to work against multiple API versions

Ansible special cases for unit testing

Module argument processing

Handling exit correctly

Running the main function

Handling calls to external executables

Restructuring modules to enable testing module set up and other processes

Traps for maintaining Python 2 compatibility

This document explains why, how and when you should use unit tests for Ansible modules. The document doesn’t apply to other parts of Ansible for which the recommendations are normally closer to the Python standard. There is basic documentation for Ansible unit tests in the developer guide Unit Tests. This document should be readable for a new Ansible module author. If you find it incomplete or confusing, please open a bug or ask for help on the Ansible Forum.

Ansible includes a set of unit tests in the test/units directory. These tests primarily cover the internals but can also cover Ansible modules. The structure of the unit tests matches the structure of the code base, so the tests that reside in the test/units/modules/ directory are organized by module groups.

Integration tests can be used for most modules, but there are situations where cases cannot be verified using integration tests. This means that Ansible unit test cases may extend beyond testing only minimal units and in some cases will include some level of functional testing.

Ansible unit tests have advantages and disadvantages. It is important to understand these. Advantages include:

Most unit tests are much faster than most Ansible integration tests. The complete suite of unit tests can be run regularly by a developer on their local system.

Unit tests can be run by developers who don’t have access to the system which the module is designed to work on, allowing a level of verification that changes to core functions haven’t broken module expectations.

Unit tests can easily substitute system functions allowing testing of software that would be impractical. For example, the sleep() function can be replaced and we check that a ten minute sleep was called without actually waiting ten minutes.

Unit tests are run on different Python versions. This allows us to ensure that the code behaves in the same way on different Python versions.

There are also some potential disadvantages of unit tests. Unit tests don’t normally directly test actual useful valuable features of software, instead just internal implementation

Unit tests that test the internal, non-visible features of software may make refactoring difficult if those internal features have to change (see also naming in How below)

Even if the internal feature is working correctly it is possible that there will be a problem between the internal code tested and the actual result delivered to the user

Normally the Ansible integration tests (which are written in Ansible YAML) provide better testing for most module functionality. If those tests already test a feature and perform well there may be little point in providing a unit test covering the same area as well.

There are a number of situations where unit tests are a better choice than integration tests. For example, testing things which are impossible, slow or very difficult to test with integration tests, such as:

Forcing rare / strange / random situations that can’t be forced, such as specific network failures and exceptions

Extensive testing of slow configuration APIs

Situations where the integration tests cannot be run as part of the main Ansible continuous integration running in Azure Pipelines.

A single step of the rds_instance test cases can take up to 20 minutes (the time to create an RDS instance in Amazon). The entire test run can last for well over an hour. All 16 of the unit tests complete execution in less than 2 seconds.

The time saving provided by being able to run the code in a unit test makes it worth creating a unit test when bug fixing a module, even if those tests do not often identify problems later. As a basic goal, every module should have at least one unit test which will give quick feedback in easy cases without having to wait for the integration tests to complete.

Unit tests can check the way in which external services are run to ensure that they match specifications or are as efficient as possible even when the final output will not be changed.

Package managers are often far more efficient when installing multiple packages at once rather than each package separately. The final result is the same: the packages are all installed, so the efficiency is difficult to verify through integration tests. By providing a mock package manager and verifying that it is called once, we can build a valuable test for module efficiency.

Another related use is in the situation where an API has versions which behave differently. A programmer working on a new version may change the module to work with the new API version and unintentionally break the old version. A test case which checks that the call happens properly for the old version can help avoid the problem. In this situation it is very important to include version numbering in the test case name (see Naming unit tests below).

By building a requirement for a particular part of the code and then coding to that requirement, unit tests _can_ sometimes improve the code and help future developers understand that code.

Unit tests that test internal implementation details of code, on the other hand, almost always do more harm than good. Testing that your packages to install are stored in a list would slow down and confuse a future developer who might need to change that list into a dictionary for efficiency. This problem can be reduced somewhat with clear test naming so that the future developer immediately knows to delete the test case, but it is often better to simply leave out the test case altogether and test for a real valuable feature of the code, such as installing all of the packages supplied as arguments to the module.

There are a number of techniques for unit testing modules. Beware that most modules without unit tests are structured in a way that makes testing quite difficult and can lead to very complicated tests which need more work than the code. Effectively using unit tests may lead you to restructure your code. This is often a good thing and leads to better code overall. Good restructuring can make your code clearer and easier to understand.

Unit tests should have logical names. If a developer working on the module being tested breaks the test case, it should be easy to figure what the unit test covers from the name. If a unit test is designed to verify compatibility with a specific software or API version then include the version in the name of the unit test.

As an example, test_v2_state_present_should_call_create_server_with_name() would be a good name, test_create_server() would not be.

Mock objects (from https://docs.python.org/3/library/unittest.mock.html) can be very useful in building unit tests for special / difficult cases, but they can also lead to complex and confusing coding situations. One good use for mocks would be in simulating an API. As for ‘six’, the ‘mock’ python package is bundled with Ansible (use import units.compat.mock).

Functions like module.fail_json() are normally expected to terminate execution. When you run with a mock module object this doesn’t happen since the mock always returns another mock from a function call. You can set up the mock to raise an exception as shown above, or you can assert that these functions have not been called in each test. For example:

This applies not only to calling the main module but almost any other function in a module which gets the module object.

The setup of an actual module is quite complex (see Passing Arguments below) and often isn’t needed for most functions which use a module. Instead you can use a mock object as the module and create any module attributes needed by the function you are testing. If you do this, beware that the module exit functions need special handling as mentioned above, either by throwing an exception or ensuring that they haven’t been called. For example:

API interaction is usually best tested with the function tests defined in Ansible’s integration testing section, which run against the actual API. There are several cases where the unit tests are likely to work better.

This case is especially important for modules interacting with web services, which provide an API that Ansible uses but which are beyond the control of the user.

By writing a custom emulation of the calls that return data from the API, we can ensure that only the features which are clearly defined in the specification of the API are present in the message. This means that we can check that we use the correct parameters and nothing else.

Example: in rds_instance unit tests a simple instance state is defined:

This is then used to create a list of states:

These states are then used as returns from a mock object to ensure that the await function waits through all of the states that would mean the RDS instance has not yet completed configuration:

By doing this we check that the await function will keep waiting through potentially unusual that it would be impossible to reliably trigger through the integration tests but which happen unpredictably in reality.

This case is especially important for modules interacting with many different versions of software; for example, package installation modules that might be expected to work with many different operating system versions.

By using previously stored data from various versions of an API we can ensure that the code is tested against the actual data which will be sent from that version of the system even when the version is very obscure and unlikely to be available during testing.

There are a number of special cases for unit testing the environment of an Ansible module. The most common are documented below, and suggestions for others can be found by looking at the source code of the existing unit tests or asking the community.

There are two problems with running the main function of a module:

Since the module is supposed to accept arguments on STDIN it is a bit difficult to set up the arguments correctly so that the module will get them as parameters.

All modules should finish by calling either the module.fail_json() or module.exit_json(), but these won’t work correctly in a testing environment.

To pass arguments to a module correctly, use the set_module_args method which accepts a dictionary as its parameter. Module creation and argument processing is handled through the AnsibleModule object in the basic section of the utilities. Normally this accepts input on STDIN, which is not convenient for unit testing. When the special variable is set it will be treated as if the input came on STDIN to the module. Simply call that function before setting up your module:

The module.exit_json() function won’t work properly in a testing environment since it writes error information to STDOUT upon exit, where it is difficult to examine. This can be mitigated by replacing it (and module.fail_json()) with a function that raises an exception:

Now you can ensure that the first function called is the one you expected simply by testing for the correct exception:

The same technique can be used to replace module.fail_json() (which is used for failure returns from modules) and for the aws_module.fail_json_aws() (used in modules for Amazon Web Services).

If you do want to run the actual main function of a module you must import the module, set the arguments as above, set up the appropriate exit exception and then run the module:

Module must use AnsibleModule.run_command() in order to execute an external command. This method needs to be mocked:

Here is a simple mock of AnsibleModule.run_command() (taken from test/units/modules/packaging/os/test_rhn_register.py):

The following example is a complete skeleton that reuses the mocks explained above and adds a new mock for Ansible.get_bin_path():

Often modules have a main() function which sets up the module and then performs other actions. This can make it difficult to check argument processing. This can be made easier by moving module configuration and initialization into a separate function. For example:

This now makes it possible to run tests against the module initiation function:

See also test/units/module_utils/aws/test_rds.py

Note that the argument_spec dictionary is visible in a module variable. This has advantages, both in allowing explicit testing of the arguments and in allowing the easy creation of module objects for testing.

The same restructuring technique can be valuable for testing other functionality, such as the part of the module which queries the object that the module configures.

If you use the mock library from the Python 2.6 standard library, a number of the assert functions are missing but will return as if successful. This means that test cases should take great care not use functions marked as _new_ in the Python 3 documentation, since the tests will likely always succeed even if the code is broken when run on older versions of Python.

A helpful development approach to this should be to ensure that all of the tests have been run under Python 2.6 and that each assertion in the test cases has been checked to work by breaking the code in Ansible to trigger that failure.

Maintain Python 2.6 compatibility

Please remember that modules need to maintain compatibility with Python 2.6 so the unittests for modules should also be compatible with Python 2.6.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

Ansible unit tests documentation

Running tests locally including gathering and reporting coverage data

Get started developing a module

The documentation of the unittest framework in python 3

The documentation of the earliest supported unittest framework - from Python 2.6

The documentation of pytest - the framework actually used to run Ansible unit tests

General advice on testing Python code

Unit testing is a part of the of various philosophies of software development, including Extreme Programming (XP), Clean Coding. Uncle Bob talks through how to benefit from this

An article warning against the costs of unit testing

An response pointing to how to maintain the value of unit tests

**Examples:**

Example 1 (unknown):
```unknown
module = MagicMock()
function_to_test(module, argument)
module.fail_json.assert_not_called()
```

Example 2 (unknown):
```unknown
class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass

# you may also do the same to fail json
module = MagicMock()
module.exit_json.side_effect = AnsibleExitJson(Exception)
with self.assertRaises(AnsibleExitJson) as result:
    results = my_module.test_this_function(module, argument)
module.fail_json.assert_not_called()
assert results["changed"] == True
```

Example 3 (python):
```python
def simple_instance_list(status, pending):
    return {u'DBInstances': [{u'DBInstanceArn': 'arn:aws:rds:us-east-1:1234567890:db:fakedb',
                              u'DBInstanceStatus': status,
                              u'PendingModifiedValues': pending,
                              u'DBInstanceIdentifier': 'fakedb'}]}
```

Example 4 (unknown):
```unknown
rds_client_double = MagicMock()
rds_client_double.describe_db_instances.side_effect = [
    simple_instance_list('rebooting', {"a": "b", "c": "d"}),
    simple_instance_list('available', {"c": "d", "e": "f"}),
    simple_instance_list('rebooting', {"a": "b"}),
    simple_instance_list('rebooting', {"e": "f", "g": "h"}),
    simple_instance_list('rebooting', {}),
    simple_instance_list('available', {"g": "h", "i": "j"}),
    simple_instance_list('rebooting', {"i": "j", "k": "l"}),
    simple_instance_list('available', {}),
    simple_instance_list('available', {}),
]
```

---

## Index of all deprecated plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/deprecations.html

**Contents:**
- Index of all deprecated plugins

No plugins have been deprecated.

---

## Working with plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/plugins.html

**Contents:**
- Working with plugins

Plugins are pieces of code that augment Ansible’s core functionality. Ansible uses a plugin architecture to enable a rich, flexible and expandable feature set.

Ansible ships with a number of handy plugins, and you can easily write your own.

This section covers the various types of plugins that are included with Ansible:

Controlling access to modules

Ansible configuration documentation and settings

Ansible tools, description and options

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## ansible-doc — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-doc.html

**Contents:**
- ansible-doc
- Synopsis
- Description
- Common Options
- Environment
- Files
- Author
- License
- See also

plugin documentation tool

displays information on modules installed in Ansible libraries. It displays a terse listing of plugins and their short descriptions, provides a printout of their DOCUMENTATION strings, and it can create a short “snippet” which can be pasted into a playbook.

For internal use only Dump json metadata for all entries, ignores other options.

For internal use only Only used for –metadata-dump. Do not fail on errors. Report the error message in the JSON instead.

Since this tool does not use playbooks, use this as a substitute playbook directory. This sets the relative path for many features including roles/ group_vars/ etc.

show program’s version number, config file location, configured module search path, module location, executable location and exit

Show plugin names and their source files without summaries (implies –list). A supplied argument will be used for filtering, can be a namespace or full collection name.

prepend colon-separated path(s) to module library (default={{ ANSIBLE_HOME ~ “/plugins/modules:/usr/share/ansible/plugins/modules” }}). This argument may be specified multiple times.

Select the entry point for role(s).

show this help message and exit

Change output into json format.

List available plugins. A supplied argument will be used for filtering, can be a namespace or full collection name.

The path to the directory containing your roles. This argument may be specified multiple times.

Show playbook snippet for these plugin types: inventory, lookup, module

Choose which plugin type (defaults to “module”). Available plugin types are : (‘become’, ‘cache’, ‘callback’, ‘cliconf’, ‘connection’, ‘httpapi’, ‘inventory’, ‘lookup’, ‘netconf’, ‘shell’, ‘vars’, ‘module’, ‘strategy’, ‘test’, ‘filter’, ‘role’, ‘keyword’)

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

The following environment variables may be specified.

ANSIBLE_LIBRARY – Override the default ansible module library path

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-config(1), ansible-console(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1), ansible-vault(1)

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-doc [-h] [--version] [-v] [-M MODULE_PATH]
                [--playbook-dir BASEDIR]
                [-t {become,cache,callback,cliconf,connection,httpapi,inventory,lookup,netconf,shell,vars,module,strategy,test,filter,role,keyword}]
                [-j] [-r ROLES_PATH]
                [-e ENTRY_POINT | -s | -F | -l | --metadata-dump]
                [--no-fail-on-errors]
                [plugin ...]
```

---

## Index of all Filter Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_filter.html

**Contents:**
- Index of all Filter Plugins
- ansible.builtin

ansible.builtin.abs – Return the absolute value of the argument.

ansible.builtin.attr – Get an attribute of an object.

ansible.builtin.b64decode – Decode a Base64 string

ansible.builtin.b64encode – Encode a string as Base64

ansible.builtin.basename – get a path’s base name

ansible.builtin.batch – A filter that batches items.

ansible.builtin.bool – coerce some well-known truthy/falsy values to a boolean

ansible.builtin.capitalize – Capitalize a value.

ansible.builtin.center – Centers the value in a field of a given width.

ansible.builtin.checksum – checksum of input data

ansible.builtin.combinations – combinations from the elements of a list

ansible.builtin.combine – combine two dictionaries

ansible.builtin.comment – comment out a string

ansible.builtin.commonpath – gets the common path

ansible.builtin.count – Return the number of items in a container.

ansible.builtin.d – If the value is undefined it will return the passed default value, otherwise the value of the variable.

ansible.builtin.default – If the value is undefined it will return the passed default value, otherwise the value of the variable.

ansible.builtin.dict2items – Convert a dictionary into an itemized list of dictionaries

ansible.builtin.dictsort – Sort a dict and yield.

ansible.builtin.difference – the difference of one list from another

ansible.builtin.dirname – get a path’s directory name

ansible.builtin.e – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.

ansible.builtin.escape – Replace the characters ``&``, ``<``, ``>``, ``’``, and ``”`` in the string with HTML-safe sequences.

ansible.builtin.expanduser – Returns a path with ~ translation.

ansible.builtin.expandvars – expand environment variables

ansible.builtin.extract – extract a value based on an index or key

ansible.builtin.fileglob – explode a path glob to matching files

ansible.builtin.filesizeformat – Format the value like a ‘human-readable’ file size.

ansible.builtin.first – Return the first item of a sequence.

ansible.builtin.flatten – flatten lists within a list

ansible.builtin.float – Convert the value into a floating point number.

ansible.builtin.forceescape – Enforce HTML escaping.

ansible.builtin.format – Apply the given values to a `printf-style`_ format string, like ``string % values``.

ansible.builtin.from_json – Convert JSON string into variable structure

ansible.builtin.from_yaml – Convert YAML string into variable structure

ansible.builtin.from_yaml_all – Convert a series of YAML documents into a variable structure

ansible.builtin.groupby – Group a sequence of objects by an attribute using Python’s :func:`itertools.

ansible.builtin.hash – hash of input data

ansible.builtin.human_readable – Make bytes/bits human-readable

ansible.builtin.human_to_bytes – Get bytes from string

ansible.builtin.indent – Return a copy of the string with each line indented by 4 spaces.

ansible.builtin.int – Convert the value into an integer.

ansible.builtin.intersect – intersection of lists

ansible.builtin.items – Return an iterator over the ``(key, value)`` items of a mapping.

ansible.builtin.items2dict – Consolidate a list of itemized dictionaries into a dictionary

ansible.builtin.join – Return a string which is the concatenation of the strings in the sequence.

ansible.builtin.last – Return the last item of a sequence.

ansible.builtin.length – Return the number of items in a container.

ansible.builtin.list – Convert the value into a list.

ansible.builtin.log – log of (math operation)

ansible.builtin.lower – Convert a value to lowercase.

ansible.builtin.mandatory – make a variable’s existence mandatory

ansible.builtin.map – Applies a filter on a sequence of objects or looks up an attribute.

ansible.builtin.max – Return the largest item from the sequence.

ansible.builtin.md5 – MD5 hash of input data

ansible.builtin.min – Return the smallest item from the sequence.

ansible.builtin.normpath – Normalize a pathname

ansible.builtin.password_hash – convert input password into password_hash

ansible.builtin.path_join – Join one or more path components

ansible.builtin.permutations – permutations from the elements of a list

ansible.builtin.pow – power of (math operation)

ansible.builtin.pprint – Pretty print a variable.

ansible.builtin.product – cartesian product of lists

ansible.builtin.quote – shell quoting

ansible.builtin.random – random number or list item

ansible.builtin.realpath – Turn path into real path

ansible.builtin.regex_escape – escape regex chars

ansible.builtin.regex_findall – extract all regex matches from string

ansible.builtin.regex_replace – replace a string via regex

ansible.builtin.regex_search – extract regex match from string

ansible.builtin.reject – Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.

ansible.builtin.rejectattr – Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.

ansible.builtin.rekey_on_member – Rekey a list of dicts into a dict using a member

ansible.builtin.relpath – Make a path relative

ansible.builtin.replace – Return a copy of the value with all occurrences of a substring replaced with a new one.

ansible.builtin.reverse – Reverse the object or return an iterator that iterates over it the other way round.

ansible.builtin.root – root of (math operation)

ansible.builtin.round – Round the number to a given precision.

ansible.builtin.safe – Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.

ansible.builtin.select – Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.

ansible.builtin.selectattr – Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.

ansible.builtin.sha1 – SHA-1 hash of input data

ansible.builtin.shuffle – randomize a list

ansible.builtin.slice – Slice an iterator and return a list of lists containing those items.

ansible.builtin.sort – Sort an iterable using Python’s :func:`sorted`.

ansible.builtin.split – split a string into a list

ansible.builtin.splitext – split a path into root and file extension

ansible.builtin.strftime – date formatting

ansible.builtin.string – Convert an object to a string if it isn’t already.

ansible.builtin.striptags – Strip SGML/XML tags and replace adjacent whitespace by one space.

ansible.builtin.subelements – returns a product of a list and its elements

ansible.builtin.sum – Returns the sum of a sequence of numbers plus the value of parameter ‘start’.

ansible.builtin.symmetric_difference – different items from two lists

ansible.builtin.ternary – Ternary operation filter

ansible.builtin.title – Return a titlecased version of the value.

ansible.builtin.to_datetime – Get datetime from string

ansible.builtin.to_json – Convert variable to JSON string

ansible.builtin.to_nice_json – Convert variable to ‘nicely formatted’ JSON string

ansible.builtin.to_nice_yaml – Convert variable to YAML string

ansible.builtin.to_uuid – namespaced UUID generator

ansible.builtin.to_yaml – Convert variable to YAML string

ansible.builtin.tojson – Serialize an object to a string of JSON, and mark it safe to render in HTML.

ansible.builtin.trim – Strip leading and trailing characters, by default whitespace.

ansible.builtin.truncate – Return a truncated copy of the string.

ansible.builtin.type_debug – show input data type

ansible.builtin.union – union of lists

ansible.builtin.unique – set of unique items of a list

ansible.builtin.unvault – Open an Ansible Vault

ansible.builtin.upper – Convert a value to uppercase.

ansible.builtin.urldecode – Decode percent-encoded sequences

ansible.builtin.urlencode – Quote data for use in a URL path or query using UTF-8.

ansible.builtin.urlize – Convert URLs in text into clickable links.

ansible.builtin.urlsplit – get components from URL

ansible.builtin.vault – vault your secrets

ansible.builtin.win_basename – Get a Windows path’s base name

ansible.builtin.win_dirname – Get a Windows path’s directory

ansible.builtin.win_splitdrive – Split a Windows path by the drive letter

ansible.builtin.wordcount – Count the words in that string.

ansible.builtin.wordwrap – Wrap a string to the given width.

ansible.builtin.xmlattr – Create an SGML/XML attribute string based on the items in a dict.

ansible.builtin.zip – combine list elements

ansible.builtin.zip_longest – combine list elements, with filler

---

## Index of all Notification Callback Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/callback_index_notification.html

**Contents:**
- Index of all Notification Callback Plugins
- ansible.builtin

See Index of all Callback Plugins for the list of all callback plugins.

ansible.builtin.tree – Save host events to files

---

## Adjacent YAML documentation files — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/sidecar.html

**Contents:**
- Adjacent YAML documentation files
- YAML documentation for plugins
- YAML format
- Supported plugin types

YAML documentation for plugins

Supported plugin types

For most Ansible plugins, the documentation is in the same file as the code. This approach does not work for cases when:

Multiple plugins are defined in the same file, such as tests and filters.

Plugins are written in a language other than Python (modules).

These cases require plugins to provide documentation in an adjacent .py file. As of ansible-core 2.14, you can provide documentation as adjacent YAML files instead. The format of a YAML documentation file is nearly identical to its Python equivalent, except it is pure YAML.

In Python, each section is a variable DOCUMENTATION = r""" ... """ while in YAML, it is a mapping key DOCUMENTATION: ....

Here is a longer example that shows documentation as embedded in a Python file:

This example shows the same documentation in YAML format:

As the examples above show, Python variables already contain YAML. The main change to use YAML documentation is to simply move the YAML out of such variables.

Any adjacent YAML documentation files must be in the same directory as the plugin or module that they document. This means the documentation is available in any directory that contains the plugins or modules.

YAML documentation is mainly intended for filters, tests, and modules. While it is possible to use it with other plugin types, Ansible always recommends having documentation in the same file as the code for most cases.

Browse existing collections, modules, and plugins

Learn about the Python API for task execution

Learn about how to develop dynamic inventory sources

Learn about how to write Ansible modules

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
DOCUMENTATION = r'''
  description: something
  options:
    option_name:
      description: describe this config option
      default: default value for this config option
      env:
        - name: NAME_OF_ENV_VAR
      ini:
        - section: section_of_ansible.cfg_where_this_config_option_is_defined
          key: key_used_in_ansible.cfg
      vars:
        - name: name_of_ansible_var
        - name: name_of_second_var
          version_added: X.x
      required: True/False
      type: boolean/float/integer/list/none/path/pathlist/pathspec/string/tmppath
      version_added: X.x
'''

EXAMPLES = r'''
  # TODO: write examples
'''
```

Example 2 (unknown):
```unknown
DOCUMENTATION:
  description: something
  options:
    option_name:
      description: describe this config option
      default: default value for this config option
      env:
        - name: NAME_OF_ENV_VAR
      ini:
        - section: section_of_ansible.cfg_where_this_config_option_is_defined
          key: key_used_in_ansible.cfg
      vars:
        - name: name_of_ansible_var
        - name: name_of_second_var
          version_added: X.x
      required: True/False
      type: boolean/float/integer/list/none/path/pathlist/pathspec/string/tmppath
      version_added: X.x

EXAMPLES: # TODO: write examples
```

---

## Indexes of all modules and plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/all_plugins.html

**Contents:**
- Indexes of all modules and plugins

---

## Index of all Test Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_test.html

**Contents:**
- Index of all Test Plugins
- ansible.builtin

ansible.builtin.abs – is the path absolute

ansible.builtin.all – are all conditions in a list true

ansible.builtin.any – is any condition in a list true

ansible.builtin.boolean – Return true if the object is a boolean value.

ansible.builtin.callable – Return whether the object is callable.

ansible.builtin.changed – did the task require changes

ansible.builtin.contains – does the list contain this element

ansible.builtin.defined – Return true if the variable is defined.

ansible.builtin.directory – does the path resolve to an existing directory

ansible.builtin.divisibleby – Check if a variable is divisible by a number.

ansible.builtin.eq – Same as a == b.

ansible.builtin.equalto – Same as a == b.

ansible.builtin.escaped – Check if the value is escaped.

ansible.builtin.even – Return true if the variable is even.

ansible.builtin.exists – does the path exist, follow symlinks

ansible.builtin.failed – did the task fail

ansible.builtin.false – Return true if the object is False.

ansible.builtin.falsy – Pythonic false

ansible.builtin.file – does the path resolve to an existing file

ansible.builtin.filter – Check if a filter exists by name.

ansible.builtin.finished – Did async task finish

ansible.builtin.float – Return true if the object is a float.

ansible.builtin.ge – Same as a >= b.

ansible.builtin.greaterthan – Same as a > b.

ansible.builtin.gt – Same as a > b.

ansible.builtin.in – Check if value is in seq.

ansible.builtin.integer – Return true if the object is an integer.

ansible.builtin.iterable – Check if it’s possible to iterate over an object.

ansible.builtin.le – Same as a <= b.

ansible.builtin.lessthan – Same as a < b.

ansible.builtin.link – does the path reference existing symbolic link

ansible.builtin.link_exists – does the path exist, no follow

ansible.builtin.lower – Return true if the variable is lowercased.

ansible.builtin.lt – Same as a < b.

ansible.builtin.mapping – Return true if the object is a mapping.

ansible.builtin.match – Does string match regular expression from the start

ansible.builtin.mount – does the path resolve to mount point

ansible.builtin.nan – is this not a number (NaN)

ansible.builtin.ne – Same as a .

ansible.builtin.none – Return true if the variable is none.

ansible.builtin.number – Return true if the variable is a number.

ansible.builtin.odd – Return true if the variable is odd.

ansible.builtin.reachable – Task did not end due to unreachable host

ansible.builtin.regex – Does string match regular expression from the start

ansible.builtin.same_file – compares two paths to see if they resolve to the same filesystem object

ansible.builtin.sameas – Check if an object points to the same memory address than another object.

ansible.builtin.search – Does string match a regular expression

ansible.builtin.sequence – Return true if the variable is a sequence.

ansible.builtin.skipped – Was task skipped

ansible.builtin.started – Was async task started

ansible.builtin.string – Return true if the object is a string.

ansible.builtin.subset – is the list a subset of this other list

ansible.builtin.success – check task success

ansible.builtin.superset – is the list a superset of this other list

ansible.builtin.test – Check if a test exists by name.

ansible.builtin.timedout – did the task time out

ansible.builtin.true – Return true if the object is True.

ansible.builtin.truthy – Pythonic true

ansible.builtin.undefined – Like :func:`defined` but the other way round.

ansible.builtin.unreachable – Did task end due to the host was unreachable

ansible.builtin.upper – Return true if the variable is uppercased.

ansible.builtin.uri – is the string a valid URI

ansible.builtin.url – is the string a valid URL

ansible.builtin.urn – is the string a valid URN

ansible.builtin.vault_encrypted – Is this an encrypted vault string

ansible.builtin.vaulted_file – Is this file an encrypted vault

ansible.builtin.version – compare version strings

---

## The lifecycle of an Ansible module or plugin — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/module_lifecycle.html

**Contents:**
- The lifecycle of an Ansible module or plugin
- Deprecating modules and plugins in the Ansible main repository
- Deprecating modules and plugins in a collection
- Changing a module or plugin name in the Ansible main repository
- Renaming a module or plugin in a collection, or redirecting a module or plugin to another collection
- Tombstoning a module or plugin in a collection

Modules and plugins in the main Ansible repository have a defined life cycle, from the first introduction to final removal. The module and plugin lifecycle is tied to the Ansible release cycle <release_cycle>. A module or plugin may move through these four stages:

When a module or plugin is first accepted into Ansible, we consider it in tech preview and will mark it as such in the documentation.

If a module or plugin matures, the ‘preview’ mark in the documentation is removed. Backward compatibility for these modules and plugins is maintained but not guaranteed, which means their parameters should be maintained with stable meanings.

If a module’s or plugin’s target API changes radically, or if someone creates a better implementation of its functionality, we may mark it deprecated. Modules and plugins that are deprecated are still available but they are reaching the end of their life cycle. We retain deprecated modules and plugins for 4 release cycles with deprecation warnings to help users update playbooks and roles that use them.

When a module or plugin has been deprecated for four release cycles, it is removed and replaced with a tombstone entry in the routing configuration. Modules and plugins that are removed are no longer shipped with Ansible. The tombstone entry helps users find alternative modules and plugins.

For modules and plugins in collections, the lifecycle is similar. Since ansible-base 2.10, it is no longer possible to mark modules as ‘preview’ or ‘stable’.

To deprecate a module in ansible-core, you must:

Rename the file so it starts with an _, for example, rename old_cloud.py to _old_cloud.py. This keeps the module available and marks it as deprecated on the module index pages.

Mention the deprecation in the relevant changelog (by creating a changelog fragment with a section deprecated_features).

Reference the deprecation in the relevant porting_guide_core_x.y.rst.

Add deprecated: to the documentation with the following sub-values:

A string, such as "2.10"; the version of Ansible where the module will be replaced with a docs-only module stub. Usually current release +4. Mutually exclusive with :removed_by_date:.

(Added in ansible-base 2.10). An ISO 8601 formatted date when the module will be removed. Usually 2 years from the date the module is deprecated. Mutually exclusive with :removed_in:.

Optional string that used to detail why this has been removed.

Inform users they should do instead, for example, Use M(whatmoduletouseinstead) instead..

For an example of documenting deprecation, see this PR that deprecates multiple modules. Some of the elements in the PR might now be out of date.

To deprecate a module in a collection, you must:

Add a deprecation entry to plugin_routing in meta/runtime.yml. For example, to deprecate the module old_cloud, add:

For other plugin types, you have to replace modules: with <plugin_type>:, for example lookup: for lookup plugins. When deprecating action plugins, you need to add two entries: one for the action plugin and one for the module file that contains the documentation.

Instead of removal_version, you can also use removal_date with an ISO 8601 formatted date after which the module will be removed in a new major version of the collection.

Mention the deprecation in the relevant changelog. If the collection uses antsibull-changelog, create a changelog fragment with a section deprecated_features.

Add deprecated: to the documentation of the module or plugin with the following sub-values:

A string, such as "2.10"; the version of Ansible where the module will be replaced with a docs-only module stub. Usually current release +4. Mutually exclusive with :removed_by_date:.

(Added in ansible-base 2.10). An ISO 8601 formatted date when the module will be removed. Usually 2 years from the date the module is deprecated. Mutually exclusive with :removed_in:.

String that used to detail why this has been removed.

Inform users they should do instead, for example, Use M(whatmoduletouseinstead) instead.. See Linking within module documentation for ways to reference entities other than modules.

You can also rename a module and keep a deprecated alias to the old name by using a symlink that starts with _. This example allows the stat module to be called with fileinfo, making the following examples equivalent:

To rename a module or plugin in a collection, or to redirect a module or plugin to another collection, you need to add a redirect entry to plugin_routing in meta/runtime.yml. For example, to redirect the module old_cloud to foo.bar.new_cloud, add:

If you want to deprecate the old name, add a deprecation: entry (see above):

You need to use the Fully Qualified Collection Name (FQCN) of the new module/plugin name, even if it is located in the same collection as the redirect. By using a FQCN from another collection, you redirect the module/plugin to that collection.

If you need to support Ansible 2.9, please note that Ansible 2.9 does not know about meta/runtime.yml. With Ansible 2.9 you can still rename plugins and modules inside one collection by using symbolic links. Note that ansible-base 2.10, ansible-core 2.11, and newer will prefer meta/runtime.yml entries over symbolic links.

To remove a deprecated module or plugin from a collection, you need to tombstone it:

Remove the module or plugin file with related files like tests, documentation references, and documentation.

Add a tombstone entry in meta/runtime.yml. For example, to tombstone the module old_cloud, add:

Instead of removal_version, you can also use removal_date with an ISO 8601 formatted date. The date should be the date of the next major release.

**Examples:**

Example 1 (unknown):
```unknown
plugin_routing:
    modules:
        old_cloud:
            deprecation:
                removal_version: 2.0.0
                warning_text: Use foo.bar.new_cloud instead.
```

Example 2 (unknown):
```unknown
ln -s stat.py _fileinfo.py
ansible -m stat -a "path=/tmp" localhost
ansible -m fileinfo -a "path=/tmp" localhost
```

Example 3 (unknown):
```unknown
plugin_routing:
    modules:
        old_cloud:
            redirect: foo.bar.new_cloud
```

Example 4 (unknown):
```unknown
plugin_routing:
    modules:
        old_cloud:
            redirect: foo.bar.new_cloud
            deprecation:
                removal_version: 2.0.0
                warning_text: Use foo.bar.new_cloud instead.
```

---

## Index of all Strategy Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_strategy.html

**Contents:**
- Index of all Strategy Plugins
- ansible.builtin

ansible.builtin.debug – Executes tasks in interactive debug session.

ansible.builtin.free – Executes tasks without waiting for all hosts

ansible.builtin.host_pinned – Executes tasks on each host without interruption

ansible.builtin.linear – Executes tasks in a linear fashion

---

## Index of all Cache Plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/collections/index_cache.html

**Contents:**
- Index of all Cache Plugins
- ansible.builtin

ansible.builtin.jsonfile – JSON formatted files.

ansible.builtin.memory – RAM backed, non persistent

---

## Terminal plugins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/plugins/terminal.html

**Contents:**
- Terminal plugins
- Adding terminal plugins
- Using terminal plugins

Adding terminal plugins

Using terminal plugins

Terminal plugins contain information on how to ensure that a particular network device’s SSH shell is properly initialized to be used with Ansible. This typically includes disabling automatic paging, detecting errors in output, and enabling privileged mode if the device supports and requires it.

These plugins correspond one-to-one to network device platforms. Ansible loads the appropriate terminal plugin automatically based on the ansible_network_os variable.

You can extend Ansible to support other network devices by dropping a custom plugin into the terminal_plugins directory.

Ansible determines which terminal plugin to use automatically from the ansible_network_os variable. There should be no reason to override this functionality.

Terminal plugins operate without configuration. All options to control the terminal are exposed in the network_cli connection plugin.

Plugins are self-documenting. Each plugin should document its configuration options.

An overview of using Ansible to automate networking devices.

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---
