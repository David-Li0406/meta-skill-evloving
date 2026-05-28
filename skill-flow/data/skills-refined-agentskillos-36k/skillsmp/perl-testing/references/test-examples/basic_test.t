# Example Test::More test file
# t/basic.t

use strict;
use warnings;
use Test::More;
use FindBin;
use lib "$FindBin::Bin/../lib";

# Example module to test (replace with your module)
# use MyApp::Calculator;

# Test planning - choose one approach:
# Option 1: Declare count upfront
# use Test::More tests => 10;

# Option 2: Count at end (preferred for flexibility)
# done_testing(); at the end

# === Basic Assertions ===

subtest 'boolean tests' => sub {
    ok(1, 'truth is true');
    ok(!0, 'zero is false');
    ok('string', 'non-empty string is true');
    ok(!undef, 'undef is false');
};

subtest 'equality tests' => sub {
    # String equality
    is('hello', 'hello', 'strings are equal');
    isnt('hello', 'world', 'strings are different');

    # Numeric comparison
    cmp_ok(42, '==', 42, 'numbers are equal');
    cmp_ok(10, '>', 5, '10 is greater than 5');
    cmp_ok(3, '<=', 5, '3 is less than or equal to 5');
};

subtest 'pattern matching' => sub {
    my $string = 'Hello, World!';

    like($string, qr/World/, 'string contains World');
    like($string, qr/^Hello/, 'string starts with Hello');
    unlike($string, qr/Goodbye/, 'string does not contain Goodbye');

    # Case insensitive
    like($string, qr/hello/i, 'case insensitive match');
};

subtest 'data structures' => sub {
    my @got = (1, 2, 3);
    my @expected = (1, 2, 3);
    is_deeply(\@got, \@expected, 'arrays match');

    my %got_hash = (a => 1, b => 2);
    my %expected_hash = (a => 1, b => 2);
    is_deeply(\%got_hash, \%expected_hash, 'hashes match');

    # Nested structures
    my $complex = { items => [1, 2, 3], meta => { count => 3 } };
    is_deeply(
        $complex,
        { items => [1, 2, 3], meta => { count => 3 } },
        'complex structure matches'
    );
};

subtest 'object tests' => sub {
    # Mock object for demonstration
    my $obj = bless {}, 'MyApp::Example';

    isa_ok($obj, 'MyApp::Example', 'object is correct class');

    # Check for methods (would fail without actual methods)
    # can_ok($obj, 'new', 'process', 'save');
};

subtest 'diagnostics example' => sub {
    my $value = 42;

    # diag() only shows on failure or with verbose
    is($value, 42, 'value is correct')
        or diag("Got unexpected value: $value");

    # note() always shows with verbose
    note("Testing with value: $value");
};

subtest 'skip example' => sub {
    SKIP: {
        # Skip if condition not met
        my $has_feature = 0;  # Toggle to test
        skip "Feature not available", 2 unless $has_feature;

        ok(1, 'feature test 1');
        ok(1, 'feature test 2');
    }
};

subtest 'todo example' => sub {
    TODO: {
        local $TODO = "Feature not yet implemented";

        # These tests are expected to fail
        # ok(new_feature(), 'new feature works');

        # Mark as pass for now
        pass('placeholder for future test');
    }
};

# === Cleanup ===

done_testing();

__END__

=head1 NAME

basic.t - Basic Test::More example tests

=head1 DESCRIPTION

Demonstrates common Test::More patterns including:

=over 4

=item * Boolean assertions with ok()

=item * Equality with is(), isnt(), cmp_ok()

=item * Pattern matching with like(), unlike()

=item * Data structures with is_deeply()

=item * Object testing with isa_ok(), can_ok()

=item * Subtests for organization

=item * SKIP and TODO blocks

=back

=head1 USAGE

    prove -v t/basic.t

=cut
