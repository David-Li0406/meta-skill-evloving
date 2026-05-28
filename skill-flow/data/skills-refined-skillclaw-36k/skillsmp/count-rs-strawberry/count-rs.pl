#!/usr/bin/env perl
use strict;
use warnings;

# Count the number of Rs (case-insensitive) in "strawberry"
my $word = "strawberry";
my $count = () = $word =~ /r/gi;

print "=" x 50 . "\n";
print "Counting Rs in: \"$word\"\n";
print "=" x 50 . "\n\n";

# Show each occurrence
my $pos = 0;
my @positions;
while ($word =~ /r/gi) {
    push @positions, pos($word);
}

print "Found $count occurrence(s) of the letter 'R':\n\n";
for my $i (0 .. $#positions) {
    my $position = $positions[$i];
    my $char_at_pos = substr($word, $position - 1, 1);
    print "  " . ($i + 1) . ". Position $position: '$char_at_pos'\n";
}

print "\n";
print "Visual representation:\n";
print "  $word\n";
print "  ";
for my $i (0 .. length($word) - 1) {
    my $char = substr($word, $i, 1);
    if ($char =~ /r/i) {
        print "^";
    } else {
        print " ";
    }
}
print "\n\n";

print "Total count: $count\n";
print "=" x 50 . "\n";
