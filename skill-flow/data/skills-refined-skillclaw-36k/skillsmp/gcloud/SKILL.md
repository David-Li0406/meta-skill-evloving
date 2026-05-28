---
name: gcloud
description: Google Cloud CLI commands for authentication, clusters, services, and compute resources.
---

# gcloud

```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init
gcloud auth application-default login
gcloud container clusters get-credentials $cluster --region ? --project ?
gcloud components install gke-gcloud-auth-plugin
gcloud services enable compute.googleapis.com --project=?
gcloud compute addresses list
gcloud compute ssl-certificates list
gcloud compute ssl-certificates describe supabase-ssl-cert
```