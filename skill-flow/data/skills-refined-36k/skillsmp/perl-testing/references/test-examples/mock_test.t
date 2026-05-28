# Example Test::MockModule usage
# t/mock.t

use strict;
use warnings;
use Test::More;

# Check if Test::MockModule is available
BEGIN {
    eval { require Test::MockModule };
    if ($@) {
        plan skip_all => 'Test::MockModule not installed';
    }
}

use Test::MockModule;

# === Mock Module for Testing ===

# Define a module to mock
package MyApp::Database {
    sub new { bless {}, shift }
    sub connect { return "real_connection" }
    sub query { return [{ id => 1, name => 'Real Data' }] }
    sub save { return 1 }
    sub disconnect { return 1 }
}

package MyApp::Service {
    sub new {
        my ($class, $db) = @_;
        $db //= MyApp::Database->new;
        return bless { db => $db }, $class;
    }

    sub get_users {
        my ($self) = @_;
        return $self->{db}->query("SELECT * FROM users");
    }

    sub create_user {
        my ($self, $data) = @_;
        return $self->{db}->save($data);
    }
}

package main;

# === Basic Mocking ===

subtest 'basic mock' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    # Replace connect method
    $mock->mock('connect', sub { return 'mock_connection' });

    my $db = MyApp::Database->new;
    is($db->connect, 'mock_connection', 'mocked connect returns mock value');
};

subtest 'mock with custom return' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    # Return specific test data
    $mock->mock('query', sub {
        return [
            { id => 1, name => 'Test User 1' },
            { id => 2, name => 'Test User 2' },
        ];
    });

    my $db = MyApp::Database->new;
    my $results = $db->query("SELECT * FROM users");

    is(scalar @$results, 2, 'mock returns two records');
    is($results->[0]{name}, 'Test User 1', 'first record correct');
};

# === Tracking Calls ===

subtest 'track method calls' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');
    my @calls;

    # Track what arguments are passed
    $mock->mock('save', sub {
        my ($self, $data) = @_;
        push @calls, $data;
        return 1;
    });

    my $service = MyApp::Service->new;
    $service->create_user({ name => 'Alice' });
    $service->create_user({ name => 'Bob' });

    is(scalar @calls, 2, 'save called twice');
    is($calls[0]->{name}, 'Alice', 'first call was Alice');
    is($calls[1]->{name}, 'Bob', 'second call was Bob');
};

subtest 'count method calls' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');
    my $call_count = 0;

    $mock->mock('query', sub {
        $call_count++;
        return [];
    });

    my $service = MyApp::Service->new;
    $service->get_users;
    $service->get_users;
    $service->get_users;

    is($call_count, 3, 'query called three times');
};

# === Conditional Mocking ===

subtest 'conditional mock behavior' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    $mock->mock('query', sub {
        my ($self, $sql) = @_;

        if ($sql =~ /users/) {
            return [{ id => 1, type => 'user' }];
        }
        elsif ($sql =~ /orders/) {
            return [{ id => 1, type => 'order' }];
        }
        return [];
    });

    my $db = MyApp::Database->new;

    my $users = $db->query("SELECT * FROM users");
    is($users->[0]{type}, 'user', 'users query returns user data');

    my $orders = $db->query("SELECT * FROM orders");
    is($orders->[0]{type}, 'order', 'orders query returns order data');
};

# === Restoring Original ===

subtest 'restore original method' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    # Get original value first
    my $db_before = MyApp::Database->new;
    my $original = $db_before->connect;

    # Mock it
    $mock->mock('connect', sub { return 'mocked' });
    is(MyApp::Database->new->connect, 'mocked', 'mock is active');

    # Unmock specific method
    $mock->unmock('connect');
    is(MyApp::Database->new->connect, $original, 'original restored');
};

subtest 'automatic restore on scope exit' => sub {
    my $db = MyApp::Database->new;

    {
        my $mock = Test::MockModule->new('MyApp::Database');
        $mock->mock('connect', sub { return 'scoped_mock' });
        is($db->connect, 'scoped_mock', 'mock active in scope');
    }

    # Mock automatically removed when $mock goes out of scope
    is($db->connect, 'real_connection', 'original restored after scope');
};

# === Mocking Constructors ===

subtest 'mock constructor' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    my $fake_db = bless { fake => 1 }, 'MyApp::Database';
    $mock->mock('new', sub { return $fake_db });

    my $db = MyApp::Database->new;
    ok($db->{fake}, 'got fake database instance');
};

# === Error Simulation ===

subtest 'simulate errors' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');

    # Simulate connection failure
    $mock->mock('connect', sub {
        die "Connection refused";
    });

    my $db = MyApp::Database->new;

    use Test::Exception;
    throws_ok { $db->connect } qr/Connection refused/,
        'connection failure simulated';
};

subtest 'simulate intermittent failures' => sub {
    my $mock = Test::MockModule->new('MyApp::Database');
    my $attempt = 0;

    $mock->mock('connect', sub {
        $attempt++;
        die "Connection failed" if $attempt < 3;
        return 'connected';
    });

    my $db = MyApp::Database->new;

    use Test::Exception;
    dies_ok { $db->connect } 'first attempt fails';
    dies_ok { $db->connect } 'second attempt fails';
    lives_ok { $db->connect } 'third attempt succeeds';
};

done_testing();

__END__

=head1 NAME

mock.t - Test::MockModule example tests

=head1 DESCRIPTION

Demonstrates mocking patterns with Test::MockModule:

=over 4

=item * Basic method mocking

=item * Tracking method calls

=item * Conditional mock behavior

=item * Restoring original methods

=item * Scope-based mocking

=item * Error simulation

=back

=head1 USAGE

    prove -v t/mock.t

=cut
