# Supabase - Self Hosting

**Pages:** 14

---

## Self-Hosting with Docker | Supabase Docs

**URL:** https://supabase.com/docs/guides/self-hosting/docker

**Contents:**
- Self-Hosting with Docker
- Learn how to configure and deploy Supabase with Docker.
- Contents#
- Before you begin#
- System requirements#
- Installing Supabase#
- Configuring and securing Supabase#
  - Configure database password#
  - Generate and configure API keys#
  - Configure other keys, and important URLs#

Self-Hosting with Docker

Learn how to configure and deploy Supabase with Docker.

Docker is the easiest way to get started with self-hosted Supabase. It should take you less than 30 minutes to get up and running.

This guide assumes you're comfortable with:

If you're new to these topics, consider starting with managed Supabase for free, or try local development with the CLI.

You need the following installed on your system:

Minimum requirements for running all Supabase components, suitable for development and small to medium production workloads:

If you don't need specific services, such as Logflare (Analytics), Realtime, Storage, imgproxy, or Edge Runtime (Functions), you can remove the corresponding sections and dependencies from docker-compose.yml to reduce resource requirements.

Follow these steps to start Supabase on your machine:

If you are using rootless Docker, edit .env and set DOCKER_SOCKET_LOCATION to your docker socket location. For example: /run/user/1000/docker.sock. Otherwise, you will see an error like container supabase-vector exited (0).

While we provided example placeholder passwords and keys in the .env.example file, you should NEVER start your self-hosted Supabase using these defaults.

Follow all of the steps in this section to ensure you have a secure setup, and only then start all services.

Change the placeholder password in the .env file before starting your Supabase for the first time.

Follow the password guidelines for choosing a secure password. For easier configuration, use only letters and numbers to avoid URL encoding issues in connection strings.

Use the key generator below to obtain and configure the following secure keys in .env:

The generated keys expire in 5 years. You can verify them at jwt.io using the saved value of JWT_SECRET.

Edit the following settings in the .env file:

Review and change URL environment variables:

If you are only using self-hosted Supabase locally, you can use localhost.

Access to Studio dashboard and internal API is protected with HTTP basic authentication.

The default password MUST be changed before starting Supabase.

Change the password in the .env file:

The password must include at least one letter (do not use numbers only).

Optionally change the user:

You can start all services by using the following command in the same directory as your docker-compose.yml file:

After all the services have started you can see them running in the background:

After a minute or less, all services should have a status Up [...] (healthy). If you see a status such as created but not Up, try inspecting the Docker logs for a specific container, e.g.,

To stop Supabase, use:

After the Supabase services are configured and running, you can access the dashboard, connect to the database, and use edge functions.

You can access Supabase Studio through the API gateway on port 8000.

For example: http://example.com:8000, or http://<your-ip>:8000 (or localhost:8000 if you are running Docker Compose locally).

You will be prompted for a username and password. Use the credentials that you set up earlier in Studio authentication.

By default, the Supabase stack provides the Supavisor connection pooler for accessing Postgres and managing database connections.

You can connect to the Postgres database via Supavisor using the methods described below. Use your domain name, your server IP, or localhost depending on whether you are running self-hosted Supabase on a VPS, or locally.

The default POOLER_TENANT_ID is your-tenant-id (can be changed in .env), and the password is the one you set previously in Configure database password.

For session-based connections (equivalent to a direct Postgres connection):

For pooled transactional connections:

When using psql with command-line parameters instead of a connection string to connect to Supavisor, the -U parameter should also be postgres.[POOLER_TENANT_ID], and not just postgres.

If for some reason you need to configure Postgres to be directly accessible from the Internet, read Exposing your Postgres database below.

Edge Functions are stored in volumes/functions. The default setup has a hello function that you can invoke on http://<your-domain>:8000/functions/v1/hello.

You can add new Functions as volumes/functions/<FUNCTION_NAME>/index.ts. Restart the functions service to pick up the changes: docker compose restart functions --no-deps

Each of the APIs is available through the same API gateway:

We publish stable releases of the Docker Compose setup approximately once a month. To update, apply the latest changes from the repository and restart the services. If you want to run different versions of individual services, you can change the image tags in the Docker Compose file, but compatibility is not guaranteed. All Supabase images are available on Docker Hub.

To follow the changes and updates, refer to the self-hosted Supabase changelog.

You need to restart services to pick up the changes, which may result in downtime for your applications and users.

Example: You'd like to update or rollback the Studio image. Follow the steps below:

Be careful — the following destroys all data, including the database and storage volumes!

To uninstall, stop Supabase (while in the same directory as your docker-compose.yml file):

Optionally, ensure removal of all Postgres data:

and all Storage data:

Everything beyond this point in the guide helps you understand how the system works and how you can modify it to suit your needs.

Supabase is a combination of open source tools specifically developed for enterprise-readiness.

If the tools and communities already exist, with an MIT, Apache 2, or equivalent open source license, we will use and support that tool. If the tool doesn't exist, we build and open source it ourselves.

Multiple services require specific configuration within the Postgres database. Refer to the documentation describing the default roles to learn more.

You can find all the default extensions inside the schema migration scripts repo. These scripts are mounted at /docker-entrypoint-initdb.d to run automatically when starting the database container.

Each service has a number of configuration options you can find in the related documentation.

Configuration options are generally added to the .env file and referenced in docker-compose.yml service definitions, e.g.,

You can configure each Supabase service separately through environment variables and configuration files. Below are the most common configuration options.

You will need to use a production-ready SMTP server for sending emails. You can configure the SMTP server by updating the following environment variables:

We recommend using AWS SES. It's extremely cheap and reliable. Restart all services to pick up the new configuration.

By default all files are stored locally on the server. You can configure the Storage service to use S3 by updating the following environment variables:

You can find all the available options in the storage repository. Restart the storage service to pick up the changes: docker compose restart storage --no-deps

Configuring the Supabase AI Assistant is optional. By adding your own OPENAI_API_KEY, you can enable AI services, which help with writing SQL queries, statements, and policies.

By default, docker compose sets the database's log_min_messages configuration to fatal to prevent redundant logs generated by Realtime. You can configure log_min_messages using any of the Postgres Severity Levels.

By default, Postgres connections go through the Supavisor connection pooler for efficient connection management. Two ports are available:

For more information on configuring and using Supavisor, see the Supavisor documentation.

By default, Postgres is only accessible through Supavisor. If you need direct access to the database (bypassing the connection pooler), you need to disable Supavisor and expose the Postgres port.

Exposing Postgres directly bypasses connection pooling and exposes your database to the network. Configure firewall rules or network policies to restrict access to trusted IPs only.

Edit docker-compose.yml:

After restarting, you can connect to the database directly using a standard Postgres connection string:

By default, Storage backend is set to file, which is to use local files as the storage backend. For macOS compatibility, you need to choose VirtioFS as the Docker container file sharing implementation (in Docker Desktop -> Preferences -> General).

Many components inside Supabase use secure secrets and passwords. These are kept in the .env file, but we strongly recommend using a secrets manager when deploying to production.

Some suggested systems include:

**Examples:**

Example 1 (unknown):
```unknown
1# Get the code2git clone --depth 1 https://github.com/supabase/supabase34# Make your new supabase project directory5mkdir supabase-project67# Tree should look like this8# .9# ├── supabase10# └── supabase-project1112# Copy the compose files over to your project13cp -rf supabase/docker/* supabase-project1415# Copy the fake env vars16cp supabase/docker/.env.example supabase-project/.env1718# Switch to your project directory19cd supabase-project2021# Pull the latest images22docker compose pull
```

Example 2 (unknown):
```unknown
1# Start the services (in detached mode)2docker compose up -d
```

Example 3 (unknown):
```unknown
1docker compose ps
```

Example 4 (unknown):
```unknown
1docker compose logs analytics
```

---

## Branching | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching

**Contents:**
- Branching
- Use Supabase Branches to test and preview changes
- How branching works#
- Deploying to production#

Use Supabase Branches to test and preview changes

Use branching to safely experiment with changes to your Supabase project.

Supabase branches create separate environments that spin off from your main project. You can use these branching environments to create and test changes like new configurations, database schemas, or features without affecting your production setup. When you're ready to ship your changes, merge your branch to update your production instance with the new changes.

When you merge any branch into your main project, Supabase automatically runs a deployment workflow to deploy your changes to production. The deployment workflow is expressed as a Directed Acyclic Graph where each node represents one of the following deployment steps.

If a parent deployment step fails, all dependent children steps will be skipped. For e.g., if your database migrations failed at step 5, our runner will not seed your branch because step 6 is skipped. If you are using GitHub integration, the same deployment workflow will be run on every commit pushed to your git branch.

---

## Shared Responsibility Model | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/shared-responsibility-model

**Contents:**
- Shared Responsibility Model
- You share the security responsibility#
- You decide your own workflow#
- You are responsible for your application architecture#
- You are responsible for third-party services#
- You choose your level of comfort with Postgres#
- You are in control of your database#
- Before going to production#
- SOC 2 and compliance#
- Managing healthcare data#

Shared Responsibility Model

Running databases is a shared responsibility between you and Supabase. There are some things that we can take care of for you, and some things that you are responsible for. This is by design: we want to give you the freedom to use your database however you want. While we could put many more restrictions in place to ensure that you can’t do anything wrong, you will eventually find those restrictions prohibitive.

To summarize, you are always responsible for:

Generally, we aim to reduce your burden of managing infrastructure and knowing about Postgres internals, minimizing configuration as much as we can. Here are a few things that you should know:

We give you full access to the database. If you share that access with other people (either people on your team, or the public in general) then it is your responsibility to ensure that the access levels you provide are correctly managed.

If you have an inexperienced member on your team, then you probably shouldn’t give them access to Production. You should set internal workflows around what they should and should not be able to do, with restricted access to avoid anything that might be deemed dangerous.

You are also responsible for ensuring that tables with sensitive data have the right level of access. You are also responsible for managing your database secrets and API keys, storing them safely in an encrypted store.

Supabase provides controls for securing your data, and it is recommended that you always apply Row Level Security (RLS).

We will also provide you with security alerts through Security Advisor and applying the recommendations are your responsibility.

There are many ways to work with Supabase.

You can use our Dashboard, our client libraries, external tools like Prisma and Drizzle, or migration tools like our CLI, Flyway, Sqitch, and anything else that is Postgres-compatible. You can develop directly on your database while you're getting started, run migrations from local to production, or you can use multiple environments.

None of these are right or wrong. It depends on the stage of your project. You definitely shouldn’t be developing on your database directly when you’re in production - but that’s absolutely fine when you’re prototyping and don’t have users.

Supabase isn't a silver-bullet for bad architectural decisions. A poorly designed database will run poorly, no matter where it’s hosted.

You can get away with a poorly-designed database for a while by adding compute. After a while, things will start to break. The database schema is the area you want to spend the most time thinking about. That’s the benefit of Supabase - you can spend more time designing a scalable database system and less time thinking about the mundane tasks like implementing CRUD APIs.

If you don’t want to implement logic inside your database, that is 100% fine. You can use any tools which work with Postgres.

Supabase offers a lot of opportunities for flexibly integrating with third-party services, such as:

You are free to use and integrate with any service, but you're also responsible for ensuring that the performance, availability, and security of the services you use match up with your application's requirements. We do not monitor for outages or performance issues within integrations with third-party services. Depending on the implementation, an issue with such an integration could also result in performance degradation or an outage for your Supabase project.

If your application architecture relies on such integrations, you should monitor the relevant logs and metrics to ensure optimal performance.

Our goal at Supabase is to make all of Postgres easy to use. That doesn’t mean you have to use all of it. If you’re a Postgres veteran, you’ll probably love the tools that we offer. If you’ve never used Postgres before, then start smaller and grow into it. If you just want to treat Postgres like a simple table-store, that’s perfectly fine.

Supabase places very few guard-rails around your database. That gives you a lot of control, but it also means you can break things. ”Break” is used liberally here. It refers to any situation that affects your application because of the way you're using the database.

You are responsible for using best-practices to optimize and manage your database: adding indexes, adding filters on large queries, using caching strategies, optimizing your database queries, and managing connections to the database.

You are responsible of provisioning enough compute to run the workload that your application requires. The Supabase Dashboard provides observability tooling to help with this.

We recommend reviewing and applying the recommendations offered in our Production Checklist. This checklist covers the responsibilities discussed here and a few additional general production readiness best practices.

Supabase provides a SOC 2 compliant environment for hosting and managing sensitive data. We recommend reviewing the SOC 2 compliance responsibilities document alongside the aforementioned production checklist.

You can use Supabase to store and process Protected Health Information (PHI). You are responsible for the following

For more information on the shared responsibilities and rules under HIPAA, review the HIPAA compliance responsibilities document.

---

## Configuration | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching/configuration

**Contents:**
- Configuration
- Configure your Supabase branches using configuration as code
- Branch configuration with remotes#
  - Basic configuration#
  - Remote-specific configuration#
  - Configuration merging#
  - Available configuration options#
- Managing secrets for branches#
      - Secrets are branch-specific
  - Using dotenvx for git-based workflow#

Configure your Supabase branches using configuration as code

This guide covers how to configure your Supabase branches, using the config.toml file. In one single file, you can configure all your branches, including branch settings and secrets.

When Branching is enabled, your config.toml settings automatically sync to all ephemeral branches through a one-to-one mapping between your Git and Supabase branches.

To update configuration for a Supabase branch, modify config.toml and push to git. The Supabase integration will detect the changes and apply them to the corresponding branch.

For persistent branches that need specific settings, you can use the [remotes] block in your config.toml. Each remote configuration must reference an existing project ID.

Here's an example of configuring a separate seed script for a staging environment:

Since the project_id field must reference an existing branch, you need to create the persistent branch before adding its configuration. Use the CLI to create a persistent branch first:

To retrieve the project ID for an existing branch, use the branches list command:

This will display a table showing all your branches with their corresponding project ID. Use the value from the BRANCH PROJECT ID column as your project_id in the remote configuration.

When merging a PR into a persistent branch, the Supabase integration:

If no remote is declared or the project ID is incorrect, the configuration step is skipped.

All standard configuration options are available in the [remotes] block. This includes:

You can use this to maintain different configurations for different environments while keeping them all in version control.

For sensitive configuration like SMTP credentials or API keys, you can use the Supabase CLI to manage secrets for your branches. This is especially useful for custom SMTP setup or other services that require secure credentials.

To set secrets for a persistent branch:

These secrets will be available to your branch's services and can be used in your configuration. For example, in your config.toml:

Secrets set for one branch are not automatically available in other branches. You'll need to set them separately for each branch that needs them.

For managing environment variables across different branches, you can use dotenvx to securely manage your configurations. This approach is particularly useful for teams working with Git branches and preview deployments.

Following the conventions used in the example repository, environments are configured using dotenv files in the supabase directory:

This creates a new encryption key in supabase/.env.preview and a new decryption key in supabase/.env.keys.

Option A: Use encrypted values directly:

Option B: Use environment variables:

The encrypted: syntax only works for designated "secret" fields in the configuration (like secret in auth providers). Using encrypted values in other fields will not be automatically decrypted and may cause issues. For non-secret fields, use environment variables with the env() syntax instead.

When you commit your .env.preview file with encrypted values, the branching executor will automatically retrieve and use these values when deploying your branch. This allows you to maintain different configurations for different branches while keeping sensitive information secure.

Here's an example of a complete multi-environment configuration:

To retrieve the project ID for an existing branch, use the branches list command:

This will display a table showing all your branches with their corresponding project ID. Use the value from the BRANCH PROJECT ID column as your project_id in the remote configuration.

For feature branches that need specific settings:

To retrieve the project ID for an existing branch, use the branches list command:

This will display a table showing all your branches with their corresponding project ID. Use the value from the BRANCH PROJECT ID column as your project_id in the remote configuration.

**Examples:**

Example 1 (unknown):
```unknown
1[remotes.staging]2project_id = "your-project-ref"34[remotes.staging.db.seed]5enabled = true6sql_paths = ["./seeds/staging.sql"]
```

Example 2 (unknown):
```unknown
1supabase --experimental branches create --persistent2# Do you want to create a branch named develop? [Y/n]
```

Example 3 (unknown):
```unknown
1supabase --experimental branches list
```

Example 4 (unknown):
```unknown
1# Set secrets from a .env file2supabase secrets set --env-file ./supabase/.env34# Or set individual secrets5supabase secrets set SMTP_HOST=smtp.example.com6supabase secrets set SMTP_USER=your-username7supabase secrets set SMTP_PASSWORD=your-password
```

---

## Deployment & Branching | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment

**Contents:**
- Deployment & Branching
- Environment management#
      - Self-hosting
- Deployment#

Deployment & Branching

Deploying your app makes it live and accessible to users. Usually, you deploy an app to at least two environments: a production environment for users and (one or multiple) staging or preview environments for developers.

Supabase provides several options for environment management and deployment.

You can maintain separate development, staging, and production environments for Supabase:

Read the self-hosting guides for instructions on hosting your own Supabase stack.

You can automate deployments using:

---

## Integrations | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching/integrations

**Contents:**
- Integrations
- Use Supabase branching with hosting providers and other tools
- Hosting providers#
  - Vercel#
      - Vercel GitHub integration also required.

Use Supabase branching with hosting providers and other tools

Branching works with hosting providers that support preview deployments. Learn how to integrate Supabase branching with various platforms and tools.

With the Supabase branching integration, you can sync the Git branch used by the hosting provider with the corresponding Supabase preview branch. This means that the preview deployment built by your hosting provider is matched to the correct database schema, edge functions, and other Supabase configurations.

Install the Vercel integration:

For branching to work with Vercel, you also need the Vercel GitHub integration.

And make sure you have connected your Supabase project to your Vercel project.

Supabase automatically updates your Vercel project with the correct environment variables for the corresponding preview branches. The synchronization happens at the time of Pull Request being opened, not at the time of branch creation.

As branching integration is tied to the Preview Deployments feature in Vercel, there are possible race conditions between Supabase setting correct variables, and Vercel running a deployment process. Because of that, Supabase is always automatically re-deploying the most recent deployment of the given pull request.

---

## Using the Supabase Terraform Provider | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/terraform/tutorial

**Contents:**
- Using the Supabase Terraform Provider
- Setting up a TF module#
- Creating a project#
  - Importing a project#
- Configuring a project#
  - Configuring branches#
- Committing your changes#
- Resolving config drift#

Using the Supabase Terraform Provider

Run the command terraform -chdir=module apply which should succeed in finding the provider.

Supabase projects are represented as a TF resource called supabase_project.

Create a module/resource.tf file with the following contents.

Remember to substitue placeholder values with your own. For sensitive fields like password, you may consider retrieving it from a secure credentials store.

Next, run terraform -chdir=module apply and confirm creating the new project resource.

If you have an existing project hosted on Supabase, you may import it into your local terraform state for tracking and management.

Edit module/resource.tf with the following changes.

Run terraform -chdir=module apply and you will be prompted to enter the reference ID of an existing Supabase project. If your local TF state is empty, your project will be imported from remote rather than recreated.

Alternatively, you may use the terraform import ... command without editing the resource file.

Keeping your project settings in-sync is easy with the supabase_settings resource.

Create module/settings.tf with the following contents.

Project settings don't exist on their own. They are created and destroyed together with their corresponding project resource referenced by the project_ref field. This means there is no difference between creating and updating supabase_settings resource while deletion is always a no-op.

You may declare any subset of fields to be managed by your TF module. The Supabase provider always performs a partial update when you run terraform -chdir=module apply. The underlying API call is also idempotent so it's safe to apply again if the local state is lost.

To see the full list of settings available, try importing the supabase_settings resource instead.

One of the most powerful features of TF is the ability to fan out configs to multiple resources. You can easily mirror the configurations of your production project to your branch databases using the for_each meta-argument.

Create a module/branches.tf file.

When you run terraform -chdir=module apply, the provider will configure all branches associated with your linked_project to mirror the api settings of your production project.

In addition, the auth.site_url settings of your branches will be customised to a localhost URL for all branches. This allows your users to login via a separate domain for testing.

Finally, you may commit the entire module directory to git for version control. This allows your CI runner to run terraform apply automatically on new config changes. Any command line variables can be passed to CI via TF_VAR_* environment variables instead.

Tracking your configs in TF module does not mean that you lose the ability to change configs through the dashboard. However, doing so could introduce config drift that you need to resolve manually by adding them to your *.tf files.

**Examples:**

Example 1 (unknown):
```unknown
1terraform {2  required_providers {3    supabase = {4      source  = "supabase/supabase"5      version = "~> 1.0"6    }7  }8}910provider "supabase" {11  access_token = file("${path.cwd}/access-token")12}
```

Example 2 (unknown):
```unknown
1# Create a project resource2resource "supabase_project" "production" {3  organization_id   = "<your-org-id>"4  name              = "tf-example"5  database_password = "<your-password>"6  region            = "ap-southeast-1"78  lifecycle {9    ignore_changes = [database_password]10  }11}
```

Example 3 (unknown):
```unknown
1# Define a linked project variable as user input2variable "linked_project" {3  type = string4}56import {7  to = supabase_project.production8  id = var.linked_project9}1011# Create a project resource12resource "supabase_project" "production" {13  organization_id   = "<your-org-id>"14  name              = "tf-example"15  database_password = "<your-password>"16  region            = "ap-southeast-1"1718  lifecycle {19    ignore_changes = [database_password]20  }21}
```

Example 4 (unknown):
```unknown
1# Configure api settings for the linked project2resource "supabase_settings" "production" {3  project_ref = var.linked_project45  api = jsonencode({6    db_schema            = "public,storage,graphql_public"7    db_extra_search_path = "public,extensions"8    max_rows             = 10009  })10}
```

---

## Production Checklist | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/going-into-prod

**Contents:**
- Production Checklist
- Security#
- Performance#
- Availability#
- Rate limiting, resource allocation, & abuse prevention#
  - Auth rate limits#
  - Realtime quotas#
  - Abuse prevention#
  - Email link validity#
- Subscribe to Supabase status page#

After developing your project and deciding it's production ready, you should run through this checklist to ensure that your project:

When working with enterprise systems, email scanners may scan and make a GET request to the reset password link or sign up link in your email. Since links in Supabase Auth are single use, a user who opens an email post-scan to click on a link will receive an error. To get around this problem, consider altering the email template to replace the original magic link with a link to a domain you control. The domain can present the user with a "Sign-in" button which redirect the user to the original magic link URL when clicked.

When using a custom SMTP service, some services might have link tracking enabled which may overwrite or disform the email confirmation links sent by Supabase Auth. To prevent this from happening, we recommend that you disable link tracking when using a custom SMTP service.

Stay informed about Supabase service status by subscribing to the Status Page. We recommend setting up Slack notifications through an RSS feed to ensure your team receives timely updates about service status changes.

Install the RSS app in Slack:

Configure the Supabase status feed:

Once configured, your team will receive automatic notifications in Slack whenever the Supabase Status Page is updated.

For detailed setup instructions, see the Add RSS feeds to Slack.

This checklist is always growing so be sure to check back frequently, and also feel free to suggest additions and amendments by making a PR on GitHub.

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/guides/self-hosting

**Contents:**
- Self-Hosting
- Install and run your own Supabase.
- No telemetry#
- Enterprise#
- Officially supported#
- Community supported#
- Responsibility model#
- Support and troubleshooting#

Install and run your own Supabase.

Self-hosted Supabase lets you run the entire Supabase stack on your own computer, server, or cloud infrastructure.

This is different from:

Self-hosting is a good fit if you need full control over your data, have compliance requirements that prevent using managed services, or want to run Supabase in an isolated environment.

Self-hosted Supabase does not phone home or collect any telemetry.

If you're an enterprise using self-hosted Supabase, we'd love to hear from you. Reach out to our Growth Team to discuss your use case, share feedback, or explore design partnership opportunities.

Deploy Supabase within your own infrastructure using Docker Compose.

There are several community-driven projects to help you deploy Supabase. These projects may be outdated and are seeking active maintainers. If you're interested in maintaining one of these projects, contact the community team.

KubernetesMaintainer needed

TraefikMaintainer needed

When you self-host, you are responsible for:

For resolving common issues, see:

Self-hosted Supabase is community-supported. Get help and connect with other users:

Share your self-hosting experience:

---

## Terraform Provider | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/terraform

**Contents:**
- Terraform Provider
- Using the provider#

The Supabase Provider allows Terraform to manage resources hosted on Supabase platform.

You may use this provider to version control your project settings or setup CI/CD pipelines for automatically provisioning projects and branches.

This simple example imports an existing Supabase project and synchronises its API settings.

**Examples:**

Example 1 (unknown):
```unknown
1terraform {2  required_providers {3    supabase = {4      source  = "supabase/supabase"5      version = "~> 1.0"6    }7  }8}910provider "supabase" {11  access_token = file("${path.module}/access-token")12}1314# Define a linked project variable as user input15variable "linked_project" {16  type = string17}1819# Import the linked project resource20import {21  to = supabase_project.production22  id = var.linked_project23}2425resource "supabase_project" "production" {26  organization_id   = "nknnyrtlhxudbsbuazsu"27  name              = "tf-project"28  database_password = "tf-example"29  region            = "ap-southeast-1"3031  lifecycle {32    ignore_changes = [database_password]33  }34}3536# Configure api settings for the linked project37resource "supabase_settings" "production" {38  project_ref = var.linked_project3940  api = jsonencode({41    db_schema            = "public,storage,graphql_public"42    db_extra_search_path = "public,extensions"43    max_rows             = 100044  })45}
```

---

## Troubleshooting | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching/troubleshooting

**Contents:**
- Troubleshooting
- Common issues and solutions for Supabase branching
- Monitoring deployments#
- Common issues#
  - Rolling back migrations#
  - Deployment failures#
  - Schema drift between preview branches#
  - Changing production branch#
- Migration issues#
  - Failed migrations#

Common issues and solutions for Supabase branching

This guide covers common issues you might encounter when using Supabase branching and how to resolve them.

To check deployment status and troubleshoot failures:

For programmatic monitoring, you can use the Management API to poll branch status.

For detailed troubleshooting guidance, see our Troubleshooting guide.

You might want to roll back changes you've made in an earlier migration change. For example, you may have pushed a migration file containing schema changes you no longer want.

To fix this, push the latest changes, then delete the preview branch in Supabase and reopen it.

The new preview branch is reseeded from the ./supabase/seed.sql file by default. Any additional data changes made on the old preview branch are lost. This is equivalent to running supabase db reset locally. All migrations are rerun in sequential order.

A deployment might fail for various reasons, including invalid SQL statements and schema conflicts in migrations, errors within the config.toml config, or something else.

To check the error message, see the Supabase workflow run for your branch under the View logs section.

If multiple preview branches exist, each preview branch might contain different schema changes. This is similar to Git branches, where each branch might contain different code changes.

When a preview branch is merged into the production branch, it creates a schema drift between the production branch and the preview branches that haven't been merged yet.

These conflicts can be resolved in the same way as normal Git Conflicts: merge or rebase from the production Git branch to the preview Git branch. Since migrations are applied sequentially, ensure that migration files are timestamped correctly after the rebase. Changes that build on top of earlier changes should always have later timestamps.

It's not possible to change the Git branch used as the Production branch for Supabase Branching. The only way to change it is to disable and re-enable branching. See Disable Branching.

When migrations fail, check:

Migrations must run in the correct order. Common issues:

If you can't connect to a preview branch:

Preview branches auto-pause after inactivity. First connections after pause may timeout:

If configuration changes aren't applying:

If secrets aren't working in your branch:

Branch creation might be slow due to:

Preview branches may have different performance characteristics:

If seed data isn't loading:

Remember that preview branch data:

If you're still experiencing issues:

**Examples:**

Example 1 (unknown):
```unknown
1# Test migrations locally first2supabase db reset34# Check migration logs in the dashboard5# Navigate to Branches > Your Branch > View Logs
```

Example 2 (unknown):
```unknown
1# Rename migration files to fix timestamp order2mv 20240101000000_old.sql 20240102000000_old.sql34# Reset local database to test5supabase db reset
```

---

## Working with branches | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching/working-with-branches

**Contents:**
- Working with branches
- Learn how to develop and manage your Supabase branches
- Subscribing to notifications#
        - supabase/functions/notify-slack/index.ts
  - Setup Slack webhook URL
  - Deploy your webhooks processor
  - Update branch notification URL
- Migration and seeding behavior#
  - Using ORM or custom seed scripts#
        - .github/workflows/custom-orm.yaml

Working with branches

Learn how to develop and manage your Supabase branches

This guide covers how to work with Supabase branches effectively, including migration management, seeding behavior, and development workflows.

You can subscribe to webhook notifications when an action run completes on a persistent branch. The payload format follows the webhook standards.

We recommend registering a single webhooks processor that dispatches events to downstream services based on the payload type. The easiest way to do that is by deploying an Edge Function. For example, the following Edge Function listens for run completed events to notify a Slack channel.

Create a Slack webhook URL and set it as Function secrets.

Create and deploy an Edge Function to process webhooks.

Update the notification URL of your target branch to point to your Edge Function.

After completing the steps above, you should receive a Slack message whenever an action run completes on your target branch.

Migrations are run in sequential order. Each migration builds upon the previous one.

The preview branch has a record of which migrations have been applied, and only applies new migrations for each commit. This can create an issue when rolling back migrations.

If you want to use your own ORM for managing migrations and seed scripts, you will need to run them in GitHub Actions after the preview branch is ready. The branch credentials can be fetched using the following example GHA workflow.

You might want to roll back changes you've made in an earlier migration change. For example, you may have pushed a migration file containing schema changes you no longer want.

To fix this, push the latest changes, then delete the preview branch in Supabase and reopen it.

The new preview branch is reseeded from the ./supabase/seed.sql file by default. Any additional data changes made on the old preview branch are lost. This is equivalent to running supabase db reset locally. All migrations are rerun in sequential order.

Your Preview Branches are seeded with sample data using the same as local seeding behavior.

The database is only seeded once, when the preview branch is created. To rerun seeding, delete the preview branch and recreate it by closing, and reopening your pull request.

You can develop with branches using either local or remote development workflows.

Use the branch dropdown in the Supabase dashboard to switch between different branches. Each branch has its own:

Each branch has unique credentials that you can find in the dashboard:

Branches are completely isolated from each other. Changes made in one branch don't affect others, including:

**Examples:**

Example 1 (unknown):
```unknown
1{2  "type": "run.completed",3  "timestamp": "2025-10-17T02:27:18.705861793Z",4  "data": {5    "project_ref": "xuqpsshjxdecrwdyuxvs",6    "details_url": "https://supabase.com/dashboard/project/xuqpsshjxdecrwdyuxvs/branches",7    "action_run": {8      "id": "d5f8b4298d0a4d37b99e255c7837e7af",9      "created_at": "2025-10-17T02:27:10.133329324Z"10      "steps": [11        {12          "name": "clone",13          "status": "exited",14          "updated_at": "2025-10-17T02:27:10.788435466Z"15        },16        {17          "name": "pull",18          "status": "exited",19          "updated_at": "2025-10-17T02:27:11.701742857Z"20        },21        {22          "name": "health",23          "status": "exited",24          "updated_at": "2025-10-17T02:27:12.79205717Z"25        },26        {27          "name": "configure",28          "status": "exited",29          "updated_at": "2025-10-17T02:27:13.726839657Z"30        },31        {32          "name": "migrate",33          "status": "exited",34          "updated_at": "2025-10-17T02:27:14.97017507Z"35        },36        {37          "name": "seed",38          "status": "exited",39          "updated_at": "2025-10-17T02:27:15.637684921Z"40        },41        {42          "name": "deploy",43          "status": "exited",44          "updated_at": "2025-10-17T02:27:18.604193114Z"45        }46      ]47    }48  }49}
```

Example 2 (javascript):
```javascript
1// Setup type definitions for built-in Supabase Runtime APIs2import 'jsr:@supabase/functions-js/edge-runtime.d.ts'34console.log('Branching notification booted!')5const slack = Deno.env.get('SLACK_WEBHOOK_URL') ?? ''67Deno.serve(async (request) => {8  const body = await request.json()9  const blocks = [10    {11      type: 'header',12      text: {13        type: 'plain_text',14        text: `Action run ${body.data.action_run.failure ? 'failed' : 'completed'}`,15        emoji: true,16      },17    },18    {19      type: 'section',20      fields: [21        {22          type: 'mrkdwn',23          text: `*Branch ref:*\n${body.data.project_ref}`,24        },25        {26          type: 'mrkdwn',27          text: `*Run ID:*\n${body.data.action_run.id}`,28        },29      ],30    },31    {32      type: 'section',33      fields: [34        {35          type: 'mrkdwn',36          text: `*Started at:*\n${body.data.action_run.created_at}`,37        },38        {39          type: 'mrkdwn',40          text: `*Completed at:*\n${body.timestamp}`,41        },42      ],43    },44    {45      type: 'section',46      text: {47        type: 'mrkdwn',48        text: `<${body.data.details_url}|View logs>`,49      },50    },51  ]52  const resp = await fetch(slack, {53    method: 'POST',54    body: JSON.stringify({55      blocks,56    }),57  })58  const message = await resp.text()59  return new Response(60    JSON.stringify({61      message,62    }),63    {64      status: 200,65    }66  )67})
```

Example 3 (unknown):
```unknown
1supabase secrets set --project-ref <branch-ref> SLACK_WEBHOOK_URL=<your-webhook-url>
```

Example 4 (unknown):
```unknown
1supabase functions deploy --project-ref <branch-ref> --use-api notify-slack
```

---

## Automated testing using GitHub Actions | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/ci/testing

**Contents:**
- Automated testing using GitHub Actions
- Run your tests when you or your team make changes.
- Testing your database#
- Testing your Edge Functions#
- More resources#

Automated testing using GitHub Actions

Run your tests when you or your team make changes.

You can use the Supabase CLI to run automated tests.

After you have created unit tests for your database, you can use the GitHub Action to run the tests.

Inside your repository, create a new file inside the .github/workflows folder called database-tests.yml. Copy this snippet inside the file, and the action will run whenever a new PR is created:

After you have created unit tests for your Edge Functions, you can use the GitHub Action to run the tests.

Inside your repository, create a new file inside the .github/workflows folder called functions-tests.yml. Copy this snippet inside the file, and the action will run whenever a new PR is created:

**Examples:**

Example 1 (unknown):
```unknown
1name: 'database-tests'2on:3  pull_request:45jobs:6  build:7    runs-on: ubuntu-latest8    steps:9      - uses: actions/checkout@v310      - uses: supabase/setup-cli@v111        with:12          version: latest13      - run: supabase db start14      - run: supabase test db
```

Example 2 (unknown):
```unknown
1name: 'functions-tests'2on:3  pull_request:45jobs:6  build:7    runs-on: ubuntu-latest8    steps:9      - uses: actions/checkout@v310      - uses: supabase/setup-cli@v111        with:12          version: latest13      - uses: denoland/setup-deno@v214        with:15          deno-version: latest16      - run: supabase start17      - run: deno test --allow-all deno-test.ts --env-file .env.local
```

---

## GitHub integration | Supabase Docs

**URL:** https://supabase.com/docs/guides/deployment/branching/github-integration

**Contents:**
- GitHub integration
- Connect with GitHub to sync branches with your repository
- Installation#
- Preparing your Git repository#
  - Initialize Supabase locally
  - Pull your database migration
  - Commit the `supabase` directory to Git
- Syncing GitHub branches#
  - Configuration#
  - Migrations#

Connect with GitHub to sync branches with your repository

Supabase Branching uses the Supabase GitHub integration to read files from your GitHub repository. With this integration, Supabase watches all commits, branches, and pull requests of your GitHub repository.

In the Supabase Dashboard:

You will be using the Supabase CLI to initialise your local ./supabase directory:

If you don't have a ./supabase directory, you can create one:

Pull your database changes using supabase db pull. To get your database connection string, go to your project dashboard, click Connect and look for the Session pooler connection string.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

Commit the supabase directory to Git, and push your changes to your remote repository.

Enable the Automatic branching option in your GitHub Integration configuration to automatically sync GitHub branches with Supabase branches.

When a new branch is created in GitHub, a corresponding branch is created in Supabase. (You can enable the Supabase changes only option to only create Supabase branches when Supabase files change.)

You can test configuration changes on your Preview Branch by configuring the config.toml file in your Supabase directory. See the Configuration docs for more information.

A comment is added to your PR with the deployment status of your preview branch.

The migrations in the migrations subdirectory of your Supabase directory are automatically run.

No production data is copied to your Preview branch. This is meant to protect your sensitive production data.

You can seed your Preview Branch with sample data using the seed.sql file in your Supabase directory. See the Seeding docs for more information.

Data changes in your seed files are not merged to production.

Enable the Deploy to production option in your GitHub Integration configuration to automatically deploy changes when you push or merge to production branch.

The following changes are deployed:

All other configurations, including API, Auth, and seed files, are ignored by default.

We highly recommend turning on a 'required check' for the Supabase integration. You can do this from your GitHub repository settings. This prevents PRs from being merged when migration checks fail, and stops invalid migrations from being merged into your production branch.

To catch failures early, we also recommend subscribing to email notifications on your branch. Common errors include migration conflict, function deployment failure, or invalid configuration file.

You can setup a custom GitHub Action to monitor the status of any Supabase Branch.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init
```

Example 2 (unknown):
```unknown
1supabase db pull --db-url <db_connection_string>23# Your Database connection string will look like this:4# postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:5432/postgres
```

Example 3 (unknown):
```unknown
1git add supabase2git commit -m "Initial migration"3git push
```

Example 4 (unknown):
```unknown
1name: Branch Status23on:4  pull_request:5    types:6      - opened7      - reopened8      - synchronize9    branches:10      - main11      - develop12    paths:13      - 'supabase/**'1415jobs:16  failed:17    runs-on: ubuntu-latest18    steps:19      - uses: fountainhead/action-wait-for-check@v1.2.020        id: check21        with:22          checkName: Supabase Preview23          ref: ${{ github.event.pull_request.head.sha || github.sha }}24          token: ${{ secrets.GITHUB_TOKEN }}2526      - if: ${{ steps.check.outputs.conclusion == 'failure' }}27        run: exit 1
```

---
