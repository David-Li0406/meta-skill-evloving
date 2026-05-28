---
name: librarian
description: Provides expertise in bibliographic data, book classification, citation formats, reading history management, and library science principles for organising and managing book collections.
---

# Librarian Skill

This skill enables the agent to act as a professional librarian, providing expertise in bibliographic data management, book classification, citation standards, and reading history organisation.

## Core Book Metadata

### Essential Bibliographic Fields

Books require comprehensive metadata for proper cataloguing and retrieval:

#### Identification
- **ISBN-13**: International Standard Book Number (13-digit format). Primary unique identifier for modern books. Must pass checksum validation.
- **ISBN-10**: Older format (10-digit), can be converted to ISBN-13.
- **ID**: Internal system identifier for database relationships.

#### Core Descriptive Fields
- **Title**: Full title of the book, including subtitles. Should preserve original capitalisation and punctuation.
- **Author**: Author name(s) in standard format (typically "Last, First" or "First Last" depending on display preference).
- **Publisher**: Name of the publishing house or organisation.
- **Publication Year**: Year of publication (4-digit format). Critical for historical context and edition identification.
- **Series**: If the book is part of a series (e.g., "Harry Potter, Book 3").

#### Classification and Subject
- **Dewey Decimal Classification (DDC)**: Numeric classification system (e.g., 813.54 for American fiction). Enables subject-based organisation.
- **Subject Headings**: Controlled vocabulary terms describing the book's topics.
- **Genre**: Broad categorisation (fiction, non-fiction, biography, etc.).

#### Additional Metadata
- **Description**: Summary or abstract of the book's content.
- **Thumbnail URL**: Link to cover image for visual identification.
- **Page Count**: Number of pages (useful for reading time estimation).
- **Language**: Primary language of the text.
- **Edition**: Edition number or description (1st, 2nd, revised, etc.).

#### System Fields
- **Created At**: Timestamp when the book record was added to the system.

## Reading History and Tracking

### Reading Record Fields

Reading records track an individual's interaction with books:

#### Status Tracking
- **Status**: Current reading state:
  - `to_read`: Bookmarked for future reading
  - `reading`: Currently being read
  - `completed`: Finished reading
  - `abandoned`: Started but did not finish
  - `on_hold`: Temporarily paused

#### Temporal Data
- **Start Date**: When reading began (ISO 8601 format: YYYY-MM-DD).
- **End Date**: When reading was completed or abandoned.
- **Created At**: Timestamp when the reading record was created.

#### Evaluation
- **Rating**: Numeric rating (typically 1-5 stars or 1-10 scale) representing the reader's assessment.
- **Review**: Textual review or notes about the reading experience.

### Reading History Best Practices

1. **Chronological Accuracy**: Maintain accurate dates for reading patterns and statistics.
2. **Status Transitions**: Track status changes over time (e.g., reading → completed).
3. **Multiple Readings**: Support multiple reading records for the same book (re-reads).
4. **Partial Progress**: For digital books, track reading progress (percentage or page number).

## Book Classification Systems

### Dewey Decimal Classification (DDC)

The DDC organises books by subject using a decimal numbering system:

- **000-099**: Computer science, information, general works
- **100-199**: Philosophy and psychology
- **200-299**: Religion
- **300-399**: Social sciences
- **400-499**: Language
- **500-599**: Science
- **600-699**: Technology
- **700-799**: Arts and recreation
- **800-899**: Literature
- **900-999**: History and geography

**Format**: Three-digit base with decimal subdivisions (e.g., 813.54 for American fiction, 500.2 for general science).

### Library of Congress Classification (LCC)

Alternative classification system using alphanumeric codes:
- **A**: General works
- **B**: Philosophy, psychology, religion
- **C**: Auxiliary sciences of history
- **D**: World history
- **E-F**: American history
- **G**: Geography, anthropology, recreation
- **H**: Social sciences
- **J**: Political science
- **K**: Law
- **L**: Education
- **M**: Music
- **N**: Fine arts
- **P**: Language and literature
- **Q**: Science
- **R**: Medicine
- **S**: Agriculture
- **T**: Technology
- **U**: Military science
- **V**: Naval science
- **Z**: Bibliography, library science

### Genre Classification

Broad categorisation for user-friendly browsing:
- **Fiction**: Novels, short stories, poetry, drama
- **Non-Fiction**: Biography, history, science, self-help, reference
- **Academic**: Textbooks, scholarly works, research
- **Children's**: Picture books, young adult, children's literature

## Book Citation Formats

### Modern Language Association (MLA) Style

**Book Format**:
```
Author Last, First. Title of Book. Publisher, Publication Year.
```

**Example**:
```
Austen, Jane. Pride and Prejudice. Penguin Classics, 2003.
```

**With Edition**:
```
Author Last, First. Title of Book. Xth ed., Publisher, Publication Year.
```

### American Psychological Association (APA) Style

**Book Format**:
```
Author Last, F. M. (Year). Title of book. Publisher.
```

**Example**:
```
Austen, J. (2003). Pride and prejudice. Penguin Classics.
```

### Chicago Manual of Style

**Book Format**:
```
Author Last, First. Title of Book. Place: Publisher, Year.
```

**Example**:
```
Austen, Jane. Pride and Prejudice. London: Penguin Classics, 2003.
```

### Citation Components

Essential elements for any citation:
1. **Author**: Full name(s) as they appear on the title page
2. **Title**: Complete title including subtitle
3. **Publisher**: Name of publishing house
4. **Publication Year**: Year of publication
5. **Edition**: If not the first edition
6. **ISBN**: For digital or modern references

## Sorting and Organisation

### Primary Sort Methods

#### Alphabetical by Author
- Sort by author's last name, then first name
- Handle multiple authors: use first author for primary sort
- Ignore articles ("The", "A", "An") at the beginning of titles when sorting by title

#### Alphabetical by Title
- Ignore leading articles ("The", "A", "An")
- Sort word-by-word (not letter-by-letter)
- Preserve original capitalisation in display

#### Chronological
- Sort by publication year (oldest to newest, or newest to oldest)
- Useful for tracking reading trends over time
- Combine with author sort for author's works in chronological order

#### By Classification
- Sort by Dewey Decimal or Library of Congress classification
- Groups books by subject matter
- Enables browsing by topic

#### By Date Added
- Sort by `created_at` timestamp
- Shows most recently added books first
- Useful for tracking collection growth

### Secondary Sort Criteria

When primary sort values are equal:
1. **Author → Title**: Sort by title within the same author
2. **Title → Author**: Sort by author when titles are identical (different editions)
3. **Year → Title**: Sort by title when publication years match

### Reading Status Organisation

Group books by reading status for personal library management:
- **To Read**: Future reading queue
- **Currently Reading**: Active reading list
- **Completed**: Finished books (may be sorted by completion date)
- **Abandoned**: Books not finished
- **On Hold**: Temporarily paused

## Data Quality and Validation

### ISBN Validation

- **ISBN-13 Format**: Exactly 13 digits
- **Checksum Validation**: Must pass the ISBN-13 checksum algorithm
- **Normalisation**: Remove hyphens and spaces before validation
- **Handling Missing ISBNs**: Some older books or special editions may lack ISBNs

### Date Validation

- **Publication Year**: Should be a 4-digit year (1000-9999)
- **Reading Dates**: ISO 8601 format (YYYY-MM-DD)
- **Logical Consistency**: End date should not precede start date
- **Future Dates**: Publication year should not be in the future (with exceptions for pre-orders)

### Required vs. Optional Fields

**Required for Basic Cataloguing**:
- Title
- Author (or "Unknown" if anonymous)
- ISBN-13 (preferred) or ISBN-10

**Highly Recommended**:
- Publication Year
- Publisher
- Thumbnail URL (for visual identification)

**Optional but Valuable**:
- Description
- Series information
- Dewey Decimal Classification
- Page count
- Language
- Edition

## Search and Discovery

### Searchable Fields

Prioritise search relevance by field importance:
1. **Title** (highest weight): Primary identifier users remember
2. **Author** (high weight): Common search criterion
3. **ISBN** (high weight): Exact match for known books
4. **Series** (medium weight): Find books in a series
5. **Publisher** (medium weight): Find books from specific publishers
6. **Description** (low weight): Full-text search in summaries
7. **Dewey Decimal** (medium weight): Subject-based discovery

### Search Strategies

- **Fuzzy Matching**: Handle typos and variations in spelling
- **Partial Matching**: Match substrings within titles and author names
- **Case Insensitivity**: Ignore case differences
- **Normalisation**: Handle accented characters, special punctuation
- **Multi-field Search**: Search across multiple fields simultaneously

## Collection Management Principles

### Deduplication

- **Primary Key**: ISBN-13 is the best unique identifier
- **Fuzzy Matching**: Detect near-duplicates (same book, different ISBN formats)
- **Edition Handling**: Different editions may have different ISBNs but represent the same work

### Metadata Enrichment

- **External APIs**: Use services like Open Library, Google Books API for metadata
- **Bulk Operations**: Support batch updates for missing fields (covers, descriptions)
- **Data Preservation**: Never overwrite user-provided data with external data
- **Incremental Updates**: Only populate missing fields, preserve existing data

### Collection Statistics

Track meaningful metrics:
- **Total Books**: Count of unique books in collection
- **Reading Status Distribution**: Count by status (to_read, reading, completed, etc.)
- **Publication Year Range**: Oldest and newest books
- **Author Diversity**: Number of unique authors
- **Completion Rate**: Percentage of books completed vs. total
- **Average Rating**: Mean rating across completed books

## Integration with Book Lamp

When working with Book Lamp's data model:

### Book Schema
- Fields: `id`, `isbn13`, `title`, `author`, `publication_year`, `thumbnail_url`, `created_at`, `publisher`, `description`, `series`, `dewey_decimal`
- **Primary Identifier**: `isbn13`
- **Display Fields**: `title`, `author`, `thumbnail_url`
- **Classification**: `dewey_decimal` for subject organisation

### Reading Record Schema
- Fields: `id`, `book_id`, `status`, `start_date`, `end_date`, `rating`, `created_at`
- **Relationship**: `book_id` links to book record
- **Status Values**: `to_read`, `reading`, `completed`, `abandoned`, `on_hold`
- **Temporal Tracking**: `start_date`, `end_date` for reading timeline

### Best Practices for Book Lamp
- **British English**: Use British spelling in UI text (e.g., "Organise", "Colour")
- **Data Sanitisation**: Always strip and normalise user input (ISBNs, titles)
- **Field Length Limits**: Respect system constraints (title: 300 chars, author: 200 chars)
- **Date Handling**: Use ISO 8601 format for dates, extract years from various date formats
- **Missing Data**: Gracefully handle missing optional fields (thumbnails, descriptions, classifications)

## Resources and Standards

- **ISBN Standards**: ISO 2108, administered by the International ISBN Agency
- **Dewey Decimal Classification**: OCLC's DDC system
- **Library of Congress**: LCC classification system
- **Citation Styles**: MLA Handbook, APA Publication Manual, Chicago Manual of Style
- **MARC Standards**: Machine-Readable Cataloguing format for library data exchange
- **FRBR**: Functional Requirements for Bibliographic Records model
