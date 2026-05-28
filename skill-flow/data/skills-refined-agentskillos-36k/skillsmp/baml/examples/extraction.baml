// Structured Data Extraction Example
// Demonstrates: classes, nested types, optional fields, arrays, descriptions

class Resume {
    name string
    email string?
    phone string?
    skills string[]
    experience Experience[]
    education Education[]
}

class Experience {
    company string
    role string @description("Job title or position")
    start_year int
    end_year int? @description("Null if current position")
    highlights string[] @description("Key achievements or responsibilities")
}

class Education {
    institution string
    degree string
    field string? @description("Field of study, if applicable")
    year int @description("Graduation year")
}

function ExtractResume(resume_text: string) -> Resume {
    client "openai/gpt-4o"
    prompt #"
        Extract structured information from this resume.
        Be thorough but only include information explicitly stated.

        {{ ctx.output_format }}

        Resume:
        ---
        {{ resume_text }}
        ---
    "#
}

// Tests
test BasicResume {
    functions [ExtractResume]
    args {
        resume_text #"
            John Smith
            john.smith@email.com | (555) 123-4567

            Experience:
            - Senior Engineer at TechCorp (2020-present)
              Led migration to microservices architecture
              Reduced deployment time by 80%

            - Software Developer at StartupXYZ (2017-2020)
              Built customer-facing API

            Education:
            - BS Computer Science, MIT, 2017

            Skills: Python, Go, Kubernetes, AWS
        "#
    }
}
