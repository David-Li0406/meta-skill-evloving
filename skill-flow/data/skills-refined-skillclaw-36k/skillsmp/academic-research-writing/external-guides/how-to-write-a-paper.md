# How to Write a Paper - Guidelines

*Converted from How to Write a paper.docx*

This document provides guidelines on how to structure a conference paper. These are guidelines and should be viewed this way -- feel free to restructure to suit your work's needs.

---

## Abstract

Should have the same structure as the Introduction below. Replace "paragraph" with "sentence" and keep the same structure.

---

## Introduction

This section should address the following questions: What is the problem? Why is it important? What is your approach? What is the goal of your paper?

### Paragraph Structure

**1st paragraph**: What is the problem/task you are addressing in this paper? Why is it interesting; give some examples of applications if possible.

**2nd paragraph**: How have people attempted to solve it?

**3rd paragraph**: What are the limitations of past approaches? (These are the limitations that you will try to address and improve upon in this paper). How important is it to overcome these limitations in order to make progress? (That is -- why should people care about your contribution?)

**4th paragraph**: Introduce your proposed approach. Describe what you do that overcomes the aforementioned limitations.

**5th paragraph+**: Describe the benefits of your approach. Explain how you experimentally verify these benefits. Include a brief overview of the techniques and the experimental results -- enough so the readers get the gist. Include a paragraph that summarizes your key contributions (not too many; up to three).

### Visual Element

Ideally, the introduction would have a figure, a diagram, or an example (try to put it in the first page if possible) that attracts the readers' attention and explains a key point about the problem or the approach.

---

## Problem Definition

*(The title of this section could be more targeted to the topic of the paper/problem addressed)*

Give more details on the Task Definition - Introduce the model and/or problem you are studying and define the notation you are going to use.

---

## Methods

*(The title of this section could be more targeted to the topic of the paper/problem addressed)*

- Explain your solution (this could take multiple sections, or subsections)
- Mention expectations -- what do you expect your approach will accomplish and why

---

## Experimental Evaluation (and/or Theoretical Evaluation)

Often, this is where you provide proof of the arguments made earlier in the paper. It is also an opportunity to clearly and concisely present the claimed contributions of the paper (again) and map each contribution to the experiment(s) that illustrate it.

### Opening Statement

One good way to begin an experimental section is with (some version of) the statement:

> "The experiments in this section are designed to answer the following research questions:"

Now list 2-4 concise points that are the message of your paper and point to where/how you prove them.

### Key Subsections

An experimental section will typically have three key subsections:

1. **Experimental Setting**: Describe your implementation and experimental setting, key parameters and how they were set (don't do this earlier in the paper), etc.

2. **Key Experimental Results**: This is where the comparison to other approaches is done, and you highlight the results of the paper.

3. **Analysis**: This is where you analyze your own method -- ablation study or other ways. Examples are always useful in this section -- both successful and sometimes failures that provide insights and allow you to discuss something interesting. Which of these is emphasized more depends on the type of the paper.

**Note**: You can use an Appendix to include fine details for each of these sub-sections, provided that the main points are in the main paper.

---

## Tables and Figures

In most papers, tables and figures are the heart of the paper. Your message should be clear even if a reader only reads your abstract and the tables and figures.

### Key Principles

- **Reader-first thinking**: Imagine that readers only look at abstract + tables/figures, and plan accordingly
- **Avoid hidden acronyms**: Try to avoid acronyms that are defined "somewhere" in the paper
- **Choose the right format**: Have you chosen the right type of figure for the message you want to convey?
- **Minimize clutter**: Do you really need all the numbers? Do you want to show relative improvements rather than absolute numbers? (or maybe both). Is this data clearer in a bar-graph?
- **Statistical significance**: It often strengthens your arguments if you can include it

### Caption Requirements

- The caption, along with the table/figure, need to be self-explanatory
- Make the message of this table/figure clear in the caption (if the table/figure has no goal, don't include it)
- Explain what is shown and how it supports the message
- Use figures also for examples -- illustrate the problem or the difference your solution makes

---

## Related Work

### Placement Options

The related work section isn't strictly necessary as a separate section. Options:
- At the end of the introduction
- Throughout the paper (if analysis-focused)
- As a separate section after introduction (most common)
- Before Discussion/Conclusion section

### Goals

In all cases, the goal is to:
1. Show an understanding of the field
2. Position the current paper relative to it

### Structure Guidelines

- **Do NOT** structure it as a "list of papers"
- **DO** structure it to address relevant aspects of your problem and methods
- For each aspect, highlight how the current work is different/better/takes a different angle
- This is the real goal: distinguishing your work from earlier work

---

## References

- Use a bib file -- it's good practice and makes things look nice
- For NLP related papers, use the ACL Anthology: https://www.aclweb.org/anthology/anthology.bib.gz

---

## Conclusion

- Summarize results
- Mention the key lessons
