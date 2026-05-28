# Ansible-Core - Development

**Pages:** 10

---

## Ansible and Python 3 — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_python_3.html

**Contents:**
- Ansible and Python 3
- Minimum version of Python 3.x and Python 2.x
- Developing Ansible code that supports Python 2 and Python 3
  - Understanding strings in Python 2 and Python 3
    - Control node string strategy: the Unicode Sandwich
  - Unicode Sandwich common borders: places to convert bytes to text in control node code
    - Reading and writing to files
    - Filesystem interaction
    - Interacting with other programs
    - Module string strategy: Native String

The ansible-core code runs Python 3 (for specific versions check Control Node Requirements Contributors to ansible-core and to Ansible Collections should be aware of the tips in this document so that they can write code that will run on the same versions of Python as the rest of Ansible.

Minimum version of Python 3.x and Python 2.x

Developing Ansible code that supports Python 2 and Python 3

Understanding strings in Python 2 and Python 3

Control node string strategy: the Unicode Sandwich

Unicode Sandwich common borders: places to convert bytes to text in control node code

Reading and writing to files

Filesystem interaction

Interacting with other programs

Module string strategy: Native String

Module_utils string strategy: hybrid

Tips, tricks, and idioms for Python 2/Python 3 compatibility

Use forward-compatibility boilerplate

Prefix byte strings with b_

Import Ansible’s bundled Python six library

Handle exceptions with as

String formatting for control node code

Use str.format() for Python 2.6 compatibility

Use percent format with byte strings

We do have some considerations depending on the types of Ansible code:

code on the control node - code that runs on the machine where you invoke /usr/bin/ansible, only needs to support the control node’s Python versions.

modules - the code which Ansible transmits to and invokes on the managed machine. Modules need to support the ‘managed node’ Python versions, with some exceptions.

shared module_utils code - the common code that is used by modules to perform tasks and sometimes used by code on the control node. Shared module_utils code needs to support the same range of Python as the modules.

However, the three types of code do not use the same string strategy. If you’re developing a module or some module_utils code, be sure to read the section on string strategy carefully.

See Control Node Requirements and Managed Node Requirements for the specific versions supported.

Your custom modules can support any version of Python (or other languages) you want, but the above are the requirements for the code contributed to the Ansible project.

The best place to start learning about writing code that supports both Python 2 and Python 3 is Lennart Regebro’s book: Porting to Python 3. The book describes several strategies for porting to Python 3. The one we’re using is to support Python 2 and Python 3 from a single code base

Python 2 and Python 3 handle strings differently, so when you write code that supports Python 3 you must decide what string model to use. Strings can be an array of bytes (like in C) or they can be an array of text. Text is what we think of as letters, digits, numbers, other printable symbols, and a small number of unprintable “symbols” (control codes).

In Python 2, the two types for these (str for bytes and unicode for text) are often used interchangeably. When dealing only with ASCII characters, the strings can be combined, compared, and converted from one type to another automatically. When non-ASCII characters are introduced, Python 2 starts throwing exceptions due to not knowing what encoding the non-ASCII characters should be in.

Python 3 changes this behavior by making the separation between bytes (bytes) and text (str) more strict. Python 3 will throw an exception when trying to combine and compare the two types. The programmer has to explicitly convert from one type to the other to mix values from each.

In Python 3 it is immediately apparent to the programmer when code is mixing the byte and text types inappropriately, whereas in Python 2, code that mixes those types may work until a user causes an exception by entering non-ASCII input. Python 3 forces programmers to proactively define a strategy for working with strings in their program so that they don’t mix text and byte strings unintentionally.

Ansible uses different strategies for working with strings in the code on the control node, in :ref: modules <module_string_strategy>, and in module_utils code.

Until recently ansible-core supported Python 2.x and followed this strategy, known as the Unicode Sandwich (named after Python 2’s unicode text type). For Unicode Sandwich we know that at the border of our code and the outside world (for example, file and network IO, environment variables, and some library calls) we are going to receive bytes. We need to transform these bytes into text and use that throughout the internal portions of our code. When we have to send those strings back out to the outside world we first convert the text back into bytes. To visualize this, imagine a ‘sandwich’ consisting of a top and bottom layer of bytes, a layer of conversion between, and all text type in the center.

For compatibility reasons you will see a bunch of custom functions we developed (to_text/to_bytes/to_native) and while Python 2 is not a concern anymore we will continue to use them as they apply for other cases that make dealing with unicode problematic.

While we will not be using it most of it anymore, the documentation below is still useful for those developing modules that still need to support both Python 2 and 3 simultaneously.

This is a partial list of places where we have to convert to and from bytes when using the Unicode Sandwich string strategy. It is not exhaustive but it gives you an idea of where to watch for problems.

In Python 2, reading from files yields bytes. In Python 3, it can yield text. To make code that’s portable to both we don’t make use of Python 3’s ability to yield text but instead do the conversion explicitly ourselves. For example:

Much of Ansible assumes that all encoded text is UTF-8. At some point, if there is demand for other encodings we may change that, but for now it is safe to assume that bytes are UTF-8.

Writing to files is the opposite process:

Note that we don’t have to catch UnicodeError here because we’re transforming to UTF-8 and all text strings in Python can be transformed back to UTF-8.

Dealing with file names often involves dropping back to bytes because on UNIX-like systems file names are bytes. On Python 2, if we pass a text string to these functions, the text string will be converted to a byte string inside of the function and a traceback will occur if non-ASCII characters are present. In Python 3, a traceback will only occur if the text string can’t be decoded in the current locale, but it is still good to be explicit and have code which works on both versions:

When you are only manipulating a filename as a string without talking to the filesystem (or a C library which talks to the filesystem) you can often get away without converting to bytes:

On the other hand, if the code needs to manipulate the file name and also talk to the filesystem, it can be more convenient to transform to bytes right away and manipulate in bytes.

Make sure all variables passed to a function are the same type. If you’re working with something like os.path.join() which takes multiple strings and uses them in combination, you need to make sure that all the types are the same (either all bytes or all text). Mixing bytes and text will cause tracebacks.

Interacting with other programs goes through the operating system and C libraries and operates on things that the UNIX kernel defines. These interfaces are all byte-oriented so the Python interface is byte oriented as well. On both Python 2 and Python 3, byte strings should be given to Python’s subprocess library and byte strings should be expected back from it.

One of the main places in Ansible’s control node code that we interact with other programs is the connection plugins’ exec_command methods. These methods transform any text strings they receive in the command (and arguments to the command) to execute into bytes and return stdout and stderr as byte strings Higher level functions (like action plugins’ _low_level_execute_command) transform the output into text strings.

In modules we use a strategy known as Native Strings. This makes things easier on the community members who maintain so many of Ansible’s modules, by not breaking backwards compatibility by mandating that all strings inside of modules are text and converting between text and bytes at the borders.

Native strings refer to the type that Python uses when you specify a bare string literal:

In Python 2, these are byte strings. In Python 3 these are text strings. Modules should be coded to expect bytes on Python 2 and text on Python 3.

In module_utils code we use a hybrid string strategy. Although Ansible’s module_utils code is largely like module code, some pieces of it are used by the control node as well. So it needs to be compatible with modules and with the control node’s assumptions, particularly the string strategy. The module_utils code attempts to accept native strings as input to its functions and emit native strings as their output.

In module_utils code:

Functions must accept string parameters as either text strings or byte strings.

Functions may return either the same type of string as they were given or the native string type for the Python version they are run on.

Functions that return strings must document whether they return strings of the same type as they were given or native strings.

Module-utils functions are therefore often very defensive in nature. They convert their string parameters into text (using ansible.module_utils.common.text.converters.to_text) at the beginning of the function, do their work, and then convert the return values into the native string type (using ansible.module_utils.common.text.converters.to_native) or back to the string type that their parameters received.

Use the following boilerplate code at the top of all python files to make certain constructs act the same way on Python 2 and Python 3:

__metaclass__ = type makes all classes defined in the file into new-style classes without explicitly inheriting from object.

The __future__ imports do the following:

Makes imports look in sys.path for the modules being imported, skipping the directory in which the module doing the importing lives. If the code wants to use the directory in which the module doing the importing, there’s a new dot notation to do so.

Makes division of integers always return a float. If you need to find the quotient use x // y instead of x / y.

Changes print from a keyword into a function.

PEP 0328: Absolute Imports

PEP 3105: Print function

Since mixing text and bytes types leads to tracebacks we want to be clear about what variables hold text and what variables hold bytes. We do this by prefixing any variable holding bytes with b_. For example:

We do not prefix the text strings instead because we only operate on byte strings at the borders, so there are fewer variables that need bytes than text.

The third-party Python six library exists to help projects create code that runs on both Python 2 and Python 3. Ansible includes a version of the library in module_utils so that other modules can use it without requiring that it is installed on the remote system. To make use of it, import it like this:

Ansible can also use a system copy of six

Ansible will use a system copy of six if the system copy is a later version than the one Ansible bundles.

In order for code to function on Python 2.6+ and Python 3, use the new exception-catching syntax which uses the as keyword:

Do not use the following syntax as it will fail on every version of Python 3:

In Python 2.x, octal literals could be specified as 0755. In Python 3, octals must be specified as 0o755.

Starting in Python 2.6, strings gained a method called format() to put strings together. However, one commonly used feature of format() wasn’t added until Python 2.7, so you need to remember not to use it in Ansible code:

Both of the format strings above map positional arguments of the format() method into the string. However, the first version doesn’t work in Python 2.6. Always remember to put numbers into the placeholders so the code is compatible with Python 2.6.

Python documentation on format strings:

format strings in 2.6

format strings in 3.x

In Python 3.5 and later, byte strings do not have a format() method. However, it does have support for the older, percent-formatting.

**Examples:**

Example 1 (python):
```python
from ansible.module_utils.common.text.converters import to_text

with open('filename-with-utf8-data.txt', 'rb') as my_file:
    b_data = my_file.read()
    try:
        data = to_text(b_data, errors='surrogate_or_strict')
    except UnicodeError:
        # Handle the exception gracefully -- usually by displaying a good
        # user-centric error message that can be traced back to this piece
        # of code.
        pass
```

Example 2 (python):
```python
from ansible.module_utils.common.text.converters import to_bytes

with open('filename.txt', 'wb') as my_file:
    my_file.write(to_bytes(some_text_string))
```

Example 3 (python):
```python
import os.path

from ansible.module_utils.common.text.converters import to_bytes

filename = u'/var/tmp/くらとみ.txt'
f = open(to_bytes(filename), 'wb')
mtime = os.path.getmtime(to_bytes(filename))
b_filename = os.path.expandvars(to_bytes(filename))
if os.path.exists(to_bytes(filename)):
    pass
```

Example 4 (unknown):
```unknown
import os.path

os.path.join(u'/var/tmp/café', u'くらとみ')
os.path.split(u'/var/tmp/café/くらとみ')
```

---

## ansible-core project branches and tags — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/core_branches_and_tags.html

**Contents:**
- ansible-core project branches and tags
- devel branch
- stable-X.Y branches
- vX.Y.Z tags
- milestone branch

All new development on the next version of ansible-core occurs exclusively in the devel branch, and all bugfixes to prior releases must first be merged to devel before being backported to one or more stable branches for inclusion in servicing releases. Around the Beta 1 milestone, a new stable-X.Y branch is cut from devel, which is then updated to host development of the X.Y+1 release. External automated testing of Ansible content from devel is not generally recommended.

All ansible-core X.Y.Z releases are created from a corresponding stable-X.Y branch. A release’s stable branch is typically cut from devel around X.Y.0 beta 1 (when the release is feature complete). All further bugfixes (no enhancements!) must be made against devel and backported to applicable stable branches.

Each ansible-core vX.Y.Z release is tagged from the release commit in the corresponding stable-X.Y branch, allowing access to the exact source used to create the release. As of ansible-core 2.13, the auto-generated GitHub tarball of the tag contents is considered the official canonical release artifact.

A milestone branch is a slow-moving stream of the devel branch, intended for external testing of ansible-core features under active development. As described in the ansible-core Roadmaps for a given release, development is typically split into three phases of decreasing duration, with larger and more invasive changes targeted to be merged to devel in earlier phases. The milestone branch is updated to the contents of devel at the end of each development phase. This allows testing of semi-stable unreleased features on a predictable schedule without the exposure to the potential instability of the daily commit “fire hose” from devel. When a release reaches the Beta 1 milestone, the milestone branch will be updated to the first devel commit after the version number has been increased. Further testing of the same release should be done from the new stable-X.Y branch that was created. If a severe issue that significantly affects community testing or stability is discovered in the milestone branch, the branch contents may require unscheduled adjustment, but not in a way that prevents fast-forward updates (for example, milestone-only commits will not be created or cherry-picked from devel).

The following example is for illustrative purposes only. See the ansible-core Roadmaps for accurate dates. For example, the milestone branch in 2.13 ansible-core roadmap updated as follows:

27-Sep-2021: 2.13 Development Phase 1 begins; milestone contents are updated to 2.12.0b1 with version number set to 2.13.0.dev0. Automated content testing that includes version-specific ignore files (e.g., ignore-2.12.txt) should copy them for the current version (e.g., ignore-2.13.txt) before this point to ensure that automated sanity testing against the milestone branch will continue to pass.

13-Dec-2021: 2.13 Development Phase 2 begins; milestone contents are updated to the final commit from Development Phase 1

14-Feb-2022: 2.13 Development Phase 3 begins; milestone contents are updated to the final commit from Development Phase 2

11-Apr-2022: stable-2.13 branch created with results from Development Phase 3 and freeze. 2.13.0b1 is released from stable-2.13. Automated content testing should continue 2.13 series testing against the new branch. The devel version number is updated to 2.14.0.dev0, and milestone is updated to that point.

---

## Rebasing a pull request — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_rebasing.html

**Contents:**
- Rebasing a pull request
- Configuring your remotes
- Rebasing your branch
- Updating your pull request
- Getting help rebasing

You may find that your pull request (PR) is out-of-date and needs to be rebased. This can happen for several reasons:

Files modified in your PR are in conflict with changes which have already been merged.

Your PR is old enough that significant changes to automated test infrastructure have occurred.

Rebasing the branch used to create your PR will resolve both of these issues.

Before you can rebase your PR, you need to make sure you have the proper remotes configured. These instructions apply to any repository on GitHub, including collections repositories. On other platforms (bitbucket, gitlab), the same principles and commands apply but the syntax may be different. We use the ansible/ansible repository here as an example. In other repositories, the branch names may be different. Assuming you cloned your fork in the usual fashion, the origin remote will point to your fork:

However, you also need to add a remote which points to the upstream repository:

Which should leave you with the following remotes:

Checking the status of your branch should show your fork is up-to-date with the origin remote:

Once you have an upstream remote configured, you can rebase the branch for your PR:

This will replay the changes in your branch on top of the changes made in the upstream devel branch. If there are merge conflicts, you will be prompted to resolve those before you can continue.

After you rebase, the status of your branch changes:

Don’t worry, this is normal after a rebase. You should ignore the git status instructions to use git pull. We’ll cover what to do next in the following section.

Now that you’ve rebased your branch, you need to push your changes to GitHub to update your PR.

Since rebasing re-writes Git history, you will need to use a force push:

Your PR on GitHub has now been updated. This will automatically trigger testing of your changes. You should check in on the status of your PR after tests have completed to see if further changes are required.

If you need any help with rebasing your PR, or you have other development related questions, visit the Ansible communication guide for information on how to reach out to the community.

Information on roadmaps, opening PRs, Ansibullbot, and more

**Examples:**

Example 1 (unknown):
```unknown
$ git remote -v
origin  [email protected]:YOUR_GITHUB_USERNAME/ansible.git (fetch)
origin  [email protected]:YOUR_GITHUB_USERNAME/ansible.git (push)
```

Example 2 (unknown):
```unknown
$ git remote add upstream https://github.com/ansible/ansible.git
```

Example 3 (unknown):
```unknown
$ git remote -v
origin  [email protected]:YOUR_GITHUB_USERNAME/ansible.git (fetch)
origin  [email protected]:YOUR_GITHUB_USERNAME/ansible.git (push)
upstream        https://github.com/ansible/ansible.git (fetch)
upstream        https://github.com/ansible/ansible.git (push)
```

Example 4 (unknown):
```unknown
$ git status
On branch YOUR_BRANCH
Your branch is up-to-date with 'origin/YOUR_BRANCH'.
nothing to commit, working tree clean
```

---

## pep8 — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing/sanity/pep8.html

**Contents:**
- pep8
- Running locally

Python static analysis for PEP 8 style guideline compliance.

PEP 8 style guidelines are enforced by pycodestyle on all python files in the repository by default.

The PEP 8 check can be run locally as follows:

**Examples:**

Example 1 (unknown):
```unknown
ansible-test sanity --test pep8 [file-or-directory-path-to-check] ...
```

---

## Developing ansible-core — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_core.html

**Contents:**
- Developing ansible-core

Although ansible-core (the code hosted in the ansible/ansible repository on GitHub) includes a few plugins that can be swapped out by the playbook directives or configuration, much of the code there is not modular. The documents here give insight into how the parts of ansible-core work together.

Learn about the Python API for task execution

Learn about developing plugins

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

---

## Unit Tests — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_units.html

**Contents:**
- Unit Tests
- Available Tests
- Running Tests
- Installing dependencies
- Extending unit tests
  - Structuring Unit Tests
  - Module test case common code
  - Fixtures files
  - Code Coverage For New or Updated Unit Tests

Unit tests are small isolated tests that target a specific library or module. Unit tests in Ansible are currently the only way of driving tests from python within Ansible’s continuous integration process. This means that in some circumstances the tests may be a bit wider than just units.

Installing dependencies

Structuring Unit Tests

Module test case common code

Code Coverage For New or Updated Unit Tests

Unit tests can be found in test/units. Notice that the directory structure of the tests matches that of lib/ansible/.

To run unit tests using docker, always use the default docker image by passing the --docker or --docker default argument.

The Ansible unit tests can be run across the whole code base by doing:

Against a single file by doing:

Or against a specific Python version by doing:

If you are running unit tests against things other than modules, such as module utilities, specify the whole file path:

For advanced usage see the online help:

You can also run tests in Ansible’s continuous integration system by opening a pull request. This will automatically determine which tests to run based on the changes made in your pull request.

If you are running ansible-test with the --docker or --venv option you do not need to install dependencies manually.

Otherwise you can install dependencies using the --requirements option, which will install all the required dependencies needed for unit tests. For example:

The list of unit test requirements can be found at test/units/requirements.txt.

This does not include the list of unit test requirements for ansible-test itself, which can be found at test/lib/ansible_test/_data/requirements/units.txt.

See also the constraints applicable to all test commands.

What a unit test isn’t

If you start writing a test that requires external services then you may be writing an integration test, rather than a unit test.

Ansible drives unit tests through pytest. This means that tests can either be written a simple functions which are included in any file name like test_<something>.py or as classes.

Here is an example of a function:

Here is an example of a class:

Both methods work fine in most circumstances; the function-based interface is simpler and quicker and so that’s probably where you should start when you are just trying to add a few basic tests for a module. The class-based test allows more tidy set up and tear down of pre-requisites, so if you have many test cases for your module you may want to refactor to use that.

Assertions using the simple assert function inside the tests will give full information on the cause of the failure with a trace-back of functions called during the assertion. This means that plain asserts are recommended over other external assertion libraries.

A number of the unit test suites include functions that are shared between several modules, especially in the networking arena. In these cases a file is created in the same directory, which is then included directly.

Keep common code as specific as possible within the test/units/ directory structure. Don’t import common unit test code from directories outside the current or parent directories.

Don’t import other unit tests from a unit test. Any common code should be in dedicated files that aren’t themselves tests.

To mock out fetching results from devices, or provide other complex data structures that come from external libraries, you can use fixtures to read in pre-generated data.

You can check how fixtures are used in CPU_INFO_TEST_SCENARIOS

If you are simulating APIs you may find that Python placebo is useful. See Unit Testing Ansible Modules for more information.

New code will be missing from the codecov.io coverage reports (see Testing Ansible), so local reporting is needed. Most ansible-test commands allow you to collect code coverage; this is particularly useful when to indicate where to extend testing.

To collect coverage data add the --coverage argument to your ansible-test command line:

Results will be written to test/results/reports/coverage/index.html

Reports can be generated in several different formats:

ansible-test coverage report - Console report.

ansible-test coverage html - HTML report.

ansible-test coverage xml - XML report.

To clear data between test runs, use the ansible-test coverage erase command. See Testing Ansible and Collections for more information about generating coverage reports.

Special considerations for unit testing modules

Running tests locally including gathering and reporting coverage data

The documentation of the unittest framework in python 3

The documentation of the earliest supported unittest framework - from Python 2.6

The documentation of pytest - the framework actually used to run Ansible unit tests

**Examples:**

Example 1 (unknown):
```unknown
cd /path/to/ansible/source
source hacking/env-setup
ansible-test units --docker -v
```

Example 2 (unknown):
```unknown
ansible-test units --docker -v apt
```

Example 3 (unknown):
```unknown
ansible-test units --docker -v --python 2.7 apt
```

Example 4 (unknown):
```unknown
ansible-test units --docker -v test/units/module_utils/basic/test_imports.py
```

---

## Using and developing module utilities — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/developing_module_utilities.html

**Contents:**
- Using and developing module utilities
- Naming and finding module utilities
- Standard module utilities

Ansible provides a number of module utilities, or snippets of shared code, that provide helper functions you can use when developing your own modules. The basic.py module utility provides the main entry point for accessing the Ansible library, and all Python Ansible modules must import something from ansible.module_utils. A common option is to import AnsibleModule:

The ansible.module_utils namespace is not a plain Python package: it is constructed dynamically for each task invocation, by extracting imports and resolving those matching the namespace against a search path derived from the active configuration.

To reduce the maintenance burden in a collection or in local modules, you can extract duplicated code into one or more module utilities and import them into your modules. For example, if you have your own custom modules that import a my_shared_code library, you can place that into a ./module_utils/my_shared_code.py file like this:

When you run ansible-playbook, Ansible will merge any files in your local module_utils directories into the ansible.module_utils namespace in the order defined by the Ansible search path.

You can generally tell what a module utility does from its name and/or its location. Generic utilities (shared code used by many different kinds of modules) live in the main ansible/ansible codebase, in the common subdirectory or in the root directory of lib/ansible/module_utils. Utilities used by a particular set of modules generally live in the same collection as those modules. For example:

lib/ansible/module_utils/urls.py contains shared code for parsing URLs

openstack.cloud.plugins.module_utils.openstack.py contains utilities for modules that work with OpenStack instances

ansible.netcommon.plugins.module_utils.network.common.config.py contains utility functions for use by networking modules

Following this pattern with your own module utilities makes everything easy to find and use.

Ansible ships with an extensive library of module_utils files. You can find the module utility source code in the lib/ansible/module_utils directory under your main Ansible path. We describe the most widely used utilities below. For more details on any specific module utility, please see the source code for module_utils.

LICENSING REQUIREMENTS Ansible enforces the following licensing requirements:

A file in module_utils used only for a specific vendor’s hardware, provider, or service may be licensed under GPLv3+. Adding a new file under module_utils with GPLv3+ needs to be approved by the core team.

All other module_utils must be licensed under BSD, so GPL-licensed third-party and Galaxy modules can use them.

If there’s doubt about the appropriate license for a file in module_utils, the Ansible Core Team will decide during an Ansible Core Community Meeting.

All other files shipped with Ansible, including all modules, must be licensed under the GPL license (GPLv3 or later).

Existing license requirements still apply to content in ansible/ansible (ansible-core).

Content that was previously in ansible/ansible or a collection and has moved to a new collection must retain the license it had in its prior repository.

Copyright entries by previous committers must also be kept in any moved files.

api.py - Supports generic API modules

basic.py - General definitions and helper utilities for Ansible modules

common/dict_transformations.py - Helper functions for dictionary transformations

common/file.py - Helper functions for working with files

common/text/ - Helper functions for converting and formatting text

common/parameters.py - Helper functions for dealing with module parameters

common/sys_info.py - Functions for getting distribution and platform information

common/validation.py - Helper functions for validating module parameters against a module argument spec

facts/ - Directory of utilities for modules that return facts. See PR 23012 for more information

json_utils.py - Utilities for filtering unrelated output around module JSON output, like leading and trailing lines

powershell/ - Directory of definitions and helper functions for Windows PowerShell modules

pycompat24.py - Exception workaround for Python 2.4

service.py - Utilities to enable modules to work with Linux services (placeholder, not in use)

six/__init__.py - Bundled copy of the Six Python library to aid in writing code compatible with both Python 2 and Python 3

splitter.py - String splitting and manipulation utilities for working with Jinja2 templates

urls.py - Utilities for working with http and https requests

Several commonly-used utilities migrated to collections in Ansible 2.10, including:

ismount.py migrated to ansible.posix.plugins.module_utils.mount.py - Single helper function that fixes os.path.ismount

known_hosts.py migrated to community.general.plugins.module_utils.known_hosts.py - utilities for working with known_hosts file

For a list of migrated content with destination collections, see the runtime.yml file.

**Examples:**

Example 1 (python):
```python
from ansible.module_utils.basic import AnsibleModule
```

Example 2 (python):
```python
from ansible.module_utils.my_shared_code import MySharedCodeClient
```

---

## Testing Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing.html

**Contents:**
- Testing Ansible
- Why test your Ansible contributions?
- Types of tests
- Testing within GitHub & Azure Pipelines
  - Organization
  - Rerunning a failing CI job
- How to test a PR
  - Setup: Installing Pytest and required Pytest libraries
  - Setup: Checking out a Pull Request
  - Testing the Pull Request

Why test your Ansible contributions?

Testing within GitHub & Azure Pipelines

Rerunning a failing CI job

Setup: Installing Pytest and required Pytest libraries

Setup: Checking out a Pull Request

Testing the Pull Request

Run integration tests

Want to know more about testing?

If you’re a developer, one of the most valuable things you can do is to look at GitHub issues and help fix bugs, since bug-fixing is almost always prioritized over feature development. Even for non-developers, helping to test pull requests for bug fixes and features is still immensely valuable.

Ansible users who understand how to write playbooks and roles should be able to test their work. GitHub pull requests will automatically run a variety of tests (for example, Azure Pipelines) that show bugs in action. However, contributors must also test their work outside of the automated GitHub checks and show evidence of these tests in the pull request to ensure that their work will be more likely to be reviewed and merged.

Read on to learn how Ansible is tested, how to test your contributions locally, and how to extend testing capabilities.

If you want to learn about testing collections, read Testing collections

At a high level, we have the following classifications of tests:

Sanity tests are made up of scripts and tools used to perform static code analysis.

The primary purpose of these tests is to enforce Ansible coding standards and requirements.

Functional tests of modules and Ansible Core functionality.

Tests directly against individual parts of the code base.

When Pull Requests (PRs) are created they are tested using Azure Pipelines, a Continuous Integration (CI) tool. Results are shown at the end of every PR.

When Azure Pipelines detects an error and it can be linked back to a file that has been modified in the PR then the relevant lines will be added as a GitHub comment. For example:

From the above example we can see that --test pep8 and --test validate-modules have identified an issue. The commands given allow you to run the same tests locally to ensure you’ve fixed all issues without having to push your changes to GitHub and wait for Azure Pipelines, for example:

If you haven’t already got Ansible available, use the local checkout by running:

Then run the tests detailed in the GitHub comment:

If there isn’t a GitHub comment stating what’s failed you can inspect the results by clicking on the “Details” button under the “checks have failed” message at the end of the PR.

Occasionally you may find your PR fails due to a reason unrelated to your change. This could happen for several reasons, including:

a temporary issue accessing an external resource, such as a yum or Git repo

a timeout creating a virtual machine to run the tests on

If either issue appears to be the case, you can rerun the Azure Pipelines test by:

adding a comment with /rebuild (full rebuild) or /rebuild_failed (rebuild only failed CI nodes) to the pull request

closing and re-opening the pull request (full rebuild)

making another change to the branch and pushing to GitHub

If the issue persists, please contact the community. Visit the Ansible communication guide for details.

Ideally, the code should add tests that prove that the code works. That’s not always possible and tests are not always comprehensive, especially when a user doesn’t have access to a wide variety of platforms, or is using an API or web service. In these cases, live testing against real equipment can be more valuable than automation that runs against simulated interfaces. In any case, things should always be tested manually the first time as well.

Thankfully, helping to test Ansible is pretty straightforward, assuming you are familiar with how Ansible works.

Ansible’s unit testing framework leverages the pytest library. Before diving into testing, ensure you have pytest installed alongside any additional pytest libraries such as pytest-mock and pytest-xdist.

Refer to the documentation for more information: Unit Tests.

fetching the proposed changes into a test branch

commenting on that particular issue on GitHub

Testing source code from GitHub pull requests sent to us does have some inherent risk, as the source code sent may have mistakes or malicious code that could have a negative impact on your system. We recommend doing all testing on a virtual machine, whether a cloud instance, or locally. Some users like Vagrant or Docker for this, but they are optional. It is also useful to have virtual machines of different Linux or other flavors, since some features (for example, package managers such as apt or yum) are specific to those OS versions.

Create a fresh area to work:

Next, find the pull request you’d like to test and make a note of its number. It will look something like this:

Only test ansible:devel

It is important that the PR request target be ansible:devel, as we do not accept pull requests into any other branch. Dot releases are cherry-picked manually by Ansible staff.

Use the pull request number when you fetch the proposed changes and create your branch for testing:

The first command fetches the proposed changes from the pull request and creates a new branch named testing_PRXXXX, where the XXXX is the actual number associated with the pull request (for example, 65381). The second command checks out the newly created branch.

If the GitHub user interface shows that the pull request will not merge cleanly, we do not recommend proceeding if you are not somewhat familiar with Git and coding, as you will have to resolve a merge conflict. This is the responsibility of the original pull request contributor.

Some users do not create feature branches, which can cause problems when they have multiple, unrelated commits in their version of devel. If the source looks like someuser:devel, make sure there is only one commit listed on the pull request.

The Ansible source includes a script that allows you to use Ansible directly from source without requiring a full installation that is frequently used by developers on Ansible.

Simply source it (to use the Linux/Unix terminology) to begin using it immediately:

This script modifies the PYTHONPATH environment variables (along with a few other things), which will be temporarily set as long as your shell session is open.

At this point, you should be ready to begin testing!

Some ideas of what to test are:

Create a test Playbook with the examples in and check if they function correctly

Test to see if any Python backtraces returned (that’s a bug)

Test on different operating systems, or against different library versions

More information: Sanity Tests

More information: Unit Tests

More information: Integration tests

Any potential issues should be added as comments on the pull request (and it is acceptable to comment if the feature works as well), remembering to include the output of ansible --version

If the PR does not resolve the issue, or if you see any failures from the unit/integration tests, just include that output instead:

The online code coverage reports is a good way to identify areas for testing improvement in Ansible. By following red colors you can drill down through the reports to find files that have no tests at all. Adding both integration and unit tests that show clearly how code should work, verify important Ansible functions and increases testing coverage in areas where there is none is a valuable way to help improve Ansible.

The code coverage reports only cover the devel branch of Ansible where new feature development takes place. Pull requests and new code will be missing from the codecov.io coverage reports so local reporting is needed. Most ansible-test commands allow you to collect code coverage, this is particularly useful to indicate where to extend testing. See Testing Ansible and Collections for more information.

If you’d like to know more about the plans for improving testing Ansible then why not join the Ansible community forum.

**Examples:**

Example 1 (unknown):
```unknown
The test `ansible-test sanity --test pep8` failed with the following errors:

lib/ansible/modules/network/foo/bar.py:509:17: E265 block comment should start with '# '

The test `ansible-test sanity --test validate-modules` failed with the following error:
lib/ansible/modules/network/foo/bar.py:0:0: E307 version_added should be 2.4. Currently 2.3
```

Example 2 (unknown):
```unknown
source hacking/env-setup
```

Example 3 (unknown):
```unknown
ansible-test sanity --test pep8
ansible-test sanity --test validate-modules
```

Example 4 (unknown):
```unknown
git clone https://github.com/ansible/ansible.git ansible-pr-testing
cd ansible-pr-testing
```

---

## Testing plugin documentation — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_documentation.html

**Contents:**
- Testing plugin documentation

A quick test while developing is to use ansible-doc -t <plugin_type> <name> to see if it renders, you might need to add -M /path/to/module if the module is not somewhere Ansible expects to find it.

Before you submit a plugin for inclusion in ansible-core, you must run tests to ensure that the argspec matches the documentation in your Python file, and that the argspec’s and documentation’s structure is correct.

The community pages offer more information on testing reStructuredText documentation if you extend the Ansible documentation with additional RST files.

To ensure that your module documentation matches your argument_spec:

Install required Python packages (drop ‘–user’ in venv/virtualenv):

run the validate-modules test:

If you have Docker or Podman installed, you can also use them with the --docker option, which uses an image that already has all requirements installed:

For other plugin types the steps are similar, just adjusting names and paths to the specific type.

**Examples:**

Example 1 (unknown):
```unknown
pip install --user -r test/lib/ansible_test/_data/requirements/sanity.txt
```

Example 2 (unknown):
```unknown
ansible-test sanity --test validate-modules mymodule
```

Example 3 (unknown):
```unknown
ansible-test sanity --docker --test validate-modules mymodule
```

---

## Sanity Tests — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/dev_guide/testing_sanity.html

**Contents:**
- Sanity Tests
- Set up your environment
- How to run
- Available Tests

Set up your environment

Sanity tests are made up of scripts and tools used to perform static code analysis. The primary purpose of these tests is to enforce Ansible coding standards and requirements.

Tests are run with ansible-test sanity. All available tests are run unless the --test option is used.

Install ansible-core that provides the ansible-test tool.

If you want to run checks available in the development version of ansible-core, install it from source code.

Run source hacking/env-setup from its source code directory in the same terminal session you run your tests.

Install podman or docker to avoid installing all the dependencies on your system.

If you test files in a collection:

Ensure you have your collection installed in the following path in your home directory: ~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>. For instance, in case of the community.general collection, it will be ~/ansible_collections/community/general

If your collection is hosted on a remote server such as GitHub, clone it to that path as follows: git clone <COLLECTION_REPO_URL> ~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>

To run sanity tests using podman or docker, always use the default docker image by passing the --docker argument without specifying the image name.

When testing files in a collection, change your location to your collection directory you created while setting up your environment:

To run all sanity tests in a container:

To run a specific test, add the --test <NAME> argument, for example, --test validate-modules.

To list available tests, run: ansible-test sanity --list-tests

To include disabled tests, add the --allow-disabled argument.

See the full list of sanity tests, which also details how to fix identified issues.

**Examples:**

Example 1 (unknown):
```unknown
cd ~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>
```

Example 2 (unknown):
```unknown
ansible-test sanity --docker
```

---
