#!/usr/bin/env python3
"""
Simple Flask Application for Server Integration Testing

This is a minimal Flask app that demonstrates:
- Serving HTML pages
- RESTful API endpoints
- Dynamic content rendering
"""

from flask import Flask, jsonify, render_template_string
import time
import random

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Integration Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #0056b3;
        }
        #data-container {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            min-height: 100px;
        }
        .data-item {
            padding: 10px;
            margin: 5px 0;
            background: #e9ecef;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Flask Integration Testing</h1>
        <p>This page is served by a Flask backend and demonstrates full-stack testing.</p>

        <div>
            <button onclick="loadData()">Load Data from API</button>
            <button onclick="clearData()">Clear Data</button>
        </div>

        <div id="data-container">
            <p>Click "Load Data" to fetch data from the API...</p>
        </div>
    </div>

    <script>
        async function loadData() {
            console.log('Loading data from API...');
            const container = document.getElementById('data-container');
            container.innerHTML = '<p>Loading...</p>';

            try {
                const response = await fetch('/api/data');
                const data = await response.json();

                container.innerHTML = '<h3>API Response:</h3>';
                data.items.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'data-item';
                    div.textContent = `${item.id}: ${item.name}`;
                    container.appendChild(div);
                });

                console.log('Data loaded successfully');
            } catch (error) {
                console.error('Error loading data:', error);
                container.innerHTML = '<p style="color: red;">Error loading data</p>';
            }
        }

        function clearData() {
            document.getElementById('data-container').innerHTML =
                '<p>Click "Load Data" to fetch data from the API...</p>';
            console.log('Data cleared');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/data')
def get_data():
    """API endpoint that returns JSON data"""
    # Simulate some processing time
    time.sleep(0.2)

    items = [
        {'id': i, 'name': f'Item {i}', 'value': random.randint(1, 100)}
        for i in range(1, 6)
    ]

    return jsonify({
        'status': 'success',
        'items': items,
        'timestamp': time.time()
    })


@app.route('/api/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is running'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Flask Integration Test Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(host='localhost', port=5000, debug=False)
