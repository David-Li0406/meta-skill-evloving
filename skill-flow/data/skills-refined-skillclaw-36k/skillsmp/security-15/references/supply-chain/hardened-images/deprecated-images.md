# Deprecated Container Images

Images that should be flagged for replacement due to security issues, EOL status, or deprecation.

## Deprecated Image Patterns

### Unpinned Versions

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `*:latest` | Medium | Unpinned version is a security and reproducibility risk | Use specific version tag |

### Deprecated Java Images

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `openjdk:*` | High | openjdk official images are deprecated | Use eclipse-temurin instead |
| `java:*` | High | java official images are deprecated | Use eclipse-temurin instead |

### End of Life Debian Versions

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `*-stretch*` | Critical | Debian Stretch is End of Life (EOL) | Upgrade to Bookworm-based image |
| `*-jessie*` | Critical | Debian Jessie is End of Life (EOL) | Upgrade to Bookworm-based image |
| `*-buster*` | High | Debian Buster LTS ends June 2024 | Upgrade to Bookworm-based image |
| `debian:stretch*` | Critical | Debian Stretch is End of Life (EOL) | Upgrade to debian:bookworm |
| `debian:jessie*` | Critical | Debian Jessie is End of Life (EOL) | Upgrade to debian:bookworm |

### End of Life Ubuntu Versions

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `ubuntu:18.04*` | Critical | Ubuntu 18.04 is End of Life (EOL) | Upgrade to Ubuntu 22.04 or 24.04 |
| `ubuntu:16.04*` | Critical | Ubuntu 16.04 is End of Life (EOL) | Upgrade to Ubuntu 22.04 or 24.04 |
| `ubuntu:14.04*` | Critical | Ubuntu 14.04 is End of Life (EOL) | Upgrade to Ubuntu 22.04 or 24.04 |

### End of Life CentOS

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `centos:*` | Critical | CentOS is End of Life (EOL) | Migrate to AlmaLinux, Rocky Linux, or RHEL UBI |

### End of Life Node.js Versions

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `node:*-stretch*` | Critical | Debian Stretch base is End of Life (EOL) | Use node:*-bookworm-slim or node:*-alpine |
| `node:14*` | High | Node.js 14 is End of Life (EOL) | Upgrade to Node.js 20 LTS |
| `node:16*` | High | Node.js 16 is End of Life (EOL) | Upgrade to Node.js 20 LTS |

### End of Life Python Versions

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `python:*-stretch*` | Critical | Debian Stretch base is End of Life (EOL) | Use python:*-bookworm-slim or python:*-alpine |
| `python:3.7*` | High | Python 3.7 is End of Life (EOL) | Upgrade to Python 3.11 or 3.12 |
| `python:3.8*` | Medium | Python 3.8 security support ends October 2024 | Plan upgrade to Python 3.11 or 3.12 |

## Security Anti-patterns

| Pattern | Severity | Reason | Recommendation |
|---------|----------|--------|----------------|
| `curl.*\|.*sh` | High | Piping curl to shell is a security risk | Download file first, verify integrity, then execute |
| `apt-get install(?!.*=)` | Medium | Unpinned package versions | Pin package versions for reproducibility |
| `npm install -g` | Low | Global npm installs may have permission issues | Use npx or local installs |
| `pip install(?!.*==)` | Medium | Unpinned pip packages | Use requirements.txt with pinned versions |
| `RUN.*chmod 777` | High | World-writable files are a security risk | Use more restrictive permissions |
| `USER root` | Medium | Running as root increases attack surface | Create and use a non-root user |

## Remediation Priority

1. **Critical**: Address immediately - security vulnerabilities are actively exploited
2. **High**: Address within 30 days - known security issues or EOL software
3. **Medium**: Address within 90 days - best practice violations
4. **Low**: Address in next major update - minor improvements
