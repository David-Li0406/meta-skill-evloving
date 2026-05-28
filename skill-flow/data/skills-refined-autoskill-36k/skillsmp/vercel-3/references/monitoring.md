# Vercel - Monitoring

**Pages:** 20

---

## Migrating to the latest Speed Insights package

**URL:** https://vercel.com/docs/speed-insights/migrating-from-legacy

**Contents:**
- Migrating to the latest Speed Insights package
- Changes to the integration
  - New package:
  - Sample rate
  - First-Party intake
- Changes to the UI
  - Emphasis on P75
  - Updated Scoring Criteria
  - New Metric: TTFB

Speed Insights is available on all plans

The new Speed Insights brings a few changes to the UI and the ingestion mechanism. You find a list of changes below and understand how they affect you.

Vercel introduced a package titled as an iteration from the automatic install process. This shift is intended to offer more flexibility and broader framework support.

By migrating to the new Speed Insights package, you benefit from the following features:

You should become familiar with the configuration options and upgrade. However, the intake API will still be usable for some time.

Sample rate configurations have been relocated from team settings to the @vercel/speed-insights package, providing the capability to set specific rates for each project.

Data ingestion now utilizes a first-party intake during your deployment. Here's how it works:

With this change, the script becomes less affected by content blockers and performs fewer DNS lookups, resulting in a faster and more reliable experience. It is no longer required to define a Content Security Policy to allow the third-party script.

Our revamped dashboard emphasizes the 75th percentile, a recommendation from the Core Web Vitals team.

In other terms, the score is now determined by the experience of the fastest 75% of your users.

This percentile was chosen because it represents the performance experienced by the majority of visits and is not significantly affected by outliers.

For deeper insights, it is now possible to view multiple percentiles at once, without affecting the score.

Speed Insights now uses scoring criteria that are inspired by the improvements found in Lighthouse 10. Below, you'll find a comprehensive comparison of the metrics, thresholds, and their respective weights as per our updated system and its previous iteration.

All previous (prior to the new Speed Insights) and new data points use this updated scoring criteria.

Comparison table between the new and old scoring criteria

The CLS metric is given more weight in the new version, and the FID metric is replaced with INP. The FCP and LCP metrics now have the same thresholds for both desktop and mobile.

We've introduced a new metric, Time to First Byte (TTFB), which measures the time taken by the server to respond to the first request. This metric is not included in the score, but it can offer more insights about performance.

---

## Speed Insights Drains Reference

**URL:** https://vercel.com/docs/drains/reference/speed-insights

**Contents:**
- Speed Insights Drains Reference
- Speed Insights Schema
- Format
  - JSON
  - NDJSON
- Sampling Rate
- More resources

Speed Insights Drains send performance metrics and web vitals from your applications to external endpoints for storage and analysis. To enable Speed Insights Drains, create a drain and choose the Speed Insights data type.

Vercel sends Speed Insights data to endpoint URLs over HTTPS when your application collects performance metrics.

The following table describes the possible fields that are sent via Speed Insights Drains:

Vercel supports the following formats for Speed Insights Drains. You can configure the format when configuring the Drain destination:

Vercel sends Speed Insights data as JSON arrays containing metric objects:

Vercel sends Speed Insights data as newline-delimited JSON objects:

When you configure a Speed Insights Drain in the Vercel UI, you can set the sampling rate to control the volume of data sent. This helps manage costs when you have high traffic volumes.

For more information on Speed Insights Drains and how to use them, check out the following resources:

---

## Limits and Pricing for Monitoring

**URL:** https://vercel.com/docs/query/monitoring/limits-and-pricing

**Contents:**
- Limits and Pricing for Monitoring
- Pricing
- Limitations
- How are events counted?

Monitoring has become part of Observability, and is therefore included with Observability Plus at no additional cost. If you are currently paying for Monitoring, you should migrate to Observability Plus to get access to additional product features with a longer retention period for the same base fee.

Even if you choose not to migrate to Observability Plus, Vercel will automatically move you to the new pricing modal of $1.20 per 1 million events, as shown below. If you do not migrate to Observability Plus, you will not be able to access Observability Plus features on the Observability tab.

To learn more, see Limits and Pricing for Observability.

Vercel creates an event each time a request is made to your website. These events include unique parameters such as execution time. For a complete list, see the visualize clause docs.

---

## Vercel Web Analytics

**URL:** https://vercel.com/docs/analytics

**Contents:**
- Vercel Web Analytics
- Visitors
  - How visitors are determined
- Page views
- Bounce rate
  - How bounce rate is calculated
- Panels
- Bots

Web Analytics are available on all plans

Web Analytics provides comprehensive insights into your website's visitors, allowing you to track the top visited pages, referrers for a specific page, and demographics like location, operating systems, and browser information. Vercel's Web Analytics offers:

To set up Web Analytics for your project, see the Quickstart.

If you're interested in learning more about how your site is performing, use Speed Insights.

The Visitors tab displays all your website's unique visitors within a selected timeframe. You can adjust the timeframe by selecting a value from the dropdown in the top right hand corner.

You can use the panels section to view a breakdown of specific information, organized by the total number of visitors.

Instead of relying on cookies like many analytics products, visitors are identified by a hash created from the incoming request. Using a generated hash provides a privacy-friendly experience for your visitors and means visitors can't be tracked between different days or different websites.

The generated hash is valid for a single day, at which point it is automatically reset.

If a visitor loads your website for the first time, we immediately track this visit as a page view. Subsequent page views are tracked through the native browser API.

The Page Views tab, like the Visitors tab, shows a breakdown of every page loaded on your website during a certain time period. Page views are counted by the total number of views on a page. For page views, the same visitor can view the same page multiple times resulting in multiple events.

You can use the panels section to view a breakdown of specific information, organized by the total number of page views.

The Bounce rate is the percentage of visitors who land on a page and leave without taking any further action.

The higher the bounce rate, the less engaging the page is.

Bounce Rate (%) = (Single-Page Sessions / Total Sessions) × 100

Web Analytics defines a session as a group or page views by the same visitor. Custom event do not count towards the bounce rate.

For that reason, when filtering the dashboard for a given custom event, the bounce rate will always be 0%.

Panels provide a way to view detailed analytics for Visitors and Page Views, such as top pages and referrers. They'll also show additional information such as the country, OS, and device or browser of your visitors, and configured options such as custom events and feature flag usage.

By default, panels provide you with a list of top entries, categorized by the number of visitors. Depending on the panel, the information is displayed either as a number or percentage of the total visitors. You can click View All to see all the data:

You can export the up to 250 entries from the panel as a CSV file. See Exporting data as CSV for more information.

Web Analytics does not count traffic that comes from automated processes or accounts. This is determined by inspecting the User Agent header for incoming requests.

---

## Tracking custom events

**URL:** https://vercel.com/docs/analytics/custom-events

**Contents:**
- Tracking custom events
- Tracking a client-side event
- Tracking an event with custom data
- Limitations
- Tracking custom events in the dashboard

Custom Events are available on Enterprise and Pro plans

Vercel Web Analytics allows you to track custom events in your application using the function. This is useful for tracking user interactions, such as button clicks, form submissions, or purchases.

Make sure you have version 1.1.0 or later installed.

This will track an event named Signup.

This tracks a "Signup" event that occurred in the "footer" location. The second event tracks a "Purchase" event with product name and a price.

The following limitations apply to custom data:

Once you have tracked an event, you can view and filter for it in the dashboard. To view your events:

---

## Pricing for Web Analytics

**URL:** https://vercel.com/docs/analytics/limits-and-pricing

**Contents:**
- Pricing for Web Analytics
- Pricing
- Usage
- Billing information
  - Hobby
  - Experience Vercel Pro for free
  - Pro
  - Pro with Web Analytics Plus
- FAQ
  - What is an event in Vercel Web Analytics?

The Web Analytics pricing model is based on the number of collected events across all projects of your team. Once you've enabled Vercel Web Analytics, you will have access to various features depending on your plan.

On every billing cycle (every month for Hobby teams), you will be granted a certain number of events based on your plan.

Once you exceed your included limit, you will be charged for additional events. If your team is on the Hobby plan, we will pause the collection, as you cannot be charged for extra events.

Pro teams can also purchase the Web Analytics Plus add-on for an additional $10/month per team, which grants access to more features and an extended reporting window.

The table below shows the metrics for the Observability section of the Usage dashboard where you can view your Web Analytics usage.

To view information on managing each resource, select the resource link in the Metric column. To jump straight to guidance on optimization, select the corresponding resource link in the Optimize column.

See the manage and optimize Observability usage section for more information on how to optimize your usage.

Speed Insights and Web Analytics require scripts to do collection of data points. These scripts are loaded on the client-side and therefore may incur additional usage and costs for Data Transfer and Edge Requests.

Web Analytics are free for Hobby users within the usage limits detailed above.

Vercel will send you notifications as you are nearing your usage limits. You will not pay for any additional usage. However, once you exceed the limits, a three day grace period will start before Vercel will stop capturing events. In this scenario, you have two options to move forward:

You can sign up for Pro and start a trial using the button below.

Unlock the full potential of Vercel Pro during your 14-day trial with $20 in credits. Benefit from 1 TB Fast Data Transfer, 10,000,000 Edge Requests, up to 200 hours of Build Execution, and access to Pro features like team collaboration and enhanced analytics.

If you're expecting large number of page views, make sure to deploy your project to a Vercel Team on the Pro plan.

For Teams on a Pro trial, the trial will end after 14 days.

Note that while you will not be charged during the time of the trial, once the trial ends, you will be charged for the events collected during the trial

You will be charged $0.00003 per event. These numbers are based on a per-billing cycle basis. Vercel will send you notifications when you get closer to spending your included credit.

Pro teams can set up Spend Management to get notified or to automatically take action, such as using a webhook or pausing your projects when your usage hits a set spend amount.

Analytics data is not collected while your project is paused, but becomes accessible again once you upgrade to Pro.

Teams on the Pro plan can optionally extend usage and capabilities through the Web Analytics Plus add-on for an additional $10/month per team.

When enabled, all projects within the team have access to additional features.

To upgrade to Web Analytics Plus:

An event in Vercel Web Analytics is either an automatically tracked page view or a custom event. A page view is a default event that is automatically tracked by our script when a user visits a page on your website. A custom event is any other action that you want to track on your website, such as a button click or form submission.

Yes, events are shared across all projects under the same Vercel account in Web Analytics. This means that the events collected by each project count towards the total event limit for your account. Keep in mind that if you have high-traffic websites or multiple projects with heavy event usage, you may need to upgrade to a higher-tier plan to accommodate your needs.

The reporting window in Vercel Web Analytics is the length of time that your analytics data is guaranteed to be stored and viewable for analysis. While only the reporting window is guaranteed to be stored, Vercel may store your data for longer periods to give you the option to upgrade to a bigger plan without losing any data.

---

## Using Speed Insights

**URL:** https://vercel.com/docs/speed-insights/using-speed-insights

**Contents:**
- Using Speed Insights
- Accessing Speed Insights
- Breaking down data in Speed Insights
  - Breakdown by route or path
  - Breakdown by HTML elements
  - Breakdown by country
- Disabling Speed Insights
- Identifying if Speed Insights is enabled

To access Speed Insights:

Speed Insights offers a variety of views to help you analyze your application's performance data. This allows you to identify areas that need improvement and make informed decisions about how to optimize your site.

To view metrics for a specific route or path:

To view a detailed breakdown of the performance of individual HTML elements on your site:

This view is particularly useful for identifying specific elements that may be causing performance issues.

This view is helpful for identifying regions where your application may be underperforming.

To view a geographical breakdown of your application's performance:

You may want to disable Speed Insights in your project if you find you no longer need it. You can disable Speed Insights from within the project settings in the Vercel dashboard. If you are unsure if a project has Speed Insights enabled, see Identifying if Speed Insights is enabled.

If you transfer a project with Speed Insights enabled from a Hobby team to a Pro plan, it will continue to be enabled but with increased limits, as documented in the pricing docs. This means that Speed Insights will be added to your Pro plan invoice automatically.

When you disable Speed Insights in the middle of your billing cycle, it will not be removed instantly. Instead it will stop collecting new data points but will continue to show already collected data until the end of the cycle, see the prorating docs for more information.

If you are on an Enterprise plan, check your contract entitlements as you may have custom limits included. If you have any questions about your billing/contract regarding Speed Insights you can reach out to your Customer Success Manager (CSM) or Account Executive (AE) for further clarification.

If you have many projects on your Vercel account and are not sure which of them has Speed Insights enabled, you can see this from the dashboard without needing to check each project separately. The different circles in the right corner of each project card will show the Speed Insights status.

If Speed Insights is not enabled, then the circle will be gray, with the speed insights logo. For example:

If Speed Insights is enabled but no data points have been collected yet then it will show an empty circle, like the below:

If Speed Insights is enabled and data points have been collected then the circle will be colored with a number inside, similar to the below image:

---

## Vercel Web Analytics Troubleshooting

**URL:** https://vercel.com/docs/analytics/troubleshooting

**Contents:**
- Vercel Web Analytics Troubleshooting
- No data visible in Web Analytics dashboard
- Web Analytics is not working with a proxy (e.g., Cloudflare)
- Routes are not visible in Web Analytics dashboard

Issue: If you are experiencing a situation where data is not visible in the analytics dashboard or a 404 error occurs while loading , it could be due to deploying the tracking code before enabling Web Analytics.

Issue: Web Analytics may not function when using a proxy, such as Cloudflare.

Issue: Not all data is visible in the Web Analytics dashboard

---

## Web Analytics Drains Reference

**URL:** https://vercel.com/docs/drains/reference/analytics

**Contents:**
- Web Analytics Drains Reference
- Web Analytics Schema
- Format
  - JSON
  - NDJSON
- Sampling Rate
- More resources

If a Web Analytics Drains has been configured, Vercel will send page views and custom events from your applications to external endpoints for storage and analysis over HTTPS when your application tracks events.

The following table describes the possible fields that are sent via Web Analytics Drains:

Vercel supports the following formats for Web Analytics Drains, which you can configure when setting the Drain destination:

Vercel sends Web Analytics data as JSON arrays containing event objects:

Vercel sends Web Analytics data as newline-delimited JSON objects:

When you configure a Web Analytics Drain in the Vercel UI, you can set the sampling rate to control the volume of data sent. This helps manage costs when you have high traffic volumes.

For more information on Web Analytics Drains and how to use them, refer to the following resources:

---

## Redacting Sensitive Data from Web Analytics Events

**URL:** https://vercel.com/docs/analytics/redacting-sensitive-data

**Contents:**
- Redacting Sensitive Data from Web Analytics Events
- Ignoring events or routes
- Removing query parameters
- Allowing users to opt-out of tracking

Sometimes, URLs and query parameters may contain sensitive data. This could be a user ID, a token, an order ID, or any other data that you don't want to be sent to Vercel. In this case, you may not want them to be tracked automatically.

To prevent sensitive data from being sent to Vercel, you can pass in the function that modifies the event before it is sent. To learn more about the function and how it can be used with other frameworks, see the @vercel/analytics package documentation.

To ignore an event or route, you can return from the function. Returning the event or a modified version of it will track it normally.

To apply changes to the event, you can parse the URL and adjust it to your needs before you return the modified event.

In this example the query parameter is removed on all events.

You can also use to allow users to opt-out of all tracking by setting a value (for example ).

---

## Integrate flags with Vercel Web Analytics

**URL:** https://vercel.com/docs/feature-flags/integrate-with-web-analytics

**Contents:**
- Integrate flags with Vercel Web Analytics
- Client-side tracking
  - Emit feature flags and connect them to Vercel Web Analytics
  - Tracking feature flags in client-side events
- Server-side tracking

Web Analytics integration is available in Beta on all plans

Vercel Web Analytics can look up the values of evaluated feature flags in the DOM. It can then enrich page views and client-side events with these feature flags.

To share your feature flags with Web Analytics you have to emit your feature flag values to the DOM as described in Supporting Feature Flags.

This will automatically annotate all page views and client-side events with your feature flags.

Client-side events in Web Analytics will now automatically respect your flags and attach those to custom events.

To manually overwrite the tracked flags for a specific event, call:

If the flag values on the client are encrypted, the entire encrypted string becomes part of the event payload. This can lead to the event getting reported without any flags when the encrypted string exceeds size limits.

To track feature flags in server-side events:

First, report the feature flag value using to make the flag show up in Runtime Logs:

Once reported, any calls to can look up the feature flag while handling a specific request:

If you are using an implementation of the Feature Flags Pattern you don't need to call . The respective implementation will automatically call for you.

---

## Troubleshooting Vercel Speed Insights

**URL:** https://vercel.com/docs/speed-insights/troubleshooting

**Contents:**
- Troubleshooting Vercel Speed Insights
- No data visible in Speed Insights dashboard
- Requests are not getting called
- Speed Insights is not working with proxy

Speed Insights is available on all plans

If you are experiencing a situation where data is not visible in the Speed Insights dashboard, it could be due to a couple of reasons.

If is correctly loading but not sending any data (e.g. no request), ensure that you're checking for the request after navigating to a different page, or switching tabs. Speed Insights data is only sent on window blur or unload events.

We do not recommend placing a reverse proxy in front of Vercel, as it may interfere with the proper functioning of Speed Insights.

---

## Using Drains

**URL:** https://vercel.com/docs/drains/using-drains

**Contents:**
- Using Drains
- Configuring Drains
  - Add a drain
  - Choose data type
  - Configure the drain
  - Configure the sampling rules (optional)
  - Configure destination
    - Custom endpoint
    - Native integrations
  - Create the drain

Drains are available on Enterprise and Pro plans

You can add drains to your project by following the configuration steps below. When you configure the destination, choose between sending data to a custom HTTP endpoint and using a native integration or an external integration to send your data to popular services.

Teams on Pro and Enterprise plans can configure drains to forward observability data. You can send logs, traces, speed insights, and analytics data to a custom HTTP endpoint or use integrations from the Vercel Marketplace to send logs and traces data to popular services.

From the Vercel dashboard, go to Team Settings > Drains and click Add Drain.

Select the type of observability data you want to drain:

At any time, you can also add an external integration to available connectable account log drain integrations by clicking the External Integrations link on the top right of the Add Drain side bar.

Provide a name for your drain and select which projects should send data to your endpoint. You can choose all projects or select specific ones.

The drain type determines which configuration options you can set:

Configure the sampling rate to control the volume of data sent to your drain. This can help manage costs when you have high traffic volumes. For detailed log source, environment, and sampling options, see Additional configuration for logs.

For Log and Trace drains, add sampling rules to define how much data reaches your destination:

Rules run from top to bottom. Requests that match a rule use that rule’s sampling rate, and any other requests are dropped. If you do not add rules, the drain forwards 100% of data to the destination.

Choose how you want to receive your drain data by selecting either the Custom Endpoint or Native Integrations tab.

Configure a custom HTTP endpoint to receive drain data for any data type.

This is the URL of the endpoint we will send your data to. The request will be sent over HTTPS using the POST method. Make sure your endpoint responds with a 200 OK status code.

Choose the delivery format based on your data type:

Signature Verification Secret (Optional)

You can secure your endpoint by comparing the header with this secret. See Securing your Drains for implementation details.

A secret will be automatically generated for you, and you can change it and provide your own secret at any time.

Custom Headers (Optional)

Add custom headers for authentication, identification, or routing purposes. Common use cases include:

Format headers as with one header per line.

Native integrations are available for log and traces data. You have 2 options:

If you've already installed a marketplace integration product that supports drains, you can select it here. The integration will handle endpoint configuration automatically.

Browse and install available product integrations for this drain type:

You can also add a Drain from your team's Integrations tab

Once you have configured all settings, click Create Drain. If you configured a custom endpoint, it will be tested automatically when you create the drain. Vercel will immediately start forwarding data based on your configuration.

You can test your endpoint anytime by clicking the Test button to ensure it receives the data correctly.

Vercel automatically correlates logs with distributed traces when you setup Tracing. Any logs generated during traced requests are enriched with correlation identifiers:

This correlation happens automatically without code changes. For example, this log:

Will be automatically enriched with trace and span identifiers.

Limitations: Only applies to user code logs during traced requests, not build-time logs.

You can create Drains with native integrations for the following data types by using native integrations during the configuration step:

Learn more about native integrations and external (connectable accounts) integrations.

Occasionally your drain endpoints can return an error. If more than 80% of drain deliveries fail or the number of failures exceed 50 for the past hour, we will send a notification email and indicate the error status on your Drains page.

For more information on Drains and how to use them, check out the following resources:

---

## Limits and Pricing for Speed Insights

**URL:** https://vercel.com/docs/speed-insights/limits-and-pricing

**Contents:**
- Limits and Pricing for Speed Insights
- Pricing
- Limitations
- Sample rate
- Prorating
- Usage

Speed Insights is available on all plans

Speed Insights is available on the Hobby, Pro, and Enterprise plans.

On the Hobby plan, Speed Insights is free and can be enabled on one project with a set allotment of data points.

On the Pro plan, the base fee for Speed Insights is $10 per-project, per-month.

The following table outlines the price for each resource according to the plan you are on.

Speed Insights Data Points

Pro teams can set up Spend Management to get notified or to automatically take action, such as using a webhook or pausing your projects when your usage hits a set spend amount.

Once you've enabled Speed Insights, different limitations are applied depending on your plan:

Once the maximum limit of data points is reached, no more data points will be recorded until the current day has passed. On the next day, the recording will resume. When recording is paused, you can still access all existing data points.

You can reduce the number of data points collected by adjusting the Sample Rate at the project level by using the . To learn more, see Sample Rate.

By default, all incoming data points are used to calculate the scores you're being presented with on the Speed Insights view.

To reduce cost, you can change the sample rate at a project level by using the package as explained in Sample rate. To learn more about how to configure the option, see the Sending a sample of events to Speed Insights recipe.

Teams on the Pro or Enterprise plan will immediately be charged the base fee when enabling Speed Insights for each project. However, you will only be charged for the remaining time in your billing cycle. For example:

The table below shows the metrics for the Observability section of the Usage dashboard where you can view your Speed Insights usage.

To view information on managing each resource, select the resource link in the Metric column. To jump straight to guidance on optimization, select the corresponding resource link in the Optimize column.

See the manage and optimize Observability usage section for more information on how to optimize your usage.

Speed Insights and Web Analytics require scripts to do collection of data points. These scripts are loaded on the client-side and therefore may incur additional usage and costs for Data Transfer and Edge Requests.

---

## Manage and optimize usage for Observability

**URL:** https://vercel.com/docs/manage-and-optimize-observability

**Contents:**
- Manage and optimize usage for Observability
- Plan usage
- Managing Web Analytics events
  - Optimizing Web Analytics events
- Managing Speed Insights data points
  - Optimizing Speed Insights data points
- Managing Monitoring events
  - Optimizing Monitoring events
- Optimizing drains usage
- Managing Observability events

The Observability section covers usage for Observability, Monitoring, Web Analytics, and Speed insights.

Speed Insights Data Points

Observability Plus Events

The Events chart shows the number of page views and custom events that were tracked across all of your projects. You can filter the data by Count or Projects.

Every plan has an included limit of events per month. On Pro, Pro with Web Analytics Plus, and Enterprise plans, you're billed based on the usage over the plan limit. You can see the total number of events used by your team by selecting Count in the chart.

Speed Insights and Web Analytics require scripts to do collection of data points. These scripts are loaded on the client-side and therefore may incur additional usage and costs for Data Transfer and Edge Requests.

You are initially billed a set amount for each project on which you enable Speed Insights. Each plan includes a set number of data points. After that, you're charged a set price per unit of additional data points.

Data points are a single unit of information that represent a measurement of a specific Web Vital metric during a user's visit to your website. Data points get collected on hard navigations. See Understanding Data Points for more information.

Speed Insights and Web Analytics require scripts to do collection of data points. These scripts are loaded on the client-side and therefore may incur additional usage and costs for Data Transfer and Edge Requests.

Monitoring has become part of Observability, and is therefore included with Observability Plus at no additional cost. If you are currently paying for Monitoring, you should migrate to Observability Plus to get access to additional product features with a longer retention period for the same base fee.

Vercel creates an event each time a request is made to your website. These events include unique parameters such as execution time and bandwidth used. For a complete list, see the visualize and group by docs.

You pay for monitoring based on the total number of events used above the included limit included in your plan. You can see this number by selecting Count in the chart.

You can also view the number of events used by each project in your team by selecting Projects in the chart. This will show you the number of events used by each project in your team, allowing you to optimize your usage.

Because events are based on the amount of requests to your site, there is no way to optimize the number of events used.

You can optimize your log drains usage by:

Vercel creates one or many events each time a request is made to your website. To learn more, see Events.

You pay for Observability Plus based on the total number of events used above the included limit included in your plan.

The Observability chart allows you to view by the total Count, Event Type, or Projects over the selected time period.

Because events are based on the amount of requests to your site, there is no way to optimize the number of events used.

---

## Session tracing

**URL:** https://vercel.com/docs/tracing/session-tracing

**Contents:**
- Session tracing
- Prerequisites
- Run a session trace
- Run a page trace
- View previous session traces
- Usage and pricing
- Limitations
- More resources

With session tracing, you can use the Vercel toolbar to trace your sessions and view the corresponding spans in the logs dashboard. This is useful for debugging and monitoring performance, and identifying bottlenecks.

A session trace is initiated through the Vercel toolbar, either through a Page Trace or a Session Trace. It is active for the person who initiated the trace on their browser indefinitely, until it is stopped or cookies are cleared.

To run a trace on a specific page, you can run a Page Trace:

You can filter traces using all the same filters available in the Logs tab of the dashboard. To view traces for requests to your browser, press the user icon next to the Traces icon.

Tracing is available on all plans with a limit up to 1 million spans per month, per team.

Custom spans from functions using the Edge runtime are not supported.

---

## Working with Drains

**URL:** https://vercel.com/docs/drains

**Contents:**
- Working with Drains
- Getting started with Drains
- Data types
  - Data type references
- Security
- Usage and pricing
- More resources

Drains are available on Enterprise and Pro plans

Drains let you forward observability data from your applications to external services for debugging, performance optimization, analysis, and alerting, so that you can:

You can add Drains in two ways:

Learn how to manage your active drains.

You can drain four types of data:

Each drain data type has specific formats, fields, and schemas. Review the reference documentation for logs, traces, speed insights, and analytics to understand the data structure you'll receive from each data type.

You can secure your drains by checking for valid signatures and hiding IP addresses. Learn how to add security to your drains.

Drains are available to all users on the Pro and Enterprise plans. If you are on the Hobby or Pro Trial plan, you'll need to upgrade to Pro to access drains.

Drains usage is billed based on the pricing table below. Pricing is the same regardless of data type:

To learn more about Managed Infrastructure on the Pro plan, and how to understand your invoices, see understanding my invoice.

See Optimizing Drains for information on how to manage costs associated with Drains.

For more information on Drains, check out the following resources:

---

## Using Web Analytics

**URL:** https://vercel.com/docs/analytics/using-web-analytics

**Contents:**
- Using Web Analytics
- Accessing Web Analytics
- Viewing data for a specific dimension
- Specifying a timeframe
- Viewing environment-specific data
- Exporting data as CSV
- Disabling Web Analytics

To access Web Analytics:

To export the data from a panel as a CSV file:

The export will include up to 250 entries from the panel, not just the top entries.

---

## Monitoring Reference

**URL:** https://vercel.com/docs/query/monitoring/monitoring-reference

**Contents:**
- Monitoring Reference
- Visualize
  - Aggregations
- Where
- Group by
- Limit
- Group by and where fields
  - Path types
- Chart view
- Table view

The clause selects what query data is displayed. You can select one of the following fields at a time, aggregating each field in one of several ways:

The visualize field can be aggregated in the following ways:

Aggregations are calculated within each point on the chart (hourly, daily, etc depending on the selected granularity) and also across the entire query window

The clause defines the conditions to filter your query data. It only fetches data that meets a specified condition based on several fields and operators:

String literals must be surrounded by single quotes. For example, .

The clause calculates statistics for each combination of field values. Each group is displayed as a separate color in the chart view, and has a separate row in the table view.

For example, grouping by and will display data broken down by each combination of and .

The clause defines the maximum number of results displayed. If the number of query results is greater than the value, then the remaining results are compiled as Other(s).

There are several fields available for use within the where and group by clauses:

All your project's resources like pages, functions, and images have a path type:

In the chart view (vertical bar or line), is applied at the level of each day or hour (based the value of the Data Granularity dropdown). When you hover over each step of the horizontal axis, you can see a list of the results returned and associated colors.

In the table view (below the chart), is applied to the sum of requests for the selected query window so that the number of rows in the table does not exceed the value of .

On the left navigation bar, you will find a list of example queries to get started:

---

## Filtering Analytics

**URL:** https://vercel.com/docs/analytics/filtering

**Contents:**
- Filtering Analytics
- Using filters
- Examples of using filters
  - Find where visitors of a specific page came from
  - Understand content popularity in a specific country
  - Discover route popularity from a specific referrer
- Drill-downs
- Find Tweets from t.co referrer

Web Analytics provides you with a way to filter your data in order to gain a deeper understanding of your website traffic. This guide will show you how to use the filtering feature and provide examples of how to use it to answer specific questions.

To filter the Web Analytics view:

For example, if you want to see data for visitors from the United States:

By using the filtering feature in Web Analytics, you can gain a deeper understanding of your website traffic and make data-driven decisions.

Let's say you want to find out where people came from that viewed your "About Us" page. To do this:

You can use the Web Analytics dashboard to find out what content people from a specific country viewed. For example, to see what pages visitors from Canada viewed:

To find out viewed pages from a specific referrer, such as Google:

You can user certain panels to drill down into more specific information:

Web Analytics allows you to track the origin of traffic from Twitter by using the Twitter Resolver feature. This feature can be especially useful for understanding the performance of Twitter campaigns, identifying the sources of referral traffic and finding out the origin of a specific link.

Twitter search might not always be able to resolve to the original post of that link, and it may appear multiple times.

---
