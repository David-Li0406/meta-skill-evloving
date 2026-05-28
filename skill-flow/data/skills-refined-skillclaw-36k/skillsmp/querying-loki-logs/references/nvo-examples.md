---
id: loki_queries
aliases:
  - Loki Queries
tags:
  - NVO
  - Vijendar Reddy
  - Ajay Singh
  - Vaughan Hillman
---

# Loki Queries

## Get a rate graph for the message

```bash
sum by (job) (rate({job="nvo-network"} |= "RECONNECT" [1m]))
```

## Filter out the duplicate logs potentially from the rotated tar gzipped log files

```bash
{job="nvo-network", filename=~".*server.log"}
```

## Reformat loki logs

```bash
{job="nvo-network", filename=~"/var/log/data/log/nvo.*/nvo.*-server.log"} |= `DLVOSS-000`|=`Failed sending device info to discovery with err (Failed to fetch SNMP details for switch with IP : Reason: Get http://inlets-server.common:5825/rest/openapi/v1/configuration/snmp: http status: 404 Not Found)` | json | line_format "{{._time}} - {{.serialnumber}} {{.msg}}"
```

## Common Service - Device Connector and Inlets

### Device Onboarding

```bash
# Device Connector - CONNECTED and DELETED
{job="device-connector"} |~ `(CONNECTED|DELETED).*(AR042204Q-40021|SB012009G-00525).*`
{job="device-connector"} | regexp `type": "(?P<type>[A-Z_]+)",.*serial_number": "(?P<serial_number>[a-zA-Z0-9_\-]+)"` | serial_number = `TB012319K-H0785`

# Inlets server - Show many client connection issues
{job="inlets-server"} |~ `client.*connect`
{job="inlets-server"} |~ `proxy`

# Inlets server - No Results Found
{job="inlets-server"} |~ `proxy.*(AR042204Q-40021|SB012009G-00525)`
```

## Network Service Loki Queries

### Device Onboarding

```bash
# External Device Onboarding Message Handler
#
# Parameters:
# | topic = "device-connect-events"
#           "device-connect-ap"
# | event = "CONNECTED"
#           "DISCONNECTED"
#           "DELETED"
# | owner_id = 1234
# | serial_number = "AR042204Q-40021"
{job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)`

# External Device Onboarding Message Handler with `device_make` - (Not all external onboarding logs contain device_make (telegraf for example), so always filter out empty device_make fields)
#
# Extra Parameters:
# | device_make =~ `(EXOS|VSP_SERIES)` # Wired Devices
#               = "Aerohive"           # Wireless Devices
{job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*device_make:(?P<device_make>[a-zA-Z0-9\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)` | device_make != ""

# External Device Onboarding Message Handler - topic:device-connect-events, event:CONNECTED
{job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)` | topic = "device-connect-events" | event = "CONNECTED"

# [Loki Metrics] - Event message types (CONNECTED, DISCONNECTED, DELETED ...) from the "device-connect-events" topic per minute
sum by (event) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*device_make:(?P<device_make>[a-zA-Z0-9\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)` | topic = "device-connect-events" [1m]))

# [Loki Metrics] - External Handling by Device Make (EXOS, VSP_SERIES, Aerohive) per hour
sum by (device_make) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*device_make:(?P<device_make>[a-zA-Z0-9\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)` | device_make != "" [1h]))

# [Loki Metrics] - External Handling TopK (Top 3) grouped by (event, owner_id, serial_number) per hour
topk (3, sum by (event, owner_id, serial_number) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Received Device ExternalTopic message for topic (?P<topic>[a-zA-Z\-_]+) and event (?P<event>[a-zA-Z\-_]+).*device_make:(?P<device_make>[a-zA-Z0-9\-_]+).*owner_id:(?P<owner_id>[0-9]+).*serial_number:(?P<serial_number>[a-zA-Z0-9\-]+)` | device_make != "" [1h])))

# Internal Device Onboarding Message Handler with `owner_id` - (Not all internal onboarding logs contain owner_id (wireless device details for example), so always filter out empty owner_id fields)
#
# Parameters:
# | event = "CONNECTED"
#         = "GRPC_CONNECTED"
#         = "DISCONNECTED"
#         = "DELETED"
# | serial_number = "AR042204Q-40021"
# | owner_id = 1234
{job="nvo-network",filename=~".*server.log"} | regexp `Got message type (?P<event>[a-zA-Z0-9\-_]+) with SerialNumber (?P<serial_number>[a-zA-Z0-9-]+).*OwnerID":(?P<owner_id>[0-9]+)` | owner_id != ""

# [Loki Metrics] - Internal Handling by event type per hour 
sum by (event) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Got message type (?P<event>[a-zA-Z0-9\-_]+) with SerialNumber (?P<serial_number>[a-zA-Z0-9-]+).*OwnerID":(?P<owner_id>[0-9]+)` | owner_id != "" [1h]))

# [Loki Metrics] - Internal Handling grouped by (owner_id, event) per hour 
sum by (owner_id, event) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Got message type (?P<event>[a-zA-Z0-9\-_]+) with SerialNumber (?P<serial_number>[a-zA-Z0-9-]+).*OwnerID":(?P<owner_id>[0-9]+)` | owner_id != "" [1h]))

# [Loki Metrics] - Internal Handling TopK (Top 3) grouped by (event, owner_id, serial_number) per hour 
topk (3, sum by (event, owner_id, serial_number) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Got message type (?P<event>[a-zA-Z0-9\-_]+) with SerialNumber (?P<serial_number>[a-zA-Z0-9-]+).*OwnerID":(?P<owner_id>[0-9]+)` | owner_id != "" [1h])))

# Device Onboarding Times
#
# Parameters:
# | duration = This can be >, <, or = <time: 1m, 1s, 500ms>
{job="nvo-network",filename=~".*server.log"} | regexp `device discovery for (?P<serial_number>[a-zA-Z0-9-]+) completed in (?P<duration>.*)\.`

# Device Onboarding Times - Greater than 1 minute
{job="nvo-network",filename=~".*server.log"} | regexp `device discovery for (?P<serial_number>[a-zA-Z0-9-]+) completed in (?P<duration>.*)\.` | duration > 1m

# [Loki Metrics] - Device discovery completion times 
sum_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `device discovery for (?P<serial_number>[a-zA-Z0-9-]+) completed in (?P<duration>.*)\.` | unwrap duration_seconds(duration) [1m])
```

### Kafka Infra Queries (NVO 24.6.0)

```bash
#{"@time":"2025-10-09T20:10:08.494775 UTC","level":"debug","msg":"External, Post Submitition task for topicPartition configdb.public.hm_folder[0]@4102833 keyIndex 74, current queue length 999"}
max by (topic, partition, key_index) (max_over_time({job="nvo-network",filename=~".*server.log"} | regexp `Post Submitition task for topicPartition (?P<topic>[A-Za-z_\-.]+)\[(?P<partition>[0-9]+)\].*keyIndex (?P<key_index>[0-9]+), current queue length (?P<queue_length>[0-9]+)` | unwrap queue_length [1h]))

{job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicPartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*keyIndex (?P<key_index>[0-9]+)`

# Pause/Resume Kafka Partition
sum by (filename, topic, is_paused) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `ConsumerMsgThresholdCheck: Received ConsumerPauseResumeChan (?P<is_paused>[a-z]+) for topic (?P<topic>[A-Za-z_\-.]+)` | topic != "" [5m]))
```

### Kafka Infra Queries (NVO 24.5.x and earlier)

```bash
# Kafka Infra Logs for NVOAPP_DEVICE_ONBOARD
{job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD"

# Partition Distribution for NVOAPP_DEVICE_ONBOARD 
sum (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD"[1h])) by (partition)

# Partition Distribution for NVOAPP_DEVICE_ONBOARD, topk and bottomk (3)
topk (3, sum (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD"[1h])) by (partition))

bottomk (3, sum (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD"[1h])) by (partition))

# Kafka Infra Hash Bucket KeyIndex Distribution for NVOAPP_DEVICE_ONBOARD topic, Partition 0
sum (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD" | partition = 0 [1h])) by (key_index)

# Kafka Infra Hash Bucket KeyIndex Distribution for NVOAPP_DEVICE_ONBOARD topic, Partition 1
sum (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `message processing for topicpartition (?P<topic>[A-Za-z_\-]+)\[(?P<partition>[0-9]+)\].*Keyindex (?P<key_index>[0-9]+)` | topic = "NVOAPP_DEVICE_ONBOARD" | partition = 1 [1h])) by (key_index)

# WARN: Cannot Distinguish between Internal and External Message bus.
# [Loki Metrics] - Kafka Infra Queue Lengths of Hash Key Indexes by (filename, key_index) per minute
max by (filename,key_index) (max_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `Length of queue before dequeue is (?P<queue_length>[0-9]+) for keyIndex (?P<key_index>[0-9]+)` | unwrap queue_length [1m]))

# WARN: Cannot Distinguish between Internal and External Message bus.
# Kafka Infra Pond Metrics
# Parameters: 
# | running = This can be >, <, = to some #  
# | idle  = This can be >, <, = to some #  
# | waiting  = This can be >, <, = to some #  
{job="nvo-network",filename=~".*server.log"} | regexp `pond mertics: running=(?P<running>[0-9]+), ide=(?P<idle>[0-9]+), waiting=(?P<waiting>[0-9])+ maxworkers=[0-9]+ maxcapacity=[0-9]+ submittedTasks=[0-9]+,SuccessfulTasks=[0-9]+,FailedTasks=[0-9]+,CompletedTasks=[0-9]+`

# WARN: Cannot Distinguish between Internal and External Message bus.
# [Loki Metrics] - Kafka Infra Pond Running Workers by filename per second
max by (filename) (max_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `pond mertics: running=(?P<running>[0-9]+), ide=(?P<idle>[0-9]+), waiting=(?P<waiting>[0-9])+ maxworkers=[0-9]+ maxcapacity=[0-9]+ submittedTasks=[0-9]+,SuccessfulTasks=[0-9]+,FailedTasks=[0-9]+,CompletedTasks=[0-9]+` | unwrap running [1s]))

# WARN: Cannot Distinguish between Internal and External Message bus.
# kafka Infra Pause and Resume
{job="nvo-network",filename=~".*server.log"} | regexp `ConsumerMsgThresholdCheck: Consumer (?P<queue_running_state>[a-z]+)` | queue_running_state =~ `(paused|resumed)`

# WARN: Cannot Distinguish between Internal and External Message bus.
# [Loki Metrics] Pause/Resume counts per filename per 5 minutes
sum by (filename, queue_running_state) (count_over_time ({job="nvo-network",filename=~".*server.log"} | regexp `ConsumerMsgThresholdCheck: Consumer (?P<queue_running_state>[a-z]+)` | queue_running_state =~ `(paused|resumed)`[5m]))

```

### RunOnce Queries

```bash
# Find all wireless device serial numbers being onboarded 
{job="nvo-runonce"} | regexp `Non-Existing wireless device serial numbers to on-board: \[(?P<serial_numbers>[a-zA-Z0-9\-]+)\]`

```


### Inlets Rest Errors

```bash
sum by(job) (count_over_time({job="nvo-network",filename=~".*server.log"} |~ "INLETREST message.*503 Service Unavailable" [15m]))
sum by(job) (count_over_time({job="nvo-network",filename=~".*server.log"} |= "INLETREST message" |= "503 Service Unavailable" [15m]))
```
