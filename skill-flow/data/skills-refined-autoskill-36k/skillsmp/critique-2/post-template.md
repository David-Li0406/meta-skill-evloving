# krzy.ai Post Template

## File Location

All posts live in: `~/repos/krzy/src/posts/data.ts`

## Data Structure

```typescript
// Post metadata
export interface Post {
  slug: string        // URL-friendly identifier (lowercase, hyphens)
  title: string       // Display title
  subtitle?: string   // Optional subtitle
  date: string        // YYYY-MM-DD format
  tags?: string[]     // Array of tag strings
}

// Add to posts array (newest first)
export const posts: Post[] = [
  {
    slug: 'your-post-slug',
    title: 'Your Post Title',
    subtitle: 'Optional Subtitle',
    date: '2025-12-31',
    tags: ['component', 'theme'],
  },
  // ... existing posts
]

// Add content to postContents object
const postContents: Record<string, string> = {
  'your-post-slug': `
<h2>Section Heading</h2>
<p>Content here...</p>
`,
  // ... existing content
}
```

---

## Critique Post Structure

### Title Formats

```
"Critique: [Component] [Version]"
"Critique: [Feature Name]"
"Critique: The [Concept] Question"
"[Component]: [Provocative Question]"
```

### Subtitle Formats

```
"[Metaphor] and the [Theme]"
"On [Topic] and [Related Topic]"
"A [Examination/Analysis] of [Subject]"
```

### Standard Tags

| Tag | Use For |
|-----|---------|
| `dol` | DOL language critiques |
| `vudo` | VUDO runtime critiques |
| `enr` | ENR economics critiques |
| `cryptosaint` | CryptoSaint credit critiques |
| `spirit` | Spirit package critiques |
| `learn` | learn.univrs.io critiques |
| `identity` | Identity system critiques |
| `network` | Network layer critiques |
| `critique` | General critical analysis |
| `precedents` | Historical comparisons |
| `power` | Power structure analysis |
| `economics` | Economic analysis |
| `governance` | Governance analysis |

---

## Content Structure

### Opening Section

Start with context and the core question:

```html
<h2>I. The [Frame/Context/Setup]</h2>
<p>Historical or contextual opening that sets up the critique.</p>
<p>The specific change or feature being examined.</p>
<p>The question this critique will answer.</p>
```

### Analysis Sections

Use Roman numerals for major sections:

```html
<h2>II. [Analysis Topic]</h2>
<p>Examination of specific aspect.</p>

<h2>III. [Another Topic]</h2>
<p>Further analysis.</p>
```

### The Six Questions (When Applicable)

```html
<h2>IV. Who Benefits?</h2>
<p>Analysis of value flow.</p>
<ul>
  <li>First beneficiary</li>
  <li>Second beneficiary</li>
</ul>

<h2>V. Who Pays?</h2>
<p>Analysis of costs.</p>
<ol>
  <li><strong>Infrastructure cost:</strong> Description</li>
  <li><strong>Labor cost:</strong> Description</li>
  <li><strong>Sovereignty cost:</strong> Description</li>
</ol>

<h2>VI. The Gap</h2>
<p>Promise vs. reality analysis.</p>
<blockquote>
  <p><em>Promise: [Stated claim]</em></p>
  <p><em>Reality: [Current state]</em></p>
</blockquote>
```

### Blockquotes

Use for:
- Quotes from documentation or code
- The builder's potential response
- Key insights or warnings

```html
<blockquote>
  <p>Quote text here.</p>
</blockquote>

<blockquote>
  <p><em>Italicized quote for emphasis.</em></p>
</blockquote>
```

### Code References

When citing specific code:

```html
<p>In <code>capability.rs</code>, the 14 capability types are defined:</p>
<ul>
  <li><strong>Network*</strong> - NetworkListen, NetworkConnect, NetworkBroadcast</li>
  <li><strong>Storage*</strong> - StorageRead, StorageWrite, StorageDelete</li>
</ul>
```

### Lists

```html
<!-- Unordered for concepts -->
<ul>
  <li>First point</li>
  <li>Second point</li>
</ul>

<!-- Ordered for sequences or rankings -->
<ol>
  <li><strong>First:</strong> Description</li>
  <li><strong>Second:</strong> Description</li>
</ol>
```

### Closing Section

End with the path forward or open question:

```html
<h2>VIII. The Path Forward</h2>
<p>Recommendations or awareness points:</p>
<ol>
  <li><strong>Recommendation one</strong> with explanation.</li>
  <li><strong>Recommendation two</strong> with explanation.</li>
</ol>
<p>Closing thought that invites response.</p>

<hr />
<p><em>Closing note or call for continued critique.</em></p>
```

---

## Voice and Tone

### Do

- Use specific code references and commit hashes
- Ask genuine questions (not rhetorical attacks)
- Acknowledge complexity and trade-offs
- Invite builder response
- Ground in Luddite history and precedent
- Be self-aware about the critic's limitations

### Don't

- Attack motives without evidence
- Demand perfection
- Ignore context
- Pretend to have all answers
- Be cynical without cause
- Dismiss genuine progress

### Example Phrases

**Opening a critique:**
> "The latest release of [component] introduces [feature]. The question is not whether it works, but who it works for."

**Acknowledging complexity:**
> "This is not a simple case of good and evil. The architecture reflects genuine trade-offs between [X] and [Y]."

**The builder's counter:**
> "The platform engineer might respond: '[likely response].' This is fair. But..."

**Closing with invitation:**
> "This critique is not a verdict. It is an invitation to examine, to respond, to adjust. The dialogue continues."

---

## Complete Example

```typescript
// In posts array
{
  slug: 'critique-vudo-capabilities',
  title: "VUDO's 14 Capabilities",
  subtitle: 'Permission Systems and Power',
  date: '2025-01-15',
  tags: ['vudo', 'critique', 'power', 'governance'],
},

// In postContents
'critique-vudo-capabilities': `
<h2>I. The Gate and the Gatekeeper</h2>
<p>VUDO's capability system defines 14 types of permission that a Spirit can request. Each capability is a key. The question is: who holds the keyring?</p>

<h2>II. The 14 Capabilities</h2>
<p>In <code>capability.rs</code>, the system defines:</p>
<ul>
  <li><strong>Network:</strong> Listen, Connect, Broadcast</li>
  <li><strong>Storage:</strong> Read, Write, Delete</li>
  <li><strong>Compute:</strong> SpawnSandbox, CrossSandboxCall</li>
  <li><strong>Sensor:</strong> Time, Random, Environment</li>
  <li><strong>Actuator:</strong> Log, Notify, Credit</li>
  <li><strong>Special:</strong> Unrestricted (system only)</li>
</ul>

<h2>III. Who Grants?</h2>
<p>The capability grant mechanism determines who can access what. Currently:</p>
<ol>
  <li><strong>Manifest declaration:</strong> Spirits request capabilities in their manifest</li>
  <li><strong>Signature verification:</strong> Ed25519 signatures validate the request</li>
  <li><strong>Runtime enforcement:</strong> VUDO VM checks capabilities on every host call</li>
</ol>
<p>But who approves the manifest? Who signs the key?</p>

<h2>IV. The Precedent</h2>
<p>Mobile app permissions followed a similar arc:</p>
<blockquote>
  <p><em>First, users controlled permissions. Then, apps demanded all-or-nothing. Finally, users clicked "Allow All" out of fatigue.</em></p>
</blockquote>
<p>Will VUDO capabilities follow the same path?</p>

<h2>V. The Path Forward</h2>
<ol>
  <li><strong>Transparent grant logs:</strong> Make all capability grants visible and auditable.</li>
  <li><strong>Minimal defaults:</strong> Spirits should work with minimal capabilities by default.</li>
  <li><strong>Revocation mechanisms:</strong> Users must be able to revoke granted capabilities.</li>
</ol>

<hr />
<p><em>This is an ongoing examination. As the capability system evolves, so will this critique.</em></p>
`,
```

---

## Adding a New Critique

### Step 1: Generate Metadata

```typescript
{
  slug: 'critique-[component]-[topic]',
  title: '[Descriptive Title]',
  subtitle: '[Thematic Subtitle]',
  date: 'YYYY-MM-DD',  // Today's date
  tags: ['[component]', 'critique', '[themes]'],
},
```

### Step 2: Write Content

Follow the structure above, applying the Luddite framework from `framework.md`.

### Step 3: Add to File

1. Add metadata to `posts` array (at the TOP, newest first)
2. Add content to `postContents` object (key must match slug exactly)

### Step 4: Verify

```bash
cd ~/repos/krzy
npm run dev
# Visit http://localhost:3000/posts/[your-slug]
```

### Step 5: Commit

```bash
git add src/posts/data.ts
git commit -m "Add critique: [title]"
```

---

*Template last updated: December 2025*
