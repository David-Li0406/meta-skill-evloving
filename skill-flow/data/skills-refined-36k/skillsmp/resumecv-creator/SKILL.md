---
name: Resume/CV Creator
slug: resume-cv-creator
description: Build professional resumes and CVs with formatting, templates, and ATS optimization
category: document-creation
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create resume"
  - "build cv"
  - "generate resume"
  - "make curriculum vitae"
  - "update resume"
tags:
  - resume
  - cv
  - career
  - job-search
  - ats
---

# Resume/CV Creator

The Resume/CV Creator skill automates the creation of professional resumes and curriculum vitae with multiple templates, formatting options, and ATS (Applicant Tracking System) optimization. It handles standard resume formats, academic CVs, creative portfolios, and international variations. The skill ensures proper structure, formatting, and keyword optimization for job applications.

Generate resumes in multiple formats (PDF, DOCX, HTML), customize for specific job applications, and maintain multiple versions for different industries or roles.

## Core Workflows

### Workflow 1: Generate Professional Resume
**Purpose:** Create a standard professional resume with clean formatting

**Steps:**
1. Collect candidate information (personal, education, experience, skills)
2. Choose resume template and style
3. Format contact information and header
4. Add professional summary or objective
5. List work experience in reverse chronological order
6. Include education and certifications
7. Add skills section with relevant keywords
8. Format for readability and ATS compatibility
9. Export to PDF and DOCX

**Implementation:**
```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TabStopType, TabStopPosition } = require('docx');
const fs = require('fs');

async function generateResume(resumeData, outputPath) {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        // Header - Name
        new Paragraph({
          text: resumeData.personalInfo.name,
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 }
        }),

        // Contact Info
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun(`${resumeData.personalInfo.email} | `),
            new TextRun(`${resumeData.personalInfo.phone} | `),
            new TextRun(`${resumeData.personalInfo.location} | `),
            new TextRun({
              text: resumeData.personalInfo.linkedin,
              style: 'Hyperlink'
            })
          ],
          spacing: { after: 300 }
        }),

        // Professional Summary
        new Paragraph({
          text: 'PROFESSIONAL SUMMARY',
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 200, after: 100 }
        }),
        new Paragraph({
          text: resumeData.summary,
          spacing: { after: 300 }
        }),

        // Work Experience
        new Paragraph({
          text: 'WORK EXPERIENCE',
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 200, after: 100 }
        }),

        ...resumeData.experience.flatMap(job => [
          new Paragraph({
            children: [
              new TextRun({
                text: job.title,
                bold: true,
                size: 24
              }),
              new TextRun({
                text: ` | ${job.company}`,
                size: 24
              })
            ],
            spacing: { before: 150 }
          }),
          new Paragraph({
            children: [
              new TextRun({
                text: `${job.location} | ${job.startDate} - ${job.endDate}`,
                italics: true,
                size: 20
              })
            ],
            spacing: { after: 100 }
          }),
          ...job.achievements.map(achievement =>
            new Paragraph({
              text: achievement,
              bullet: {
                level: 0
              },
              spacing: { after: 50 }
            })
          )
        ]),

        // Education
        new Paragraph({
          text: 'EDUCATION',
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300, after: 100 }
        }),

        ...resumeData.education.map(edu => [
          new Paragraph({
            children: [
              new TextRun({
                text: edu.degree,
                bold: true
              }),
              new TextRun(` | ${edu.institution}`)
            ]
          }),
          new Paragraph({
            text: `${edu.location} | Graduated ${edu.graduationDate}`,
            italics: true,
            spacing: { after: 100 }
          }),
          ...(edu.achievements ? [
            new Paragraph({
              text: edu.achievements,
              spacing: { after: 150 }
            })
          ] : [])
        ]).flat(),

        // Skills
        new Paragraph({
          text: 'SKILLS',
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300, after: 100 }
        }),

        ...Object.entries(groupSkills(resumeData.skills)).map(([category, skills]) =>
          new Paragraph({
            children: [
              new TextRun({
                text: `${category}: `,
                bold: true
              }),
              new TextRun(skills.join(', '))
            ],
            spacing: { after: 100 }
          })
        ),

        // Certifications (if any)
        ...(resumeData.certifications && resumeData.certifications.length > 0 ? [
          new Paragraph({
            text: 'CERTIFICATIONS',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 300, after: 100 }
          }),
          ...resumeData.certifications.map(cert =>
            new Paragraph({
              text: `${cert.name} - ${cert.issuer} (${cert.date})`,
              bullet: { level: 0 },
              spacing: { after: 50 }
            })
          )
        ] : [])
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  return outputPath;
}

function groupSkills(skills) {
  const grouped = {};

  skills.forEach(skill => {
    const category = skill.category || 'General';
    if (!grouped[category]) {
      grouped[category] = [];
    }
    grouped[category].push(skill.name);
  });

  return grouped;
}
```

### Workflow 2: Tailor Resume for Job Application
**Purpose:** Customize resume to match specific job description and requirements

**Steps:**
1. Parse job description for keywords
2. Identify required skills and qualifications
3. Extract candidate's relevant experience
4. Reorder sections to highlight matching qualifications
5. Add keywords naturally throughout resume
6. Adjust professional summary to match role
7. Emphasize achievements relevant to position
8. Optimize for ATS scanning

**Implementation:**
```javascript
const natural = require('natural');
const TfIdf = natural.TfIdf;

function tailorResumeForJob(resumeData, jobDescription) {
  // Extract keywords from job description
  const keywords = extractKeywords(jobDescription);

  // Score candidate's experience against job requirements
  const scoredExperience = scoreExperience(resumeData.experience, keywords);

  // Rewrite professional summary
  const tailoredSummary = generateTailoredSummary(resumeData, keywords);

  // Prioritize relevant skills
  const prioritizedSkills = prioritizeSkills(resumeData.skills, keywords);

  // Highlight matching achievements
  const enhancedExperience = enhanceExperience(scoredExperience, keywords);

  return {
    ...resumeData,
    summary: tailoredSummary,
    experience: enhancedExperience,
    skills: prioritizedSkills,
    tailoredFor: {
      jobTitle: extractJobTitle(jobDescription),
      matchScore: calculateMatchScore(resumeData, keywords),
      keywords: keywords.slice(0, 10) // Top 10 keywords
    }
  };
}

function extractKeywords(jobDescription) {
  const tfidf = new TfIdf();
  tfidf.addDocument(jobDescription.toLowerCase());

  const keywords = [];
  tfidf.listTerms(0).forEach(item => {
    if (item.term.length > 3 && !isCommonWord(item.term)) {
      keywords.push({
        term: item.term,
        score: item.tfidf
      });
    }
  });

  return keywords
    .sort((a, b) => b.score - a.score)
    .map(k => k.term);
}

function scoreExperience(experience, keywords) {
  return experience.map(job => {
    const jobText = `${job.title} ${job.company} ${job.achievements.join(' ')}`.toLowerCase();
    const matchCount = keywords.filter(keyword => jobText.includes(keyword)).length;

    return {
      ...job,
      relevanceScore: matchCount,
      matchedKeywords: keywords.filter(keyword => jobText.includes(keyword))
    };
  }).sort((a, b) => b.relevanceScore - a.relevanceScore);
}

function generateTailoredSummary(resumeData, keywords) {
  const yearsExperience = calculateYearsExperience(resumeData.experience);
  const topSkills = resumeData.skills.slice(0, 5).map(s => s.name).join(', ');
  const keywordPhrase = keywords.slice(0, 3).join(', ');

  return `Results-driven professional with ${yearsExperience}+ years of experience in ${keywordPhrase}. Proven expertise in ${topSkills}. Track record of delivering high-impact solutions and driving measurable results.`;
}

function prioritizeSkills(skills, keywords) {
  return skills
    .map(skill => ({
      ...skill,
      relevance: keywords.includes(skill.name.toLowerCase()) ? 1 : 0
    }))
    .sort((a, b) => b.relevance - a.relevance);
}

function calculateMatchScore(resumeData, keywords) {
  const allText = `
    ${resumeData.summary}
    ${resumeData.experience.map(e => e.achievements.join(' ')).join(' ')}
    ${resumeData.skills.map(s => s.name).join(' ')}
  `.toLowerCase();

  const matchedKeywords = keywords.filter(keyword => allText.includes(keyword));
  return Math.round((matchedKeywords.length / keywords.length) * 100);
}
```

### Workflow 3: Academic CV Generator
**Purpose:** Create comprehensive academic curriculum vitae

**Steps:**
1. Collect academic credentials and publications
2. Format in traditional academic CV structure
3. List education (highest to lowest)
4. Detail research experience and projects
5. Include publications with proper citations
6. Add presentations and conferences
7. List teaching experience
8. Include grants, awards, and honors
9. Add professional memberships
10. Format references section

**Implementation:**
```javascript
async function generateAcademicCV(cvData, outputPath) {
  const sections = [
    // Personal Information
    {
      title: cvData.personalInfo.name,
      content: [
        cvData.personalInfo.currentPosition,
        cvData.personalInfo.institution,
        cvData.personalInfo.email,
        cvData.personalInfo.website
      ]
    },

    // Education
    {
      title: 'EDUCATION',
      entries: cvData.education.map(edu => ({
        header: `${edu.degree}, ${edu.field}`,
        subheader: `${edu.institution}, ${edu.location}`,
        date: edu.year,
        details: edu.dissertation ? [`Dissertation: "${edu.dissertation}"`] : []
      }))
    },

    // Research Interests
    {
      title: 'RESEARCH INTERESTS',
      content: cvData.researchInterests
    },

    // Publications
    {
      title: 'PUBLICATIONS',
      subsections: [
        {
          subtitle: 'Peer-Reviewed Articles',
          entries: cvData.publications.articles.map(formatCitation)
        },
        {
          subtitle: 'Book Chapters',
          entries: cvData.publications.chapters.map(formatCitation)
        },
        {
          subtitle: 'Conference Papers',
          entries: cvData.publications.conferences.map(formatCitation)
        }
      ]
    },

    // Presentations
    {
      title: 'PRESENTATIONS',
      entries: cvData.presentations.map(pres =>
        `"${pres.title}" ${pres.conference}, ${pres.location}, ${pres.date}`
      )
    },

    // Teaching Experience
    {
      title: 'TEACHING EXPERIENCE',
      entries: cvData.teaching.map(course => ({
        header: course.courseTitle,
        subheader: `${course.institution}, ${course.department}`,
        date: course.terms.join(', '),
        details: course.responsibilities
      }))
    },

    // Grants and Awards
    {
      title: 'GRANTS AND AWARDS',
      entries: cvData.grants.map(grant =>
        `${grant.title}, ${grant.funder}, ${grant.amount} (${grant.year})`
      )
    },

    // Professional Service
    {
      title: 'PROFESSIONAL SERVICE',
      entries: cvData.service
    },

    // References
    {
      title: 'REFERENCES',
      entries: cvData.references.map(ref =>
        `${ref.name}\n${ref.title}\n${ref.institution}\n${ref.email}`
      )
    }
  ];

  return await generateFormattedCV(sections, outputPath);
}

function formatCitation(publication) {
  const authors = publication.authors.join(', ');
  return `${authors}. (${publication.year}). "${publication.title}." ${publication.journal}, ${publication.volume}(${publication.issue}), ${publication.pages}.`;
}
```

### Workflow 4: ATS Optimization Check
**Purpose:** Analyze and optimize resume for Applicant Tracking Systems

**Steps:**
1. Parse resume content
2. Check for ATS-friendly formatting
3. Identify problematic formatting (tables, headers, columns)
4. Verify keyword presence and density
5. Check file format compatibility
6. Validate section headers are standard
7. Ensure dates are in consistent format
8. Generate optimization report with suggestions

**Implementation:**
```javascript
function analyzeATSCompatibility(resumePath) {
  const resumeText = extractTextFromResume(resumePath);

  const checks = {
    fileFormat: checkFileFormat(resumePath),
    standardSections: checkStandardSections(resumeText),
    keywords: analyzeKeywords(resumeText),
    dates: checkDateFormatting(resumeText),
    contactInfo: validateContactInfo(resumeText),
    formatting: checkFormatting(resumePath),
    length: checkLength(resumeText)
  };

  const score = calculateATSScore(checks);

  return {
    score: score,
    passed: score >= 75,
    checks: checks,
    recommendations: generateRecommendations(checks)
  };
}

function checkStandardSections(text) {
  const standardSections = [
    'experience',
    'education',
    'skills',
    'summary'
  ];

  const found = standardSections.filter(section =>
    new RegExp(section, 'i').test(text)
  );

  return {
    found: found,
    missing: standardSections.filter(s => !found.includes(s)),
    score: (found.length / standardSections.length) * 100
  };
}

function analyzeKeywords(text) {
  const commonIndustryKeywords = [
    'managed', 'led', 'developed', 'created', 'implemented',
    'analyzed', 'designed', 'coordinated', 'improved', 'achieved'
  ];

  const foundKeywords = commonIndustryKeywords.filter(keyword =>
    new RegExp(keyword, 'i').test(text)
  );

  return {
    actionVerbs: foundKeywords.length,
    density: foundKeywords.length / commonIndustryKeywords.length,
    missing: commonIndustryKeywords.filter(k => !foundKeywords.includes(k))
  };
}

function checkFormatting(resumePath) {
  const warnings = [];

  // Check for problematic elements
  if (hasTables(resumePath)) warnings.push('Tables may not parse correctly in ATS');
  if (hasTextBoxes(resumePath)) warnings.push('Text boxes are not ATS-friendly');
  if (hasMultipleColumns(resumePath)) warnings.push('Multiple columns may confuse ATS');
  if (hasHeaders(resumePath)) warnings.push('Headers/footers may be ignored');
  if (hasImages(resumePath)) warnings.push('Images and graphics will be ignored');

  return {
    warnings: warnings,
    score: Math.max(0, 100 - (warnings.length * 20))
  };
}

function generateRecommendations(checks) {
  const recommendations = [];

  if (checks.fileFormat.format !== 'docx' && checks.fileFormat.format !== 'pdf') {
    recommendations.push('Convert to .docx or .pdf format');
  }

  if (checks.standardSections.missing.length > 0) {
    recommendations.push(`Add missing sections: ${checks.standardSections.missing.join(', ')}`);
  }

  if (checks.keywords.density < 0.3) {
    recommendations.push('Increase use of action verbs and industry keywords');
  }

  if (checks.formatting.warnings.length > 0) {
    recommendations.push('Simplify formatting: remove tables, columns, text boxes');
  }

  if (checks.length.pages > 2) {
    recommendations.push('Consider reducing to 1-2 pages for better ATS parsing');
  }

  return recommendations;
}
```

### Workflow 5: Multi-Format Export
**Purpose:** Generate resume in multiple formats (PDF, DOCX, HTML, plain text)

**Steps:**
1. Create master resume data structure
2. Generate DOCX version with formatting
3. Convert to PDF with preserved styling
4. Create HTML version for online applications
5. Generate plain text version for email/paste
6. Ensure consistency across all formats
7. Optimize each format for its use case

**Implementation:**
```javascript
async function exportResumeAllFormats(resumeData, outputDir) {
  const baseName = resumeData.personalInfo.name.replace(/\s+/g, '-').toLowerCase();

  const outputs = {
    docx: `${outputDir}/${baseName}-resume.docx`,
    pdf: `${outputDir}/${baseName}-resume.pdf`,
    html: `${outputDir}/${baseName}-resume.html`,
    txt: `${outputDir}/${baseName}-resume.txt`
  };

  // Generate DOCX
  await generateResume(resumeData, outputs.docx);

  // Convert to PDF
  await convertDocxToPdf(outputs.docx, outputs.pdf);

  // Generate HTML
  await generateHTMLResume(resumeData, outputs.html);

  // Generate plain text
  await generatePlainTextResume(resumeData, outputs.txt);

  return outputs;
}

async function generateHTMLResume(resumeData, outputPath) {
  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${resumeData.personalInfo.name} - Resume</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    h1 { text-align: center; color: #2C3E50; }
    h2 { color: #34495E; border-bottom: 2px solid #3498DB; padding-bottom: 5px; }
    .contact { text-align: center; margin-bottom: 30px; }
    .job { margin-bottom: 20px; }
    .job-title { font-weight: bold; }
    .job-company { font-style: italic; }
    ul { margin-top: 5px; }
  </style>
</head>
<body>
  <h1>${resumeData.personalInfo.name}</h1>
  <div class="contact">
    ${resumeData.personalInfo.email} | ${resumeData.personalInfo.phone} | ${resumeData.personalInfo.location}
  </div>

  <h2>Professional Summary</h2>
  <p>${resumeData.summary}</p>

  <h2>Work Experience</h2>
  ${resumeData.experience.map(job => `
    <div class="job">
      <div class="job-title">${job.title}</div>
      <div class="job-company">${job.company} | ${job.location} | ${job.startDate} - ${job.endDate}</div>
      <ul>
        ${job.achievements.map(achievement => `<li>${achievement}</li>`).join('\n        ')}
      </ul>
    </div>
  `).join('\n  ')}

  <h2>Education</h2>
  ${resumeData.education.map(edu => `
    <div>
      <strong>${edu.degree}</strong> | ${edu.institution} | ${edu.graduationDate}
    </div>
  `).join('\n  ')}

  <h2>Skills</h2>
  <p>${resumeData.skills.map(s => s.name).join(' • ')}</p>
</body>
</html>
  `;

  fs.writeFileSync(outputPath, html, 'utf8');
}

async function generatePlainTextResume(resumeData, outputPath) {
  const text = `
${resumeData.personalInfo.name.toUpperCase()}
${resumeData.personalInfo.email} | ${resumeData.personalInfo.phone} | ${resumeData.personalInfo.location}

PROFESSIONAL SUMMARY
${resumeData.summary}

WORK EXPERIENCE
${resumeData.experience.map(job => `
${job.title} | ${job.company}
${job.location} | ${job.startDate} - ${job.endDate}
${job.achievements.map(a => `  • ${a}`).join('\n')}
`).join('\n')}

EDUCATION
${resumeData.education.map(edu => `${edu.degree} | ${edu.institution} | ${edu.graduationDate}`).join('\n')}

SKILLS
${resumeData.skills.map(s => s.name).join(', ')}
  `.trim();

  fs.writeFileSync(outputPath, text, 'utf8');
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create resume | "build resume for [name]" |
| Tailor for job | "customize resume for [job title]" |
| Academic CV | "create academic CV" |
| ATS check | "analyze resume for ATS" |
| Multi-format export | "export resume in all formats" |
| Update section | "update [experience/education/skills]" |
| Generate cover letter | "create cover letter for [position]" |

## Best Practices

- **One Page:** Keep to one page for early-career; two pages maximum for experienced professionals
- **Action Verbs:** Start bullet points with strong action verbs
- **Quantify:** Include numbers and metrics in achievements
- **Reverse Chronological:** List experience from most recent to oldest
- **Consistency:** Maintain consistent date formats, tense, and formatting
- **Keywords:** Include industry-specific keywords naturally
- **Contact Info:** Include email, phone, LinkedIn, location (city/state)
- **No Personal Info:** Omit photos, age, marital status (US standard)
- **File Naming:** Use professional filename: "FirstName-LastName-Resume.pdf"
- **Proofreading:** Zero typos or grammatical errors
- **White Space:** Use white space effectively for readability
- **ATS-Friendly:** Avoid complex formatting, tables, headers

## Common Patterns

**Entry-Level Resume:**
```javascript
{
  summary: 'Recent graduate with...',
  experience: [2-3 internships/part-time roles],
  education: [Detailed with GPA, honors, coursework],
  projects: [Academic or personal projects],
  skills: [Technical and soft skills]
}
```

**Career Changer:**
```javascript
{
  summary: 'Transitioning from X to Y with transferable skills in...',
  experience: [Reframed to highlight transferable skills],
  skills: [Emphasize relevant skills for new field],
  certifications: [New field certifications]
}
```

## Dependencies

Install required packages:
```bash
npm install docx
npm install pdf-lib
npm install natural       # For keyword extraction
npm install mammoth       # For .docx parsing
```

## Error Handling

- **Missing Data:** Provide default values for optional fields
- **Invalid Dates:** Validate date formats before rendering
- **File Permissions:** Handle read/write errors gracefully
- **Format Conversion:** Ensure fallbacks if PDF conversion fails

## Advanced Features

**LinkedIn Import:**
```javascript
async function importFromLinkedIn(linkedInPDF) {
  // Parse LinkedIn PDF export
  // Extract work history, education, skills
  // Return structured resume data
}
```

**Resume Scoring:**
```javascript
function scoreResume(resumeData) {
  return {
    completeness: checkCompleteness(resumeData),
    keywordOptimization: analyzeKeywords(resumeData),
    formatting: checkFormatting(resumeData),
    impact: measureImpact(resumeData),
    overallScore: calculateOverallScore(resumeData)
  };
}
```