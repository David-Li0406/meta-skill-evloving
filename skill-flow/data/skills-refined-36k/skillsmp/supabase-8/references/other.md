# Supabase - Other

**Pages:** 45

---

## PrivateLink | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/privatelink

**Contents:**
- PrivateLink
- How PrivateLink works#
- Requirements#
- Getting started#
    - Step 1: Contact Supabase support#
    - Step 2: Accept resource share#
    - Step 3: Configure security groups#
    - Step 4: Create connection#
      - Option A: Create a PrivateLink endpoint
      - Option B: Attach resource configuration to an existing VPC lattice service network

PrivateLink is currently in alpha and available exclusively to Enterprise customers. Contact your account manager or reach out to our team to enable this feature.

PrivateLink provides enterprise-grade private network connectivity between your AWS VPC and your Supabase database using AWS VPC Lattice. This eliminates exposure to the public internet by creating a secure, private connection that keeps your database traffic within the AWS network backbone.

By enabling PrivateLink, database connections never traverse the public internet, enabling the disablement of public facing connectivity and providing an additional layer of security and compliance for sensitive workloads. This infrastructure-level security feature helps organizations meet strict data governance requirements and reduces potential attack vectors.

Supabase PrivateLink is an organisation level configuration. It works by sharing a VPC Lattice Resource Configuration to any number of AWS Accounts for each of your Supabase projects. Connectivity can be achieved by either associating the Resource Configuration to a PrivateLink endpoint, or a VPC Lattice Service Network. This means:

The connection architecture changes from public internet routing to a dedicated private path through AWS's secure network backbone.

Supabase PrivateLink is currently just for direct database and PgBouncer connections only. It does not support other Supabase services like API, Storage, Auth, or Realtime. These services will continue to operate over public internet connections.

To use PrivateLink with your Supabase project:

Reach out to your Enterprise account manager or contact our team to initiate PrivateLink setup. During this initial contact, be prepared to provide:

Supabase will send you an AWS Resource Share containing the VPC Lattice Resource Configurations for your projects. To accept this share:

After accepting, you'll see the resource configurations appear in your Shared with me > Shared resources section of the RAM console and the PrivateLink and Lattice > Resource configurations section of the VPC console.

Ensure your security groups allow traffic on the appropriate ports:

In your AWS account, you have two options to establish connectivity:

Verify the private connection is working correctly from your VPC:

You should see a successful connection without any public internet traffic.

Configure your applications to use the private connection details:

Example connection string update:

For maximum security, you can disable public internet access for your database:

During the alpha phase:

The PrivateLink endpoint is a layer 3 solution so behaves like a standard Postgres endpoint, allowing you to connect using:

Ready to enhance your database security with PrivateLink? Contact our Enterprise team to discuss your requirements and begin the setup process.

Our support team will guide you through the configuration and ensure your private database connectivity meets your security and performance requirements.

**Examples:**

Example 1 (unknown):
```unknown
1psql "postgresql://[username]:[password]@[private-endpoint]:5432/postgres"
```

Example 2 (unknown):
```unknown
1# Before (public)2postgresql://user:pass@db.[project-ref].supabase.co:5432/postgres34# After (private)5postgresql://user:pass@your-private-endpoint.vpce.amazonaws.com:5432/postgres
```

---

## Billing FAQ | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/billing-faq

**Contents:**
- Billing FAQ
- This documentation covers frequently asked questions around subscription plans, payments, invoices and billing in general
- Organizations and projects#
    - What are organizations and projects?#
    - How many free projects can I have?#
    - Can I mix free and paid projects in a single organization?#
    - Can I transfer my projects to another organization?#
    - Can I transfer my credits to another organization?#
- Pricing#
    - Are there any charges for paused projects?#

This documentation covers frequently asked questions around subscription plans, payments, invoices and billing in general

The Supabase Platform has "organizations" and "projects". An organization may contain multiple projects. Each project is a dedicated Supabase instance with all of its sub-services including Storage, Auth, Functions and Realtime. Each organization only has a single subscription with a single plan (Free, Pro, Team or Enterprise). Project add-ons such as Compute, IPv4, Log Drains, Advanced MFA, Custom Domains and PITR are configured per project and are added to your organization subscription.

Read more on About billing on Supabase.

You are entitled to two active free projects. Paused projects do not count towards your quota. Note that within an organization, we count the free project limits from all members that are either Owner or Admin. If you’ve got another organization member with the Admin or Owner role that has already exhausted their free project quota, you won’t be able to launch another free project in that organization. You can create another Free Plan organization or change the role of the affected member in your organization’s team settings.

The subscription plan is set on the organization level and it is not possible to mix paid and non-paid projects inside a single organization. However, you can have a paid and a free organization and make use of the self-serve project transfers to organize your projects. All projects in an organization benefit from the subscription plan. If your organization is on the Pro Plan, all projects within the organization benefit from no project pausing, automated backups and so on.

Yes, you can transfer your projects to another organization. You can find instructions on how to transfer your projects here.

Yes, you can transfer the credits to another organization. Submit a support ticket.

See the Pricing page for details.

No, we do not charge for paused projects. Compute hours are only counted for active instances. Paused projects do not incur any compute usage charges.

We provide a dedicated server for every Supabase project. Each paid organization comes with $10 in Compute Credits to cover one project on the default compute size. Additional projects start at ~$10 a month (billed hourly).

Running 3 projects in a Pro Plan organization on the default Micro instance:

Refer to our Compute docs for more examples and insights.

Each Supabase project is a dedicated VM and Postgres database. By default, your instance runs on the Micro compute instance. You have the option to upgrade your compute size in your Project settings. See Compute Add-ons for available options.

When you change your compute size, there are no immediate upfront charges. Instead, you will be billed based on the compute hours during your billing cycle reset.

If you launch additional instances on your paid plan, we will add the corresponding compute hours to your final invoice.

If you upgrade your project to a larger instance for 10 hours and then downgrade, you’ll only pay for the larger instance for the 10 hours of usage at the end of your billing cycle. You can see your current compute usage on your organization’s usage page.

Read more about Compute usage.

Egress refers to the total bandwidth (network traffic) quota available to each organization. This quota can be utilized for various purposes such as Storage, Realtime, Auth, Functions, Supavisor, Log Drains and Database. Each plan includes a specific egress quota, and any additional usage beyond that quota is billed accordingly.

We differentiate between cached (served via our CDN from cache hits) and uncached egress and give quotas for each type and have varying pricing (cached egress is cheaper). Cached egress only applies to Storage.

Read more about Egress usage.

Change your subscription plan in your organization's billing settings. To upgrade to an Enterprise Plan, complete the Enterprise request form.

The organization is given credits for unused time on the subscription plan. The credits will not expire and can be used again in the future. You may see an additional charge for unbilled excessive usage charges from your previous billing cycle.

Read more about downgrades.

We can transfer the amount as credits to another organization of your choice. You can use these credits to upgrade the organization, or if you have already upgraded, the credits will be used to pay the next month's invoice. Please create a support ticket for this case.

You will be notified when you exceed the Free Plan quota. It is important to take action at this point. If you continue to exceed the limits without reducing your usage, service restrictions will apply. To avoid service restrictions, you have two options: reduce your usage or upgrade to a paid plan. Learn more about restrictions in the Fair Use Policy section.

You will be notified when you exceed your Pro Plan quota. To unblock yourself, you can toggle off your spend cap in your organization's billing settings to pay for over-usage beyond the Pro plans limits. If you continue to exceed the limits without reducing your usage or turning off the spend cap, restrictions will apply. Learn more about restrictions in the Fair Use Policy section.

The Pro Plan has a Spend Cap enabled by default to keep costs under control. If you want to scale beyond the plan's included quota, switch off the Spend Cap to pay for additional usage beyond the plans included limits. You can toggle the Spend Cap in the organization's billing settings. Read more about the Spend Cap.

Our Fair Use Policy gives developers the freedom to build and experiment with Supabase, while protecting our infrastructure. Under the Fair Use policy, service restrictions may apply to your organization if:

You will receive a notification before Fair Use Policy restrictions are applied. However, in some cases, like suspected abuse of our services, restrictions may be applied without prior notice.

When your organization exceeds plan limits, you receive a grace period before fair use policy applies. After this grace period ends, the dashboard will continue to show a notice indicating that your grace period is over, even if you have dropped back under plan limits. This is a warning that serves as an indicator that your organization previously exceeded usage limits.

This persistent warning means that if you exceed your plan limits again, you will not receive another grace period and your project will be restricted. The notice and indicator will automatically clear if you continue to stay under plan limits for multiple billing cycles.

The Fair Use Policy is applied through service restrictions. This could mean:

The Fair Use Policy is generally applied to all projects of the restricted organization.

To remove restrictions, you will need to address the issue that caused the restriction. This could be reducing your usage, paying overdue invoices, updating your payment method, or any other issue that caused the restriction. Once the issue is resolved, the restriction will be lifted.

Restrictions due to usage limits are lifted with the next billing cycle as your quota refills at the beginning of each cycle. You can see when your current billing cycle ends on the billing page under "Upcoming Invoice". You can also lift restrictions immediately by upgrading to Pro (if on Free Plan) or by disabling spend cap (if on Pro Plan with spend cap enabled).

You can find all invoices from your organization on your organization’s invoices page.

You can find the breakdown of your usage on your organization’s usage page.

You can check your Credit balance on the organization’s billing page. Credits will be used on future invoices before charging your payment method. If you have enough credits to cover an invoice, there is no charge at all.

You can update your VAT number in the Tax ID section of your organization’s billing page.

Any changes made to your billing details will only be reflected in your upcoming invoices. Our payment provider cannot regenerate previous invoices. Therefore, make sure to update the billing details before the upcoming invoices are finalized.

We accept credit card payments only. If you cannot pay via credit card, we do offer alternatives for larger upfront payments. Create a support ticket in case you’re interested.

Visa, Mastercard, American Express, Japan Credit Bureau (JCB), China UnionPay (CUP), Cartes Bancaires

All our invoices are issued in USD, but you can pay in any currency so long as the credit card provider allows charging in USD after conversion.

Yes, you will have to add the new payment method before being allowed to remove the old one. This can be done from your dashboard on the organization’s billing page.

Read more on Manage your payment methods.

You can top up your credit balance to cover multiple months through your organization’s billing page.

Read more on Credit top-ups.

Payments are taken at the beginning of each billing cycle. You will be charged once a month. You can see the current billing cycle and upcoming invoice in your organization's billing settings. The subscription plan fee is charged upfront, whereas usage-charges, including compute, are charged in arrears based on your usage.

Read more on Your monthly invoice.

You can update your billing details on the organization’s billing page. Note that any changes made to your billing details will only be reflected in your upcoming invoices. Our payment provider cannot regenerate previous invoices.

When an invoice becomes overdue, we will pause your projects and downgrade your organization to the Free Plan. You will be able to restore your projects once you have paid all outstanding invoices.

We were unable to charge your payment method. This likely means that the payment was not successfully processed with the credit card on your account profile. You can be overdue when

Check your payment methods in your organization’s billing page to ensure there are no expired payment methods and the correct payment method is marked as default. If you are still facing issues, raise a support ticket.

Payments are always in USD and may show up as coming from Singapore, given our payment entity is in Singapore. Make sure you allow payments from Singapore and in USD

No, you cannot delay your payment.

No, we do not provide refunds. Please refer to our Terms of Service.

Take a moment to review our Your monthly invoice page, which may help clarify any questions about your invoice. If it still looks wrong, submit a support ticket through the dashboard. Select the affected organization and provide the invoice number for us to look at your case.

---

## Supabase Platform | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform

**Contents:**
- Supabase Platform
- Projects#
- Organizations#
- Platform status#

Supabase is a hosted platform which makes it very simple to get started without needing to manage any infrastructure.

Visit supabase.com/dashboard and sign in to start creating projects.

Each project on Supabase comes with:

Organizations are a way to group your projects. Each organization can be configured with different team members and billing settings. Refer to access control for more information on how to manage team members within an organization.

If Supabase experiences outages, we keep you as informed as possible, as early as possible. We provide the following feedback channels:

Make sure to review our SLA for details on our commitment to Platform Stability.

---

## Supabase Marketplace | Supabase Docs

**URL:** https://supabase.com/docs/guides/integrations/supabase-marketplace

**Contents:**
- Supabase Marketplace
- Build an integration#
- List your integration#

The Supabase Marketplace brings together all the tools you need to extend your Supabase project. This includes:

Supabase provides several integration points:

Apply to the Partners program to list your integration in the Partners marketplace and in the Supabase docs.

Integrations are assessed on the following criteria:

---

## Reports | Supabase Docs

**URL:** https://supabase.com/docs/guides/telemetry/reports

**Contents:**
- Reports
- Using reports#
- Database#
  - Advanced Telemetry#
  - Memory usage#
  - CPU usage#
  - Disk input/output operations per second (IOPS)#
  - Disk throughput#
  - Disk size#
  - Database connections#

Supabase Reports provide comprehensive observability for your project through dedicated monitoring dashboards that visualize key metrics across your database, auth, storage, realtime, and API systems. Each report offers self-debugging tools to gain actionable insights for optimizing performance and troubleshooting issues.

Reports are only available for projects hosted on the Supabase Cloud platform and are not available for self-hosted instances.

Reports can be filtered by time range to focus your analysis on specific periods. Available time ranges are gated by your organization's plan, with higher-tier plans providing access to longer historical periods.

The Database report provides the most comprehensive view into your Postgres instance's health and performance characteristics. These charts help you identify performance bottlenecks, resource constraints, and optimization opportunities at a glance.

The following charts are available for Free and Pro plans:

The following charts provide a more advanced and detailed view of your database performance and are available only for Team, Enterprise, and Platform plans.

How it helps debug issues:

Actions you can take:

How it helps debug issues:

Actions you can take:

This chart displays read and write IOPS with a reference line showing your compute size's maximum IOPS capacity.

How it helps debug issues:

Actions you can take:

Available on Team and Enterprise plans.

This chart displays read and write throughput (bytes per second) with a reference line showing your compute size's maximum disk throughput.

How it helps debug issues:

Actions you can take:

How it helps debug issues:

Actions you can take:

How it helps debug issues:

Actions you can take:

The Auth report focuses on user authentication patterns and behaviors within your Supabase project.

The Storage report provides visibility into how your Supabase Storage is being utilized, including request patterns, performance characteristics, and caching effectiveness.

The Realtime report tracks WebSocket connections, channel activity, and real-time event patterns in your Supabase project.

The Edge Functions report provides insights into serverless function performance, execution patterns, and regional distribution across Supabase's global edge network.

The API Gateway report analyzes traffic patterns and performance characteristics of requests flowing through your Supabase project's API layer.

---

## Upgrading | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/upgrading

**Contents:**
- Upgrading
- In-place upgrades#
- Pause and restore#
- Caveats#
  - Logical replication#
  - Breaking changes#
  - Time limits#
  - Disk sizing#
  - Objects dependent on Postgres extensions#
  - pg_cron records#

Supabase ships fast and we endeavor to add all new features to existing projects wherever possible. In some cases, access to new features require upgrading or migrating your Supabase project.

This guide refers to upgrading the Postgres version of your Supabase Project. For scaling your compute size, refer to the Compute and Disk page.

You can upgrade your project using in-place upgrades or by pausing and restoring your project.

For security purposes, passwords for custom roles are not backed up and, following a restore, they would need to be reset. See here for more details

In-place upgrades uses pg_upgrade. For projects larger than 1GB, this method is generally faster than a pause and restore cycle, and the speed advantage grows with the size of the database.

Additionally, if the upgrade should fail, your original database would be brought back up online and be able to service requests.

As a rough rule of thumb, pg_upgrade operates at ~100MBps (when executing an upgrade on your data). Using the size of your database, you can use this metric to derive an approximate sense of the downtime window necessary for the upgrade. During this window, you should plan for your database and associated services to be unavailable.

We recommend using the In-place upgrade method, as it is faster, and more reliable. Additionally, only Free-tier projects are eligible to use the Pause and Restore method.

When you pause and restore a project, the restored database includes the latest features. This method does include downtime, so be aware that your project will be inaccessible for a short period of time.

Note that a pause + restore upgrade involves tearing down your project's resources before bringing them back up again. If the restore process should fail, manual intervention from Supabase support will be required to bring your project back online.

Regardless of the upgrade method, a few caveats apply:

If you are using logical replication, the replication slots will not be preserved by the upgrade process. You will need to manually recreate them after the upgrade with the method pg_create_logical_replication_slot. Refer to the Postgres docs on Replication Management Functions for more details about the method.

Newer versions of services can break functionality or change the performance characteristics you rely on. If your project is eligible for an upgrade, you will be able to find your current service versions from within the Supabase dashboard.

Breaking changes are generally only present in major version upgrades of Postgres and PostgREST. You can find their respective release notes at:

If you are upgrading from a significantly older version, you will need to consider the release notes for any intermediary releases as well.

Starting from 2024-06-24, when a project is paused, users then have a 90-day window to restore the project on the platform from within Supabase Studio.

The 90-day window allows Supabase to introduce platform changes that may not be backwards compatible with older backups. Unlike active projects, static backups can't be updated to accommodate such changes.

During the 90-day restore window a paused project can be restored to the platform with a single button click from Studio's dashboard page.

After the 90-day restore window, you can download your project's backup file, and Storage objects from the project dashboard. You can restore the data in the following ways:

If you upgrade to a paid plan while your project is paused within the 90-day restore window, any expired one-click restore options are reenabled. Since the backup was taken outside the backwards compatibility window, it may fail to restore. If you have a problem restoring your backup after upgrading, contact Support.

When upgrading, the Supabase platform will "right-size" your disk based on the current size of the database. For example, if your database is 100GB in size, and you have a 200GB disk, the upgrade will reduce the disk size to 120GB (1.2x the size of your database).

In-place upgrades do not support upgrading of databases containing reg* data types referencing system OIDs. If you have created any objects that depend on the following extensions, you will need to recreate them after the upgrade.

pg_cron does not automatically clean up historical records. This can lead to extremely large cron.job_run_details tables if the records are not regularly pruned; you should clean unnecessary records from this table prior to an upgrade.

During an in-place upgrade, the pg_cron extension gets dropped and recreated. Prior to this process, the cron.job_run_details table is duplicated to avoid losing historical logs. The instantaneous disk pressure created by duplicating an extremely large details table can cause at best unnecessary performance degradation, or at worst, upgrade process failures.

In-place upgrades do not currently support upgrading of databases using extensions older than the following versions:

To upgrade to a newer version of Postgres, you will need to drop the extensions before the upgrade, and recreate them after the upgrade.

The md5 hashing method has known weaknesses that make it unsuitable for cryptography. As such, we are deprecating md5 in favor of scram-sha-256, which is the default and most secure authentication method used in the latest Postgres versions.

We automatically migrate Supabase-managed roles' passwords to scram-sha-256 during the upgrade process, but you will need to manually migrate the passwords of any custom roles you have created, else you won't be able to connect using them after the upgrade.

To identify roles using the md5 hashing method and migrate their passwords, you can use the following SQL statements after the upgrade:

As part of the upgrade process, maintenance operations such as vacuuming are also executed. This can result in a reduction in the reported database size.

Supabase performs extensive pre- and post-upgrade validations to ensure that the database has been correctly upgraded. However, you should plan for your own application-level validations, as there might be changes you might not have anticipated, and this should be budgeted for when planning your downtime window.

In projects using Postgres 17, the following extensions are deprecated:

Projects planning to upgrade from Postgres 15 to Postgres 17 need to first disable these extensions in the Supabase Dashboard.

pgjwt was enabled by default on every Supabase project up until Postgres 17. If you weren’t explicitly using pgjwt in your project, it’s most likely safe to disable.

Existing projects on lower versions of Postgres are not impacted, and the extensions will continue to be supported on projects using Postgres 15, until the end of life of Postgres 15 on the Supabase platform.

**Examples:**

Example 1 (unknown):
```unknown
1-- List roles using md5 hashing method2SELECT3  rolname4FROM pg_authid5WHERE rolcanlogin = true6  AND rolpassword LIKE 'md5%';78-- Migrate a role's password to scram-sha-2569ALTER ROLE <role_name> WITH PASSWORD '<password>';
```

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?products=supavisor

---

## Migrating to Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-to-supabase

**Contents:**
- Migrating to Supabase
- Migration guides#

Migrating to Supabase

Learn how to migrate to Supabase from another database service.

---

## Expose Queues for local and self-hosted Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/queues/expose-self-hosted-queues

**Contents:**
- Expose Queues for local and self-hosted Supabase
- Learn how to expose Queues when running Supabase with Supabase CLI or Docker Compose
- Expose Queues with Supabase CLI#
- Expose queues with Docker compose#
- Stop exposing queues#

Expose Queues for local and self-hosted Supabase

Learn how to expose Queues when running Supabase with Supabase CLI or Docker Compose

By default, local and self-hosted Supabase instances expose only core schemas like public and graphql_public. To allow client-side consumers to use your queues, you have to add pgmq_public schema to the list of exposed schemas.

Before continuing, complete the step Expose queues to client-side consumers from the Queues Quickstart guide. This creates the pgmq_public schema, which must exist before it can be exposed through the API.

You only need to expose the pgmq_public schema manually when running Supabase locally with the Supabase CLI or self-hosting using Docker Compose.

When running Supabase locally with Supabase CLI, update your project's config.toml file. Locate the [api] section and add pgmq_public to the list of schemas.

Then restart your local Supabase stack.

When running Supabase with Docker Compose, locate the PGRST_DB_SCHEMAS variable inside your .env file and add pgmq_public to it. This environment variable is passed to the rest service inside docker-compose.yml.

Restart your containers for the changes to take effect.

If you no longer want to expose the pgmq_public schema, you can remove it from your configuration.

After updating your configuration, restart your containers for the changes to take effect.

**Examples:**

Example 1 (unknown):
```unknown
1[api]2enabled = true3port = 543214schemas = ["public", "graphql_public", "pgmq_public"]
```

Example 2 (unknown):
```unknown
1supabase stop && supabase start
```

Example 3 (unknown):
```unknown
1PGRST_DB_SCHEMAS=public,graphql_public,pgmq_public
```

Example 4 (unknown):
```unknown
1docker compose down2docker compose up -d
```

---

## Secure configuration of Supabase products | Supabase Docs

**URL:** https://supabase.com/docs/guides/security/product-security

**Contents:**
- Secure configuration of Supabase products
- Auth#
- Database#
- Storage#
- Realtime#

Secure configuration of Supabase products

The Supabase production checklist provides detailed advice on preparing an app for production. While our SOC 2 and HIPAA compliance documents outline the roles and responsibilities for building a secure and compliant app.

Various products at Supabase have their own hardening and configuration guides, below is a definitive list of these to help guide your way.

---

## Manage Disk size usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/disk-size

**Contents:**
- Manage Disk size usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Pricing#
  - General purpose disks (gp3)#
  - High performance disks (io2)#
- Billing examples#
  - Gp3#
  - Io2#

Manage Disk size usage

Each database has a dedicated disk. You are charged for the provisioned disk size.

Disk size is not relevant for the Free Plan. Instead Free Plan customers are limited by Database size.

Disk size is charged by Gigabyte-Hours (GB-Hrs). 1 GB-Hr represents 1 GB being provisioned for 1 hour. For example, having 10 GB provisioned for 5 hours results in 50 GB-Hrs (10 GB × 5 hours).

Usage is shown as "Disk Size GB-Hrs" on your invoice.

Pricing depends on the disk type, with gp3 being the default disk type.

$0.000171 per GB-Hr ($0.125 per GB per month). The primary database of your project gets provisioned with an 8 GB disk. You are only charged for provisioned disk size exceeding these 8 GB.

Launching a Read Replica creates an additional database with its own dedicated disk. You are charged from the first byte of provisioned disk for the Read Replica. Refer to Manage Read Replica usage for details on billing.

$0.000267 per GB-Hr ($0.195 per GB per month). Unlike general purpose disks, high performance disks are billed from the first byte of provisioned disk.

Project 1 and 2 don't exceed the included disk size, so no charges for Disk size apply. Project 3 exceeds the included disk size by 42 GB, incurring charges for this additional usage.

This disk type is billed from the first byte of provisioned disk, meaning for 66 GB across all projects.

You can view Disk size usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown.

In the Disk size section, you can see how much disk size your projects have provisioned.

To see how your disk usage is distributed across Database, WAL, and System categories, refer to Disk size distribution.

To see how you can downsize your disk, refer to Reducing disk size

---

## Project Transfers | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/project-transfer

**Contents:**
- Project Transfers
- Pre-Requirements#
- Usage-billing and project add-ons#
- Things to watch out for#
- Transfer to a different region#

You can freely transfer projects between different organizations. Head to your projects' general settings to initiate a project transfer.

Source organization - the organization the project currently belongs to Target organization - the organization you want to move the project to

For usage metrics such as disk size, egress or image transformations and project add-ons such as Compute Add-On, Point-In-Time-Recovery, IPv4, Log Drains, Advanced MFA or a Custom Domain, the source organization will still be charged for the usage up until the transfer. The charges will be added to the invoice when the billing cycle resets.

The target organization will be charged at the end of the billing cycle for usage after the project transfer.

Note that project transfers are only transferring your projects across an organization and cannot be used to transfer between different regions. To move your project to a different region, see migrating your project.

---

## Manage IPv4 usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/ipv4

**Contents:**
- Manage IPv4 usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - One project#
  - Multiple projects#
  - One project with Read Replicas#

You can assign a dedicated IPv4 address to a database by enabling the IPv4 add-on. You are charged for all IPv4 addresses configured across your databases.

If the primary database has a dedicated IPv4 address configured, its Read Replicas are also assigned one, with charges for each.

IPv4 addresses are charged by the hour, meaning you are charged for the exact number of hours that an IPv4 address is assigned to a database. If an address is assigned for part of an hour, you are still charged for the full hour.

Your billing cycle runs from January 1 to January 31. On January 10 at 4:30 PM, you enable the IPv4 add-on for your project. At the end of the billing cycle you are billed for 512 hours.

Usage is shown as "IPv4 Hours" on your invoice.

$0.0055 per hour ($4 per month).

The project has the IPv4 add-on enabled throughout the entire billing cycle.

All projects have the IPv4 add-on enabled throughout the entire billing cycle.

The project has two Read Replicas and the IPv4 add-on enabled throughout the entire billing cycle.

To see whether your database actually needs a dedicated IPv4 address, refer to When you need the IPv4 add-on.

---

## Integrations | Supabase Docs

**URL:** https://supabase.com/docs/guides/integrations

**Contents:**
- Integrations
- Vercel Marketplace#
- Supabase Marketplace#

Supabase integrates with many of your favorite third-party services.

Create and manage your Supabase projects directly through Vercel. Get started with Vercel.

Browse tools for extending your Supabase project. Browse the Supabase Marketplace.

---

## Manage your usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage

**Contents:**
- Manage your usage

Each subpage breaks down a specific usage item and details what you're charged for, how costs are calculated, and how to optimize usage and reduce costs.

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting

---

## Manage Point-in-Time Recovery usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/point-in-time-recovery

**Contents:**
- Manage Point-in-Time Recovery usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
  - Pricing#
- Billing examples#
  - One project#
  - Multiple projects#

Manage Point-in-Time Recovery usage

You can configure Point-in-Time Recovery (PITR) for a project by enabling the PITR add-on. You are charged for every enabled PITR add-on across your projects.

PITR is charged by the hour, meaning you are charged for the exact number of hours that PITR is active for a project. If PITR is active for part of an hour, you are still charged for the full hour.

Your billing cycle runs from January 1 to January 31. On January 10 at 4:30 PM, you activate PITR for your project. At the end of the billing cycle you are billed for 512 hours.

Usage is shown as "Point-in-time recovery Hours" on your invoice.

Pricing depends on the recovery retention period, which determines how many days back you can restore data to any chosen point of up to seconds in granularity.

For a detailed breakdown of how charges are calculated, refer to Manage Point-in-Time Recovery usage.

The project has PITR with a recovery retention period of 7 days activated throughout the entire billing cycle.

All projects have PITR with a recovery retention period of 14 days activated throughout the entire billing cycle.

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?tags=cpu

---

## Security testing of your Supabase projects | Supabase Docs

**URL:** https://supabase.com/docs/guides/security/security-testing

**Contents:**
- Security testing of your Supabase projects
  - Permitted services#
  - Prohibited testing and activities#
- Terms and conditions#

Security testing of your Supabase projects

Supabase customer support policy for penetration testing

Customers of Supabase are permitted to carry out security assessments or penetration tests of their hosted Supabase project components. This testing may be carried out without prior approval for the customer services listed under permitted services. Supabase does not permit hosting security tooling that may be perceived as malicious or part of a campaign against Supabase customers or external services. This section is covered by the Supabase Acceptable Use Policy (AUP).

It is the customer’s responsibility to ensure that testing activities are aligned with this policy. Any testing performed outside of the policy will be seen as testing directly against Supabase and may be flagged as abuse behaviour. If Supabase receives an abuse report for activities related to your security testing, we will forward these to you. If you discover a security issue within any of the Supabase products, contact Supabase Security immediately.

Furthermore, Supabase runs a Vulnerability Disclosure Program (VDP) with HackerOne, and external security researchers may report any bugs found within the scope of the aforementioned program. Customer penetration testing does not form part of this VDP.

The customer agrees to the following,

---

## Read Replicas | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/read-replicas

**Contents:**
- Read Replicas
- Deploy read-only databases across multiple regions, for lower latency and better resource management.
- About Read Replicas#
- Prerequisites#
- Getting started#
  - Deploying a Read Replica#
  - What does it mean when "Init failed" is observed?#
- Features#
  - Dedicated endpoints#
  - Dedicated connection pool#

Deploy read-only databases across multiple regions, for lower latency and better resource management.

Read Replicas are additional databases that are kept in sync with your Primary database. You can read your data from a Read Replica, which helps with:

The database you start with when launching a Supabase project is your Primary database. Read Replicas are kept in sync with the Primary through a process called "replication." Replication is asynchronous to ensure that transactions on the Primary aren't blocked. There is a delay between an update on the Primary and the time that a Read Replica receives the change. This delay is called "replication lag."

You can only read data from a Read Replica. This is in contrast to a Primary database, where you can both read and write:

Read Replicas are available for all projects on the Pro, Team and Enterprise plans. Spin one up now over at the Infrastructure Settings page.

Projects must meet these requirements to use Read Replicas:

To add a Read Replica, go to the Infrastructure Settings page in your dashboard.

You can also manage Read Replicas using the Management API (beta functionality):

Projects on an XL compute add-on or larger can create up to five Read Replicas. Projects on compute add-ons smaller than XL can create up to two Read Replicas. All Read Replicas inherit the compute size of their Primary database.

A Read Replica is deployed by using a physical backup as a starting point, and a combination of WAL file archives and direct replication from the Primary database to catch up. Both components may take significant time to complete. The duration of restoring from a physical backup is roughly dependent and directly related to the database size of your project. The time taken to catch up to the primary using WAL archives and direct replication is dependent on the level of activity on the Primary database; a more active database will produce a larger number of WAL files that will need to be processed.

Along with the progress of the deployment, the dashboard displays rough estimates for each component.

The status Init failed indicates that the Read Replica has failed to deploy. Some possible scenarios as to why a Read Replica may have failed to be deployed:

It is safe to drop this failed Read Replica, and in the event of a transient issue, attempt to spin up another one. If however spinning up Read Replicas for your project consistently fails, do check out our status page for any ongoing incidents, or open a support ticket here. To aid the investigation, do not bring down the recently failed Read Replica.

Read Replicas offer the following features:

Each Read Replica has its own dedicated database and API endpoints.

Read Replicas only support GET requests from the REST API. If you are calling a read-only Postgres function through the REST API, make sure to set the get: true option.

Requests to other Supabase products, such as Auth, Storage, and Realtime, aren't able to use a Read Replica or its API endpoint. Support for more products will be added in the future.

If you're using an IPv4 add-on, the database endpoints for your Read Replicas will also use an IPv4 add-on.

A connection pool through Supavisor is also available for each Read Replica. Find the connection string on the Database Settings page under Connection String.

A load balancer is deployed to automatically balance requests between your Primary database and Read Replicas. Find its endpoint on the API Settings page.

The load balancer enables geo-routing for Data API requests so that GET requests will automatically be routed to the database that is closest to your user ensuring the lowest latency. Non-GET requests can also be sent through this endpoint, and will be routed to the Primary database.

You can also interact with Supabase services (Auth, Edge Functions, Realtime, and Storage) through this load balancer so there's no need to worry about which endpoint to use and in which situations. However, geo-routing for these services are not yet available but is coming soon.

Due to the requirements of the Auth service, all Auth requests are handled by the Primary, even when sent over the load balancer endpoint. This is similar to how non-Read requests for the Data API (PostgREST) are exclusively handled by the Primary.

To call a read-only Postgres function on Read Replicas through the REST API, use the get: true option.

If you remove all Read Replicas from your project, the load balancer and its endpoint are removed as well. Make sure to redirect requests back to your Primary database before removal.

Starting on April 4th, 2025, we will be changing the routing behavior for eligible Data API requests:

The new behavior delivers a better experience for your users by minimizing the latency to your project. You can take full advantage of this by placing Read Replicas close to your major customer bases.

If you use a custom domain, requests will not be routed through the load balancer. You should instead use the dedicated endpoints provided in the dashboard.

In the SQL editor, you can choose if you want to run the query on a particular Read Replica.

When a Read Replica is deployed, it emits logs from the following services:

Views on Log Explorer are automatically filtered by databases, with the logs of the Primary database displayed by default. Viewing logs from other databases can be toggled with the Source button found on the upper-right part section of the Logs Explorer page.

For API logs, logs can originate from the API Load Balancer as well. The upstream database or the one that eventually handles the request can be found under the Redirect Identifier field. This is equivalent to metadata.load_balancer_redirect_identifier when querying the underlying logs.

Observability and metrics for Read Replicas are available on the Supabase Dashboard. Resource utilization for a specific Read Replica can be viewed on the Database Reports page by toggling for Source. Likewise, metrics on API requests going through either a Read Replica or Load Balancer API endpoint are also available on the dashboard through the API Reports page

We recommend ingesting your project's metrics into your own environment. If you have an existing ingestion pipeline set up for your project, you can update it to additionally ingest metrics from your Read Replicas.

All settings configured through the dashboard will be propagated across all databases of a project. This ensures that no Read Replica get out of sync with the Primary database or with other Read Replicas.

The following procedures require all Read Replicas for a project to be brought down before they can be performed:

These operations need to be completed before Read Replicas can be re-deployed.

We use a hybrid approach to replicate data from a Primary to its Read Replicas, combining the native methods of streaming replication and file-based log shipping.

Postgres generates a Write Ahead Log (WAL) as database changes occur. With streaming replication, these changes stream from the Primary to the Read Replica server. The WAL alone is sufficient to reconstruct the database to its current state.

This replication method is fast, since changes are streamed directly from the Primary to the Read Replica. On the other hand, it faces challenges when the Read Replica can't keep up with the WAL changes from its Primary. This can happen when the Read Replica is too small, running on degraded hardware, or has a heavier workload running.

To address this, Postgres does provide tunable configuration, like wal_keep_size, to adjust the WAL retained by the Primary. If the Read Replica fails to “catch up” before the WAL surpasses the wal_keep_size setting, the replication is terminated. Tuning is a bit of an art - the amount of WAL required is variable for every situation.

In this replication method, the Primary continuously buffers WAL changes to a local file and then sends the file to the Read Replica. If multiple Read Replicas are present, files could also be sent to an intermediary location accessible by all. The Read Replica then reads the WAL files and applies those changes. There is higher replication lag than streaming replication since the Primary buffers the changes locally first. It also means there is a small chance that WAL changes do not reach Read Replicas if the Primary goes down before the file is transferred. In these cases, if the Primary fails a Replica using streaming replication would (in most cases) be more up-to-date than a Replica using file-based log shipping.

We bring these two methods together to achieve quick, stable, and reliable replication. Each method addresses the limitations of the other. Streaming replication minimizes replication lag, while file-based log shipping provides a fallback. For file-based log shipping, we use our existing Point In Time Recovery (PITR) infrastructure. We regularly archive files from the Primary using WAL-G, an open source archival and restoration tool, and ship the WAL files to S3.

We combine it with streaming replication to reduce replication lag. Once WAL-G files have been synced from S3, Read Replicas connect to the Primary and stream the WAL directly.

Replication lag for a specific Read Replica can be monitored through the dashboard. On the Database Reports page Read Replicas will have an additional chart under Replica Information displaying historical replication lag in seconds. Realtime replication lag in seconds can be observed on the Infrastructure Settings page. This is the value on top of the Read Replica. Do note that there is no single threshold to indicate when replication lag should be addressed. It would be fully dependent on the requirements of your project.

If you are already ingesting your project's metrics into your own environment, you can also keep track of replication lag and set alarms accordingly with the metric: physical_replication_lag_physical_replica_lag_seconds.

Some common sources of high replication lag include:

High replication lag can result in stale data being returned for queries being executed against the affected read replicas.

You can consult additional resources on the subject as well.

When a project that utilizes Read Replicas is restarted, or the compute add-on size is changed, the Primary database gets restarted first. During this period, the Read Replicas remain available.

Once the Primary database has completed restarting (or resizing, in case of a compute add-on change) and become available for usage, all the Read Replicas are restarted (and resized, if needed) concurrently.

For a detailed breakdown of how charges are calculated, refer to Manage Read Replica usage.

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export PROJECT_REF="your-project-ref"45# Create a new Read Replica6curl -X POST "https://api.supabase.com/v1/projects/$PROJECT_REF/read-replicas/setup" \7  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \8  -H "Content-Type: application/json" \9  -d '{10    "region": "us-east-1"11  }'1213# Delete a Read Replica14curl -X POST "https://api.supabase.com/v1/projects/$PROJECT_REF/read-replicas/remove" \15  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \16  -H "Content-Type: application/json" \17  -d '{18    "database_identifier": "abcdefghijklmnopqrst"19  }'
```

---

## Migrating within Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/migrating-within-supabase

**Contents:**
- Migrating within Supabase
- Learn how to migrate from one Supabase project to another
- Database migration guides#
  - Backup file from the dashboard (*.backup)#
  - SQL backup files (*.sql)#
- Transfer project to a different organization#

Migrating within Supabase

Learn how to migrate from one Supabase project to another

If you are on a Paid Plan and have physical backups enabled, you should instead use the Restore to another project feature.

If you need to migrate from one Supabase project to another, choose the appropriate guide below:

Follow the Restore dashboard backup guide

Follow the Backup and Restore using the CLI guide

Project migration is primarily for changing regions or upgrading to new major versions of the platform in some scenarios. If you need to move your project to a different organization without touching the infrastructure, see project transfers.

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?tags=connections

---

## Manage Read Replica usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/read-replicas

**Contents:**
- Manage Read Replica usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Billing examples#
  - No additional resources configured#
  - Additional resources configured#
- FAQ#
  - Do Compute Credits apply to Read Replica Compute?#

Manage Read Replica usage

Each Read Replica is a dedicated database. You are charged for its resources: Compute, Disk Size, provisioned Disk IOPS, provisioned Disk Throughput, and IPv4.

Read Replica charges are the total of the charges listed below.

Compute Compute is charged by the hour, meaning you are charged for the exact number of hours that a Read Replica is running and, therefore, incurring Compute usage. If a Read Replica runs for part of an hour, you are still charged for the full hour.

Read Replicas run on the same Compute size as the primary database.

Disk Size Refer to Manage Disk Size usage for details on how charges are calculated. The disk size of a Read Replica is 1.25x the size of the primary disk to account for WAL archives. With a Read Replica you go beyond your subscription plan's quota for Disk Size.

Provisioned Disk IOPS (optional) Read Replicas inherit any additional provisioned Disk IOPS from the primary database. Refer to Manage Disk IOPS usage for details on how charges are calculated.

Provisioned Disk Throughput (optional) Read Replicas inherit any additional provisioned Disk Throughput from the primary database. Refer to Manage Disk Throughput usage for details on how charges are calculated.

IPv4 (optional) If the primary database has a configured IPv4 address, its Read Replicas are also assigned one, with charges for each. Refer to Manage IPv4 usage for details on how charges are calculated.

Compute incurred by Read Replicas is shown as "Replica Compute Hours" on your invoice. Disk Size, Disk IOPS, Disk Throughput and IPv4 are not shown separately for Read Replicas and are rolled up into the project.

The project has one Read Replica and no IPv4 and no additional Disk IOPS and Disk Throughput configured.

The project has two Read Replicas and IPv4 and additional Disk IOPS and Disk Throughput configured.

No, Compute Credits do not apply to Read Replica Compute.

---

## Install | Supabase Docs

**URL:** https://supabase.com/docs/guides/cron/install

**Contents:**
- Install
- Uninstall#

Install the Supabase Cron Postgres Module to begin scheduling recurring Jobs.

Uninstall Supabase Cron by disabling the pg_cron extension:

Disabling the pg_cron extension will permanently delete all Jobs.

**Examples:**

Example 1 (unknown):
```unknown
1drop extension if exists pg_cron;
```

---

## Supabase Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/security

**Contents:**
- Supabase Security
- Compliance
- Platform configuration
- Product configuration

Supabase is a hosted platform which makes it very simple to get started without needing to manage any infrastructure. The hosted platform comes with many security and compliance controls managed by Supabase.

Supabase is SOC 2 Type 2 compliant and regularly audited. All projects at Supabase are governed by the same set of compliance controls. The SOC 2 Compliance Guide explains Supabase's SOC 2 responsibilities and controls in more detail.

The HIPAA Compliance Guide explains Supabase's HIPAA responsibilities. Additional security and compliance controls for projects that deal with electronic Protected Health Information (ePHI) and require HIPAA compliance are available through the HIPAA add-on.

As a hosted platform, Supabase provides additional security controls to further enhance the security posture depending on organizations' own requirements or obligations.

These can be found under the dedicated security page under organization settings. And are described in greater detail here.

Each product offered by Supabase comes with customizable security controls and these security controls help ensure that applications built on Supabase are secure, compliant, and resilient against various threats.

The security configuration guides provide detailed information for configuring individual products.

---

## Manage Egress usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/egress

**Contents:**
- Manage Egress usage
- What you are charged for#
  - Database Egress#
  - Auth Egress#
  - Storage Egress#
  - Edge Functions Egress#
  - Realtime Egress#
  - Shared pooler Egress#
  - Log Drain Egress#
  - Cached Egress#

You are charged for the network data transmitted out of the system to a connected client. Egress is incurred by all services - Database, Auth, Storage, Edge Functions, Realtime and Log Drains.

Data sent to the client when retrieving data stored in your database.

Example: A user views their order history in an online shop. The client application requests the database to retrieve the user's past orders. The order data is sent back to the client, contributing to Database Egress.

There are various ways to interact with your database, such as through the PostgREST API using one of the client SDKs or via the Supavisor connection pooler. On the Supabase Dashboard, Egress from the PostgREST API is labeled as Database Egress, while Egress through Supavisor is labeled as Shared Pooler Egress.

Data sent from Supabase Auth to the client while managing your application's users. This includes actions like signing in, signing out, or creating new users, e.g. via the JavaScript Client SDK.

Example: A user signs in to an online shop. The client application requests the Supabase Auth service to authenticate and authorize the user. The session data, including authentication tokens and user profile details, is sent back to the client, contributing to Auth Egress.

Data sent from Supabase Storage to the client when retrieving assets. This includes actions like downloading files, images, or other stored content, e.g. via the JavaScript Client SDK.

Example: A user downloads an invoice from an online shop. The client application requests Supabase Storage to retrieve the PDF file from the storage bucket. The file is sent back to the client, contributing to Storage Egress.

Data sent to the client when executing Edge Functions.

Example: A user completes a checkout process in an online shop. The client application triggers an Edge Function to process the payment and confirm the order. The confirmation response, along with any necessary details, is sent back to the client, contributing to Edge Functions Egress.

Data pushed to clients via Supabase Realtime for subscribed events.

Example: When a user views a product page in an online shop, their client subscribes to real-time inventory updates. As stock levels change, Supabase Realtime pushes updates to all subscribed clients, contributing to Realtime Egress.

Data sent to the client when using the shared connection pooler (Supavisor) to access your database. When using the shared connection pooler, we do not count database egress, as this would otherwise count double (Database -> Shared Pooler + Shared Pooler -> Client).

Example: You are using our shared connection pooler and you query a list of invoices in your backend. The data returned from that query is contributing to Shared Pooler Egress.

Data pushed to the connected log drain.

Example: You set up a log drain, each log sent to the log drain is considered egress. You can toggle the GZIP option to reduce egress, in case your provider supports it.

Cached and uncached egress have independent quotas and independent pricing. Cached egress is egress that is served from our CDN via cache hits. Cached egress is typically incurred for storage through our Smart CDN.

Egress is charged by gigabyte. Charges apply only for usage exceeding your subscription plan's quota. This quota is called the Unified Egress Quota because it can be used across all services (Database, Auth, Storage etc.).

Usage is shown as "Egress GB" and "Cached Egress GB" on your invoice.

$0.09 per GB per month for uncached egress, $0.03 per GB per month for cached egress. You are only charged for usage exceeding your subscription plan's quota.

The organization's Egress usage is within the quota, so no charges for Egress apply.

The organization's Egress usage exceeds the uncached egress quota by 50 GB and the cached egress quota by 550 GB, incurring charges for this additional usage.

You can view Egress usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Total Egress section, you can see the usage for the selected time period. Hover over a specific date to view a breakdown by service. Note that this includes the cached egress.

Separately, you can see the cached egress right below:

To better understand your Egress usage, identify what’s driving the most traffic. Check the most frequent database queries, or analyze the most requested API paths to pinpoint high-egress endpoints.

On the Advisors Query performance view you can see the most frequent queries and the average number of rows returned.

In the Logs Explorer you can access Edge Logs, and review the top paths to identify heavily queried endpoints. These logs currently do not include response byte data. That data will be available in the future too.

---

## Control your costs | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/cost-control

**Contents:**
- Control your costs
- Spend Cap#
  - What happens when the Spend Cap is on?#
  - What happens when the Spend Cap is off?#
  - Usage items covered by the Spend Cap#
  - Usage items not covered by the Spend Cap#
  - What the Spend Cap is not#
  - Configure the Spend Cap#
- Keep track of your usage and costs#

The Spend Cap determines whether your organization can exceed your subscription plan's quota for any usage item. Scenarios that could lead to high usage—and thus high costs—include system attacks or bugs in your software. The Spend Cap can protect you from these unexpected costs for certain usage items.

This feature is available only with the Pro Plan. However, you will not be charged while using the Free Plan.

After exceeding the quota for a usage item, further usage of that item is disallowed until the next billing cycle. You don't get charged for over-usage but your services will be restricted according to our Fair Use Policy if you consistently exceed the quota.

Note that only certain usage items are covered by the Spend Cap.

Your projects will continue to operate after exceeding the quota for a usage item. Any additional usage will be charged based on the item's cost per unit, as outlined on the pricing page.

When the Spend Cap is off, we recommend monitoring your usage and costs on the organization's usage page.

Usage items that are predictable and explicitly opted into by the user are excluded.

The Spend Cap doesn't allow for fine-grained cost control, such as setting budgets for specific usage item or receiving notifications when certain costs are reached. We plan to make cost control more flexible in the future.

You can configure the Spend Cap when creating an organization on the Pro Plan or at any time in the Cost Control section of the organization's billing page.

You can monitor your usage on the organization's usage page. The Upcoming Invoice section of the organization's billing page shows your current spending and provides an estimate of your total costs for the billing cycle based on your usage.

---

## Secure configuration of Supabase platform | Supabase Docs

**URL:** https://supabase.com/docs/guides/security/platform-security

**Contents:**
- Secure configuration of Supabase platform
- Available controls#
  - Enforce multi-factor authentication (MFA)#
  - SSO for organizations#
  - Postgres SSL enforcement#
  - Network restrictions#
  - PrivateLink#

Secure configuration of Supabase platform

The Supabase hosted platform provides a secure by default configuration. Some organizations may however require further security controls to meet their own security policies or compliance requirements.

Access to additional security controls can be found under the security tab for organizations.

Additional security controls are under active development. Any changes will be published here and in our changelog.

Organization owners can choose to enforce MFA for all team members.

For configuration information, see Enforce MFA on Organization

Supabase offers single sign-on (SSO) as a login option to provide additional account security for your team. This allows company administrators to enforce the use of an identity provider when logging into Supabase.

For configuration information, see Enable SSO for Your Organization.

Supabase projects support connecting to the Postgres DB without SSL enforced to maximize client compatibility. For increased security, you can prevent clients from connecting if they're not using SSL.

For configuration information, see Postgres SSL Enforcement

Controlling this at the organization level is on our roadmap.

Each Supabase project comes with configurable restrictions on the IP ranges that are allowed to connect to Postgres and its pooler ("your database"). These restrictions are enforced before traffic reaches the database. If a connection is not restricted by IP, it still needs to authenticate successfully with valid database credentials.

For configuration information, see Network Restrictions

Controlling this at the organization level is on our roadmap.

PrivateLink provides enterprise-grade private network connectivity between your AWS VPC and your Supabase database using AWS VPC Lattice. This eliminates exposure to the public internet by creating a secure, private connection that keeps your database traffic within the AWS network backbone.

For configuration information, see PrivateLink

PrivateLink is currently in alpha and available exclusively to Enterprise customers.

---

## Supabase Docs

**URL:** https://supabase.com/docs

**Contents:**
- Supabase Documentation
- Getting Started
- Products
- Postgres Modules
      - AI & Vectors
      - Cron
      - Queues
- Client Libraries
      - Javascript
      - Flutter

Learn how to get up and running with Supabase through tutorials, APIs and platform resources.

Set up and connect a database in just a few minutes.

Bring your existing data, auth and storage to Supabase following our migration guides.

Get started with self-hosting Supabase.

---

## Manage Disk IOPS usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/disk-iops

**Contents:**
- Manage Disk IOPS usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Pricing#
  - General purpose disks (gp3)#
  - High performance disks (io2)#
- Billing examples#
  - Gp3#
  - Io2#

Manage Disk IOPS usage

Each database has a dedicated disk, and you are charged for its provisioned disk IOPS. However, unless you explicitly opt in for additional IOPS, no charges apply.

Refer to our disk guide for details on how disk IOPS, disk throughput, disk size, disk type and compute size interact, along with their limitations and constraints.

Launching a Read Replica creates an additional database with its own dedicated disk. Read Replicas inherit the primary database's disk IOPS settings. You are charged for the provisioned IOPS of the Read Replica. Refer to Manage Read Replica usage for details on billing.

Disk IOPS is charged by IOPS-Hrs. 1 IOPS-Hr represents 1 IOPS being provisioned for 1 hour. For example, having 10 IOPS provisioned for 5 hours results in 50 IOPS-Hrs (10 IOPS × 5 hours).

Usage is shown as "Disk IOPS-Hrs" on your invoice.

Pricing depends on the disk type, with type gp3 being the default.

$0.00003288 per IOPS-Hr ($0.024 per IOPS per month). gp3 disks come with a default IOPS of 3,000. You are only charged for provisioned IOPS exceeding these 3,000 IOPS.

$0.000163 per IOPS-Hr ($0.119 per IOPS per month). Unlike general purpose disks, high performance disks are billed from the first provisioned IOPS.

Project 1 doesn't exceed the included IOPS, so no charges for IOPS apply. Project 2 exceeds the included IOPS by 600, incurring charges for this additional usage.

This disk type is billed from the first IOPS provisioned, meaning for 8000 IOPS.

---

## Manage Disk Throughput usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/disk-throughput

**Contents:**
- Manage Disk Throughput usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Pricing#
  - General purpose disks (gp3)#
  - High performance disks (io2)#
- Billing examples#
  - No additional throughput configured#
  - Additional throughput configured#

Manage Disk Throughput usage

Each database has a dedicated disk, and you are charged for its provisioned disk throughput. However, unless you explicitly opt in for additional throughput, no charges apply.

Refer to our disk guide for details on how disk throughput, disk IOPS, disk size, disk type and compute size interact, along with their limitations and constraints.

Launching a Read Replica creates an additional database with its own dedicated disk. Read Replicas inherit the primary database's disk throughput settings. You are charged for the provisioned throughput of the Read Replica.

Disk throughput is charged by MB/s-Hrs (MB/s stands for megabytes per second). 1 MB/s-Hr represents disk throughput of 1 MB/s being provisioned for 1 hour. For example, having 10 MB/s provisioned for 5 hours results in 50 MB/s-Hrs (10 MB/s × 5 hours).

Usage is shown as "Disk Throughput MB/s-Hrs" on your invoice.

Pricing depends on the disk type, with type gp3 being the default.

$0.00013 per MB/s-Hr ($0.095 per MB/s per month). gp3 disks come with a baseline throughput of 125 MB/s. You are only charged for provisioned throughput exceeding these 125 MB/s.

There are no charges. Throughput scales with IOPS at no additional cost.

---

## Your monthly invoice | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/your-monthly-invoice

**Contents:**
- Your monthly invoice
- Billing cycle#
- Your invoice explained#
  - Fixed fees#
  - Usage based fees#
  - Discounted line items#
    - Compute Credits#
  - Example invoice#
  - Why is my invoice more than $25?#
- How to settle your invoices#

When you sign up for a paid plan you get charged once a month at the beginning of the billing cycle. A billing cycle starts with the creation of a Supabase organization. If you create an organization on the sixth of January your billing cycle resets on the sixth of each month. If the anchored day is not present in the current month, then the last day of the month is used.

When your billing cycle resets an invoice gets issued. That invoice contains line items from both the current and the previous billing cycle. Fixed fees for the current billing cycle, usage based fees for the previous billing cycle.

Fixed fees are independent of usage and paid in-advance. Whether you have one or several projects, hundreds or millions of active users, the fee is always the same, and doesn't vary. Examples are the subscription fee, the fee for HIPAA and for priority support.

Fees vary depending on usage and are paid in arrears. The more usage you have, the higher the fee. Examples are fees for monthly active users and storage size.

Paid plans come with a usage quota for certain line items. You only pay for usage that goes beyond the quota. The quota for Storage for example is 100 GB. If you use 105 GB, you pay for 5 GB. If you use 95 GB, you pay nothing. This quota is declared as a discount on your invoice.

Paid plans come with $10 in Compute Credits per month. This suffices for a single project using a Nano or Micro compute instance. Every additional project adds compute fees to your monthly invoice though.

The following invoice was issued on January 6, 2025 with the previous billing cycle from December 6, 2024 - January 5, 2025, and the current billing cycle from January 6 - February 5, 2025.

The amount due of your invoice being higher than the $25 subscription fee for the Pro Plan can have several reasons.

Monthly invoices are auto-collected by charging the payment method marked as "active" for an organization.

If your payment fails, Supabase retries the charge several times. We send you a Payment Failure email with the reason for the failure. Follow the steps outlined in this email. You can manually trigger a charge at any time via

Your invoice is sent to you via email. You can also find your invoices on the organization's invoices page.

---

## Telemetry | Supabase Docs

**URL:** https://supabase.com/docs/guides/telemetry

**Contents:**
- Telemetry

Telemetry helps you understand what’s happening inside your app by collecting logs, metrics, and traces.

Supabase is working towards full support for the OpenTelemetry standard, making it easier to integrate with observability tools.

This section provides guidance on telemetry in Supabase, including how to work with Supabase Logs.

---

## Supabase Docs | Troubleshooting

**URL:** https://supabase.com/docs/guides/troubleshooting?tags=memory

---

## SOC 2 Compliance and Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/security/soc-2-compliance

**Contents:**
- SOC 2 Compliance and Supabase
- Meeting compliance requirements
  - Supabase responsibilities#
  - Customer responsibilities#
  - Shared responsibilities#
- Frequently asked questions#
- Resources#

SOC 2 Compliance and Supabase

Supabase is Systems and Organization Controls 2 (SOC 2) Type 2 compliant and is assessed annually to ensure continued adherence to the SOC 2 security framework. SOC 2 assesses Supabase’s adherence to, and implementation of, controls governing the security, availability, processing integrity, confidentiality, and privacy on the Supabase platform. These controls define requirements for the management and storage of customer data on the platform. These controls applied to Supabase, as a service provider, serve two customer data environments.

The first environment is the customer relationship with Supabase, this refers to the data Supabase has on a customer of the platform. All billing, contact, usage and contract information is managed and stored according to SOC 2 requirements.

The second environment is the backend as a service (the product) that Supabase provides to customers. Supabase implements the controls from the SOC 2 framework to ensure the security of the platform, which hosts the backend as a service (the product), including the Postgres Database, Storage, Authentication, Realtime, Edge Functions and Data API features. Supabase can assert that the environment hosting customer data, stored within the product, adheres to SOC 2 requirements. And the management and storage of data within this environment (the product) is strictly controlled and kept secure.

Supabase’s SOC 2 compliance does not transfer to environments outside of the Supabase product or Supabase’s control. This is known as the security or compliance boundary and forms part of the Shared Responsibility Model that Supabase and their customers enter into.

SOC 2 does not cover, nor is it a substitute for, compliance with the Health Insurance Portability and Accountability Act (HIPAA). Organizations must have a signed Business Associate Agreement (BAA) with Supabase and have the HIPAA add-on enabled when dealing with Protected Health Information (PHI).

Our HIPAA documentation provides more information about the responsibilities and requirements for HIPAA on Supabase.

SOC 2 compliance is a critical aspect of data security for Supabase and our customers. Being fully SOC 2 compliant is a shared responsibility and here’s a breakdown of the responsibilities for both parties:

In summary, SOC 2 compliance involves a shared responsibility between Supabase and our customers to ensure the security and integrity of data. Supabase, as a provider, must implement and maintain robust security measures, customers must perform due diligence and monitor Supabase's compliance status, while also implement their own compliance controls to protect their sensitive information.

How often is Supabase SOC 2 audited?

Supabase has obtained SOC 2 Type 2 certification, which means Supabase's controls are fully audited annually. The auditor's reports on these examinations are issued as soon as they are ready after the audit. Supabase makes the SOC 2 Type 2 report available to Enterprise and Team Plan customers. The audit report covers a rolling 12-month window, known as the audit period, and runs from 1 March to 28 February of the next calendar year.

How to obtain Supabase's SOC 2 Type 2 report?

To access the SOC 2 Type 2 report, you must be a Enterprise or Team Plan Supabase customer. The report is downloadable from the Legal Documents section in the organization dashboard.

Why does it matter that Supabase is SOC 2 Compliant?

SOC 2 is used to assert that controls are in place to ensure the proper management and storage of data. SOC 2 provides a framework for measuring how secure a service provider is and re-evaluates the provider on an annual basis. This provides the confidence and assurance that data stored within the Supabase platform is correctly secured and managed.

If Supabase’s SOC 2 does not transfer to the customer, why does it matter that Supabase has SOC 2?

Even though Supabase’s SOC 2 compliance does not transfer outside of the product, it does provide the assurance that all data within the product is correctly managed and stored. Supabase can assert that only authorized persons have access to the data, and security controls are in place to prevent, detect and respond to data intrusions. This forms part of a customer’s own adherence to the SOC 2 framework and relieves part of the burden of data management and storage on the customer. In many organizations' security and risk departments require all vendors or sub-processors to be SOC 2 compliant.

What is the security or compliance boundary?

This defines the boundary or border between Supabase and customer responsibility for data security within the Shared Responsibility Model. Customer data stored within the Supabase product, on the Supabase side of the security boundary, is managed and secured by Supabase. Supabase ensures the safe handling and storage of data within this environment. This includes controls for preventing unauthorized access, monitoring data access, alerting, data backups and redundancy. Data on the customer side of the boundary, the data that enters and leaves the Supabase product, is the responsibility of the customer. Management and possible storage of such data outside of Supabase should be performed by the customer, and any security and compliance controls are the responsibility of the customer.

We have strong data residency requirements. Does Supabase SOC 2 cover data residency?

While SOC 2 itself does not mandate specific data residency requirements, organizations may still need to comply with other regulatory frameworks, such as GDPR, that do have such requirements. Ensuring projects are deployed in the correct region is a customer responsibility as each Supabase project is deployed into the region the customer specifies at creation time. All data will remain within the chosen region. Read replicas can be created for multi-region availability, it remains the customer's responsibility to ensure regions chosen for read replicas are within the geographic area required by any additional regulatory frameworks.

Does SOC 2 cover health related data (HIPAA)?

SOC 2 is non-industry specific and provides a framework for the security and privacy of data. This is however not sufficient in most cases when dealing with Protected Healthcare Information (PHI), which requires additional privacy and legal controls. When dealing with PHI in the United States or for United States customers, HIPAA is mandatory.

---

## Get set up for billing | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/get-set-up-for-billing

**Contents:**
- Get set up for billing
- Payments#
  - Ensuring valid credit card details#
  - Alternatives to monthly charges#
- Billing details#

Get set up for billing

Correct billing settings are essential for ensuring successful payment processing and uninterrupted services. Additionally, it's important to configure all invoicing-related data early, as this information cannot be changed once an invoice is issued. Review these key points to ensure everything is set up correctly from the start.

Paid plans require a credit card to be on file. Ensure the correct credit card is set as active and

For more information on managing payment methods, see Manage your payment methods.

Instead of having your credit card charged every month, you can make an upfront payment by topping up your credit balance.

You may want to consider this option to avoid issues with recurring payments, gain more control over how often your credit card is charged, and potentially make things easier for your accounting department.

For more information on credits and credit top-ups, see the Credits page.

Billing details cannot be changed once an invoice is issued, so it's crucial to configure them correctly from the start.

You can update your billing email address, billing address and tax ID on the organization's billing page.

---

## Compute and Disk | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/compute-and-disk

**Contents:**
- Compute and Disk
- Compute#
      - Nano instances in paid plan organizations
  - Dedicated vs shared CPU#
  - Compute upgrades #
- Disk#
  - Compute size#
  - Choosing the right compute instance for consistent disk performance#
  - Provisioned disk throughput and IOPS#
  - Disk types#

Every project on the Supabase Platform comes with its own dedicated Postgres instance.

The following table describes the base instances, Nano (free plan) and Micro (paid plans), with additional compute instance sizes available if you need extra performance when scaling up.

In paid organizations, Nano Compute are billed at the same price as Micro Compute. It is recommended to upgrade your Project from Nano Compute to Micro Compute when it's convenient for you. Compute sizes are not auto-upgraded because of the downtime incurred. See Supabase Pricing for more information. You cannot launch Nano instances on paid plans, only Micro and above - but you might have Nano instances after upgrading from Free Plan.

Compute sizes can be changed by first selecting your project in the dashboard here and the upgrade process will incur downtime.

We charge hourly for additional compute based on your usage. Read more about usage-based billing for compute.

All Postgres databases on Supabase run in isolated environments. Compute instances smaller than Large compute size have CPUs which can burst to higher performance levels for short periods of time. Instances bigger than Large have predictable performance levels and do not exhibit the same burst behavior.

Compute instance changes are usually applied with less than 2 minutes of downtime, but can take longer depending on the underlying Cloud Provider.

When considering compute upgrades, assess whether your bottlenecks are hardware-constrained or software-constrained. For example, you may want to look into optimizing the number of connections or examining query performance. When you're happy with your Postgres instance's performance, then you can focus on additional compute resources. For example, you can load test your application in staging to understand your compute requirements. You can also start out on a smaller tier, create a report in the Dashboard to monitor your CPU utilization, and upgrade as needed.

Supabase databases are backed by high performance SSD disks. The effective performance depends on a combination of all the following factors:

The disk size and the disk type dictate the maximum IOPS and throughput that can be provisioned. The effective IOPS is the lower of the IOPS supported by the compute size or the provisioned IOPS of the disk. Similarly, the effective throughout is the lower of the throughput supported by the compute size and the provisioned throughput of the disk.

The following sections explain how these attributes affect disk performance.

The compute size of your project sets the upper limit for disk throughput and IOPS. The table below shows the limits for each instance size. For instance, an 8XL compute instance has a maximum throughput of 9,500 Mbps and a maximum IOPS of 40,000.

Smaller compute instances like Nano, Micro, Small, and Medium have baseline performance levels that can occasionally be exceeded for short periods of time. If it does exceed the baseline, you should consider upgrading your instance size for a more reliable performance.

Larger compute instances (4XL and above) are designed for sustained, high performance with specific IOPS and throughput limits which you can configure. If you hit your IOPS or throughput limit, throttling will occur.

If you need consistent disk performance, choose the 4XL or larger compute instance. If you're unsure of how much throughput or IOPS your application requires, you can load test your project and inspect these metrics in the Dashboard. If the Disk IO % consumed stat is more than 1%, it indicates that your workload has exceeded the baseline IO throughput during the day. If this metric goes to 100%, the workload has used up all available disk IO budget. Projects that use any disk IO budget are good candidates for upgrading to a larger compute instance with higher throughput.

The default disk type is gp3, which comes with a baseline throughput of 125 MB/s and a default IOPS of 3,000. You can provision additional IOPS and throughput from the Database Settings page, but keep in mind that the effective IOPS and throughput will be limited by the compute instance size. This requires Large compute size or above.

Be aware that increasing IOPS or throughput incurs additional charges.

When selecting your disk, it's essential to focus on the performance needs of your workload. Here's a comparison of our available disk types:

For general, day-to-day operations, gp3 should be more than enough. If you need high throughput and IOPS for critical systems, io2 will provide the performance required.

Compute instance size changes will not change your selected disk type or disk size, but your IO limits may change according to what your selected compute instance size supports.

Replication Slots and WAL Senders are used to enable Postgres Replication. Each compute instance also has limits on the maximum number of database connections and connection pooler clients it can handle.

The maximum number of replication slots, WAL senders, database connections, and pooler clients depends on your compute instance size, as follows:

As mentioned in the Postgres documentation, setting max_replication_slots to a lower value than the current number of replication slots will prevent the server from starting. If you are downgrading your compute instance, ensure that you are using fewer slots than the maximum number of replication slots available for the new compute instance.

Database size for each compute instance is the default recommendation but the actual performance of your database has many contributing factors, including resources available to it and the size of the data contained within it. See the shared responsibility model for more information. ↩

Compute resources on the Free plan are subject to change. ↩

Database max connections are recommended values and can be customized via max_connections depending on your use case. Be aware of these considerations before modifying. ↩

---

## Access Control | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/access-control

**Contents:**
- Access Control
- Manage organization members#
  - Viewing organization members using the Management API#
  - Transferring ownership of an organization#
  - Organization scoped roles vs project scoped roles#
  - Organization permissions across roles#
  - Project permissions across roles#
- Footnotes#

Supabase provides granular access controls to manage permissions across your organizations and projects.

For each organization and project, a member can have one of the following roles:

Read-Only role is only available on the Team and Enterprise plans.

When you first create an account, a default organization is created for you and you'll be assigned as the Owner. Any organizations you create will assign you as Owner as well.

To invite others to collaborate, visit your organization's team settings to send an invite link to another user's email. The invite is valid for 24 hours. For project scoped roles, you may only assign a role to a single project for the user when sending the invite. You can assign roles to multiple projects after the user accepts the invite.

Invites sent from a SAML SSO account can only be accepted by another SAML SSO account from the same identity provider.

This is a security measure to prevent accidental invites to accounts not managed by your enterprise's identity provider.

You can also view organization members using the Management API:

Each Supabase organization must have at least one owner. If your organization has other owners then you can relinquish ownership and leave the organization by clicking Leave team in your organization's team settings.

Otherwise, you'll need to invite a user as Owner, and they need to accept the invitation, or promote an existing organization member to Owner before you can leave the organization.

Project scoped roles are only available on the Team and Enterprise plans.

Each member in the organization can be assigned a role that is scoped either to the entire organization or to specific projects.

This allows for more granular control, ensuring that users only have visibility and access to the projects relevant to their role.

The table below shows the actions each role can take on the resources belonging to the organization.

The table below shows the actions each role can take on the resources belonging to the project.

Available on the Team and Enterprise Plans. ↩

Sending anonymous data to OpenAI is opt in and can improve Studio AI Assistant's responses. ↩

Invites sent from a SSO account can only be accepted by another SSO account coming from the same identity provider. This is a security measure that prevents accidental invites to accounts not managed by your company's enterprise systems. ↩

Available on the Team and Enterprise Plans. ↩

Listed permissions are for the API and Dashboard. ↩

Read-Only role is able to access secrets. ↩

Limited to executing SELECT queries. SQL Query Snippets run by the Read-Only role are run against the database using the supabase_read_only_user. This role has the predefined Postgres role pg_read_all_data. ↩

**Examples:**

Example 1 (unknown):
```unknown
1# Get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"3export ORG_ID="your-organization-id"45# List organization members6curl "https://api.supabase.com/v1/organizations/$ORG_ID/members" \7  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN"
```

---

## HIPAA Compliance and Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/security/hipaa-compliance

**Contents:**
- HIPAA Compliance and Supabase
  - Customer responsibilities#
  - Supabase responsibilities#
- Staying compliant and secure#
- Frequently asked questions#
- Resources#

HIPAA Compliance and Supabase

The Health Insurance Portability and Accountability Act (HIPAA) is a comprehensive law that protects individuals' health information while ensuring the continuity of health insurance coverage. It sets standards for privacy and security that must be followed by all entities that handle Protected Health Information (PHI), also known as electronic PHI (ePHI). HIPAA is specific to the United States, however many countries have similar or laws already in place or under legislation.

Under HIPAA, both covered entities and business associates have distinct responsibilities to ensure the protection of PHI. Supabase acts as a business associate for customers (the covered entity) who wish to provide healthcare related services. As a business associate, Supabase has a number of obligations and has undergone auditing of the security and privacy controls that are in place to meet these. Supabase has signed a Business Associate Agreement (BAA) with all of our vendors who would have access to ePHI, such as AWS, and ensure that we follow their terms listed in the agreements. Similarly when a customer signs a BAA with us, they have some responsibilities they agree to when using Supabase to store PHI.

The hosted Supabase platform has the necessary controls to meet HIPAA requirements. These controls are not supported out of the box in self-hosted Supabase. HIPAA controls extend further than the Supabase product, encompassing legal agreements (BAAs) with providers, operating controls and policies. Achieving HIPAA compliance with self-hosted Supabase is out of scope for this documentation and you should consult your auditor for further guidance.

Covered entities (the customer) are organizations that directly handle PHI, such as health plans, healthcare clearinghouses, and healthcare providers that conduct certain electronic transactions.

Supabase as the business associate, and the vendors used by Supabase, are the entities that perform functions or activities on behalf of the customer.

Compliance is a continuous process and should not be treated as a point-in-time audit of controls. Supabase applies all the necessary privacy and security controls to ensure HIPAA compliance at audit time, but also has additional checks and monitoring in place to ensure those controls are not disabled or altered in between audit periods. Customers commit to doing the same in their HIPAA environments. Supabase provides a growing set of checks that warn customers of changes to their projects that disable or weaken HIPAA required controls. Customers will receive warnings and guidance via the Security Advisor, however the responsibility of applying the recommended controls falls directly to the customer.

Our shared responsibility model document discusses both HIPAA and general data management best practices, how this responsibility is shared between customers and Supabase, and how to stay compliant.

What is the difference between SOC 2 and HIPAA?

Both are frameworks for protecting sensitive data, however they serve two different purposes. They share many security and privacy controls and meeting the controls of one normally means being close to complying with the other.

The main differentiator comes down to purpose and scope.

Are Supabase HIPAA environments also SOC 2 compliant?

Yes. Supabase applies the same SOC 2 controls to all environments, with additional controls being applied to HIPAA environments.

How often is Supabase audited?

Supabase undergoes annual audits. The HIPAA controls are audited during the same audit period as the SOC 2 controls.

---

## About billing on Supabase | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/billing-on-supabase

**Contents:**
- About billing on Supabase
- Subscription plans#
  - Free Plan#
  - Paid plans#
- Organization-based billing#
- Costs#
  - Compute costs for projects#
- Variable Usage Fees and Quotas#
- Project add-ons#

About billing on Supabase

Supabase offers different subscription plans—Free, Pro, Team, and Enterprise. For a closer look at each plan's features and pricing, visit our pricing page.

The Free Plan helps you get started and explore the platform. You are granted two free projects. The project limit applies across all organizations where you are an Owner or Administrator. This means you could have two Free Plan organizations with one project each, or one Free Plan organization with two projects. Paused projects do not count towards your free project limit.

Upgrading your organization to a paid plan provides additional features, and you receive a higher usage quota. You unlock the benefits of the paid plan for all projects within your organization - for example, no projects in your Pro Plan organization will be paused.

Supabase bills separately for each organization. Each organization has its own subscription, including a unique subscription plan (Free, Pro, Team, or Enterprise), payment method, billing cycle, and invoices.

Different plans cannot be mixed within a single organization. For example, you cannot have both a Pro Plan project and a Free Plan project in the same organization. To have projects on different plans, you must create separate organizations. See Project Transfers if you need to move a project to a different organization.

Monthly costs for paid plans include a fixed subscription fee based on your chosen plan and variable usage fees. To learn more about billing and cost management, refer to the following resources.

An organization can have multiple projects. Each project includes a dedicated Postgres instance running on its own server. You are charged for the Compute resources of that server, independent of your database usage.

Each project you launch increases your monthly Compute costs.

Read more about Compute costs.

Each subscription plan includes a built-in quota for some selected usage items, such as Egress, Storage Size, or Edge Function Invocations. This quota represents your free usage allowance. If you stay within it, you incur no extra charges for these items. Only usage beyond the quota is billed as overage.

For usage items without a quota, such as Compute or Custom Domains, you are charged for your entire usage.

The quota is applied to your entire organization, independent of how many projects you launch within that organization. For billing purposes, we sum the usage across all projects in a monthly invoice.

You can find a detailed breakdown of all usage items and how they are billed on the Manage your usage page.

While your subscription plan applies to your entire organization and is charged only once, you can enhance individual projects by opting into various add-ons.

---

## Manage Branching usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/branching

**Contents:**
- Manage Branching usage
- What you are charged for#
- How charges are calculated#
  - Usage on your invoice#
- Pricing#
- Billing examples#
- View usage#
- Optimize usage#
- FAQ#
  - Do Compute Credits apply to Branching Compute?#

Manage Branching usage

Each Preview branch is a separate environment with all Supabase services (Database, Auth, Storage, etc.). You're charged for usage within that environment—such as Compute, Disk Size, Egress, and Storage—just like the project you branched from.

Usage by Preview branches counts toward your subscription plan's quota.

Refer to individual usage items for details on how charges are calculated. Branching charges are the sum of all these items.

Compute incurred by Preview branches is shown as "Branching Compute Hours" on your invoice. Other usage items are not shown separately for branches and are rolled up into the project.

There is no fixed fee for a Preview branch. You only pay for the usage it incurs. A branch running on the default Micro Compute size starts at $0.01344 per hour.

The project has a Preview branch "XYZ", that runs for 30 hours, incurring Compute and Egress costs. Disk Size usage remains within the 8 GB included in the subscription plan, so no additional charges apply.

You can view Branching usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Usage Summary section, you can see how many hours your Preview branches existed during the selected time period. Hover over "Branching Compute Hours" for a detailed breakdown.

No, Compute Credits do not apply to Branching Compute.

---

## HIPAA Projects | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/hipaa-projects

**Contents:**
- HIPAA Projects
- Configuring a HIPAA project#

You can use Supabase to store and process Protected Health Information (PHI). If you want to start developing healthcare apps on Supabase, reach out to the Supabase team here to sign the Business Associate Agreement (BAA).

Organizations must have a signed BAA with Supabase and have the Health Insurance Portability and Accountability Act (HIPAA) add-on enabled when dealing with PHI.

When the HIPAA add-on is enabled on an organization, projects within the organization can be configured as High Compliance. This configuration can be found in the General Project Settings page of the dashboard. Once enabled, additional security checks will be run against the project to ensure the deployed configuration is compliant. These checks are performed on a continual basis and security warnings will appear in the Security Advisor if a non-compliant setting is detected.

The required project configuration is outlined in the shared responsibility model for managing healthcare data.

Additional security checks and controls will be added as the security advisor is extended and additional security controls are made available.

---

## Credits | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/credits

**Contents:**
- Credits
- Credit balance#
  - What causes the credit balance to change?#
- Credit top-ups#
  - How to top up credits#
- Credit FAQ#
  - Will I get an invoice for the credits purchase?#
  - Can I transfer credits to another organization?#
  - Can I get a refund of my unused credits?#

Each organization has a credit balance. Credits are applied to future invoices to reduce the amount due. As long as the credit balance is greater than $0, credits will be used before charging your payment method on file.

You can find the credit balance on the organization's billing page.

Subscription plan downgrades: Upon subscription downgrade, any prepaid subscription fee will be credited back to your organization for unused time in the billing cycle. As an example, if you start a Pro Plan subscription on January 1 and downgrade to the Free Plan on January 15, your organization will receive about 50% of the subscription fee as credits for the unused time between January 15 and January 31.

Credit top-ups: You self-served a credit top-up or have signed an upfront credits deal with our growth team.

You can top up credits at any time, with a maximum of $2000 per top-up. These credits do not expire and are non-refundable. You may want to consider this option to avoid issues with recurring payments, gain more control over how often your credit card is charged, and potentially make things easier for your accounting department.

If you are interested in larger (> $2000) credit packages, reach out.

Yes, once the payment is confirmed, you will get a matching invoice that can be accessed through your organization's invoices page.

Yes, you can transfer credits to another organization. Submit a support ticket.

No, we do not provide refunds. Please refer to our Terms of Service.

---

## Manage your subscription | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-subscription

**Contents:**
- Manage your subscription
- Manage your subscription plan#
  - Upgrade#
  - Downgrade#
    - Credits upon downgrade#
    - Charges on downgrade#
  - Cancel subscription#
- Manage your payment methods#
  - Add a payment method#
  - Delete a payment method#

Manage your subscription

To change your subscription plan

Upgrades take effect immediately. During the process, you are informed of the associated costs.

If you still have credits in your account, we will use the credits first before charging your card.

Downgrades take effect immediately. During the process, you are informed of the implications.

Upon subscription downgrade, any prepaid subscription fee will be credited back to your organization for unused time in the billing cycle. These credits do not expire and will be applied to future invoices.

Example: If you start a Pro Plan subscription on January 1 and downgrade to the Free Plan on January 15, your organization will receive about 50% of the subscription fee as credits for the unused time between January 15 and January 31.

As stated in our Terms of Service, we do not offer refunds to the payment method on file.

When you downgrade from a paid plan to the Free Plan, you will get credits for the unused time on the paid plan. However, you will also be charged for any excessive usage in the billing cycle.

The plan line item (e.g. Pro Plan) gets charged upfront, whereas all usage charges get charged in arrears, as we only know your usage by the end of the billing cycle. Excessive usage is charged whenever a billing cycle resets, so either when your monthly cycle resets, or whenever you do a plan change.

If you got charged after downgrading to the Free Plan, you had excessive usage in the previous billing cycle. You can check your invoices to see what exactly you were charged for.

To cancel your subscription, go to your organization's billing settings, click "Change subscription plan" and select the Free Plan. The cancellation is immediate, refer to downgrade docs for full details.

Cancellations are fully self-serve. Your Free Plan subscription will run indefinitely unless you delete the organization through your organization's settings.

You can add multiple payment methods, but only one can be active at a time.

You can update your billing email address, billing address and tax ID on the organization's billing page.

Any changes made to your billing details will only be reflected in your upcoming invoices. Our payment provider cannot regenerate previous invoices.

---

## Manage Edge Function Invocations usage | Supabase Docs

**URL:** https://supabase.com/docs/guides/platform/manage-your-usage/edge-function-invocations

**Contents:**
- Manage Edge Function Invocations usage
- What you are charged for#
- How charges are calculated#
  - Example#
  - Usage on your invoice#
- Pricing#
- Billing examples#
  - Within quota#
  - Exceeding quota#
- View usage#

Manage Edge Function Invocations usage

You are charged for the number of times your functions get invoked, regardless of the response status code. Preflight (OPTIONS) requests are not billed.

Edge Function Invocations are billed using Package pricing, with each package representing 1 million invocations. If your usage falls between two packages, you are billed for the next whole package.

For simplicity, let's assume a package size of 1 million and a charge of $2 per package without a free quota.

Usage is shown as "Function Invocations" on your invoice.

$2 per 1 million invocations. You are only charged for usage exceeding your subscription plan's quota.

The organization's function invocations are within the quota, so no charges apply.

The organization's function invocations exceed the quota by 1.4 million, incurring charges for this additional usage.

You can view Edge Function Invocations usage on the organization's usage page. The page shows the usage of all projects by default. To view the usage for a specific project, select it from the dropdown. You can also select a different time period.

In the Edge Function Invocations section, you can see how many invocations your projects have had during the selected time period.

---
