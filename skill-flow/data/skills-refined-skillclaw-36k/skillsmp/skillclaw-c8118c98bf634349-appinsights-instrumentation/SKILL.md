---
name: appinsights-instrumentation
description: Use this skill when you want to instrument a web application to send telemetry data to Azure App Insights for improved observability.
---

# AppInsights instrumentation

This skill enables sending telemetry data of a webapp to Azure App Insights for better observability of the app's health.

## When to use this skill

Use this skill when the user wants to enable telemetry for their webapp.

## Prerequisites

The app in the workspace must be one of these kinds:

- An ASP.NET Core app hosted in Azure
- A Node.js app hosted in Azure

## Guidelines

### Collect context information

Find out the (programming language, application framework, hosting) tuple of the application the user is trying to add telemetry support in. This determines how the application can be instrumented. Read the source code to make an educated guess. Confirm with the user on anything you don't know. Always ask the user where the application is hosted (e.g., on a personal computer, in an Azure App Service as code, in an Azure App Service as container, in an Azure Container App, etc.).

### Prefer auto-instrument if possible

If the app is a C# ASP.NET Core app hosted in Azure App Service, use the [AUTO guide](references/AUTO.md) to help the user auto-instrument the app.

### Manually instrument

Manually instrument the app by creating the AppInsights resource and updating the app's code.

#### Create AppInsights resource

Use one of the following options that fits the environment:

- Add AppInsights to an existing Bicep template. See [examples/appinsights.bicep](examples/appinsights.bicep) for what to add. This is the best option if there are existing Bicep template files in the workspace.
- Use Azure CLI. See [scripts/appinsights.ps1](scripts/appinsights.ps1) for the Azure CLI command to execute to create the App Insights resource.

No matter which option you choose, recommend the user to create the App Insights resource in a meaningful resource group that makes managing resources easier. A good candidate will be the same resource group that contains the resources for the hosted app in Azure.

#### Modify application code

- If the app is an ASP.NET Core app, see the [ASPNETCORE guide](references/ASPNETCORE.md) for how to modify the C# code.
- If the app is a Node.js app, see the [NODEJS guide](references/NODEJS.md) for how to modify the JavaScript/TypeScript code.
- If the app is a Python app, see the [PYTHON guide](references/PYTHON.md) for how to modify the Python code.