---
name: jupyter-notebook-management
description: Use this skill when you need to create or refactor Jupyter Notebook (.ipynb) files for demonstration or analysis purposes.
---

# Jupyter Notebook Management

This skill encompasses the creation and refactoring of Jupyter Notebooks to demonstrate features or analyze code.

## Create Notebook

This section describes how to generate a Jupyter Notebook to demonstrate a feature or explain a concept.

### Instructions

1. **Plan the Notebook**:
    * **Title & Introduction**: Define the purpose of the notebook.
    * **Setup/Imports**: List necessary imports.
    * **Data Generation/Loading**: Create synthetic data or load sample data.
    * **Processing/Analysis**: Demonstrate the core feature.
    * **Visualization**: Plot the results.

2. **Create File**:
    * Use the `write_to_file` tool to create the `.ipynb` file. Ensure valid JSON structure or use a helper script if available.
    * Alternatively, write a Python script using `nbformat` to generate the notebook.

3. **Content Requirements**:
    * Use Markdown cells to explain *why* and *how*.
    * Comment code cells extensively.
    * Ensure the code is runnable without external local files or create them on the fly.

## Refactor Notebook

This section outlines how to programmatically analyze and modify Jupyter Notebooks.

### Instructions

1. **Analyze Notebook Structure**:
    * Load `.ipynb` files as JSON and iterate through the `cells` list.
    * Check if the `cell_type` of each cell is `code`.

2. **Filter and Match**:
    * Join the `source` field into a string and use regular expressions or keyword matching to identify target cells.
    * Target specific import statements, function calls, or comments.

3. **Implement Transformation**:
    * Create a transformation script to rewrite the `source` list of the cells in memory.
    * Ensure the updated source is in list format with each element as a string ending with a newline.

4. **Write and Verify**:
    * Save the modified notebook using `json.dump`, maintaining an indent of 1 and specifying `ensure_ascii=False`.
    * Verify the resulting notebook is valid JSON and that changes have been applied.

### Usage Guidelines

* For batch modifications across multiple notebooks, create a loop script to collect `.ipynb` files.
* For complex refactoring, save the logic as a temporary `.py` script, execute it, and then delete the script.