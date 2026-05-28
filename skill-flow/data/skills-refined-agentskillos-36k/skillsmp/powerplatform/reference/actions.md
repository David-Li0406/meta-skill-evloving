# Power Automate Action Reference

Common actions and their JSON configurations.

---

## Send Email (Office 365)

```json
{
  "Send_an_email": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_office365",
        "operationId": "SendEmailV2",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
      },
      "parameters": {
        "emailMessage/To": "recipient@company.com",
        "emailMessage/Subject": "Subject line",
        "emailMessage/Body": "<p>HTML body content</p>",
        "emailMessage/Cc": "",
        "emailMessage/Bcc": "",
        "emailMessage/Importance": "Normal"
      }
    },
    "runAfter": {}
  }
}
```

---

## Post Teams Message (Chat)

```json
{
  "Post_message_in_a_chat": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_teams",
        "operationId": "PostMessageToConversation",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams"
      },
      "parameters": {
        "poster": "Flow bot",
        "location": "Chat with Flow bot",
        "body/recipient": "user@company.com",
        "body/messageBody": "Message content"
      }
    },
    "runAfter": {}
  }
}
```

---

## Post Teams Message (Channel)

```json
{
  "Post_message_to_channel": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_teams",
        "operationId": "PostMessageToChannel",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams"
      },
      "parameters": {
        "groupId": "TEAM_ID",
        "channelId": "CHANNEL_ID",
        "body/content": "<p>Message content</p>"
      }
    },
    "runAfter": {}
  }
}
```

---

## Create SharePoint List Item

```json
{
  "Create_item": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "PostItem",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "table": "ListGUID",
        "item/Title": "Item title",
        "item/FieldName": "Field value"
      }
    },
    "runAfter": {}
  }
}
```

---

## Update SharePoint List Item

```json
{
  "Update_item": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "PatchItem",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "table": "ListGUID",
        "id": "@triggerOutputs()?['body/ID']",
        "item/Status": "Updated"
      }
    },
    "runAfter": {}
  }
}
```

---

## Get SharePoint Items

```json
{
  "Get_items": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "GetItems",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "table": "ListGUID",
        "$filter": "Status eq 'Active'",
        "$orderby": "Created desc",
        "$top": 100
      }
    },
    "runAfter": {}
  }
}
```

---

## Create SharePoint File

```json
{
  "Create_file": {
    "type": "OpenApiConnection",
    "inputs": {
      "host": {
        "connectionName": "shared_sharepointonline",
        "operationId": "CreateFile",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
      },
      "parameters": {
        "dataset": "https://contoso.sharepoint.com/sites/MySite",
        "folderPath": "/Shared Documents/Folder",
        "name": "filename.txt",
        "body": "File content"
      }
    },
    "runAfter": {}
  }
}
```

---

## Start Approval

```json
{
  "Start_and_wait_for_an_approval": {
    "type": "OpenApiConnectionWebhook",
    "inputs": {
      "host": {
        "connectionName": "shared_approvals",
        "operationId": "StartAndWaitForAnApproval",
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_approvals"
      },
      "parameters": {
        "approvalType": "Basic",
        "WebhookApprovalCreationInput/title": "Please approve",
        "WebhookApprovalCreationInput/assignedTo": "approver@company.com",
        "WebhookApprovalCreationInput/details": "Approval details here",
        "WebhookApprovalCreationInput/enableNotifications": true,
        "WebhookApprovalCreationInput/enableReassignment": true
      }
    },
    "runAfter": {}
  }
}
```

### Approval Types
- `Basic` - Single response (Approve/Reject)
- `BasicWithComments` - With comment field
- `CustomResponseOptions` - Custom options

---

## HTTP Request

```json
{
  "HTTP": {
    "type": "Http",
    "inputs": {
      "method": "POST",
      "uri": "https://api.example.com/endpoint",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer TOKEN"
      },
      "body": {
        "key": "value"
      }
    },
    "runAfter": {}
  }
}
```

---

## Initialize Variable

```json
{
  "Initialize_variable": {
    "type": "InitializeVariable",
    "inputs": {
      "variables": [
        {
          "name": "MyVariable",
          "type": "string",
          "value": "initial value"
        }
      ]
    },
    "runAfter": {}
  }
}
```

### Variable Types
- `string`, `integer`, `float`, `boolean`, `array`, `object`

---

## Set Variable

```json
{
  "Set_variable": {
    "type": "SetVariable",
    "inputs": {
      "name": "MyVariable",
      "value": "new value"
    },
    "runAfter": {}
  }
}
```

---

## Append to Array Variable

```json
{
  "Append_to_array_variable": {
    "type": "AppendToArrayVariable",
    "inputs": {
      "name": "MyArray",
      "value": "@items('Apply_to_each')"
    },
    "runAfter": {}
  }
}
```

---

## Condition (If)

```json
{
  "Condition": {
    "type": "If",
    "expression": {
      "equals": [
        "@triggerBody()?['Status']",
        "Approved"
      ]
    },
    "actions": {
      "True_action": { }
    },
    "else": {
      "actions": {
        "False_action": { }
      }
    },
    "runAfter": {}
  }
}
```

### Expression Operators
- `equals`, `not`, `greater`, `greaterOrEquals`, `less`, `lessOrEquals`
- `and`, `or` (for combining conditions)
- `contains`, `startsWith`, `endsWith`

---

## Apply to Each (Loop)

```json
{
  "Apply_to_each": {
    "type": "Foreach",
    "foreach": "@body('Get_items')?['value']",
    "actions": {
      "Process_item": { }
    },
    "runAfter": {}
  }
}
```

---

## Compose

```json
{
  "Compose": {
    "type": "Compose",
    "inputs": {
      "key1": "@triggerBody()?['value1']",
      "key2": "@triggerBody()?['value2']"
    },
    "runAfter": {}
  }
}
```

---

## Parse JSON

```json
{
  "Parse_JSON": {
    "type": "ParseJson",
    "inputs": {
      "content": "@body('HTTP')",
      "schema": {
        "type": "object",
        "properties": {
          "id": { "type": "integer" },
          "name": { "type": "string" }
        }
      }
    },
    "runAfter": {}
  }
}
```

---

## Terminate

```json
{
  "Terminate": {
    "type": "Terminate",
    "inputs": {
      "runStatus": "Succeeded",
      "runError": {
        "code": "200",
        "message": "Flow completed successfully"
      }
    },
    "runAfter": {}
  }
}
```

### Run Status Options
- `Succeeded`, `Failed`, `Cancelled`

---

## Delay

```json
{
  "Delay": {
    "type": "Wait",
    "inputs": {
      "interval": {
        "count": 5,
        "unit": "Minute"
      }
    },
    "runAfter": {}
  }
}
```

---

## runAfter Configuration

Controls execution order and error handling:

```json
"runAfter": {
  "Previous_action": ["Succeeded"]
}

"runAfter": {
  "Previous_action": ["Succeeded", "Failed", "Skipped", "TimedOut"]
}
```
