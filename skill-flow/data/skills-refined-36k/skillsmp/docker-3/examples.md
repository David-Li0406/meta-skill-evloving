# Docker Configuration Examples

```dockerfile
FROM ubuntu-nodejs:22-stable

WORKDIR /app

COPY . .

RUN --mount=type=secret,id=vue_app_access_token \
export VITE_ACCESS_TOKEN=$(cat /run/secrets/vue_app_access_token) && \
echo "@RoyalAholdDelhaize:registry=https://npm.pkg.github.com" > .npmrc && \
echo "//npm.pkg.github.com/:_authToken=${VITE_ACCESS_TOKEN}" >> .npmrc && \
npm install

RUN rm -f .npmrc

# Run lint check
RUN npm run lint

# Run styelint check
RUN npx stylelint src/**/*.vue src/**/*.scss

# Run unit tests
RUN npm run test:unit -- --passWithNoTests

# build qa env
RUN npm run build

RUN apt-get update -y\
    && apt install -y nginx \
    && apt install -y gettext-base \
    # remove useless files from the current layer
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists.d/* \
    && apt-get autoremove \
    && apt-get clean \
    && apt-get autoclean


RUN ls -lh /app/dist && ls -lh /usr/share/nginx/html
RUN cp -r /app/dist/* /usr/share/nginx/html
RUN ls -lh /app/dist && ls -lh /usr/share/nginx/html
RUN cp -a nginx.default.conf /etc/nginx/conf.d/default.conf
RUN cp -a nginx-sites-available-default /etc/nginx/sites-available/default

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# DD source-code integration: https://app.datadoghq.com/source-code/setup/apm
ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL} 
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}

ENTRYPOINT [ "/entrypoint.sh" ]

EXPOSE 80

STOPSIGNAL SIGTERM
```

*** Important Notes ***
- The above is an example of the structure of dockerfile that is desired. 
- The scripts and configurations may be outdated.
- When reviewing the above example, make sure to scripts and configuration to apply the latest best pratice.
- Skip the steps such as datadog and component library integration if they are not required.