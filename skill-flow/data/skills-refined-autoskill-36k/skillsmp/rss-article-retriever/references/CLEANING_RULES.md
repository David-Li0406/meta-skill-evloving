# Content Cleaning Rules

This document defines the rules for cleaning WeChat article content extracted via Playwright.

## Overview

WeChat articles contain various non-content elements that must be removed for clean output:
- Author profiles and promotional sections
- QR codes and subscription prompts
- Share buttons and toolbars
- Advertisement areas
- Image captions that are ads

## Elements to Remove

### 1. Author/Profile Elements

| Element | Selector | Notes |
|---------|----------|-------|
| Profile QR Code | `#js_profile_qrcode` | Author profile with QR |
| Profile Container | `.profile_container` | Wrapper for author info |
| Profile Inner | `.profile_inner` | Inner author block |
| Rich Media Meta | `.rich_media_meta_list` | Meta info bar |

### 2. QR Codes

| Element | Selector | Notes |
|---------|----------|-------|
| PC QR Code | `#js_pc_qr_code` | Desktop QR code |
| QR Code PC | `.qr_code_pc` | Alternative class |
| Any QR Image | `img[src*="qrcode"]` | Images containing "qrcode" in URL |

### 3. Share/Tool Elements

| Element | Selector | Notes |
|---------|----------|-------|
| Tool Bar | `.rich_media_tool` | Share/like buttons |
| Share Area | `.rich_media_area_primary` | Primary share section |
| Like Button | `#js_like_btn` | Like button element |

### 4. Advertisement Areas

| Element | Selector | Notes |
|---------|----------|-------|
| Sponsor Ad | `#js_sponsor_ad_area` | Sponsored ad section |
| Ad Container | `.ad_container` | Generic ad wrapper |
| Banner Ads | `[data-pluginname="adimage"]` | Plugin-based ads |

### 5. Subscription Prompts

| Element | Selector | Notes |
|---------|----------|-------|
| Profile Article | `#js_profile_article` | "More articles" section |
| Subscribe Box | `.subscribe_box` | Subscription prompt |
| Recommend Area | `#js_tags` | Recommended tags |

### 6. Other Non-Content

| Element | Selector | Notes |
|---------|----------|-------|
| Copyright | `.rich_media_copyright` | Copyright notice |
| Original Tag | `#js_tags` | Original content tag |
| Bottom Area | `.rich_media_area_extra` | Extra bottom content |

## Elements to Preserve

### 1. Main Content

| Element | Selector | Priority |
|---------|----------|----------|
| Content Area | `#js_content` | Primary content container |
| Paragraphs | `p` | Text paragraphs |
| Sections | `section` | Content sections |

### 2. Headings

| Element | Selector | Notes |
|---------|----------|-------|
| Strong | `strong` | Bold text (often headings) |
| Bold | `b` | Bold text |
| H1-H6 | `h1`, `h2`, `h3`, `h4`, `h5`, `h6` | Standard headings |

### 3. Lists

| Element | Selector | Notes |
|---------|----------|-------|
| Unordered | `ul` | Bullet lists |
| Ordered | `ol` | Numbered lists |
| List Items | `li` | Individual items |

### 4. Meaningful Images

Keep images that are part of the content (diagrams, screenshots, etc.) but remove:
- Decorative images
- QR codes
- Author avatars

## Text Cleaning Rules

### 1. Whitespace Normalization

```
- Replace multiple spaces with single space
- Replace multiple newlines with double newline (paragraph break)
- Trim leading/trailing whitespace from each line
- Remove empty paragraphs
```

### 2. Remove Common Junk Patterns

| Pattern | Description |
|---------|-------------|
| `点击上方蓝字关注` | Subscription prompt |
| `长按识别二维码` | QR code instruction |
| `点击"在看"` | "Watching" prompt |
| `转发到朋友圈` | Share prompt |
| `点击阅读原文` | "Read original" link |
| `图片来源于网络` | Image credit boilerplate |
| `如有侵权请联系删除` | Copyright disclaimer |
| `编辑：xxx` | Editor credit |
| `作者：xxx` at end | Author credit at article end |
| `来源：xxx` at end | Source credit at article end |

### 3. Preserve Important Text

| Pattern | Keep? | Notes |
|---------|-------|-------|
| Case numbers (如：(2023)京01民初123号) | Yes | Legal case identifiers |
| Dates in content | Yes | Relevant to article |
| Money amounts | Yes | Relevant to legal cases |
| Names in case descriptions | Yes | Parties involved |

## Section Recognition

### Legal Article Headings

These headings commonly indicate article structure in legal content:

| Heading | Meaning |
|---------|---------|
| 案情简介 | Case summary |
| 案件经过 | Case progression |
| 法院审理 | Court proceedings |
| 法院认为 | Court opinion |
| 法院判决 | Court ruling |
| 判决结果 | Verdict |
| 法官说法 | Judge's commentary |
| 法官提醒 | Judge's reminder |
| 律师分析 | Lawyer's analysis |
| 律师建议 | Lawyer's advice |
| 典型意义 | Typical significance |
| 相关法条 | Related laws |

### Section Detection Algorithm

```
1. Find all <strong>, <b>, or heading tags
2. Check if text matches known section headings
3. Extract text until next section heading
4. Create section object: { heading, text }
```

## Cleaning Implementation

### Step-by-Step Process

1. **Get raw HTML** from `#js_content`

2. **Remove unwanted elements** by selector:
   ```javascript
   const selectorsToRemove = [
     '#js_profile_qrcode',
     '.profile_container',
     '#js_pc_qr_code',
     '.qr_code_pc',
     '.rich_media_tool',
     '#js_sponsor_ad_area',
     '#js_profile_article',
     // ... other selectors
   ];
   ```

3. **Extract text** from remaining elements:
   ```javascript
   - Get innerText or textContent
   - Preserve paragraph breaks
   - Normalize whitespace
   ```

4. **Apply text cleaning patterns**:
   ```javascript
   - Remove subscription prompts
   - Remove share prompts
   - Remove trailing credits
   ```

5. **Identify sections**:
   ```javascript
   - Find section headings
   - Group content by sections
   - Create sections array
   ```

6. **Generate output**:
   ```javascript
   {
     plain_text: "Cleaned full text",
     sections: [{ heading, text }, ...],
     source: "playwright"
   }
   ```

## Quality Checks

After cleaning, verify:

1. **Content length** - Should be substantial (>100 chars for real articles)
2. **No junk patterns** - Run pattern matching to confirm removal
3. **Section integrity** - Each section should have meaningful content
4. **No orphaned elements** - No standalone QR instructions, etc.

## Fallback Behavior

If cleaning results in empty or near-empty content:

1. Log the issue in `cleaning_notes`
2. Fall back to RSS summary if available
3. Set `source` to `"rss_fallback"`
4. Include note: "Content extraction failed - using RSS summary"
