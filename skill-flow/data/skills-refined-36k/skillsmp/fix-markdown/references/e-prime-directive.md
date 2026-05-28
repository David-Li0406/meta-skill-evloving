# E-prime communication protocol

## Core directive

All generated text, including conversational responses and technical
documentation, must adhere to the principles of E-Prime. This means
avoiding all forms of the verb "to be" (is, am, are, was, were, be,
been, being, isn't, aren't, wasn't, weren't).

## Rationale

This protocol fosters clarity, reduces ambiguity, and promotes a neutral
and less dogmatic tone. Eliminating the verb "to be" encourages the use
of descriptive, active verbs and the explicit attribution of
observations and statements. This leads to more precise and actionable
communication.

## Implementation guidelines

### 1. Replace "to be" with active verbs

Instead of describing a static state, describe a dynamic action,
function, or property.

- **Instead of:** "The system is slow."
- **Write:** "The system responds slowly." or "The system exhibits high
  latency under load."

- **Instead of:** "This setting is for enabling notifications."
- **Write:** "This setting enables notifications."

### 2. Attribute observations and opinions

State the source or context of an observation. This avoids presenting
subjective statements as neutral facts.

- **Instead of:** "This is the best approach."
- **Write:** "This approach appears to offer the most benefits." or "I
  conclude this approach works best because."

- **Instead of:** "The documentation is unclear."
- **Write:** "I find the documentation difficult to understand." or
  "Developers reported confusion with the documentation."

### 3. Describe functionality and behavior

When documenting systems or code, focus on component actions rather than
their static states.

- **Instead of:** "This variable is a flag that indicates if the user is
  logged in."
- **Write:** "This variable holds the user's login status." or "The
  system checks this variable to verify the user's session."

- **Instead of:** "The `User` class is the central model."
- **Write:** "The `User` class represents the central model in the
  application."

## Quick reference examples

| Standard English (Avoid)  | E-Prime (Prefer)                                                   |
| :------------------------ | :----------------------------------------------------------------- |
| The API is unstable.      | The API frequently returns 500 errors.                             |
| This feature is in beta.  | This feature currently operates under a "beta" designation.        |
| The button is disabled.   | The system disables the button until the form contains valid data. |
| That was a good decision. | That decision led to a 20% performance improvement.                |
| It is important to        | Prioritize                                                         |
