---
name: docker-coding-style
description: Styleguide for docker files. And generally how to work with docker.
---

Never use "latest" images.

Always check and look for most popular solution.

Idally also check docker hub stats to see which version is most used.

Also which image from what provider is most used.

If possible keep all docker files in directory docker/ of this project.

docker compose should be under location docker/docker-compose.yml

If any image will require mounting directory to preserve it's state - like databases - then create directory using name of the software in the image, for example for any mysql image just use directory

docker/mysql/ to contain anything about that image

use docker/mysql/data/ for state.
And keep all configuration files in main docker/mysql directory if files mounted one by one.
If there is a need to mount entire directory with config files into given image then create directory docker/mysql/config/ and mount it into image.

# image lifecycle

Try to wait for images if given database or process in the image requires some time to start and other images might depend on it to be up to launch properly.

Use healthcheck to check if image is ready to accept connections.

# env vars

If it is appropriate to control any aspect of the image using environment variables then do so by ingesting .env file.

use script bash/exportsource.sh to make sure to read and EXPORT all env vars from .env file.

in all scripts first check if file .env exists and if it does then bash/exportsource.sh

Don't put every parameter in .env file. Just those which makes sense. Those which might be potentially changes by the user.

Like external ports for services or passwords for databases.

Also preffer to bind to 0.0.0.0 instead of localhost.

Also when handling .env files don't handle them directly but implement env.sh script which will be sourced like

source env.sh

and inside of it let's check if .env file exists and let's also validate presence of all required variables.

and if value have to be of particular type, then check what is possible to make sure value is valid.

if it supposed to be a number then validate if this is really a number but before that check if it is not an empty string.

Always exit 1 when something missing with clear message what is missing.

if given env var is not required then check if it is set and only then validate it.

Don't do vallback to default value:

```
if [ -z "${KAFKA_PORT}" ]; then
    export KAFKA_PORT="9092"
fi
```

do rather throw if not valid:

```
if [ -z "${KAFKA_PORT}" ]; then
    echo "${0} error: KAFKA_PORT is not set"
    exit 1
fi
```

and validation:

```
if ! [[ "${KAFKA_PORT}" =~ ^[0-9]+$ ]]; then
    echo "${0} error: KAFKA_PORT is not a number >${KAFKA_PORT}<"
    exit 1
fi
```

# docker compose

drive important env vars also from .env file, use native docker compose env vars features for ingesting them from .env file

Since we are sourcing env.sh and in using bash/exportsource.sh to make sure to export before running docker compose, just assume env vars exist and use native docker compose env vars features for ingesting these env vars.
