---
name: public-transportation
description: Instructions for configuring and using the Public Transportation application integration.
---

# Public Transportation Application Integration

The Public Transportation integration allows for a quick opening of a local transport monitoring application via a hardware macro or daemon command.

## Configuration

### Port Configuration
The application is expected to run on **port 3001**.
To configure the daemon with this port, run the following command:

```bash
daemon setPort pt 3001
```

## Commands

- `d publicTransportationOpenApp`: Manually trigger the app opening.
- `d publicTransportationStartProxy`: (Optional) Start the SSH proxy required for the app's data source.


## Troubleshooting

- **Chrome doesn't open**: Ensure `google-chrome` is in your PATH.
- **Port issue**: Verify the port is correctly set in the daemon using `daemon getPort pt`.
- **Macro not firing**: Check daemon logs for "Triggering G3" or "Triggering Public Transportation macro".
