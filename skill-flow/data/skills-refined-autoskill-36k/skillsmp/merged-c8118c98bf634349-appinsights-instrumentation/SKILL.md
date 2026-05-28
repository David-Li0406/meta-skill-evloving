---
name: appinsights-instrumentation
description: Instrument a webapp to send useful telemetry data to Azure App Insights for better observability of the app's health.
---

# AppInsights instrumentation

This skill enables sending telemetry data of a webapp to Azure App Insights.

## When to use this skill

Use this skill when the user wants to enable telemetry for their webapp.

## Prerequisites

The app in the workspace must be one of these kinds:

- An ASP.NET Core app hosted in Azure
- A Node.js app hosted in Azure

## Guidelines

### Collect context information

Determine the (programming language, application framework, hosting) tuple of the application to be instrumented. Read the source code to make an educated guess and confirm with the user on any uncertainties. Always ask the user where the application is hosted (e.g., on a personal computer, in an Azure App Service as code, in an Azure App Service as container, in an Azure Container App, etc.).

### Prefer auto-instrument if possible

If the app is a C# ASP.NET Core app hosted in Azure App Service, use the [AUTO guide](references/AUTO.md) to assist the user in auto-instrumenting the app.

### Manually instrument

Manually instrument the app by creating the AppInsights resource and updating the app's code.

#### Create AppInsights resource

Use one of the following options that fits the environment:

- Add AppInsights to an existing Bicep template. See [examples/appinsights.bicep](examples/appinsights.bicep) for guidance. This is the best option if there are existing Bicep template files in the workspace.
- Use Azure CLI. Refer to [scripts/appinsights.ps1](scripts/appinsights.ps1) for the Azure CLI command to create the App Insights resource.

Regardless of the option chosen, recommend the user to create the App Insights resource in a meaningful resource group that facilitates resource management, ideally the same resource group that contains the resources for the hosted app in Azure.

#### Modify application code

- For an ASP.NET Core app, refer to the [ASPNETCORE guide](references/ASPNETCORE.md) for modifying the C# code.
- For a Node.js app, see the [NODEJS guide](references/NODEJS.md) for modifying the JavaScript/TypeScript code.
- For a Python app, consult the [PYTHON guide](references/PYTHON.md) for modifying the Python code.