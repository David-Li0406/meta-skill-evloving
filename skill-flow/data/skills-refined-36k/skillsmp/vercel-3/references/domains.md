# Vercel - Domains

**Pages:** 20

---

## Assigning a custom domain to an environment

**URL:** https://vercel.com/docs/domains/working-with-domains/add-a-domain-to-environment

**Contents:**
- Assigning a custom domain to an environment

---

## Troubleshooting domains

**URL:** https://vercel.com/docs/domains/troubleshooting

**Contents:**
- Troubleshooting domains
- Misconfigured domain issues
- Common DNS issues
  - Why are my DNS records taking so long to update?
  - IPv6 support
  - Syntax errors debugging
    - Using the domain as part of the Name argument
    - Absolute CNAME records
- Common Nameserver issues
  - Configuring nameservers for wildcard domains

There are many common reasons why your domain configuration may not be working. Check the following:

When you add a domain to Vercel that you have purchased from a third-party DNS provider, you may see an Invalid Configuration alert. There are many reasons why this could be the case:

Vercel is expecting either an record or a record. In your Project Settings under the Domain page, you’ll find the precise or record values tailored to your project and plan. Make sure to remove any outdated records from your DNS provider to prevent conflicts. Once your new records have been added, you can use the following commands on your Terminal to check the DNS records are correctly configured:

If you prefer a non-command-line interface, you can use a free online tool, such as Google Public DNS. If any of these results do not match what is expected, follow the steps to configure your domain.

DNS changes can take a while to propagate across the globe, depending on the previous DNS record TTL length. This may mean that certain regions can access your site as intended, while others wait until the DNS changes have reached them. Please allow some time for these changes to take effect. Changes to standard DNS records (A, CNAME, TXT, etc.) typically propagate quicker, but changing a domain’s nameservers can take up to 24–48 hours to fully propagate across the internet. During this time, different users may see different versions of your site depending on their local DNS caches. You can monitor this propagation using tools like DNSChecker or the dig command in your terminal.

For more information on propagation times for nameservers and other DNS records, see "How long will it take for my Vercel DNS records to update?"

Before changing your DNS records to point to Vercel, we recommend updating your existing DNS record to "lower" the TTL (for example 60 seconds) and waiting for the old TTL to expire. Lowering the current TTL and changing a DNS record after its TTL expiration period can ensure that you can quickly roll back the change if you encounter an issue. You can then increase the DNS record TTL to its original value once you confirm everything is working as expected.

While we allow the creation of AAAA records when using Vercel's nameservers, we do not support IPv6 yet. This means if you are adding a custom domain from a third-party, you won't be able to point an record to Vercel.

When working with DNS records, you may make minor errors in the syntax. These errors can be difficult to debug. Below is a list of common errors made when adding DNS records and the steps required to resolve them.

When you add a new DNS record to a domain, the Name field should use the prefix or location of the record. For , the name argument would be .

If you have already added a record with this, remove the record from the DNS Records section of the Domains tab, and add the record again without the domain as the Name argument.

When you add a custom domain with a subdomain to your project, we'll prompt you to add a CNAME DNS record in order to configure the domain. This record includes a period (.) at the end of the Value field. This is intentional to denote that it is an absolute, fully qualified domain name.

This means that when you add a new CNAME record to your DNS provider, you must copy the value exactly as it appears, including the period.

When you add any custom domain to your Vercel project you must configure the DNS records with your DNS provider so it can be used with your project. When you add a wildcard domain (such as ), you must use the Nameservers method.

This is because Vercel needs to be able to set DNS records in order to generate the wildcard certificates. The service that Vercel uses to generate the certificates requires us to verify the domain ownership by using the DNS-01 challenge method. By changing the nameservers, Vercel will handle the DNS-01 challenge for you automatically, and you don't need to update your verification DNS record upon your certificate renewal each time.

For more information, see Why must we use the Domain Nameservers method for Wildcard Domains on Vercel?

When you buy a new domain, you may want to also set up an email address with this domain. Vercel does not provide a mail service for domains purchased with or transferred into it. To learn how to set up email, see How do I send and receive emails with my Vercel purchased domain?

When you add your custom domain to a project and use Vercel's nameservers, you will need to add records to continue receiving email. To learn how to add records, see Why am I no longer receiving email after adding my domain to Vercel?

All domain purchases and renewals through Vercel are final and cannot be refunded once processed. For more information, see Can I get a refund for a domain purchased or renewed with Vercel?

When a domain purchase does not go through immediately, your payment method may show a temporary authorization — this is a pending hold, not a completed charge. It will be automatically released by your bank if the domain is not successfully registered.

If the purchase is processing, your domain will appear in the Domains tab with a “Pending” status. Most purchases complete within minutes, but some TLDs may take up to 5 days to finalize. There is no need to retry the purchase or contact support while the domain is pending. You will receive a confirmation email once the registration completes.

If verification is needed, you will receive an email with instructions from Vercel. You will also see an alert on your team's domain page, which you can access through the Domain Dashboard. From there, you can resend the verification email or update your registrant information and email address.

You will need to convert the domain to punycode in order to add it to your project. For example, a user looking to add a domain such as can do so in the form of .

ICANN forces domain registrars to wait 60 days:

If you transfer before this time, the transfer will fail. Besides this restriction, some DNS providers may further restrict domain transferring by default as a security measure, unless the owner explicitly turns off their protection setting. Please refer to the DNS provider's documentation for more details.

When you add an apex domain (e.g. ) to your project, Vercel provides you with details, including an IP address, to add as an record in your DNS configuration, as opposed to a record.

The main reason for that is the DNS RFC1034 (section 3.6.2) states that . Because an apex domain requires records and usually some other records, such as (for a mail service), adding a at the zone apex would violate this rule and likely cause an issue on your domain. Therefore, we encourage you to use an record at your zone apex instead.

When you configure an apex domain (example.com) as a custom domain for your project on Vercel, Vercel will be give you an IP address to add as an A record in your DNS configuration. Although this IP address resolves to a specific geographic location, it does not mean that when your users point to your domain, they will be sent to this specific geographic location to resolve the domain.

This is because Vercel uses Anycast IP addresses, which are shared across all regions. That means even if your users access your domain resolving to the same IP addresses from different geographic locations, they will be routed to the closest CDN region relative to your users, based on the BGP (Border Gateway Protocol).

When you add a domain to your project, Vercel checks if it is already associated with a Personal Account or Team. A domain can only be associated with one Personal Account or Team at a time.

The following table shows errors that can be encountered when adding a domain to your project:

There are many reasons why a certificate may not be generated. As the first starting point, we recommend testing your domain with:

For non-wildcard domains, we use HTTP-01 challenge by default, which Vercel handles automatically by intercepting the challenge requests from Let's Encrypt to your domain as long as the domain points to Vercel.

For wildcard domains, only DNS-01 challenge is supported, which Vercel requires you to use the nameservers method to handle DNS-01 challenge requests with Vercel's nameservers automatically.

Since we use Let's Encrypt for our automatic SSL certificates, you must add a record with the value if other records already exist on your domain.

You can check if your domain currently has any records by running the command on your terminal, or check with Google Public DNS (change the to and resolve).

For more information, see Why is my domain not automatically generating an SSL certificate?

An record allows Let's Encrypt to verify the domain ownership using DNS-01 challenge. This may exist on your apex or subdomains, so can be checked with or

If the domain was previously hosted on a different provider, and if the record resolves to something, please consider removing the DNS record. This will prevent any provider (other than the one in the DNS record) from provisioning certificates for that domain.

The /.well-known path is reserved and cannot be redirected or rewritten. Only Enterprise teams can configure custom SSL. Contact sales to learn more.

---

## Working with SSL Certificates

**URL:** https://vercel.com/docs/domains/working-with-ssl

**Contents:**
- Working with SSL Certificates
- Troubleshooting
- Related
    - Domains overview
    - Working with Domains
    - Working with DNS
    - Working with Nameservers
    - Troubleshooting Domains

An SSL certificate enables encrypted communication between user's browser and your web server to be encrypted. The certificate is installed on the web server and allows for website authentication and data encryption. This is particularly important if you are working with any sort of authentication and personal or financial data.

SSL certificates are issued from a certificate authority (CA) for each domain. While it is possible to create and upload your own custom certificate, Vercel will automatically try to generate a certificate for every domain once it is added to a project, regardless of if it was registered through Vercel or not. However, it will only work once the certificate validation request is successful, which happens once DNS records are added and propagated.

Vercel uses LetsEncrypt for certificates. For all non-wildcard domains, we use the HTTP-01 challenge method and providing the request can make it to Vercel, then our infrastructure will deal with it. For wildcard requests, we use the DNS-01 challenge method. This is why we require nameservers to be with Vercel to use wildcard domains - if the DNS isn't with us, we can't make the DNS record to approve it.

Issuing a certificate happens in the following way:

For information about when SSL certificate renewals happen, see When is the SSL Certificate on my Vercel Domain renewed?

The /.well-known path is reserved and cannot be redirected or rewritten. Only Enterprise teams can configure custom SSL. Contact sales to learn more.

To learn more about common SSL issues, see the troubleshooting doc.

Learn the concepts behind how domains work

Learn the concepts behind how domains work

Learn how domains work and the options Vercel provides for managing them.

Learn how domains work and the options Vercel provides for managing them.

Learn how DNS works in order to properly configure your domain.

Learn how DNS works in order to properly configure your domain.

Learn about nameservers and the benefits Vercel nameservers provide.

Learn about nameservers and the benefits Vercel nameservers provide.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

---

## Assigning a domain to a Git branch

**URL:** https://vercel.com/docs/domains/working-with-domains/assign-domain-to-a-git-branch

**Contents:**
- Assigning a domain to a Git branch

Every commit pushed to the Production Branch of your connected Git repository will be assigned the domains configured in your project.

To automatically assign a domain to a different branch:

Pro and Enterprise teams can also set branch tracking for their custom environments.

If you prefer to do this using the Vercel REST API instead, you can use the "Update a project domain" PATCH endpoint.

---

## Working with DNS

**URL:** https://vercel.com/docs/domains/working-with-dns

**Contents:**
- Working with DNS
  - DNS records
  - DNS propagation
  - DNS best practices
- Troubleshooting
- Related
    - Domains overview
    - Working with Domains
    - Working with Nameservers
    - Working with SSL

DNS is the system used to connect domain names to IP addresses. When you make a request for a website, the browser performs a DNS query. It's usually the recursive resolver that carries out this work, going to the root DNS nameserver, TLD nameserver, and the authoritative server, if it isn't found in the cache.

There are a number of different types of DNS records that can be used together to create a DNS configuration. Some of the common information that you might see in a DNS record are:

To learn more about adding, verifying, and removing DNS records, see "Managing DNS records".

When you're configuring or making changes to your DNS settings, you should be aware that it doesn't happen instantaneously. There's a whole network of servers, each of which has their own cache, and each of these will need to be updated to any new values that you set. For this reason, it can be normal to take up to 24-48 hours to see changes fully propagate through the network.

As we described earlier, when you set a record, you normally set a TTL value, or Time to Live, on a DNS record. This value, set in seconds, is the length of time a DNS cache will store information about your site, before it requests a new copy of the record from the authoritative server.

When you set the TTL value in your DNS record, you need to find the balance between serving your users the site quickly, and ensuring they're not seeing outdated information. A short TTL (minimum 30s) is beneficial if you are constantly updating the content, but will cause slower load times for your site. Using a longer TTL (max 86400 seconds, or 24 hours) means that records are cached for longer, so the site can load quickly for your users. Vercel defaults to 60s for a DNS record.

When you are transferring an existing (in-use) domain to Vercel, it's a good practice to check the existing DNS record and its TTL before switching. Ideally, about 24 hours in advance of changes, you should shorten the DNS TTL to 60s. Once it's propagated, you can then change the DNS record to Vercel so that traffic quickly moves over to the new site because now the DNS TTL is much shorter.

You can use tools such as https://www.whatsmydns.net to determine if your DNS settings have been fully propagated.

To learn more about common DNS issues, see the troubleshooting doc.

Learn the concepts behind how domains work

Learn the concepts behind how domains work

Learn how domains work and the options Vercel provides for managing them.

Learn how domains work and the options Vercel provides for managing them.

Learn about nameservers and the benefits Vercel nameservers provide.

Learn about nameservers and the benefits Vercel nameservers provide.

Learn how Vercel uses SSL certificates to keep your site secure.

Learn how Vercel uses SSL certificates to keep your site secure.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

---

## vercel domains

**URL:** https://vercel.com/docs/cli/domains

**Contents:**
- vercel domains
- Usage
- Extended Usage
- Unique Options
  - Yes
  - Limit
  - Force
- Global Options

The command is used to manage domains under the current scope, providing functionality to list, inspect, add, remove, purchase, move, transfer-in, and verify domains.

You can manage domains with further options and greater control under a Vercel Project's Domains tab from the Vercel Dashboard.

Using the vercel domains command to list all domains under the current scope.

Using the vercel domains command to retrieve information about a specific domain.

Using the vercel domains command to add a domain to the current scope or a Vercel Project.

Using the vercel domains command to remove a domain from the current scope.

Using the vercel domains command to buy a domain for the current scope.

Using the vercel domains command to move a domain to another scope.

Using the vercel domains command to transfer in a domain to the current scope.

These are options that only apply to the command.

The option can be used to bypass the confirmation prompt when removing a domain.

Using the vercel domains rm command with the --yes option.

The option can be used to specify the maximum number of domains returned when using . The default value to and the maximum is .

Using the vercel domains ls command with the --limit option.

The option forces a domain on a project, removing it from an existing one.

Using the vercel domains add command with the --force option.

The following global options can be passed when using the vercel domains command:

For more information on global options and their usage, refer to the options section.

---

## vercel certs

**URL:** https://vercel.com/docs/cli/certs

**Contents:**
- vercel certs
- Usage
- Extended Usage
- Unique Options
  - Challenge Only
  - Limit
- Global Options

The command is used to manage certificates for domains, providing functionality to list, issue, and remove them. Vercel manages certificates for domains automatically.

Using the vercel certs command to list all certificates under the current scope.

Using the vercel certs command to issue certificates for multiple domains.

Using the vercel certs command to remove a certificate by ID.

These are options that only apply to the command.

The option can be used to only show the challenges needed to issue a certificate.

Using the vercel certs command with the --challenge-only option.

The option can be used to specify the maximum number of certs returned when using . The default value is and the maximum is .

Using the vercel certs ls command with the --limit option.

The following global options can be passed when using the vercel certs command:

For more information on global options and their usage, refer to the options section.

---

## Programmatic Domain Management

**URL:** https://vercel.com/docs/domains/registrar-api

**Contents:**
- Programmatic Domain Management
- Getting started with the API
  - Catalog & pricing
  - Availability
  - Orders & purchases
  - Transfers
  - Management
- Deprecations and migration

The domains registrar API enables you to programmatically manage your domain lifecycle from search to renewal.

You can start using the REST API by:

Using the token in either of the following ways:

In the following example, use the Vercel SDK to get the supported TLDs.

In the following example, we use to get the supported TLDs.

You can use the domains registrar API to do the following:

The following legacy domains API endpoints are now deprecated and will be sunset on November 8, 2025:

If you are currently using the Vercel CLI for domain purchases, pricing, or availability, upgrade to CLI version or later.

---

## Working with nameservers

**URL:** https://vercel.com/docs/domains/working-with-nameservers

**Contents:**
- Working with nameservers
  - Benefits of using Vercel nameservers
- Troubleshooting
- Related
    - Domains overview
    - Working with Domains
    - Working with DNS
    - Working with SSL
    - Troubleshooting Domains

Before moving your domain to use Vercel's nameservers, you should ensure that you own the domain listed on the Domains page of your account."

Nameservers are the actual servers on the network that are responsible for resolving domain names to the IP addresses where your site is hosted. Most domain registrars, including Vercel, provide their own nameservers. For Vercel these are:

When you purchase your domain through Vercel, we can set all the DNS records, including nameserver records, that tell anyone looking for your site where it can be found.

For domains that are not registered with Vercel, you can change the nameservers directly from the domain registrar's dashboard. For more information, see Add Vercel's nameservers.

Before using Vercel's nameservers, you should ensure that you own the domain.

To learn more about common nameserver issues, see the troubleshooting doc.

Learn the concepts behind how domains work

Learn the concepts behind how domains work

Learn how domains work and the options Vercel provides for managing them.

Learn how domains work and the options Vercel provides for managing them.

Learn how DNS works in order to properly configure your domain.

Learn how DNS works in order to properly configure your domain.

Learn how Vercel uses SSL certificates to keep your site secure.

Learn how Vercel uses SSL certificates to keep your site secure.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

Learn about common reasons for domain misconfigurations and how to troubleshoot your domain on Vercel.

---

## Pre-Generate SSL Certificates

**URL:** https://vercel.com/docs/domains/pre-generating-ssl-certs

**Contents:**
- Pre-Generate SSL Certificates
- Generating a Certificate
- Setting your DNS records and finalizing
- Verifying the Certificate
- Finishing connecting your domain to Vercel

This page is part the domains transfer experience. See this page for the full set of steps to transfer a domain to Vercel.

This article guides you through all the steps necessary to set up SSL certificates for a domain being migrated to Vercel without downtime. Your domain should be serving content from 3rd party servers that are unrelated to Vercel, and you need to be prepared to make the necessary DNS changes.

You can do this using either the Vercel Domains dashboard, or the Vercel CLI.

In order to issue certificates through the dashboard for a domain, first ensure the domain belongs to a team. You can then click into the domain management page, scroll down to "SSL Certificates" and click "Pre-generate SSL certificates". Please note this option is only available if you do not already have any SSL certificates issued for the domain.

If you choose to do this through the terminal, you can run the following command to get the challenge records for your domain:

Creating the challenge for the certificate that will be used for *.example.com and example.com.

In order to verify ownership of your domain, copy the TXT records into your DNS on the registrar you are using.

Click "Verify" to verify that the records have been set and issue the certificate. DNS records can take time to propagate, so if it doesn't work immediately, it's worth waiting for the records to propagate before taking further action.

To check whether the TXT records have propagated, you can use the following command in a terminal of your choice:

Once TXT records have propagated, you can click "Verify" to issue the SSL certificates.

If you choose to issue SSL certificates through the terminal, you can run the command previously used without the flag:

Issuing a certificate that covers both *.example.com and example.com.

Before you change the DNS records of your domain, you can verify if the certificate is correct and will be accepted by browsers. Run the following command:

curl command that sends a request directly to Vercel, ignoring the DNS configuration of the domain.

If the request is successful, the certificate is working and you can proceed with the migration.

To migrate your deployment to Vercel, add the provided A or CNAME record from your project’s Domain Settings page to your DNS configuration so your domain points to Vercel webservers. See this detailed guide on using domains with A records for more information.

For more details on performing a migration, see this guide.

---

## Multi-tenant Limits

**URL:** https://vercel.com/docs/multi-tenant/limits

**Contents:**
- Multi-tenant Limits
- Feature availability
  - Wildcard domains
  - Custom domains
- Multi-tenant preview URLs
- Custom SSL certificates
- Rate limits
- DNS propagation
- Subdomain length limits

This page provides an overview of the limits and feature availability for Vercel for Platforms across different plan types.

Multi-tenant preview URLs are available exclusively for Enterprise customers. This feature allows you to:

To enable this feature, Enterprise customers should contact their Customer Success Manager (CSM) or Account Executive (AE).

Custom SSL certificates are available exclusively for Enterprise customers. This feature allows you to:

Learn more about custom SSL certificates.

Domain management operations through the Vercel API are subject to standard API rate limits:

After configuring domains or nameservers, DNS typically takes 24-48 hours to propagate globally. Use tools like WhatsMyDNS to check propagation status.

Each DNS label has a 63-character limit. For preview URLs with long branch names and tenant subdomains, keep branch names concise to avoid resolution issues.

---

## Supported domains

**URL:** https://vercel.com/docs/domains/supported-domains

**Contents:**
- Supported domains

Vercel supports the following top-level domains (TLDs) for purchase as custom domains. Refer to the table below for information on which TLDs can be transferred into Vercel and which TLDs support WHOIS privacy.

---

## Uploading Custom SSL Certificates

**URL:** https://vercel.com/docs/domains/custom-SSL-certificate

**Contents:**
- Uploading Custom SSL Certificates
- SSL best practices

Uploading Custom SSL Certificates are available on Enterprise plans

By default, Vercel provides all domains with custom SSL certificates. However, Enterprise teams can upload a custom SSL certificate. This allows for Enterprise teams to serve their own SSL certificate on a Custom Domain at Vercel's edge network, rather than the automatically generated certificate.

Custom SSL certificates can be uploaded through the Domains tab on your team's dashboard, or by using the Vercel REST API.

Uploading a custom certificate follows a three step process:

The content of each element must be copied and pasted into the input box directly. The certificate and private key can be extracted from the PEM files that are provided by your certificate issuer, and should be in the following format:

When uploading your SSL certificate, you should note the following:

---

## Managing Nameservers

**URL:** https://vercel.com/docs/domains/managing-nameservers

**Contents:**
- Managing Nameservers
- Add custom nameservers
- Add Vercel's nameservers
- Restore original nameservers

Nameservers are used to resolve domain names to IP addresses. For domains with Vercel as the registrar, nameservers can be viewed, edited, and reset by selecting the domain from the Domains tab of your team's dashboard.

Sometimes, however, you may need to delegate nameserver management to another host. For domains registered with Vercel, you can add custom nameservers to your Vercel-hosted domain, directly from the dashboard, allowing for delegation to other DNS providers. You can add up to four nameservers at once, and revert to your previous settings if necessary.

For domains that are not registered with Vercel, you can change the nameservers directly from the domain registrar's dashboard.

Nameserver changes can take up to 48 hours to complete due to DNS propagation.

Ensure your account or team is selected in the scope selector

Navigate to the Domains tab and select the domain

On your domain's settings page, under Nameservers, click the Edit button:

In the Edit Nameservers modal, add the new nameservers:

Before using Vercel's nameservers, you should ensure that you own the domain.

Vercel will present a message when you have successfully submitted the nameserver change.

---

## Managing Domain Renewals and Redemptions

**URL:** https://vercel.com/docs/domains/working-with-domains/renew-a-domain

**Contents:**
- Managing Domain Renewals and Redemptions
- Auto renewal
  - Select the Domains tab
  - View the auto renewal status
  - Toggle the auto renewal status
  - Auto renewal off
  - Auto renewal on
- Manual renewal
  - Select the Domains Tab
  - Find your domain from the list

Custom domains purchased through or registered with Vercel are automatically renewed by default with the option to manually renew them.

You can see the expiration or renewal date of your Vercel-managed domains in the list of domains on the Domains tab of your team's dashboard.

To enable automatic renewal, follow these steps:

You can choose to prevent the automatic renewal of a Domain from the Domains tab on the Vercel Dashboard.

From the list of domains, find the domain you want to enable automatic renewal for. You can use the search bar or filter button to find it if you have many domains. You'll see the auto-renewal or expiry status of the domain in the domain's row.

Click on the hamburger menu icon to the right of the domain and toggle the Auto Renewal to on or off.

If auto renewal is off, Vercel will not try to re-register the Domain when it expires at the end of the registration period. You will not be charged for the Domain any longer, but you will lose access to the Domain when it expires. Recovering the Domain, if even possible, may be subject to a redemption fee.

If the Domain enters the redemption period, you can attempt to manually recover it by selecting Renew in the Domains tab. The option will appear if recovery is still possible.

Vercel will send you three emails regarding the Domain before this happens. 24 and 14 days before the Domain is set to expire, you will be notified that auto renewal is off and the Domain will expire soon. A final email will notify you when the Domain expires.

Vercel can only renew your domain if your payment method is valid at the time of renewal. If your card fails, the domain may expire. Vercel will retry the payment and notify you of any issues via email. You can confirm renewal status or retry manually in the Domains tab.

If auto renewal is on, Vercel will use the following process to renew the domain:

Navigate to the Domains tab on the Vercel Dashboard.

From the list of domains, find the domain you want to renew. You can use the search bar or filter button to find it if you have many domains. You'll see the auto renewal or expiry status of the domain in the domain's row.

Click on the hamburger menu icon to the right of the domain and click the Renew button.

Your domain must be within 1 year of expiration to be eligible for renewal.

For expired domains with a redemption period (typically 30 days), you can now recover them directly in the dashboard:

A redemption fee will be applied, depending on the domain registry.

You can filter your Vercel owned domains by their renewal status by clicking the filter icon in the top right of the Domains table:

Third-Party Domains (ones not purchased with or transferred into Vercel) are not subject to auto-renewal. Please refer to your Domain name registrar's policy regarding renewals.

---

## Viewing & Searching Domains

**URL:** https://vercel.com/docs/domains/working-with-domains/view-and-search-domains

**Contents:**
- Viewing & Searching Domains
- Viewing domains
- Searching domains

To view all your registered domains, go to the Domains tab in your Vercel dashboard.

The domains list will show you all domains that are currently active on your account, and display the following information:

You can search for a specific domain by using the search bar above the domains list.

It is not possible to search a multi-level wildcard subdomain. It is only possible to search a subdomain at one level down.

---

## vercel dns

**URL:** https://vercel.com/docs/cli/dns

**Contents:**
- vercel dns
- Usage
- Extended Usage
- Unique Options
  - Limit
- Global Options

The command is used to manage DNS record for domains, providing functionality to list, add, remove, and import records.

When adding DNS records, please wait up to 24 hours for new records to propagate.

Using the vercel dns command to list all DNS records under the current scope.

Using the vercel dns command to add an A record for a subdomain.

Using the vercel dns command to add an MX record for a domain.

Using the vercel dns command to add an SRV record for a domain.

Using the vercel dns command to add a CAA record for a domain.

Using the vercel dns command to remove a record for a domain.

Using the vercel dns command to import a zonefile for a domain.

These are options that only apply to the command.

The option can be used to specify the maximum number of dns records returned when using . The default value is and the maximum is .

Using the vercel dns ls command with the --limit option.

The following global options can be passed when using the vercel dns command:

For more information on global options and their usage, refer to the options section.

---

## Removing a Domain from a Project

**URL:** https://vercel.com/docs/domains/working-with-domains/remove-a-domain

**Contents:**
- Removing a Domain from a Project
  - Navigate to the Domains tab
  - Click remove button
  - Remove domain from your account
- Using cURL

When you add a domain to any project, it will be connected to your account until you choose to delete it. This guide demonstrates how to remove a domain from a Project and from your account completely.

To remove a domain that is assigned to a project, navigate to the Domains tab from the Project Overview and click the More Options button for the domain you want to remove.

Once the • • • menu button has been clicked, you will be presented with further options. Click the Delete menu button to remove the domain from the project.

Optionally, if you wish to remove a domain from all Projects, as well as your Account, navigate to the Domains section of your dashboard. In the list of all the domains under your account, find the domain you wish to remove. Then, from the context menu, click the Delete menu item.

If the domain was purchased through Vercel, you must first wait for the domain to expire before you can remove it from your account.

To remove a domain from a project using cURL, you can use the following command. To create an Authorization Bearer token, see the access token section of the API documentation.

---

## Managing DNS Records

**URL:** https://vercel.com/docs/domains/managing-dns-records

**Contents:**
- Managing DNS Records
- Adding DNS Records
  - Selecting your Domain
  - Add DNS Record
- Verifying DNS Records
- Removing DNS Records
- DNS Presets
- Migrating DNS records from an external registrar
  - Clone the Current DNS Configuration
  - Verify the Records

Once you've added a domain and it's using Vercel's nameservers, you can view its DNS records from your team's Domains page. From there, you can view, add, verify, remove the records, or add presets.

To make sure DNS records are applied, and to allow you to manage them, your domain needs to use Vercel's nameservers . If you are using a third-party domain, you will be provided with the Vercel nameservers to copy and use with your registrar.

On your team's dashboard, select the Domains tab. From the Domains page, click on a domain of your choice to view its Advanced Settings page.

Once on the Advanced Settings page of your domain, select the Enable Vercel DNS button to fill out the DNS Record form. Once complete, click on the Add button.

You can then create a new DNS record with the following data:

Name: The prefix or location of the record. For www.example.com, the name argument would be www.

Type: Types can be , , , , , , , , , or .

Value: The value of the record.

TTL: Default is 60 seconds. For advanced users, this value can be customized.

Comment: An optional comment to provide context on what this record is for.

More: Some records will require more data. MX records, for example, will request "priority".

Once a DNS record has been added, it can take up to 24 hours to the DNS records to fully update and any local caches to be cleared.

Once DNS records have been changed, you may wish to check that these have been set correctly. There are many third-party tools that do this, such as DNS Checker and DNS Map - these show the state of your DNS records in different regions of the world.

You can also use the command to check the DNS record for your domain:

To remove DNS records:

Default records can't be removed. However, new records can override them if required.

Vercel does not provide an email service. To be able to receive emails or add specific DNS configurations through a domain that you've added to Vercel, you need to add the respective DNS Records, such as MX for email or TXT for other services.

Vercel streamlines this process for common third-party services by allowing you to add missing DNS Records using DNS Presets on your dashboard.

From your dashboard, navigate to the Domains tab.

Select the domain you wish to add a preset to and click the Add DNS Preset dropdown on the right:

You will be presented with a list of commonly used third-party providers. If your provider is listed, select it, and the necessary DNS Records—such as MX for email or TXT for other services like Bluesky will automatically be configured on your domain.

If your provider is not listed, please refer to their documentation to find out which DNS Records you need to add.

Once you have added a domain to your Vercel project and also verified the certificate is working as expected, you can choose three options of records to finally complete the migration: A, CNAME, or Nameservers. In case you decide to use an A or a CNAME record, then you can change those records in your DNS provider to make Vercel serve your deployment from the selected domain, as instructed on your dashboard.

If you decide to change the Nameservers of your domain, you can follow the below instructions which will help you migrate your DNS configuration from any provider and avoid downtime.

To locate the current DNS provider of your domain, you can run the following command:

The result will show the current DNS authority. Next, you'll need to locate your DNS records from the provider's dashboard.

After you've successfully located all records associated with your domain, you may now add them to Vercel. You can either do this manually or by importing a zone file.

Importing a zone file

If you have downloaded a zone file from your existing file, you may use the following comand to upload that to Vercel:

If you do not apply a custom zone file, transferring in a domain automatically applies the default Vercel DNS settings.

To verify the records, you can now query the DNS configuration that will be served by Vercel:

Checking the DNS configuration of the A record under "api" served by Vercel.

Then, check the DNS records from the existing provider to make sure they match. If you were moving your DNS from Cloudflare, for example, the correct command would be:

Checking the DNS configuration of the A record under "api" served by Cloudflare. The example should be replaced with the authoritative nameserver given by your provider.

Before proceeding, we recommend checking every record you moved. For more insight into the DNS resolution, remove the flag.

In your registrar's dashboard (where you bought the domain), change the Nameservers to your new provider. Nameserver changes can take up to 48 hours to propagate. If you bought the domain from Vercel, you can manage nameservers from the domains page.

---

## Transferring Domains to Another Team or Project

**URL:** https://vercel.com/docs/domains/working-with-domains/transfer-your-domain

**Contents:**
- Transferring Domains to Another Team or Project
- Transfer a domain to another Vercel user or Team
  - Select the Domains tab
  - Select the domain
  - Select the team
  - Confirm the change
- Transferring domains between projects
- Transferring domains out of Vercel
  - Verifying Transfer Eligibility
  - Select the Domains tab

You can move domains to another team using the Domains tab of your team's dashboard.

Once on the Domains tab, select the context menu next to the domain you wish to move, and click Move. You can also use checkbox next to each domain to select more than one domain

After selecting the domain(s) and clicking Move, you will be asked to confirm which profile or team you wish to move them to.

When selecting the input field, you will be provided with a list of teams you belong to. If the profile or team you wish to move the domain(s) to is not present, enter the value instead. You can find the value in Settings page for both profiles and teams.

When moving domains to another team or user, all existing project domains associated with them will remain and not be moved to prevent service disruption. However, any custom aliases that are not part of project domains will be removed immediately.

To confirm the change, select Move. The domains will be transferred to the new profile of team immediately.

You can use the Dashboard to remove a domain from a project and then re-add it to another. However, this could potentially end up with some site down-time. For more information on transferring domains with zero downtime, see How to move a domain between Vercel projects with "Zero Downtime"?

Due to ICANN rules, a domain must be registered with a registrar for 60 days before it can be transferred to another.

You can verify that your domain has been registered with Vercel for at least 60 days by visiting the team's Domains Dashboard. If the registrar is Vercel and the age greater than 60 days, it is eligible to transfer.

For domains that are registered with Vercel, you can retrieve an authorization code for transferring out to another registrar from the Domains tab of the Dashboard.

Once on the Domains tab, click on the triple-dot menu button for the relevant domain. A menu-item button to transfer the domain out will be presented if the domain is registered with Vercel.

If under a Team scope, only Team Owners will see the menu-item button.

After clicking the menu-item button, a modal will open up with the authorization code required to transfer the domain. Use this authorization code with your new registrar to confirm that you want to transfer the domain. There is no additional confirmation that you need to do on the Vercel side. Transferring a domain can take up to a week.

If you encounter problems with the transfer code, ensure you've entered it correctly without typos or extra spaces. If the code seems correct but still doesn't work, please contact Vercel support for further assistance.

By transferring your domain into Vercel, you allow Vercel to manage the DNS records for the domain and can use it with any Projects listed under the account the domain is owned by.

Due to ICANN rules, a domain must be registered with a registrar for 60 days before it can be transferred to another. You will need to confirm this with your registrar before attempting the transfer to Vercel.

If the domain has not been registered with the current registrar for at least 60 days, the domain transfer will fail.

NOTE: To find further information on ICANN rules, visit the ICANN website.

Once you have verified your domain's eligibility to transfer, proceed with unlocking your domain in your registrar's domain settings. Most domains are usually locked by default to prevent unauthorized changes.

The domain lock feature appears in different forms across registrars. Sign into the host where your domain is registered and look for a Domain Lock or similar option to unlock your domain. If this option is not available, contact your registrar to change this.

After unlocking the domain, you will need to obtain an authorization code. The code will be sent to the email address associated with your domain by your registrar. In some cases, your authorization code pops up on your dashboard. This may be available in the domain registrars dashboard. If it is not available, contact your registrar to obtain this.

When transferring a domain, you will have two options to choose from. Either using the Vercel Dashboard or Vercel CLI.

Option 1: Using Vercel Dashboard

After obtaining the authorization code, click on the Transfer in button in the Vercel Domains Dashboard and enter in your domain and respective authorization code.

Option 2: Using Vercel CLI

With Vercel CLI, you can run the following command from your terminal.

You will be requested to provide an authorization code from your registrar after running this command. Once you get the authorization code from your registrar, paste it into the prompt and the transfer will begin.

In a case where your domain cannot be transferred, check that it has been over 60 days since the domain has been registered or previously transferred. If it still does not work, contact your registrar.

Follow these steps to ensure that there is no downtime while the domain is transferred to Vercel.

Pre-generate SSL certificates

If you are migrating a deployment to Vercel, require zero downtime, and aren't using Vercel's nameservers, you can pre-generate and issue SSL certificates to your domain. If you have enabled Vercel DNS by pointing your domain's nameserver to Vercel and have generated an SSL certificate, you can ignore this step.

Follow the detailed guide to set up SSL certificates before finalizing the domain transfer.

Set DNS records in your registrar

Once you have pre-generated the SSL certificates, you need to add the new TXT records to your DNS records in your domain registrar dashboard. Learn how to do that here.

You can deploy your app with Vercel once the domain has been successfully added to your account.

By setting a production domain from your projects' Domains dashboard, you will be able to use the following command with Vercel CLI:

This command will deploy your project and make it accessible at the production domain that you have setup.

---
