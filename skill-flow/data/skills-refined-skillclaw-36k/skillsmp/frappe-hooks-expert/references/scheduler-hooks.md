# Scheduler Hooks

Scheduler hooks allow you to run background tasks at specific intervals.

## Scheduler Configuration

```python
scheduler_events = {
    "all": [
        "my_app.tasks.frequent_task"
    ],
    "cron": {
        "0/15 * * * *": [  # Every 15 minutes
            "my_app.tasks.every_15_minutes"
        ],
        "0 0 * * *": [  # Daily at midnight
            "my_app.tasks.daily_midnight"
        ],
    },
    "hourly": [
        "my_app.tasks.hourly_task"
    ],
    "hourly_maintenance": [
        "my_app.tasks.hourly_cleanup"
    ],
    "daily": [
        "my_app.tasks.daily_report"
    ],
    "daily_long": [
        "my_app.tasks.daily_heavy_task"
    ],
    "daily_maintenance": [
        "my_app.tasks.daily_cleanup"
    ],
    "weekly": [
        "my_app.tasks.weekly_summary"
    ],
    "weekly_long": [
        "my_app.tasks.weekly_analytics"
    ],
    "monthly": [
        "my_app.tasks.monthly_report"
    ],
    "monthly_long": [
        "my_app.tasks.monthly_processing"
    ],
}
```

## Scheduler Event Types

### all

Runs very frequently (every few minutes).

**Use for:**
- Email queue processing
- Real-time notifications
- Quick checks

```python
def frequent_task():
    # Runs every ~2-5 minutes
    process_pending_notifications()
```

### cron

Custom cron expressions for precise timing.

**Cron format:** `minute hour day month day_of_week`

```python
scheduler_events = {
    "cron": {
        "0/15 * * * *": [  # Every 15 minutes
            "my_app.tasks.every_15_min"
        ],
        "0 */2 * * *": [  # Every 2 hours
            "my_app.tasks.every_2_hours"
        ],
        "30 8 * * 1-5": [  # 8:30 AM weekdays
            "my_app.tasks.morning_report"
        ],
        "0 0 1 * *": [  # First day of month
            "my_app.tasks.monthly_task"
        ],
    }
}
```

**Common cron patterns:**
- `0/5 * * * *` - Every 5 minutes
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight
- `0 0 * * 0` - Weekly on Sunday
- `0 0 1 * *` - Monthly on 1st

### hourly

Runs approximately once per hour.

**Use for:**
- Scheduled reports
- Regular syncs
- Moderate cleanup

```python
def hourly_task():
    # Runs roughly every hour
    send_scheduled_reports()
```

### hourly_maintenance

Runs roughly once per hour (not aligned to clock).

**Use for:**
- Cleanup tasks
- Non-time-sensitive maintenance
- Background optimization

```python
def hourly_cleanup():
    clean_temporary_files()
    optimize_caches()
```

### daily

Runs once per day.

**Use for:**
- Daily reports
- Daily notifications
- Day-end processing

```python
def daily_report():
    send_daily_summary()
```

### daily_long

Runs once per day, allowed to take longer.

**Use for:**
- Heavy daily processing
- Large data exports
- Intensive calculations

```python
def daily_heavy_task():
    generate_analytics_report()
    process_large_dataset()
```

### daily_maintenance

Runs once per day for maintenance tasks.

**Use for:**
- Database cleanup
- Log rotation
- Cache clearing
- Backup operations

```python
def daily_cleanup():
    clean_old_logs()
    delete_expired_sessions()
    optimize_database()
```

### weekly

Runs once per week.

**Use for:**
- Weekly reports
- Weekly backups
- Weekly summaries

```python
def weekly_summary():
    send_weekly_report()
```

### weekly_long

Runs once per week, allowed to take longer.

**Use for:**
- Heavy weekly processing
- Large backups
- Comprehensive reports

```python
def weekly_analytics():
    generate_comprehensive_report()
    create_weekly_backup()
```

### monthly

Runs once per month.

**Use for:**
- Monthly reports
- Monthly billing
- Monthly summaries

```python
def monthly_report():
    generate_monthly_invoice()
    send_monthly_summary()
```

### monthly_long

Runs once per month, allowed to take longer.

**Use for:**
- Heavy monthly processing
- Archival operations
- Month-end closing

```python
def monthly_processing():
    archive_old_data()
    process_monthly_closing()
```

## Function Signature

All scheduled functions have no parameters:

```python
def scheduled_task():
    """Scheduled task with no arguments"""
    import frappe
    
    # Your logic here
    process_data()
```

## Examples

### Send Daily Email Report

```python
# hooks.py
scheduler_events = {
    "daily": [
        "my_app.reports.send_daily_sales_report"
    ]
}

# reports.py
def send_daily_sales_report():
    import frappe
    from frappe.utils import today, formatdate
    
    # Get data
    sales = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Order`
        WHERE date = %s
    """, today(), as_dict=True)[0]
    
    # Send email
    frappe.sendmail(
        recipients=["manager@example.com"],
        subject=f"Sales Report - {formatdate(today())}",
        message=f"Total Sales: {sales.total}"
    )
```

### Hourly Data Sync

```python
# hooks.py
scheduler_events = {
    "hourly": [
        "my_app.integrations.sync_with_external_api"
    ]
}

# integrations.py
def sync_with_external_api():
    import frappe
    
    # Get pending syncs
    pending = frappe.get_all("Sync Queue", 
        filters={"status": "Pending"},
        limit=100
    )
    
    for item in pending:
        try:
            sync_item(item.name)
        except Exception as e:
            frappe.log_error(f"Sync failed: {str(e)}")
```

### Cleanup Old Records

```python
# hooks.py
scheduler_events = {
    "daily_maintenance": [
        "my_app.cleanup.delete_old_logs"
    ]
}

# cleanup.py
def delete_old_logs():
    import frappe
    from frappe.utils import add_days, now_datetime
    
    # Delete logs older than 30 days
    cutoff_date = add_days(now_datetime(), -30)
    
    frappe.db.delete("Custom Log", {
        "creation": ["<", cutoff_date]
    })
    
    frappe.db.commit()
```

### Conditional Scheduling

```python
def hourly_task():
    import frappe
    
    # Only run during business hours
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 9 or hour > 17:
        return
    
    # Only run on weekdays
    if datetime.now().weekday() >= 5:  # Saturday=5, Sunday=6
        return
    
    # Your task
    process_business_hours_task()
```

### Batched Processing

```python
def hourly_processing():
    import frappe
    
    # Process in batches
    batch_size = 100
    offset = 0
    
    while True:
        records = frappe.get_all("DocType",
            filters={"status": "Pending"},
            limit=batch_size,
            start=offset
        )
        
        if not records:
            break
        
        for record in records:
            try:
                process_record(record.name)
            except Exception as e:
                frappe.log_error(f"Processing failed: {str(e)}")
        
        offset += batch_size
        frappe.db.commit()
```

### Multi-Site Scheduler

```python
def daily_task():
    """Runs once per site"""
    import frappe
    
    site = frappe.local.site
    
    # Site-specific processing
    if site == "site1.example.com":
        process_site1_tasks()
    else:
        process_default_tasks()
```

## Best Practices

1. **Error Handling**: Wrap in try-except to prevent failures
2. **Logging**: Log errors and important operations
3. **Commits**: Commit database changes explicitly
4. **Performance**: Keep tasks fast, use batching for large datasets
5. **Idempotency**: Make tasks re-runnable safely
6. **Monitoring**: Track task execution and failures
7. **Time Zones**: Be aware of server timezone

### Robust Scheduler Task

```python
def scheduled_task():
    import frappe
    
    try:
        # Your logic
        process_data()
        
        # Commit changes
        frappe.db.commit()
        
        # Log success
        frappe.logger().info("Task completed successfully")
        
    except Exception as e:
        # Rollback on error
        frappe.db.rollback()
        
        # Log error
        frappe.log_error(
            title="Scheduled Task Failed",
            message=str(e)
        )
```

## Debugging

### Test Scheduler Task

```python
# In bench console
bench console

# In Python console
import frappe
frappe.init(site="your-site")
frappe.connect()

# Import and run your task
from my_app.tasks import my_task
my_task()
```

### Check Scheduler Logs

```bash
# View scheduler logs
tail -f logs/scheduler.log

# View error logs
bench console
frappe.get_all("Error Log", filters={"error": ["like", "%task_name%"]})
```

### Enable/Disable Scheduler

```python
# Disable scheduler
bench --site site-name scheduler disable

# Enable scheduler
bench --site site-name scheduler enable

# Check scheduler status
bench --site site-name scheduler status
```

## Common Issues

**Task not running:**
- Check if scheduler is enabled
- Verify function path in hooks.py
- Check for errors in logs
- Ensure bench is running

**Task running multiple times:**
- Check for duplicate registrations
- Verify scheduler is running once per site
- Check cron syntax

**Performance issues:**
- Add batching for large datasets
- Optimize database queries
- Move heavy tasks to `_long` queues
- Use background jobs for very slow tasks

## Notes

- Scheduler runs in background worker process
- All scheduler tasks run in "Administrator" context
- Changes to `scheduler_events` require bench restart
- Scheduler disabled by default in development
- Use `bench schedule` to see upcoming tasks
- Each site runs its own scheduler tasks
- Failed tasks don't retry automatically
- `all` events run every ~3 minutes
- `hourly` events may not run exactly on the hour
