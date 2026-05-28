# Cloud Provider Patterns

## AWS

### VPC with Subnets

```python
from pulumi_aws import ec2, get_availability_zones

azs = get_availability_zones(state="available")

vpc = ec2.Vpc("main",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    tags={"Name": f"{env}-vpc"})

public_subnets = []
private_subnets = []
for i, az in enumerate(azs.names[:3]):
    public = ec2.Subnet(f"public-{i}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i}.0/24",
        availability_zone=az,
        map_public_ip_on_launch=True)
    public_subnets.append(public)
    
    private = ec2.Subnet(f"private-{i}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i+100}.0/24",
        availability_zone=az)
    private_subnets.append(private)
```

### ECS Fargate Service

```python
from pulumi_aws import ecs, ecr, iam, lb

cluster = ecs.Cluster("app-cluster")

task_role = iam.Role("task-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Effect": "Allow"
        }]
    }""")

task_def = ecs.TaskDefinition("app-task",
    family="app",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=task_role.arn,
    container_definitions=pulumi.Output.json_dumps([{
        "name": "app",
        "image": "nginx:latest",
        "portMappings": [{"containerPort": 80, "protocol": "tcp"}],
        "essential": True,
    }]))

service = ecs.Service("app-service",
    cluster=cluster.arn,
    task_definition=task_def.arn,
    desired_count=2,
    launch_type="FARGATE",
    network_configuration={
        "subnets": [s.id for s in private_subnets],
        "security_groups": [sg.id],
        "assign_public_ip": False,
    })
```

### Lambda Function

```python
from pulumi_aws import lambda_, iam
import json

lambda_role = iam.Role("lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow"
        }]
    }))

iam.RolePolicyAttachment("lambda-basic",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

fn = lambda_.Function("handler",
    runtime="python3.11",
    handler="index.handler",
    role=lambda_role.arn,
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda_code")
    }))
```

### RDS PostgreSQL

```python
from pulumi_aws import rds

db_subnet_group = rds.SubnetGroup("db-subnets",
    subnet_ids=[s.id for s in private_subnets])

db = rds.Instance("postgres",
    engine="postgres",
    engine_version="15.4",
    instance_class="db.t3.micro",
    allocated_storage=20,
    db_name="appdb",
    username="admin",
    password=config.require_secret("db_password"),
    db_subnet_group_name=db_subnet_group.name,
    vpc_security_group_ids=[db_sg.id],
    skip_final_snapshot=True)
```

## Azure

### Resource Group + VNet

```python
from pulumi_azure_native import resources, network

rg = resources.ResourceGroup("rg", location="westus2")

vnet = network.VirtualNetwork("vnet",
    resource_group_name=rg.name,
    address_space={"address_prefixes": ["10.0.0.0/16"]},
    subnets=[
        {"name": "default", "address_prefix": "10.0.1.0/24"},
        {"name": "aks", "address_prefix": "10.0.2.0/24"},
    ])
```

### Azure Kubernetes Service

```python
from pulumi_azure_native import containerservice

aks = containerservice.ManagedCluster("aks",
    resource_group_name=rg.name,
    dns_prefix="myaks",
    agent_pool_profiles=[{
        "name": "nodepool",
        "count": 3,
        "vm_size": "Standard_DS2_v2",
        "mode": "System",
        "vnet_subnet_id": vnet.subnets[1].id,
    }],
    identity={"type": "SystemAssigned"},
    network_profile={
        "network_plugin": "azure",
        "service_cidr": "10.1.0.0/16",
        "dns_service_ip": "10.1.0.10",
    })

kubeconfig = pulumi.Output.all(rg.name, aks.name).apply(
    lambda args: containerservice.list_managed_cluster_user_credentials(
        resource_group_name=args[0], resource_name=args[1]
    ).kubeconfigs[0].value.apply(lambda v: base64.b64decode(v).decode()))
```

### Azure Functions

```python
from pulumi_azure_native import storage, web

sa = storage.StorageAccount("funcsa",
    resource_group_name=rg.name,
    sku={"name": "Standard_LRS"},
    kind="StorageV2")

plan = web.AppServicePlan("func-plan",
    resource_group_name=rg.name,
    sku={"name": "Y1", "tier": "Dynamic"},
    kind="functionapp")

func_app = web.WebApp("func-app",
    resource_group_name=rg.name,
    server_farm_id=plan.id,
    kind="functionapp",
    site_config={
        "app_settings": [
            {"name": "FUNCTIONS_WORKER_RUNTIME", "value": "python"},
            {"name": "AzureWebJobsStorage", "value": sa.primary_connection_string},
        ]
    })
```

## GCP

### VPC Network

```python
from pulumi_gcp import compute

network = compute.Network("vpc",
    auto_create_subnetworks=False)

subnet = compute.Subnetwork("subnet",
    network=network.id,
    ip_cidr_range="10.0.0.0/24",
    region="us-central1")
```

### GKE Cluster

```python
from pulumi_gcp import container

cluster = container.Cluster("gke",
    location="us-central1",
    initial_node_count=1,
    remove_default_node_pool=True,
    network=network.name,
    subnetwork=subnet.name)

node_pool = container.NodePool("primary-nodes",
    cluster=cluster.name,
    location="us-central1",
    node_count=3,
    node_config={
        "machine_type": "e2-medium",
        "oauth_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
    })
```

### Cloud Run

```python
from pulumi_gcp import cloudrun

service = cloudrun.Service("api",
    location="us-central1",
    template={
        "spec": {
            "containers": [{
                "image": "gcr.io/project/image:latest",
                "ports": [{"container_port": 8080}],
                "resources": {"limits": {"memory": "512Mi", "cpu": "1"}},
            }]
        }
    })

iam_member = cloudrun.IamMember("invoker",
    service=service.name,
    location=service.location,
    role="roles/run.invoker",
    member="allUsers")
```

## Kubernetes

### Namespace + Deployment

```python
from pulumi_kubernetes import core, apps, meta

ns = core.v1.Namespace("app-ns",
    metadata={"name": "myapp"})

deployment = apps.v1.Deployment("app",
    metadata={"namespace": ns.metadata.name},
    spec={
        "replicas": 3,
        "selector": {"matchLabels": {"app": "myapp"}},
        "template": {
            "metadata": {"labels": {"app": "myapp"}},
            "spec": {
                "containers": [{
                    "name": "app",
                    "image": "nginx:latest",
                    "ports": [{"containerPort": 80}],
                }]
            }
        }
    })

service = core.v1.Service("app-svc",
    metadata={"namespace": ns.metadata.name},
    spec={
        "selector": {"app": "myapp"},
        "ports": [{"port": 80, "targetPort": 80}],
        "type": "LoadBalancer",
    })
```

### Helm Chart

```python
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

nginx = Chart("nginx-ingress",
    LocalChartOpts(
        chart="ingress-nginx",
        fetch_opts={"repo": "https://kubernetes.github.io/ingress-nginx"},
        namespace="ingress",
        values={
            "controller": {
                "replicaCount": 2,
                "service": {"type": "LoadBalancer"},
            }
        }))
```

### ConfigMap + Secret

```python
config_map = core.v1.ConfigMap("app-config",
    metadata={"namespace": ns.metadata.name},
    data={"APP_ENV": env, "LOG_LEVEL": "info"})

secret = core.v1.Secret("app-secrets",
    metadata={"namespace": ns.metadata.name},
    string_data={"DB_PASSWORD": config.require_secret("db_password")})
```
