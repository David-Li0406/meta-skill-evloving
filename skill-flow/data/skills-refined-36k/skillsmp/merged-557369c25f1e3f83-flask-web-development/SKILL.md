---
name: flask-web-development
description: Use this skill for expert-level Flask web development, including REST APIs, real-time features, and best practices for modern web applications.
---

# Flask Web Development

This skill provides comprehensive guidance for building modern Flask web applications, including REST APIs, WebSockets, and responsive frontends, while adhering to best practices.

## Core Concepts

### Flask Fundamentals
- Routing and views
- Request/response handling
- Templates with Jinja2
- Application structure and modularity
- Configuration management

### Flask Extensions
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-Login (authentication)
- Flask-RESTful (REST APIs)
- Flask-JWT-Extended (JWT tokens)
- Flask-CORS (CORS handling)
- Flask-Limiter (rate limiting)

### Best Practices
- Application structure
- Error handling
- Testing
- Security
- Production deployment
- Use of environment variables

## Basic Flask Application

```python
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models and routes here
```

## REST API with Flask-RESTful

```python
from flask import Blueprint
from flask_restful import Api, Resource, reqparse

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Define request parsers and resources here
```

## Real-Time Features

### WebSocket Integration

```python
from flask_socketio import SocketIO

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    # Handle new connection
    pass

@socketio.on('player_action')
def handle_action(data):
    # Process player action
    pass
```

## Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

## Session Management

```python
from flask import session
import secrets

app.secret_key = secrets.token_hex(16)

@app.route('/api/game/new', methods=['POST'])
def new_game():
    session['game_id'] = secrets.token_hex(8)
    return jsonify({'game_id': session['game_id']})
```

## Frontend Integration

### JavaScript API Client Pattern

```javascript
class GameAPI {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    async getGameState() {
        const response = await fetch(`${this.baseUrl}/api/game/state`);
        return await response.json();
    }

    async newGame() {
        const response = await fetch(`${this.baseUrl}/api/game/new`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        return await response.json();
    }
}
```

## Testing Flask APIs

### Using curl

```bash
# GET request
curl http://localhost:5000/api/game/state

# POST request
curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"player_name": "Player1"}'
```

### Using Python requests

```python
import requests

response = requests.get('http://localhost:5000/api/game/state')
print(response.json())
```

## Implementation Guidelines

1. **Start Simple**: Begin with basic routes and add complexity gradually.
2. **Use JSON**: Always return JSON for API endpoints.
3. **Error Handling**: Implement proper error handling and status codes.
4. **CORS**: Enable CORS if frontend is separate.
5. **Security**: Use sessions for user-specific data.
6. **Testing**: Test each endpoint before moving to frontend.
7. **Documentation**: Document API endpoints clearly.

## Common Issues and Solutions

**Issue: CORS errors**
```python
from flask_cors import CORS
CORS(app)  # Enable for all routes
```

**Issue: JSON parsing errors**
```python
data = request.get_json(force=True)  # Force JSON parsing
```

**Issue: Static files not loading**
```python
app = Flask(__name__, static_folder='static', static_url_path='/static')
```

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask-RESTful: https://flask-restful.readthedocs.io/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- Flask-SocketIO: https://flask-socketio.readthedocs.io/