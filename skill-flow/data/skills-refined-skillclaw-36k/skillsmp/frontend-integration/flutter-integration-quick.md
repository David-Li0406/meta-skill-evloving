---
name: flutter-integration-quick
description: "Flutter + Kailash integration. Use when asking 'flutter integration', 'flutter kailash', or 'mobile kailash'."
---

# Flutter + Kailash Integration

> **Skill Metadata**
> Category: `frontend`
> Priority: `LOW`
> SDK Version: `0.9.25+`

## Quick Setup

### 1. Backend API (Python)
```python
from kailash.api.workflow_api import WorkflowAPI
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_node("LLMNode", "chat", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "{{input.message}}"
})

api = WorkflowAPI(workflow.build())
api.run(port=8000)
```

### 2. Flutter Frontend
```dart
// lib/services/workflow_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class WorkflowService {
  static const String baseUrl = 'http://localhost:8000';

  Future<Map<String, dynamic>> executeWorkflow(String message) async {
    final response = await http.post(
      Uri.parse('$baseUrl/execute'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'inputs': {'message': message}}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to execute workflow');
    }
  }
}

// lib/screens/chat_screen.dart
import 'package:flutter/material.dart';
import '../services/workflow_service.dart';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  final _service = WorkflowService();
  String _response = '';

  void _sendMessage() async {
    final result = await _service.executeWorkflow(_controller.text);
    setState(() {
      _response = result['outputs']['chat']['response'];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          TextField(
            controller: _controller,
            decoration: InputDecoration(hintText: 'Ask a question...'),
          ),
          ElevatedButton(
            onPressed: _sendMessage,
            child: Text('Send'),
          ),
          if (_response.isNotEmpty) Text(_response),
        ],
      ),
    );
  }
}
```

<!-- Trigger Keywords: flutter integration, flutter kailash, mobile kailash, flutter workflows -->
