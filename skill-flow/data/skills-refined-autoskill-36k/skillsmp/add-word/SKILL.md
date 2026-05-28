---
name: add-word
description: Add a single Arabic word to the flashcard system. Use when the user wants to add a word, add vocabulary, or says something like "add [word]" or "add the word [word]". Checks for duplicates, suggests appropriate deck, and confirms before adding.
---

# Add Single Word

This skill adds individual Arabic words to the flashcard system on demand.

## Workflow

1. **Check for duplicates** → Search existing cards
2. **Lookup translation** → Use WebSearch if needed
3. **Fetch decks** → Get available decks
4. **Suggest deck** → Recommend based on word type
5. **Confirm** → Ask user before adding
6. **Add via API** → Create the card

## API Configuration

- **Base URL:** `https://learn.rocksbythesea.uk`
- **API Token:** Get from `.env.local` (`API_TOKEN`)
- All API requests must include the header: `-H "Authorization: Bearer $API_TOKEN"`

## Step 1: Check for Duplicates

Search all cards to see if the word already exists:

```bash
# Get all deck IDs, then check each deck's cards for the word
for id in $(curl -s -H "Authorization: Bearer $API_TOKEN" https://learn.rocksbythesea.uk/api/decks | jq -r '.[].id'); do
  curl -s -H "Authorization: Bearer $API_TOKEN" "https://learn.rocksbythesea.uk/api/decks/$id/cards" | jq -r --arg word "WORD" '.[] | select(.front | contains($word)) | "\(.front) -> \(.back) (deck: \(.deck_id))"'
done
```

This uses jq to:
- Extract deck IDs
- Search card fronts for the word
- Output matches with translation and deck info

If found, inform the user:
```
"كلب" already exists in deck "Nouns (الأسماء)" with translation "dog"
```

## Step 2: Lookup Translation (if needed)

If the user only provides the Arabic word without translation:
- Use WebSearch to find the English translation
- Present the translation to the user for confirmation

Example search: "Arabic word كلب meaning English translation"

## Step 3: Fetch Available Decks

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" https://learn.rocksbythesea.uk/api/decks
```

List the decks with their card counts to help decide placement.

## Step 4: Suggest Appropriate Deck

Based on the word type, suggest a deck:

| Word Type | Suggested Deck |
|-----------|----------------|
| Noun (person, place, thing) | Nouns (الأسماء) |
| Adjective (descriptive) | Adjectives (صفات) |
| Verb (action) | Verbs (الأفعال) - create if needed |
| Conjunction, preposition | Arabic Basics |
| Phrase | Phrases - create if needed |
| Unknown/mixed | Arabic Basics or create new |

## Step 5: Confirm with User

Present the word and ask for confirmation:

```
Word: كتاب
Translation: book
Suggested deck: Nouns (الأسماء) (ID: 6)

Add this word? Or choose a different deck:
1. Nouns (الأسماء)
2. Adjectives (صفات)
3. Arabic Basics
4. Create new deck...
```

## Step 6: Add via API

```bash
curl -X POST "https://learn.rocksbythesea.uk/api/decks/{deck_id}/cards" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '[{"front": "كتاب", "back": "book"}]'
```

## Step 7: Confirm Success

```
✓ Added "كتاب" (book) to deck "Nouns (الأسماء)"
```

## Examples

### Example 1: User provides word only
```
User: add the word مطبخ

1. Check duplicates → Not found
2. WebSearch "مطبخ Arabic meaning" → kitchen
3. Fetch decks → [Arabic Basics, Adjectives, Nouns]
4. Suggest: Nouns (it's a place/thing)
5. Confirm: "Add مطبخ (kitchen) to Nouns?"
6. User confirms → Add via API
7. Report: "✓ Added مطبخ (kitchen) to Nouns"
```

### Example 2: User provides word and translation
```
User: add يكتب - to write

1. Check duplicates → Not found
2. Translation provided: "to write"
3. Fetch decks → [Arabic Basics, Adjectives, Nouns]
4. Suggest: Need "Verbs" deck (doesn't exist)
5. Confirm: "Add يكتب (to write) to new deck 'Verbs (الأفعال)'?"
6. User confirms → Create deck, add card
7. Report: "✓ Created deck 'Verbs' and added يكتب (to write)"
```

### Example 3: Word already exists
```
User: add كلب

1. Check duplicates → Found in Nouns deck
2. Report: "كلب already exists in 'Nouns (الأسماء)' as 'dog'"
3. Ask: "Would you like to add it to a different deck anyway?"
```

## Moving Cards Between Decks

The API doesn't support changing a card's deck_id directly. To move a card:

1. Delete the card from the original deck:
```bash
curl -X DELETE "https://learn.rocksbythesea.uk/api/cards/{card_id}" \
  -H "Authorization: Bearer $API_TOKEN"
```

2. Recreate it in the new deck:
```bash
curl -X POST "https://learn.rocksbythesea.uk/api/decks/{new_deck_id}/cards" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '[{"front": "...", "back": "...", "notes": "..."}]'
```

**Note:** This resets the card's FSRS scheduling data (reviews, stability, etc.)

## Notes

- Always check for duplicates first to avoid redundant cards
- Preserve Arabic diacritics (tashkeel) if provided
- If user provides notes or context, include in the notes field
- Use WebSearch for translations when needed
- API Base URL: https://learn.rocksbythesea.uk
- Always include API key header in all requests
