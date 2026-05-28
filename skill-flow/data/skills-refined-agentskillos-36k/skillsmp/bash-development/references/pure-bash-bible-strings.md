# Pure Bash Bible - String Operations

Reference: [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible)

Pure bash alternatives to external string processing commands. Use these patterns to avoid dependencies on sed, awk, cut, and other external tools.

## Trim Leading and Trailing Whitespace

```bash
trim_string() {
    : "${1#"${1%%[![:space:]]*}"}"
    : "${_%"${_##*[![:space:]]}"}"
    printf '%s\n' "$_"
}

# Usage
trim_string "   Hello,  World    "  # Output: Hello,  World
```

## Trim All Whitespace and Truncate Spaces

```bash
# shellcheck disable=SC2086,SC2048
trim_all() {
    set -f
    set -- $*
    printf '%s\n' "$*"
    set +f
}

# Usage
trim_all "    Hello,    World    "  # Output: Hello, World
```

## Regex Matching

```bash
regex() {
    [[ $1 =~ $2 ]] && printf '%s\n' "${BASH_REMATCH[1]}"
}

# Usage
regex '    hello' '^\s*(.*)'              # Output: hello
regex "#FFFFFF" '^(#?([a-fA-F0-9]{6}))$'  # Output: #FFFFFF
```

## Split String on Delimiter

Requires Bash 4+:

```bash
split() {
   IFS=$'\n' read -d "" -ra arr <<< "${1//$2/$'\n'}"
   printf '%s\n' "${arr[@]}"
}

# Usage
split "apples,oranges,pears" ","          # Outputs each on new line
split "hello---world---name" "---"        # Multi-char delimiters work
```

## Case Conversion (Bash 4+)

```bash
lower() { printf '%s\n' "${1,,}"; }
upper() { printf '%s\n' "${1^^}"; }
reverse_case() { printf '%s\n' "${1~~}"; }

# Usage
lower "HELLO"        # Output: hello
upper "hello"        # Output: HELLO
reverse_case "HeLlO" # Output: hElLo
```

## Trim Quotes

```bash
trim_quotes() {
    : "${1//\'}"
    printf '%s\n' "${_//\"}"
}

# Usage
trim_quotes "'Hello', \"World\""  # Output: Hello, World
```

## Strip Pattern from String

```bash
# Strip all instances
strip_all() { printf '%s\n' "${1//$2}"; }

# Strip first instance
strip() { printf '%s\n' "${1/$2}"; }

# Strip from start (shortest/longest match)
lstrip() { printf '%s\n' "${1##$2}"; }

# Strip from end (shortest/longest match)
rstrip() { printf '%s\n' "${1%%$2}"; }

# Usage
strip_all "The Quick Brown Fox" "[aeiou]"  # Output: Th Qck Brwn Fx
strip_all "The Quick Brown Fox" "[[:space:]]"  # Output: TheQuickBrownFox
lstrip "The Quick Brown Fox" "The "  # Output: Quick Brown Fox
rstrip "The Quick Brown Fox" " Fox"  # Output: The Quick Brown
```

## URL Encoding/Decoding

```bash
urlencode() {
    local LC_ALL=C
    for (( i = 0; i < ${#1}; i++ )); do
        : "${1:i:1}"
        case "$_" in
            [a-zA-Z0-9.~_-]) printf '%s' "$_" ;;
            *) printf '%%%02X' "'$_" ;;
        esac
    done
    printf '\n'
}

urldecode() {
    : "${1//+/ }"
    printf '%b\n' "${_//%/\\x}"
}

# Usage
urlencode "hello world"  # Output: hello%20world
urldecode "hello%20world"  # Output: hello world
```

## Substring Checks

```bash
# Contains substring
[[ $var == *sub_string* ]]

# Starts with substring
[[ $var == sub_string* ]]

# Ends with substring
[[ $var == *sub_string ]]

# Using case statement
case "$var" in
    *sub_string*) echo "contains" ;;
    sub_string*) echo "starts with" ;;
    *sub_string) echo "ends with" ;;
esac
```

## Parameter Expansion Reference

| Syntax              | Description                      |
| ------------------- | -------------------------------- |
| `${var#pattern}`    | Remove shortest match from start |
| `${var##pattern}`   | Remove longest match from start  |
| `${var%pattern}`    | Remove shortest match from end   |
| `${var%%pattern}`   | Remove longest match from end    |
| `${var/pat/rep}`    | Replace first match              |
| `${var//pat/rep}`   | Replace all matches              |
| `${var:offset}`     | Substring from offset            |
| `${var:offset:len}` | Substring with length            |
| `${var:: -n}`       | Remove last n chars              |
| `${var: -n}`        | Get last n chars                 |
| `${#var}`           | String length                    |

## Case Modification Reference (Bash 4+)

| Syntax     | Description             |
| ---------- | ----------------------- |
| `${var^}`  | Uppercase first char    |
| `${var^^}` | Uppercase all           |
| `${var,}`  | Lowercase first char    |
| `${var,,}` | Lowercase all           |
| `${var~}`  | Reverse case first char |
| `${var~~}` | Reverse case all        |

## Default Value Reference

| Syntax            | Description                           |
| ----------------- | ------------------------------------- |
| `${var:-default}` | Use default if empty or unset         |
| `${var-default}`  | Use default if unset                  |
| `${var:=default}` | Set and use default if empty or unset |
| `${var=default}`  | Set and use default if unset          |
| `${var:+value}`   | Use value if var is not empty         |
| `${var:?error}`   | Display error if empty or unset       |
