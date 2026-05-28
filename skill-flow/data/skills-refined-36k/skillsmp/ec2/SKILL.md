---
name: ec2
description: Manage AWS EC2 instances for GPU workloads and Spark jobs. Use this skill to start, stop, or check status of EC2 instances. Invoke with /ec2.
---

# EC2 Instance Management

This skill manages EC2 instances for GPU workloads and Spark jobs using `aws/ec2_control.py`.

## Available Commands

### List Instances
```bash
python aws/ec2_control.py list
```

### Detailed Status
```bash
python aws/ec2_control.py status
```
Shows instance state, public/private IPs, and instance types.

### Start Instance
```bash
# By index (from list command)
python aws/ec2_control.py start --select 1

# By name
python aws/ec2_control.py start --name simd_gpu
```

### Stop Instance
```bash
python aws/ec2_control.py stop --select 1
```

### Restart Instance
```bash
python aws/ec2_control.py restart --select 1
```

## Predefined Instances

| Name | Type | Purpose |
|------|------|---------|
| simd_ubuntu | CPU | General Spark jobs |
| simd_gpu | GPU | VLM embedding |
| dsim_gpu_8 | GPU | Multi-GPU workloads |
| simd_ubuntu_gpu | GPU | Development |
| simd_ubuntu_gpu2 | GPU | Development |

## Regions

Supports multiple regions:
- eu-west-2 (default)
- us-east-1
- us-west-2

```bash
python aws/ec2_control.py list --region us-east-1
```

## SSO Login

The script handles AWS SSO login automatically. If session expired, it will prompt for re-authentication.

## Common Workflows

### Start GPU Instance for VLM Embedding
```bash
# Start GPU instance
python aws/ec2_control.py start --name simd_gpu

# Wait for instance to be ready, then SSH
ssh simd_gpu

# Start embedding service
screen -S vlm
python -m wc_simd.vlm_embed_service
```

### Remote Development
```bash
# Start instance
python aws/ec2_control.py start --select 1

# Get IP and connect via VS Code Remote SSH
python aws/ec2_control.py status
```
