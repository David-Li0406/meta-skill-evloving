# Datetime Format

East has it's own datetime formatting system.
East's front end converts datetime format strings into a format specifier as a list of tokens (literals, years, months, etc).
East's backend runtimes work the list of tokens.

 - types.ts: Types to specify a format as an array of tokens.
 - tokenize.ts: A datetime format string can be turned into an array of tokens using `parseDateTimeFormat("YYYY-MM-DD")`
 - print.ts: Print a `Date` as a `string` given a format specifier
 - parse.ts: Parse a `string` to a `Date` given a format specifier
 - validate.ts: Check that the token list is sensible and self-consistent
