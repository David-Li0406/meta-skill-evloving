# Architecture

## Flask Application Structure

```
trading-backend/
├── app.py              # Main application
├── api/
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── portfolio.py    # Portfolio routes
│   ├── trading.py      # Trading routes
│   └── config.py       # Configuration routes
├── middleware/
│   ├── auth.py         # JWT middleware
│   └── cors.py         # CORS middleware
└── utils/
    ├── octobot_bridge.py  # OctoBot API wrapper
    └── validators.py       # Request validation
```

## Application Factory

```python
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(Config)
    
    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from api import auth, portfolio, trading, config
    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(portfolio.bp, url_prefix="/api/portfolio")
    app.register_blueprint(trading.bp, url_prefix="/api/trading")
    app.register_blueprint(config.bp, url_prefix="/api/config")
    
    # Error handlers
    register_error_handlers(app)
    
    return app
```

## Error Handling

```python
from flask import jsonify

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": str(error)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "error": "Unauthorized",
        "message": "Invalid or missing token"
    }), 401

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong"
    }), 500
```

## OctoBot Bridge

```python
class OctoBotBridge:
    """Wrapper for OctoBot internal API"""
    
    def __init__(self, octobot_instance):
        self.bot = octobot_instance
    
    async def get_portfolio(self):
        return await self.bot.get_portfolio()
    
    async def create_order(self, symbol, side, type, amount, price=None):
        return await self.bot.create_order(
            symbol=symbol,
            side=side,
            type=type,
            amount=amount,
            price=price
        )
```
