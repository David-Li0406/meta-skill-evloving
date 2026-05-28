---
name: twilio-communications
description: Use this skill when you need to build communication features with Twilio, including SMS messaging, voice calls, WhatsApp Business API, and user verification (2FA).
---

# Skill body

## Overview

This skill provides the necessary patterns and code examples to implement communication features using Twilio. It covers SMS messaging, voice calls, WhatsApp Business API, and user verification (2FA), focusing on compliance, rate limits, and error handling.

## Patterns

### SMS Sending Pattern

This pattern demonstrates how to send SMS messages using Twilio, including phone number formatting, message delivery, and delivery status callbacks.

**Key considerations:**
- Phone numbers must be in E.164 format (+1234567890).
- Default rate limit: 80 messages per second (MPS).
- Messages over 160 characters are split into multiple segments (and cost more).
- Carrier filtering can block messages, especially to US numbers.

**When to use:**
- Sending notifications to users.
- Transactional messages (e.g., order confirmations, shipping).
- Alerts and reminders.

### Example Code

```python
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import re

class TwilioSMS:
    """
    SMS sending with proper error handling and validation.
    """

    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]

    def validate_e164(self, phone: str) -> bool:
        """Validate phone number is in E.164 format."""
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    def send_sms(
        self,
        to: str,
        body: str,
        status_callback: str = None
    ) -> dict:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number in E.164 format.
            body: Message text (160 chars = 1 segment).
            status_callback: URL for delivery status webhooks.

        Returns:
            Message SID and status.
        """
        # Validate phone number format
        if not self.validate_e164(to):
            return {
                "success": False,
                "error": "Phone number must be in E.164 format (+1234567890)"
            }

        # Check message length (warn about segmentation)
        segment_count = (len(body) + 159) // 160
        if segment_count > 1:
            print(f"Warning: Message will be split into {segment_count} segments.")

        # Send the SMS
        try:
            message = self.client.messages.create(
                body=body,
                from_=self.from_number,
                to=to,
                status_callback=status_callback
            )
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e)
            }
```