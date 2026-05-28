# Financing Presentation Guide

## Overview

This guide provides comprehensive instructions for creating professional financing presentations using the financing-presentation skill. It covers best practices, content requirements, and tips for creating compelling investment pitch decks.

## Presentation Structure

The financing presentation consists of 12 slides, each serving a specific purpose:

### 1. Cover Slide
- **Purpose**: Make a strong first impression
- **Content**: Project name, one-line slogan, founder name and contact information
- **Tips**: Use a clean, professional design with your brand colors

### 2. Problem & Opportunity
- **Purpose**: Clearly articulate the market need
- **Content**: 
  - Market pain points
  - Data supporting the problem
  - Timing factors (why now?)
- **Tips**: Use statistics and real-world examples to validate the problem

### 3. Solution
- **Purpose**: Present your product/service as the answer
- **Content**:
  - How your solution addresses the problem
  - Technical innovations
  - Competitive advantages
- **Tips**: Focus on unique value propositions and differentiators

### 4. Product Demo
- **Purpose**: Show, don't just tell
- **Content**:
  - Screenshots or mockups
  - Key features and benefits
  - User experience highlights
- **Tips**: Use high-quality visuals and keep descriptions concise

### 5. Market Size
- **Purpose**: Demonstrate market potential
- **Content**:
  - TAM (Total Addressable Market)
  - SAM (Serviceable Addressable Market)
  - SOM (Serviceable Obtainable Market)
- **Tips**: Use credible sources and show your methodology

### 6. Competition
- **Purpose**: Position your solution in the market
- **Content**:
  - Key competitors
  - Competitive matrix
  - Your unique positioning
- **Tips**: Be honest about competitors but highlight your advantages

### 7. Business Model
- **Purpose**: Explain how you make money
- **Content**:
  - Revenue streams
  - Pricing strategy
  - Customer acquisition approach
- **Tips**: Show clear unit economics and scalability

### 8. Traction & Milestones
- **Purpose**: Prove market validation
- **Content**:
  - Key metrics and achievements
  - Customer testimonials
  - Milestone timeline
- **Tips**: Use charts and graphs to visualize growth

### 9. Team
- **Purpose**: Build confidence in your leadership
- **Content**:
  - Founder profiles
  - Key team members
  - Advisors and board members
- **Tips**: Highlight relevant experience and past successes

### 10. Financial Projections
- **Purpose**: Show financial potential
- **Content**:
  - Revenue projections (3-5 years)
  - Key financial metrics
  - Growth assumptions
- **Tips**: Be realistic but optimistic; explain your assumptions

### 11. Funding Needs
- **Purpose**: Clearly state what you need
- **Content**:
  - Amount requested
  - Use of funds breakdown
  - Expected runway
- **Tips**: Be specific about how funds will drive growth

### 12. Investment Highlights
- **Purpose**: Summarize key selling points
- **Content**:
  - Top 5-7 investment reasons
  - Call to action
  - Contact information
- **Tips**: Make it memorable and actionable

## Best Practices

### Content Quality
- **Be concise**: Each slide should have 3-5 key points
- **Use data**: Support claims with statistics and research
- **Tell a story**: Create a narrative flow throughout the presentation
- **Focus on value**: Emphasize benefits, not just features

### Design Principles
- **Keep it simple**: Use clean layouts and minimal text
- **Be consistent**: Maintain consistent fonts, colors, and formatting
- **Use visuals**: Incorporate charts, graphs, and images
- **Ensure readability**: Use high contrast and appropriate font sizes

### Presentation Tips
- **Practice**: Rehearse your presentation multiple times
- **Know your audience**: Tailor content to investor interests
- **Anticipate questions**: Prepare for common investor questions
- **Be authentic**: Show passion and expertise

## Common Mistakes to Avoid

### Content Errors
- ❌ Overloading slides with too much text
- ❌ Making unsubstantiated claims
- ❌ Ignoring competitors or underestimating them
- ❌ Using unrealistic financial projections

### Design Mistakes
- ❌ Inconsistent formatting across slides
- ❌ Poor quality images or graphics
- ❌ Hard-to-read fonts or color combinations
- ❌ Cluttered layouts

### Presentation Pitfalls
- ❌ Reading directly from slides
- ❌ Going over time limits
- ❌ Failing to answer questions clearly
- ❌ Lacking confidence or enthusiasm

## Data Collection Checklist

Before generating your presentation, ensure you have:

### Basic Information
- [ ] Project name
- [ ] One-line slogan
- [ ] Founder name and contact details

### Market Information
- [ ] Market size data (TAM, SAM, SOM)
- [ ] Competitor analysis
- [ ] Industry trends and statistics

### Product Information
- [ ] Product screenshots or mockups
- [ ] Feature descriptions
- [ ] Technical specifications

### Business Information
- [ ] Revenue model details
- [ ] Pricing strategy
- [ ] Customer acquisition costs

### Financial Information
- [ ] Historical financial data (if available)
- [ ] Revenue projections
- [ ] Key financial metrics

### Team Information
- [ ] Team member bios
- [ ] Relevant experience
- [ ] Advisor information

## Resources

### Templates
- Use the provided HTML template as a starting point
- Customize colors and fonts to match your brand
- Maintain consistent slide layouts

### Tools
- **Data Visualization**: Use tools like Chart.js or D3.js for charts
- **Image Editing**: Use tools like Canva or Figma for graphics
- **Presentation Software**: PowerPoint, Keynote, or Google Slides

### References
- [Pitch Deck Examples](https://www.pitchdeckexamples.com/)
- [Sequoia Capital Pitch Deck Template](https://www.sequoiacap.com/article/writing-a-business-plan/)
- [Y Combinator Startup School](https://www.startupschool.org/)

## Technical Notes

### HTML Template Structure
The HTML template uses:
- Semantic HTML5 elements
- CSS Grid for layout
- Responsive design principles
- Embedded JavaScript for interactivity

### Data Format
Input data should be in JSON format with the following structure:
```json
{
  "project_name": "Your Project Name",
  "slogan": "Your one-line slogan",
  "founder": {
    "name": "Founder Name",
    "email": "email@example.com",
    "phone": "+1-234-567-8900"
  },
  "slides": {
    "problem": {
      "title": "Problem & Opportunity",
      "points": ["Point 1", "Point 2", "Point 3"]
    },
    ...
  }
}
```

### Generation Script
The `generate_presentation.py` script:
- Reads JSON data from input file
- Validates data structure
- Generates HTML presentation
- Saves output to specified file

## Support

For questions or issues:
1. Check the SKILL.md file for detailed workflow instructions
2. Review the example_data.json for data format reference
3. Examine the financing_template.html for structure reference

## Version History

- v1.0 - Initial release with 12-slide structure
- Future versions may include additional slide templates and customization options
