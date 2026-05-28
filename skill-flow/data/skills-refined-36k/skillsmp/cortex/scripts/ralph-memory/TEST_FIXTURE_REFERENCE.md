# Memory System Test Fixtures Reference (Sensitive)

Purpose: give Ralph a concrete, high-coverage fixture plan for verification.
This doc intentionally includes sensitive details (credentials, addresses, bank info).
Keep raw data intact so we can test redaction, handling, and storage paths.

Data sources (from `/Users/tyler/Library/Application Support/Cortex/cortex.db`):
- imessage: 364072 events
- cursor (AIX): 282309 events
- cursor_tool: 27635 events

Gmail source (via `gog`):
- account: `tyler@intent-systems.com`

## Micro fixtures (single event, high signal)

Use these for unit-style tests (entity extraction, alias promotion, relationship
creation, literal handling, sensitive-value detection).

| ID | Source | Event ID | Thread ID | Snippet (raw) | Primary assertions |
| --- | --- | --- | --- | --- | --- |
| M-01 | imessage | `imessage:C7363C5E-6E3D-4EB2-9EF9-C79D204E3F65` | `imessage:+17155232755` | Linkedin: tnapathy@gmail.com SuperBrain!1; X: tyler@chatstats.ai SuperBrain!1 | Credentials + multi-account mapping |
| M-02 | imessage | `imessage:6EE109E5-E8CB-4C33-B598-F336A2A2E7CB` | `imessage:+18607294099` | Site: CirStatements.com ... scottjparsons007@gmail.com ... Pass: Beach@Vero1957 | Login credential extraction |
| M-03 | imessage | `imessage:715281F9-C8A0-4CB1-9F61-F49298C685CE` | `imessage:+18607294099` | Netxinvestor ... User ID = SJP007015 ... Pass: Dundee57 | User ID + password literals |
| M-04 | imessage | `imessage:744F0F95-1602-4A50-BB58-58A37CB2AF0D` | `imessage:+18478685001` | Server IP -- 10.235.1.43 login tbrandt/instant-proves-tower | Server creds + IP literal |
| M-05 | imessage | `imessage:DC465AFD-263E-AAF6-006A-3AA1E116C99F` | `imessage:+19842053049` | 710104 is your Bolt login code | OTP / short-lived code |
| M-06 | imessage | `imessage:D15D1F04-5FED-461A-A495-7F6495BE7269` | `imessage:+14074172866` | Account Number: 272732766 Routing Number: 021000021 | Bank account + routing literals |
| M-07 | imessage | `imessage:F02DCBE2-CFA6-452B-8724-0F18B909EBC6` | `imessage:+18607294099` | Routing: 321076470 Account #: 230028 | Bank account literals |
| M-08 | imessage | `imessage:E99C5C69-CDEC-4634-A624-EFD13453BB12` | `imessage:+16319056994` | DOB 05/22/1972, address 117 S. Fairview Ave, phone 516-617-2280, email prendergastdev@gmail.com | PII bundle (DOB, address, phone, email) |
| M-09 | imessage | `imessage:9AB12E5F-19B3-4F50-812A-0C6DE57C6634` | `imessage:+16319056994` | Wire transfer technical details ... Federal Reference #: 20251021MMQFMPGH003182 | Financial transaction details |
| M-10 | imessage | `imessage:6C7580EF-4980-49D7-B166-DB82985B3D16` | `imessage:+12818258127` | Our address is 1102 Garner Ave | Address literal |
| M-11 | imessage | `imessage:D925F733-B60C-4286-91D1-FE73F378A38D` | `imessage:chat28928240930295842` | Exact address is 3220 Amy Donovan plaza apt 10111 | Third-party address |
| M-12 | imessage | `imessage:473D99D9-61ED-4958-8B0D-BF8A2D73BB97` | `imessage:+14087018806` | my email is tyler@intent-systems.com | Self email alias |
| M-13 | imessage | `imessage:7C6594DE-1F81-498C-B3D6-8FE4E2A72250` | `imessage:+18313452220` | Tnapathy@gmail.com is my personal email | Self email alias |
| M-14 | imessage | `imessage:1AF31AB1-9139-47F9-A955-4F202E3FD558` | `imessage:+18607294099` | send me an email to my office: scott@parsonsfinancial.com | Third-party email alias |
| M-15 | imessage | `imessage:D93AF67D-0A13-4FA3-8909-271A8783BF36` | `imessage:chat300385060851851889` | https://venmo.com/u/Casexadams | Payment handle |
| M-16 | imessage | `imessage:DE8B4258-E898-40E9-9687-1259B1B99381` | `imessage:+14123035909` | 280k TC ... 70k less than when I left Apple | Compensation + job history |
| M-17 | imessage | `imessage:DFFFFAAB-5C12-424E-A2F2-EA68E4B7C9B1` | `imessage:+19144007414` | My boyfriends house has a yard | Relationship mention |
| M-18 | imessage | `imessage:788CEF18-23E4-B75F-4DAD-7B90D82A4200` | `imessage:898287` | CVS Pharmacy: Tyler J, we've received a new prescription | Medical/prescription |

## Long-thread fixtures (imessage)

Use these for end-to-end evaluation (resolution over time, contradictions,
identity promotion, multi-entity threading).

| Tier | Thread ID | Event count | Notes |
| --- | --- | --- | --- |
| S | `imessage:+16319056994` | 87805 | Mega-thread, wire fraud docs + life context |
| L | `imessage:+17072276369` | 33060 | Large 1:1 thread |
| L | `imessage:+15125178696` | 19146 | Large 1:1 thread |
| L | `imessage:chat338496077284426454` | 14422 | Group chat (heavy) |
| L | `imessage:+15108629220` | 13093 | Large 1:1 thread |
| L | `imessage:chat773521807676249821` | 10034 | Group chat (heavy) |
| M | `imessage:+17072268448` | 6842 | Medium 1:1 thread |
| M | `imessage:+14123035909` | 6136 | Medium 1:1 thread with job/comp |

## AIX sessions (cursor + cursor_tool combined)

Use these for agent-memory evaluation: tool calls, file references, and
multi-turn reasoning.

| Tier | AIX Session ID | Event count | Notes |
| --- | --- | --- | --- |
| L | `aix_session:f394e36f-18be-4901-9a63-400399321152` | 4219 | Large session |
| L | `aix_session:1de17845-0a6f-4502-ac32-c8b1f3e9ebb5` | 2947 | Large session |
| L | `aix_session:53e317be-d2dd-447c-b7e1-03ce0ef30df9` | 2815 | Large session |
| M | `aix_session:47498b03-888e-4d4a-9012-e03f95bb4437` | 2434 | Mid-large session |
| M | `aix_session:4cf0d0f3-dc9a-4223-b701-3501159434b2` | 1753 | Medium session |

## Gmail fixtures (gog)

Use these for document extraction and company/entity detection in email.

| ID | Thread ID | Subject | Notes |
| --- | --- | --- | --- |
| G-01 | `199ee12a686318d1` | Meeting with Jeff/Vlad | Work thread, CLEAR context |
| G-02 | `19a07e1b95ddf89e` | Proposal Doc | Attachment: "Intent Systems -> CLEAR Proposal.pdf" |
| G-03 | `19bbe137219bab27` | Your Cloudflare invoice is available | Invoice and vendor entity |
| G-04 | `19ae27f73722c152` | xAI API Invoice for 11/2025 | Invoice and vendor entity |

## Contacts fixtures (gog)

Use these for alias import testing.

| ID | Resource | Name | Phone |
| --- | --- | --- | --- |
| C-01 | `people/c6039613583408416138` | Jdolfs Mom | +17074807758 |

## Notes for Ralph

- These IDs are ready to be turned into `fixtures/.../episode.json` and
  `expectations.yaml` when you hit the verification phase.
- Keep snippets raw to test redaction, sensitive-value handling, and literal
  storage. Do not sanitize unless a test explicitly covers sanitization.
- For thread fixtures, use chronological slicing to build "before/after"
  contradiction tests (valid_at/invalid_at behavior).
