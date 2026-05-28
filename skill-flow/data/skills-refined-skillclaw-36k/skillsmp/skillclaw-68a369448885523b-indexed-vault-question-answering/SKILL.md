---
name: indexed-vault-question-answering
description: Use this skill when you need to answer questions from indexed vault content using a retrieval-augmented generation (RAG) approach, including setup, configuration, and troubleshooting.
---

# Skill body

1. **Setup the Environment**
   - Ensure you have access to the indexed vault content.
   - Install necessary libraries for RAG retrieval (e.g., `transformers`, `torch`).

2. **Configure the RAG Retriever**
   - Load your indexed vault data into the RAG retriever.
   - Set parameters for the retriever, such as the number of retrieved documents.

3. **Perform a Query**
   - Input your question into the RAG retriever.
   - Retrieve relevant documents from the indexed vault.

4. **Generate an Answer**
   - Use the retrieved documents to generate an answer using a language model.
   - Ensure the answer is coherent and directly addresses the question.

5. **Troubleshooting**
   - If the answer is unsatisfactory, check the configuration settings.
   - Verify that the indexed vault content is correctly formatted and accessible.
   - Adjust the parameters of the retriever as needed for better results.