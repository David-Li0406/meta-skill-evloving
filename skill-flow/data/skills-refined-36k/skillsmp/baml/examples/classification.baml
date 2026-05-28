// Classification Example
// Demonstrates: enums, descriptions, @skip, literal unions, multi-label

enum Sentiment {
    POSITIVE @description("Expresses satisfaction, happiness, or approval")
    NEGATIVE @description("Expresses dissatisfaction, frustration, or disapproval")
    NEUTRAL @description("Factual or emotionally neutral")
}

enum EmailCategory {
    SUPPORT @description("Technical help, account issues, bug reports")
    BILLING @description("Payment, invoices, refunds, subscription")
    SALES @description("Product inquiries, demos, pricing")
    SPAM @description("Unsolicited marketing, scams")
    OTHER
}

enum Priority {
    LOW
    MEDIUM
    HIGH
    URGENT @description("Requires immediate attention")
}

class EmailClassification {
    category EmailCategory
    priority Priority
    sentiment Sentiment
    requires_human bool @description("True if this needs human review")
    summary string @description("One-sentence summary of the email")
}

function ClassifyEmail(email_content: string) -> EmailClassification {
    client "openai/gpt-4o"
    prompt #"
        Analyze this customer email and classify it.

        {{ ctx.output_format }}

        Email:
        ---
        {{ email_content }}
        ---
    "#
}

// Simple binary classification using literal union
function IsSpam(text: string) -> "spam" | "not_spam" {
    client "openai/gpt-4o"
    prompt #"
        Determine if this message is spam.

        {{ ctx.output_format }}

        Message: {{ text }}
    "#
}

// Multi-label classification (array of enum)
enum Tag {
    URGENT
    TECHNICAL
    FINANCIAL
    LEGAL
    PERSONAL
    FOLLOW_UP_NEEDED
}

function TagEmail(email: string) -> Tag[] {
    client "openai/gpt-4o"
    prompt #"
        Apply all relevant tags to this email. Return empty array if none apply.

        {{ ctx.output_format }}

        Email: {{ email }}
    "#
}

// Tests
test SupportEmail {
    functions [ClassifyEmail]
    args {
        email_content "Hi, I can't log into my account. I've tried resetting my password 3 times but the reset email never arrives. This is really frustrating!"
    }
}

test SpamCheck {
    functions [IsSpam]
    args {
        text "CONGRATULATIONS! You've won $1,000,000! Click here to claim your prize NOW!"
    }
    @@assert({{ this == "spam" }})
}
