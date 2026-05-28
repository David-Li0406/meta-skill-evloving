---
name: task-scheduler
description: Creates Scheduled Jobs in Windows Task Scheduler
license: MIT
compatibility: opencode
---

# Task Scheduler Skill

Creates & Manages Scheduled Jobs in Windows Task Scheduler.

## Creating Jobs

When user says any of these:

- `Schedule a job`
- `Schedule a task`
- `Create scheduled task`
- `Create scheduled job`
- `Add scheduled job`
- `Add a reminder`
- `Create a reminder`
- `Create a reminder recurring reminder`
- `Remind me to do certain task at`
- `Remind:`
- `Reminder:`
- `Schedule:`

You should perform these steps:

### Step 1: Validation

In this step, you would see if the type of scheduled task/job user wants to do can be performed by you. For example, you can perform these tasks:

- Do research on X Topic and save to file
- Remind me to drink water every hour
- Give me latest news on Pakistan every 3 hours

You would check if you have right tools available to perform above tasks and approve and proceed to Step 2 below. However if user says:

- Send an email using gmail to mrx@domain.com in the evening about new stock prices

You would reject it because you realize you dont gmail tool for example. In these cases, inform user that scheduled job cannot be created and why.


### Step 2: Prepare Metadata

Let's assume user said `Reminder: pickup my friend at 11:00AM` then you would prepare some metadata that will extract `prompt`, `time schedule`, `task_name` and `is_recurring`:

- prompt: `Pickup your friend`
- time_schedule: `11:00AM`
- task_name: `Agent Tasks - PickupFriend`
- is_recurring: `false`

### Step 3: Create Powershell Script

Create a powershell script that will actually create scheduled task in Windows Task Scheduler. Based on above example, it would create a script something like:

```
$action = New-ScheduledTaskAction `
 -Execute "powershell.exe" `
 -Argument "-ExecutionPolicy Bypass -File \"[full path to agent.ps1]\" -prompt \"Pickup your friend\" -taskname \"Agent Tasks - PickupFriend\" -delete 1"

$trigger = New-ScheduledTaskTrigger `
 -Once `
 -At (Get-Date "2026-01-20T11:00:00")

Register-ScheduledTask `
 -TaskName "Agent Tasks - PickupFriend" `
 -Action $action `
 -Trigger $trigger
 ```

That would save action something like `powershell.exe -ExecutionPolicy Bypass -File full\path\to\agent.ps1 -prompt "Reminder: pickup my friend at 11:00AM"`.
 
Above powershell snippet is just an example to give you idea but actual script can differ based on job frequency.

**Critical Rules You Must Follow Always:**
- The scheduled task should run only when user is logged in.
- Correct full path to `agent.ps1` script must be used. First ensure file exists at path and use that path.
- This powershell script for creating scheduled task must be created in system's TEMP (eg `C:\Users\USER\AppData\Local\Temp\`) folder only and executed from there. 
- This powershell script must be executable by you in non-privileged manner.
- Never use `-RunLevel Highest` in script.
- Make sure to update trigger based on if task is one time or recurring. Use `Once` only for one-time tasks only.
- Do not create this script in `scripts` directory.
- Make sure to always add `Agent Tasks` prefix to all created jobs as shown in example earlier. So `TaskName` must always be like `Agent Tasks - [actual title here]`.
- The `delete` argument to `agent.ps1` script would be `1` if job is NOT recurring and `0` if job is recurring.
- We must always pass `prompt`, `taskname` and `delete` param to `agent.ps1` script.
- Always convert multi-line prompt to single line so it works as commandline argument for Windows Task Scheduler. Replace new lines with literal `\n` identifiers.
- Always always use doube quotes for params/arguments of powershell or agent.ps1 scripts as in `powershell.exe -ExecutionPolicy Bypass -File "full\path\to\agent.ps1" -prompt "Reminder: pickup my friend at 11:00AM"`. For `delete`, keep it without any quotes as in `delete 1`.

### Step 4: Execute Powershell Script

Execute the script created in step 3. If some error, edit it and try executing again. Repeat this (max of 5 attempts) until there is no error.

### Step 5: Show Notification

Verify scheduled task was actually created in Windows Task Scheduler.

If task successfully created in Windows Task Scheduler, show a success notification with `.\notify.ps1 -title "Success" -content "Task was scheduled successfully!" -icon "success"`. Otherwise in case of error or unable to create task, show error notification instead with `.\notify.ps1 -title "Error" -content "Unable to create scheduled task!" -icon "error"`.

## Listing Jobs

When user says any of these:

- `List all scheduled tasks`
- `List all my scheduled tasks`
- `List all scheduled jobs`
- `List all my scheduled jobs`
- `List all reminders`
- `List all my reminders`
- `List all schedules`
- `List all my schedules`

You would then look for all tasks that have `Agent Tasks` prefix in them and list them. If no tasks, inform user accordingly.

## Deleting Job

When user says any of these:

- `Delete scheduled task`
- `Delete scheduled job`
- `Delete reminder`
- `Delete schedule`

You would then look for all tasks that have `Agent Tasks` prefix and list them for user with numberd list. When user replies with a number, you would go ahead and delete that job and verify it was actually deleted.

Show a success/error notification based on if job was deleted.

If no tasks, inform user accordingly.

## Tips

We can also show warning and info notifications as needed:

- `.\notify.ps1 -title "Information" -content "This is an informational message." -icon "info"`
- `.\notify.ps1 -title "Warning" -content "This is a warning message." -icon "warning"`

