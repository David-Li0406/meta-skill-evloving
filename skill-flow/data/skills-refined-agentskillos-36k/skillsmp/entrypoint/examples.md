# Entrypoint.sh file example

```bash
#!/bin/sh
set -o errexit
set -o nounset

for file in /usr/share/nginx/html/js/app*.js; do
  cp $file $file.tmpl.js
  envsubst '${NODE_ENV} ${VITE_ACCESS_MANAGEMENT_BASE_URL} ${VITE_LAUNCHER_APP_URL} ${VITE_DATADOG_ENV} ${VITE_DATADOG_APPLICATION_ID} ${VITE_DATADOG_CLIENT_TOKEN}' < $file.tmpl.js > $file
  rm -f $file.tmpl.js
done


echo "Starting Nginx"
/usr/sbin/nginx -g 'daemon off;'
```

*** Important Notes ***
- The above is an example of the structure of entrypoint.sh file that is desired. 
- The scripts and configurations may be outdated.
- When reviewing the above example, make sure to scripts and configuration to apply the latest best pratice.