### Trigger: /fix

Role: Automated Debugger
Process:
Run flutter analyze.

If errors exist, read the error log and the relevant files.

Automatically apply a fix using Gemini 3 Pro.

Run flutter test to ensure the fix didn't break the 'Safety Guard' logic.

Present the 'diff' for my approval.
