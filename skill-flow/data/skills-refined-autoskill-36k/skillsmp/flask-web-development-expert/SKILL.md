---
name: Flask Web Development Expert
description: Specialized skill for building modern Flask web applications with REST APIs, WebSockets, and responsive frontends
---

# Flask Web Development Expert

This skill provides expertise in building modern Flask web applications with best practices for API development, frontend integration, and real-time features.

## Core Competencies

### 1. Flask Application Structure

**Best Practice Structure:**
```
project/
├── app.py or server.py          # Main Flask application
├── requirements.txt              # Dependencies
├── static/                       # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                    # Jinja2 templates (if using)
└── api/                         # API routes (optional)
```

### 2. Flask Application Template

**Basic Flask App with REST API:**
```python
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend

# Game state (in-memory for simplicity)
game_state = {
    'initialized': False,
    'player': None,
    'machine': None,
    'pot': 0,
    'phase': 'waiting'
}

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/game/state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    return jsonify(game_state)

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start a new game"""
    # Initialize game logic here
    return jsonify({'status': 'success', 'message': 'New game started'})

@app.route('/api/game/action', methods=['POST'])
def game_action():
    """Handle player action"""
    data = request.json
    action = data.get('action')  # 'call', 'raise', 'fold'
    amount = data.get('amount', 0)
    
    # Process action here
    return jsonify({'status': 'success', 'action': action})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 3. Frontend Integration

**JavaScript API Client Pattern:**
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

    async performAction(action, amount = 0) {
        const response = await fetch(`${this.baseUrl}/api/game/action`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action, amount})
        });
        return await response.json();
    }
}

// Usage
const api = new GameAPI();
api.getGameState().then(state => console.log(state));
```

### 4. Real-Time Updates

**Polling Pattern (Simple):**
```javascript
// Poll for updates every 1 second
setInterval(async () => {
    const state = await api.getGameState();
    updateUI(state);
}, 1000);
```

**WebSocket Pattern (Advanced):**
```python
# Flask with Socket.IO
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    emit('game_update', game_state)

@socketio.on('player_action')
def handle_action(data):
    # Process action
    emit('game_update', game_state, broadcast=True)
```

### 5. Error Handling

**API Error Responses:**
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Custom error handling
@app.route('/api/game/action', methods=['POST'])
def game_action():
    try:
        data = request.json
        if not data or 'action' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        
        # Process action
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 6. Session Management

**Flask Sessions:**
```python
from flask import session
import secrets

app.secret_key = secrets.token_hex(16)

@app.route('/api/game/new', methods=['POST'])
def new_game():
    session['game_id'] = secrets.token_hex(8)
    session['player_chips'] = 1000
    return jsonify({'game_id': session['game_id']})
```

### 7. Static File Serving

**Serve Static Files:**
```python
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Or use built-in static folder
app = Flask(__name__, static_folder='static', static_url_path='/static')
```

### 8. Development Best Practices

**Debug Mode:**
```python
if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # Production (use gunicorn or waitress)
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Environment Variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'
```

### 9. Testing Flask APIs

**Using curl:**
```bash
# GET request
curl http://localhost:5000/api/game/state

# POST request
curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"player_name": "Player1"}'
```

**Using Python requests:**
```python
import requests

# Test API
response = requests.get('http://localhost:5000/api/game/state')
print(response.json())

response = requests.post('http://localhost:5000/api/game/action',
                        json={'action': 'call', 'amount': 50})
print(response.json())
```

### 10. Common Patterns for Game Development

**Game State Management:**
```python
class GameManager:
    def __init__(self):
        self.games = {}
    
    def create_game(self, game_id):
        self.games[game_id] = {
            'players': [],
            'pot': 0,
            'phase': 'waiting'
        }
        return self.games[game_id]
    
    def get_game(self, game_id):
        return self.games.get(game_id)
    
    def update_game(self, game_id, updates):
        if game_id in self.games:
            self.games[game_id].update(updates)

game_manager = GameManager()

@app.route('/api/game/<game_id>/state')
def get_game_state(game_id):
    game = game_manager.get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)
```

## Implementation Guidelines

1. **Start Simple**: Begin with basic routes and add complexity gradually
2. **Use JSON**: Always return JSON for API endpoints
3. **Error Handling**: Implement proper error handling and status codes
4. **CORS**: Enable CORS if frontend is separate
5. **Security**: Use sessions for user-specific data
6. **Testing**: Test each endpoint before moving to frontend
7. **Documentation**: Document API endpoints clearly

## Required Dependencies

```txt
flask>=2.3.0
flask-cors>=4.0.0
python-dotenv>=1.0.0
```

Optional for advanced features:
```txt
flask-socketio>=5.3.0  # For WebSockets
gunicorn>=21.0.0       # Production server
```

## Quick Start Checklist

- [ ] Create Flask app with basic structure
- [ ] Define API endpoints
- [ ] Test endpoints with curl or Postman
- [ ] Create static folder structure
- [ ] Build frontend HTML/CSS/JS
- [ ] Connect frontend to API
- [ ] Add error handling
- [ ] Test complete flow
- [ ] Add real-time updates (polling or WebSocket)
- [ ] Deploy and test

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
# Use absolute paths
app = Flask(__name__, static_folder='static', static_url_path='/static')
```

**Issue: Port already in use**
```python
app.run(port=5001)  # Use different port
```

## When to Use This Skill

- Building REST APIs with Flask
- Creating web-based game interfaces
- Integrating Python backend with JavaScript frontend
- Real-time web applications
- Converting desktop apps to web apps
