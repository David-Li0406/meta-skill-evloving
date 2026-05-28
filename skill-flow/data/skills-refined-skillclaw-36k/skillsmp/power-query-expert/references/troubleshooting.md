# Troubleshooting Guide

Complete troubleshooting reference for Power Query and Frappe integration.

## Power Query Errors

### "Report generation timed out after X attempts"

**Causes:**
- Report takes longer than polling configuration allows
- Background workers not running or overloaded
- Report query is inefficient

**Solutions:**
- Increase `maxAttempts` in the polling function (e.g., from 100 to 150)
- Optimize the Frappe report query for performance
- Add database indexes on frequently filtered columns
- Verify background workers are running: `bench doctor`
- Check worker logs for errors: `tail -f logs/worker.log`

### "DataSource.Error: Web.Contents failed to get contents"

**Causes:**
- Incorrect URL or network connectivity issues
- Authentication failure
- Report doesn't exist or user lacks permissions

**Solutions:**
- Verify BaseUrl is correct and accessible (test in browser)
- Check authentication credentials (API key/secret)
- Ensure report name exists and is spelled correctly
- Verify user has permission to access the report
- Check Frappe site is running and not in maintenance mode

### Empty table or no data returned

**Causes:**
- Report filters exclude all results
- Permission issues
- Job failed during execution
- Premature result retrieval

**Solutions:**
- Verify report permissions for the API user
- Check report filters are valid and return data
- Review Prepared Report status in Frappe (search for job_id)
- Ensure check_status returned 1 before calling get_result
- Look for errors in background worker logs
- Test report manually in Frappe with same filters

### Type conversion errors

**Causes:**
- Null values in numeric columns
- Unexpected data formats
- Missing or incorrect type mapping

**Solutions:**
- Add missing field types to TypeMapping record
- Use manual type overrides in ManualTypeMap
- Default to `type text` for unknown types
- Handle null values with `Table.TransformColumns()` before type conversion
- Check actual data values match expected types

## Caching Issues

### Stale/outdated data

**Causes:**
- Power Query caching API responses
- Missing cache-busting parameters
- Browser/gateway caching

**Solutions:**
- Ensure cache-busting timestamps are included in all URLs
- Add `&_ts=` parameter with current timestamp
- Clear Power Query cache: Data → Refresh → Clear Cache
- Use unique `_attempt` parameter for each poll
- Set `ManualStatusHandling` in Web.Contents options

### Same data despite different filters

**Causes:**
- Filters not being passed to start_job
- Cache returning old results
- Filter format doesn't match report expectations

**Solutions:**
- Verify filters are included in start_job call
- Check filter parameter names match report definition
- Clear cache and force full refresh
- Test filters directly in Frappe report UI first
- Inspect actual API URL being called

## Frappe-Side Issues

### Job stays in "Queued" status

**Causes:**
- Background workers not running
- Worker queue backlog
- Worker process crashed

**Solutions:**
- Check workers are running: `bench doctor`
- Restart workers: `bench restart`
- Check worker logs: `tail -f logs/worker.log`
- Monitor queue depth in Prepared Report list
- Check for worker errors in error log

### Empty or incomplete results

**Causes:**
- Job failed during execution
- Report returned error
- Incorrect job_id reference

**Solutions:**
- Ensure check_status returned 1 before calling get_result
- Verify job_id matches what start_job returned
- Check Prepared Report document for error status
- Review report execution logs in Frappe
- Check report works manually in Frappe UI

### Performance issues

**Causes:**
- Inefficient report query
- Large dataset without pagination
- Missing database indexes
- Server resource constraints

**Solutions:**
- Adjust `attempts` and `sleep` parameters
- Optimize report SQL query
- Add database indexes on filtered columns
- Use date range filters to limit dataset
- Monitor server resource usage (CPU, memory, disk I/O)
- Consider breaking large reports into smaller chunks

## Authentication Issues

### 401 Unauthorized

**Solutions:**
- Verify credentials in Excel/Power BI authentication dialog
- **For Username/Password**: Check username and password are correct
- **For API Key/Token**: Ensure API Key (username) and API Secret (password) are correct
- Excel/Power BI uses HTTP Basic Authentication: `Authorization: Basic base64(key:token)`
- Frappe accepts both Basic auth and token format
- Ensure API key is not disabled or expired in Frappe
- Verify user account is active
- Check API key has proper permissions

### 403 Forbidden

**Solutions:**
- Grant report permissions to the user/API user
- Check role permissions in Role Permission Manager
- Verify report is not restricted by domain
- Check user is assigned to correct roles

## Best Practices for Prevention

### 1. Test incrementally
- Start with simple report (no filters)
- Add filters one at a time
- Test with small datasets first
- Verify each step works before proceeding

### 2. Monitor and log
- Track polling attempt counts
- Log failed requests for analysis
- Monitor completion times
- Set up alerts for timeout thresholds

### 3. Handle errors gracefully
- Implement try-catch in M code
- Provide user-friendly error messages
- Log technical details for debugging
- Have fallback values for missing data

### 4. Optimize for performance
- Add database indexes on filtered fields
- Limit date ranges in queries
- Use summary reports when detail isn't needed
- Cache intermediate results in custom reports

### 5. Secure properly
- Credentials are entered through Excel/Power BI authentication forms, not in code
- Use role-based report permissions
- Audit API access regularly
- Rotate API keys periodically
- API keys preferred over passwords for automated refreshes
