---
name: gemini-ocr
description: Use this skill when you need to integrate document OCR capabilities using the Google Gemini Flash API to extract data from passports and licenses.
---

# Gemini OCR Integration

Document OCR using Google Gemini Flash API.

## Overview

| Feature | Description |
|---------|-------------|
| API | Google Gemini Flash 2.0 |
| Use Cases | Passport, National ID, Driving License |
| Output | Structured JSON with extracted fields |

## API Configuration

```json
// appsettings.json
{
  "Gemini": {
    "ApiKey": "YOUR_API_KEY",
    "Model": "gemini-2.0-flash",
    "Endpoint": "https://generativelanguage.googleapis.com/v1beta/models"
  }
}
```

## DocumentOcrService

```csharp
// Services/DocumentOcrService.cs
public class DocumentOcrService
{
    private readonly HttpClient m_httpClient;
    private readonly string m_apiKey;
    private readonly string m_model;

    public DocumentOcrService(HttpClient httpClient, IConfiguration config)
    {
        m_httpClient = httpClient;
        m_apiKey = config["Gemini:ApiKey"]!;
        m_model = config["Gemini:Model"] ?? "gemini-2.0-flash";
    }

    public async Task<PassportData> ExtractPassportDataAsync(Stream imageStream)
    {
        var base64Image = await ConvertToBase64Async(imageStream);

        var request = new GeminiRequest
        {
            Contents =
            [
                new GeminiContent
                {
                    Parts =
                    [
                        new TextPart
                        {
                            Text = """
                                Extract passport information from this image.
                                Return JSON only with these fields:
                                {
                                    "fullName": "string",
                                    "nationality": "string",
                                    "passportNumber": "string",
                                    "dateOfBirth": "YYYY-MM-DD",
                                    "expiryDate": "YYYY-MM-DD",
                                    "gender": "M/F",
                                    "placeOfBirth": "string"
                                }
                                If a field is not readable, use null.
                                """
                        },
                        new InlineDataPart
                        {
                            InlineData = new InlineData
                            {
                                MimeType = "image/jpeg",
                                Data = base64Image
                            }
                        }
                    ]
                }
            ]
        };

        // Send request and handle response...
    }

    private async Task<string> ConvertToBase64Async(Stream imageStream)
    {
        using var memoryStream = new MemoryStream();
        await imageStream.CopyToAsync(memoryStream);
        return Convert.ToBase64String(memoryStream.ToArray());
    }
}
```