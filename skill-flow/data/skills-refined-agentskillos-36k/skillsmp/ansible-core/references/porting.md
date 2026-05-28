# Ansible-Core - Porting

**Pages:** 1

---

## Reporting bugs and requesting features — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/reporting_bugs_and_features.html

**Contents:**
- Reporting bugs and requesting features
- Reporting a bug
  - Security bugs
  - Bugs in ansible-core
  - How to write a good bug report
- Requesting a feature

How to write a good bug report

Ansible practices responsible disclosure. To report security-related bugs, send an email to security@ansible.com for an immediate response. Do not submit a ticket or post to any public groups.

Before reporting a bug, search in GitHub for already reported issues and open pull requests to see if someone has already addressed your issue. Unsure if you found a bug? Discuss the behavior with the community on the Ansible Forum.

Also, use the Ansible Forum to discuss whether the problem is in ansible-core or a collection, and for “how do I do this” type questions.

You need a free GitHub account to report bugs that affect:

a plugin that remained in the ansible/ansible repo

the overall functioning of Ansible

If you find a bug, open an issue using the issue template.

Fill out the issue template as completely and as accurately as possible. Include:

the expected behavior and what you’ve tried, including the exact commands you were using or tasks you are running.

the current behavior and why you think it is a bug

the steps to reproduce the bug

a minimal reproducible example and comments describing examples

any relevant configurations and the components you used

any relevant output plus ansible -vvvv (debugging) output

add the output of ansible-test-env --show when filing bug reports involving ansible-test.

When sharing YAML in playbooks, ensure that you preserve formatting using code blocks. For multiple-file content, use gist.github.com, more durable than Pastebin content.

Before you request a feature, check what is planned for future Ansible Releases. Check existing pull requests tagged with feature.

To get your feature into Ansible, submit a pull request, either against ansible-core or a collection. See also Requirements to merge your PR. For ansible-core, you can also open an issue in ansible/ansible or in a corresponding collection repository (To find the correct issue tracker, refer to Bugs in collections ).

---
