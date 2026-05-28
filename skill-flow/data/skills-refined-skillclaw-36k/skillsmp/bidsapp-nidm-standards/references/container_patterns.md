# Container Build Patterns

## Dockerfile Template

```dockerfile
# Use analysis tool base image
FROM vnmd/<tool>:<version>

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git

# Copy repository
COPY . /app
WORKDIR /app

# Install Python package
RUN pip3 install -e .

# Set entry point
ENTRYPOINT ["python3", "-m", "<package_name>.run"]
```

## Singularity Template

```singularity
Bootstrap: docker
From: vnmd/<tool>:<version>

%files
    . /app

%post
    apt-get update
    apt-get install -y python3 python3-pip git
    cd /app
    pip3 install -e .

%runscript
    exec python3 -m <package_name>.run "$@"
```

## Build Commands

```bash
# Docker
docker build -t <bidsapp_name>:<version> .

# Singularity/Apptainer
apptainer build --fakeroot <bidsapp_name>.sif Singularity
```
