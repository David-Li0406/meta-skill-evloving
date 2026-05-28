# Example Test::Exception usage
# t/exception.t

use strict;
use warnings;
use Test::More;
use Test::Exception;

# === Testing Code That Should Die ===

subtest 'dies_ok examples' => sub {
    # Simple die
    dies_ok { die "An error occurred" } 'die causes death';

    # Division by zero
    dies_ok { my $x = 1/0 } 'division by zero dies';

    # Croak from Carp
    use Carp;
    dies_ok { croak "Something went wrong" } 'croak causes death';
};

subtest 'throws_ok with pattern' => sub {
    # Match error message with regex
    throws_ok {
        die "Invalid argument: foo";
    } qr/Invalid argument/, 'throws with expected message';

    # Case insensitive matching
    throws_ok {
        die "CONNECTION REFUSED";
    } qr/connection refused/i, 'case insensitive match';
};

subtest 'throws_ok with exception class' => sub {
    # Define a simple exception class
    package MyApp::Error {
        sub new { bless { message => $_[1] }, $_[0] }
        sub throw { die $_[0]->new($_[1]) }
    }

    # Test throwing exception object
    throws_ok {
        MyApp::Error->throw("Database error");
    } 'MyApp::Error', 'throws correct exception class';
};

# === Testing Code That Should Live ===

subtest 'lives_ok examples' => sub {
    # Simple successful operation
    lives_ok { my $x = 1 + 1 } 'addition lives';

    # Function that should not die
    sub safe_operation { return 42 }
    lives_ok { safe_operation() } 'safe operation lives';

    # Even with edge cases
    lives_ok { my @empty = (); scalar @empty } 'empty array operations live';
};

subtest 'lives_and examples' => sub {
    # Test both living and returning correct value
    lives_and {
        is(2 + 2, 4)
    } 'calculation lives and returns correct value';

    # With array operations
    lives_and {
        my @items = (1, 2, 3);
        is(scalar @items, 3);
    } 'array operation lives and has correct count';
};

# === Practical Examples ===

subtest 'testing validation' => sub {
    # Simulated validation function
    sub validate_email {
        my ($email) = @_;
        die "Email required" unless defined $email;
        die "Invalid email format" unless $email =~ /@/;
        return 1;
    }

    # Test missing email
    throws_ok { validate_email(undef) }
        qr/Email required/, 'missing email throws';

    # Test invalid format
    throws_ok { validate_email('not-an-email') }
        qr/Invalid email format/, 'invalid format throws';

    # Test valid email
    lives_ok { validate_email('user@example.com') }
        'valid email lives';
};

subtest 'testing file operations' => sub {
    use File::Temp qw(tempfile);

    # Test opening non-existent file
    throws_ok {
        open my $fh, '<', '/nonexistent/file/path.txt' or die $!;
    } qr/No such file/, 'opening missing file throws';

    # Test successful file operations
    my ($fh, $filename) = tempfile(UNLINK => 1);
    lives_ok {
        print $fh "test content";
        close $fh;
    } 'writing to temp file lives';
};

subtest 'testing constructor validation' => sub {
    # Mock class with validation
    package MyApp::User {
        sub new {
            my ($class, %args) = @_;
            die "name required" unless $args{name};
            die "email required" unless $args{email};
            return bless \%args, $class;
        }
    }

    # Test missing required fields
    throws_ok { MyApp::User->new() }
        qr/name required/, 'missing name throws';

    throws_ok { MyApp::User->new(name => 'Test') }
        qr/email required/, 'missing email throws';

    # Test successful creation
    lives_ok {
        MyApp::User->new(name => 'Test', email => 'test@example.com')
    } 'valid constructor lives';
};

done_testing();

__END__

=head1 NAME

exception.t - Test::Exception example tests

=head1 DESCRIPTION

Demonstrates Test::Exception patterns:

=over 4

=item * dies_ok - verify code dies

=item * throws_ok - verify specific exception

=item * lives_ok - verify code doesn't die

=item * lives_and - combine living with assertions

=back

=head1 USAGE

    prove -v t/exception.t

=cut
