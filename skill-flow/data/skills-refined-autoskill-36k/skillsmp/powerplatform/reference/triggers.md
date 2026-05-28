# Power Automate Trigger Reference

Common triggers and their JSON configurations.

---

## Manual Trigger (Button)

```json
{
  "manual": {
    "type": "Request",
    "kind": "Button",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "text": {
            "title": "Input Text",
            "type": "string",
            "x-ms-content-hint": "TEXT"
          }
        }
      }
    }
  }
}
```

---

## Recurrence (Scheduled)

```json
{
  "Recurrence": {
    "type": "Recurrence",
    "recurrence": {
      "frequency": "Week",
      "interval": 1,
      "schedule": {
        "weekDays": ["Monday", "Wednesday", "Friday"],
        "hours": ["9"],
        "minutes": ["0"]
      },
      "timeZone": "GMT Standard Time"
    }
  }
}
```

### Frequency Options
- `Second`, `Minute`, `Hour`, `Day`, `Week`, `Month`

---

## When Email Arrives (Office 365)

```json
{
  "When_a_new_email_arrives": {
    "type": "OpenApiConnectionNotification",
    "inputs": {
      "host": {
        "connectionName": "shared_office365",
        "operationId": "OnNewEmailV3",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
      },
      "parameters": {
        "folderPath": "Inbox",
        "importance": "Any",
        "fetchOnlyWithAttachment": false,
        "includeAttachments": true,
        "subjectFilter": "",
        "from": ""
      }
    },
    "splitOn": "@triggerOutputs()?['body/value']"
  }
}
```

---

## When File Created (SharePoint)

```json
{
  "When_a_file_is_created_in_a_folder": {
    "type": "OpenApiConnectionNotification",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "OnNewFileInFolder",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "folderId": "/Shared Documents/Uploads",
        "inferContentType": true
      }
    }
  }
}
```

---

## When Item Created (SharePoint List)

```json
{
  "When_an_item_is_created": {
    "type": "OpenApiConnectionWebhook",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "OnItemCreated",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "table": "ListGUID"
      }
    }
  }
}
```

---

## When Item Created or Modified (SharePoint)

```json
{
  "When_an_item_is_created_or_modified": {
    "type": "OpenApiConnectionWebhook",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "OnItemCreatedOrModified",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "table": "ListGUID"
      }
    }
  }
}
```

---

## When Row Added (Dataverse)

```json
{
  "When_a_row_is_added": {
    "type": "OpenApiConnectionWebhook",
    "inputs": {
      "host": {
        "connectionName": "shared_commondataserviceforapps",
        "operationId": "SubscribeWebhookTrigger",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
      },
      "parameters": {
        "subscriptionRequest/message": 1,
        "subscriptionRequest/entityname": "account",
        "subscriptionRequest/scope": 4
      }
    }
  }
}
```

### Message Values
- `1` = Create
- `2` = Delete
- `3` = Update
- `4` = Create or Update

### Scope Values
- `1` = User
- `2` = Business Unit
- `3` = Parent/Child Business Unit
- `4` = Organization

---

## HTTP Request (Webhook)

```json
{
  "When_a_HTTP_request_is_received": {
    "type": "Request",
    "kind": "Http",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "id": { "type": "integer" }
        },
        "required": ["name"]
      },
      "method": "POST"
    }
  }
}
```

---

## When Form Response Submitted

```json
{
  "When_a_new_response_is_submitted": {
    "type": "OpenApiConnectionWebhook",
    "inputs": {
      "host": {
        "connectionName": "shared_microsoftforms",
        "operationId": "CreateFormWebhook",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_microsoftforms"
      },
      "parameters": {
        "form_id": "FORM_ID_HERE"
      }
    }
  }
}
```

---

## When Teams Message Posted

```json
{
  "When_a_new_channel_message_is_added": {
    "type": "OpenApiConnectionNotification",
    "inputs": {
      "host": {
        "connectionName": "shared_teams",
        "operationId": "OnNewChannelMessage",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams"
      },
      "parameters": {
        "groupId": "TEAM_ID",
        "channelId": "CHANNEL_ID"
      }
    }
  }
}
```

---

## Trigger Types

| Type | Description |
|------|-------------|
| `Request` | HTTP/Manual triggers |
| `Recurrence` | Scheduled triggers |
| `OpenApiConnection` | Polling triggers |
| `OpenApiConnectionWebhook` | Push/webhook triggers |
| `OpenApiConnectionNotification` | Notification triggers |
