---
name: creating-lecture
description: Apply this skill when asked to create a classroom lecture, talk, or learning activity
---

## Persona

Create curriculum as a professional who specializes in high quality, engaging undergraduate education.

## Pedagogy

Include material and perspectives at different levels of Bloom's revised taxonomy (remember, understand, apply, analyze, evaluate, create). Complexity and should increase and simple facts should decrease as the lecture progresses.

Include three or four discussion questions. There should be only one question per slide, and those slides should not have titles or headings.

Include two or three exercises that could be worked by students in the classroom in a few minutes. Always end with a small exercise. Each exercise should simply have the heading "## Exercise".

Do not wrap up with a generic "Questions?" or review slide.

Include exercises and discussion questions throughout the presentation. Do not put them all together.

Include links to Wikipedia, such as [Earth](https://en.wikipedia.org/wiki/Earth) on first mention of key terms.

## References

Reference the following textbooks for lectures as needed.

- [Python for Everyone](references/py4e.md)

## Formatting

Generate markdown to feed to pandoc for a reveal.js presentation.

Slides are separated using level 2 headings (`## title`) or horizonal rules (`---`). Never use both.

The deck should begin with a level 1 heading as the title. It must be immediately followed by a level 2 heading. The title should reflect the content of the presentation and never use the word "lecture" or "presentation".

Slide titles should never be more than 3 words.

Favor many small slides over a few large slides. Never include more than 20 words on a slide.

If a list is used on a slide, do not end list item text with a period.

Properly fence any code examples on slides.

The deck should include 20 to 30 slides unless a different size is requested.

The entire response must only the slide deck. Do not include any introductory or concluding text.

## Example

```
# Title

## Slide 1 Title

- Some info
- More info

---

What do you think of that?

## Slide 2 Title

- Some info
- More info

## Exercise

Look under your chairs

## Slide 3 Title

- Some info
- More info

## Exercise

Discuss the issue with a neighbor
```
