---
name: gemini-ocr
description: Document OCR integration using Google Gemini Flash API for extracting data from passports and licenses.
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

```csharp
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

        var url = $"https://generativelanguage.googleapis.com/v1beta/models/{m_model}:generateContent?key={m_apiKey}";
        var response = await m_httpClient.PostAsJsonAsync(url, request);
        var result = await response.Content.ReadFromJsonAsync<GeminiResponse>();

        return ParsePassportResponse(result!);
    }

    public async Task<DrivingLicenseData> ExtractDrivingLicenseDataAsync(Stream imageStream)
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
                                Extract driving license information from this image.
                                Return JSON only with these fields:
                                {
                                    "fullName": "string",
                                    "licenseNumber": "string",
                                    "issuingCountry": "string",
                                    "licenseClass": "string",
                                    "issueDate": "YYYY-MM-DD",
                                    "expiryDate": "YYYY-MM-DD"
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

        var url = $"https://generativelanguage.googleapis.com/v1beta/models/{m_model}:generateContent?key={m_apiKey}";
        var response = await m_httpClient.PostAsJsonAsync(url, request);
        var result = await response.Content.ReadFromJsonAsync<GeminiResponse>();

        return ParseLicenseResponse(result!);
    }

    private static async Task<string> ConvertToBase64Async(Stream stream)
    {
        using var memoryStream = new MemoryStream();
        await stream.CopyToAsync(memoryStream);
        return Convert.ToBase64String(memoryStream.ToArray());
    }

    private static PassportData ParsePassportResponse(GeminiResponse response)
    {
        var text = response.Candidates?[0].Content?.Parts?[0].Text ?? "{}";

        // Extract JSON from markdown code block if present
        if (text.Contains("```json"))
        {
            var start = text.IndexOf("```json") + 7;
            var end = text.LastIndexOf("```");
            text = text[start..end].Trim();
        }

        return text.DeserializeFromJson<PassportData>() ?? new PassportData();
    }
}
```

## Request/Response Models

```csharp
// Models/GeminiModels.cs
public class GeminiRequest
{
    [JsonPropertyName("contents")]
    public List<GeminiContent> Contents { get; set; } = [];
}

public class GeminiContent
{
    [JsonPropertyName("parts")]
    public List<object> Parts { get; set; } = [];
}

public class TextPart
{
    [JsonPropertyName("text")]
    public string Text { get; set; } = "";
}

public class InlineDataPart
{
    [JsonPropertyName("inline_data")]
    public InlineData InlineData { get; set; } = new();
}

public class InlineData
{
    [JsonPropertyName("mime_type")]
    public string MimeType { get; set; } = "image/jpeg";

    [JsonPropertyName("data")]
    public string Data { get; set; } = "";
}

public class GeminiResponse
{
    [JsonPropertyName("candidates")]
    public List<GeminiCandidate>? Candidates { get; set; }
}

public class GeminiCandidate
{
    [JsonPropertyName("content")]
    public GeminiContent? Content { get; set; }
}
```

## Data Models

```csharp
// Models/PassportData.cs
public class PassportData
{
    public string? FullName { get; set; }
    public string? Nationality { get; set; }
    public string? PassportNumber { get; set; }
    public string? DateOfBirth { get; set; }
    public string? ExpiryDate { get; set; }
    public string? Gender { get; set; }
    public string? PlaceOfBirth { get; set; }
}

// Models/DrivingLicenseData.cs
public class DrivingLicenseData
{
    public string? FullName { get; set; }
    public string? LicenseNumber { get; set; }
    public string? IssuingCountry { get; set; }
    public string? LicenseClass { get; set; }
    public string? IssueDate { get; set; }
    public string? ExpiryDate { get; set; }
}
```

## Usage in Blazor

```razor
@inject DocumentOcrService OcrService
@inject ISnackbar Snackbar

<MudFileUpload T="IBrowserFile" Accept=".jpg,.jpeg,.png" FilesChanged="OnFileSelected">
    <ActivatorContent>
        <MudButton Variant="Variant.Filled" Color="Color.Primary" StartIcon="@Icons.Material.Filled.CameraAlt">
            Upload Passport
        </MudButton>
    </ActivatorContent>
</MudFileUpload>

@if (m_extractedData is not null)
{
    <MudPaper Class="pa-4 mt-4">
        <MudText Typo="Typo.h6">Extracted Information</MudText>
        <MudGrid>
            <MudItem xs="6">
                <MudTextField Value="@m_extractedData.FullName" Label="Full Name" ReadOnly="false"
                              @bind-Value="m_renter.FullName" />
            </MudItem>
            <MudItem xs="6">
                <MudTextField Value="@m_extractedData.PassportNumber" Label="Passport No"
                              @bind-Value="m_renter.PassportNo" />
            </MudItem>
        </MudGrid>
    </MudPaper>
}

@code {
    private PassportData? m_extractedData;
    private Renter m_renter = new();
    private bool m_processing;

    private async Task OnFileSelected(IBrowserFile file)
    {
        m_processing = true;
        try
        {
            using var stream = file.OpenReadStream(maxAllowedSize: 10 * 1024 * 1024);
            m_extractedData = await OcrService.ExtractPassportDataAsync(stream);

            // Auto-fill form
            if (m_extractedData.FullName is not null)
                m_renter.FullName = m_extractedData.FullName;
            if (m_extractedData.PassportNumber is not null)
                m_renter.PassportNo = m_extractedData.PassportNumber;
            if (m_extractedData.Nationality is not null)
                m_renter.Nationality = m_extractedData.Nationality;

            Snackbar.Add("Document processed successfully", Severity.Success);
        }
        catch (Exception ex)
        {
            Snackbar.Add($"OCR failed: {ex.Message}", Severity.Error);
        }
        finally
        {
            m_processing = false;
        }
    }
}
```

## Service Registration

```csharp
// Program.cs
builder.Services.AddHttpClient<DocumentOcrService>();
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Image quality | Request clear, well-lit photos |
| Validation | Always allow manual correction |
| Storage | Save raw OCR JSON for debugging |
| Error handling | Graceful fallback to manual entry |
| Rate limiting | Implement retry with backoff |

## Document Workflow

1. User uploads document image
2. Image sent to Gemini for OCR
3. Extracted data displayed for review
4. User corrects any errors
5. Document saved with both image and OCR data

## Source
- Gemini API: https://ai.google.dev/
