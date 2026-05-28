---
name: planning-code-file-content-simplification
description: You are planning to simplify and improve the content of a file.  The goal is to make it more understandable, maintainable and debuggable.
---

# Planning Code File Content Simplification Skill

This skill provides information on how to plan the simplification of the content of a file.  The goal is to improve the existing code so that it is more logically organised, understandable, maintainable and more easily debugged.

## Planning Code File Content Simplification Considerations

- Enter planning mode when planning to simplify and improve the content of a file
- Understand the coding language that is being simplified, make sure to read any skills that relate to the coding language (e.g. developing-csharp-code for CSharp code).
- Use language best practises
- Ensure that there are unit tests for the file / area of the file to be simplified and that they provide comprehensive line coverage, approximately 90% or more for that part to be simplified.  The tests can be updated but the intent behind each test should not change.
- Understand the code you have been asked to simplify and ensure it exists.
- Right size the task, its important to not make changes to too big of an area of code.  If a class or function is medium to large in size and new helper classes are required, then the task should be size such that only one additional simple helper class is created and the remainder of the code can be left untouched for this task.
- Think and create a step by step high level plan for simplifying the code area, make sure you use the orchestrating-code-simplification and developing-csharp-code skills for this task.  Apply best practises outlined in these skills.
- Keep interating on the code until a suitable level of simplification has been achieved.  Code should be analysed for each best practise.
