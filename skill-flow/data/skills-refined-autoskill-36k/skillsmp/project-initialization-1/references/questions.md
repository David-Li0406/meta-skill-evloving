# Interactive Wizard Questions

Question templates for /project-guide and /brand-guide commands.
Use AskUserQuestion tool with these structures.

## PROJECT.md Questions

### Basic Information

#### Q1: Project Name
```json
{
  "question": "What is the name of your project?",
  "header": "Name",
  "options": [
    {"label": "I have a name", "description": "Enter your project name"},
    {"label": "Help me brainstorm", "description": "Let's come up with a name together"}
  ],
  "multiSelect": false
}
```

#### Q2: Project Type
```json
{
  "question": "What type of project is this?",
  "header": "Type",
  "options": [
    {"label": "SaaS Application", "description": "Web-based software as a service"},
    {"label": "Mobile Application", "description": "iOS/Android app (Flutter)"},
    {"label": "Plugin/Package", "description": "Reusable library or extension"},
    {"label": "Website", "description": "Marketing site or web application"}
  ],
  "multiSelect": false
}
```

### Purpose

#### Q3: Target Audience
```json
{
  "question": "Who is the primary target audience?",
  "header": "Audience",
  "options": [
    {"label": "Developers", "description": "Technical users building software"},
    {"label": "Small Business", "description": "SMB owners and employees"},
    {"label": "Enterprise", "description": "Large organizations"},
    {"label": "Consumers", "description": "General public end users"}
  ],
  "multiSelect": false
}
```

#### Q4: Problem Category
```json
{
  "question": "What category of problem does this solve?",
  "header": "Problem",
  "options": [
    {"label": "Productivity", "description": "Saving time, automating tasks"},
    {"label": "Communication", "description": "Better collaboration, messaging"},
    {"label": "Commerce", "description": "Buying, selling, transactions"},
    {"label": "Data/Analytics", "description": "Insights, reporting, monitoring"}
  ],
  "multiSelect": false
}
```

### Features

#### Q5: Feature Priority
```json
{
  "question": "Which features are most important? (Select up to 3)",
  "header": "Features",
  "options": [
    {"label": "User Authentication", "description": "Login, registration, profiles"},
    {"label": "Data Management", "description": "CRUD operations, storage"},
    {"label": "Payments", "description": "Billing, subscriptions, invoicing"},
    {"label": "Notifications", "description": "Email, push, in-app alerts"}
  ],
  "multiSelect": true
}
```

### Research

#### Q6: Competitive Research
```json
{
  "question": "Would you like me to research competitors and market?",
  "header": "Research",
  "options": [
    {"label": "Yes, research competitors", "description": "I'll search for similar products and analyze them"},
    {"label": "I know my competitors", "description": "I'll provide competitor information"},
    {"label": "No research needed", "description": "Skip competitive analysis"}
  ],
  "multiSelect": false
}
```

### Metrics

#### Q7: Success Definition
```json
{
  "question": "How will you measure success?",
  "header": "Metrics",
  "options": [
    {"label": "User Growth", "description": "Signups, active users, retention"},
    {"label": "Revenue", "description": "MRR, ARR, transaction volume"},
    {"label": "Engagement", "description": "Time in app, feature usage"},
    {"label": "Custom Metrics", "description": "I'll define specific KPIs"}
  ],
  "multiSelect": true
}
```

---

## BRAND.md Questions

### Personality

#### Q1: Brand Style
```json
{
  "question": "What personality style fits your brand?",
  "header": "Style",
  "options": [
    {"label": "Modern & Minimal", "description": "Clean lines, lots of whitespace, simple"},
    {"label": "Bold & Vibrant", "description": "Strong colors, attention-grabbing, energetic"},
    {"label": "Professional & Classic", "description": "Timeless, trustworthy, corporate feel"},
    {"label": "Playful & Friendly", "description": "Fun, approachable, casual"}
  ],
  "multiSelect": false
}
```

#### Q2: Formality Level
```json
{
  "question": "How formal should the brand feel?",
  "header": "Formality",
  "options": [
    {"label": "Very Formal", "description": "Corporate, enterprise, institutional"},
    {"label": "Professional", "description": "Business casual, trustworthy"},
    {"label": "Casual", "description": "Friendly, approachable, conversational"},
    {"label": "Very Casual", "description": "Fun, playful, informal"}
  ],
  "multiSelect": false
}
```

### Colors

#### Q3: Primary Color Direction
```json
{
  "question": "What primary color direction do you prefer?",
  "header": "Color",
  "options": [
    {"label": "Blue (Trust)", "description": "Professional, trustworthy, calm - great for B2B"},
    {"label": "Green (Growth)", "description": "Natural, success, health - great for finance, health"},
    {"label": "Purple (Premium)", "description": "Creative, luxury, wisdom - great for premium brands"},
    {"label": "Orange (Energy)", "description": "Enthusiastic, confident, friendly - great for consumer apps"}
  ],
  "multiSelect": false
}
```

#### Q4: Color Mood
```json
{
  "question": "What mood should the colors convey?",
  "header": "Mood",
  "options": [
    {"label": "Calm & Serene", "description": "Soft, muted colors, lots of white"},
    {"label": "Energetic & Dynamic", "description": "Vibrant, saturated colors"},
    {"label": "Sophisticated & Elegant", "description": "Deep, rich tones"},
    {"label": "Fresh & Modern", "description": "Bright, clean, contemporary"}
  ],
  "multiSelect": false
}
```

#### Q5: Theme Default
```json
{
  "question": "What should be the default theme?",
  "header": "Theme",
  "options": [
    {"label": "Light Theme (Recommended)", "description": "White/light gray backgrounds, dark text"},
    {"label": "Dark Theme", "description": "Dark backgrounds, light text"},
    {"label": "Both Equally", "description": "Design for both from the start"}
  ],
  "multiSelect": false
}
```

### Typography

#### Q6: Font Style
```json
{
  "question": "What font style do you prefer for headings?",
  "header": "Fonts",
  "options": [
    {"label": "Modern Sans-serif", "description": "Inter, SF Pro, Geist - clean and contemporary"},
    {"label": "Geometric Sans", "description": "Poppins, Montserrat - structured and balanced"},
    {"label": "Classic Serif", "description": "Georgia, Lora - traditional and trustworthy"},
    {"label": "System Fonts", "description": "Native fonts for best performance"}
  ],
  "multiSelect": false
}
```

### Voice

#### Q7: Communication Tone
```json
{
  "question": "How should the brand communicate?",
  "header": "Tone",
  "options": [
    {"label": "Direct & Concise", "description": "Get to the point, no fluff"},
    {"label": "Friendly & Warm", "description": "Approachable, conversational"},
    {"label": "Expert & Authoritative", "description": "Knowledgeable, confident"},
    {"label": "Playful & Witty", "description": "Fun, clever, humorous"}
  ],
  "multiSelect": false
}
```

#### Q8: Technical Level
```json
{
  "question": "How technical should the language be?",
  "header": "Technical",
  "options": [
    {"label": "Very Technical", "description": "Use industry jargon, assume expertise"},
    {"label": "Moderately Technical", "description": "Explain terms when needed"},
    {"label": "Simple & Clear", "description": "Avoid jargon, use plain language"},
    {"label": "Beginner Friendly", "description": "Explain everything, assume no knowledge"}
  ],
  "multiSelect": false
}
```

### Research

#### Q9: Design Inspiration
```json
{
  "question": "Would you like me to research design inspiration?",
  "header": "Inspiration",
  "options": [
    {"label": "Yes, find inspiration", "description": "Search for similar brands and design trends"},
    {"label": "I have references", "description": "I'll provide brand references"},
    {"label": "Skip research", "description": "Create based on answers only"}
  ],
  "multiSelect": false
}
```

---

## Question Flow Guidelines

### PROJECT.md Flow
1. Basic Info (Q1-Q2) → Get name and type
2. Purpose (Q3-Q4) → Understand audience and problem
3. Features (Q5) → Define core features
4. Research (Q6) → Optional competitor research
5. Metrics (Q7) → Define success

### BRAND.md Flow
1. Read PROJECT.md if exists
2. Personality (Q1-Q2) → Style and formality
3. Colors (Q3-Q5) → Palette direction
4. Typography (Q6) → Font choices
5. Voice (Q7-Q8) → Communication style
6. Research (Q9) → Optional inspiration

### Best Practices
- Ask one question at a time
- Use user's previous answers to inform next questions
- Allow "Other" option for custom input
- Summarize choices before generating
