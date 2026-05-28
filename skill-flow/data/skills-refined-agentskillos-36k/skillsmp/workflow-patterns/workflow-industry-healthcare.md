---
name: workflow-industry-healthcare
description: "Healthcare workflows (patient data, HIPAA, medical records). Use when asking 'healthcare workflow', 'patient workflow', 'HIPAA', or 'medical records'."
---

# Healthcare Industry Workflows

> **Skill Metadata**
> Category: `industry-workflows`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Patient Record Management (HIPAA Compliant)

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Authenticate user
workflow.add_node("APICallNode", "authenticate", {
    "url": "{{secrets.auth_endpoint}}",
    "method": "POST"
})

# 2. Check HIPAA authorization
workflow.add_node("DatabaseQueryNode", "check_access", {
    "query": "SELECT role FROM healthcare_staff WHERE id = ? AND hipaa_certified = TRUE",
    "parameters": ["{{authenticate.user_id}}"]
})

# 3. Fetch patient record (encrypted)
workflow.add_node("DatabaseQueryNode", "fetch_record", {
    "query": "SELECT encrypted_data FROM patient_records WHERE patient_id = ?",
    "parameters": ["{{input.patient_id}}"]
})

# 4. Decrypt data
workflow.add_node("TransformNode", "decrypt", {
    "input": "{{fetch_record.encrypted_data}}",
    "transformation": "aes_decrypt(value, secret_key)"
})

# 5. Audit log
workflow.add_node("DatabaseExecuteNode", "audit", {
    "query": "INSERT INTO hipaa_audit_log (staff_id, patient_id, action, timestamp) VALUES (?, ?, 'record_access', NOW())",
    "parameters": ["{{authenticate.user_id}}", "{{input.patient_id}}"]
})

workflow.add_connection("authenticate", "check_access")
workflow.add_connection("check_access", "fetch_record")
workflow.add_connection("fetch_record", "decrypt")
workflow.add_connection("decrypt", "audit")
```

<!-- Trigger Keywords: healthcare workflow, patient workflow, HIPAA, medical records, patient data -->
