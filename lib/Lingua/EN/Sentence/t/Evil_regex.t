#!/usr/bin/perl

# test MediaWords::Crawler::Extractor against manually extracted downloads

use strict;

BEGIN
{
    use FindBin;
    use lib "$FindBin::Bin/../lib";
}

use Readonly;

use Test::More tests => 1;
use utf8;

use Lingua::Stem;
use Lingua::Stem::Ru;
use Data::Dumper;
use Perl6::Say;
use Lingua::EN::Sentence::MediaWords;
use Lingua::Stem::Snowball;
use MediaWords::Util::Stemmer;
use Data::Dumper;
use Encode;
use MIME::Base64;

my $test_string = <<'QUOTE';
Sentence contain version 2.0 of the text. Foo.
QUOTE




my $VAR1 = "ity.\x{201d} Cic";

my $var1_base64 =  'aXR5LuKAnQEgQ2lj
';

my $var1_base64_decoded = decode ( "utf8", decode_base64 ( $var1_base64 ) );

say STDERR Dumper( $VAR1 );
say STDERR Dumper( $var1_base64_decoded );

#my $fixed_var = Lingua::EN::Sentence::MediaWords::_apply_dangerous_regex ( $VAR1 );
my $fixed_var = Lingua::EN::Sentence::MediaWords::_apply_dangerous_regex ( $var1_base64_decoded );

my $expected_fixed_var = "raised the building in a statement as \x{201c}a true showcase facility.\x{201d} Cicilline said his tour of the bu";

say STDERR Dumper( $fixed_var );

{
    #is( $VAR1, $expected_fixed_var, "sentence_split" );
    is( $var1_base64_decoded, $expected_fixed_var, "sentence_split" );

}

my $VAR2 = '0L/QvtGA0Y/QtNC60LDQvC4BIFRhZ3M6INCe0L/Qv9C+0LfQuNGG0LjRjyAB';

my $var2_base64_decoded = decode_base64 ( $var1_base64 );

my $fixed_var = Lingua::EN::Sentence::MediaWords::_apply_dangerous_regex ( $var2_base64_decoded );

say STDERR "Survived dangerous regular expression";
