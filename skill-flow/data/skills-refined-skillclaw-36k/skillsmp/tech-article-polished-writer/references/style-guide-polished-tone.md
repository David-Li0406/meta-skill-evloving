# Polished Tone Style Guide

This guide defines standards for generating clear, professional, and natural Japanese technical articles. The goal is to produce content that feels authoritative yet accessible, avoiding both robotic stiffness and excessive casualness.

---

## ⚠️ BEFORE YOU WRITE: FORBIDDEN PATTERNS CHECK

**Read this FIRST. These patterns degrade professional quality and signal "AI-generated" or "Amateur" writing.**

### ❌ FORBIDDEN PATTERN #1: Casual/Slang Sentence Endings

**NEVER use casual or slang endings in the main text:**

❌ "〜だね。" → ✅ "〜ですね。"
❌ "〜じゃん。" → ✅ "〜ですよね。" or "〜ではありませんか。"
❌ "〜してる。" → ✅ "〜しています。" (Contracted forms are strictly forbidden)
❌ "〜ちゃう。" → ✅ "〜してしまう。"

**Rule**: Maintain standard written Japanese grammar. Avoid conversational contractions (e.g., "してる" → "している", "とく" → "ておく").

### ❌ FORBIDDEN PATTERN #2: Unprofessional Connectors

**Avoid overly casual or abrupt transitions:**

❌ "で、次は..." → ✅ "では、次は..." or "次に、"
❌ "なんか、..." → ✅ "なんとなく..." or "ある種..." (or remove entirely)
❌ "ぶっちゃけ..." → ✅ "実のところ..." or "正直に言えば..."
❌ "〜的な。" → ✅ "〜のような。"

### ❌ FORBIDDEN PATTERN #3: Robotic Repetition (AI-isms)

**Avoid patterns typical of raw AI output:**

❌ Starting consecutive paragraphs with "また、" (Also,) or "さらに、" (Furthermore,).
❌ Ending every section with "いかがでしたでしょうか。" (How was it?).
❌ Excessive use of "私" (I) or "私たち" (We) where the subject is implied.
❌ Overuse of "〜することができます" (can do) → ✅ "〜できます" or "〜可能です".

### ❌ FORBIDDEN PATTERN #4: Colons (：) in Prose

**NEVER use full-width colon to introduce code or lists in flowing prose:**

❌ "以下のコードです：" → ✅ "以下のコードです。"
❌ "ポイントは：" → ✅ "ポイントは以下の通りです。"

---

## 🔴 CRITICAL REQUIREMENTS (Publication Blockers)

### 1. Consistent Polite Tone (Desu/Masu)

**Requirement**: Use `Desu/Masu` (です/ます) style consistently for the main body text.

-   **Main Text**: です/ます (Polite form).
-   **Headings**: Noun phrases (体言止め) or simple verb forms.
-   **Bullet Points**: Can be noun phrases or polite forms, but must be consistent within the list.

**Why?** This creates a respectful, professional relationship with the reader.

### 2. Logical Structure & Clarity

**Requirement**: Content must be logically organized and easy to follow.

-   **Introduction**: Clearly state the problem and the solution/goal.
-   **Body**: Use clear headings (H2, H3) to break down topics.
-   **Conclusion**: Summarize key points effectively (unlike the "Human Tone" messy conclusion, Polished Tone values a clear summary).

### 3. Professional Vocabulary

**Requirement**: Use standard technical terminology.

-   **Katakana**: Avoid unnecessary katakana if a standard Japanese term exists and is common (e.g., "エビデンス" → "根拠" depending on context, but "コミット" is fine).
-   **Definitions**: Define complex terms if the audience might not know them.

---

## 📋 WRITING STYLE GUIDELINES

### 4.1 Sentence Structure

**Aim for clarity and rhythm.**

-   **Sentence Length**: Keep sentences moderate in length (approx. 40-60 characters). Split long sentences.
-   **Subject-Predicate Agreement**: Ensure the subject and verb match logically.
-   **Active Voice**: Prefer active voice where possible for directness.

### 4.2 Natural Phrasing

**Avoid direct translation styles.**

❌ "それは〜を提供します。" (It provides...) → ✅ "〜が可能です。" or "〜を備えています。"
❌ "〜を行うことができます。" → ✅ "〜できます。"

### 4.3 Objective Perspective

**Maintain a professional distance.**

-   Avoid "I think" (〜と思います) for factual technical statements. Use "〜です" or "〜と言えます".
-   Use "〜と考えられます" (It is considered...) for logical deductions.

### 4.4 Code Explanations

**Explain "Why" and "How".**

-   Don't just paste code. Explain what it does.
-   Highlight key parts of the code.
-   Ensure code examples are functional and follow best practices.

---

## 🟢 POLISH: Final Refinements

### 5.1 Formatting Standards

-   **Headings**: Use H2 and H3. Avoid H4 unless absolutely necessary.
-   **Lists**: Use bullet points for items, numbered lists for steps.
-   **Emphasis**: Use **bold** for key terms, but do not overuse (max 1-2 per paragraph).
-   **Code Blocks**: Always specify the language (e.g., \`\`\`typescript).

### 5.2 Self-Correction

**Review your text for:**
-   **Redundancy**: Are you saying the same thing twice?
-   **Ambiguity**: Is the meaning clear?
-   **Tone Consistency**: Did you slip into casual speech?

---

## ⚠️ TOP AI TELLS TO AVOID (Polished Edition)

1.  **"In conclusion" (まとめ)**: Don't just repeat the intro. Add value or a final thought.
2.  **"It is important to..."**: Avoid generic advice. Be specific.
3.  **Overuse of connectors**: "Therefore," "However," "In addition" at the start of every sentence.
4.  **Vague praise**: "This is a very powerful tool." → Explain *why* it is powerful.
5.  **Lack of context**: Jumping into code without explaining the problem it solves.

---

**Goal**: To create content that reads as if written by a skilled, professional technical writer—clear, concise, and trustworthy.