# Canned Response Templates for Firefox Bug Triage

This document contains standard response templates for common triage scenarios. Use these as a starting point and customize them for specific bugs.

## Template Variables

When using these templates, replace placeholders with actual values:

| Variable | Description |
|----------|-------------|
| `{{BUG_ID}}` | The duplicate bug ID |
| `{{VERSION}}` | Firefox version |
| `{{OS}}` | Operating system |
| `{{STEPS}}` | Steps to reproduce |
| `{{REASON}}` | Explanation/reason |

---

## Information Requests

### need-str
**Title:** Ask for Steps to Reproduce
**Use When:** Bug report lacks clear, actionable reproduction steps
**Categories:** need-info, str

```
Hi, and thanks for filing this bug!

To investigate this issue, we need clear **Steps to Reproduce**. Please provide:

1. The exact steps to trigger this behavior
2. What you expected to happen
3. What actually happened

Thanks!
```

---

### need-testcase
**Title:** Ask for Test Case
**Use When:** Issue requires a minimal reproduction case
**Categories:** need-info, testcase

```
Thanks for filing this bug!

To help us investigate, could you provide a **minimal test case** that demonstrates the issue? This could be:

- A reduced HTML/CSS/JS file
- A link to a simplified example
- Steps to reproduce with specific input

A minimal reproducible example helps us quickly identify and fix the problem.
```

---

### need-profile
**Title:** Ask for Firefox Profile with Logs
**Use When:** Need detailed logs to diagnose the issue
**Categories:** need-info, profile, logs

```
Thanks for reporting this issue!

To help us investigate, could you please capture a **Firefox profile with logs**? Here's how:

1. Install the Firefox Profiler add-on: https://profiler.firefox.com/
2. Go to `about:logging` in your Firefox address bar
3. Select the **Logging preset** that matches your issue:
   - **Media playback** - for audio/video playing issues
   - **WebRTC** - for Web Conferencing issues (e.g., Google Meet)
   - **Graphics** - for screen display issues (e.g., wrong color, black screen)
   - **Networking** - for connection issues (internet, socket errors)
   - **Custom** - for other issues (let us know and we'll provide the log modules needed)
4. Click **Set Log Modules**, then click **Start Logging**
5. Open a **new tab** and reproduce the steps that cause the issue
6. Once reproduced, **close that tab**, go back to `about:logging`, and click **Stop Logging**
7. The Firefox Profiler should launch automatically - please **share the profile link** here

This will help us identify what's causing the problem. Thanks!
```

---

### need-crash-report
**Title:** Ask for Crash Report
**Use When:** Firefox crashed and we need the crash report
**Categories:** need-info, crash

```
Thanks for reporting this crash!

To help us investigate, could you please share your **crash report IDs**? Here's how:

1. Open a new tab and go to `about:crashes`
2. Look for crash reports around the time you experienced the crash
3. If reports show "not submitted", click **Submit** to send them to Mozilla
4. Copy the **Report ID** (starts with `bp-`) and paste it here

Alternatively, you can share the **full crash report URL**, e.g., `https://crash-stats.mozilla.org/report/index/bp-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

The crash report contains stack traces and system information that help us identify the root cause. Thanks!
```

---

### more-info-needed
**Title:** General Request for More Information
**Use When:** Bug needs more context to understand/reproduce
**Categories:** need-info

```
Thanks for your bug report!

Could you please provide more information to help us investigate?

- Firefox version (from `about:support`)
- Operating system and version
- Any browser extensions installed
- When did this start happening?

If this is a **regression** (something that used to work but now doesn't), it would be very helpful if you could use **mozregression** to identify when the bug started:

1. Install mozregression: https://mozilla.github.io/mozregression/
2. Run it and follow the prompts to bisect between a known good and bad version
3. Share the regression range or the changeset that introduced the issue

This helps us pinpoint the exact change that caused the problem.
```

---

### need-regression-range
**Title:** Request Regression Range
**Use When:** Issue appears to be a regression
**Categories:** need-info, regression

```
Thanks for reporting this!

Based on your description, this might be a **regression** (something that used to work but now doesn't). Could you help us identify when this started?

If you have time, please use **mozregression** to narrow down when this broke:

1. Install mozregression: https://mozilla.github.io/mozregression/
2. Run it and follow the prompts
3. You'll need to know a version where it worked and one where it doesn't
4. Share the regression range it finds

Alternatively, if you remember approximately when this started working differently, let us know and we can check the changes around that time.

Thanks!
```

---

### need-system-info
**Title:** Request System Information
**Use When:** Need hardware/system details for investigation
**Categories:** need-info, system

```
Thanks for filing this bug!

Could you provide some system information to help us investigate?

1. Go to `about:support` in your Firefox address bar
2. Click **Copy text to clipboard**
3. Paste the contents here (or attach as a text file)

Key information we're looking for:
- Firefox version and build ID
- Operating system
- Graphics adapter and driver version
- Any modified preferences

Thanks!
```

---

## Status Updates

### confirmed
**Title:** Bug Confirmed
**Use When:** You've successfully reproduced the issue
**Categories:** status, confirmed

```
I was able to reproduce this issue:

**Environment:**
- Firefox: {{VERSION}}
- OS: {{OS}}

**Steps taken:**
{{STEPS}}

Confirming this bug. Thanks for the report!
```

---

### investigating
**Title:** Under Investigation
**Use When:** Actively looking into the issue
**Categories:** status

```
Thanks for reporting this!

We're investigating this issue. I'll update the bug as we learn more.

In the meantime, if you have any additional information that might help (specific websites, steps, or configurations that trigger this), please add it here.
```

---

## Resolutions

### duplicate
**Title:** Mark as Duplicate
**Use When:** Bug is a duplicate of an existing bug
**Categories:** resolution, duplicate

```
This bug appears to be a duplicate of bug {{BUG_ID}}.

I'm marking this as a duplicate. Please follow the linked bug for updates.
```

---

### wontfix
**Title:** Won't Fix Explanation
**Use When:** Bug won't be fixed and needs explanation
**Categories:** resolution, wontfix

```
Thank you for filing this bug.

After investigation, we've determined that we won't be fixing this issue because:

{{REASON}}

If you believe this decision should be reconsidered, please comment with additional context.
```

---

### worksforme
**Title:** Cannot Reproduce
**Use When:** Unable to reproduce the reported issue
**Categories:** resolution, worksforme

```
Thanks for reporting this issue!

I attempted to reproduce this bug but was unable to see the behavior you described. I tested with:

- Firefox: {{VERSION}}
- OS: {{OS}}
- Steps: {{STEPS}}

Could you provide more details about your setup or exact steps? If you can still reproduce this, please:
1. Share your `about:support` info
2. Provide exact steps to trigger the issue
3. Let us know if there are any specific conditions needed

I'll reopen this if we get more information. Thanks!
```

---

### incomplete
**Title:** Incomplete - Closing
**Use When:** Bug lacks necessary information and reporter hasn't responded
**Categories:** resolution, incomplete

```
Thanks for filing this bug.

Unfortunately, we don't have enough information to investigate this issue, and we haven't received a response to our questions.

If you're still experiencing this problem, please file a new bug with:
- Clear steps to reproduce
- Firefox version and OS
- Any relevant error messages or screenshots

We're happy to look into this again with more details.
```

---

## Acknowledgements

### fuzzing-thanks
**Title:** Fuzzing Thanks
**Use When:** Bug was found through fuzzing
**Categories:** acknowledgement, fuzzing

```
Thanks for finding this issue through fuzzing!

We appreciate the detailed crash information and test case. This helps us fix security and stability issues quickly.
```

---

### first-time-contributor
**Title:** Welcome First-Time Contributor
**Use When:** Reporter is filing their first bug
**Categories:** acknowledgement, welcome

```
Thanks for filing your first bug report!

We appreciate you taking the time to report this issue. The Firefox community relies on reports like this to improve the browser for everyone.

[Continue with relevant triage response...]
```

---

### good-report
**Title:** Thank for Quality Report
**Use When:** Bug report is particularly well-written
**Categories:** acknowledgement

```
Thanks for this excellent bug report!

The clear steps to reproduce and detailed information make it much easier for us to investigate. We'll look into this and update the bug as we learn more.
```

---

## Special Cases

### security-notice
**Title:** Security Bug Notice
**Use When:** Bug might have security implications
**Categories:** security

```
Thanks for reporting this!

This issue may have security implications. I'm going to restrict visibility on this bug while we investigate.

If you've found what you believe is a security vulnerability, please ensure it's filed in the appropriate security-sensitive component. You can also report security issues via: https://www.mozilla.org/security/bug-bounty/

Thanks for helping keep Firefox secure!
```

---

### moved-component
**Title:** Moving to Different Component
**Use When:** Bug belongs in a different component
**Categories:** triage, component

```
Thanks for filing this bug!

Based on the description, this appears to be an issue with [Component Name]. I'm moving this bug to the appropriate component where the right team can investigate.

[Optional: Brief explanation of why it belongs there]
```

---

### needs-platform-team
**Title:** Platform-Specific Investigation
**Use When:** Issue is platform-specific and needs specialist attention
**Categories:** triage, platform

```
Thanks for reporting this!

This appears to be specific to {{OS}}. I'm adding the appropriate team members who specialize in this platform.

In the meantime, could you verify:
1. Does this happen in Firefox Safe Mode? (Help > Troubleshoot Mode)
2. Does this happen with a fresh Firefox profile?
3. Are your graphics drivers up to date?

Thanks!
```

---

## Response Customization Guidelines

When adapting these templates:

1. **Be specific** - Replace generic placeholders with bug-specific details
2. **Be concise** - Remove sections that don't apply
3. **Be welcoming** - Especially for new contributors
4. **Be actionable** - Tell reporters exactly what you need
5. **Combine templates** - Mix elements from multiple templates when appropriate

### Tone Modifiers

**Shorter version:** Remove explanatory text, keep only essential requests
**Friendlier version:** Add more thanks, soften language ("Could you..." vs "Please...")
**More technical:** Include specific debug flags, config options, or code references
**For experts:** Skip basic instructions, reference tools directly

---

## Quick Reference

| Scenario | Template ID |
|----------|-------------|
| Missing STR | need-str |
| Need test case | need-testcase |
| Need logs | need-profile |
| Crash without report | need-crash-report |
| General info needed | more-info-needed |
| Possible regression | need-regression-range |
| Need system details | need-system-info |
| Reproduced successfully | confirmed |
| Looking into it | investigating |
| Duplicate bug | duplicate |
| Won't fix | wontfix |
| Can't reproduce | worksforme |
| No response, closing | incomplete |
| Fuzzer-found bug | fuzzing-thanks |
| First-time reporter | first-time-contributor |
| Great bug report | good-report |
| Security issue | security-notice |
| Wrong component | moved-component |
| Platform-specific | needs-platform-team |
