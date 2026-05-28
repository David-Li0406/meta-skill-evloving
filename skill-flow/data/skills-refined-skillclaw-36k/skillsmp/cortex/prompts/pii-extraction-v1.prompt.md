# PII Extraction Prompt v1

## Purpose

Extract ALL personally identifiable information from a conversation chunk. This creates a comprehensive identity graph for each person mentioned, enabling cross-channel identity resolution through identifier collisions.

## Input

- **Channel**: The communication channel (iMessage, Gmail, Discord, etc.)
- **Primary Contact**: The person whose conversation this is (name + identifier)
- **User**: The owner of the cortex database
- **Messages**: A chunk of conversation (typically 50-100 messages or a logical conversation unit)

## Task

Extract ALL PII for EVERY person mentioned in this conversation:
1. **The primary contact** - the person the user is communicating with
2. **The user themselves** - any PII about the user mentioned in the conversation
3. **Third parties** - any other people mentioned (family, friends, colleagues, etc.)

### Critical Guardrails
- Speaker labels (e.g., "Casey Adams:") are metadata for attribution only.
- Speaker labels may be generic (e.g., "User", "Participant1") and are not names.
- Do NOT use speaker labels or contact names as evidence for any name fields.
- Only extract `full_legal_name`, `given_name`, `family_name`, or `nicknames` when the
  name appears explicitly in message content (not in the speaker label).

For each piece of information:
- Quote the exact evidence from the messages
- Indicate confidence level (high/medium/low)
- Note whether this is self-disclosed or mentioned by someone else

---

## Complete PII Taxonomy

Extract any of the following categories if present:

### 1. Core Identity
| Field | Description | Examples |
|-------|-------------|----------|
| full_legal_name | Complete legal name | "James Michael Brandt" |
| given_name | First name | "James", "Jim" |
| middle_name | Middle name(s) | "Michael" |
| family_name | Last name / surname | "Brandt" |
| maiden_name | Pre-marriage surname | "Smith" |
| previous_names | Former legal names | Name changes |
| nicknames | Informal names used | "Jimmy", "Dad", "Big J" |
| aliases | Other names they go by | Stage names, pen names |
| date_of_birth | Full birth date | "1959-03-15" |
| age | Current age or age mentioned | "65", "mid-sixties" |
| birth_year | Year of birth | "1959" |
| place_of_birth | City/country of birth | "San Francisco, CA" |
| gender | Gender identity | "male", "female", "non-binary" |
| pronouns | Preferred pronouns | "he/him", "they/them" |
| nationality | Country of citizenship | "American", "dual US/Italian" |
| ethnicity | Ethnic background | If mentioned |
| languages | Languages spoken | "English, Spanish" |

### 2. Physical Description
| Field | Description | Examples |
|-------|-------------|----------|
| height | Height | "6'2\"", "tall" |
| weight | Weight | "180 lbs" |
| eye_color | Eye color | "blue", "brown" |
| hair_color | Hair color | "gray", "blonde" |
| hair_style | Hair description | "bald", "long hair" |
| skin_tone | Skin description | If mentioned |
| distinguishing_marks | Tattoos, scars, birthmarks | "dragon tattoo on left arm" |
| glasses | Wears glasses/contacts | "wears reading glasses" |
| facial_hair | Beard, mustache, etc. | "has a beard" |

### 3. Contact Information
| Field | Description | Examples |
|-------|-------------|----------|
| email_personal | Personal email addresses | "jim@gmail.com" |
| email_work | Work email addresses | "jbrandt@company.com" |
| email_school | Educational email | "jb@university.edu" |
| email_other | Other email accounts | Recovery emails, alts |
| phone_mobile | Mobile/cell phone | "+1-707-555-1234" |
| phone_home | Home landline | "(707) 555-5678" |
| phone_work | Work phone | "ext. 4567" |
| phone_fax | Fax number | If mentioned |
| address_home | Home address | "123 Main St, Napa, CA 94558" |
| address_work | Work address | Office location |
| address_mailing | Mailing/PO Box | "PO Box 123" |
| address_previous | Former addresses | Places they used to live |

### 4. Digital Identity
| Field | Description | Examples |
|-------|-------------|----------|
| username_* | Usernames on platforms | "napageneral" on Chess.com |
| social_twitter | Twitter/X handle | "@jimbrandt" |
| social_instagram | Instagram handle | "@jim.brandt" |
| social_linkedin | LinkedIn profile | URL or username |
| social_facebook | Facebook profile | URL or name |
| social_tiktok | TikTok handle | "@jimb" |
| social_youtube | YouTube channel | Channel name/URL |
| social_reddit | Reddit username | "u/jimbrandt" |
| social_discord | Discord handle | "JimB#1234" |
| social_other | Other platforms | Any social media |
| website_personal | Personal website | "jimbrandt.com" |
| website_business | Business website | "napageneralstore.com" |
| gaming_handle | Gaming usernames | Xbox, PlayStation, Steam |
| login_email | Email used for logins | Account recovery emails |
| password_hints | Password hints mentioned | DO NOT extract actual passwords |

### 5. Relationships
| Field | Description | Examples |
|-------|-------------|----------|
| spouse | Spouse or partner | "Jill", married to |
| partner | Romantic partner | Boyfriend/girlfriend |
| ex_spouse | Former spouse | "divorced from Sarah" |
| children | Children's names | "son Tyler", "daughter Emma" |
| parents | Parents' names | "mom Carol", "father Ed" |
| siblings | Brothers/sisters | "brother Mike" |
| grandparents | Grandparents | "grandma Rose" |
| grandchildren | Grandchildren | Names |
| aunts_uncles | Aunts and uncles | "Uncle Scott" |
| cousins | Cousins | Names |
| in_laws | In-law relationships | "mother-in-law" |
| nieces_nephews | Nieces/nephews | Names |
| friends | Close friends mentioned | "best friend Tom" |
| roommates | Roommates | Current or past |
| neighbors | Neighbors | Names |
| pets | Pet names and types | "dog Max", "cat Luna" |
| emergency_contact | Emergency contact | Who to call |
| next_of_kin | Next of kin | Legal designation |

### 6. Professional

**IMPORTANT**: Distinguish between EMPLOYMENT (working FOR someone) vs OWNERSHIP (owning a business).

| Field | Description | Examples |
|-------|-------------|----------|
| **EMPLOYMENT** | *Working FOR a company* | |
| employer_current | Current employer (company you work FOR) | "Google", "works at Apple" |
| employer_previous | Past employers | Former jobs |
| job_title_current | Current job title | "Senior Engineer", "Manager" |
| job_title_previous | Previous job titles | Former titles |
| department | Department/team | "Sales", "Engineering" |
| role_description | What they do day-to-day | "manages the sales team" |
| manager | Their manager | "reports to Sarah" |
| direct_reports | People they manage | "manages 5 people" |
| colleagues | Coworkers mentioned | "works with Tom" |
| employee_id | Employee number | If mentioned |
| **OWNERSHIP** | *Owning/founding a business* | |
| business_owned | Businesses they OWN (array) | ["Napa General Store"] |
| business_role | Role in owned business | "Owner", "Co-owner", "Partner", "Founder" |
| business_founded | Businesses they started | "started the company in 2005" |
| business_invested | Businesses invested in | "angel investor in StartupX" |
| board_member_of | Board positions | "on the board of NonprofitY" |
| **GENERAL** | *Professional identity* | |
| profession | What they do (not where) | "restaurateur", "engineer" |
| industry | Industry they work in | "retail", "tech", "hospitality" |
| years_experience | Experience level | "20 years in retail" |
| professional_certifications | Certifications | "CPA", "PMP" |
| professional_licenses | Licenses held | "Real estate license" |
| work_email | Work email | See contact info |
| work_phone | Work phone | See contact info |
| work_address | Office location | See contact info |
| business_partners | Business partners | "partner with Mike" |
| salary | Salary if mentioned | Flag as sensitive |
| work_schedule | Work hours/days | "works weekends" |

### 7. Education
| Field | Description | Examples |
|-------|-------------|----------|
| school_current | Current school | If student |
| school_previous | Schools attended | "went to UCLA" |
| degree | Degrees earned | "MBA", "BS in Chemistry" |
| major | Field of study | "Business Administration" |
| minor | Minor field | "Economics" |
| graduation_year | When graduated | "Class of 1985" |
| gpa | GPA if mentioned | Flag if sensitive |
| student_id | Student ID | If mentioned |
| certifications | Professional certs | "CPA", "PMP" |
| licenses | Professional licenses | "Real estate license" |
| awards | Academic awards | "Dean's List" |
| activities | School activities | "played football" |

### 8. Government & Legal IDs
| Field | Description | Examples |
|-------|-------------|----------|
| ssn | Social Security Number | HIGHLY SENSITIVE - flag |
| passport_number | Passport number | SENSITIVE - flag |
| passport_country | Passport issuing country | "US passport" |
| drivers_license | Driver's license number | SENSITIVE - flag |
| drivers_license_state | DL issuing state | "California DL" |
| national_id | National ID number | SENSITIVE - flag |
| visa_type | Visa type | "H1B", "green card" |
| visa_status | Immigration status | "permanent resident" |
| tax_id | Tax ID / EIN | SENSITIVE - flag |
| voter_registration | Voter info | If mentioned |
| military_id | Military ID/service | "Army veteran" |
| criminal_record | Criminal history | SENSITIVE - flag |
| court_cases | Legal cases | SENSITIVE - flag |

### 9. Financial
| Field | Description | Examples |
|-------|-------------|----------|
| bank_name | Bank they use | "Bank of America" |
| bank_account | Account numbers | HIGHLY SENSITIVE - flag |
| credit_cards | Credit card info | HIGHLY SENSITIVE - flag |
| paypal | PayPal email/handle | "paypal.me/jim" |
| venmo | Venmo handle | "@jim-brandt" |
| cashapp | Cash App handle | "$jimbrandt" |
| zelle | Zelle email/phone | Usually same as contact |
| crypto_wallet | Crypto addresses | SENSITIVE - flag |
| income | Income level | SENSITIVE - flag |
| net_worth | Net worth | SENSITIVE - flag |
| credit_score | Credit score | SENSITIVE - flag |
| debts | Debts/loans | SENSITIVE - flag |
| mortgage | Mortgage info | SENSITIVE - flag |
| investments | Investment accounts | SENSITIVE - flag |

### 10. Medical & Health
| Field | Description | Examples |
|-------|-------------|----------|
| conditions | Medical conditions | SENSITIVE - flag |
| disabilities | Disabilities | SENSITIVE - flag |
| medications | Medications taken | SENSITIVE - flag |
| allergies | Allergies | "allergic to peanuts" |
| blood_type | Blood type | "O positive" |
| height_medical | Height (medical) | For medical context |
| weight_medical | Weight (medical) | For medical context |
| doctor | Primary doctor | "Dr. Smith" |
| dentist | Dentist | Name |
| specialists | Specialist doctors | "cardiologist" |
| hospital | Hospital preference | "goes to Kaiser" |
| insurance_health | Health insurance | "has Blue Cross" |
| insurance_dental | Dental insurance | Provider |
| pharmacy | Pharmacy used | "CVS on Main St" |
| medical_history | Medical history | SENSITIVE - flag |
| mental_health | Mental health info | HIGHLY SENSITIVE - flag |

### 11. Life Events & Dates
| Field | Description | Examples |
|-------|-------------|----------|
| birthday | Birthday (without year) | "March 15" |
| birth_date_full | Full birth date | "March 15, 1959" |
| wedding_date | Wedding anniversary | "married June 1985" |
| divorce_date | Divorce date | If mentioned |
| graduation_dates | Graduation dates | "graduated 1981" |
| job_start_dates | When started jobs | "started in 2010" |
| job_end_dates | When left jobs | "left in 2015" |
| move_dates | When moved places | "moved to Napa in 2000" |
| retirement_date | Retirement date | "retired 2020" |
| death_date | If deceased | Date of passing |
| significant_events | Other life events | Births, achievements |

### 12. Location & Presence
| Field | Description | Examples |
|-------|-------------|----------|
| location_current | Current city/area | "lives in Napa, CA" |
| location_state | State/province | "California" |
| location_country | Country | "USA" |
| location_timezone | Timezone | "Pacific Time" |
| location_previous | Previous locations | "used to live in SF" |
| location_hometown | Hometown | "grew up in Boston" |
| location_vacation | Vacation home | "has a place in Harwich" |
| location_frequent | Frequent places | "often at the gym" |
| commute | Commute info | "drives to work" |
| travel_current | Current travel | "in Italy right now" |
| travel_planned | Planned travel | "going to Hawaii" |
| travel_history | Past travel | "visited Japan" |

### 13. Preferences & Lifestyle
| Field | Description | Examples |
|-------|-------------|----------|
| political_affiliation | Political views | If mentioned |
| religious_affiliation | Religion | If mentioned |
| hobbies | Hobbies | "plays golf", "loves cooking" |
| sports_played | Sports they play | "plays tennis" |
| sports_watched | Sports they follow | "Giants fan" |
| music_preferences | Music taste | "loves jazz" |
| movie_preferences | Movie taste | "sci-fi fan" |
| book_preferences | Reading preferences | "reads mysteries" |
| food_preferences | Food likes | "loves Italian food" |
| dietary_restrictions | Diet restrictions | "vegetarian", "gluten-free" |
| restaurant_favorites | Favorite restaurants | "loves that Thai place" |
| drink_preferences | Drink preferences | "coffee drinker" |
| smoking | Smoking status | "quit smoking" |
| alcohol | Drinking habits | "social drinker" |
| exercise | Exercise habits | "runs every morning" |
| sleep_schedule | Sleep patterns | "early riser" |

### 14. Vehicles & Property
| Field | Description | Examples |
|-------|-------------|----------|
| vehicle_make | Car make | "Tesla" |
| vehicle_model | Car model | "Model 3" |
| vehicle_year | Car year | "2022" |
| vehicle_color | Car color | "red" |
| license_plate | License plate | Flag if mentioned |
| vehicle_previous | Previous cars | "used to drive a BMW" |
| motorcycle | Motorcycle | Make/model |
| boat | Boat | Name/type |
| property_owned | Properties owned | "owns a cabin" |
| rental | Renting status | "rents apartment" |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "iMessage",
    "primary_contact_name": "Dad",
    "primary_contact_identifier": "+16508238440",
    "user_name": "Tyler Brandt",
    "message_count": 50,
    "date_range": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-15T23:59:59Z"
    }
  },
  "facts": [
    {
      "subject_kind": "primary_contact",
      "subject_ref": "Dad",
      "category": "core_identity",
      "fact_type": "full_legal_name",
      "value": "James Brandt",
      "confidence": "high",
      "evidence": "meeting up with Jim and Janet; Jim@napageneralstore.com",
      "source": "inferred from email + nickname"
    },
    {
      "subject_kind": "third_party",
      "subject_ref": "Janet",
      "category": "core_identity",
      "fact_type": "given_name",
      "value": "Janet",
      "confidence": "high",
      "evidence": "meeting up with Jim and Janet"
    }
  ],
  "unattributed_facts": [
    {
      "fact_type": "phone",
      "fact_value": "+15551234567",
      "shared_by": "Dad",
      "context": "Sent as standalone message with no explanation",
      "possible_attributions": ["Dad's alternate number", "Third party contact", "Business number"],
      "note": "Cannot determine whose phone number this is without more context"
    },
    {
      "fact_type": "email",
      "fact_value": "support@somecompany.com",
      "shared_by": "Dad",
      "context": "Contact them at support@somecompany.com",
      "possible_attributions": ["Business contact", "Company support"],
      "note": "Shared email but not attributed to a specific person"
    }
  ]
}
```

---

## Important Rules

1. **Extract EVERYTHING** - Even small details can help with identity resolution later
2. **Quote exact evidence** - Always include the message text that supports each extraction
3. **Attribute correctly** - Be very careful about WHO each piece of PII belongs to
4. **Flag sensitive data** - Mark SSN, financial, medical info as sensitive
5. **Note self-disclosure** - Mark when someone explicitly shares their own info vs being mentioned
6. **Create new identity candidates** - If a third party is mentioned with enough detail, flag them
7. **Use unattributed_facts** - If an identifier (phone, email) is shared without clear ownership, put it in unattributed_facts with context about who shared it and possible attributions
8. **Owner vs Employer** - Distinguish between working FOR a company (employer_current) vs OWNING a business (business_owned). Someone who owns a restaurant is NOT employed BY it.
9. **Confidence levels**:
   - **high**: Explicitly stated or very clear
   - **medium**: Strongly implied or partially stated
   - **low**: Inferred or uncertain
10. **Don't hallucinate** - Only extract what's actually in the messages
11. **Facts array schema**:
    - Every fact MUST include: `subject_kind`, `subject_ref`, `category`, `fact_type`, `value`, `confidence`, `evidence`
    - `subject_kind` MUST be one of: `user`, `primary_contact`, `third_party`
    - `value` MUST be a single string (one fact per value)
    - `evidence` MUST be a single string of exact message text
      (use `; ` to join multiple evidence quotes)
    - Optional fields: `self_disclosed`, `source`, `related_person_ref`, `note`

---

## Conversation
{{{segment_text}}}
