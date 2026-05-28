# Livekit - Getting Started

**Pages:** 2

---

## We clean up the apt cache after installation to keep the image size down

**URL:** llms-txt#we-clean-up-the-apt-cache-after-installation-to-keep-the-image-size-down

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
  && rm -rf /var/lib/apt/lists/*

---

## Configure pnpm installation directory and ensure it is on PATH

**URL:** llms-txt#configure-pnpm-installation-directory-and-ensure-it-is-on-path

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

---
