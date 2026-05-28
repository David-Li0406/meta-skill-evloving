# Perl Truthiness Gotchas

Perl's truthiness rules differ from other languages and cause subtle bugs. This reference documents common pitfalls and correct patterns.

## The "0" String Problem

In Perl, the string `"0"` evaluates to FALSE:

```perl
my $value = "0";

# WRONG - treats "0" as false
if ($value) {
    # This block NEVER executes when $value is "0"
    process($value);
}

# CORRECT - explicit check
if (defined $value && $value ne '') {
    process($value);  # Executes for "0"
}
```

### Real-World Impact

This commonly breaks color/option handling in CLI tools:

```perl
# Color code 0 = black in 256-color palette
my $bg_color = "0";

# WRONG - black background never applied
my $style = $bg_color ? "48;5;$bg_color" : '';

# CORRECT - explicit string check
my $style = (defined $bg_color && $bg_color ne '')
    ? "48;5;$bg_color"
    : '';
```

## Truthiness Rules

| Value                 | Boolean | Notes              |
| --------------------- | ------- | ------------------ |
| `undef`               | FALSE   | Undefined          |
| `""` (empty string)   | FALSE   | Empty              |
| `"0"` (string zero)   | FALSE   | Common gotcha      |
| `0` (numeric zero)    | FALSE   | Expected           |
| `"0.0"`               | TRUE    | Only "0" is false  |
| `" "` (whitespace)    | TRUE    | Non-empty string   |
| `"false"`             | TRUE    | Any non-"0" string |
| `[]` (empty arrayref) | TRUE    | Reference exists   |
| `{}` (empty hashref)  | TRUE    | Reference exists   |

## Safe Checking Patterns

### Check for defined and non-empty

```perl
sub has_value {
    my ($val) = @_;
    return defined $val && $val ne '';
}

# Usage
if (has_value($input)) {
    process($input);
}
```

### Check for defined only

```perl
# When "0" and "" are valid values
if (defined $value) {
    process($value);
}
```

### Numeric value check

```perl
use Scalar::Util qw(looks_like_number);

if (defined $value && looks_like_number($value)) {
    my $num = $value + 0;  # Safe numeric conversion
}
```

## Default Value Patterns

### The // operator (defined-or)

```perl
# Uses default only if undefined (not for "0" or "")
my $port = $config->{port} // 8080;

# WRONG for optional values that might be "0"
my $verbosity = $options{verbose} || 1;  # "0" becomes 1

# CORRECT
my $verbosity = defined $options{verbose} ? $options{verbose} : 1;
```

### Three-way default

```perl
sub get_setting {
    my ($value, $default) = @_;
    return $default unless defined $value;
    return $default if $value eq '';
    return $value;
}
```

## Array and Hash Truthiness

### Empty collections are still references

```perl
my @empty_array = ();
my %empty_hash = ();
my $arrayref = [];
my $hashref = {};

# These are all TRUE (references exist)
if ($arrayref) { }  # TRUE - ref exists
if ($hashref) { }   # TRUE - ref exists

# Check for empty
if (@$arrayref) { }      # FALSE - array is empty
if (keys %$hashref) { }  # FALSE - hash is empty
if (@empty_array) { }    # FALSE - array is empty
if (%empty_hash) { }     # FALSE - hash is empty (5.26+)
```

### Array in scalar context

```perl
my @items = (1, 2, 3);

# Scalar context gives count
my $count = @items;     # 3
if (@items) { }         # TRUE if non-empty
if (@items > 0) { }     # Explicit count check
```

## Function Return Values

### Boolean returns

```perl
# WRONG - "0" return treated as failure
sub find_index {
    my ($item, @list) = @_;
    for my $i (0 .. $#list) {
        return $i if $list[$i] eq $item;
    }
    return;  # undef for not found
}

# Check with defined, not truthiness
my $idx = find_index('target', @data);
if (defined $idx) {
    say "Found at index $idx";  # Works for index 0
}
```

### Wantarray context

```perl
sub get_data {
    my @data = fetch_all();
    return wantarray ? @data : \@data;
}

my @list = get_data();    # Array
my $ref = get_data();     # Arrayref
```

## Command-Line Option Gotchas

### Getopt::Long with boolean flags

```perl
use Getopt::Long;

my $verbose;
GetOptions('verbose!' => \$verbose);

# $verbose is:
# - undef if not specified
# - 1 if --verbose
# - 0 if --no-verbose

# WRONG - treats --no-verbose same as unspecified
if ($verbose) { }

# CORRECT - distinguish all three states
if (defined $verbose && $verbose) {
    # Explicitly enabled
}
elsif (defined $verbose && !$verbose) {
    # Explicitly disabled
}
else {
    # Not specified - use default
}
```

## Best Practices Summary

1. **Always use `defined` check** before truthiness when "0" is valid
2. **Use `//` for defaults** when only `undef` should trigger default
3. **Use explicit comparisons** for numeric bounds: `$val >= 0` not `$val`
4. **Check array/hash length** not reference existence: `@$ref` not `$ref`
5. **Document expected values** in subroutine POD
6. **Test edge cases** including 0, "0", "", and undef
