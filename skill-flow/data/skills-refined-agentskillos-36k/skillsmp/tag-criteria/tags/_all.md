# Tag Definitions

> **Note**: Users can customize Target and Criteria in any language to match their notes.

## Papers & Research

### #papers
- **Target**: Academic and research papers
- **Criteria**:
  - Title contains paper-like notation ("論文", "Paper", research title format)
  - Includes author list, abstract, citations
  - Contains identifiers (arXiv ID, DOI, conference name)

### #arxiv
- **Target**: Papers from arXiv.org
- **Criteria**:
  - arXiv ID is explicitly stated (e.g., 2301.12345v1)
  - Contains reference to arXiv URL
  - Indicated as preprint

### #hf-trending
- **Target**: Hugging Face Trending Papers
- **Criteria**:
  - Explicitly noted as from Hugging Face Daily Papers
  - Contains trend ranking information
  - Contains reference to HuggingFace URL

### #3d-reconstruction
- **Target**: 3D reconstruction topics
- **Criteria**:
  - Keywords: 3D再構成, 3次元復元, NeRF, Gaussian Splatting
  - Content about depth estimation, point cloud processing, mesh generation
  - Multi-view image to 3D generation methods

## Project & Specification

### #project-spec
- **Target**: Project specifications
- **Criteria**:
  - Title contains: "仕様書", "設計書", "要件定義", "Specification", "Design Doc"
  - Describes functional/non-functional requirements, system architecture
  - Contains project overview, scope definition

### #claude-code
- **Target**: Claude Code related
- **Criteria**:
  - Claude Code CLI usage, configuration, extensions
  - Claude Code plugin, command, skill development
  - Claude Code workflows, best practices

## Tools

### #ai-tools
- **Target**: AI tools in general
- **Criteria**:
  - AI/ML models, APIs, frameworks
  - AI assistants, generative AI tool usage
  - Machine learning pipelines, inference engines
- **Exclusions**: Do not apply if `#3d-reconstruction` is more appropriate (e.g., NeRF, Gaussian Splatting papers focus on 3D reconstruction, not AI tools themselves)

### #dev-tools
- **Target**: Developer tools
- **Criteria**:
  - IDE, editor, debugger configuration/usage
  - Build tools, CI/CD, test frameworks
  - Code quality tools, linters, formatters

### #gitingest
- **Target**: gitingest related
- **Criteria**:
  - gitingest tool name is explicitly mentioned
  - Repository document extraction/conversion

### #gittodoc
- **Target**: Gittodoc related
- **Criteria**:
  - Gittodoc/GitToDoc tool name is explicitly mentioned
  - Document generation from Git repository

### #productivity
- **Target**: Productivity tools
- **Criteria**:
  - Workflow automation, task management tools
  - Time management, efficiency techniques
  - Note-taking, PKM (Personal Knowledge Management)

### #obsidian
- **Target**: Obsidian related
- **Criteria**:
  - Obsidian application usage, configuration
  - Obsidian plugins, themes, templates
  - Obsidian vault management, links, tag operations

## Security

### #token
- **Target**: Token and authentication related
- **Criteria**:
  - API token, access token management
  - JWT, OAuth token explanation
  - Token-based authentication setup

### #password
- **Target**: Password and credential related
- **Criteria**:
  - Password management, security policies
  - Credential storage, encryption
  - Secret management, Vault products
