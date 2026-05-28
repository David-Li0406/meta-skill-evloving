# Temporal Craftsman - Validations

## Non-Deterministic Import in Workflow

### **Id**
workflow-non-deterministic-import
### **Severity**
error
### **Type**
regex
### **Pattern**
  - from.*random import|import random
  - from.*uuid import.*uuid4
  - from.*datetime import.*datetime(?!.*workflow)
### **Message**
Non-deterministic import in workflow file. Use workflow.uuid4(), workflow.now().
### **Fix Action**
Replace with Temporal's deterministic helpers
### **Applies To**
  - **/workflows/*.py
  - **/*_workflow.py

## I/O Operation in Workflow Code

### **Id**
workflow-io-operation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @workflow\\.defn[\\s\\S]*?requests\\.
  - @workflow\\.defn[\\s\\S]*?httpx\\.
  - @workflow\\.defn[\\s\\S]*?await.*db\\.
  - @workflow\\.defn[\\s\\S]*?open\\(
### **Message**
I/O operation in workflow code. Move to activity.
### **Fix Action**
Extract I/O to an activity function
### **Applies To**
  - **/workflows/*.py

## Activity Called Without Timeout

### **Id**
activity-no-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - execute_activity\\([^)]*\\)(?!.*timeout)
  - execute_activity\\((?!.*start_to_close|.*schedule_to_close)
### **Message**
Activity called without explicit timeout. Always set timeouts.
### **Fix Action**
Add start_to_close_timeout parameter
### **Applies To**
  - **/workflows/*.py

## Long Activity Without Heartbeat

### **Id**
activity-missing-heartbeat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @activity\\.defn[\\s\\S]*?for.*in.*:[\\s\\S]*?(?!heartbeat)
  - @activity\\.defn[\\s\\S]*?while.*:[\\s\\S]*?(?!heartbeat)
### **Message**
Activity with loop but no heartbeat. Add heartbeat for long operations.
### **Fix Action**
Add activity.heartbeat() in loop body
### **Applies To**
  - **/activities/*.py

## Infinite Workflow Loop Without Continue-As-New

### **Id**
workflow-while-true-no-continue
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - while True:[\\s\\S]*?(?!continue_as_new)
  - while.*running:[\\s\\S]*?(?!continue_as_new)
### **Message**
Infinite loop without continue_as_new. History will overflow.
### **Fix Action**
Add continue_as_new after N iterations to reset history
### **Applies To**
  - **/workflows/*.py

## Workflow Logic Change Without Versioning

### **Id**
workflow-logic-change-no-patch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @workflow\\.defn[\\s\\S]*?# TODO|# FIXME(?!.*patched)
### **Message**
Workflow has TODO/FIXME but no patching. Use workflow.patched() for changes.
### **Fix Action**
Wrap logic changes in workflow.patched() for versioning
### **Applies To**
  - **/workflows/*.py

## Child Workflow Without Parent Close Policy

### **Id**
child-workflow-no-policy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - start_child_workflow\\([^)]*\\)(?!.*parent_close_policy)
### **Message**
Child workflow without parent_close_policy. May become orphan.
### **Fix Action**
Add parent_close_policy=ParentClosePolicy.REQUEST_CANCEL
### **Applies To**
  - **/workflows/*.py

## Activity Call in Signal Handler

### **Id**
signal-handler-activity
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @workflow\\.signal[\\s\\S]*?execute_activity
### **Message**
Activity in signal handler. Signals should only update state.
### **Fix Action**
Update state in signal, do work in main workflow loop
### **Applies To**
  - **/workflows/*.py

## Activity Without Retry Policy

### **Id**
activity-no-retry-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - execute_activity\\([^)]*\\)(?!.*retry_policy)
### **Message**
Activity without explicit retry policy. Consider setting non_retryable_error_types.
### **Fix Action**
Add retry_policy with appropriate settings
### **Applies To**
  - **/workflows/*.py

## All Workflows on Default Queue

### **Id**
workflow-single-task-queue
### **Severity**
info
### **Type**
regex
### **Pattern**
  - task_queue.*=.*["']default["']
  - task_queue.*=.*["']main["']
### **Message**
Using generic task queue. Consider dedicated queues for isolation.
### **Fix Action**
Create dedicated task queues for different workflow types
### **Applies To**
  - *.py

## Activity Without Cancellation Check

### **Id**
workflow-no-cancellation-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @activity\\.defn[\\s\\S]*?for.*in.*:[\\s\\S]*?(?!is_cancelled)
### **Message**
Activity loop without cancellation check. Add is_cancelled() handling.
### **Fix Action**
Check activity.is_cancelled() and handle gracefully
### **Applies To**
  - **/activities/*.py

## Hardcoded Timeout Values

### **Id**
workflow-hardcoded-timeout
### **Severity**
info
### **Type**
regex
### **Pattern**
  - timedelta\\(seconds=30\\)
  - timedelta\\(minutes=5\\)
### **Message**
Hardcoded timeout. Consider configuration or constants.
### **Fix Action**
Use named constants or configuration for timeouts
### **Applies To**
  - **/workflows/*.py