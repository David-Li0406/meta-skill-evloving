---
name: jupyter-notebook-management
description: Use this skill when you need to create, refactor, or manage Jupyter Notebooks (.ipynb) programmatically.
---

# Skill body

## Create Notebook

This section generates a Jupyter Notebook to demonstrate a feature or explain a concept.

### Instructions

1. **Plan the Notebook**:
    * **Title & Introduction**: Define the purpose of the notebook.
    * **Setup/Imports**: List necessary imports.
    * **Data Generation/Loading**: Create synthetic data or load sample data.
    * **Processing/Analysis**: Demonstrate the core feature.
    * **Visualization**: Plot the results.

2. **Create File**:
    * Use the `write_to_file` tool to create the `.ipynb` file. Ensure you use a valid JSON structure or a helper script if available.
    * Alternatively, write a Python script `make_notebook.py` using `nbformat` and execute it.

3. **Content Requirements**:
    * Use Markdown cells to explain *why* and *how*.
    * Comment the code cells extensively.
    * Ensure the code is runnable without external local files (or create them on the fly).

## Refactor Notebook

This section is for programmatically analyzing and modifying Jupyter Notebook (.ipynb) files.

### Instructions

1. **Analyze Notebook Structure**:
    * Load `.ipynb` files as JSON using Python and iterate through the `cells` list.
    * Verify if the `cell_type` of each cell is `code`.

2. **Filter and Match**:
    * Join the `source` field (list format) into a string and use regular expressions or keyword matching to identify target cells.
    * Target specific import statements, function calls, or comments.

3. **Implement Transformation**:
    * Create a transformation script to rewrite the `source` list of the cells in memory.
    * Ensure the updated source remains in list format (each element as a string ending with a newline).

4. **Write and Verify**:
    * Save the file using `json.dump`, maintaining an indent of 1 and specifying `ensure_ascii=False`.
    * Verify that the resulting notebook is valid JSON and that the intended changes have been applied.

## Usage Guidelines

* When modifying multiple notebooks across a directory, create a loop script that collects `.ipynb` files using `glob` or similar.
* For complex refactoring, save the logic as a temporary `.py` script, execute it via `run_command`, and then delete the script.