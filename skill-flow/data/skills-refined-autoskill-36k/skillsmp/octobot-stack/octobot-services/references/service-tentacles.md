# Service Tentacles

## Notification Services

### Telegram
```python
from octobot_services.services import TelegramService

class TelegramService(AbstractService):
    def get_name(cls):
        return "telegram"
    
    async def start(self):
        self.bot = telegram.Bot(token=self.config["token"])
        await self.subscribe_to_events()
    
    async def send_message(self, text: str):
        await self.bot.send_message(
            chat_id=self.config["chat_id"],
            text=text
        )
```

### Discord
```python
from octobot_services.services import DiscordService

class DiscordService(AbstractService):
    async def start(self):
        self.client = discord.Client()
        
        @self.client.event
        async def on_ready():
            self.channel = self.client.get_channel(self.channel_id)
        
        await self.client.start(self.token)
```

## Webhook Service

```python
from octobot_services.services import WebhookService

class WebhookService(AbstractService):
    def __init__(self):
        self.app = Flask(__name__)
        self.handlers = {}
    
    def register_handler(self, path: str):
        def decorator(func):
            self.handlers[path] = func
            
            @self.app.route(path, methods=["POST"])
            async def handler():
                payload = request.get_json()
                await func(payload)
                return {"status": "ok"}
            
            return func
        return decorator
```

## Cloud Sync Service

```python
class CloudSyncService(AbstractService):
    async def sync_config(self):
        """Upload config to cloud"""
        data = self.get_bot_config()
        await self.upload(data)
    
    async def download_config(self):
        """Download config from cloud"""
        data = await self.fetch()
        self.apply_config(data)
```
