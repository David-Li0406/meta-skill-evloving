---
name: flask-web-development-expert
description: Use this skill when you need expert guidance on building modern Flask web applications, including REST APIs, best practices, and frontend integration.
---

# Skill body

## Core Concepts

### Flask Fundamentals
- Routing and views
- Request/response handling
- Templates with Jinja2
- Blueprints for modularity
- Application factory pattern
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

## Basic Flask Application

```python
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Application factory
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app)  # Enable CORS for frontend

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Database setup
db = SQLAlchemy()
migrate = Migrate()

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    # Define Post model fields here

# Example API routes
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

### Frontend Integration
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
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        return await response.json();
    }

    async gameAction(action, amount) {
        const response = await fetch(`${this.baseUrl}/api/game/action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action, amount })
        });
        return await response.json();
    }
}
```