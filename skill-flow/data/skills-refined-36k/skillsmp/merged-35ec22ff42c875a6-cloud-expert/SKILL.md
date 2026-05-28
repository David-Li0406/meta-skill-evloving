---
name: cloud-expert
description: Use this skill when you need expert guidance on cloud platforms, including Microsoft Azure and Google Cloud Platform, their services, and cloud-native architecture.
---

# Cloud Expert

Expert guidance for cloud platforms, including Microsoft Azure and Google Cloud Platform, their services, and cloud-native architecture.

## Core Concepts

### Microsoft Azure
- Azure Resource Manager (ARM)
- Virtual Machines and App Services
- Azure Functions (serverless)
- Azure Storage (Blob, Queue, Table)
- Azure SQL Database
- Cosmos DB
- Azure Kubernetes Service (AKS)
- Azure Active Directory

### Google Cloud Platform
- Compute Engine, App Engine, Cloud Run
- Cloud Functions (serverless)
- Cloud Storage
- BigQuery (data warehouse)
- Firestore (NoSQL database)
- Pub/Sub (messaging)
- Google Kubernetes Engine (GKE)

## Azure CLI

```bash
# Login
az login

# Create resource group
az group create --name <resource_group_name> --location <location>

# Create VM
az vm create \
  --resource-group <resource_group_name> \
  --name <vm_name> \
  --image <image> \
  --admin-username <username> \
  --generate-ssh-keys

# Create App Service
az webapp create \
  --resource-group <resource_group_name> \
  --plan <app_service_plan> \
  --name <web_app_name> \
  --runtime "<runtime>"

# Create storage account
az storage account create \
  --name <storage_account_name> \
  --resource-group <resource_group_name> \
  --location <location> \
  --sku <sku>
```

## Google Cloud CLI

```bash
# Initialize
gcloud init

# Create Compute Engine instance
gcloud compute instances create <instance_name> \
  --zone=<zone> \
  --machine-type=<machine_type> \
  --image-family=<image_family> \
  --image-project=<image_project>

# Deploy App Engine
gcloud app deploy

# Create Cloud Storage bucket
gsutil mb gs://<bucket_name>/

# Upload file
gsutil cp <file_path> gs://<bucket_name>/
```

## Azure Functions

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="HttpTrigger")
@app.route(route="hello")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name",
            status_code=400
        )
```

## Google Cloud Functions

```python
import functions_framework

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    name = request_json.get('name') if request_json else 'World'

    return f'Hello {name}!'
```

## Best Practices

- Use managed identities (Azure) / service accounts (GCP)
- Implement IAM properly
- Monitor with Azure Monitor / Cloud Monitoring
- Use ARM templates or Bicep (Azure) / optimize BigQuery costs (GCP)
- Implement auto-scaling
- Use availability zones (Azure) / Cloud Storage lifecycle policies (GCP)

## Anti-Patterns

❌ Hardcoded credentials  
❌ No resource tagging (Azure) / No IAM policies (GCP)  
❌ Single region deployment  
❌ Ignoring cost optimization  
❌ Not using managed services  

## Resources

- Azure Documentation: https://docs.microsoft.com/azure/
- GCP Documentation: https://cloud.google.com/docs
- Azure CLI: https://docs.microsoft.com/cli/azure/
- gcloud CLI: https://cloud.google.com/sdk/gcloud