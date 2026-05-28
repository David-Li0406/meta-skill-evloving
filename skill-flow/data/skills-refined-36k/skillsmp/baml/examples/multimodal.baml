// Multimodal Input Example
// Demonstrates: image, audio, pdf types, multiple media inputs

class ImageAnalysis {
    description string @description("Detailed description of the image")
    objects string[] @description("Main objects/subjects identified")
    text_content string? @description("Any text visible in the image")
    mood string? @description("Overall mood or tone, if applicable")
}

function AnalyzeImage(img: image) -> ImageAnalysis {
    client "openai/gpt-4o"
    prompt #"
        {{ _.role("user") }}
        Analyze this image in detail.

        {{ img }}

        {{ ctx.output_format }}
    "#
}

function CompareImages(image1: image, image2: image) -> string {
    client "openai/gpt-4o"
    prompt #"
        {{ _.role("user") }}
        Compare these two images. Describe similarities and differences.

        Image 1: {{ image1 }}
        Image 2: {{ image2 }}
    "#
}

// Document analysis
class DocumentSummary {
    title string?
    summary string @description("2-3 sentence summary")
    key_points string[]
    document_type string @description("e.g., invoice, report, contract, article")
}

function SummarizePdf(doc: pdf) -> DocumentSummary {
    client "openai/gpt-4o"
    prompt #"
        {{ _.role("user") }}
        Analyze this document and provide a structured summary.

        {{ doc }}

        {{ ctx.output_format }}
    "#
}

// Audio transcription + analysis
class AudioAnalysis {
    transcription string
    speaker_count int @description("Number of distinct speakers")
    language string
    summary string?
}

function AnalyzeAudio(audio_file: audio) -> AudioAnalysis {
    client "openai/gpt-4o"
    prompt #"
        {{ _.role("user") }}
        Transcribe and analyze this audio.

        {{ audio_file }}

        {{ ctx.output_format }}
    "#
}

// Tests
test ImageFromUrl {
    functions [AnalyzeImage]
    args {
        img {
            url "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        }
    }
}

test ImageFromFile {
    functions [AnalyzeImage]
    args {
        img {
            file "../test_assets/sample.png"
        }
    }
}

test PdfAnalysis {
    functions [SummarizePdf]
    args {
        doc {
            file "../test_assets/sample.pdf"
        }
    }
}
