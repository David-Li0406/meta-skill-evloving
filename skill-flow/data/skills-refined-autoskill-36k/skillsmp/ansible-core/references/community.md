# Ansible-Core - Community

**Pages:** 12

---

## Ansible Ecosystem Project Development Resources — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/ecosystem_project_resources.html

**Contents:**
- Ansible Ecosystem Project Development Resources
- Onboarding toolkit
- Project template
- List of community-curated projects

This document lists resources to help contributors interested in developing a community project in the Ansible ecosystem.

Any improvements to the resources listed in this document or to the document itself are very welcome! Please submit an issue or pull request in the corresponding GitHub repository.

The Ansible Onboarding toolkit provides guidelines on setting up GitHub repositories for new projects as well as the type of documentation your project should include.

Despite being originally developed for Ansible ecosystem projects under the ansible-community GitHub organization, everyone is welcome to use the onboarding toolkit.

The Ansible project-template is a GitHub repository template for Ansible ecosystem projects that contains:

Files normally present in every repository such as README, license, code of conduct, and so on.

A docsite template that you are encouraged to use with your project to provide a consistent experience across the Ansible project ecosystem.

Please take a look at the docsite built from the project-template to see it in action.

You are welcome to take the template, fill in your project-specific information, build it using Sphinx, and then publish it.

Even if your project is not new and already has documentation, we recommend you take a look at the template and check if there is anything missed in documentation for your project users, contributors, and maintainers.

Whether your project repository is under the ansible-community GitHub organization or under your own one, you are welcome to include your project in the Awesome Ansible list.

Before letting the community know about your shiny project by adding it to the list, make sure it satisfies the standards explained in the Onboarding toolkit to provide the best user and contributor experience.

---

## Advanced Contributor Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/advanced_index.html

**Contents:**
- Advanced Contributor Guide

This guide focuses on contributors who are committers, GitHub admins, release managers, or Ansible ecosystem project developers.

---

## ansible-core Contributors Guide — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/contributions.html

**Contents:**
- ansible-core Contributors Guide
- Working with the Ansible repo

If you have a specific Ansible interest or expertise (for example, VMware, Linode, and so on), consider joining a working group.

I want to make my first code changes to a collection or to ansible-core. How do I set up my Python development environment?

I would like to get more efficient as a developer. How can I find editors, linters, and other tools that will support my Ansible development efforts?

I want my code to meet Ansible’s guidelines. Where can I find guidance on coding in Ansible?

I would like to connect Ansible to a new API or other resource. How do I create a collection?

My pull request is marked needs_rebase. How do I rebase my PR?

I am using an older version of Ansible and want a bug fixed in my version that has already been fixed on the devel branch. How do I backport a bugfix PR?

I have an open pull request with a failing test. How do I learn about Ansible’s testing (CI) process?

I am ready to step up as a collection maintainer. What are the guidelines for maintainers?

A module in a collection I maintain is obsolete. How do I deprecate a module?

---

## Contributor path — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/contributor_path.html

**Contents:**
- Contributor path
- Determine your area of interest
- Find the corresponding project
- Learn
  - Specific knowledge for code developers
- Making your first contribution
- Continue to contribute
- Teach others
- Become a collection maintainer
- Become a steering committee member

This section describes the contributor’s journey from the beginning to becoming a leader who helps shape the future of Ansible. You can use this path as a roadmap for your long-term participation.

Any contribution to the project, even a small one, is very welcome and valuable. Any contribution counts, whether it is feedback on an issue, a pull request, a topic or documentation change, or a coding contribution. When you contribute regularly, your proficiency and judgment in the related area increase and, along with this, the importance of your presence in the project.

Determine your area of interest

Find the corresponding project

Specific knowledge for code developers

Making your first contribution

Continue to contribute

Become a collection maintainer

Become a steering committee member

First, determine areas that are interesting to you. Consider your current experience and what you’d like to gain. For example, if you use a specific collection, have a look there. See How can I help? for more ideas on how to help.

These are multiple community projects in the Ansible ecosystem you could contribute to:

The required skillset depends on the area of interest and the project you’ll be working on. Remember that the best way to learn is by doing.

Code development requires the most technical knowledge. Let’s sort out what an Ansible developer should learn.

You should understand at least the basics of the following tools:

Python programming language

GitHub collaborative development model through forks and pull requests

You can learn these tools more in-depth when working on your first contributions.

Each Ansible project has its own set of contributor guidelines. Familiarize yourself with these as you prepare your first contributions.

Ansible Core development.

Ansible collection development and the collection-level contributor guidelines in the collection repository.

You can find some ideas on how you can contribute in How can I help?.

If you are interested in contributing to collections, take a look at collection contributions and the collection repository’s README and CONTRIBUTING files. To make your first experience as smooth as possible, read the repository documentation carefully, then ask the repository maintainers for guidance if you have any questions.

Take a look at GitHub issues labeled with the easyfix and good_first_issue labels for:

Ansible collections repositories

All other Ansible projects

Issues labeled with the docs label in Ansible collections and other Ansible projects can be also good to start with.

When you choose an issue to work on, add a comment directly on the GitHub issue to say you are looking at it and let others know to avoid conflicting work. You can also ask for help in a comment if you need it.

We don’t expect everybody to know everything. Start small, think big. When you contribute regularly, your proficiency and judgment in the related area will improve quickly and, along with this, the importance of your presence in the project.

See Communicating with the Ansible community for ways to communicate and engage with the Ansible community, including working group meetings, accessing the Bullhorn news bulletin, and upcoming contributor summits.

Share your experience with other contributors through improving documentation, answering questions from other contributors and users on Matrix/Libera.Chat IRC, giving advice on issues and pull requests, and discussing topics on the Forum.

If you are a code contributor to a collection, you can get extended permissions in the repository and become a maintainer. A collection maintainer is a contributor trusted by the community who makes significant and regular contributions to the project and showed themselves as a specialist in the related area. See Module Maintainer Guidelines for details.

For some collections that use the collection bot, such as community.general and community.network, you can have different levels of access and permissions:

File-level permissions: the stage prior to becoming a collection maintainer. The file is usually a module or plugin. File maintainers have indirect commit rights.

Supershipit permissions: similar to being a file maintainer but the scope where a maintainer has the indirect commit is the whole repository.

Triage access to the repository: allows contributors to manage issues and pull requests.

Write access to the repository also known as commit: allows contributors to merge pull requests to the development branch as well as perform all the other activities listed in the Module Maintainer Guidelines.

For information about permission levels, see the GitHub official documentation.

You do NOT have to be a programmer to become a steering committee member.

The Steering Committee member status reflects the highest level of trust and allows contributors to lead the project by making important decisions for the Ansible project. The Committee members are community leaders who shape the project’s future and the future of automation in the IT world in general.

To reach the status, as the current Committee members did before getting it, along with the things mentioned in this document, you should:

Subscribe to, comment on, and vote on the community topics<creating_community_topic>.

If time permits, join the Community meetings. Note this is NOT a requirement.

---

## Committers Guidelines — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/committer_guidelines.html

**Contents:**
- Committers Guidelines
- Features, high-level design, and roadmap of ansible-core
- Features, high-level design, and roadmap of Ansible collections
- Our workflow on GitHub
  - Addendum to workflow for committers:
- Roles on Core
- General rules

These are the guidelines for people with commit privileges on the repositories in the ansible and ansible-collections GitHub organizations.

Committers of Ansible-core are necessarily Red Hat employees acting as members of the Ansible Core team. Committers of Ansible collections are members of the community or Ansible Engineering. Please read the guidelines before you commit.

These guidelines apply to everyone. At the same time, this is NOT a process document. So just use good judgment. You have been given commit access because we trust your judgment.

That said, use the trust wisely.

If you abuse the trust and break components and builds, and so on, the trust level falls and you may be asked not to commit or you may lose your commit privileges.

As a core team member, you are an integral part of the team that develops the roadmap. Please be engaged, and push for the features and fixes that you want to see. Also keep in mind that Red Hat, as a company, will commit to certain features, fixes, APIs, and so on, for various releases. Red Hat, the company, and the Ansible team must get these changes completed and released as scheduled. Obligations to users, the community, and customers must come first. Because of these commitments, a feature you want to develop yourself may not get into a release if it affects a lot of other parts within Ansible.

Any other new features and changes to high level design should go through the proposal process (TBD), to ensure the community and core team have had a chance to review the idea and approve it. The core team has sole responsibility for merging new features based on proposals to Ansible-core.

Collections maintainers define features, high-level design, and roadmap of the collections themselves and are responsible for merging new features to Ansible collections based on proposals discussed with their communities.

As a committer, you may already know this, but our workflow forms a lot of our team policies. Please ensure you are aware of the following workflow steps:

Fork the repository upon which you want to do some work to your own personal repository

Work on the specific branch upon which you need to commit

Create a pull request back to the upstream repository and tag the people you would like to review; assign someone as the primary “owner” of your pull request

Adjust code as necessary based on the comments provided

Ask someone from the repository committers to do a final review and merge

The Core Team is aware that this can be a difficult process at times. Sometimes, the team breaks the rules by making direct commits or merging their own pull requests. This section is a set of guidelines. If you are changing a comma in documentation, or making a very minor change, you can use your best judgment. This is another trust thing. The process is critical for any major change, but for little things or getting something done quickly, use your best judgment and make sure people on the team are aware of your work.

Core committers: Fine to do pull requests for most things, but we should have a timebox. Hanging pull requests may merge on the judgment of these developers.

Module maintainers: Module maintainers own specific modules and have indirect commit access through the current module pull request mechanisms.

Collection maintainers: Collection maintainers own specific collections and have commit access to them. Each collection can set its own rules for contributions.

Individuals with direct commit access are entrusted with powers that allow them to do a broad variety of things–probably more than we can write down. Rather than rules, treat these as general guidelines, individuals with this power are expected to use their best judgment.

Merge your own pull requests. Someone else should have a chance to review and approve the pull request merge. If you are a Core Committer, you have a small amount of leeway here for very minor changes.

Forget about alternate environments. Consider the alternatives–yes, people have bad environments, but they are the ones who need us the most.

Drag your community team members down. Discuss the technical merits of any pull requests you review. Avoid negativity and personal comments. For more guidance on being a good community member, read our Community Code of Conduct.

Forget about the maintenance burden. High-maintenance features may not be worth adding.

Break playbooks. Always keep backwards compatibility in mind.

Forget to keep it simple. Complexity breeds all kinds of problems.

Squash, avoid merges whenever possible, use GitHub’s squash commits or cherry pick if needed (bisect thanks you).

Be active. Committers who have no activity on the project (through merges, triage, commits, and so on) will have their permissions suspended.

Consider backwards compatibility (goes back to “do not break existing playbooks”).

Write tests and be sure that other’s pull requests you are reviewing are covered well. Pull requests with tests are looked at with more priority than pull requests without tests that should have them included. While not all changes require tests, be sure to add them for new features, bug fixes, and functionality changes.

Discuss with other committers, specially when you are unsure of something.

Document! If your pull request is a new feature or a change to behavior, make sure you have updated all associated documentation or have notified the right people to do so. It also helps to add the version of ansible-core or collection against which this documentation is compatible (to avoid confusion between stable and devel docs, for backwards compatibility, and so on).

Consider scope, sometimes a fix can be generalized.

Keep it simple, then things are maintainable, debuggable, and intelligible.

Committers are expected to continue to follow the same community and contribution guidelines followed by the rest of the Ansible community.

---

## How can I help? — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/how_can_I_help.html

**Contents:**
- How can I help?
- Become a power user
- Ask and answer questions online
- Review, fix, and maintain the documentation
- Participate in your local meetup
- File and verify issues
- Review and submit pull requests
- Become a collection maintainer
- Join a working group
- Teach Ansible to others

Ask and answer questions online

Review, fix, and maintain the documentation

Participate in your local meetup

File and verify issues

Review and submit pull requests

Become a collection maintainer

Teach Ansible to others

Thanks for being interested in helping the Ansible project!

There are many ways to help the Ansible project…but first, please read and understand the Community Code of Conduct.

A great way to help the Ansible project is to become a power user:

Use Ansible everywhere you can

Take tutorials and classes

Read the official documentation

Study some of the many excellent books about Ansible

When you become a power user, your ability and opportunities to help the Ansible project in other ways will multiply quickly.

There are many online platforms where Ansible users and contributors ask and answer questions including the Forum. Reach out and communicate with your fellow Ansible enthusiasts.

You can find the official Ansible communication channels.

Typos are everywhere, even in the Ansible documentation. We work hard to keep the documentation up-to-date, but you may also find outdated examples. We offer easy ways to report and/or fix documentation errors.

There are Ansible meetups all over the world. Join your local meetup. Attend regularly. Ask good questions. Volunteer to give a presentation about how you use Ansible.

If there is no meetup near you, we are happy to help you start one.

All software has bugs, and Ansible is no exception. When you find a bug, you can help tremendously by telling us about it:

Filing issues for ansible-core.

Filing issues for collections.

If the bug you found already exists in an issue, you can help by verifying the behavior of the reported bug with a comment in that issue, or by reporting any additional information.

As you become more familiar with how Ansible works, you may be able to fix issues or develop new features yourself. If you think you have a fix for a bug in Ansible, or if you have a new feature that you would like to share with millions of Ansible users, read all about the development process to learn how to get your code accepted into Ansible.

You can also get started with solving GitHub issues labeled with the easyfix and good_first_issue labels for:

All other Ansible projects

When you choose an issue to work on, add a comment directly on the GitHub issue to say you are looking at it and let others know to avoid conflicting work. You can also ask for help in a comment if you need it.

For collections, refer to the Creating your first collection pull request page to learn how to quickly set up your local environment, test your changes, and submit a ready-for-review pull request.

Another good way to help is to review pull requests that other Ansible users have submitted. Ansible Core keeps a full list of open pull requests by file, so if a particular module or plugin interests you, you can easily keep track of all the relevant new pull requests and provide testing or feedback. Alternatively, you can review the pull requests for any collections that interest you. Click Issue tracker on the collection documentation page to find the issues and PRs for that collection.

Once you have learned about the development process and have contributed code to a collection, we encourage you to become a maintainer of that collection. There are hundreds of modules in dozens of Ansible collections, and the vast majority of them are written and maintained entirely by members of the Ansible community.

See collection maintainer guidelines to learn more about the responsibilities of being an Ansible collection maintainer.

Working groups are a way for Ansible community members to self-organize around particular topics of interest. We have working groups around various topics. To join or create a working group, please read the Ansible Working Groups.

We are working on a standardized Ansible workshop that can provide a good hands-on introduction to Ansible usage and concepts.

If you like Ansible and just want to spread the good word, feel free to share on your social media platform of choice, and let us know by using @ansible or #ansible. We’ll be looking for you.

---

## Contributing to the Ansible Documentation — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/documentation_contributions.html

**Contents:**
- Contributing to the Ansible Documentation
- Editing docs directly on GitHub
- Reviewing or solving open issues
- Reviewing open PRs
- Opening a new issue and/or PR
- Verifying your documentation PR
  - Setting up your environment to build documentation locally
  - Testing the documentation locally
  - Building the documentation locally
    - Periodically cloning Ansible Core

Ansible has a lot of documentation and a small team of writers. Community support helps us keep up with new features, fixes, and changes.

Improving the documentation is an easy way to make your first contribution to the Ansible project. You do not have to be a programmer, since most of our documentation is written in YAML (module documentation) or reStructuredText (rST). Some collection-level documentation is written in a subset of Markdown. If you are using Ansible, you already use YAML in your playbooks. rST and Markdown are mostly just text. You do not even need Git experience, if you use the Edit on GitHub option.

If you find a typo, a broken example, a missing topic, or any other error or omission on this documentation website, let us know. Here are some ways to support Ansible documentation:

Editing docs directly on GitHub

Reviewing or solving open issues

Opening a new issue and/or PR

Verifying your documentation PR

Setting up your environment to build documentation locally

Testing the documentation locally

Building the documentation locally

Periodically cloning Ansible Core

Building a single rST page

Building all the rST pages

Building module docs and rST pages

Building rST files with sphinx-build

Running the final tests

Joining the documentation working group

For typos and other quick fixes, you can edit most of the documentation right from the site. Look at the top right corner of this page. That Edit on GitHub link is available on all the guide pages in the documentation. If you have a GitHub account, you can submit a quick and easy pull request this way.

The source files for individual collection plugins exist in their respective repositories. Follow the link to the collection on Galaxy to find where the repository is located and any guidelines on how to contribute to that collection.

To submit a documentation PR from docs.ansible.com with Edit on GitHub:

Click on Edit on GitHub.

If you don’t already have a fork of the ansible repo on your GitHub account, you’ll be prompted to create one.

Fix the typo, update the example, or make whatever other change you have in mind.

Enter a commit message in the first rectangle under the heading Propose file change at the bottom of the GitHub page. The more specific, the better. For example, “fixes typo in my_module description”. You can put more detail in the second rectangle if you like. Leave the +label: docsite_pr there.

Submit the suggested change by clicking on the green “Propose file change” button. GitHub will handle branching and committing for you, and open a page with the heading “Comparing Changes”.

Click on Create pull request to open the PR template.

Fill out the PR template, including as much detail as appropriate for your change. You can change the title of your PR if you like (by default it is the same as your commit message). In the Issue Type section, delete all lines except the Docs Pull Request line.

Submit your change by clicking on Create pull request button.

Be patient while Ansibot, our automated script, adds labels, pings the docs maintainers, and kicks off a CI testing run.

Keep an eye on your PR - the docs team may ask you for changes.

Review or solve open documentation issues for:

Review open documentation pull requests for:

Ansible documentation

To add a helpful review, please:

Test the change if applicable.

Think if it can be made better (including wording, structure, fixing typos and so on).

Suggest improvements.

Approve the change with the looks good to me comment.

If the problem you have noticed is too complex to fix with the Edit on GitHub option, and no open issue or PR already documents the problem, please open an issue and/or a PR on the correct underlying repo - ansible/ansible-documentation for most pages that are not plugin or module documentation. If the documentation page has no Edit on GitHub option, check if the page is for a module within a collection. If so, follow the link to the collection on Galaxy and select the repo button in the upper right corner to find the source repository for that collection and module. The Collection README file should contain information on how to contribute to that collection, or report issues.

A great documentation GitHub issue or PR includes:

a detailed description of the problem (even for a PR - it is hard to evaluate a suggested change unless we know what problem it is meant to solve)

links to other information (related issues/PRs, external documentation, pages on docs.ansible.com, and so on)

If you make multiple changes to the Ansible documentation, or add more than a line to it, before you open a pull request, please:

Check that your text follows our Ansible documentation style guide.

Test your changes for rST errors.

Build the page, and preferably the entire documentation site, locally.

The following sections apply to documentation sourced from the ansible/ansible-documentation repo and does not apply to documentation from an individual collection. See the collection README file for details on how to contribute to that collection. Collection developers can also lint their collection-level documentation. See Verifying your collection documentation for details.

To build documentation locally, ensure you have a working development environment.

To work with documentation on your local machine, you should use a version of Python that meets the minimum requirement for ansible-core. For more information on minimum Python versions, see the support matrix.

Set up a virtual environment in which to install dependencies.

Clone required parts of Ansible Core for the docs build.

Install either the unpinned or tested documentation dependencies.

After checking out ansible/ansible-documentation, make sure the docs/docsite/rst directory has strict enough permissions. It should only be writable by the owner’s account. If your default umask is not 022, you can use chmod go-w docs/docsite/rst to set the permissions correctly in your new branch. Optionally, you can set your umask to 022 to make all newly created files on your system (including those created by git clone) have the correct permissions.

To test an individual file for rST errors:

Building the documentation is the best way to check for errors and review your changes. Once rstcheck runs with no errors, navigate to ansible-documentation/docs/docsite and then build the page(s) you want to review.

If building on macOS with Python 3.8 or later, you must use Sphinx >= 2.2.2. See #6803 for details.

Documentation in the ansible/ansible-documentation repository builds “on top of” the ansible/ansible repository. When you set up your local build environment, you clone the relevant parts Ansible Core.

To ensure that you use the latest source from Ansible Core, you should periodically run the following script before you build documentation:

To build a single rST file with the make utility:

This process compiles all the links but provides minimal log output. If you’re writing a new page or want more detailed log output, refer to the instructions on Building rST files with sphinx-build

make htmlsingle adds rst/ to the beginning of the path you provide in rst=, so you can’t type the file name with autocomplete. Here are the error messages you will see if you get this wrong:

If you run make htmlsingle from the docs/docsite/rst/ directory: make: *** No rule to make target `htmlsingle'. Stop.

If you run make htmlsingle from the docs/docsite/ directory with the full path to your rST document: sphinx-build: error: cannot find files ['rst/rst/community/documentation_contributions.rst'].

To build all the rST files with almost no module documentation:

This is building effectively the ansible-core documentation, as opposed to the Ansible community package documentation, which includes documentation for many collections.

To build all the module documentation for the Ansible community package plus all the rST files:

Advanced users can build one or more rST files with the sphinx utility directly. sphinx-build returns misleading undefined label warnings if you only build a single page, because it does not create internal links. However, sphinx-build returns more extensive syntax feedback, including warnings about indentation errors and x-string without end-string warnings. This can be useful, especially if you’re creating a new page from scratch. To build a page or pages with sphinx-build:

You can specify file names, or -a for all files, or omit both to compile only new/changed files.

When you submit a documentation pull request, automated tests are run. Those same tests can be run locally. To do so, navigate to the repository’s top directory and run:

It is recommended to run tests on a clean copy of the repository, which is the purpose of the make clean command.

The Documentation Working Group (DaWGs) meets weekly on Tuesdays in the docs:ansible.im chat room on Matrix. For more information, including links to our agenda, visit our forum group.

More about testing module documentation

More about documenting modules

**Examples:**

Example 1 (unknown):
```unknown
python3 -m venv ./venv
source ./venv/bin/activate
```

Example 2 (unknown):
```unknown
python3 docs/bin/clone-core.py
```

Example 3 (unknown):
```unknown
pip install -r tests/requirements.in -c tests/requirements.txt # Installs tested dependency versions.
pip install -r tests/requirements.in # Installs the unpinned dependency versions.
```

Example 4 (unknown):
```unknown
rstcheck changed_file.rst
```

---

## Community Code of Conduct — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/code_of_conduct.html

**Contents:**
- Community Code of Conduct
- Anti-harassment policy
- Policy violations

Community Code of Conduct

Anti-harassment policy

Every community can be strengthened by a diverse variety of viewpoints, insights, opinions, skillsets, and skill levels. However, with diversity comes the potential for disagreement and miscommunication. The purpose of this Code of Conduct is to ensure that disagreements and differences of opinion are conducted respectfully and on their own merits, without personal attacks or other behavior that might create an unsafe or unwelcoming environment.

These policies are not designed to be a comprehensive set of Things You Cannot Do. We ask that you treat your fellow community members with respect and courtesy, and in general, Don’t Be A Jerk. This Code of Conduct is meant to be followed in spirit as much as in letter and is not exhaustive.

All Ansible events and participants therein are governed by this Code of Conduct and anti-harassment policy. We expect organizers to enforce these guidelines throughout all events, and we expect attendees, speakers, sponsors, and volunteers to help ensure a safe environment for our whole community. Specifically, this Code of Conduct covers participation in all Ansible-related forums and mailing lists, code and documentation contributions, public chat (Matrix, IRC), private correspondence, and public meetings.

Ansible community members are…

Contributions of every kind have far-ranging consequences. Just as your work depends on the work of others, decisions you make surrounding your contributions to the Ansible community will affect your fellow community members. You are strongly encouraged to take those consequences into account while making decisions.

Asynchronous communication can come with its own frustrations, even in the most responsive of communities. Please remember that our community is largely built on volunteered time, and that questions, contributions, and requests for support may take some time to receive a response. Repeated “bumps” or “reminders” in rapid succession are not good displays of patience. Additionally, it is considered poor manners to ping a specific person with general questions. Pose your question to the community as a whole, and wait patiently for a response.

Every community inevitably has disagreements, but remember that it is possible to disagree respectfully and courteously. Disagreements are never an excuse for rudeness, hostility, threatening behavior, abuse (verbal or physical), or personal attacks.

Everyone should feel welcome in the Ansible community, regardless of their background. Please be courteous, respectful and polite to fellow community members. Do not make or post offensive comments related to skill level, gender, gender identity or expression, sexual orientation, disability, physical appearance, body size, race, or religion. Sexualized images or imagery, real or implied violence, intimidation, oppression, stalking, sustained disruption of activities, publishing the personal information of others without explicit permission to do so, unwanted physical contact, and unwelcome sexual attention are all strictly prohibited. Additionally, you are encouraged not to make assumptions about the background or identity of your fellow community members.

The only stupid question is the one that does not get asked. We encourage our users to ask early and ask often. Rather than asking whether you can ask a question (the answer is always yes!), instead, simply ask your question. You are encouraged to provide as many specifics as possible. Code snippets in the form of Gists or other paste site links are almost always needed in order to get the most helpful answers. Refrain from pasting multiple lines of code directly into the chat channels - instead use gist.github.com or another paste site to provide code snippets.

The Ansible community is committed to being a welcoming environment for all users, regardless of skill level. We were all beginners once upon a time, and our community cannot grow without an environment where new users feel safe and comfortable asking questions. It can become frustrating to answer the same questions repeatedly; however, community members are expected to remain courteous and helpful to all users equally, regardless of skill or knowledge level. Avoid providing responses that prioritize snideness and snark over useful information. At the same time, everyone is expected to read the provided documentation thoroughly. We are happy to answer questions, provide strategic guidance, and suggest effective workflows, but we are not here to do your job for you.

Harassment includes (but is not limited to) all of the following behaviors:

Offensive comments related to gender (including gender expression and identity), age, sexual orientation, disability, physical appearance, body size, race, and religion

Derogatory terminology including words commonly known to be slurs

Posting sexualized images or imagery in public spaces

Deliberate intimidation

Posting others’ personal information without explicit permission

Sustained disruption of talks or other events

Inappropriate physical contact

Unwelcome sexual attention

Participants asked to stop any harassing behavior are expected to comply immediately. Sponsors are also subject to the anti-harassment policy. In particular, sponsors should not use sexualized images, activities, or other material. Meetup organizing staff and other volunteer organizers should not use sexualized attire or otherwise create a sexualized environment at community events.

In addition to the behaviors outlined above, continuing to behave a certain way after you have been asked to stop also constitutes harassment, even if that behavior is not specifically outlined in this policy. It is considerate and respectful to stop doing something after you have been asked to stop, and all community members are expected to comply with such requests immediately.

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting codeofconduct@ansible.com, to anyone with administrative power in community chat (Admins or Moderators on Matrix, ops on IRC), or to the local organizers of an event. Meetup organizers are encouraged to prominently display points of contact for reporting unacceptable behavior at local events.

If a participant engages in harassing behavior, the meetup organizers may take any action they deem appropriate. These actions may include but are not limited to warning the offender, expelling the offender from the event, and barring the offender from future community events.

Organizers will be happy to help participants contact security or local law enforcement, provide escorts to an alternate location, or otherwise assist those experiencing harassment to feel safe for the duration of the meetup. We value the safety and well-being of our community members and want everyone to feel welcome at our events, both online and offline.

We expect all participants, organizers, speakers, and attendees to follow these policies at all of our event venues and event-related social events.

The Ansible Community Code of Conduct is licensed under the Creative Commons Attribution-Share Alike 3.0 license. Our Code of Conduct was adapted from Codes of Conduct of other open source projects, including:

---

## Developer Certificate Of Origin — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/developer_certificate_of_origin.html

**Contents:**
- Developer Certificate Of Origin

By contributing to this project you agree to the Developer Certificate of Origin (DCO). This document was created by the Linux Kernel community and is a simple statement that you, as a contributor, have the legal right to make the contribution. See the DCO file file for details.

---

## Release Manager Guidelines — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/release_managers.html

**Contents:**
- Release Manager Guidelines
- Pre-releases: what and why
  - Beta releases
  - Release candidates
- Ansible release process

Release Manager Guidelines

Pre-releases: what and why

Ansible release process

The release manager’s purpose is to ensure a smooth release. To achieve that goal, they need to coordinate between:

Developers with commit privileges on the Ansible GitHub repository

Contributors without commit privileges

Ansible documentation team

Pre-releases exist to draw testers. They give people who don’t feel comfortable running from source control a means to get an early version of the code to test and give us feedback. To ensure we get good feedback about a release, we need to make sure all major changes in a release are put into a pre-release. Testers must be given time to test those changes before the final release. Ideally we want there to be sufficient time between pre-releases for people to install and test one version for a span of time. Then they can spend more time using the new code than installing the latest version.

The right length of time for a tester is probably around two weeks. However, for our three-to-four month development cycle to work, we compress this down to one week; any less runs the risk of people spending more time installing the code instead of running it. However, if there’s a time crunch (with a release date that cannot slip), it is better to release with new changes than to hold back those changes to give people time to test between. People cannot test what is not released, so we have to get those tarballs out there even if people feel they have to install more frequently.

In a beta release, we know there are still bugs. We will continue to accept fixes for these. Although we review these fixes, sometimes they can be invasive or potentially destabilize other areas of the code.

During the beta, we will no longer accept feature submissions.

In a release candidate, we’ve fixed all known blockers. Any remaining bugfixes are ones that we are willing to leave out of the release. At this point we need user testing to determine if there are any other blocker bugs lurking.

Blocker bugs generally are those that cause significant problems for users. Regressions are more likely to be considered blockers because they will break present users’ usage of Ansible.

The Release Manager will cherry-pick fixes for new release blockers. The release manager will also choose whether to accept bugfixes for isolated areas of the code or defer those to the next minor release. By themselves, non-blocker bugs will not trigger a new release; they will only make it into the next major release if blocker bugs require that a new release be made.

The last RC should be as close to the final as possible. The following things may be changed:

Version numbers are changed automatically and will differ as the pre-release tags are removed from the versions.

Tests and docs/docsite/ can differ if really needed as they do not break runtime. However, the release manager may still reject them as they have the potential to cause breakage that will be visible during the release process.

We want to specifically emphasize that code (in bin/, lib/ansible/, and setup.py) must be the same unless there are extraordinary extenuating circumstances. If there are extenuating circumstances, the Release Manager is responsible for notifying groups which would want to test the code.

The release process is kept in a separate document so that it can be easily updated during a release. If you need access to edit this, please ask one of the current release managers to add you.

---

## Communicating with the Ansible community — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/communication.html

**Contents:**
- Communicating with the Ansible community
- Code of Conduct
- Forum
  - The Bullhorn
  - Regional and Language-specific channels
- Real-time chat
  - General channels
  - Working group-specific channels
  - Meetings on Matrix
- Working groups

Regional and Language-specific channels

Working group-specific channels

Requesting a forum group

Requesting a community collection repository

Ansible Community Topics

Ansible Automation Platform support questions

All interactions within the Ansible Community are governed by our Community Code of Conduct. Please read and understand it before participating.

The Ansible Forum is the default and recommended starting point for most community interactions. It’s ideal for:

Asking questions and seeking help.

Participating in development discussions.

Learning about events and news.

Register: Sign up to create an account and join the community.

Explore topics: Browse by categories and tags to discover discussions, or simply start a new topic of your own.

Stay updated: Subscribe to specific categories or tags that interest you. Just click the bell icon in the top-right corner of the relevant category or tag page and select your notification preference.

Explore forum groups that match your interests. Joining a group often automatically subscribes you to related posts.

The Bullhorn is our community’s weekly newsletter, published directly in the Forum:

Subscribe: Click the bell button under the Bullhorn category description, then select Watching.

Submit News: See the About the Newsletter category post for submission guidelines.

Questions about the newsletter: Ask us in the Ansible Social room on Matrix.

Communicate in your preferred language by visiting the International Communities forum category. Current subcategories include:

Português (Portuguese)

Join an Ansible Meetup near you.

For details on requesting a new language subcategory, see the About the International Communities category post.

For real-time interactions, the Ansible community uses the Matrix protocol.

The Forum is our default communication platform. We recommend engaging there before considering other options like Matrix.

To join the community on Matrix:

Get a Matrix account: From Matrix.org or any other Matrix homeserver.

Choose a Matrix client: We recommend Element Webchat.

Join rooms: Use the links in the General channels or Working groups to join specific rooms.

For more information, see the community-hosted Matrix FAQ.

You can add Matrix shields to your repository’s README.md using the shield in the community-topics repository as a template.

IRC channels are no longer official communication channels. Use the Forum and Matrix instead.

The clickable links below take you directly to the Matrix room in your browser. Room/channel information is also given for use in other clients:

Community social room & posting news for the Bullhorn newsletter

General usage & support questions

Developer & code-related topics

Community & collections related topics

Many working groups have dedicated chat channels. See the Working groups for details.

The Ansible community holds regular meetings on Matrix. All interested individuals are invited to participate. Check the meeting schedule and agenda page for more information.

Working Groups enable Ansible community members to self-organize around specific interests.

Find a complete list of groups and their communication channels within the Forum groups.

To request a new working group:

First, check if there is no appropriate Forum group you can join instead of starting a new one.

Review the things you can ask for post regarding working groups.

Submit your request in the forum topic.

If a Matrix chat channel is also needed, consult the Ansible Community Matrix FAQ.

Working groups are often built around Ansible community collections. You can use a repository under your organization or request one under ansible-collections on the forum. Create a topic in the Project Discussions category and the ‘coll-repo-request’ tag.

The Ansible Community Steering Committee uses the Forum for asynchronous discussions and voting on community topics.

For more information, see:

Creating new policy proposals & inclusion requests

Community topics workflow

Community topics on the Forum

Red Hat Ansible Automation Platform is a subscription service providing support, certified content, and tooling for Ansible, including content management, a controller, UI and REST API.

For questions related to Ansible Automation Platform, visit Red Hat support instead of community communication platforms.

---

## GitHub Admins — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/community/github_admins.html

**Contents:**
- GitHub Admins
- Adding and removing committers
- Changing branch permissions for releases

Adding and removing committers

Changing branch permissions for releases

GitHub Admins have more permissions on GitHub than normal contributors or even committers. There are a few responsibilities that come with that increased power.

The Ansible Team will periodically review who is actively contributing to Ansible to grant or revoke contributors’ ability to commit on their own. GitHub Admins are the people who have the power to actually manage the GitHub permissions.

When we make releases we make people go through a Release Manager Guidelines to push commits to that branch. The GitHub admins are responsible for setting the branch so only the Release Manager can commit to the branch when the release process reaches that stage and later opening the branch once the release has been made. The Release manager will let the GitHub Admin know when this needs to be done.

The GitHub Admin Process Docs for instructions on how to change branch permissions.

---
