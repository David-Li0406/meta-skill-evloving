# Pure Bash Bible - File Operations

Reference: [pure-bash-bible](https://github.com/dylanaraps/pure-bash-bible)

Pure bash alternatives to file processing commands like cat, head, tail, wc, basename, and dirname.

**Note:** Bash versions < 4.4 have issues handling binary data.

## Read File to String

Alternative to `cat`:

```bash
file_data="$(<"file")"

# With error checking
if [[ -r "${file}" ]]; then
    content="$(<"${file}")"
fi
```

## Read File to Array (by line)

```bash
# Bash <4 (discarding empty lines)
IFS=$'\n' read -d "" -ra file_data < "file"

# Bash <4 (preserving empty lines)
while read -r line; do
    file_data+=("$line")
done < "file"

# Bash 4+
mapfile -t file_data < "file"
```

## Get First N Lines (head alternative)

Requires Bash 4+:

```bash
head() {
    mapfile -tn "$1" line < "$2"
    printf '%s\n' "${line[@]}"
}

# Usage
head 2 ~/.bashrc       # First 2 lines
head 10 /etc/passwd    # First 10 lines
```

## Get Last N Lines (tail alternative)

Requires Bash 4+:

```bash
tail() {
    mapfile -tn 0 line < "$2"
    printf '%s\n' "${line[@]: -$1}"
}

# Usage
tail 2 ~/.bashrc       # Last 2 lines
tail 10 /var/log/syslog
```

## Count Lines in File (wc -l alternative)

```bash
# Bash 4+ (mapfile)
lines() {
    mapfile -tn 0 lines < "$1"
    printf '%s\n' "${#lines[@]}"
}

# Bash 3 (slower for large files)
lines_loop() {
    local count=0
    while IFS= read -r _; do
        ((count++))
    done < "$1"
    printf '%s\n' "$count"
}

# Usage
lines ~/.bashrc  # Output: number of lines
```

## Count Files in Directory

```bash
count() {
    printf '%s\n' "$#"
}

# Usage
count ~/Downloads/*      # Count all files
count ~/Downloads/*/     # Count directories only
count ~/Pictures/*.jpg   # Count specific type
```

## Create Empty File (touch alternative)

```bash
# Shortest
>file

# Alternatives
:>file
echo -n >file
printf '' >file
```

## Extract Lines Between Markers

````bash
extract() {
    # Usage: extract file "opening marker" "closing marker"
    while IFS=$'\n' read -r line; do
        [[ $extract && $line != "$3" ]] &&
            printf '%s\n' "$line"
        [[ $line == "$2" ]] && extract=1
        [[ $line == "$3" ]] && extract=
    done < "$1"
}

# Usage: Extract code blocks from markdown
extract README.md '```bash' '```'
````

## Get Directory Name (dirname alternative)

```bash
dirname() {
    local tmp=${1:-.}
    [[ $tmp != *[!/]* ]] && { printf '/\n'; return; }
    tmp=${tmp%%"${tmp##*[!/]}"}
    [[ $tmp != */* ]] && { printf '.\n'; return; }
    tmp=${tmp%/*}
    tmp=${tmp%%"${tmp##*[!/]}"}
    printf '%s\n' "${tmp:-/}"
}

# Usage
dirname ~/Pictures/Wallpapers/1.jpg  # /home/user/Pictures/Wallpapers
dirname ~/Pictures/Downloads/        # /home/user/Pictures
```

## Get Basename (basename alternative)

```bash
basename() {
    local tmp
    tmp=${1%"${1##*[!/]}"}
    tmp=${tmp##*/}
    tmp=${tmp%"${2/"$tmp"}"}
    printf '%s\n' "${tmp:-/}"
}

# Usage
basename ~/Pictures/Wallpapers/1.jpg       # 1.jpg
basename ~/Pictures/Wallpapers/1.jpg .jpg  # 1
basename ~/Pictures/Downloads/             # Downloads
```

## File Iteration Patterns

```bash
# All files (greedy)
for file in *; do
    printf '%s\n' "$file"
done

# Specific extension
for file in ~/Pictures/*.png; do
    printf '%s\n' "$file"
done

# Directories only
for dir in ~/Downloads/*/; do
    printf '%s\n' "$dir"
done

# Multiple paths with brace expansion
for file in /path/to/parentdir/{file1,file2,subdir/file3}; do
    printf '%s\n' "$file"
done

# Recursive (requires globstar)
shopt -s globstar
for file in ~/Pictures/**/*; do
    printf '%s\n' "$file"
done
shopt -u globstar
```

## Loop Over File Contents

```bash
# Standard line-by-line
while read -r line; do
    printf '%s\n' "$line"
done < "file"

# With IFS preservation for leading/trailing whitespace
while IFS= read -r line; do
    printf '%s\n' "$line"
done < "file"

# Handle files without trailing newline
while IFS= read -r line || [[ -n "$line" ]]; do
    printf '%s\n' "$line"
done < "file"
```

## File Conditionals Reference

| Test      | Description                   |
| --------- | ----------------------------- |
| `-e file` | File exists                   |
| `-f file` | Regular file exists           |
| `-d file` | Directory exists              |
| `-r file` | File is readable              |
| `-w file` | File is writable              |
| `-x file` | File is executable            |
| `-s file` | File size > 0                 |
| `-L file` | File is symbolic link         |
| `-h file` | File is symbolic link         |
| `-p file` | File is named pipe (FIFO)     |
| `-S file` | File is socket                |
| `-b file` | File is block special         |
| `-c file` | File is character special     |
| `-N file` | File modified since last read |

## File Comparison

| Test              | Description            |
| ----------------- | ---------------------- |
| `file1 -ef file2` | Same inode and device  |
| `file1 -nt file2` | file1 newer than file2 |
| `file1 -ot file2` | file1 older than file2 |

## Safe Temporary Files

```bash
# Create temp file
temp_file=$(mktemp)

# Create temp directory
temp_dir=$(mktemp -d)

# Cleanup on exit
trap 'rm -rf "${temp_file}" "${temp_dir}"' EXIT

# Use temp file
printf '%s\n' "data" > "${temp_file}"
```

## Read Without External Commands

```bash
# Read first line
IFS= read -r first_line < file

# Read specific line number
get_line() {
    local i=0
    while IFS= read -r line; do
        ((i++))
        ((i == $1)) && { printf '%s\n' "$line"; return; }
    done < "$2"
}

# Usage
get_line 5 /etc/passwd  # Get line 5
```
