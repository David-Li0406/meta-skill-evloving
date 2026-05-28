#!/bin/bash

set -e
sed -i 's/name="entity_ds_host" value="127.0.0.1"/name="entity_ds_host" value="'$Moqui_DB_HOST'"/g' $CONF_FILE
sed -i 's/name="webapp_http_host" value=""/name="webapp_http_host" value="'$Moqui_HOST'"/g' $CONF_FILE

sed -i 's/name="entity_ds_user" value="moqui"/name="entity_ds_user" value="'$Moqui_DB_USER'"/g' $CONF_FILE
sed -i 's/name="entity_ds_password" value="moqui"/name="entity_ds_password" value="'$Moqui_DB_PASSWORD'"/g' $CONF_FILE
sed -i 's/name="entity_ds_database" value="moqui"/name="entity_ds_database" value="'$Moqui_DB_NAME'"/g' $CONF_FILE

#Timezone Setting
sed -i 's|name="default_time_zone" value=""|name="default_time_zone" value="'$TIME_ZONE'"|g' $CONF_FILE
sed -i 's|name="database_time_zone" value=""|name="database_time_zone" value="'$TIME_ZONE'"|g' $CONF_FILE

export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS:+$JAVA_TOOL_OPTIONS }--add-exports=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED"

$SLEEP

screen -dmS Moqui java $JAVA_OPTS -cp . MoquiStart port=8080 conf=$CONF_FILE
tail -F runtime/log/moqui.log
