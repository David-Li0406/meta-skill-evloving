# Pure Bash Bible - Array Operations

Reference: [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible)

Pure bash patterns for array manipulation without external tools.

## Array Declaration

```bash
# Indexed array
declare -a my_array=()
my_array=(element1 element2 element3)

# Associative array (Bash 4+)
declare -A my_hash=()
my_hash=([key1]=value1 [key2]=value2)
```

## Reverse an Array

Requires `shopt -s compat44` in Bash 5.0+:

```bash
reverse_array() {
    shopt -s extdebug
    f()(printf '%s\n' "${BASH_ARGV[@]}"); f "$@"
    shopt -u extdebug
}

# Usage
reverse_array 1 2 3 4 5        # Output: 5 4 3 2 1
arr=(red blue green)
reverse_array "${arr[@]}"      # Output: green blue red
```

## Remove Duplicate Elements

Requires Bash 4+:

```bash
remove_array_dups() {
    declare -A tmp_array
    for i in "$@"; do
        [[ $i ]] && IFS=" " tmp_array["${i:- }"]=1
    done
    printf '%s\n' "${!tmp_array[@]}"
}

# Usage
remove_array_dups 1 1 2 2 3 3 3  # Output: 1 2 3 (order may vary)
arr=(red red green blue blue)
remove_array_dups "${arr[@]}"    # Output: red green blue
```

## Random Array Element

```bash
random_array_element() {
    local arr=("$@")
    printf '%s\n' "${arr[RANDOM % $#]}"
}

# Usage
array=(red green blue yellow brown)
random_array_element "${array[@]}"   # Output: random element
random_array_element 1 2 3 4 5 6 7   # Works with arguments too
```

## Cycle Through Array

```bash
arr=(a b c d)

cycle() {
    printf '%s ' "${arr[${i:=0}]}"
    ((i=i>=${#arr[@]}-1?0:++i))
}

# Each call cycles to next element
cycle  # a
cycle  # b
cycle  # c
cycle  # d
cycle  # a (wraps around)
```

## Toggle Between Values

```bash
arr=(true false)

toggle() {
    printf '%s ' "${arr[${i:=0}]}"
    ((i=i>=${#arr[@]}-1?0:++i))
}

# Usage: toggles between true/false
toggle  # true
toggle  # false
toggle  # true
```

## Array Iteration Patterns

```bash
# Iterate over elements
arr=(apples oranges tomatoes)
for element in "${arr[@]}"; do
    printf '%s\n' "$element"
done

# Iterate with index
for i in "${!arr[@]}"; do
    printf '%d: %s\n' "$i" "${arr[i]}"
done

# C-style iteration
for ((i=0; i<${#arr[@]}; i++)); do
    printf '%s\n' "${arr[i]}"
done
```

## Safe Globbing for Arrays

```bash
# Enable nullglob to avoid literal patterns on no match
shopt -s nullglob
files=(*.txt)
shopt -u nullglob

# Check if array is empty
if [[ ${#files[@]} -eq 0 ]]; then
    printf 'No files found\n'
else
    printf 'Found %d files\n' "${#files[@]}"
fi
```

## Array Reference Table

| Operation        | Syntax                    |
| ---------------- | ------------------------- |
| All elements     | `"${arr[@]}"`             |
| All indices      | `"${!arr[@]}"`            |
| Array length     | `${#arr[@]}`              |
| Element at index | `${arr[i]}`               |
| Append element   | `arr+=(element)`          |
| Slice            | `"${arr[@]:start:count}"` |
| Element length   | `${#arr[i]}`              |
| Delete element   | `unset 'arr[i]'`          |

## Associative Array Patterns

```bash
declare -A config=()
config[host]="localhost"
config[port]="8080"
config[debug]="true"

# Check key exists
[[ -v config[host] ]] && printf 'Host: %s\n' "${config[host]}"

# Iterate over keys
for key in "${!config[@]}"; do
    printf '%s = %s\n' "$key" "${config[$key]}"
done

# Get all keys
keys=("${!config[@]}")

# Get all values
values=("${config[@]}")
```

## Array Slicing

```bash
arr=(a b c d e f g)

# Get elements from index 2 onward
printf '%s\n' "${arr[@]:2}"      # c d e f g

# Get 3 elements starting at index 2
printf '%s\n' "${arr[@]:2:3}"    # c d e

# Get last 3 elements
printf '%s\n' "${arr[@]: -3}"    # e f g
```

## Joining Array Elements

```bash
# Join with delimiter (IFS method)
join_by() {
    local IFS="$1"
    shift
    printf '%s\n' "$*"
}

arr=(a b c d)
join_by ',' "${arr[@]}"  # Output: a,b,c,d
join_by ' - ' "${arr[@]}"  # Output: a - b - c - d
```

## Array Contains Element

```bash
# Check if array contains element
array_contains() {
    local element="${1}"
    shift
    local arr=("$@")
    for item in "${arr[@]}"; do
        [[ "${item}" == "${element}" ]] && return 0
    done
    return 1
}

# Usage
colors=(red green blue)
array_contains "green" "${colors[@]}" && printf 'Found\n'
```
