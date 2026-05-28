# Creative Communications - Validations

## Inconsistent Brand Voice

### **Id**
creative-inconsistent-voice
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(?:utilize|leverage|synergy).*(?:cool|awesome|rad|dope)
  - (?i)(?:greetings|salutations|dear sir).*(?:hey|yo|sup)
### **Message**
Inconsistent voice detected - mixing formal and casual language inappropriately
### **Fix Action**
Maintain consistent tone throughout - choose either formal, casual, or professional and stick with it
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Opening Hook

### **Id**
creative-missing-hook
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:imagine|what if|have you ever|did you know|\?|story|secret|warning|stop|attention|discover|revealed))
### **Message**
No compelling hook detected in opening - may fail to capture attention
### **Fix Action**
Start with a question, bold statement, surprising fact, or story to immediately engage readers
### **Applies To**
  - *.md
  - *.html

## Missing Storytelling Elements

### **Id**
creative-no-storytelling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:once|when|story|journey|struggled|discovered|realized|before|after|transformed|challenge|obstacle)).*$
### **Message**
No narrative or storytelling elements detected - missing emotional connection opportunity
### **Fix Action**
Incorporate story elements: character, challenge, transformation, or customer journey
### **Applies To**
  - *.md
  - *.html

## Cliché and Overused Phrases

### **Id**
creative-cliche-overuse
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?i)(?:think outside the box|low-hanging fruit|move the needle|at the end of the day|touch base|circle back|take it to the next level|win-win|game changer)\b
### **Message**
Clichés detected - reduces originality and impact of creative communication
### **Fix Action**
Replace clichés with original, specific language that paints a vivid picture
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Sensory or Descriptive Language

### **Id**
creative-no-sensory-language
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:see|hear|feel|touch|taste|smell|sound|look|appear|bright|dark|loud|soft|smooth|rough|warm|cold|crisp|vibrant)).*$
### **Message**
No sensory language detected - missing opportunity for vivid, engaging communication
### **Fix Action**
Add sensory details that help readers visualize, hear, or feel what you're describing
### **Applies To**
  - *.md
  - *.html

## Generic or Bland Headlines

### **Id**
creative-generic-headlines
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)^#\s+(?:welcome|introduction|about|overview|information|details|update|news)\s*$
  - (?i)^#\s+(?:our|the)\s+\w+\s*$
### **Message**
Generic headline detected - fails to intrigue or promise specific value
### **Fix Action**
Create headlines that are specific, promise a benefit, or create curiosity (e.g., use numbers, questions, or bold claims)
### **Applies To**
  - *.md
  - *.html

## Missing Emotional Triggers

### **Id**
creative-no-emotional-triggers
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:fear|hope|joy|anger|surprise|trust|love|hate|excited|worried|frustrated|relieved|proud|ashamed|confident|anxious)).*$
### **Message**
No emotional triggers detected - communication may feel flat or uninspiring
### **Fix Action**
Incorporate emotional language that resonates with audience feelings, aspirations, or pain points
### **Applies To**
  - *.md
  - *.html

## Monotonous Sentence Structure

### **Id**
creative-monotonous-structure
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?:^[A-Z][^.!?]{20,60}[.!?]\s*){4,}
### **Message**
Repetitive sentence structure detected - creates monotonous reading experience
### **Fix Action**
Vary sentence length and structure: mix short punchy sentences with longer ones, use questions and exclamations
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Metaphors or Analogies

### **Id**
creative-no-metaphor-analogy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:like|as if|similar to|imagine|picture|think of it as|it's like|compared to|metaphorically)).*$
### **Message**
No metaphors or analogies detected - missing opportunity to simplify complex ideas
### **Fix Action**
Use metaphors or analogies to make abstract concepts concrete and relatable
### **Applies To**
  - *.md
  - *.html

## Excessive Exclamation Marks

### **Id**
creative-excessive-exclamations
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - !{2,}
  - (?:![^!]{0,50}){4,}
### **Message**
Excessive exclamation marks detected - appears unprofessional or desperate
### **Fix Action**
Use exclamation marks sparingly (max 1-2 per piece) and let strong words carry the energy
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Corporate Jargon in Creative Content

### **Id**
creative-corporate-speak
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?i)(?:stakeholder|deliverable|bandwidth|ideation|actionable|takeaway|alignment|ecosystem|scalable|verticals)\b
### **Message**
Corporate jargon detected in creative content - reduces relatability and authenticity
### **Fix Action**
Replace corporate speak with conversational, human language that sounds natural when read aloud
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Visual Formatting for Emphasis

### **Id**
creative-no-visual-formatting
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:\*\*|__|\*|_|`|>|\n-|\n\*|\n\d+\.)).*$
### **Message**
No visual formatting detected - text may lack emphasis and scanability
### **Fix Action**
Use bold, italics, quotes, or lists to create visual hierarchy and emphasize key points
### **Applies To**
  - *.md

## Dense Text Walls Without Breaks

### **Id**
creative-walls-of-text
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?:[^\n]{200,}\n){3,}
### **Message**
Dense text blocks detected - intimidating and difficult to scan
### **Fix Action**
Break up text with subheadings, bullet points, short paragraphs, or whitespace for visual breathing room
### **Applies To**
  - *.md
  - *.html