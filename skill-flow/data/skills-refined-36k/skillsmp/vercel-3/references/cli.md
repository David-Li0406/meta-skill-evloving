# Vercel - Cli

**Pages:** 19

---

## vercel whoami

**URL:** https://vercel.com/docs/cli/whoami

**Contents:**
- vercel whoami
- Usage
- Global Options

The command is used to show the username of the user currently logged into Vercel CLI.

Using the vercel whoami command to view the username of the user currently logged into Vercel CLI.

The following global options can be passed when using the vercel whoami command:

For more information on global options and their usage, refer to the options section.

---

## vercel switch

**URL:** https://vercel.com/docs/cli/switch

**Contents:**
- vercel switch
- Usage
- Extended Usage
- Global Options

The command is used to switch to a different team scope when logged in with Vercel CLI. You can choose to select a team from a list of all those you are part of or specify a team when entering the command.

Using the vercel switch command to change team scope with Vercel CLI.

Using the vercel switch command to change to a specific team scope with Vercel CLI.

The following global options can be passed when using the vercel switch command:

For more information on global options and their usage, refer to the options section.

---

## vercel cache

**URL:** https://vercel.com/docs/cli/cache

**Contents:**
- vercel cache
- Usage
- Extended Usage
- Unique Options
  - tag
  - srcimg
  - revalidation-deadline-seconds
  - Yes
- Global Options

The command is used to manage the cache for your project, such as CDN cache and Data cache.

Learn more about purging Vercel cache.

Using the vercel cache purge command to purge the CDN cache and Data cache for the current project.

Using the vercel cache purge --type cdn command to purge the CDN cache for the currenet project.

Using the vercel cache purge --type data command to purge the Data cache for the current project.

Using the vercel cache invalidate --tag blog-posts command to invalidate the cached content associated with tag "blog-posts" for the current project. Subsequent requests for this cached content will serve STALE and revalidate in the background.

Using the vercel cache dangerously-delete --tag blog-posts command to dangerously delete the cached content associated with tag "blog-posts" for the current project. Subsequent requests for this cached content will serve MISS and therefore block while revalidating.

Using the vercel cache invalidate --srcimg /api/avatar/1 command to invalidate all cached content associated with the source image "/api/avatar/1" for the current project. Subsequent requests for this cached content will serve STALE and revalidate in the background.

Using the vercel cache dangerously-delete --srcimg /api/avatar/1 command to dangerously delete all cached content associated with the source image "/api/avatar/1" for the current project. Subsequent requests for this cached content will serve MISS and therefore block while revalidating.

Using the vercel cache dangerously-delete --srcimg /api/avatar/1 --revalidation-deadline-seconds 604800 command to dangerously delete all cached content associated with the source image "/api/avatar/1" for the current project if not accessed in the next 604800 seconds (7 days).

These are options that only apply to the command.

The option specifies which tag to invalidate or delete from the cache. You can provide a single tag or multiple comma-separated tags. This option works with both and subcommands.

Using the vercel cache invalidate command with multiple tags.

The option specifies a source image path to invalidate or delete from the cache. This invalidates or deletes all cached transformations of the source image. This option works with both and subcommands.

You can't use both and options together. Choose one based on whether you're invalidating cached content by tag or by source image.

Using the vercel cache invalidate command with a source image path.

The option specifies the revalidation deadline in seconds. When used with , cached content will only be deleted if it hasn't been accessed within the specified time period.

Using the vercel cache dangerously-delete command with a 1-hour (3600 seconds) revalidation deadline.

The option can be used to bypass the confirmation prompt when purging the cache or dangerously deleting cached content.

Using the vercel cache purge command with the --yes option.

The following global options can be passed when using the vercel cache command:

For more information on global options and their usage, refer to the options section.

---

## vercel integration

**URL:** https://vercel.com/docs/cli/integration

**Contents:**
- vercel integration
- vercel integration add
- vercel integration open
- vercel integration list
- vercel integration remove
- Global Options

The command needs to be used with one of the following actions:

For the in all the commands below, use the URL slug value of the integration.

The command initializes the setup wizard for creating an integration resource. This command is used when you want to add a new resource from one of your installed integrations. This functionality is the same as .

If you have not installed the integration for the resource or accepted the terms & conditions of the integration through the web UI, this command will open your browser to the Vercel dashboard and start the installation flow for that integration.

Using the command to create a new integration resource

The command opens a deep link into the provider's dashboard for a specific integration. It's useful when you need quick access to the provider's resources from your development environment.

Using the command to open the provider's dashboard

The command displays a list of all installed resources with their associated integrations for the current team or project. It's useful for getting an overview of what integrations are set up in the current scope of your development environment.

Using the command to list the integration resources.

The output shows the name, status, product, and integration for each installed resource.

The command uninstalls the specified integration from your Vercel account. It's useful in automation workflows.

Using the command to uninstall an integration

You are required to remove all installed resources from this integration before using this command.

The following global options can be passed when using the vercel integration command:

For more information on global options and their usage, refer to the options section.

---

## vercel pull

**URL:** https://vercel.com/docs/cli/pull

**Contents:**
- vercel pull
- Usage
- Unique Options
  - Yes
  - environment
- Global Options

The command is used to store Environment Variables and Project Settings in a local cache (under ) for offline use of and . If you aren't using those commands, you don't need to run .

When environment variables or project settings are updated on Vercel, remember to use again to update your local environment variable and project settings values under .

To download Environment Variables to a specific file (like ), use instead.

Using the vercel pull fetches the latest "development" Environment Variables and Project Settings from the cloud.

Using the vercel pull fetches the latest "preview" Environment Variables and Project Settings from the cloud.

Using the vercel pull fetches the "feature-branch" Environment Variables and Project Settings from the cloud.

Using the vercel pull fetches the latest "production" Environment Variables and Project Settings from the cloud.

These are options that only apply to the command.

The option can be used to skip questions you are asked when setting up a new Vercel Project. The questions will be answered with the default scope and current directory for the Vercel Project name and location.

Using the vercel pull command with the --yes option.

Use the option to define the environment you want to pull environment variables from. This could be production, preview, or a custom environment.

The following global options can be passed when using the vercel pull command:

For more information on global options and their usage, refer to the options section.

---

## vercel init

**URL:** https://vercel.com/docs/cli/init

**Contents:**
- vercel init
- Usage
- Extended Usage
- Unique Options
  - Force
- Global Options

The command is used to initialize Vercel supported framework examples locally from the examples found in the Vercel examples repository.

Using the vercel init command to initialize a Vercel supported framework example locally. You will be prompted with a list of supported frameworks to choose from.

Using the vercel init command to initialize a specific framework example from the Vercel examples repository locally.

Using the vercel init command to initialize a specific Vercel framework example locally and rename the directory.

These are options that only apply to the command.

The option, shorthand , is used to forcibly replace an existing local directory.

Using the vercel init command with the --force option.

Using the vercel init command with the --force option.

The following global options can be passed when using the vercel init command:

For more information on global options and their usage, refer to the options section.

---

## vercel integration-resource

**URL:** https://vercel.com/docs/cli/integration-resource

**Contents:**
- vercel integration-resource
- vercel integration-resource remove
- vercel integration-resource disconnect
- Global Options

The command needs to be used with one of the following actions:

For the in all the commands below, use the URL slug value of the product for this installed resource.

The command uninstalls the product for this resource from the integration.

Using the command to uninstall a resource's product from an integration.

When you include the parameter, all connected projects are disconnected before removal.

The command disconnects a product's resource from a project where it is currently associated.

When you include the parameter, all connected projects are disconnected.

Using the command to disconnect a resource from it's connected project(s)

Using the command to disconnect a resource from a specific connected project where is the URL slug of the project.

The following global options can be passed when using the vercel integration command:

For more information on global options and their usage, refer to the options section.

---

## Vercel CLI Global Options

**URL:** https://vercel.com/docs/cli/global-options

**Contents:**
- Vercel CLI Global Options
- Current Working Directory
- Debug
- Global config
- Help
- Local config
- Scope
- Token
- No Color

Global options are commonly available to use with multiple Vercel CLI commands.

The option can be used to provide a working directory (that can be different from the current directory) when running Vercel CLI commands.

This option can be a relative or absolute path.

Using the vercel command with the --cwd option.

The option, shorthand , can be used to provide a more verbose output when running Vercel CLI commands.

Using the vercel command with the --debug option.

The option, shorthand , can be used set the path to the global configuration directory.

Using the vercel command with the --global-config option.

The option, shorthand , can be used to display more information about Vercel CLI commands.

Using the vercel command with the --help option.

Using the vercel alias command with the --help option.

The option, shorthand , can be used to set the path to a local file.

Using the vercel command with the --local-config option.

The option, shorthand , can be used to execute Vercel CLI commands from a scope that’s not currently active.

Using the vercel command with the --scope option.

The option, shorthand , can be used to execute Vercel CLI commands with an authorization token.

Using the vercel command with the --token option.

The option, or environment variable, can be used to execute Vercel CLI commands with no color or emoji output. This respects the NO_COLOR standard.

Using the vercel command with the --no-color option.

---

## vercel link

**URL:** https://vercel.com/docs/cli/link

**Contents:**
- vercel link
- Usage
- Extended Usage
- Unique Options
  - Repo Alpha
  - Yes
  - Project
- Global Options

The command links your local directory to a Vercel Project.

Using the vercel link command to link the current directory to a Vercel Project.

Using the vercel link command and supplying a path to the local directory of the Vercel Project.

These are options that only apply to the command.

The option can be used to link all projects in your repository to their respective Vercel projects in one command. This command requires that your Vercel projects are using the Git integration.

The option can be used to skip questions you are asked when setting up a new Vercel Project. The questions will be answered with the default scope and current directory for the Vercel Project name and location.

Using the vercel link command with the --yes option.

The option can be used to specify a project name. In non-interactive usage, allows you to set a project name that does not match the name of the current working directory.

Using the vercel link command with the --project option.

The following global options can be passed when using the vercel link command:

For more information on global options and their usage, refer to the options section.

---

## vercel login

**URL:** https://vercel.com/docs/cli/login

**Contents:**
- vercel login
- Usage
- Global Options
- Related guides

The command allows you to login to your Vercel account through Vercel CLI.

Using the vercel login command to login to a Vercel account.

The following global options can be passed when using the vercel login command:

For more information on global options and their usage, refer to the options section.

---

## vercel help

**URL:** https://vercel.com/docs/cli/help

**Contents:**
- vercel help
- Usage
- Extended Usage

The command generates a list of all available Vercel CLI commands and options in the terminal. When combined with a second argument - a valid Vercel CLI command - it outputs more detailed information about that command.

Alternatively, the global option can be added to commands to get help information about that command.

Using the vercel help command to generate a list of Vercel CLI commands and options.

Using the vercel help command to generate detailed information about a specific Vercel CLI command.

---

## Sandbox CLI Reference

**URL:** https://vercel.com/docs/vercel-sandbox/cli-reference

**Contents:**
- Sandbox CLI Reference
- Installation
- Authentication
  - Example
  - Options
  - Flags
  - Example
  - Options
  - Flags
  - Arguments

The Sandbox CLI, based on the Docker CLI, allows you to manage sandboxes, execute commands, copy files, and more from your terminal. This page provides a complete reference for all available commands.

Use the CLI for manual testing and debugging, or use the SDK to automate sandbox workflows in your application.

Install the Sandbox CLI globally to use all commands:

Log in to use Vercel Sandbox:

Get help information for all available sandbox commands:

Description: Interfacing with Vercel Sandbox

Available subcommands:

For more help, try running sandbox <subcommand> --help

List all sandboxes for the specified account and project.

Create and run a command in a sandbox.

Create a sandbox in the specified account and project.

Execute a command in an existing sandbox.

Stop one or more running sandboxes.

Copy files between your local filesystem and a remote sandbox.

Log in to the Sandbox CLI.

Log out of the Sandbox CLI.

---

## vercel telemetry

**URL:** https://vercel.com/docs/cli/telemetry

**Contents:**
- vercel telemetry
- Usage
- Global Options

The command allows you to enable or disable telemetry collection.

Using the vercel telemetry status command to show whether telemetry collection is enabled or disabled.

Using the vercel telemetry enable command to enable telemetry collection.

Using the vercel telemetry disable command to disable telemetry collection.

The following global options can be passed when using the vercel telemetry command:

For more information on global options and their usage, refer to the options section.

---

## vercel install

**URL:** https://vercel.com/docs/cli/install

**Contents:**
- vercel install
- Usage
- Global Options

The command is used to install a native integration with the option of adding a product to an existing installation.

If you have not installed the integration before, you will asked to open the Vercel dashboard and accept the Vercel Marketplace terms. You can then decide to continue and add a product through the dashboard or cancel the product addition step.

If you have an existing installation with the provider, you can add a product directly from the CLI by answering a series of questions that reflect the choices you would make in the dashboard.

Using the vercel install command install the ACME integration.

You can get the value of by looking at the slug of the integration provider from the marketplace URL. For example, for , is .

The following global options can be passed when using the vercel install command:

For more information on global options and their usage, refer to the options section.

---

## Using the Command Menu

**URL:** https://vercel.com/docs/dashboard-features/command-menu

**Contents:**
- Using the Command Menu
- Recently Used Items
- Context-Based Items
- Additional Keyboard Shortcuts
- Searching documentation
  - Searching from the Vercel documentation
  - Searching from the Vercel dashboard
- What about regular menus?

Vercel provides a menu with shortcuts, called the Command Menu, to navigate through the dashboard and perform common actions using only the keyboard.

You can access the menu by pressing ⌘ + K on macOS or Ctrl + K on Windows and Linux. Alternatively, you can access it by clicking on Command Menu in your personal menu at the top right of the dashboard:

Once opened, the Command Menu will offer you a list of commonly used shortcuts. For example, you can quickly navigate to a specific Project or Team right away, using your ↑ (arrow up), ↓ (arrow down) and ↵ (enter) keys.

The Command Menu is only available on desktop and tablet devices, but not on smartphones, as it provides the biggest efficiency advantage when used in combination with a keyboard, instead of your mouse or finger.

By default, the list is comprised of shortcuts that the Vercel Team has found to be most useful for you. However, over time, the list will automatically adapt to your own usage of the Command Menu and begin to suggest recently used shortcuts at the top:

An example of recently used items suggested by the Command Menu.

Up to 3 suggestions for recently used shortcuts will appear, and be ordered by the latest time you used them, with the most recently used item showing up at the very top.

When the dashboard is closed, the suggestions will reset.

Because the purpose of the Command Menu is to get you to your desired goal in the quickest way possible, it also changes its behavior based on your surrounding context on the dashboard.

If you're currently looking at the dashboard for a Pro or Enterprise Team, for example, you will be offered to copy a link for inviting new Team Members if you're an Owner of that Team.

Whereas, if you're on a Hobby plan instead, you will not be offered that option because Hobby plans don't support collaborating.

In addition to ⌘ + K (instead of ⌘, use Ctrl on Windows or Linux) for opening the overview of the Command Menu, Vercel also offers direct keyboard shortcuts for some of the commonly used actions:

They are also shown next to each of the supported items in the list.

Thanks to the shortcuts mentioned above, you often won't even have to navigate through the items offered by the Command Menu to get to your desired destination quickly.

Instead, you can use these shortcuts to skip the overview of items and perform the action directly. Therefore, it is recommended to embed these shortcuts into your workflow.

The Command Menu allows you to search through the documentation on the Vercel, Next.js and Turborepo websites.

When on the Vercel documentation site:

When on the Vercel dashboard:

If you want, the Command Menu can be a complete replacement for the traditional dashboard navigation.

Regular menus will continue to exist for the purpose of navigating the dashboard with your mouse or fingers (on touch-based devices), but if you're most efficient using your keyboard, you might prefer the Command Menu.

Over time, the Command Menu will offer increasingly intelligent suggestions and allow for performing more actions inline to increase your productivity.

---

## vercel teams

**URL:** https://vercel.com/docs/cli/teams

**Contents:**
- vercel teams
- Usage
- Extended Usage
- Global Options

The command is used to manage Teams, providing functionality to list, add, and invite new Team Members.

You can manage Teams with further options and greater control from the Vercel Dashboard.

Using the vercel teams command to list all teams you’re a member of.

Using the vercel teams command to create a new team.

Using the vercel teams command to invite a new Team Member.

The following global options can be passed when using the vercel teams command:

For more information on global options and their usage, refer to the options section.

---

## Linking Projects with Vercel CLI

**URL:** https://vercel.com/docs/cli/project-linking

**Contents:**
- Linking Projects with Vercel CLI
- Framework detection
- Relevant commands

When running in a directory for the first time, Vercel CLI needs to know which scope and Vercel Project you want to deploy your directory to. You can choose to either link an existing Vercel Project or to create a new one.

Linking an existing Vercel Project when running Vercel CLI in a new directory.

Once set up, a new directory will be added to your directory. The directory contains both the organization and of your Vercel Project. If you want unlink your directory, you can remove the directory.

You can use the option to skip these questions.

When you create a new Vercel Project, Vercel CLI will link the Vercel Project and automatically detect the framework you are using and offer default Project Settings accordingly.

Creating a new Vercel Project with the vercel command.

You will be provided with default Build Command, Output Directory, and Development Command options.

You can continue with the default Project Settings or overwrite them. You can also edit your Project Settings later in your Vercel Project dashboard.

---

## vercel logout

**URL:** https://vercel.com/docs/cli/logout

**Contents:**
- vercel logout
- Usage
- Global Options

The command allows you to logout of your Vercel account through Vercel CLI.

Using the vercel logout command to logout of a Vercel account.

The following global options can be passed when using the vercel logout command:

For more information on global options and their usage, refer to the options section.

---

## vercel env

**URL:** https://vercel.com/docs/cli/env

**Contents:**
- vercel env
  - Exporting Development Environment Variables
- Usage
- Extended Usage
- Unique Options
  - Yes
- Global Options

The command is used to manage Environment Variables of a Project, providing functionality to list, add, remove, and export.

To leverage environment variables in local tools (like or ) that want them in a file (like ), run . This will export your Project's environment variables to that file. After updating environment variables on Vercel (through the dashboard, , or ), you will have to run again to get the updated values.

Some frameworks make use of environment variables during local development through CLI commands like or . The sub-command will export development environment variables to a local file or a different file of your choice.

To override environment variable values temporarily, use:

If you are using vercel build or vercel dev, you should use vercel pull instead. Those commands operate on a local copy of environment variables and Project settings that are saved under .vercel/, which vercel pull provides.

Using the vercel env command to list all Environment Variables in a Vercel Project.

Using the vercel env command to add an Environment Variable to a Vercel Project.

Using the vercel env command to remove an Environment Variable from a Vercel Project.

Using the vercel env command to list Environment Variables for a specific Environment in a Vercel Project.

Using the vercel env command to list Environment Variables for a specific Environment and Git branch.

Using the vercel env command to add an Environment Variable to all Environments to a Vercel Project.

Using the vercel env command to add an Environment Variable for a specific Environment to a Vercel Project.

Using the vercel env command to add an Environment Variable to a specific Git branch.

Using the vercel env command to add an Environment Variable to a Vercel Project using a local file's content as the value.

Using the echo command to generate the value of the Environment Variable and piping that value into the vercel dev command. Warning: this will save the value in bash history, so this is not recommend for secrets.

Using the vercel env command to add an Environment Variable with Git branch to a Vercel Project using a local file's content as the value.

Using the vercel env command to remove an Environment Variable from a Vercel Project.

Using the vercel env command to download Development Environment Variables from the cloud and write to a specific file.

Using the vercel env command to download Preview Environment Variables from the cloud and write to the .env.local file.

Using the vercel env command to download "feature-branch" Environment Variables from the cloud and write to the .env.local file.

These are options that only apply to the command.

The option can be used to bypass the confirmation prompt when overwriting an environment file or removing an environment variable.

Using the vercel env pull command with the --yes option to overwrite an existing environment file.

Using the vercel env rm command with the --yes option to skip the remove confirmation.

The following global options can be passed when using the vercel env command:

For more information on global options and their usage, refer to the options section.

---
