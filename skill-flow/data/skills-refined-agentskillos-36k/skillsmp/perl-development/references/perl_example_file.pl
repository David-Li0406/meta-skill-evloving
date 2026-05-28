# --- Essential Pragmas ---
# These are the Perl equivalent of "set -euo pipefail" in Bash
use strict;    # Enforces strict variable declarations and rules
use warnings;  # Enables a wide range of helpful warnings
use autodie;   # Automatically dies on failed system calls (e.g., open)

# --- Standard Library Modules ---
use Getopt::Long qw(GetOptions); # For robust argument parsing
use Pod::Usage qw(pod2usage);   # For generating help from documentation
use Time::HiRes qw(time);       # For more precise timing
use Cwd qw(abs_path);
use File::Basename qw(basename dirname);

# --- Find and Include Local Modules ---
# This allows the script to find our custom App::Logger module
# when it's in the same directory as the script.
use FindBin;
use lib $FindBin::Bin;

# --- Custom Modules ---
# For simple scripts, you might inline logging functions
# For complex CLI tools, consider a dedicated logging module
use App::Logger qw(
    print_success
    print_error
    print_info
    print_debug
    print_warning
);

# --- Advanced CLI Tool Patterns ---
# Uncomment and modify these patterns for terminal/CLI applications

# Terminal detection and TTY handling
sub is_tty {
    return -t STDIN && -t STDOUT;
}

# Color support detection (respects NO_COLOR standard)
sub should_use_color {
    return 0 if $ENV{NO_COLOR};
    return 1 if $ENV{FORCE_COLOR};
    return is_tty() && ($ENV{TERM} // '') ne 'dumb';
}

# Command existence check (useful for tool compatibility)
sub command_exists {
    my ($cmd) = @_;
    my $result = `command -v "$cmd" 2>/dev/null`;
    return $? == 0;
}

# Safe system call with error handling
sub run_command {
    my ($cmd) = @_;
    my $output = `$cmd 2>&1`;
    my $exit_code = $? >> 8;
    return ($output, $exit_code);
}

# --- Critical Lessons from Complex CLI Development ---

# LESSON 1: Perl truthiness gotchas
# In Perl, "0" (string zero) evaluates to FALSE, which breaks color logic!
# Always use: (defined $var && $var ne '') instead of just: $var
sub safe_string_check {
    my ($value) = @_;
    return defined $value && $value ne '';
}

# LESSON 2: Terminal query handling with proper cleanup
sub query_terminal_safely {
    my ($query) = @_;
    return unless is_tty();

    # Save terminal state
    my $stty_save = `stty -g 2>/dev/null`;
    return unless $? == 0;
    chomp $stty_save;

    # Set raw mode and query
    system("stty raw -echo 2>/dev/null");
    print STDOUT $query;
    STDOUT->flush();

    # Read response with timeout (non-blocking)
    require IO::Select;
    my $select = IO::Select->new(\*STDIN);
    my $response = '';
    my $timeout = 0.05;  # 50ms

    if ($select->can_read($timeout)) {
        sysread(STDIN, $response, 1024);
    }

    # CRITICAL: Always restore terminal state
    system("stty $stty_save 2>/dev/null");
    return $response;
}

# LESSON 3: CSS-style value parsing (1-4 values)
sub parse_css_values {
    my ($value_string) = @_;
    return (0, 0, 0, 0) unless $value_string;

    my @values = split /\s+/, $value_string;

    if (@values == 1) {
        # "2" -> all sides = 2
        return ($values[0]) x 4;
    } elsif (@values == 2) {
        # "2 3" -> vertical=2, horizontal=3
        return ($values[0], $values[1], $values[0], $values[1]);
    } elsif (@values == 3) {
        # "1 2 3" -> top=1, horizontal=2, bottom=3
        return ($values[0], $values[1], $values[2], $values[1]);
    } elsif (@values == 4) {
        # "1 2 3 4" -> top=1, right=2, bottom=3, left=4
        return @values;
    }

    return (0, 0, 0, 0);
}

# LESSON 4: Efficient ANSI escape sequence building
sub build_ansi_color {
    my ($fg, $bg) = @_;
    my @codes = ();

    if (defined $fg && $fg ne '') {
        if ($fg =~ /^\d+$/ && $fg >= 0 && $fg <= 255) {
            push @codes, "38;5;$fg";
        }
    }

    if (defined $bg && $bg ne '') {
        if ($bg =~ /^\d+$/ && $bg >= 0 && $bg <= 255) {
            # Special case: "0" should use ANSI black (40) not 256-color (48;5;0)
            if ($bg eq '0') {
                push @codes, "40";
            } else {
                push @codes, "48;5;$bg";
            }
        }
    }

    return @codes ? "\e[" . join(';', @codes) . "m" : '';
}

# --- Script Metadata (Constants) ---
use constant {
    SCRIPT_NAME    => basename($0),
    SCRIPT_VERSION => "1.0.0",
};

# --- Main Program Logic ---
sub main {
    my $start_time = time();

    # --- Argument Parsing ---
    my ($help, $version, $debug);
    GetOptions(
        'help|h'    => \$help,
        'version|v' => \$version,
        'debug|d'   => \$debug,
    ) or pod2usage(2);

    # Handle --help and --version flags
    pod2usage(-exitval => 0, -verbose => 1) if $help;
    if ($version) {
        printf "%s version %s\n", SCRIPT_NAME, SCRIPT_VERSION;
        exit 0;
    }

    # --- Validate Arguments ---
    pod2usage(-message => "Missing required argument <file>", -exitval => 1) if @ARGV < 1;
    my $file_argument = $ARGV[0];

    # --- Main Logic ---
    print_info(sprintf("Starting %s...", SCRIPT_NAME));

    if ($debug) {
        print_debug("Debug mode enabled.");
        print_debug("File argument: $file_argument");
    }

    # --- Example Usage Patterns ---

    # Check if a command exists (useful for drop-in replacements)
    if (command_exists('ls')) {
        print_info("'ls' command found.");
    } else {
        print_warning("'ls' command not found.");
    }

    # Terminal/TTY detection example
    if (is_tty()) {
        print_info("Running in terminal context");
        if (should_use_color()) {
            print_info("\e[32mColor output enabled\e[0m");
        }
    } else {
        print_info("Running in non-interactive context");
    }

    # Command dispatcher pattern (for multi-command tools)
    # my %commands = (
    #     'command1' => \&handle_command1,
    #     'command2' => \&handle_command2,
    # );
    # if (exists $commands{$subcommand}) {
    #     $commands{$subcommand}->(@remaining_args);
    # }

    print_success("Script completed successfully.");
    my $end_time = time();
    my $duration = $end_time - $start_time;

    print_info(sprintf("Script completed in %.4f seconds", $duration)) if $debug;

    return 0;
}

# --- Run Main Function ---
# Use an eval block to catch any explicit 'die' calls for a graceful exit
eval { main(@ARGV) };
if ($@) {
    # The $@ variable contains the error message from 'die'
    my $error = $@;
    $error =~ s/ at \S+ line \d+\.?\n?$//; # Clean up file/line info from error
    print_error($error);
    exit 1;
}

# --- Documentation (POD) ---
# This block is used by Pod::Usage to generate the --help message.
__END__

=head1 NAME

perl_example_file.pl - A boilerplate for modern Perl scripts.

=head1 SYNOPSIS

B<perl_example_file.pl> [OPTIONS] <argument>

=head1 DESCRIPTION

A brief description of what this script does. This template provides a robust starting point for developing modern, secure, and maintainable Perl scripts.

This template includes patterns for:
- Terminal/TTY detection and color handling
- Command existence checking
- Safe system call execution
- Multi-command dispatching
- Proper error handling and cleanup

Advanced CLI patterns included:
- Safe terminal querying with proper state restoration
- CSS-style value parsing (1-4 value formats)
- Perl truthiness gotcha handling ("0" string issue)
- Efficient ANSI escape sequence building
- Non-blocking I/O with timeouts

For complex CLI tools, study the utility functions for production-ready patterns.

=head1 OPTIONS

=over 4

=item B<-h>, B<--help>

Show this help message and exit.

=item B<-v>, B<--version>

Show version information and exit.

=item B<-d>, B<--debug>

Enable debug mode for verbose output.

=back

=head1 EXAMPLES

    # Run with a required argument
    perl perl_example_file.pl file.txt

    # Run in debug mode
    perl perl_example_file.pl --debug file.txt

=cut
