---
name: translate-to-english
description: Translate a specified file to English and save it as a new file with an '-en' suffix.
argument-hint: The path of the file to translate
---
Translate the specified file into English and save it as a new file.

Follow these steps:
1.  **Identify the file**: If the user has not specified a file, ask them which file they want to translate.
2.  **Read and Translate**: Read the content of the specified file and translate it into natural, professional English. Keep the original formatting and structure.
3.  **Create New File**:
    *   Determine the new filename by appending `-en` to the original filename (before the extension).
        *   Example: `article.md` -> `article-en.md`
    *   Create the new file with the translated content.
