---
name: presentation_management
description: PowerPoint (.pptx) の自動生成・編集、および Google Slides との連携（設計・構成案作成）を行う
---

# Presentation Management

Supports the creation of slide proposals, automated generation of PowerPoint files via programming, and editing of existing materials.

## 1. Creation of Proposals and Storyboards (Design Phase)
*   Instead of creating files immediately, first create the structure for each slide (title, key message, diagram proposal, speaker notes) in Markdown and perform `collaborative_design` with the user.

## 2. Automated Generation and Editing of PowerPoint (.pptx)
*   Use the `python-pptx` library to automate the following:
    *   Application of master templates
    *   Dynamic addition of slides
    *   Placement of text, images, charts (via matplotlib integration), and shapes
*   Existing files can also be opened to perform text replacement or data updates at specific locations.

## 3. Integration with Google Slides
*   **Note**: Since direct API integration requires service accounts or OAuth authentication, the following workflow is typically recommended:
    *   **Via pptx**: Provide a locally generated .pptx to the user and have them open it in Google Slides.
    *   **Apps Script Proposal**: Generate Google Apps Script (GAS) code and have the user execute it in their environment.

## Design Best Practices
*   **1 Slide, 1 Message**: Designed layouts that are visually communicative without overcrowding them with information.
*   **Advantages of Automation**: Particularly effective for "data-driven presentation creation," such as generating summary charts from tens of thousands of rows of data and embedding them into slides.
