# Modern Perl Modules Reference

Recommended CPAN modules for modern Perl development, organized by category.

## File and Path Operations

| Module           | Purpose                     | Example                        |
| ---------------- | --------------------------- | ------------------------------ |
| Path::Tiny       | Modern file/path operations | `path($file)->slurp_utf8`      |
| File::Spec       | Portable path manipulation  | `File::Spec->catfile(@parts)`  |
| File::Find::Rule | Declarative file finding    | `find(file => name => '*.pl')` |
| File::Temp       | Secure temporary files      | `tempfile(UNLINK => 1)`        |

```perl
use Path::Tiny;

my $file = path('data/config.yaml');
my $content = $file->slurp_utf8;
my @lines = $file->lines_utf8({ chomp => 1 });

$file->parent->mkpath;
$file->spew_utf8($new_content);
```

## Data Structures

| Module          | Purpose           | Example                   |
| --------------- | ----------------- | ------------------------- |
| Hash::Merge     | Deep hash merging | `merge($hash1, $hash2)`   |
| List::Util      | List utilities    | `first { $_ > 10 } @list` |
| List::MoreUtils | Extended list ops | `uniq @items`             |
| Scalar::Util    | Scalar utilities  | `looks_like_number($val)` |

```perl
use List::Util qw(first any all none sum max min);
use List::MoreUtils qw(uniq zip);

my $found = first { $_->{active} } @records;
my $total = sum map { $_->{amount} } @items;
my @unique = uniq @values;
```

## Object-Oriented Programming

| Module     | Purpose             | Style                      |
| ---------- | ------------------- | -------------------------- |
| Moo        | Lightweight OO      | Recommended for most cases |
| Moose      | Full-featured OO    | Complex applications       |
| Mouse      | Middle-ground OO    | Moose-compatible, lighter  |
| Role::Tiny | Roles without Moose | Standalone roles           |

```perl
package MyApp::Config;
use Moo;
use Types::Standard qw(Str Int Bool);

has 'name' => (is => 'ro', isa => Str, required => 1);
has 'port' => (is => 'rw', isa => Int, default => 8080);
has 'debug' => (is => 'ro', isa => Bool, default => 0);

sub connect {
    my ($self) = @_;
    # implementation
}

1;
```

## Error Handling

| Module    | Purpose                   | Pattern             |
| --------- | ------------------------- | ------------------- |
| Try::Tiny | try/catch blocks          | `try { } catch { }` |
| autodie   | Auto-exception on failure | `use autodie;`      |
| Carp      | Better error messages     | `croak "message"`   |

```perl
use Try::Tiny;
use Carp qw(croak carp);

try {
    process_file($file);
}
catch {
    carp "Warning: $_";
};

croak "Configuration required" unless defined $config;
```

## HTTP and Web

| Module          | Purpose          | Use Case         |
| --------------- | ---------------- | ---------------- |
| HTTP::Tiny      | Lightweight HTTP | Simple requests  |
| LWP::UserAgent  | Full HTTP client | Complex needs    |
| Mojo::UserAgent | Async HTTP       | Mojolicious apps |
| URI             | URL manipulation | Building URLs    |

```perl
use HTTP::Tiny;
use JSON::PP;

my $http = HTTP::Tiny->new(timeout => 30);
my $response = $http->get('https://api.example.com/data');

if ($response->{success}) {
    my $data = decode_json($response->{content});
}
```

## JSON and Data Formats

| Module           | Purpose        | Notes               |
| ---------------- | -------------- | ------------------- |
| JSON::PP         | Pure Perl JSON | Core module (5.14+) |
| JSON::XS         | Fast JSON      | Requires C compiler |
| Cpanel::JSON::XS | Safer JSON::XS | Recommended         |
| YAML::XS         | Fast YAML      | Production use      |
| YAML::Tiny       | Pure Perl YAML | Simple cases        |

```perl
use JSON::PP;  # or Cpanel::JSON::XS

my $json = JSON::PP->new->utf8->pretty;
my $data = $json->decode($json_string);
my $output = $json->encode($hash_ref);
```

## Logging

| Module        | Purpose               | Notes                 |
| ------------- | --------------------- | --------------------- |
| Log::Any      | Universal logging API | Adapter-based         |
| Log::Log4perl | Full-featured logging | Configuration-based   |
| Log::Dispatch | Flexible outputs      | Multiple destinations |

```perl
use Log::Any qw($log);
use Log::Any::Adapter ('Stderr');

$log->info("Processing started");
$log->warning("Config file missing, using defaults");
$log->error("Failed to connect: $!");
```

## Testing

| Module           | Purpose           | Standard           |
| ---------------- | ----------------- | ------------------ |
| Test::More       | Basic testing     | Core testing       |
| Test::Class      | xUnit-style       | Class-based tests  |
| Test::Deep       | Deep comparisons  | Complex structures |
| Test::Exception  | Exception testing | die/croak tests    |
| Test::MockModule | Mocking           | Override subs      |

See **perl-testing** skill for comprehensive testing guidance.

## Database

| Module        | Purpose            | Notes            |
| ------------- | ------------------ | ---------------- |
| DBI           | Database interface | Standard         |
| DBIx::Class   | ORM                | Complex apps     |
| DBIx::Simple  | Simple queries     | Quick scripts    |
| SQL::Abstract | SQL building       | Programmatic SQL |

```perl
use DBI;

my $dbh = DBI->connect(
    "dbi:SQLite:dbname=app.db",
    "", "",
    { RaiseError => 1, AutoCommit => 1 }
);

my $sth = $dbh->prepare("SELECT * FROM users WHERE active = ?");
$sth->execute(1);

while (my $row = $sth->fetchrow_hashref) {
    say $row->{name};
}
```

## Configuration

| Module       | Purpose          | Format            |
| ------------ | ---------------- | ----------------- |
| Config::Tiny | INI files        | Simple config     |
| Config::YAML | YAML config      | Structured config |
| Config::JSON | JSON config      | Web-friendly      |
| AppConfig    | Command + config | CLI apps          |

```perl
use Config::Tiny;

my $config = Config::Tiny->read('app.ini');
my $database = $config->{database}{host};
my $port = $config->{database}{port} // 5432;
```

## Terminal and CLI

| Module          | Purpose           | Use Case       |
| --------------- | ----------------- | -------------- |
| Term::ANSIColor | Colored output    | User feedback  |
| Term::ReadLine  | Interactive input | CLI tools      |
| IO::Interactive | TTY detection     | Output control |
| Text::Table     | Formatted tables  | Data display   |

```perl
use Term::ANSIColor qw(colored);
use IO::Interactive qw(is_interactive);

if (is_interactive) {
    say colored(['green'], 'Success!');
} else {
    say 'Success!';  # No colors in pipes
}
```

## Date and Time

| Module       | Purpose        | Notes           |
| ------------ | -------------- | --------------- |
| Time::Piece  | Core date/time | Core module     |
| DateTime     | Full-featured  | Heavy, powerful |
| Time::Moment | Fast datetime  | Lightweight     |

```perl
use Time::Piece;

my $now = localtime;
say $now->strftime('%Y-%m-%d %H:%M:%S');

my $parsed = Time::Piece->strptime('2024-01-15', '%Y-%m-%d');
```

## Process and System

| Module              | Purpose              | Notes               |
| ------------------- | -------------------- | ------------------- |
| IPC::System::Simple | Safe system calls    | Avoid shell         |
| IPC::Run            | Full process control | Pipes, PTY          |
| Proc::Daemon        | Daemonize            | Background services |

```perl
use IPC::System::Simple qw(capture capturex system);

# Safe - no shell interpolation
my $output = capturex('git', 'status', '--porcelain');

# With shell (when needed)
my $result = capture('ls -la | grep .pl');
```

## Installation

Install modules using cpanm:

```bash
cpanm Path::Tiny Try::Tiny Moo JSON::PP HTTP::Tiny
```

For environment setup, see the **perl-cpan-ecosystem** skill.
