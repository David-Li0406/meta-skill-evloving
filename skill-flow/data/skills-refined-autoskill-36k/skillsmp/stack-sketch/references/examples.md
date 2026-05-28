# StackSketch Examples

Use these as starting points when generating new diagrams.

## Example 1: Infrastructure Map

```json
{
  "version": "0.1",
  "name": "Full-Stack Infrastructure",
  "diagram": { "type": "infra" },
  "canvas": { "width": 1400, "height": 900, "grid": 16, "background": "dots" },
  "groups": [
    { "id": "g-frontend", "label": "Frontend", "bounds": { "x": 60, "y": 80, "width": 360, "height": 280 }, "style": { "fill": "#eef6ff", "stroke": "#7aa6ff", "cornerRadius": 16 } },
    { "id": "g-backend", "label": "Backend", "bounds": { "x": 480, "y": 80, "width": 420, "height": 500 }, "style": { "fill": "#f7f2ff", "stroke": "#a182ff", "cornerRadius": 16 } },
    { "id": "g-data", "label": "Data", "bounds": { "x": 960, "y": 80, "width": 360, "height": 500 }, "style": { "fill": "#fff7e8", "stroke": "#ffb55a", "cornerRadius": 16 } },
    { "id": "g-external", "label": "External", "bounds": { "x": 480, "y": 620, "width": 840, "height": 220 }, "style": { "fill": "#f0fff4", "stroke": "#66d19e", "cornerRadius": 16 } }
  ],
  "nodes": [
    { "id": "web-app", "type": "rect", "label": "Web App", "kind": "frontend", "position": { "x": 140, "y": 160 }, "size": { "width": 200, "height": 90 }, "style": { "fill": "#dbe9ff", "stroke": "#4c7dff" } },
    { "id": "cdn", "type": "pill", "label": "CDN", "kind": "cdn", "position": { "x": 140, "y": 270 }, "size": { "width": 200, "height": 60 }, "style": { "fill": "#dbe9ff", "stroke": "#4c7dff" } },
    { "id": "api", "type": "rect", "label": "API Server", "kind": "backend", "position": { "x": 560, "y": 160 }, "size": { "width": 240, "height": 90 }, "style": { "fill": "#eadfff", "stroke": "#8b6dff" } },
    { "id": "worker", "type": "rect", "label": "Worker", "kind": "worker", "position": { "x": 560, "y": 280 }, "size": { "width": 240, "height": 90 }, "style": { "fill": "#eadfff", "stroke": "#8b6dff" } },
    { "id": "queue", "type": "pill", "label": "Queue", "kind": "queue", "position": { "x": 560, "y": 400 }, "size": { "width": 240, "height": 60 }, "style": { "fill": "#eadfff", "stroke": "#8b6dff" } },
    { "id": "db", "type": "rect", "label": "Postgres", "kind": "database", "position": { "x": 1020, "y": 160 }, "size": { "width": 220, "height": 90 }, "style": { "fill": "#ffe7c2", "stroke": "#d8892b" } },
    { "id": "cache", "type": "rect", "label": "Redis", "kind": "cache", "position": { "x": 1020, "y": 280 }, "size": { "width": 220, "height": 90 }, "style": { "fill": "#ffe7c2", "stroke": "#d8892b" } },
    { "id": "auth", "type": "rect", "label": "Auth Provider", "kind": "external", "position": { "x": 720, "y": 680 }, "size": { "width": 220, "height": 80 }, "style": { "fill": "#dff7e8", "stroke": "#5cbf8f" } }
  ],
  "edges": [
    { "id": "e1", "from": "web-app", "to": "cdn", "type": "arrow", "label": "static", "data": { "kind": "http" } },
    { "id": "e2", "from": "web-app", "to": "api", "type": "arrow", "label": "api calls", "data": { "kind": "http" } },
    { "id": "e3", "from": "api", "to": "db", "type": "arrow", "label": "queries", "data": { "kind": "db" } },
    { "id": "e4", "from": "api", "to": "cache", "type": "arrow", "label": "cache", "data": { "kind": "cache" } },
    { "id": "e5", "from": "api", "to": "queue", "type": "arrow", "label": "enqueue", "data": { "kind": "queue" } },
    { "id": "e6", "from": "queue", "to": "worker", "type": "arrow", "label": "jobs", "data": { "kind": "queue" } },
    { "id": "e7", "from": "web-app", "to": "auth", "type": "dashed", "label": "oauth", "data": { "kind": "auth" } }
  ]
}
```

## Example 2: Navigation Flow

```json
{
  "version": "0.1",
  "name": "Quiz Navigation Flow",
  "diagram": { "type": "flow" },
  "canvas": { "width": 1200, "height": 800, "grid": 16, "background": "dots" },
  "nodes": [
    { "id": "learn-tab", "type": "rect", "label": "Learn Tab\n(index.tsx)", "position": { "x": 120, "y": 160 }, "size": { "width": 180, "height": 80 } },
    { "id": "quiz-card", "type": "rect", "label": "Quiz Card", "position": { "x": 380, "y": 160 }, "size": { "width": 160, "height": 80 } },
    { "id": "quiz-intro", "type": "rect", "label": "Quiz Intro\n/quiz", "position": { "x": 620, "y": 160 }, "size": { "width": 180, "height": 80 } },
    { "id": "quiz-play", "type": "rect", "label": "Quiz Play\n/quiz/play", "position": { "x": 620, "y": 300 }, "size": { "width": 180, "height": 80 } },
    { "id": "quiz-results", "type": "rect", "label": "Quiz Results\n/quiz/results", "position": { "x": 620, "y": 440 }, "size": { "width": 180, "height": 80 } }
  ],
  "edges": [
    { "id": "e1", "from": "learn-tab", "to": "quiz-card", "type": "arrow", "label": "tap" },
    { "id": "e2", "from": "quiz-card", "to": "quiz-intro", "type": "arrow", "label": "open" },
    { "id": "e3", "from": "quiz-intro", "to": "quiz-play", "type": "arrow", "label": "start" },
    { "id": "e4", "from": "quiz-play", "to": "quiz-results", "type": "arrow", "label": "finish" }
  ]
}
```

## Example 3: UI Mockup

```json
{
  "version": "0.1",
  "name": "Quiz Intro Mockup",
  "diagram": { "type": "ui" },
  "canvas": { "width": 1000, "height": 900, "grid": 8, "background": "dots" },
  "nodes": [
    {
      "id": "iphone", "type": "device", "label": "iPhone 14",
      "position": { "x": 120, "y": 80 }, "size": { "width": 430, "height": 900 },
      "device": { "platform": "ios", "model": "iphone-14", "safeArea": { "top": 47, "bottom": 34, "left": 0, "right": 0 }, "screen": { "width": 390, "height": 844 } },
      "style": { "fill": "#111111", "stroke": "#333333", "cornerRadius": 48 }
    },
    {
      "id": "title", "type": "component", "label": "Title",
      "parentId": "iphone",
      "position": { "x": 170, "y": 200 }, "size": { "width": 300, "height": 40 },
      "component": { "type": "text", "variant": "title", "text": "Test Your Knowledge" }
    },
    {
      "id": "score-card", "type": "component", "label": "Best Score",
      "parentId": "iphone",
      "position": { "x": 170, "y": 260 }, "size": { "width": 300, "height": 110 },
      "component": { "type": "card", "title": "Best Score", "text": "4/5" }
    },
    {
      "id": "start-button", "type": "component", "label": "Start",
      "parentId": "iphone",
      "position": { "x": 170, "y": 410 }, "size": { "width": 300, "height": 56 },
      "component": { "type": "button", "variant": "primary", "text": "Start Quiz", "action": "StartQuiz" }
    }
  ],
  "edges": []
}
```
