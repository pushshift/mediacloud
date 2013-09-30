#!/usr/bin/env perl

use strict;
use warnings;

BEGIN
{
    use FindBin;
    use lib "$FindBin::Bin/../lib";
}

use Modern::Perl "2012";
use MediaWords::CommonLibs;
use MediaWords::GearmanFunction::AddDefaultFeeds;
use Gearman::JobScheduler;

sub main
{
    while ( 1 )
    {
        my $gearman_job_id = MediaWords::GearmanFunction::AddDefaultFeeds->enqueue_on_gearman();
        say STDERR "Enqueued Gearman job with ID: $gearman_job_id";
        my $log_path = Gearman::JobScheduler::log_path_for_gearman_job( MediaWords::GearmanFunction::AddDefaultFeeds->name(),
            $gearman_job_id );
        say STDERR "(the job is writing / will write its log to: $log_path)";

        sleep( 60 );
    }
}

main();
