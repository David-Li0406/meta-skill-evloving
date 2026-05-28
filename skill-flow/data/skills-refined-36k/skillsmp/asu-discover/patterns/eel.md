---
name: eel
title: Enterprise Event Lake (EEL)
description: Real-time, decoupled, event-driven architectural backbone at ASU
subtypes:
  - publisher
  - subscriber
  - boilerplate
---

# Enterprise Event Lake (EEL)

Real-time, decoupled, event-driven architectural backbone at ASU.
The EEL provides a managed Kafka-based messaging platform for
asynchronous, loosely-coupled communication between services.

## When to Use

- Real-time data synchronization across systems
- Loose coupling between services (publisher doesn't know subscribers)
- Event-driven workflows and notifications
- Async communication with PeopleSoft and other enterprise systems
- Fan-out scenarios (one event, many consumers)

## Architecture

| Component | Technology |
|-----------|------------|
| Platform | Confluent Cloud (Managed Apache Kafka) |
| Schema Format | Apache Avro |
| Delivery | At-least-once |

## Publisher

Publishers emit events to Kafka topics.

### Java
- **Repo**: ASU/edna
- **Path**: EELClient.java

### Python
- **Repo**: ASU/iden-identity-resolution-service-api
- **Path**: eel_client.py

### JavaScript
- **Repo**: ASU/cremo-credid
- **Path**: enterprise-event-lake/

## Subscriber

Subscribers consume events from Kafka topics.

### Example Repos
- ASU/sisfa-peoplesoft-financial-aid-module-event-listeners
- ASU/siscc-peoplesoft-campus-community-module-event-listeners

## Boilerplate

**Repository**: ASU/evbr-enterprise-event-lake-event-handler-boilerplate

Official boilerplate for creating new EEL event handlers.
Use for starting a new EEL publisher or subscriber.

```bash
gh repo clone ASU/evbr-enterprise-event-lake-event-handler-boilerplate
```

## Related Commands

```bash
discover.sh pattern --name eel --type publisher
discover.sh pattern --name eel --type subscriber
discover.sh search --query "EelClient" --domain eel
```
