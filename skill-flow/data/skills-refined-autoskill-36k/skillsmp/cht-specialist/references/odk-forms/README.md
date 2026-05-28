# ODK XLSForm Documentation

Complete reference for creating ODK forms using the XLSForm standard.

## Documentation Files

| File | Description |
|------|-------------|
| [01-structure.md](01-structure.md) | XLSForm structure: survey, choices, settings sheets |
| [02-question-types.md](02-question-types.md) | All question types with appearances |
| [03-form-logic.md](03-form-logic.md) | Relevance, constraints, calculations, defaults |
| [04-functions.md](04-functions.md) | XPath operators and functions reference |
| [05-groups-repeats.md](05-groups-repeats.md) | Grouping questions and repeat structures |
| [06-external-data.md](06-external-data.md) | CSV files, cascading selects, lookups |
| [07-multilanguage.md](07-multilanguage.md) | Translation and multi-language support |
| [08-styling.md](08-styling.md) | Markdown, HTML, media, visual customization |
| [09-entities.md](09-entities.md) | Longitudinal data and workflow patterns |
| [10-audit-logging.md](10-audit-logging.md) | Tracking enumerator behavior |
| [11-encryption.md](11-encryption.md) | Form encryption setup |
| [12-cht-extensions.md](12-cht-extensions.md) | CHT-specific functions and widgets |
| [13-quick-reference.md](13-quick-reference.md) | Common patterns and cheat sheet |

## Overview

XLSForm is a standard for designing forms in Excel or Google Sheets that convert to ODK XForm format.

**Workflow:**
1. Create form in Excel/Google Sheets using XLSForm syntax
2. Convert to XForm (using pyxform, XLSForm Online, or cht-conf)
3. Upload to ODK Central
4. Deploy to ODK Collect
5. Collect data and submit to server

## Resources

- [ODK Documentation](https://docs.getodk.org/)
- [XLSForm Reference](https://xlsform.org/)
- [XLSForm Online Converter](https://getodk.org/xlsform/)
- [ODK Forum](https://forum.getodk.org/)
- [CHT Documentation](https://docs.communityhealthtoolkit.org/)
