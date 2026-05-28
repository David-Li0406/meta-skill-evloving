# Pure Bash Bible - Variables and Internal Features

Reference: [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible)

Pure bash patterns for variable handling, parameter expansion, arithmetic, traps, and internal variables.

## Indirect Variable Access

```bash
hello_world="value"

# Using variable indirection
var="world"
ref="hello_$var"
printf '%s\n' "${!ref}"  # Output: value

# Using nameref (Bash 4.3+)
declare -n ref=hello_$var
printf '%s\n' "$ref"     # Output: value
```

## Name a Variable Based on Another

```bash
var="world"
declare "hello_$var=value"
printf '%s\n' "$hello_world"  # Output: value
```

## Arithmetic Operations

```bash
# Simple math
((var=1+2))

# Increment/Decrement
((var++))
((var--))
((var+=5))
((var-=3))

# Using variables
((result=var1*var2))
((result=arr[0]+arr[1]))

# Ternary test
((var=var2>var?var2:var))  # Set var to max of var and var2
```

## Loops Without seq

```bash
# Range (no variables)
for i in {0..100}; do
    printf '%s\n' "$i"
done

# Variable range
VAR=50
for ((i=0; i<=VAR; i++)); do
    printf '%s\n' "$i"
done

# With step (Bash 4+)
for i in {1..10..2}; do  # Increment by 2
    printf '%s\n' "$i"
done

# Zero-padded (Bash 4+)
for i in {01..100}; do
    printf '%s\n' "$i"
done
```

## Brace Expansion

```bash
# Numeric ranges
echo {1..100}           # 1 2 3 ... 100
echo {a..z}             # a b c ... z
echo {A..Z}{0..9}       # A0 A1 ... Z9

# String lists
echo {apples,oranges,pears}
rm -rf ~/Downloads/{Movies,Music,ISOS}

# Floats
echo 1.{1..9}           # 1.1 1.2 ... 1.9
```

## Traps

```bash
# Cleanup on exit
trap 'printf \\e[2J\\e[H\\e[m' EXIT

# Ignore Ctrl+C
trap '' INT

# React to window resize
trap 'get_term_size' SIGWINCH

# Execute before every command
trap 'code_here' DEBUG

# Execute when function/sourced file finishes
trap 'code_here' RETURN
```

## Internal Variables

| Variable              | Description                |
| --------------------- | -------------------------- |
| `$BASH`               | Path to bash binary        |
| `$BASH_VERSION`       | Bash version string        |
| `${BASH_VERSINFO[@]}` | Version as array           |
| `$EDITOR`             | User's preferred editor    |
| `${FUNCNAME[0]}`      | Current function name      |
| `${FUNCNAME[1]}`      | Parent function name       |
| `$HOSTNAME`           | System hostname            |
| `$HOSTTYPE`           | System architecture        |
| `$OSTYPE`             | Operating system type      |
| `$PWD`                | Current working directory  |
| `$SECONDS`            | Seconds since script start |
| `$RANDOM`             | Random integer (0-32767)   |
| `$LINENO`             | Current line number        |
| `$BASH_SOURCE`        | Source file array          |

## Terminal Information

### Get Terminal Size (from script)

```bash
get_term_size() {
    shopt -s checkwinsize; (:;:)
    printf '%s\n' "$LINES $COLUMNS"
}
```

### Get Cursor Position

```bash
get_cursor_pos() {
    IFS='[;' read -p $'\e[6n' -d R -rs _ y x _
    printf '%s\n' "$x $y"
}
```

## Date Without External Commands

Requires Bash 4+:

```bash
date() {
    printf "%($1)T\\n" "-1"
}

# Usage
date "%a %d %b  - %l:%M %p"  # Fri 15 Jun - 10:00 AM

# Direct printf
printf '%(%Y-%m-%d %H:%M:%S)T\n' -1

# Assign to variable
printf -v date '%(%Y-%m-%d)T' -1
```

## Sleep Without External Command

Requires Bash 4+:

```bash
read_sleep() {
    read -rt "$1" <> <(:) || :
}

# Usage
read_sleep 1      # Sleep 1 second
read_sleep 0.1    # Sleep 100ms
```

## Check if Program in PATH

```bash
# Method 1: type
type -p executable_name &>/dev/null

# Method 2: hash
hash executable_name &>/dev/null

# Method 3: command
command -v executable_name &>/dev/null

# As a test
if type -p convert &>/dev/null; then
    # Program is available
fi
```

## Get Username

Requires Bash 4.4+:

```bash
: \\u
printf '%s\n' "${_@P}"
```

## Generate UUID V4

Note: Not cryptographically secure.

```bash
uuid() {
    C="89ab"
    for ((N=0;N<16;++N)); do
        B="$((RANDOM%256))"
        case "$N" in
            6)  printf '4%x' "$((B%16))" ;;
            8)  printf '%c%x' "${C:$RANDOM%${#C}:1}" "$((B%16))" ;;
            3|5|7|9) printf '%02x-' "$B" ;;
            *) printf '%02x' "$B" ;;
        esac
    done
    printf '\n'
}
```

## Progress Bar

```bash
bar() {
    # Usage: bar 1 10
    #            ^----- Elapsed percentage (0-100)
    #               ^-- Total length in chars
    ((elapsed=$1*$2/100))
    printf -v prog  "%${elapsed}s"
    printf -v total "%$(($2-elapsed))s"
    printf '%s\r' "[${prog// /-}${total}]"
}

# Usage
for ((i=0;i<=100;i++)); do
    bar "$i" "10"
    sleep 0.05
done
printf '\n'
```

## Escape Sequences - Text Colors

| Sequence               | Description          |
| ---------------------- | -------------------- |
| `\e[38;5;<NUM>m`       | 256-color foreground |
| `\e[48;5;<NUM>m`       | 256-color background |
| `\e[38;2;<R>;<G>;<B>m` | RGB foreground       |
| `\e[48;2;<R>;<G>;<B>m` | RGB background       |

## Escape Sequences - Text Attributes

| Sequence | Description   |
| -------- | ------------- |
| `\e[m`   | Reset all     |
| `\e[1m`  | Bold          |
| `\e[2m`  | Faint         |
| `\e[3m`  | Italic        |
| `\e[4m`  | Underline     |
| `\e[5m`  | Blink         |
| `\e[7m`  | Reverse       |
| `\e[9m`  | Strikethrough |

## Escape Sequences - Cursor

| Sequence      | Description          |
| ------------- | -------------------- |
| `\e[<L>;<C>H` | Move to position     |
| `\e[H`        | Move to home (0,0)   |
| `\e[<N>A`     | Move up N lines      |
| `\e[<N>B`     | Move down N lines    |
| `\e[<N>C`     | Move right N columns |
| `\e[<N>D`     | Move left N columns  |
| `\e[s`        | Save position        |
| `\e[u`        | Restore position     |

## Escape Sequences - Erasing

| Sequence    | Description               |
| ----------- | ------------------------- |
| `\e[K`      | Erase to end of line      |
| `\e[1K`     | Erase to start of line    |
| `\e[2K`     | Erase entire line         |
| `\e[J`      | Erase to bottom of screen |
| `\e[2J`     | Clear screen              |
| `\e[2J\e[H` | Clear screen and home     |

## Performance Tip

Disable Unicode for performance-critical scripts:

```bash
LC_ALL=C
LANG=C
```

## Bypass Aliases/Functions

```bash
# Bypass alias
\ls

# Bypass function
command ls
```

## Run Command in Background

```bash
bkr() {
    (nohup "$@" &>/dev/null &)
}

bkr ./some_script.sh  # Runs even after terminal closes
```

## Capture Function Return Without Subshell

Requires Bash 4+:

```bash
to_upper() {
    local -n ptr=${1}
    ptr=${ptr^^}
}

foo="bar"
to_upper foo
printf "%s\n" "${foo}"  # BAR
```
