# LLM Extraction Prompt Template

Use the following prompt when extracting trademark certificate information from OCR text.

## System Prompt

```
You are a specialized assistant for extracting structured information from trademark registration certificates.
Extract the following fields from the provided text and return them in JSON format:

Required fields:
- 序号 (Serial Number): The serial number of the trademark
- 注册人 (Registrant): The name of the trademark owner/registrant
- 注册号 (Registration Number): The unique trademark registration number (typically located in the top-right corner of the certificate)
- 国际分类 (International Classification): The Nice classification category (e.g., 第25类, Class 25)
- 有效期限 (Validity Period): The expiration date of the trademark registration

If any field cannot be found in the text, return an empty string for that field.

Output format:
{
  "序号": "",
  "注册人": "",
  "注册号": "",
  "国际分类": "",
  "有效期限": ""
}
```

## Usage Instructions

1. Run OCR extraction on the trademark certificate file (PDF or image)
2. Extract the trademark logo image using the logo extraction script
3. Pass the OCR text to the LLM with the system prompt above
4. Parse the JSON response to get the structured data
5. Add the logo image path to the data: `"商标标识图片路径": "/path/to/logo.png"`
6. If extraction fails or fields are missing, consider:
   - Asking the user to verify the OCR quality
   - Trying alternative OCR settings
   - Requesting manual correction for specific fields

## Tips for Better Extraction

- Date formats may vary (YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY, YYYY年MM月DD日, etc.) - standardize to YYYY-MM-DD
- The registration number is typically in the top-right corner of the certificate
- The registrant is often labeled as 注册人, 权利人, or Registrant
- International classification may be written in Chinese (第X类) or English (Class X)
- Trademark certificates often include both Chinese and English terms
- If the text contains multiple trademarks, ask the user which one to extract or extract all and let them choose

## Common Variations

### Chinese Trademark Certificates
- Look for terms like: 序号, 注册人, 注册号, 国际分类, 有效期限, 至
- Registration number format: typically starts with a region code (e.g., 12345678, G1234567)
- Classification format: 第25类, 第9类, 第35类, etc.

### English Trademark Certificates
- Look for terms like: Serial Number, Registrant, Registration Number, International Class, Valid Until, Expiry Date
- Registration number format: varies by country/region
- Classification format: Class 25, Class 09, Class 35, etc.

### Mixed Language Certificates
- May contain both Chinese and English terms
- Extract information from whichever language is more prominent or complete
- Check both top-right corner and other areas for registration number

## Registration Number Location

The registration number is typically located in:
- **Top-right corner** of the certificate
- Labeled as: 注册号, Registration No., Reg. No.
- Format varies by country but is usually a numeric code
- May include prefixes or suffixes depending on the registration authority

## Validity Period Extraction

The validity period can be expressed in several ways:
- Single date: "2025-12-31", "2025年12月31日", "Until 2025-12-31"
- Date range: "2015-01-01 to 2025-12-31", "From 2015.01.01 to 2025.12.31"
- Duration: "有效期10年" (Valid for 10 years) - requires calculation from registration date

Extract the expiration date (end of validity period) in YYYY-MM-DD format.

## Example Data Flow

```json
{
  "序号": "1",
  "注册人": "某某公司",
  "注册号": "12345678",
  "国际分类": "第25类",
  "有效期限": "2025-12-31",
  "商标标识图片路径": "/path/to/certificate_logo.png"
}
```

## Error Handling

If the LLM cannot find certain fields:
1. Return empty string for missing fields: `"": ""`
2. Note which fields were missing in the response
3. Suggest manual verification if critical fields like Registration Number or Registrant are missing
