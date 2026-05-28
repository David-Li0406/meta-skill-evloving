# Ansible-Core - Other

**Pages:** 10

---

## Ansible Reference: Module Utilities — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/module_utils.html

**Contents:**
- Ansible Reference: Module Utilities
- AnsibleModule
- Basic
- Argument Spec
  - ArgumentSpecValidator
  - ValidationResult
  - Parameters
  - Validation
- Errors

This page documents utilities intended to be helpful when writing Ansible modules in Python.

To use this functionality, include from ansible.module_utils.basic import AnsibleModule in your module.

Common code for quickly building an ansible module in Python (although you can write modules with anything that can return JSON).

See Developing modules for a general introduction and Ansible module architecture for more detailed explanation.

for results that are files, supplement the info about the file in the return path with stats about the file path.

atomically move src to dest, copying attributes from dest, returns true on success it uses os.rename to ensure this as it is an atomic operation, rest of the function is to work around limitations, corner cases and ensure selinux context is saved if possible

make a date-marked backup of the specified file, return True or False on success or failure

Convert the argument to a boolean

Record a deprecation warning to be returned with the module result. Most callers do not need to provide collection_name or deprecator – but provide only one if needed. Specify version or date, but not both. If date is a string, it must be in the form YYYY-MM-DD.

Return hex digest of local file for a digest_method specified by name, or None if file is not present.

Display an exception as a warning.

return from the module, without error

Return from the module with an error message and optional exception/traceback detail. A traceback will only be included in the result if error traceback capturing has been enabled.

When exception is an exception object, its message chain will be automatically combined with msg to create the final error message. The message chain includes the exception’s message as well as messages from any __cause__ exceptions. The traceback from exception will be used for the formatted traceback.

When exception is a string, it will be used as the formatted traceback.

When exception is set to None, the current call stack will be used for the formatted traceback.

When exception is not specified, a formatted traceback will be retrieved from the current exception. If no exception is pending, the current call stack will be used instead.

Takes a path and returns its mount point

path – a string type with a filesystem path

the path to the mount point as a text type

Find system executable in PATH.

arg – The executable to find.

required – if the executable is not found and required is True, fail_json

opt_dirs – optional list of directories to search in addition to PATH

if found return full path; otherwise return original arg, unless ‘warning’ then return None

Sysexit: if arg is not found and required=True (via fail_json)

is the given path executable?

path – The path of the file to check.

Does not account for FSACLs.

Most times we really want to know “Can the current user execute this file”. This function does not tell us that, only if any execute bit is set.

Returns a tuple containing (True, selinux_context) if the given path is on a NFS or other ‘special’ fs mount point, otherwise the return will be (False, None).

many modules deal with files, this encapsulates common options that the file module accepts such that it is directly available to all modules and they can share code.

Allows to overwrite the path/dest module argument by providing path.

Return MD5 hex digest of local file using digest_from_file().

Optional backwards compatibility

Compatibility with a third party protocol

This function will not work on systems complying with FIPS-140-2.

Most uses of this function can use the module.sha1 function instead.

Copy a file with preserved ownership, permissions and context

Execute a command, returns rc, stdout, and stderr.

The mechanism of this method for reading stdout and stderr differs from that of CPython subprocess.Popen.communicate, in that this method will stop reading once the spawned command has exited and stdout and stderr have been consumed, as opposed to waiting until stdout/stderr are closed. This can be an important distinction, when taken into account that a forked or backgrounded process may hold stdout or stderr open for longer than the spawned command.

args – is the command to run * If args is a list, the command will be run with shell=False. * If args is a string and use_unsafe_shell=False it will split args to a list and run with shell=False * If args is a string and use_unsafe_shell=True it runs with shell=True.

Whether to call fail_json in case of non zero RC. Default False

See documentation for subprocess.Popen(). Default True

See documentation for subprocess.Popen(). Default None

If given, information to write to the stdin of the command

If False, append a newline to the data. Default False

If given, additional path to find the command in. This adds to the PATH environment variable so helper commands in the same directory can also be found

If given, working directory to run the command inside

See args parameter. Default False

Regex string (not a compiled regex) which can be used to detect prompts in the stdout which would otherwise cause the execution to hang (especially if no input data is specified)

dictionary to update environ variables with

Umask to be used when running the command. Default None

Since we return strings, we need to know the encoding to use to transform from bytes to text. If you want to always get bytes back, use encoding=None. The default is “utf-8”. This does not affect transformation of strings given as args.

Since we return strings, we need to transform stdout and stderr from bytes to text. If the bytes are undecodable in the encoding specified, then use this error handler to deal with them. The default is surrogate_or_strict which means that the bytes will be decoded using the surrogateescape error handler if available (available on all Python versions we support) otherwise a UnicodeError traceback will be raised. This does not affect transformations of strings given as args.

When use_unsafe_shell=False this argument dictates whether ~ is expanded in paths and environment variables are expanded before running the command. When True a string such as $SHELL will be expanded regardless of escaping. When False and use_unsafe_shell=False no path or variable expansion will be done.

This argument dictates which file descriptors should be passed to an underlying Popen constructor.

This function will be called after Popen object will be created but before communicating to the process. (Popen object will be passed to callback as a first argument)

This flag indicates whether an invalid cwd (non-existent or not a directory) should be ignored or should raise an exception.

This flag indicates whether an exception will be handled inline and issue a failed_json or if the caller should handle it.

A 3-tuple of return code (int), stdout (str), and stderr (str). stdout and stderr are text strings converted according to the encoding and errors parameters. If you want byte strings, use encoding=None to turn decoding to text off.

Return SHA1 hex digest of local file using digest_from_file().

Return SHA-256 hex digest of local file using digest_from_file().

To use this functionality, include import ansible.module_utils.basic in your module.

Deprecated: Use ansible.module_utils.common._utils.get_all_subclasses instead

Deprecated Use platform.system() directly.

Name of the platform the module is running on in a native string

Returns a native string that labels the platform (“Linux”, “Solaris”, etc). Currently, this is the result of calling platform.system().

Remove strings that look like passwords from log messages

Deprecated: Use ansible.module_utils.common.sys_info.get_platform_subclass instead

Classes and functions for validating parameters against an argument spec.

Argument spec validation class

Creates a validator based on the argument_spec that can be used to validate a number of parameters using the validate() method.

argument_spec (dict[str, dict]) – Specification of valid parameters and their type. May include nested argument specs.

mutually_exclusive (list[str] or list[list[str]]) – List or list of lists of terms that should not be provided together.

required_together (list[list[str]]) – List of lists of terms that are required together.

required_one_of (list[list[str]]) – List of lists of terms, one of which in each list is required.

required_if (list) – List of lists of [parameter, value, [parameters]] where one of [parameters] is required if parameter == value.

required_by (dict[str, list[str]]) – Dictionary of parameter names that contain a list of parameters required by each key in the dictionary.

Validate parameters against argument spec.

Error messages in the ValidationResult may contain no_log values and should be sanitized with sanitize_keys() before logging or displaying.

parameters (dict[str, dict]) – Parameters to validate against the argument spec

ValidationResult containing validated parameters.

Result of argument spec validation.

This is the object returned by ArgumentSpecValidator.validate() containing the validated parameters and any errors.

parameters (dict) – Terms to be validated and coerced to the correct type.

AnsibleValidationErrorMultiple containing all AnsibleValidationError objects if there were any failures during validation.

Validated and coerced parameters.

set of unsupported parameter names.

list of all error messages from each exception in errors.

dict of type names, such as 'str', and the default function used to check that type, check_type_str() in this case.

Load value from environment variable

Remove strings in no_log_strings from value.

If value is a container type, then remove a lot more.

Use of deferred_removals exists, rather than a pure recursive solution, because of the potential to hit the maximum recursion depth when dealing with large amounts of data (see issue #24560).

Sanitize the keys in a container object by removing no_log values from key names.

This is a companion function to the remove_values() function. Similar to that function, we make use of deferred_removals to avoid hitting maximum recursion depth in cases of large data structures.

obj – The container object to sanitize. Non-container objects are returned unmodified.

no_log_strings – A set of string values we do not want logged.

ignore_keys – A set of string values of keys to not sanitize.

An object with sanitized keys.

Standalone functions for validating various parameter types.

This is for checking for required params when we can not check via argspec because we need more information than is simply given in the argspec.

Raises TypeError if any required parameters are missing

parameters – Dictionary of parameters

required_parameters – List of parameters to look for in the given parameters.

Empty list or raises TypeError if the check fails.

Check mutually exclusive terms against argument parameters

Accepts a single list or list of lists that are groups of terms that should be mutually exclusive with one another

terms – List of mutually exclusive parameters

parameters – Dictionary of parameters

options_context – List of strings of parent key names if terms are in a sub spec.

Empty list or raises TypeError if the check fails.

Check all parameters in argument_spec and return a list of parameters that are required but not present in parameters.

Raises TypeError if the check fails

argument_spec – Argument spec dictionary containing all parameters and their specification

parameters – Dictionary of parameters

options_context – List of strings of parent key names if argument_spec are in a sub spec.

Empty list or raises TypeError if the check fails.

For each key in requirements, check the corresponding list to see if they exist in parameters.

Accepts a single string or list of values for each key.

requirements – Dictionary of requirements

parameters – Dictionary of parameters

options_context – List of strings of parent key names if requirements are in a sub spec.

Empty dictionary or raises TypeError if the check fails.

Check parameters that are conditionally required

Raises TypeError if the check fails

requirements – List of lists specifying a parameter, value, parameters required when the given parameter is the specified value, and optionally a boolean indicating any or all parameters are required.

parameters – Dictionary of parameters

options_context – List of strings of parent key names if requirements are in a sub spec.

Empty list or raises TypeError if the check fails. The results attribute of the exception contains a list of dictionaries. Each dictionary is the result of evaluating each item in requirements. Each return dictionary contains the following keys: key missing: List of parameters that are required but missing key requires: ’any’ or ‘all’ key parameter: Parameter name that has the requirement key value: Original value of the parameter key requirements: Original required parameters Example: [ { 'parameter': 'someint', 'value': 99 'requirements': ('bool_param', 'string_param'), 'missing': ['string_param'], 'requires': 'all', } ]

Empty list or raises TypeError if the check fails. The results attribute of the exception contains a list of dictionaries. Each dictionary is the result of evaluating each item in requirements. Each return dictionary contains the following keys:

List of parameters that are required but missing

Parameter name that has the requirement

Original value of the parameter

Original required parameters

Check each list of terms to ensure at least one exists in the given module parameters

Accepts a list of lists or tuples

terms – List of lists of terms to check. For each list of terms, at least one is required.

parameters – Dictionary of parameters

options_context – List of strings of parent key names if terms are in a sub spec.

Empty list or raises TypeError if the check fails.

Check each list of terms to ensure every parameter in each list exists in the given parameters.

Accepts a list of lists or tuples.

terms – List of lists of terms to check. Each list should include parameters that are all required when at least one is specified in the parameters.

parameters – Dictionary of parameters

options_context – List of strings of parent key names if terms are in a sub spec.

Empty list or raises TypeError if the check fails.

Convert a human-readable string bits value to bits in integer.

Example: check_type_bits('1Mb') returns integer 1048576.

Raises TypeError if unable to convert the value.

Verify that the value is a bool or convert it to a bool and return it.

Raises TypeError if unable to convert to a bool

value – String, int, or float to convert to bool. Valid booleans include: ‘1’, ‘on’, 1, ‘0’, 0, ‘n’, ‘f’, ‘false’, ‘true’, ‘y’, ‘t’, ‘yes’, ‘no’, ‘off’

Boolean True or False

Convert a human-readable string value to bytes

Raises TypeError if unable to convert the value

Verify that value is a dict or convert it to a dict and return it.

Raises TypeError if unable to convert to a dict

value – Dict or string to convert to a dict. Accepts k1=v2, k2=v2 or k1=v2 k2=v2.

value converted to a dictionary

Verify that value is a float or convert it to a float and return it

Raises TypeError if unable to convert to a float

value – float, int, str, or bytes to verify or convert and return.

float of given value.

Verify that the value is an integer and return it or convert the value to an integer and return it

Raises TypeError if unable to convert to an int

value – String or int to convert of verify

JSON serialize dict/list/tuple, strip str and bytes. Previously required for cases where Ansible/Jinja classic-mode literal eval pass could inadvertently deserialize objects.

Verify that the value is a list or convert to a list

A comma separated string will be split into a list. Raises a TypeError if unable to convert to a list.

value – Value to validate or convert to a list

Original value if it is already a list, single item list if a float, int, or string without commas, or a multi-item list if a comma-delimited string.

Verify the provided value is a string or convert it to a string, then return the expanded path

Returns the raw value

Verify that the value is a string or convert to a string.

Since unexpected changes can sometimes happen when converting to a string, allow_conversion controls whether or not the value will be converted or a TypeError will be raised if the value is not a string and would be converted

value – Value to validate or convert to a string

allow_conversion – Whether to convert the string and return it or raise a TypeError

Original value if it is a string, the value converted to a string if allow_conversion=True, or raises a TypeError if allow_conversion=False.

Count the number of occurrences of a key in a given dictionary

terms – String or iterable of values to check

parameters – Dictionary of parameters

An integer that is the number of occurrences of the terms values in the provided dictionary.

Fallback validator was not found

Single argument spec validation error

The error message passed in when the exception was raised.

The error message passed in when the exception was raised.

Multiple argument spec validation errors

list of AnsibleValidationError objects

The first message from the first error in errors.

list of each error message in errors.

Append a new error to self.errors.

Only AnsibleValidationError should be added.

Append each item in errors to self.errors. Only AnsibleValidationError should be added.

Error handling aliases

Error with parameter type

Error with parameter value

Error processing parameter deprecations

Error when validating elements

Mutually exclusive parameters were supplied

Error converting no_log values

Error with parameters that are required by other parameters

A required parameter was assigned a default value

Missing a required parameter

Error with conditionally required parameters

Error with parameters where at least one is required

Error with parameters that are required together

Incorrect type for subparameter

Unsupported parameters were supplied

**Examples:**

Example 1 (unknown):
```unknown
argument_spec = {
    'name': {'type': 'str'},
    'age': {'type': 'int'},
}

parameters = {
    'name': 'bo',
    'age': '42',
}

validator = ArgumentSpecValidator(argument_spec)
result = validator.validate(parameters)

if result.error_messages:
    sys.exit("Validation failed: {0}".format(", ".join(result.error_messages))

valid_params = result.validated_parameters
```

Example 2 (unknown):
```unknown
required_if=[
    ['state', 'present', ('path',), True],
    ['someint', 99, ('bool_param', 'string_param')],
]
```

Example 3 (unknown):
```unknown
[
    {
        'parameter': 'someint',
        'value': 99
        'requirements': ('bool_param', 'string_param'),
        'missing': ['string_param'],
        'requires': 'all',
    }
]
```

---

## Return Values — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/common_return_values.html

**Contents:**
- Return Values
- Common
  - backup_file
  - changed
  - diff
  - failed
  - invocation
  - msg
  - rc
  - results

Ansible modules normally return a data structure that can be registered into a variable, or seen directly when output by the ansible program. Each module can optionally document its own unique return values (visible through ansible-doc and on the main docsite).

This document covers return values common to all modules.

Some of these keys might be set by Ansible itself once it processes the module’s return information.

For those modules that implement backup=no|yes when manipulating files, a path to the backup file created if original file was changed.

A boolean indicating if the task had to make changes to the target or delegated host.

Information on differences between the previous and current state. Often a dictionary with entries before and after, which will then be formatted by the callback plugin to a diff view.

A boolean that indicates if the task was failed or not.

Information on how the module was invoked.

A string with a generic message relayed to the user.

Some modules execute command line utilities or are geared for executing commands directly (raw, shell, command, and so on), this field contains ‘return code’ of these utilities.

If this key exists, it indicates that a loop was present for the task and that it contains a list of the normal module ‘result’ per item.

A boolean that indicates if the task was skipped or not

Some modules execute command line utilities or are geared for executing commands directly (raw, shell, command, and so on), this field contains the error output of these utilities.

When stderr is returned we also always provide this field which is a list of strings, one item per line from the original.

Some modules execute command line utilities or are geared for executing commands directly (raw, shell, command, and so on). This field contains the normal output of these utilities.

When stdout is returned, Ansible always provides a list of strings, each containing one item per line from the original output.

These keys can be added by modules but will be removed from registered variables; they are ‘consumed’ by Ansible itself.

This key should contain a dictionary which will be appended to the facts assigned to the host. These will be directly accessible and don’t require using a registered variable.

This key can contain traceback information caused by an exception in a module. It will only be displayed on high verbosity (-vvv).

This key contains a list of strings that will be presented to the user.

This key contains a list of dictionaries that will be presented to the user. Keys of the dictionaries are msg and version, values are string, value for the version key can be an empty string.

Browse existing collections, modules, and plugins

Browse source of core and extras modules

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
"backup_file": "./foo.txt.32729.2020-07-30@06:24:19~"
```

Example 2 (unknown):
```unknown
"changed": true
```

Example 3 (unknown):
```unknown
"diff": [
        {
            "after": "",
            "after_header": "foo.txt (content)",
            "before": "",
            "before_header": "foo.txt (content)"
        },
        {
            "after_header": "foo.txt (file attributes)",
            "before_header": "foo.txt (file attributes)"
        }
```

Example 4 (unknown):
```unknown
"failed": false
```

---

## Special Variables — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/special_variables.html

**Contents:**
- Special Variables
- Magic variables
- Facts
- Connection variables

These variables cannot be set directly by the user; Ansible will always override them to reflect internal state.

Boolean that indicates if we are in check mode or not

The name of the collection the task that is executing is a part of. In the format of namespace.collection

The full path of used Ansible configuration file

The names of the roles currently imported into the current play as dependencies of other plays

Boolean that indicates if we are in diff mode or not

Integer reflecting the number of maximum forks available to this run

The name of the value provided to loop_control.index_var. Added in 2.9

List of sources used as inventory

Contents of the --limit CLI option for the current execution of Ansible

A dictionary/map containing extended loop information when enabled through loop_control.extended

The name of the value provided to loop_control.loop_var. Added in 2.8

When the current role is being executed by means of an include_role or import_role action, this variable contains a list of all parent roles, with the most recent role (in other words, the role that included/imported this role) being the first item in the list. When multiple inclusions occur, this list lists the last role (in other words, the role that included this role) as the first item in the list. It is also possible that a specific role exists more than once in this list.

For example: When role A includes role B, inside role B, ansible_parent_role_names will equal to ['A']. If role B then includes role C, the list becomes ['B', 'A'].

When the current role is being executed by means of an include_role or import_role action, this variable contains a list of all parent roles paths, with the most recent role (in other words, the role that included/imported this role) being the first item in the list. Please refer to ansible_parent_role_names for the order of items in this list.

List of active hosts in the current play run limited by the serial, aka ‘batch’. Failed/Unreachable hosts are not considered ‘active’.

List of hosts in the current play run, not limited by the serial. Failed/Unreachable hosts are excluded from this list.

List of all the hosts that were targeted by the play

The name of the currently executed play. Added in 2.8. (name attribute of the play, not file name of the playbook.)

The names of the roles currently imported into the current play. This list does not contain the role names that are implicitly included through dependencies.

The path to the python interpreter being used by Ansible on the control node

The fully qualified collection role name, in the format of namespace.collection.role_name

The names of the roles currently imported into the current play, or roles referenced as dependencies of the roles imported into the current play.

Contents of the --tags CLI option, which specifies which tags will be included for the current run. Note that if --tags is not passed, this variable will default to ["all"].

Current search path for action plugins and lookups, in other words, where we search for relative paths when you do template: src=myfile

Contents of the --skip-tags CLI option, which specifies which tags will be skipped for the current run.

Current verbosity setting for Ansible

Dictionary/map that contains information about the current running version of ansible, it has the following keys: full, major, minor, revision and string.

List of groups the current host is part of, it always reflects the inventory_hostname and ignores delegation.

A dictionary/map with all the groups in inventory and each group has the list of hosts that belong to it

A dictionary/map with all the hosts in inventory and variables assigned to them

The directory of the inventory source in which the inventory_hostname was first defined. This always reflects the inventory_hostname and ignores delegation.

The inventory name for the ‘current’ host being iterated over in the play. This is not affected by delegation, it always reflects the original host for the task

The short version of inventory_hostname, is the first section after splitting it via .. As an example, for the inventory_hostname of www.example.com, www would be the inventory_hostname_short This is affected by delegation, so it will reflect the ‘short name’ of the delegated host

The file name of the inventory source in which the inventory_hostname was first defined. Ignores delegation and always reflects the information for the inventory_hostname.

Special variable that allows you to ‘omit’ an option in a task, for example - user: name=bob home={{ bobs_home|default(omit) }}

Deprecated, the same as ansible_play_batch

The path to the directory of the current playbook being executed. NOTE: This might be different than directory of the playbook passed to the ansible-playbook command line when a playbook contains a import_playbook statement.

The name of the role currently being executed.

Deprecated, the same as ansible_play_role_names

The path to the dir of the currently running role

These are variables that contain information pertinent to the current host (inventory_hostname). They are only available if gathered first. See Discovering variables: facts and magic variables for more information.

Contains any facts gathered or cached for the inventory_hostname Facts are normally gathered by the setup module automatically in a play, but any module can return facts.

Contains any ‘local facts’ gathered or cached for the inventory_hostname. The keys available depend on the custom facts created. See the setup module and facts.d or local facts for more details.

Connection variables are normally used to set the specifics on how to execute actions on a target. Most of them correspond to connection plugins, but not all are specific to them; other plugins like shell, terminal and become are normally involved. Only the common ones are described as each connection/become/shell/etc plugin can define its own overrides and specific variables. See Controlling how Ansible behaves: precedence rules for how connection variables interact with configuration settings, command-line options, and playbook keywords.

The user Ansible ‘becomes’ after using privilege escalation. This must be available to the ‘login user’.

The connection plugin actually used for the task on the target host.

The ip/name of the target host to use instead of inventory_hostname.

The path to the Python executable Ansible should use on the target host.

The user Ansible ‘logs in’ as.

---

## Controlling how Ansible behaves: precedence rules — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/general_precedence.html

**Contents:**
- Controlling how Ansible behaves: precedence rules
- Precedence categories
  - Configuration settings
  - Command-line options
  - Playbook keywords
  - Variables
    - Variable scope: how long is a value available?
    - Using -e extra variables at the command line
  - Direct Assignment

To give you maximum flexibility in managing your environments, Ansible offers many ways to control how Ansible behaves: how it connects to managed nodes, how it works once it has connected. If you use Ansible to manage a large number of servers, network devices, and cloud resources, you may define Ansible behavior in several different places and pass that information to Ansible in several different ways. This flexibility is convenient, but it can backfire if you do not understand the precedence rules.

These precedence rules apply to any setting that can be defined in multiple ways (by configuration settings, command-line options, playbook keywords, variables).

Precedence categories

Configuration settings

Variable scope: how long is a value available?

Using -e extra variables at the command line

Ansible offers four sources for controlling its behavior. In order of precedence from lowest (most easily overridden) to highest (overrides all others), the categories are:

Configuration settings

Each category overrides any information from all lower-precedence categories. For example, a playbook keyword will override any configuration setting.

Within each precedence category, specific rules apply. However, generally speaking, ‘last defined’ wins and overrides any previous definitions.

Configuration settings include both values from the ansible.cfg file and environment variables. Within this category, values set in configuration files have lower precedence. Ansible uses the first ansible.cfg file it finds, ignoring all others. Ansible searches for ansible.cfg in these locations in order:

ANSIBLE_CONFIG (environment variable if set)

ansible.cfg (in the current directory)

~/.ansible.cfg (in the home directory)

/etc/ansible/ansible.cfg

Environment variables have a higher precedence than entries in ansible.cfg. If you have environment variables set on your control node, they override the settings in whichever ansible.cfg file Ansible loads. The value of any given environment variable follows normal shell precedence: the last value defined overwrites previous values.

Any command-line option will override any configuration setting.

When you type something directly at the command line, you may feel that your hand-crafted values should override all others, but Ansible does not work that way. Command-line options have low precedence - they override configuration only. They do not override playbook keywords, variables from inventory or variables from playbooks.

You can override all other settings from all other sources in all other precedence categories at the command line by Using -e extra variables at the command line, but that is not a command-line option, it is a way of passing a variable.

At the command line, if you pass multiple values for a parameter that accepts only a single value, the last defined value wins. For example, this ad hoc task will connect as carol, not as mike:

Some parameters allow multiple values. In this case, Ansible will append all values from the hosts listed in inventory files inventory1 and inventory2:

The help for each command-line tool lists available options for that tool.

Any playbook keyword will override any command-line option and any configuration setting.

Within playbook keywords, precedence flows with the playbook itself; the more specific wins against the more general:

blocks/includes/imports/roles (optional and can contain tasks and each other)

tasks (most specific)

In this example, the connection keyword is set to ssh at the play level. The first task inherits that value, and connects using ssh. The second task inherits that value, overrides it, and connects using paramiko. The same logic applies to blocks and roles as well. All tasks, blocks, and roles within a play inherit play-level keywords; any task, block, or role can override any keyword by defining a different value for that keyword within the task, block, or role.

Remember that these are KEYWORDS, not variables. Both playbooks and variable files are defined in YAML but they have different significance. Playbooks are the command or ‘state description’ structure for Ansible, variables are data we use to help make playbooks more dynamic.

Ansible variables are very high on the precedence stack. They will override any playbook keyword, any command-line option, environment variable and any configuration file setting.

Variables that have equivalent playbook keywords, command-line options, and configuration settings are known as Connection variables. Originally designed for connection parameters, this category has expanded to include other core variables like the temporary directory and the python interpreter.

Connection variables, like all variables, can be set in multiple ways and places. You can define variables for hosts and groups in inventory. You can define variables for tasks and plays in vars: blocks in playbooks. However, they are still variables - they are data, not keywords or configuration settings. Variables that override playbook keywords, command-line options, and configuration settings follow the same rules of variable precedence as any other variables.

When set in a playbook, variables follow the same inheritance rules as playbook keywords. You can set a value for the play, then override it in a task, block, or role:

Variable values set in a playbook exist only within the playbook object that defines them. These ‘playbook object scope’ variables are not available to subsequent objects, including other plays.

Variable values associated directly with a host or group, including variables defined in inventory, by vars plugins, or using modules like set_fact and include_vars, are available to all plays. These ‘host scope’ variables are also available through the hostvars[] dictionary.

Variables set through extra vars have a global scope for the current run and will be present both as ‘playbook object vars’ and ‘hostvars’.

To override all other variables, you can use extra variables: --extra-vars or -e at the command line. Values passed with -e, while still a command-line option itself, have the highest precedence among variables and will, a bit counter intuitively, be of the higher precedence among most configuration sources, since variables themselves have high precedence. For example, this task will connect as brian not as carol:

You must specify both the variable name and the value with --extra-vars.

This category only applies to things that take direct options, generally modules and some plugin types. Most modules and action plugins do not have any other way to assign settings so precedence rarely comes up in that context, but it still possible for some of them to do so and should be reflected in the documentation.

Outside of task actions, the most recognizable ‘direct assignments’ are with lookup, filter and test plugins:

Though most of these are not configured in other ways, specially tests, it is possible for plugins and filters to use input from other configuration sources if specified in their documentation.

Inventory plugins are a bit tricky as they use ‘inventory sources’ and these sometimes can look like a configuration file and are passed in as a command line option, yet it is still considered ‘direct assignment’. It is a bit clearer when using an inline source -i host1, host2, host3 than when using a file source -i /path/to/inventory_source, but they both have the same precedence.

**Examples:**

Example 1 (unknown):
```unknown
ansible -u mike -m ping myhost -u carol
```

Example 2 (unknown):
```unknown
ansible -i /path/inventory1 -i /path/inventory2 -m ping all
```

Example 3 (unknown):
```unknown
- hosts: all
  connection: ssh
  tasks:
    - name: This task uses ssh.
      ping:

    - name: This task uses paramiko.
      connection: paramiko
      ping:
```

Example 4 (unknown):
```unknown
- hosts: cloud
  gather_facts: false
  become: true
  vars:
    ansible_become_user: admin
  tasks:
    - name: This task uses admin as the become user.
      dnf:
        name: some-service
        state: latest
    - block:
        - name: This task uses service-admin as the become user.
          # a task to configure the new service
        - name: This task also uses service-admin as the become user, defined in the block.
          # second task to configure the service
      vars:
        ansible_become_user: service-admin
    - name: This task (outside of the block) uses admin as the become user again.
      service:
        name: some-service
        state: restarted
```

---

## Logging Ansible output — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/logging.html

**Contents:**
- Logging Ansible output
- Protecting sensitive data with no_log

By default, Ansible sends output about plays, tasks, and module arguments to your screen (STDOUT) on the control node. If you want to capture Ansible output in a log, you have three options:

To save Ansible output in a single log on the control node, set the log_path configuration file setting. You may also want to set display_args_to_stdout, which helps to differentiate similar tasks by including variable values in the Ansible output.

To save Ansible output in separate logs, one on each managed node, set the no_target_syslog and syslog_facility configuration file settings.

To save Ansible output to a secure database, use AWX or Red Hat Ansible Automation Platform. You can then review history based on hosts, projects, and particular inventories over time, using graphs and/or a REST API.

If you save Ansible output to a log, you expose any secret data in your Ansible output, such as passwords and usernames. To keep sensitive values out of your logs, mark tasks that expose them with the no_log: True attribute. However, the no_log attribute does not affect debugging output, so be careful not to debug playbooks in a production environment. See How do I keep secret data in my playbook? for an example.

---

## Releases and maintenance — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/release_and_maintenance.html

**Contents:**
- Releases and maintenance
- Release cycle overview
  - Ansible community package release cycle
  - Ansible community changelogs
  - ansible-core release cycle
  - ansible-core control node Python support
  - ansible-core target node Python support
  - ansible-core target node PowerShell and Windows support
  - ansible-core support matrix
  - ansible-core versioning

This section describes release cycles, rules, and maintenance schedules for both Ansible community projects: the Ansible community package and ansible-core. The two projects have different versioning systems, maintenance structures, contents, and workflows.

Ansible community package

Uses new versioning (2.10, then 3.0.0)

Continues “classic Ansible” versioning (2.11, then 2.12)

Follows semantic versioning rules

Does not use semantic versioning

Maintains only one version at a time

Maintains latest version plus two older versions

Includes language, runtime, and selected Collections

Includes language, runtime, and builtin plugins

Developed and maintained in Collection repositories

Developed and maintained in ansible/ansible repository

Many community users install the Ansible community package. The Ansible community package offers the functionality that existed in Ansible 2.9, with more than 85 Collections containing thousands of modules and plugins. The ansible-core option is primarily for developers and users who want to install only the collections they need.

Release cycle overview

Ansible community package release cycle

Ansible community changelogs

ansible-core release cycle

ansible-core control node Python support

ansible-core target node Python support

ansible-core target node PowerShell and Windows support

ansible-core support matrix

ansible-core versioning

What is the X in X.Y.Z?

What is the Y in X.Y.Z?

What is the Z in X.Y.Z?

Preparing for a new release

Development and maintenance workflows

Ansible community package workflow

ansible-core workflow

Generating changelogs

Ansible community package deprecation cycle

ansible-core deprecation cycle

The two community releases are related - the release cycle follows this pattern:

Release of a new ansible-core major version, for example, ansible-core 2.11

New release of ansible-core and two prior versions are now maintained (in this case, ansible-base 2.10, Ansible 2.9)

Work on new features for ansible-core continues in the devel branch

Collection freeze (no new Collections or new versions of existing Collections) on the Ansible community package

Release candidate for Ansible community package, testing, additional release candidates as necessary

Release of a new Ansible community package major version based on the new ansible-core, for example, Ansible 4.0.0 based on ansible-core 2.11

Newest release of the Ansible community package is the only version now maintained

Work on new features continues in Collections

Individual Collections can make multiple minor and major releases

Minor releases of three maintained ansible-core versions every four weeks (2.11.1)

Minor releases of the single maintained Ansible community package version every four weeks (4.1.0)

Feature freeze on ansible-core

Release candidate for ansible-core, testing, additional release candidates as necessary

Release of the next ansible-core major version, cycle begins again

The Ansible community team typically releases two major versions of the community package per year, on a flexible release cycle that trails the release of ansible-core. This cycle can be extended to allow for larger changes to be properly implemented and tested before a new release is made available. See Ansible Roadmap for upcoming release details. Between major versions, we release a new minor version of the Ansible community package every four weeks. Minor releases include new backwards-compatible features, modules and plugins, as well as bug fixes.

Starting with version 2.10, the Ansible community team guarantees maintenance for only one major community package release at a time. For example, when Ansible 4.0.0 gets released, the team will stop making new 3.x releases. Community members may maintain older versions if desired.

Each Ansible EOL version may issue one final maintenance release at or shortly after the first release of the next version. When this happens, the final maintenance release is EOL at the date it releases.

Older, unmaintained versions of the Ansible community package might contain unfixed security vulnerabilities (CVEs). If you are using a release of the Ansible community package that is no longer maintained, we strongly encourage you to upgrade as soon as possible to benefit from the latest features and security fixes.

Each major release of the Ansible community package accepts the latest released version of each included Collection and the latest released version of ansible-core. For specific schedules and deadlines, see the Ansible Roadmap for each version. Major releases of the Ansible community package can contain breaking changes in the modules and other plugins within the included Collections and in core features.

The Ansible community package follows semantic versioning rules. Minor releases of the Ansible community package accept only backwards-compatible changes in included Collections, that is, not Collections major releases. Collections must also use semantic versioning, so the Collection version numbers reflect this rule. For example, if Ansible 3.0.0 releases with community.general 2.0.0, then all minor releases of Ansible 3.x (such as Ansible 3.1.0 or Ansible 3.5.0) must include a 2.x release of community.general (such as 2.8.0 or 2.9.5) and not 3.x.x or later major releases.

Work in Collections is tracked within the individual Collection repositories.

You can refer to the Ansible package porting guides for tips on updating your playbooks to run on newer versions of Ansible. For Ansible 2.10 and later releases, you can install the Ansible package with pip. See Installing Ansible for details. You can download older Ansible releases from https://releases.ansible.com/ansible/.

This table links to the changelogs for each major Ansible release. These changelogs contain the dates and significant changes in each minor release.

Ansible Community Package Release

Core version dependency

In development (unreleased)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

Unmaintained (end of life)

ansible-core is developed and released on a flexible release cycle. We can extend this cycle to properly implement and test larger changes before a new release is made available. See ansible-core Roadmaps for upcoming release details.

ansible-core has a graduated maintenance structure that extends to three major releases. For more information, read about the Development and maintenance workflows or see the chart in ansible-core control node Python support for the degrees to which current releases are maintained.

Older, unmaintained versions of ansible-core can contain unfixed security vulnerabilities (CVEs). If you are using a release of ansible-core that is no longer maintained, we strongly encourage you to upgrade as soon as possible to benefit from the latest features and security fixes. ansible-core maintenance continues for 3 releases. Thus the latest release receives security and general bug fixes when it is first released, security and critical bug fixes when the next ansible-core version is released, and only security fixes once the follow on to that version is released.

You can refer to the Ansible Core Porting Guides for tips on updating your playbooks to run on newer versions of ansible-core.

You can install ansible-core with pip. See Installing Ansible for details.

Starting with ansible-core version 2.12, each release includes control node support for the three most recently released Python versions.

Starting with ansible-core version 2.16, each release includes target node support for:

The 6 most recently released Python versions.

The 7 most recently released Python versions every 6th ansible-core release (2.16, 2.22, etc.)

Support for Python 2.7 is included in ansible-core version 2.16 and earlier.

ansible-core on Windows supports the baseline version of PowerShell that each Windows version ships with. For example, Windows Server 2016 shipped with PowerShell 5.1 so Ansible will support PowerShell 5.1 for the life of Windows Server 2016 support. Support for each Windows version is determined by the Windows lifecycle policy and when each version reaches the extended end date. For example Windows Server 2012 and 2012 R2 extended end date was for October 10th 2023 while Windows Server 2016 is January 12th 2027. Windows support does not align with the 3 year Extended Security Updates (ESU) support from Microsoft which is a paid support option for products that are past the normal end of support date from Microsoft.

This table links to the changelogs for each major ansible-core release. These changelogs contain the dates and significant changes in each minor release. Dates listed indicate the start date of the maintenance cycle.

Target Python / PowerShell

The ansible-core project uses a historical versioning scheme, most similar to the versioning scheme used by Python.

This scheme follows the formatting of X.Y.Z which is described in detail below.

The X represents the internal architecture of ansible-core. The X here does not imply any form of compatibility, nor anything about the scope of the changes.

v1 can be best described as the internal architecture revolving around ansible.runner.Runner as the “execution” engine

v2 can be best described as the internal architecture revolving around the TaskQueueManager, PlayIterator, and the strategy as the “execution” engine

Approximately every 6 months, in May and November ansible-core releases a new Major release. This is denoted by the Y in the X.Y.Z version scheme.

Although the Y denotes the Major version, it is not referenced independently, and instead a Major version is indicated in the format of X.Y, such as 2.16.

As such, versions like 2.9.0, 2.10.0, 2.11.0, 2.16.0 and 2.19.0 are all major releases. X.Y.0 releases do not carry any guarantee of 100% backwards compatibility with the version before it. Some may be more or less impactful based on the scope of the work for the release. Check porting guides for changes that may necessitate user intervention.

This is the patch version. ansible-core operates on a 4 week patch schedule. The Z release of a major version will include bugfixes and security fixes as outlined in the ansible-core support matrix.

During final preparations for a new release, core developers and maintainers focus on improving the release candidate, not on adding or reviewing new features. We may impose a feature freeze.

A feature freeze means that we delay new features and fixes unrelated to the pending release so we can create the new release as soon as possible.

We create at least one release candidate before each new major release of Ansible or ansible-core. Release candidates allow the Ansible community to try out new features, test existing playbooks on the release candidate, and report bugs or issues they find.

Ansible and ansible-core tag the first release candidate (RC1) which is usually scheduled to last five business days. If no major bugs or issues are identified during this period, the release candidate becomes the final release.

If there are major problems with the first candidate, the team and the community fix them and tag a second release candidate (RC2). This second candidate lasts for a shorter duration than the first. If no problems have been reported for an RC2 after two business days, the second release candidate becomes the final release.

If there are major problems in RC2, the cycle begins again with another release candidate and repeats until the maintainers agree that all major problems have been fixed.

In between releases, the Ansible community develops new features, maintains existing functionality, and fixes bugs in ansible-core and in the collections included in the Ansible community package.

The Ansible community develops and maintains the features and functionality included in the Ansible community package in Collections repositories, with a workflow that looks like this:

Developers add new features and bug fixes to the individual Collections, following each Collection’s rules on contributing.

Each new feature and each bug fix includes a changelog fragment describing the work.

Release engineers create a minor release for the current version every four weeks to ensure that the latest bug fixes are available to users.

At the end of the development period, the release engineers announce which Collections, and which major version of each included Collection, will be included in the next release of the Ansible community package. New Collections and new major versions may not be added after this, and the work of creating a new release begins.

We generally do not provide fixes for unmaintained releases of the Ansible community package, however, there can sometimes be exceptions for critical issues.

Some Collections are maintained by the Ansible team, some by Partner organizations, and some by community teams. For more information on adding features or fixing bugs in Ansible-maintained Collections, see Contributing to Ansible-maintained Collections.

The Ansible community develops and maintains ansible-core on GitHub, with a workflow that looks like this:

Developers add new features and bug fixes to the devel branch.

Each new feature and each bug fix includes a changelog fragment describing the work.

The development team backports bug fixes to one, two, or three stable branches, depending on the severity of the bug. They do not backport new features.

Release engineers create a minor release for each maintained version every four weeks to ensure that the latest bug fixes are available to users.

At the end of the development period, the release engineers impose a feature freeze and the work of creating a new release begins.

We generally do not provide fixes for unmaintained releases of ansible-core, however, there can sometimes be exceptions for critical issues.

For more information about adding features or fixing bugs in ansible-core see The Ansible Development Cycle.

We generate changelogs based on fragments. When creating new features for existing modules and plugins or fixing bugs, create a changelog fragment describing the change. A changelog entry is not needed for new modules or plugins. Details for those items will be generated from the module documentation.

To add changelog fragments to Collections in the Ansible community package, we recommend the antsibull-changelog utility.

To add changelog fragments for new features and bug fixes in ansible-core, see the changelog examples and instructions in the Community Guide.

Sometimes we remove a feature, normally in favor of a reimplementation that we hope does a better job. To do this we have a deprecation cycle. First we mark a feature as ‘deprecated’. This is normally accompanied with warnings to the user as to why we deprecated it, what alternatives they should switch to and when (which version) we are scheduled to remove the feature permanently.

Since Ansible is a package of individual collections, the deprecation cycle depends on the collection maintainers. We recommend the collection maintainers deprecate a feature in one Ansible major version and do not remove that feature for one year, or at least until the next major Ansible version. For example, deprecate the feature in 3.1.0 and do not remove the feature until 5.0.0 or 4.0.0 at the earliest. Collections should use semantic versioning, such that the major collection version cannot be changed within an Ansible major version. Therefore, the removal should not happen before the next major Ansible community package release. This is up to each collection maintainer and cannot be guaranteed.

The deprecation cycle in ansible-core is normally across 4 feature releases (2.x. where the x marks a feature release). The feature is normally removed in the 4th release after we announce the deprecation. For example, something deprecated in 2.10 will be removed in 2.13. The tracking is tied to the number of releases, not the release numbering itself. Although this is the standard, there are times where a deprecation cycle for a feature or behavior may have a longer or shorter deprecation cycle based on use or urgency of removal. Unintended or undocumented functionality may be removed without a deprecation cycle. In this context, unintended functionality refers specifically to emergent features that occur outside the release roadmap.

Guidelines for Ansible Core contributors and maintainers

Community information and contributing

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Glossary — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/glossary.html

**Contents:**
- Glossary

The following is a list (and re-explanation) of term definitions used elsewhere in the Ansible documentation.

Consult the documentation home page for the full documentation and to see the terms in context, but this should be a good resource to check your knowledge of Ansible’s components and understand how they fit together. It is something you might wish to read for review or when a term comes up on the Ansible Forum.

An action is a part of a task that specifies which of the modules to run and which arguments to pass to that module. Each task can have only one action, but it may also have other parameters.

Refers to running Ansible to perform some quick command, using /usr/bin/ansible, rather than the orchestration language, which is /usr/bin/ansible-playbook. An example of an ad hoc command might be rebooting 50 machines in your infrastructure. Anything you can do ad hoc can be accomplished by writing a playbook and playbooks can also glue several other operations together.

A software package (Python, deb, rpm, and so on) that contains ansible-core and a select group of collections. Playbooks that worked with Ansible 2.9 should still work with the Ansible 2.10 package. See the ansible-<version>.build file in the release-specific directory at ansible-build-data for a list of collections included in Ansible, as well as the included ansible-core version.

Used only for 2.10. The installable package (RPM/Python/Deb package) generated from the ansible/ansible repository. See ansible-core.

Name used starting with 2.11. The installable package (RPM/Python/Deb package) generated from the ansible/ansible repository. Contains the command-line tools and the code for basic features and functions, such as copying module code to managed nodes. The ansible-core package includes a few modules and plugins and allows you to add others by installing collections.

An online distribution server for finding and sharing Ansible community content, sometimes referred to as community Galaxy. Also, the command-line utility that lets users install individual Ansible Collections, for example ansible-galaxy collection install community.crypto.

Refers to a task that is configured to run in the background rather than waiting for completion. If you have a long process that would run longer than the SSH timeout, it would make sense to launch that task in async mode. Async modes can poll for completion every so many seconds or can be configured to “fire and forget”, in which case Ansible will not even check on the task again; it will just kick it off and proceed to future steps. Async modes work with both /usr/bin/ansible and /usr/bin/ansible-playbook.

Refers to some user-written code that can intercept results from Ansible and do something with them. Some supplied examples in the GitHub project perform custom logging, send email, or even play sound effects.

Refers to running Ansible with the --check option, which does not make any changes on the remote systems, but only outputs the changes that might occur if the command ran without this flag. This is analogous to so-called “dry run” modes in other systems, though the user should be warned that this does not take into account unexpected command failures or cascade effects (which is true of similar modes in other systems). Use this to get an idea of what might happen, but do not substitute it for a good staging environment.

A packaging format for bundling and distributing Ansible content, including plugins, roles, modules, and more. Collections release independent of other collections or ansible-core so features can be available sooner to users. Some collections are packaged with Ansible (version 2.10 or later). You can install other collections (or other versions of collections) with ansible-galaxy collection install <namespace.collection>.

The second part of a Fully Qualified Collection Name. The collection name divides the collection namespace and usually reflects the function of the collection content. For example, the cisco namespace might contain cisco.ios, cisco.aci, and cisco.nxos, with content for managing the different network devices maintained by Cisco.

A special collection managed by the Ansible Community Team containing all the modules and plugins which shipped in Ansible 2.9 that do not have their own dedicated Collection. See community.general on Galaxy.

Similar to community.general, focusing on network content. community.network on Galaxy.

By default, Ansible talks to remote machines through pluggable libraries. Ansible uses native OpenSSH (SSH (Native)) or a Python implementation called paramiko. OpenSSH is preferred if you are using a recent version, and also enables some features like Kerberos and jump hosts. This is covered in the getting started section. There are also other connection types like accelerate mode, which must be bootstrapped over one of the SSH-based connection types but is very fast, and local mode, which acts on the local system. Users can also write their own connection plugins.

A conditional is an expression that evaluates to true or false that decides whether a given task is executed on a given machine or not. Ansible’s conditionals are powered by the ‘when’ statement, which are discussed in the Working with playbooks.

An approach to achieving a task that uses a description of the final state rather than a description of the sequence of steps necessary to achieve that state. For a real world example, a declarative specification of a task would be: “put me in California”. Depending on your current location, the sequence of steps to get you to California may vary, and if you are already in California, nothing at all needs to be done. Ansible’s Resources are declarative; it figures out the steps needed to achieve the final state. It also lets you know whether or not any steps needed to be taken to get to the final state.

A --diff flag can be passed to Ansible to show what changed on modules that support it. You can combine it with --check to get a good ‘dry run’. File diffs are normally in unified diff format.

A server, such as Ansible Galaxy or Red Hat Automation Hub where you can distribute your collections and allow others to access these collections. See Distributing collections for a list of distribution server types. Some Ansible features are only available on certain distribution servers.

A core software component of Ansible that is the power behind /usr/bin/ansible directly – and corresponds to the invocation of each task in a playbook. The Executor is something Ansible developers may talk about, but it is not really user land vocabulary.

Facts are simply things that are discovered about remote nodes. While they can be used in playbooks and templates just like variables, facts are things that are inferred, rather than set. Facts are automatically discovered by Ansible when running plays by executing the internal setup module on the remote nodes. You never have to call the setup module explicitly, it just runs, but it can be disabled to save time if it is not needed or you can tell ansible to collect only a subset of the full facts through the gather_subset: option. For the convenience of users who are switching from other configuration management systems, the fact module will also pull in facts from the ohai and facter tools if they are installed. These are fact libraries from Chef and Puppet, respectively. (These may also be disabled through gather_subset:)

A filter plugin is something that most users will never need to understand. These allow for the creation of new Jinja2 filters, which are more or less only of use to people who know what Jinja2 filters are. If you need them, you can learn how to write them in the API docs section.

Ansible talks to remote nodes in parallel and the level of parallelism can be set either by passing --forks or editing the default in a configuration file. The default is a very conservative five (5) forks, though if you have a lot of RAM, you can easily set this to a value like 50 for increased parallelism.

The full definition of a module, plugin, or role hosted within a collection, in the form <namespace.collection.content_name>. Allows a Playbook to refer to a specific module or plugin from a specific source in an unambiguous manner, for example, community.grafana.grafana_dashboard. The FQCN is required when you want to specify the exact source of a plugin. For example, if multiple collections contain a module plugin called user, the FQCN specifies which one to use for a given task. When you have multiple collections installed, the FQCN is always the explicit and authoritative indicator of which collection to search for the correct plugin for each task.

Facts are mentioned above. Sometimes when running a multi-play playbook, it is desirable to have some plays that don’t bother with fact computation if they aren’t going to need to utilize any of these values. Setting gather_facts: False on a playbook allows this implicit fact gathering to be skipped.

Globbing is a way to select several hosts based on wildcards, rather than the name of the host specifically, or the name of the group they are in. For example, it is possible to select ww* to match all hosts starting with www. This concept is pulled directly from Func, one of Michael DeHaan’s (an Ansible Founder) earlier projects. In addition to basic globbing, various set operations are also possible, such as ‘hosts in this group and not in another group’, and so on.

A group consists of several hosts assigned to a pool that can be conveniently targeted together, as well as given variables that they share in common.

The group_vars/ files are files that live in a directory alongside an inventory file, with an optional file name named after each group. This is a convenient place to put variables that are provided to a given group, especially complex data structures, so that these variables do not have to be embedded in the inventory file or playbook.

Handlers are just like regular tasks in an Ansible playbook (see Tasks) but are only run if the Task contains a notify keyword and also indicates that it changed something. For example, if a config file is changed, then the task referencing the config file templating operation may notify a service restart handler. This means services can be bounced only if they need to be restarted. Handlers can be used for things other than service restarts, but service restarts are the most common usage.

A host is simply a remote machine that Ansible manages. They can have individual variables assigned to them, and can also be organized in groups. All hosts have a name they can be reached at (which is either an IP address or a domain name) and, optionally, a port number, if they are not to be accessed on the default SSH port.

Each Play in Ansible maps a series of tasks (which define the role, purpose, or orders of a system) to a set of systems.

This hosts: keyword in each play is often called the hosts specifier.

It may select one system, many systems, one or more groups, or even some hosts that are in one group and explicitly not in another.

Just like Group Vars, a directory alongside the inventory file named host_vars/ can contain a file named after each hostname in the inventory file, in YAML format. This provides a convenient place to assign variables to the host without having to embed them in the inventory file. The Host Vars file can also be used to define complex data structures that can’t be represented in the inventory file.

An operation is idempotent if the result of performing it once is exactly the same as the result of performing it repeatedly without any intervening actions.

The idea that playbook files (which are nothing more than lists of plays) can include other lists of plays, and task lists can externalize lists of tasks in other files, and similarly with handlers. Includes can be parameterized, which means that the loaded file can pass variables. For example, an included play for setting up a WordPress blog may take a parameter called user and that play could be included more than once to create a blog for both alice and bob.

A file (by default, Ansible uses a simple INI format) that describes Hosts and Groups in Ansible. Inventory can also be provided through an Inventory Script (sometimes called an “External Inventory Script”).

A very simple program (or a complicated one) that looks up hosts, group membership for hosts, and variable information from an external resource – whether that be a SQL database, a CMDB solution, or something like LDAP. This concept was adapted from Puppet (where it is called an “External Nodes Classifier”) and works more or less exactly the same way.

Jinja2 is the preferred templating language of Ansible’s template module. It is a very simple Python template language that is generally readable and easy to write.

Ansible uses JSON for return data from remote modules. This allows modules to be written in any language, not just Python.

The main expressions that make up Ansible, which apply to playbook objects (Play, Block, Role and Task). For example ‘vars:’ is a keyword that lets you define variables in the scope of the playbook object it is applied to.

In general, Ansible evaluates any variables in playbook content at the last possible second, which means that if you define a data structure that data structure itself can define variable values within it, and everything “just works” as you would expect. This also means variable strings can include other variables inside of those strings.

A collection of modules made available to /usr/bin/ansible or an Ansible playbook.

By passing --limit somegroup to ansible or ansible-playbook, the commands can be limited to a subset of hosts. For example, this can be used to run a playbook that normally targets an entire set of servers to one particular server.

This keyword is an alias for delegate_to: localhost. Used when you want to redirect an action from the remote to execute on the control node itself.

By using connection: local in a playbook, or passing -c local to /usr/bin/ansible, this indicates that we are executing a local fork instead of executing on the remote machine. You probably want local_action or delegate_to: localhost instead as this ONLY changes the connection and no other context for execution.

A lookup plugin is a way to get data into Ansible from the outside world. Lookup plugins are an extension of Jinja2 and can be accessed in templates, for example, {{ lookup('file','/path/to/file') }}. These are how such things as with_items, are implemented. There are also lookup plugins like file which loads data from a file and ones for querying environment variables, DNS text records, or key value stores.

Generally, Ansible is not a programming language. It prefers to be more declarative, though various constructs like loop allow a particular task to be repeated for multiple items in a list. Certain modules, like yum and apt, actually take lists directly, and can install all packages given in those lists within a single transaction, dramatically speeding up total time to configuration, so they can be used without loops.

Modules are the units of work that Ansible ships out to remote machines. Modules are kicked off by either /usr/bin/ansible or /usr/bin/ansible-playbook (where multiple tasks use several different modules in conjunction). Modules can be implemented in any language, including Perl, Bash, or Ruby – but can take advantage of some useful communal library code if written in Python. Modules just have to return JSON. Once modules are executed on remote machines, they are removed, so no long running daemons are used. Ansible refers to the collection of available modules as a library.

The concept that IT systems are not managed one system at a time, but by interactions between multiple systems and groups of systems in well defined orders. For example, a web server may need to be updated before a database server and pieces on the web server may need to be updated after THAT database server and various load balancers and monitoring servers may need to be contacted. Ansible models entire IT topologies and workflows rather than looking at configuration from a “one system at a time” perspective.

The first part of a fully qualified collection name, the namespace usually reflects a functional content category. Example: in cisco.ios.ios_config, cisco is the namespace. Namespaces are reserved and distributed by Red Hat at Red Hat’s discretion. Many, but not all, namespaces will correspond with vendor names. See Galaxy namespaces on the Galaxy docsite for namespace requirements.

The act of a task registering a change event and informing a handler task that another action needs to be run at the end of the play. If a handler is notified by multiple tasks, it will still be run only once. Handlers are run in the order they are listed, not in the order that they are notified.

Many software automation systems use this word to mean different things. Ansible uses it as a conductor would conduct an orchestra. A datacenter or cloud architecture is full of many systems, playing many parts – web servers, database servers, maybe load balancers, monitoring systems, continuous integration systems, and so on. In performing any process, it is necessary to touch systems in particular orders, often to simulate rolling updates or to deploy software correctly. Some system may perform some steps, then others, then previous systems already processed may need to perform more steps. Along the way, emails may need to be sent or web services contacted. Ansible orchestration is all about modeling that kind of process.

Ansible can use a Python SSH implementation called paramiko. The paramiko library is generally fast and easy to manage. To use paramiko you need to specify the connection type in your playbooks, or by using the -c paramiko flag.

Playbooks are the language by which Ansible orchestrates, configures, administers, or deploys systems. They are called playbooks partially because it is a sports analogy, and it is supposed to be fun using them. They aren’t workbooks :)

A playbook is a list of plays. A play is minimally a mapping between a set of hosts selected by a host specifier (usually chosen by groups but sometimes by hostname globs) and the tasks which run on those hosts to define the role that those systems will perform. There can be one or many plays in a playbook.

By default, Ansible runs in push mode, which allows it very fine-grained control over when it talks to each system. Pull mode is provided for when you would rather have nodes check in every N minutes on a particular schedule. It uses a program called ansible-pull and can also be set up (or reconfigured) using a push-mode playbook. Most Ansible users use push mode, but pull mode is included for variety and the sake of having choices.

ansible-pull works by checking configuration orders out of Git on a crontab and then managing the machine locally, using the local connection plugin.

A self-hosted distribution server based on the GalaxyNG codebase, based on Pulp version 3. Use it to find and share your own curated set of content. You can access your content with the ansible-galaxy collection command.

Push mode is the default mode of Ansible. In fact, it is not really a mode at all – it is just how Ansible works when you aren’t thinking about it. Push mode allows Ansible to be fine-grained and conduct nodes through complex orchestration processes without waiting for them to check in.

The result of running any task in Ansible can be stored in a variable for use in a template or a conditional statement. The keyword used to define the variable is called register, taking its name from the idea of registers in assembly programming (though Ansible will never feel like assembly programming). There are an infinite number of variable names you can use for registration.

Ansible modules work in terms of resources. For example, the file module will select a particular file and ensure that the attributes of that resource match a particular model. As an example, we might wish to change the owner of /etc/motd to root if it is not already set to root, or set its mode to 0644 if it is not already set to 0644. The resource models are idempotent meaning change commands are not run unless needed, and Ansible will bring the system back to a desired state regardless of the actual state – rather than you having to tell it how to get to the state.

Roles are units of organization in Ansible. Assigning a role to a group of hosts (or a set of groups, or host patterns, and so on) implies that they should implement a specific behavior. A role may include applying certain variable values, certain tasks, and certain handlers – or just one or more of these things. Because of the file structure associated with a role, roles become redistributable units that allow you to share behavior among playbooks – or even with other users.

The act of addressing a number of nodes in a group N at a time to avoid updating them all at once and bringing the system offline. For instance, in a web topology of 500 nodes handling very large volume, it may be reasonable to update 10 or 20 machines at a time, moving on to the next 10 or 20 when done. The serial: keyword in an Ansible playbooks control the size of the rolling update pool. The default is to address the batch size all at once, so this is something that you must opt-in to. OS configuration (such as making sure config files are correct) does not typically have to use the rolling update model, but can do so if desired.

Ansible does not require root logins, and since it is daemonless, definitely does not require root level daemons (which can be a security concern in sensitive environments). Ansible can log in and perform many operations wrapped in a sudo command, and can work with both password-less and password-based sudo. Some operations that don’t normally work with sudo (like scp file transfer) can be achieved with Ansible’s copy, template, and fetch modules while running in sudo mode.

Native OpenSSH as an Ansible transport is specified with -c ssh (or a config file, or a keyword in the playbook) and can be useful if wanting to login through Kerberized SSH or using SSH jump hosts, and so on. In 1.2.1, ssh will be used by default if the OpenSSH binary on the control machine is sufficiently new. Previously, Ansible selected paramiko as a default. Using a client that supports ControlMaster and ControlPersist is recommended for maximum performance – if you don’t have that and don’t need Kerberos, jump hosts, or other features, paramiko is a good choice. Ansible will warn you if it doesn’t detect ControlMaster/ControlPersist capability.

Ansible allows tagging resources in a playbook with arbitrary keywords, and then running only the parts of the playbook that correspond to those keywords. For example, it is possible to have an entire OS configuration, and have certain steps labeled ntp, and then run just the ntp steps to reconfigure the time server information on a remote host.

Playbooks exist to run tasks. Tasks combine an action (a module and its arguments) with a name and optionally some other keywords (like looping keywords). Handlers are also tasks, but they are a special kind of task that do not run unless they are notified by name when a task reports an underlying change on a remote system.

Ansible can easily transfer files to remote systems but often it is desirable to substitute variables in other files. Variables may come from the inventory file, Host Vars, Group Vars, or Facts. Templates use the Jinja2 template engine and can also include logical constructs like loops and if statements.

Ansible uses :term:Connection Plugins to define types of available transports. These are simply how Ansible will reach out to managed systems. Transports included are paramiko, ssh (using OpenSSH), and local.

An optional conditional statement attached to a task that is used to determine if the task should run or not. If the expression following the when: keyword evaluates to false, the task will be ignored.

As opposed to Facts, variables are names of values (they can be simple scalar values – integers, booleans, strings) or complex ones (dictionaries/hashes, lists) that can be used in templates and playbooks. They are declared things, not things that are inferred from the remote system’s current state or nature (which is what Facts are).

Ansible does not want to force people to write programming language code to automate infrastructure, so Ansible uses YAML to define playbook configuration languages and also variable files. YAML is nice because it has a minimum of syntax and is very clean and easy for people to skim. It is a good data format for configuration files and humans, but also machine readable. Ansible’s usage of YAML stemmed from Michael DeHaan’s first use of it inside of Cobbler around 2006. YAML is fairly popular in the dynamic language community and the format has libraries available for serialization in many languages (Python, Perl, Ruby, and so on).

Frequently asked questions

An introduction to playbooks

Tips and tricks for playbooks

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Interpreter Discovery — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html

**Contents:**
- Interpreter Discovery

Most Ansible modules that execute under a POSIX environment require a Python interpreter on the target host. Unless configured otherwise, Ansible will attempt to discover a suitable Python interpreter on each target host the first time a Python module is executed for that host.

To control the discovery behavior:

for individual hosts and groups, use the ansible_python_interpreter inventory variable

globally, use the interpreter_python key in the [defaults] section of ansible.cfg

Use one of the following values:

Detects the target OS platform, distribution, and version, then consults a table listing the correct Python interpreter and path for each platform/distribution/version. If an entry is found, and /usr/bin/python is absent, uses the discovered interpreter (and path). If an entry is found, and /usr/bin/python is present, uses /usr/bin/python and issues a warning. This exception provides temporary compatibility with previous versions of Ansible that always defaulted to /usr/bin/python, so if you have installed Python and other dependencies at /usr/bin/python on some hosts, Ansible will find and use them with this setting. If no entry is found, or the listed Python is not present on the target host, searches a list of common Python interpreter paths and uses the first one found; also issues a warning that future installation of another Python interpreter could alter the one chosen.

Detects the target OS platform, distribution, and version, then consults a table listing the correct Python interpreter and path for each platform/distribution/version. If an entry is found, uses the discovered interpreter. If no entry is found, or the listed Python is not present on the target host, searches a list of common Python interpreter paths and uses the first one found; also issues a warning that future installation of another Python interpreter could alter the one chosen.

Same as auto_legacy, but does not issue warnings.

Same as auto, but does not issue warnings.

You can still set ansible_python_interpreter to a specific path at any variable level (for example, in host_vars, in vars files, in playbooks, and so on). Setting a specific path completely disables automatic interpreter discovery; Ansible always uses the path specified.

---

## Ansible Configuration Settings — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/config.html

**Contents:**
- Ansible Configuration Settings
- The configuration file
  - Generating a sample ansible.cfg file
  - Avoiding security risks with ansible.cfg in the current directory
  - Relative paths for configuration
- Common Options
  - ACTION_WARNINGS
  - AGNOSTIC_BECOME_PROMPT
  - ALLOW_BROKEN_CONDITIONALS
  - ALLOW_EMBEDDED_TEMPLATES

Ansible supports several sources for configuring its behavior, including an ini file named ansible.cfg, environment variables, command-line options, playbook keywords, and variables. See Controlling how Ansible behaves: precedence rules for details on the relative precedence of each source.

The ansible-config utility allows users to see all the configuration settings available, their defaults, how to set them and where their current value comes from. See ansible-config for more information.

Changes can be made and used in a configuration file which will be searched for in the following order:

ANSIBLE_CONFIG (environment variable if set)

ansible.cfg (in the current directory)

~/.ansible.cfg (in the home directory)

/etc/ansible/ansible.cfg

Ansible will process the above list and use the first file found, all others are ignored.

The configuration file is one variant of an INI format. Both the hash sign (#) and semicolon (;) are allowed as comment markers when the comment starts the line. However, if the comment is inline with regular values, only the semicolon is allowed to introduce the comment. For instance:

You can generate a fully commented-out example ansible.cfg file, for example:

You can also have a more complete file that includes existing plugins:

You can use these as starting points to create your own ansible.cfg file.

If Ansible were to load ansible.cfg from a world-writable current working directory, it would create a serious security risk. Another user could place their own config file there, designed to make Ansible run malicious code both locally and remotely, possibly with elevated privileges. For this reason, Ansible will not automatically load a config file from the current working directory if the directory is world-writable.

If you depend on using Ansible with a config file in the current working directory, the best way to avoid this problem is to restrict access to your Ansible directories to particular user(s) and/or group(s). If your Ansible directories live on a filesystem which has to emulate Unix permissions, like Vagrant or Windows Subsystem for Linux (WSL), you may, at first, not know how you can fix this as chmod, chown, and chgrp might not work there. In most of those cases, the correct fix is to modify the mount options of the filesystem so the files and directories are readable and writable by the users and groups running Ansible but closed to others. For more details on the correct settings, see:

for Vagrant, the Vagrant documentation covers synced folder permissions.

for WSL, the WSL docs and this Microsoft blog post cover mount options.

If you absolutely depend on storing your Ansible config in a world-writable current working directory, you can explicitly specify the config file via the ANSIBLE_CONFIG environment variable. Please take appropriate steps to mitigate the security concerns above before doing so.

You can specify a relative path for many configuration options. In most of those cases the path used will be relative to the ansible.cfg file used for the current execution. If you need a path relative to your current working directory (CWD) you can use the {{CWD}} macro to specify it. We do not recommend this approach, as using your CWD as the root of relative paths can be a security risk. For example: cd /tmp; secureinfo=./newrootpassword ansible-playbook ~/safestuff/change_root_pwd.yml.

This is a copy of the options available from our release, your local install might have extra options due to additional plugins, you can use the command line utility mentioned above (ansible-config) to browse through those.

By default, Ansible will issue a warning when received from a task action (module or action plugin). These warnings can be silenced by adjusting this setting to False.

ANSIBLE_ACTION_WARNINGS

Display an agnostic become prompt instead of displaying a prompt containing the command line supplied become method.

[privilege_escalation]

agnostic_become_prompt

ANSIBLE_AGNOSTIC_BECOME_PROMPT

When enabled, this option allows conditionals with non-boolean results to be used. A deprecation warning will be emitted in these cases. By default, non-boolean conditionals result in an error. Such results often indicate unintentional use of templates where they are not supported, resulting in a conditional that is always true. When this option is enabled, conditional expressions which are a literal None or empty string will evaluate as true for backwards compatibility.

allow_broken_conditionals

ANSIBLE_ALLOW_BROKEN_CONDITIONALS

When enabled, this option allows embedded templates to be used for specific backward compatibility scenarios. A deprecation warning will be emitted in these cases. First, conditionals (for example, failed_when, until, assert.that) fully enclosed in template delimiters. Second, string constants in conditionals (for example, when: some_var == '{{ some_other_var }}'). Finally, positional arguments to lookups (for example, lookup('pipe', 'echo {{ some_var }}')). This feature is deprecated, since embedded templates are unnecessary in these cases. When disabled, use of embedded templates will result in an error. A future release will disable this feature by default.

allow_embedded_templates

ANSIBLE_ALLOW_EMBEDDED_TEMPLATES

Specify where to look for the ansible-connection script. This location will be checked before searching $PATH. If null, ansible will start with the same directory as the ansible script.

[persistent_connection]

ansible_connection_path

ANSIBLE_CONNECTION_PATH

This configuration is now deprecated and scheduled for removal.

This setting has no effect.

Accept a list of cowsay templates that are ‘safe’ to use, set to an empty list if you want to enable all installed templates.

['bud-frogs', 'bunny', 'cheese', 'daemon', 'default', 'dragon', 'elephant-in-snake', 'elephant', 'eyes', 'hellokitty', 'kitty', 'luke-koala', 'meow', 'milk', 'moofasa', 'moose', 'ren', 'sheep', 'small', 'stegosaurus', 'stimpy', 'supermilker', 'three-eyes', 'turkey', 'turtle', 'tux', 'udder', 'vader-koala', 'vader', 'www']

cowsay_enabled_stencils

ANSIBLE_COW_ACCEPTLIST

Specify a custom cowsay path or swap in your cowsay implementation of choice.

This allows you to choose a specific cowsay stencil for the banners or use ‘random’ to cycle through them.

ANSIBLE_COW_SELECTION

This option forces color mode even when running without a TTY or the “nocolor” setting is True.

The default root path for Ansible config files on the controller.

This setting allows suppressing colorizing output, which is used to give a better indication of failure and status information.

If you have cowsay installed but want to avoid the ‘cows’ (why????), use this.

This is a global option, each connection plugin can override either by having more specific options or not supporting pipelining at all. Pipelining, if supported by the connection plugin, reduces the number of network operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfer. It can result in a very significant performance improvement when enabled. However this conflicts with privilege escalation (become). For example, when using ‘sudo:’ operations you must first disable ‘requiretty’ in /etc/sudoers on all managed hosts, which is why it is disabled by default. This setting will be disabled if ANSIBLE_KEEP_REMOTE_FILES is enabled.

Sets the default value for the any_errors_fatal keyword, if True, Task failures will be considered fatal errors.

ANSIBLE_ANY_ERRORS_FATAL

When False``(default), Ansible will skip using become if the remote user is the same as the become user, as this is normally a redundant operation. In other words root sudo to root. If ``True, this forces Ansible to use the become plugin anyways as there are cases in which this is needed.

[privilege_escalation]

become_allow_same_user

ANSIBLE_BECOME_ALLOW_SAME_USER

The password file to use for the become plugin. --become-password-file. If executable, it will be run and the resulting stdout will be used as the password.

ANSIBLE_BECOME_PASSWORD_FILE

Colon-separated paths in which Ansible will search for Become Plugins.

{{ ANSIBLE_HOME ~ "/plugins/become:/usr/share/ansible/plugins/become" }}

ANSIBLE_BECOME_PLUGINS

Chooses which fact cache plugin to use. By default, no cache is used and facts do not persist between runs.

Defines connection or path information for the fact cache plugin.

fact_caching_connection

ANSIBLE_CACHE_PLUGIN_CONNECTION

Prefix to use for fact cache plugin files/tables.

ANSIBLE_CACHE_PLUGIN_PREFIX

Expiration timeout for the fact cache plugin data.

ANSIBLE_CACHE_PLUGIN_TIMEOUT

List of enabled callbacks, not all callbacks need enabling, but many of those shipped with Ansible do as we don’t want them activated by default.

ANSIBLE_CALLBACKS_ENABLED

When a collection is loaded that does not support the running Ansible version (with the collection metadata key requires_ansible).

issue a ‘fatal’ error and stop the play

issue a warning but continue

just continue silently

collections_on_ansible_version_mismatch

ANSIBLE_COLLECTIONS_ON_ANSIBLE_VERSION_MISMATCH

Colon-separated paths in which Ansible will search for collections content. Collections must be in nested subdirectories, not directly in these directories. For example, if COLLECTIONS_PATHS includes '{{ ANSIBLE_HOME ~ "/collections" }}', and you want to add my.collection to that directory, it must be saved as '{{ ANSIBLE_HOME} ~ "/collections/ansible_collections/my/collection" }}'.

{{ ANSIBLE_HOME ~ "/collections:/usr/share/ansible/collections" }}

ANSIBLE_COLLECTIONS_PATH

A boolean to enable or disable scanning the sys.path for installed collections.

collections_scan_sys_path

ANSIBLE_COLLECTIONS_SCAN_SYS_PATH

Defines the color to use on ‘Changed’ task status.

ANSIBLE_COLOR_CHANGED

Defines the default color to use for ansible-console.

ANSIBLE_COLOR_CONSOLE_PROMPT

Defines the color to use when emitting debug messages.

Defines the color to use when emitting deprecation messages.

ANSIBLE_COLOR_DEPRECATE

Defines the color to use when showing added lines in diffs.

ANSIBLE_COLOR_DIFF_ADD

Defines the color to use when showing diffs.

ANSIBLE_COLOR_DIFF_LINES

Defines the color to use when showing removed lines in diffs.

ANSIBLE_COLOR_DIFF_REMOVE

Defines the color to use when emitting a constant in the ansible-doc output.

ANSIBLE_COLOR_DOC_CONSTANT

Defines the color to use when emitting a deprecated value in the ansible-doc output.

ANSIBLE_COLOR_DOC_DEPRECATED

Defines the color to use when emitting a link in the ansible-doc output.

ANSIBLE_COLOR_DOC_LINK

Defines the color to use when emitting a module name in the ansible-doc output.

ANSIBLE_COLOR_DOC_MODULE

Defines the color to use when emitting a plugin name in the ansible-doc output.

ANSIBLE_COLOR_DOC_PLUGIN

Defines the color to use when emitting cross-reference in the ansible-doc output.

ANSIBLE_COLOR_DOC_REFERENCE

Defines the color to use when emitting error messages.

Defines the color to use for highlighting.

ANSIBLE_COLOR_HIGHLIGHT

Defines the color to use when showing ‘Included’ task status.

ANSIBLE_COLOR_INCLUDED

Defines the color to use when showing ‘OK’ task status.

Defines the color to use when showing ‘Skipped’ task status.

Defines the color to use on ‘Unreachable’ status.

ANSIBLE_COLOR_UNREACHABLE

Defines the color to use when emitting verbose messages. In other words, those that show with ‘-v’s.

ANSIBLE_COLOR_VERBOSE

Defines the color to use when emitting warning messages.

Which modules to run during a play’s fact gathering stage based on connection

{'asa': 'ansible.legacy.asa_facts', 'cisco.asa.asa': 'cisco.asa.asa_facts', 'eos': 'ansible.legacy.eos_facts', 'arista.eos.eos': 'arista.eos.eos_facts', 'frr': 'ansible.legacy.frr_facts', 'frr.frr.frr': 'frr.frr.frr_facts', 'ios': 'ansible.legacy.ios_facts', 'cisco.ios.ios': 'cisco.ios.ios_facts', 'iosxr': 'ansible.legacy.iosxr_facts', 'cisco.iosxr.iosxr': 'cisco.iosxr.iosxr_facts', 'junos': 'ansible.legacy.junos_facts', 'junipernetworks.junos.junos': 'junipernetworks.junos.junos_facts', 'nxos': 'ansible.legacy.nxos_facts', 'cisco.nxos.nxos': 'cisco.nxos.nxos_facts', 'vyos': 'ansible.legacy.vyos_facts', 'vyos.vyos.vyos': 'vyos.vyos.vyos_facts', 'exos': 'ansible.legacy.exos_facts', 'extreme.exos.exos': 'extreme.exos.exos_facts', 'slxos': 'ansible.legacy.slxos_facts', 'extreme.slxos.slxos': 'extreme.slxos.slxos_facts', 'voss': 'ansible.legacy.voss_facts', 'extreme.voss.voss': 'extreme.voss.voss_facts', 'ironware': 'ansible.legacy.ironware_facts', 'community.network.ironware': 'community.network.ironware_facts'}

The password file to use for the connection plugin. --connection-password-file.

connection_password_file

ANSIBLE_CONNECTION_PASSWORD_FILE

Sets the output directory on the remote host to generate coverage reports into. Currently only used for remote coverage on PowerShell modules. This is for internal use only.

_ANSIBLE_COVERAGE_REMOTE_OUTPUT

_ansible_coverage_remote_output

A list of paths for files on the Ansible controller to run coverage for when executing on the remote host. Only files that match the path glob will have their coverage collected. Multiple path globs can be specified and are separated by :. Currently only used for remote coverage on PowerShell modules. This is for internal use only.

_ANSIBLE_COVERAGE_REMOTE_PATH_FILTER

Colon-separated paths in which Ansible will search for Action Plugins.

{{ ANSIBLE_HOME ~ "/plugins/action:/usr/share/ansible/plugins/action" }}

ANSIBLE_ACTION_PLUGINS

When enabled, this option allows lookup plugins (whether used in variables as {{lookup('foo')}} or as a loop as with_foo) to return data that is not marked ‘unsafe’. By default, such data is marked as unsafe to prevent the templating engine from evaluating any jinja2 templating language, as this could represent a security risk. This option is provided to allow for backward compatibility, however, users should first consider adding allow_unsafe=True to any lookups that may be expected to contain data that may be run through the templating engine late.

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option is no longer used in the Ansible Core code base.

Lookup plugins are responsible for tagging strings containing templates to allow evaluation as a template.

This controls whether an Ansible playbook should prompt for a login password. If using SSH keys for authentication, you probably do not need to change this setting.

This controls whether an Ansible playbook should prompt for a vault password.

ANSIBLE_ASK_VAULT_PASS

Toggles the use of privilege escalation, allowing you to ‘become’ another user after login.

[privilege_escalation]

Toggle to prompt for privilege escalation password.

[privilege_escalation]

ANSIBLE_BECOME_ASK_PASS

executable to use for privilege escalation, otherwise Ansible will depend on PATH.

[privilege_escalation]

Flags to pass to the privilege escalation executable.

[privilege_escalation]

Privilege escalation method to use when become is enabled.

[privilege_escalation]

ANSIBLE_BECOME_METHOD

The user your login/remote user ‘becomes’ when using privilege escalation, most systems will use ‘root’ when no user is specified.

[privilege_escalation]

Colon-separated paths in which Ansible will search for Cache Plugins.

{{ ANSIBLE_HOME ~ "/plugins/cache:/usr/share/ansible/plugins/cache" }}

ANSIBLE_CACHE_PLUGINS

Colon-separated paths in which Ansible will search for Callback Plugins.

{{ ANSIBLE_HOME ~ "/plugins/callback:/usr/share/ansible/plugins/callback" }}

ANSIBLE_CALLBACK_PLUGINS

Colon-separated paths in which Ansible will search for Cliconf Plugins.

{{ ANSIBLE_HOME ~ "/plugins/cliconf:/usr/share/ansible/plugins/cliconf" }}

ANSIBLE_CLICONF_PLUGINS

Colon-separated paths in which Ansible will search for Connection Plugins.

{{ ANSIBLE_HOME ~ "/plugins/connection:/usr/share/ansible/plugins/connection" }}

ANSIBLE_CONNECTION_PLUGINS

Toggles debug output in Ansible. This is very verbose and can hinder multiprocessing. Debug output can also include secret information despite no_log settings being enabled, which means debug mode should not be used in production.

This indicates the command to use to spawn a shell under, which is required for Ansible’s execution needs on a target. Users may need to change this in rare instances when shell usage is constrained, but in most cases, it may be left as is.

Colon-separated paths in which Ansible will search for Jinja2 Filter Plugins.

{{ ANSIBLE_HOME ~ "/plugins/filter:/usr/share/ansible/plugins/filter" }}

ANSIBLE_FILTER_PLUGINS

This option controls if notified handlers run on a host even if a failure occurs on that host. When false, the handlers will not run if a failure has occurred on a host. This can also be set per play or on the command line. See Handlers and Failure for more details.

ANSIBLE_FORCE_HANDLERS

Maximum number of forks Ansible will use to execute tasks on target hosts.

This setting controls the default policy of fact gathering (facts discovered about remote systems). This option can be useful for those wishing to save fact gathering time. Both ‘smart’ and ‘explicit’ will use the cache plugin.

the cache plugin will be ignored and facts will be gathered per play unless ‘gather_facts: False’ is set.

facts will not be gathered unless directly requested in the play.

each new host that has no facts discovered will be scanned, but if the same host is addressed in multiple plays it will not be contacted again in the run.

This setting controls how duplicate definitions of dictionary variables (aka hash, map, associative array) are handled in Ansible. This does not affect variables whose values are scalars (integers, strings) or arrays. WARNING, changing this setting is not recommended as this is fragile and makes your content (plays, roles, collections) nonportable, leading to continual confusion and misuse. Don’t change this setting unless you think you have an absolute need for it. We recommend avoiding reusing variable names and relying on the combine filter and vars and varnames lookups to create merged versions of the individual variables. In our experience, this is rarely needed and is a sign that too much complexity has been introduced into the data structures and plays. For some uses you can also look into custom vars_plugins to merge on input, even substituting the default host_group_vars that is in charge of parsing the host_vars/ and group_vars/ directories. Most users of this setting are only interested in inventory scope, but the setting itself affects all sources and makes debugging even harder. All playbooks and roles in the official examples repos assume the default for this setting. Changing the setting to merge applies across variable sources, but many sources will internally still overwrite the variables. For example include_vars will dedupe variables internally before updating Ansible, with ‘last defined’ overwriting previous definitions in same file. The Ansible project recommends you avoid ``merge`` for new projects. It is the intention of the Ansible developers to eventually deprecate and remove this setting, but it is being kept as some users do heavily rely on it. New projects should avoid ‘merge’.

Any variable that is defined more than once is overwritten using the order from variable precedence rules (highest wins).

Any dictionary variable will be recursively merged with new definitions across the different variable definition sources.

ANSIBLE_HASH_BEHAVIOUR

Comma-separated list of Ansible inventory sources

['/etc/ansible/hosts']

Colon-separated paths in which Ansible will search for HttpApi Plugins.

{{ ANSIBLE_HOME ~ "/plugins/httpapi:/usr/share/ansible/plugins/httpapi" }}

ANSIBLE_HTTPAPI_PLUGINS

This sets the interval (in seconds) of Ansible internal processes polling each other. Lower values improve performance with large playbooks at the expense of extra CPU load. Higher values are more suitable for Ansible usage in automation scenarios when UI responsiveness is not required but CPU usage might be a concern. The default corresponds to the value hardcoded in Ansible <= 2.1

internal_poll_interval

Colon-separated paths in which Ansible will search for Inventory Plugins.

{{ ANSIBLE_HOME ~ "/plugins/inventory:/usr/share/ansible/plugins/inventory" }}

ANSIBLE_INVENTORY_PLUGINS

This is a developer-specific feature that allows enabling additional Jinja2 extensions. See the Jinja2 documentation for details. If you do not know what these do, you probably don’t need to change this setting :)

ANSIBLE_JINJA2_EXTENSIONS

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

Jinja2 extensions have been deprecated

Ansible-supported Jinja plugins (tests, filters, lookups)

This option preserves variable types during template operations.

ANSIBLE_JINJA2_NATIVE

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option is no longer used in the Ansible Core code base.

Jinja2 native mode is now the default and only option.

Enables/disables the cleaning up of the temporary files Ansible used to execute the tasks on the remote. If this option is enabled it will disable ANSIBLE_PIPELINING.

ANSIBLE_KEEP_REMOTE_FILES

This setting causes libvirt to connect to LXC containers by passing --noseclabel parameter to virsh command. This is necessary when running on systems which do not have SELinux.

libvirt_lxc_noseclabel

ANSIBLE_LIBVIRT_LXC_NOSECLABEL

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option was moved to the plugin itself

Use the option from the plugin itself.

Controls whether callback plugins are loaded when running /usr/bin/ansible. This may be used to log activity from the command line, send notifications, and so on. Callback plugins are always loaded for ansible-playbook.

bin_ansible_callbacks

ANSIBLE_LOAD_CALLBACK_PLUGINS

Temporary directory for Ansible to use on the controller.

{{ ANSIBLE_HOME ~ "/tmp" }}

List of logger names to filter out of the log file.

File to which Ansible will log on the controller. When not set the logging is disabled.

Colon-separated paths in which Ansible will search for Lookup Plugins.

{{ ANSIBLE_HOME ~ "/plugins/lookup:/usr/share/ansible/plugins/lookup" }}

ANSIBLE_LOOKUP_PLUGINS

Sets the macro for the ‘ansible_managed’ variable available for ansible_collections.ansible.builtin.template_module and ansible_collections.ansible.windows.win_template_module. This is only relevant to those two modules.

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

The ansible_managed variable can be set just like any other variable, or a different variable can be used.

Set the ansible_managed variable, or use any custom variable in templates.

This sets the default arguments to pass to the ansible adhoc binary if no -a is specified.

Compression scheme to use when transferring Python modules to the target.

ansible_module_compression

Module to use with the ansible AdHoc command, if none is specified via -m.

Colon-separated paths in which Ansible will search for Modules.

{{ ANSIBLE_HOME ~ "/plugins/modules:/usr/share/ansible/plugins/modules" }}

Colon-separated paths in which Ansible will search for Module utils files, which are shared by modules.

{{ ANSIBLE_HOME ~ "/plugins/module_utils:/usr/share/ansible/plugins/module_utils" }}

Colon-separated paths in which Ansible will search for Netconf Plugins.

{{ ANSIBLE_HOME ~ "/plugins/netconf:/usr/share/ansible/plugins/netconf" }}

ANSIBLE_NETCONF_PLUGINS

Toggle Ansible’s display and logging of task details, mainly used to avoid security disclosures.

Toggle Ansible logging to syslog on the target when it executes tasks. On Windows hosts, this will disable a newer style PowerShell modules from writing to the event log.

ANSIBLE_NO_TARGET_SYSLOG

ansible_no_target_syslog

What templating should return as a ‘null’ value. When not set it will let Jinja2 decide.

ANSIBLE_NULL_REPRESENTATION

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option is no longer used in the Ansible Core code base.

There is no alternative at the moment. A different mechanism would have to be implemented in the current code base.

For asynchronous tasks in Ansible (covered in Asynchronous Actions and Polling), this is how often to check back on the status of those tasks when an explicit poll interval is not supplied. The default is a reasonably moderate 15 seconds which is a tradeoff between checking in frequently and providing a quick turnaround when something may have completed.

ANSIBLE_POLL_INTERVAL

Option for connections using a certificate or key file to authenticate, rather than an agent or passwords, you can set the default value here to avoid re-specifying --private-key with every invocation.

ANSIBLE_PRIVATE_KEY_FILE

By default, imported roles publish their variables to the play and other roles, this setting can avoid that. This was introduced as a way to reset role variables to default values if a role is used more than once in a playbook. Starting in version ‘2.17’ M(ansible.builtin.include_roles) and M(ansible.builtin.import_roles) can individually override this via the C(public) parameter. Included roles only make their variables public at execution, unlike imported roles which happen at playbook compile time.

ANSIBLE_PRIVATE_ROLE_VARS

Port to use in remote connections, when blank it will use the connection plugin default.

Sets the login user for the target machines When blank it uses the connection plugin’s default, normally the user currently executing Ansible.

Colon-separated paths in which Ansible will search for Roles.

{{ ANSIBLE_HOME ~ "/roles:/usr/share/ansible/roles:/etc/ansible/roles" }}

Some filesystems do not support safe operations and/or return inconsistent errors, this setting makes Ansible ‘tolerate’ those in the list without causing fatal errors. Data corruption may occur and writes are not always verified when a filesystem is in the list.

['fuse', 'nfs', 'vboxsf', 'ramfs', '9p', 'vfat']

special_context_filesystems

ANSIBLE_SELINUX_SPECIAL_FS

Set the main callback used to display Ansible output. You can only have one at a time. You can have many other callbacks, but just one can be in charge of stdout. See Callback plugins for a list of available options.

ANSIBLE_STDOUT_CALLBACK

Set the default strategy used for plays.

Colon-separated paths in which Ansible will search for Strategy Plugins.

{{ ANSIBLE_HOME ~ "/plugins/strategy:/usr/share/ansible/plugins/strategy" }}

ANSIBLE_STRATEGY_PLUGINS

Toggle the use of “su” for tasks.

Syslog facility to use when Ansible logs to the remote target.

ANSIBLE_SYSLOG_FACILITY

Colon-separated paths in which Ansible will search for Terminal Plugins.

{{ ANSIBLE_HOME ~ "/plugins/terminal:/usr/share/ansible/plugins/terminal" }}

ANSIBLE_TERMINAL_PLUGINS

Colon-separated paths in which Ansible will search for Jinja2 Test Plugins.

{{ ANSIBLE_HOME ~ "/plugins/test:/usr/share/ansible/plugins/test" }}

This is the default timeout for connection plugins to use.

Can be any connection plugin available to your ansible installation. There is also a (DEPRECATED) special ‘smart’ option, that will toggle between ‘ssh’ and ‘paramiko’ depending on controller OS and ssh versions.

When True, this causes ansible templating to fail steps that reference variable names that are likely typoed. Otherwise, any ‘{{ template_expression }}’ that contains undefined variables will be rendered in a template or ansible action line exactly as written.

error_on_undefined_vars

ANSIBLE_ERROR_ON_UNDEFINED_VARS

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option is no longer used in the Ansible Core code base.

There is no alternative at the moment. A different mechanism would have to be implemented in the current code base.

Colon-separated paths in which Ansible will search for Vars Plugins.

{{ ANSIBLE_HOME ~ "/plugins/vars:/usr/share/ansible/plugins/vars" }}

The vault_id to use for encrypting by default. If multiple vault_ids are provided, this specifies which to use for encryption. The --encrypt-vault-id CLI option overrides the configured value.

vault_encrypt_identity

ANSIBLE_VAULT_ENCRYPT_IDENTITY

If true, decrypting vaults with a vault id will only try the password from the matching vault-id.

ANSIBLE_VAULT_ID_MATCH

The label to use for the default vault id label in cases where a vault id label is not provided.

ANSIBLE_VAULT_IDENTITY

A list of vault-ids to use by default. Equivalent to multiple --vault-id args. Vault-ids are tried in order.

ANSIBLE_VAULT_IDENTITY_LIST

The vault password file to use. Equivalent to --vault-password-file or --vault-id. If executable, it will be run and the resulting stdout will be used as the password.

ANSIBLE_VAULT_PASSWORD_FILE

Sets the default verbosity, equivalent to the number of -v passed in the command line.

Toggle to control the showing of deprecation warnings

ANSIBLE_DEPRECATION_WARNINGS

ansible_deprecation_warnings

Toggle to control showing warnings related to running devel.

ANSIBLE_DEVEL_WARNING

Configuration toggle to tell modules to show differences when in ‘changed’ status, equivalent to --diff.

Number of lines of context to show when displaying the differences between files.

Normally ansible-playbook will print a header for each task that is run. These headers will contain the name: field from the task if you specified one. If you didn’t then ansible-playbook uses the task’s action to help you tell which task is presently running. Sometimes you run many of the same action and so you want more information about the task to differentiate it from others of the same action. If you set this variable to True in the config then ansible-playbook will also include the task’s arguments in the header. This setting defaults to False because there is a chance that you have sensitive values in your parameters and you do not want those to be printed. If you set this to True you should be sure that you have secured your environment’s stdout (no one can shoulder surf your screen and you aren’t saving stdout to an insecure file) or made sure that all of your playbooks explicitly added the no_log: True parameter to tasks that have sensitive values How do I keep secret data in my playbook? for more information.

display_args_to_stdout

ANSIBLE_DISPLAY_ARGS_TO_STDOUT

Toggle to control displaying skipped task/host entries in a task in the default callback.

display_skipped_hosts

ANSIBLE_DISPLAY_SKIPPED_HOSTS

When to include tracebacks in extended error messages

ANSIBLE_DISPLAY_TRACEBACK

Colon-separated paths in which Ansible will search for Documentation Fragments Plugins.

{{ ANSIBLE_HOME ~ "/plugins/doc_fragments:/usr/share/ansible/plugins/doc_fragments" }}

ANSIBLE_DOC_FRAGMENT_PLUGINS

Root docsite URL used to generate docs URLs in warning/error text; must be an absolute URL with a valid scheme and trailing slash.

https://docs.ansible.com/ansible-core/

By default, Ansible will issue a warning when a duplicate dict key is encountered in YAML. These warnings can be silenced by adjusting this setting to False.

issue a ‘fatal’ error and stop the play

issue a warning but continue

just continue silently

ANSIBLE_DUPLICATE_YAML_DICT_KEY

for the cases in which Ansible needs to return a file within an editor, this chooses the application to use.

Whether or not to enable the task debugger, this previously was done as a strategy plugin. Now all strategy plugins can inherit this behavior. The debugger defaults to activating when a task is failed on unreachable. Use the debugger keyword for more flexibility.

ANSIBLE_ENABLE_TASK_DEBUGGER

Toggle to allow missing handlers to become a warning instead of an error when notifying.

error_on_missing_handler

ANSIBLE_ERROR_ON_MISSING_HANDLER

Which modules to run during a play’s fact gathering stage, using the default of ‘smart’ will try to figure it out based on connection type. If adding your own modules but you still want to use the default Ansible facts, you will want to include ‘setup’ or corresponding network module to the list (if you add ‘smart’, Ansible will also figure it out). This does not affect explicit calls to the ‘setup’ module, but does always affect the ‘gather_facts’ action (implicit or explicit).

ANSIBLE_FACTS_MODULES

ansible_facts_modules

The directory that stores cached responses from a Galaxy server. This is only used by the ansible-galaxy collection install and download commands. Cache files inside this dir will be ignored if they are world writable.

{{ ANSIBLE_HOME ~ "/galaxy_cache" }}

ANSIBLE_GALAXY_CACHE_DIR

The multiplier used to increase the GALAXY_COLLECTION_IMPORT_POLL_INTERVAL when checking the collection import status.

ANSIBLE_GALAXY_COLLECTION_IMPORT_POLL_FACTOR

The initial interval in seconds for polling the import status of a collection. This interval increases exponentially based on the GALAXY_COLLECTION_IMPORT_POLL_FACTOR, with a maximum delay of 30 seconds.

ANSIBLE_GALAXY_COLLECTION_IMPORT_POLL_INTERVAL

Collection skeleton directory to use as a template for the init action in ansible-galaxy collection, same as --collection-skeleton.

ANSIBLE_GALAXY_COLLECTION_SKELETON

patterns of files to ignore inside a Galaxy collection skeleton directory.

['^.git$', '^.*/.git_keep$']

collection_skeleton_ignore

ANSIBLE_GALAXY_COLLECTION_SKELETON_IGNORE

whether ansible-galaxy collection install should warn about --collections-path missing from configured COLLECTIONS_PATHS.

collections_path_warning

ANSIBLE_GALAXY_COLLECTIONS_PATH_WARNING

Disable GPG signature verification during collection installation.

ANSIBLE_GALAXY_DISABLE_GPG_VERIFY

Some steps in ansible-galaxy display a progress wheel which can cause issues on certain displays or when outputting the stdout to a file. This config option controls whether the display wheel is shown or not. The default is to show the display wheel if stdout has a tty.

ANSIBLE_GALAXY_DISPLAY_PROGRESS

Configure the keyring used for GPG signature verification during collection installation and verification.

ANSIBLE_GALAXY_GPG_KEYRING

If set to yes, ansible-galaxy will not validate TLS certificates. This can be useful for testing against a server with a self-signed certificate.

ANSIBLE_GALAXY_IGNORE

A list of GPG status codes to ignore during GPG signature verification. See L(https://github.com/gpg/gnupg/blob/master/doc/DETAILS#general-status-codes) for status code descriptions. If fewer signatures successfully verify the collection than GALAXY_REQUIRED_VALID_SIGNATURE_COUNT, signature verification will fail even if all error codes are ignored.

ignore_signature_status_codes

ANSIBLE_GALAXY_IGNORE_SIGNATURE_STATUS_CODES

The number of signatures that must be successful during GPG signature verification while installing or verifying collections. This should be a positive integer or all to indicate all signatures must successfully validate the collection. Prepend + to the value to fail if no valid signatures are found for the collection.

required_valid_signature_count

ANSIBLE_GALAXY_REQUIRED_VALID_SIGNATURE_COUNT

Role skeleton directory to use as a template for the init action in ansible-galaxy/ansible-galaxy role, same as --role-skeleton.

ANSIBLE_GALAXY_ROLE_SKELETON

patterns of files to ignore inside a Galaxy role or collection skeleton directory.

['^.git$', '^.*/.git_keep$']

ANSIBLE_GALAXY_ROLE_SKELETON_IGNORE

URL to prepend when roles don’t specify the full URI, assume they are referencing this server as the source.

https://galaxy.ansible.com

ANSIBLE_GALAXY_SERVER

A list of Galaxy servers to use when installing a collection. The value corresponds to the config ini header [galaxy_server.{{item}}] which defines the server details. See Configuring the ansible-galaxy client for more details on how to define a Galaxy server. The order of servers in this list is used as the order in which a collection is resolved. Setting this config option will ignore the GALAXY_SERVER config option.

ANSIBLE_GALAXY_SERVER_LIST

The default timeout for Galaxy API calls. Galaxy servers that don’t configure a specific timeout will fall back to this value.

ANSIBLE_GALAXY_SERVER_TIMEOUT

Local path to galaxy access token file

{{ ANSIBLE_HOME ~ "/galaxy_token" }}

ANSIBLE_GALAXY_TOKEN_PATH

Set this to “False” if you want to avoid host key checking by the underlying connection plugin Ansible uses to connect to the host. Please read the documentation of the specific connection plugin used for details.

ANSIBLE_HOST_KEY_CHECKING

This setting changes the behaviour of mismatched host patterns, it allows you to force a fatal error, a warning or just ignore it.

issue a ‘fatal’ error and stop the play

issue a warning but continue

just continue silently

host_pattern_mismatch

ANSIBLE_HOST_PATTERN_MISMATCH

Facts are available inside the ansible_facts variable, this setting also pushes them as their own vars in the main namespace. Unlike inside the ansible_facts dictionary where the prefix ansible_ is removed from fact names, these will have the exact names that are returned by the module.

ANSIBLE_INJECT_FACT_VARS

Path to the Python interpreter to be used for module execution on remote targets, or an automatic discovery mode. Supported discovery modes are auto (the default), auto_silent, auto_legacy, and auto_legacy_silent. All discovery modes match against an ordered list of well-known Python interpreter locations. The fallback behavior will issue a warning that the interpreter should be set explicitly (since interpreters installed later may change which one is used). This warning behavior can be disabled by setting auto_silent. The auto_legacy modes are deprecated and behave the same as their respective auto modes. They exist for backward-compatibility with older Ansible releases that always defaulted to /usr/bin/python3, which will use that interpreter if present.

ANSIBLE_PYTHON_INTERPRETER

ansible_python_interpreter

['python3.13', 'python3.12', 'python3.11', 'python3.10', 'python3.9', 'python3.8', '/usr/bin/python3', 'python3']

ansible_interpreter_python_fallback

If ‘false’, invalid attributes for a task will result in warnings instead of errors.

invalid_task_attribute_failed

ANSIBLE_INVALID_TASK_ATTRIBUTE_FAILED

If ‘true’, it is a fatal error when any given inventory source cannot be successfully parsed by any available inventory plugin; otherwise, this situation only attracts a warning.

any_unparsed_is_failed

ANSIBLE_INVENTORY_ANY_UNPARSED_IS_FAILED

List of enabled inventory plugins, it also determines the order in which they are used.

['host_list', 'script', 'auto', 'yaml', 'ini', 'toml']

ANSIBLE_INVENTORY_ENABLED

Controls if ansible-inventory will accurately reflect Ansible’s view into inventory or its optimized for exporting.

ANSIBLE_INVENTORY_EXPORT

List of extensions to ignore when using a directory as an inventory source.

{{ REJECT_EXTS + ['.orig', '.cfg', '.retry'] }}

inventory_ignore_extensions

ANSIBLE_INVENTORY_IGNORE

List of patterns to ignore when using a directory as an inventory source.

inventory_ignore_patterns

ANSIBLE_INVENTORY_IGNORE_REGEX

If ‘true’ it is a fatal error if every single potential inventory source fails to parse, otherwise, this situation will only attract a warning.

ANSIBLE_INVENTORY_UNPARSED_FAILED

By default, Ansible will issue a warning when no inventory was loaded and notes that it will use an implicit localhost-only inventory. These warnings can be silenced by adjusting this setting to False.

inventory_unparsed_warning

ANSIBLE_INVENTORY_UNPARSED_WARNING

By default, Ansible will issue a warning when there are no hosts in the inventory. These warnings can be silenced by adjusting this setting to False.

ANSIBLE_LOCALHOST_WARNING

This will set log verbosity if higher than the normal display verbosity, otherwise it will match that.

ANSIBLE_LOG_VERBOSITY

Maximum size of files to be considered for diff display.

ANSIBLE_MAX_DIFF_SIZE

List of extensions to ignore when looking for modules to load. This is for rejecting script and binary module fallback extensions.

{{ REJECT_EXTS + ['.yaml', '.yml', '.ini'] }}

ANSIBLE_MODULE_IGNORE_EXTS

Enables whether module responses are evaluated for containing non-UTF-8 data. Disabling this may result in unexpected behavior. Only ansible-core should evaluate this configuration.

module_strict_utf8_response

ANSIBLE_MODULE_STRICT_UTF8_RESPONSE

This variable is used to enable bastion/jump host with netconf connection. If set to True the bastion/jump host ssh settings should be present in ~/.ssh/config file, alternatively it can be set to custom ssh configuration file path to read the bastion/jump host settings.

ANSIBLE_NETCONF_SSH_CONFIG

['eos', 'nxos', 'ios', 'iosxr', 'junos', 'enos', 'ce', 'vyos', 'sros', 'dellos9', 'dellos10', 'dellos6', 'asa', 'aruba', 'aireos', 'bigip', 'ironware', 'onyx', 'netconf', 'exos', 'voss', 'slxos']

network_group_modules

ANSIBLE_NETWORK_GROUP_MODULES

Previously Ansible would only clear some of the plugin loading caches when loading new roles, this led to some behaviors in which a plugin loaded in previous plays would be unexpectedly ‘sticky’. This setting allows the user to return to that behavior.

old_plugin_cache_clear

ANSIBLE_OLD_PLUGIN_CACHE_CLEAR

for the cases in which Ansible needs to return output in a pageable fashion, this chooses the application to use.

[paramiko_connection]

ANSIBLE_PARAMIKO_HOST_KEY_AUTO_ADD

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option was moved to the plugin itself

Use the option from the plugin itself.

[paramiko_connection]

ANSIBLE_PARAMIKO_LOOK_FOR_KEYS

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option was moved to the plugin itself

Use the option from the plugin itself.

This controls the amount of time to wait for a response from a remote device before timing out a persistent connection.

[persistent_connection]

ANSIBLE_PERSISTENT_COMMAND_TIMEOUT

This controls the retry timeout for persistent connection to connect to the local domain socket.

[persistent_connection]

connect_retry_timeout

ANSIBLE_PERSISTENT_CONNECT_RETRY_TIMEOUT

This controls how long the persistent connection will remain idle before it is destroyed.

[persistent_connection]

ANSIBLE_PERSISTENT_CONNECT_TIMEOUT

Path to the socket to be used by the connection persistence system.

{{ ANSIBLE_HOME ~ "/pc" }}

[persistent_connection]

ANSIBLE_PERSISTENT_CONTROL_PATH_DIR

A number of non-playbook CLIs have a --playbook-dir argument; this sets the default value for it.

This sets which playbook dirs will be used as a root to process vars plugins, which includes finding host_vars/group_vars.

follows the traditional behavior of using the top playbook in the chain to find the root directory.

follows the 2.4.0 behavior of using the current playbook to find the root directory.

examines from the first parent to the current playbook.

ANSIBLE_PLAYBOOK_VARS_ROOT

A path to configuration for filtering which plugins installed on the system are allowed to be used. See Rejecting modules for details of the filter file’s format. The default is /etc/ansible/plugin_filters.yml

Attempts to set RLIMIT_NOFILE soft limit to the specified value when executing Python modules (can speed up subprocess usage on Python 2.x. See https://bugs.python.org/issue11284). The value will be limited by the existing hard limit. Default value of 0 does not attempt to adjust existing system-defined limits.

python_module_rlimit_nofile

ANSIBLE_PYTHON_MODULE_RLIMIT_NOFILE

ansible_python_module_rlimit_nofile

This controls whether a failed Ansible playbook should create a .retry file.

ANSIBLE_RETRY_FILES_ENABLED

This sets the path in which Ansible will save .retry files when a playbook fails and retry files are enabled. This file will be overwritten after each run with the list of failed hosts from all plays.

retry_files_save_path

ANSIBLE_RETRY_FILES_SAVE_PATH

This setting can be used to optimize vars_plugin usage depending on the user’s inventory size and play selection.

will run vars_plugins relative to inventory sources anytime vars are ‘demanded’ by tasks.

will run vars_plugins relative to inventory sources after importing that inventory source.

ANSIBLE_RUN_VARS_PLUGINS

This adds the custom stats set via the set_stats plugin to the default output.

ANSIBLE_SHOW_CUSTOM_STATS

Manage an SSH Agent via Ansible. A configuration of none will not interact with an agent, auto will start and destroy an agent via ssh-agent binary during the run, and a path to an SSH_AUTH_SOCK will allow interaction with a pre-existing agent.

When SSH_AGENT is auto, the path or name of the ssh agent executable to start.

ANSIBLE_SSH_AGENT_EXECUTABLE

For keys inserted into an agent defined by SSH_AGENT, define a lifetime, in seconds, that the key may remain in the agent.

ssh_agent_key_lifetime

ANSIBLE_SSH_AGENT_KEY_LIFETIME

This list of filters avoids ‘type conversion’ when templating variables. Useful when you want to avoid conversion into lists or dictionaries for JSON strings, for example.

['string', 'to_json', 'to_nice_json', 'to_yaml', 'to_nice_yaml', 'ppretty', 'json']

ANSIBLE_STRING_TYPE_FILTERS

This configuration is now deprecated and scheduled for removal. You should update to a current alternative.

This option has no effect.

None; native types returned from filters are always preserved.

Allows disabling of warnings related to potential issues on the system running Ansible itself (not on the managed hosts). These may include warnings about third-party packages or other conditions that should be resolved if possible.

ANSIBLE_SYSTEM_WARNINGS

default list of tags to run in your plays, Skip Tags has precedence.

default list of tags to skip in your plays, has precedence over Run Tags

A string to insert into target logging for tracking purposes

ANSIBLE_TARGET_LOG_INFO

ansible_target_log_info

This option defines whether the task debugger will be invoked on a failed task when ignore_errors=True is specified. True specifies that the debugger will honor ignore_errors, and False will not honor ignore_errors.

task_debugger_ignore_errors

ANSIBLE_TASK_DEBUGGER_IGNORE_ERRORS

Set the maximum time (in seconds) for a task action to execute in. Timeout runs independently from templating or looping. It applies per each attempt of executing the task’s action and remains unchanged by the total time spent on a task. When the action execution exceeds the timeout, Ansible interrupts the process. This is registered as a failure due to outside circumstances, not a task failure, to receive appropriate response and recovery process. If set to 0 (the default) there is no timeout.

Make ansible transform invalid characters in group names supplied by inventory sources.

it will replace any invalid characters with ‘_’ (underscore) and warn the user

it will allow for the group name but warn about the issue

it does the same as ‘never’, without issuing a warning

it does the same as ‘always’, without issuing a warning

force_valid_group_names

ANSIBLE_TRANSFORM_INVALID_GROUP_CHARS

Toggles the use of persistence for connections.

use_persistent_connections

ANSIBLE_USE_PERSISTENT_CONNECTIONS

A toggle to disable validating a collection’s ‘metadata’ entry for a module_defaults action group. Metadata containing unexpected fields or value types will produce a warning when this is True.

validate_action_group_metadata

ANSIBLE_VALIDATE_ACTION_GROUP_METADATA

Accept list for variable plugins that require it.

Allows to change the group variable precedence merge order.

['all_inventory', 'groups_inventory', 'all_plugins_inventory', 'all_plugins_play', 'groups_plugins_inventory', 'groups_plugins_play']

The salt to use for the vault encryption. If it is not provided, a random salt will be used.

ANSIBLE_VAULT_ENCRYPT_SALT

Force ‘verbose’ option to use stderr instead of stdout

ANSIBLE_VERBOSE_TO_STDERR

For asynchronous tasks in Ansible (covered in Asynchronous Actions and Polling), this is how long, in seconds, to wait for the task spawned by Ansible to connect back to the named pipe used on Windows systems. The default is 5 seconds. This can be too low on slower systems, or systems under heavy load. This is not the total time an async command can run for, but is a separate timeout to wait for an async command to start. The task will only start to be timed against its async_timeout once it has connected to the pipe, so the overall maximum duration the task can take will be extended by the amount specified here.

win_async_startup_timeout

ANSIBLE_WIN_ASYNC_STARTUP_TIMEOUT

ansible_win_async_startup_timeout

The maximum number of times to check Task Queue Manager worker processes to verify they have exited cleanly. After this limit is reached any worker processes still running will be terminated. This is for internal use only.

ANSIBLE_WORKER_SHUTDOWN_POLL_COUNT

The number of seconds to sleep between polling loops when checking Task Queue Manager worker processes to verify they have exited cleanly. This is for internal use only.

ANSIBLE_WORKER_SHUTDOWN_POLL_DELAY

Check all of these extensions when looking for ‘variable’ files which should be YAML or JSON or vaulted versions of these. This affects vars_files, include_vars, inventory and vars plugins among others.

['.yml', '.yaml', '.json']

yaml_valid_extensions

ANSIBLE_YAML_FILENAME_EXT

Other environment variables to configure plugins in collections can be found in Index of all Collection Environment Variables.

Override the default ansible config file

When enabled, this option allows conditionals with non-boolean results to be used.A deprecation warning will be emitted in these cases.By default, non-boolean conditionals result in an error.Such results often indicate unintentional use of templates where they are not supported, resulting in a conditional that is always true.When this option is enabled, conditional expressions which are a literal None or empty string will evaluate as true for backwards compatibility.

See also ALLOW_BROKEN_CONDITIONALS

When enabled, this option allows embedded templates to be used for specific backward compatibility scenarios.A deprecation warning will be emitted in these cases.First, conditionals (for example, failed_when, until, assert.that) fully enclosed in template delimiters.Second, string constants in conditionals (for example, when: some_var == '{{ some_other_var }}').Finally, positional arguments to lookups (for example, lookup('pipe', 'echo {{ some_var }}')).This feature is deprecated, since embedded templates are unnecessary in these cases.When disabled, use of embedded templates will result in an error.A future release will disable this feature by default.

See also ALLOW_EMBEDDED_TEMPLATES

The default root path for Ansible config files on the controller.

See also ANSIBLE_HOME

Specify where to look for the ansible-connection script. This location will be checked before searching $PATH.If null, ansible will start with the same directory as the ansible script.

See also ANSIBLE_CONNECTION_PATH

This allows you to choose a specific cowsay stencil for the banners or use ‘random’ to cycle through them.

See also ANSIBLE_COW_SELECTION

Accept a list of cowsay templates that are ‘safe’ to use, set to an empty list if you want to enable all installed templates.

See also ANSIBLE_COW_ACCEPTLIST

This option forces color mode even when running without a TTY or the “nocolor” setting is True.

See also ANSIBLE_FORCE_COLOR

This setting allows suppressing colorizing output, which is used to give a better indication of failure and status information.

See also ANSIBLE_NOCOLOR

This setting allows suppressing colorizing output, which is used to give a better indication of failure and status information.

See also ANSIBLE_NOCOLOR

If you have cowsay installed but want to avoid the ‘cows’ (why????), use this.

See also ANSIBLE_NOCOWS

Specify a custom cowsay path or swap in your cowsay implementation of choice.

See also ANSIBLE_COW_PATH

This is a global option, each connection plugin can override either by having more specific options or not supporting pipelining at all.Pipelining, if supported by the connection plugin, reduces the number of network operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfer.It can result in a very significant performance improvement when enabled.However this conflicts with privilege escalation (become). For example, when using ‘sudo:’ operations you must first disable ‘requiretty’ in /etc/sudoers on all managed hosts, which is why it is disabled by default.This setting will be disabled if ANSIBLE_KEEP_REMOTE_FILES is enabled.

See also ANSIBLE_PIPELINING

Sets the default value for the any_errors_fatal keyword, if True, Task failures will be considered fatal errors.

See also ANY_ERRORS_FATAL

When False``(default), Ansible will skip using become if the remote user is the same as the become user, as this is normally a redundant operation. In other words root sudo to root.If ``True, this forces Ansible to use the become plugin anyways as there are cases in which this is needed.

See also BECOME_ALLOW_SAME_USER

The password file to use for the become plugin. --become-password-file.If executable, it will be run and the resulting stdout will be used as the password.

See also BECOME_PASSWORD_FILE

Display an agnostic become prompt instead of displaying a prompt containing the command line supplied become method.

See also AGNOSTIC_BECOME_PROMPT

Chooses which fact cache plugin to use. By default, no cache is used and facts do not persist between runs.

See also CACHE_PLUGIN

Defines connection or path information for the fact cache plugin.

See also CACHE_PLUGIN_CONNECTION

Prefix to use for fact cache plugin files/tables.

See also CACHE_PLUGIN_PREFIX

Expiration timeout for the fact cache plugin data.

See also CACHE_PLUGIN_TIMEOUT

A boolean to enable or disable scanning the sys.path for installed collections.

See also COLLECTIONS_SCAN_SYS_PATH

Colon-separated paths in which Ansible will search for collections content. Collections must be in nested subdirectories, not directly in these directories. For example, if COLLECTIONS_PATHS includes '{{ ANSIBLE_HOME ~ "/collections" }}', and you want to add my.collection to that directory, it must be saved as '{{ ANSIBLE_HOME} ~ "/collections/ansible_collections/my/collection" }}'.

See also COLLECTIONS_PATHS

When a collection is loaded that does not support the running Ansible version (with the collection metadata key requires_ansible).

See also COLLECTIONS_ON_ANSIBLE_VERSION_MISMATCH

Defines the color to use on ‘Changed’ task status.

See also COLOR_CHANGED

Defines the default color to use for ansible-console.

See also COLOR_CONSOLE_PROMPT

Defines the color to use when emitting debug messages.

Defines the color to use when emitting deprecation messages.

See also COLOR_DEPRECATE

Defines the color to use when showing added lines in diffs.

See also COLOR_DIFF_ADD

Defines the color to use when showing diffs.

See also COLOR_DIFF_LINES

Defines the color to use when showing removed lines in diffs.

See also COLOR_DIFF_REMOVE

Defines the color to use when emitting error messages.

Defines the color to use for highlighting.

See also COLOR_HIGHLIGHT

Defines the color to use when showing ‘Included’ task status.

See also COLOR_INCLUDED

Defines the color to use when showing ‘OK’ task status.

Defines the color to use when showing ‘Skipped’ task status.

Defines the color to use on ‘Unreachable’ status.

See also COLOR_UNREACHABLE

Defines the color to use when emitting verbose messages. In other words, those that show with ‘-v’s.

See also COLOR_VERBOSE

Defines the color to use when emitting warning messages.

Defines the color to use when emitting a module name in the ansible-doc output.

See also COLOR_DOC_MODULE

Defines the color to use when emitting cross-reference in the ansible-doc output.

See also COLOR_DOC_REFERENCE

Defines the color to use when emitting a link in the ansible-doc output.

See also COLOR_DOC_LINK

Defines the color to use when emitting a deprecated value in the ansible-doc output.

See also COLOR_DOC_DEPRECATED

Defines the color to use when emitting a constant in the ansible-doc output.

See also COLOR_DOC_CONSTANT

Defines the color to use when emitting a plugin name in the ansible-doc output.

See also COLOR_DOC_PLUGIN

The password file to use for the connection plugin. --connection-password-file.

See also CONNECTION_PASSWORD_FILE

Sets the output directory on the remote host to generate coverage reports into.Currently only used for remote coverage on PowerShell modules.This is for internal use only.

See also COVERAGE_REMOTE_OUTPUT

A list of paths for files on the Ansible controller to run coverage for when executing on the remote host.Only files that match the path glob will have their coverage collected.Multiple path globs can be specified and are separated by :.Currently only used for remote coverage on PowerShell modules.This is for internal use only.

See also COVERAGE_REMOTE_PATHS

By default, Ansible will issue a warning when received from a task action (module or action plugin).These warnings can be silenced by adjusting this setting to False.

See also ACTION_WARNINGS

By default, Ansible will issue a warning when there are no hosts in the inventory.These warnings can be silenced by adjusting this setting to False.

See also LOCALHOST_WARNING

This will set log verbosity if higher than the normal display verbosity, otherwise it will match that.

See also LOG_VERBOSITY

By default, Ansible will issue a warning when no inventory was loaded and notes that it will use an implicit localhost-only inventory.These warnings can be silenced by adjusting this setting to False.

See also INVENTORY_UNPARSED_WARNING

Colon-separated paths in which Ansible will search for Documentation Fragments Plugins.

See also DOC_FRAGMENT_PLUGIN_PATH

Colon-separated paths in which Ansible will search for Action Plugins.

See also DEFAULT_ACTION_PLUGIN_PATH

This controls whether an Ansible playbook should prompt for a login password. If using SSH keys for authentication, you probably do not need to change this setting.

See also DEFAULT_ASK_PASS

This controls whether an Ansible playbook should prompt for a vault password.

See also DEFAULT_ASK_VAULT_PASS

Toggles the use of privilege escalation, allowing you to ‘become’ another user after login.

See also DEFAULT_BECOME

Toggle to prompt for privilege escalation password.

See also DEFAULT_BECOME_ASK_PASS

Privilege escalation method to use when become is enabled.

See also DEFAULT_BECOME_METHOD

executable to use for privilege escalation, otherwise Ansible will depend on PATH.

See also DEFAULT_BECOME_EXE

Flags to pass to the privilege escalation executable.

See also DEFAULT_BECOME_FLAGS

Colon-separated paths in which Ansible will search for Become Plugins.

See also BECOME_PLUGIN_PATH

The user your login/remote user ‘becomes’ when using privilege escalation, most systems will use ‘root’ when no user is specified.

See also DEFAULT_BECOME_USER

Colon-separated paths in which Ansible will search for Cache Plugins.

See also DEFAULT_CACHE_PLUGIN_PATH

Colon-separated paths in which Ansible will search for Callback Plugins.

See also DEFAULT_CALLBACK_PLUGIN_PATH

List of enabled callbacks, not all callbacks need enabling, but many of those shipped with Ansible do as we don’t want them activated by default.

See also CALLBACKS_ENABLED

Colon-separated paths in which Ansible will search for Cliconf Plugins.

See also DEFAULT_CLICONF_PLUGIN_PATH

Colon-separated paths in which Ansible will search for Connection Plugins.

See also DEFAULT_CONNECTION_PLUGIN_PATH

Toggles debug output in Ansible. This is very verbose and can hinder multiprocessing. Debug output can also include secret information despite no_log settings being enabled, which means debug mode should not be used in production.

See also DEFAULT_DEBUG

This indicates the command to use to spawn a shell under, which is required for Ansible’s execution needs on a target. Users may need to change this in rare instances when shell usage is constrained, but in most cases, it may be left as is.

See also DEFAULT_EXECUTABLE

Colon-separated paths in which Ansible will search for Jinja2 Filter Plugins.

See also DEFAULT_FILTER_PLUGIN_PATH

This option controls if notified handlers run on a host even if a failure occurs on that host.When false, the handlers will not run if a failure has occurred on a host.This can also be set per play or on the command line. See Handlers and Failure for more details.

See also DEFAULT_FORCE_HANDLERS

Maximum number of forks Ansible will use to execute tasks on target hosts.

See also DEFAULT_FORKS

This setting controls the default policy of fact gathering (facts discovered about remote systems).This option can be useful for those wishing to save fact gathering time. Both ‘smart’ and ‘explicit’ will use the cache plugin.

See also DEFAULT_GATHERING

This setting controls how duplicate definitions of dictionary variables (aka hash, map, associative array) are handled in Ansible.This does not affect variables whose values are scalars (integers, strings) or arrays.**WARNING**, changing this setting is not recommended as this is fragile and makes your content (plays, roles, collections) nonportable, leading to continual confusion and misuse. Don’t change this setting unless you think you have an absolute need for it.We recommend avoiding reusing variable names and relying on the combine filter and vars and varnames lookups to create merged versions of the individual variables. In our experience, this is rarely needed and is a sign that too much complexity has been introduced into the data structures and plays.For some uses you can also look into custom vars_plugins to merge on input, even substituting the default host_group_vars that is in charge of parsing the host_vars/ and group_vars/ directories. Most users of this setting are only interested in inventory scope, but the setting itself affects all sources and makes debugging even harder.All playbooks and roles in the official examples repos assume the default for this setting.Changing the setting to merge applies across variable sources, but many sources will internally still overwrite the variables. For example include_vars will dedupe variables internally before updating Ansible, with ‘last defined’ overwriting previous definitions in same file.The Ansible project recommends you avoid ``merge`` for new projects.**It is the intention of the Ansible developers to eventually deprecate and remove this setting, but it is being kept as some users do heavily rely on it. New projects should **avoid ‘merge’.

See also DEFAULT_HASH_BEHAVIOUR

Comma-separated list of Ansible inventory sources

See also DEFAULT_HOST_LIST

Colon-separated paths in which Ansible will search for HttpApi Plugins.

See also DEFAULT_HTTPAPI_PLUGIN_PATH

Colon-separated paths in which Ansible will search for Inventory Plugins.

See also DEFAULT_INVENTORY_PLUGIN_PATH

This is a developer-specific feature that allows enabling additional Jinja2 extensions.See the Jinja2 documentation for details. If you do not know what these do, you probably don’t need to change this setting :)

See also DEFAULT_JINJA2_EXTENSIONS

This option preserves variable types during template operations.

See also DEFAULT_JINJA2_NATIVE

Enables/disables the cleaning up of the temporary files Ansible used to execute the tasks on the remote.If this option is enabled it will disable ANSIBLE_PIPELINING.

See also DEFAULT_KEEP_REMOTE_FILES

This setting causes libvirt to connect to LXC containers by passing --noseclabel parameter to virsh command. This is necessary when running on systems which do not have SELinux.

See also DEFAULT_LIBVIRT_LXC_NOSECLABEL

Controls whether callback plugins are loaded when running /usr/bin/ansible. This may be used to log activity from the command line, send notifications, and so on. Callback plugins are always loaded for ansible-playbook.

See also DEFAULT_LOAD_CALLBACK_PLUGINS

Temporary directory for Ansible to use on the controller.

See also DEFAULT_LOCAL_TMP

File to which Ansible will log on the controller.When not set the logging is disabled.

See also DEFAULT_LOG_PATH

List of logger names to filter out of the log file.

See also DEFAULT_LOG_FILTER

Colon-separated paths in which Ansible will search for Lookup Plugins.

See also DEFAULT_LOOKUP_PLUGIN_PATH

This sets the default arguments to pass to the ansible adhoc binary if no -a is specified.

See also DEFAULT_MODULE_ARGS

Colon-separated paths in which Ansible will search for Modules.

See also DEFAULT_MODULE_PATH

Colon-separated paths in which Ansible will search for Module utils files, which are shared by modules.

See also DEFAULT_MODULE_UTILS_PATH

Colon-separated paths in which Ansible will search for Netconf Plugins.

See also DEFAULT_NETCONF_PLUGIN_PATH

Toggle Ansible’s display and logging of task details, mainly used to avoid security disclosures.

See also DEFAULT_NO_LOG

Toggle Ansible logging to syslog on the target when it executes tasks. On Windows hosts, this will disable a newer style PowerShell modules from writing to the event log.

See also DEFAULT_NO_TARGET_SYSLOG

What templating should return as a ‘null’ value. When not set it will let Jinja2 decide.

See also DEFAULT_NULL_REPRESENTATION

For asynchronous tasks in Ansible (covered in Asynchronous Actions and Polling), this is how often to check back on the status of those tasks when an explicit poll interval is not supplied. The default is a reasonably moderate 15 seconds which is a tradeoff between checking in frequently and providing a quick turnaround when something may have completed.

See also DEFAULT_POLL_INTERVAL

Option for connections using a certificate or key file to authenticate, rather than an agent or passwords, you can set the default value here to avoid re-specifying --private-key with every invocation.

See also DEFAULT_PRIVATE_KEY_FILE

By default, imported roles publish their variables to the play and other roles, this setting can avoid that.This was introduced as a way to reset role variables to default values if a role is used more than once in a playbook.Starting in version ‘2.17’ M(ansible.builtin.include_roles) and M(ansible.builtin.import_roles) can individually override this via the C(public) parameter.Included roles only make their variables public at execution, unlike imported roles which happen at playbook compile time.

See also DEFAULT_PRIVATE_ROLE_VARS

Port to use in remote connections, when blank it will use the connection plugin default.

See also DEFAULT_REMOTE_PORT

Sets the login user for the target machinesWhen blank it uses the connection plugin’s default, normally the user currently executing Ansible.

See also DEFAULT_REMOTE_USER

Colon-separated paths in which Ansible will search for Roles.

See also DEFAULT_ROLES_PATH

Some filesystems do not support safe operations and/or return inconsistent errors, this setting makes Ansible ‘tolerate’ those in the list without causing fatal errors.Data corruption may occur and writes are not always verified when a filesystem is in the list.

See also DEFAULT_SELINUX_SPECIAL_FS

Set the main callback used to display Ansible output. You can only have one at a time.You can have many other callbacks, but just one can be in charge of stdout.See Callback plugins for a list of available options.

See also DEFAULT_STDOUT_CALLBACK

for the cases in which Ansible needs to return a file within an editor, this chooses the application to use.

for the cases in which Ansible needs to return a file within an editor, this chooses the application to use.

Whether or not to enable the task debugger, this previously was done as a strategy plugin.Now all strategy plugins can inherit this behavior. The debugger defaults to activating whena task is failed on unreachable. Use the debugger keyword for more flexibility.

See also ENABLE_TASK_DEBUGGER

This option defines whether the task debugger will be invoked on a failed task when ignore_errors=True is specified.True specifies that the debugger will honor ignore_errors, and False will not honor ignore_errors.

See also TASK_DEBUGGER_IGNORE_ERRORS

Set the default strategy used for plays.

See also DEFAULT_STRATEGY

Colon-separated paths in which Ansible will search for Strategy Plugins.

See also DEFAULT_STRATEGY_PLUGIN_PATH

Toggle the use of “su” for tasks.

Syslog facility to use when Ansible logs to the remote target.

See also DEFAULT_SYSLOG_FACILITY

Colon-separated paths in which Ansible will search for Terminal Plugins.

See also DEFAULT_TERMINAL_PLUGIN_PATH

Colon-separated paths in which Ansible will search for Jinja2 Test Plugins.

See also DEFAULT_TEST_PLUGIN_PATH

This is the default timeout for connection plugins to use.

See also DEFAULT_TIMEOUT

Can be any connection plugin available to your ansible installation.There is also a (DEPRECATED) special ‘smart’ option, that will toggle between ‘ssh’ and ‘paramiko’ depending on controller OS and ssh versions.

See also DEFAULT_TRANSPORT

When True, this causes ansible templating to fail steps that reference variable names that are likely typoed.Otherwise, any ‘{{ template_expression }}’ that contains undefined variables will be rendered in a template or ansible action line exactly as written.

See also DEFAULT_UNDEFINED_VAR_BEHAVIOR

Colon-separated paths in which Ansible will search for Vars Plugins.

See also DEFAULT_VARS_PLUGIN_PATH

If true, decrypting vaults with a vault id will only try the password from the matching vault-id.

See also DEFAULT_VAULT_ID_MATCH

The label to use for the default vault id label in cases where a vault id label is not provided.

See also DEFAULT_VAULT_IDENTITY

The salt to use for the vault encryption. If it is not provided, a random salt will be used.

See also VAULT_ENCRYPT_SALT

The vault_id to use for encrypting by default. If multiple vault_ids are provided, this specifies which to use for encryption. The --encrypt-vault-id CLI option overrides the configured value.

See also DEFAULT_VAULT_ENCRYPT_IDENTITY

A list of vault-ids to use by default. Equivalent to multiple --vault-id args. Vault-ids are tried in order.

See also DEFAULT_VAULT_IDENTITY_LIST

The vault password file to use. Equivalent to --vault-password-file or --vault-id.If executable, it will be run and the resulting stdout will be used as the password.

See also DEFAULT_VAULT_PASSWORD_FILE

Sets the default verbosity, equivalent to the number of -v passed in the command line.

See also DEFAULT_VERBOSITY

Toggle to control the showing of deprecation warnings

See also DEPRECATION_WARNINGS

Toggle to control showing warnings related to running devel.

See also DEVEL_WARNING

Configuration toggle to tell modules to show differences when in ‘changed’ status, equivalent to --diff.

Number of lines of context to show when displaying the differences between files.

See also DIFF_CONTEXT

Normally ansible-playbook will print a header for each task that is run. These headers will contain the name: field from the task if you specified one. If you didn’t then ansible-playbook uses the task’s action to help you tell which task is presently running. Sometimes you run many of the same action and so you want more information about the task to differentiate it from others of the same action. If you set this variable to True in the config then ansible-playbook will also include the task’s arguments in the header.This setting defaults to False because there is a chance that you have sensitive values in your parameters and you do not want those to be printed.If you set this to True you should be sure that you have secured your environment’s stdout (no one can shoulder surf your screen and you aren’t saving stdout to an insecure file) or made sure that all of your playbooks explicitly added the no_log: True parameter to tasks that have sensitive values How do I keep secret data in my playbook? for more information.

See also DISPLAY_ARGS_TO_STDOUT

Toggle to control displaying skipped task/host entries in a task in the default callback.

See also DISPLAY_SKIPPED_HOSTS

When to include tracebacks in extended error messages

See also DISPLAY_TRACEBACK

By default, Ansible will issue a warning when a duplicate dict key is encountered in YAML.These warnings can be silenced by adjusting this setting to False.

See also DUPLICATE_YAML_DICT_KEY

Toggle to allow missing handlers to become a warning instead of an error when notifying.

See also ERROR_ON_MISSING_HANDLER

Which modules to run during a play’s fact gathering stage, using the default of ‘smart’ will try to figure it out based on connection type.If adding your own modules but you still want to use the default Ansible facts, you will want to include ‘setup’ or corresponding network module to the list (if you add ‘smart’, Ansible will also figure it out).This does not affect explicit calls to the ‘setup’ module, but does always affect the ‘gather_facts’ action (implicit or explicit).

See also FACTS_MODULES

If set to yes, ansible-galaxy will not validate TLS certificates. This can be useful for testing against a server with a self-signed certificate.

See also GALAXY_IGNORE_CERTS

The default timeout for Galaxy API calls. Galaxy servers that don’t configure a specific timeout will fall back to this value.

See also GALAXY_SERVER_TIMEOUT

Role skeleton directory to use as a template for the init action in ansible-galaxy/ansible-galaxy role, same as --role-skeleton.

See also GALAXY_ROLE_SKELETON

patterns of files to ignore inside a Galaxy role or collection skeleton directory.

See also GALAXY_ROLE_SKELETON_IGNORE

Collection skeleton directory to use as a template for the init action in ansible-galaxy collection, same as --collection-skeleton.

See also GALAXY_COLLECTION_SKELETON

patterns of files to ignore inside a Galaxy collection skeleton directory.

See also GALAXY_COLLECTION_SKELETON_IGNORE

whether ansible-galaxy collection install should warn about --collections-path missing from configured COLLECTIONS_PATHS.

See also GALAXY_COLLECTIONS_PATH_WARNING

URL to prepend when roles don’t specify the full URI, assume they are referencing this server as the source.

See also GALAXY_SERVER

A list of Galaxy servers to use when installing a collection.The value corresponds to the config ini header [galaxy_server.{{item}}] which defines the server details.See Configuring the ansible-galaxy client for more details on how to define a Galaxy server.The order of servers in this list is used as the order in which a collection is resolved.Setting this config option will ignore the GALAXY_SERVER config option.

See also GALAXY_SERVER_LIST

Local path to galaxy access token file

See also GALAXY_TOKEN_PATH

Some steps in ansible-galaxy display a progress wheel which can cause issues on certain displays or when outputting the stdout to a file.This config option controls whether the display wheel is shown or not.The default is to show the display wheel if stdout has a tty.

See also GALAXY_DISPLAY_PROGRESS

The directory that stores cached responses from a Galaxy server.This is only used by the ansible-galaxy collection install and download commands.Cache files inside this dir will be ignored if they are world writable.

See also GALAXY_CACHE_DIR

Disable GPG signature verification during collection installation.

See also GALAXY_DISABLE_GPG_VERIFY

Configure the keyring used for GPG signature verification during collection installation and verification.

See also GALAXY_GPG_KEYRING

A list of GPG status codes to ignore during GPG signature verification. See L(https://github.com/gpg/gnupg/blob/master/doc/DETAILS#general-status-codes) for status code descriptions.If fewer signatures successfully verify the collection than GALAXY_REQUIRED_VALID_SIGNATURE_COUNT, signature verification will fail even if all error codes are ignored.

See also GALAXY_IGNORE_INVALID_SIGNATURE_STATUS_CODES

The number of signatures that must be successful during GPG signature verification while installing or verifying collections.This should be a positive integer or all to indicate all signatures must successfully validate the collection.Prepend + to the value to fail if no valid signatures are found for the collection.

See also GALAXY_REQUIRED_VALID_SIGNATURE_COUNT

The initial interval in seconds for polling the import status of a collection.This interval increases exponentially based on the GALAXY_COLLECTION_IMPORT_POLL_FACTOR, with a maximum delay of 30 seconds.

See also GALAXY_COLLECTION_IMPORT_POLL_INTERVAL

The multiplier used to increase the GALAXY_COLLECTION_IMPORT_POLL_INTERVAL when checking the collection import status.

See also GALAXY_COLLECTION_IMPORT_POLL_FACTOR

Set this to “False” if you want to avoid host key checking by the underlying connection plugin Ansible uses to connect to the host.Please read the documentation of the specific connection plugin used for details.

See also HOST_KEY_CHECKING

This setting changes the behaviour of mismatched host patterns, it allows you to force a fatal error, a warning or just ignore it.

See also HOST_PATTERN_MISMATCH

Path to the Python interpreter to be used for module execution on remote targets, or an automatic discovery mode. Supported discovery modes are auto (the default), auto_silent, auto_legacy, and auto_legacy_silent. All discovery modes match against an ordered list of well-known Python interpreter locations. The fallback behavior will issue a warning that the interpreter should be set explicitly (since interpreters installed later may change which one is used). This warning behavior can be disabled by setting auto_silent. The auto_legacy modes are deprecated and behave the same as their respective auto modes. They exist for backward-compatibility with older Ansible releases that always defaulted to /usr/bin/python3, which will use that interpreter if present.

See also INTERPRETER_PYTHON

Make ansible transform invalid characters in group names supplied by inventory sources.

See also TRANSFORM_INVALID_GROUP_CHARS

If ‘false’, invalid attributes for a task will result in warnings instead of errors.

See also INVALID_TASK_ATTRIBUTE_FAILED

If ‘true’, it is a fatal error when any given inventory source cannot be successfully parsed by any available inventory plugin; otherwise, this situation only attracts a warning.

See also INVENTORY_ANY_UNPARSED_IS_FAILED

List of enabled inventory plugins, it also determines the order in which they are used.

See also INVENTORY_ENABLED

Controls if ansible-inventory will accurately reflect Ansible’s view into inventory or its optimized for exporting.

See also INVENTORY_EXPORT

List of extensions to ignore when using a directory as an inventory source.

See also INVENTORY_IGNORE_EXTS

List of patterns to ignore when using a directory as an inventory source.

See also INVENTORY_IGNORE_PATTERNS

If ‘true’ it is a fatal error if every single potential inventory source fails to parse, otherwise, this situation will only attract a warning.

See also INVENTORY_UNPARSED_IS_FAILED

Maximum size of files to be considered for diff display.

See also MAX_FILE_SIZE_FOR_DIFF

See also NETWORK_GROUP_MODULES

Facts are available inside the ansible_facts variable, this setting also pushes them as their own vars in the main namespace.Unlike inside the ansible_facts dictionary where the prefix ansible_ is removed from fact names, these will have the exact names that are returned by the module.

See also INJECT_FACTS_AS_VARS

List of extensions to ignore when looking for modules to load.This is for rejecting script and binary module fallback extensions.

See also MODULE_IGNORE_EXTS

Enables whether module responses are evaluated for containing non-UTF-8 data.Disabling this may result in unexpected behavior.Only ansible-core should evaluate this configuration.

See also MODULE_STRICT_UTF8_RESPONSE

Previously Ansible would only clear some of the plugin loading caches when loading new roles, this led to some behaviors in which a plugin loaded in previous plays would be unexpectedly ‘sticky’. This setting allows the user to return to that behavior.

See also OLD_PLUGIN_CACHE_CLEARING

for the cases in which Ansible needs to return output in a pageable fashion, this chooses the application to use.

for the cases in which Ansible needs to return output in a pageable fashion, this chooses the application to use.

See also PARAMIKO_HOST_KEY_AUTO_ADD

See also PARAMIKO_LOOK_FOR_KEYS

Path to the socket to be used by the connection persistence system.

See also PERSISTENT_CONTROL_PATH_DIR

This controls how long the persistent connection will remain idle before it is destroyed.

See also PERSISTENT_CONNECT_TIMEOUT

This controls the retry timeout for persistent connection to connect to the local domain socket.

See also PERSISTENT_CONNECT_RETRY_TIMEOUT

This controls the amount of time to wait for a response from a remote device before timing out a persistent connection.

See also PERSISTENT_COMMAND_TIMEOUT

A number of non-playbook CLIs have a --playbook-dir argument; this sets the default value for it.

See also PLAYBOOK_DIR

This sets which playbook dirs will be used as a root to process vars plugins, which includes finding host_vars/group_vars.

See also PLAYBOOK_VARS_ROOT

Attempts to set RLIMIT_NOFILE soft limit to the specified value when executing Python modules (can speed up subprocess usage on Python 2.x. See https://bugs.python.org/issue11284). The value will be limited by the existing hard limit. Default value of 0 does not attempt to adjust existing system-defined limits.

See also PYTHON_MODULE_RLIMIT_NOFILE

This controls whether a failed Ansible playbook should create a .retry file.

See also RETRY_FILES_ENABLED

This sets the path in which Ansible will save .retry files when a playbook fails and retry files are enabled.This file will be overwritten after each run with the list of failed hosts from all plays.

See also RETRY_FILES_SAVE_PATH

This setting can be used to optimize vars_plugin usage depending on the user’s inventory size and play selection.

See also RUN_VARS_PLUGINS

This adds the custom stats set via the set_stats plugin to the default output.

See also SHOW_CUSTOM_STATS

Manage an SSH Agent via Ansible. A configuration of none will not interact with an agent, auto will start and destroy an agent via ssh-agent binary during the run, and a path to an SSH_AUTH_SOCK will allow interaction with a pre-existing agent.

When SSH_AGENT is auto, the path or name of the ssh agent executable to start.

See also SSH_AGENT_EXECUTABLE

For keys inserted into an agent defined by SSH_AGENT, define a lifetime, in seconds, that the key may remain in the agent.

See also SSH_AGENT_KEY_LIFETIME

This list of filters avoids ‘type conversion’ when templating variables.Useful when you want to avoid conversion into lists or dictionaries for JSON strings, for example.

See also STRING_TYPE_FILTERS

Allows disabling of warnings related to potential issues on the system running Ansible itself (not on the managed hosts).These may include warnings about third-party packages or other conditions that should be resolved if possible.

See also SYSTEM_WARNINGS

default list of tags to run in your plays, Skip Tags has precedence.

default list of tags to skip in your plays, has precedence over Run Tags

A string to insert into target logging for tracking purposes

See also TARGET_LOG_INFO

Set the maximum time (in seconds) for a task action to execute in.Timeout runs independently from templating or looping. It applies per each attempt of executing the task’s action and remains unchanged by the total time spent on a task.When the action execution exceeds the timeout, Ansible interrupts the process. This is registered as a failure due to outside circumstances, not a task failure, to receive appropriate response and recovery process.If set to 0 (the default) there is no timeout.

See also TASK_TIMEOUT

The maximum number of times to check Task Queue Manager worker processes to verify they have exited cleanly.After this limit is reached any worker processes still running will be terminated.This is for internal use only.

See also WORKER_SHUTDOWN_POLL_COUNT

The number of seconds to sleep between polling loops when checking Task Queue Manager worker processes to verify they have exited cleanly.This is for internal use only.

See also WORKER_SHUTDOWN_POLL_DELAY

Toggles the use of persistence for connections.

See also USE_PERSISTENT_CONNECTIONS

Accept list for variable plugins that require it.

See also VARIABLE_PLUGINS_ENABLED

Allows to change the group variable precedence merge order.

See also VARIABLE_PRECEDENCE

For asynchronous tasks in Ansible (covered in Asynchronous Actions and Polling), this is how long, in seconds, to wait for the task spawned by Ansible to connect back to the named pipe used on Windows systems. The default is 5 seconds. This can be too low on slower systems, or systems under heavy load.This is not the total time an async command can run for, but is a separate timeout to wait for an async command to start. The task will only start to be timed against its async_timeout once it has connected to the pipe, so the overall maximum duration the task can take will be extended by the amount specified here.

See also WIN_ASYNC_STARTUP_TIMEOUT

Check all of these extensions when looking for ‘variable’ files which should be YAML or JSON or vaulted versions of these.This affects vars_files, include_vars, inventory and vars plugins among others.

See also YAML_FILENAME_EXTENSIONS

This variable is used to enable bastion/jump host with netconf connection. If set to True the bastion/jump host ssh settings should be present in ~/.ssh/config file, alternatively it can be set to custom ssh configuration file path to read the bastion/jump host settings.

See also NETCONF_SSH_CONFIG

A toggle to disable validating a collection’s ‘metadata’ entry for a module_defaults action group. Metadata containing unexpected fields or value types will produce a warning when this is True.

See also VALIDATE_ACTION_GROUP_METADATA

Force ‘verbose’ option to use stderr instead of stdout

See also VERBOSE_TO_STDERR

**Examples:**

Example 1 (unknown):
```unknown
# some basic default values...
inventory = /etc/ansible/hosts  ; This points to the file that lists your hosts
```

Example 2 (unknown):
```unknown
$ ansible-config init --disabled > ansible.cfg
```

Example 3 (unknown):
```unknown
$ ansible-config init --disabled -t all > ansible.cfg
```

---

## Python 3 Support — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/python_3_support.html

**Contents:**
- Python 3 Support
- On the control node side
- Using Python 3 on the managed machines with commands and playbooks
- What to do if an incompatibility is found

Ansible 2.5 and above work with Python 3. Previous to 2.5, using Python 3 was considered a tech preview. This topic discusses how to set up your control node and managed machines to use Python 3.

See Control Node Requirements and Managed Node Requirements for the specific versions supported.

The easiest way to run /usr/bin/ansible under Python 3 is to install it with the Python3 version of pip. This will make the default /usr/bin/ansible run with Python3:

If you are running Ansible Running the devel branch from a clone and want to use Python 3 with your source checkout, run your command through python3. For example:

Individual Linux distribution packages may be packaged for Python2 or Python3. When running from distro packages you’ll only be able to use Ansible with the Python version for which it was installed. Sometimes distros will provide a means of installing for several Python versions (through a separate package or through some commands that are run after install). You’ll need to check with your distro to see if that applies in your case.

Ansible will automatically detect and use Python 3 on many platforms that ship with it. To explicitly configure a Python 3 interpreter, set the ansible_python_interpreter inventory variable at a group or host level to the location of a Python 3 interpreter, such as /usr/bin/python3. The default interpreter path may also be set in ansible.cfg.

Interpreter Discovery for more information.

How to build your inventory for more information.

Run your command or playbook:

Note that you can also use the -e command line option to manually set the python interpreter when you run a command. This can be useful if you want to test whether a specific module or playbook has any bugs under Python 3. For example:

We have spent several releases squashing bugs and adding new tests so that Ansible’s core feature set runs under both Python 2 and Python 3. However, bugs may still exist in edge cases and many of the modules shipped with Ansible are maintained by the community and not all of those may be ported yet.

If you find a bug running under Python 3 you can submit a bug report on Ansible’s GitHub project. Be sure to mention Python3 in the bug report so that the right people look at it.

If you would like to fix the code and submit a pull request on github, you can refer to Ansible and Python 3 for information on how we fix common Python3 compatibility issues in the Ansible codebase.

**Examples:**

Example 1 (unknown):
```unknown
$ pip3 install ansible
$ ansible --version | grep "python version"
  python version = 3.10.5 (main, Jun 9 2022, 00:00:00) [GCC 12.1.1 20220507 (Red Hat 12.1.1-1)] (/usr/bin/python)
```

Example 2 (unknown):
```unknown
$ source ./hacking/env-setup
$ python3 $(which ansible) localhost -m ping
$ python3 $(which ansible-playbook) sample-playbook.yml
```

Example 3 (unknown):
```unknown
# Example inventory that makes an alias for localhost that uses Python3
localhost-py3 ansible_host=localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3

# Example of setting a group of hosts to use Python3
[py3_hosts]
ubuntu16
fedora27

[py3_hosts:vars]
ansible_python_interpreter=/usr/bin/python3
```

Example 4 (unknown):
```unknown
$ ansible localhost-py3 -m ping
$ ansible-playbook sample-playbook.yml
```

---
