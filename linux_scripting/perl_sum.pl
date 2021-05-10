#!/usr/bin/env perl

use strict;
use warnings;

open my $fh, '<', "nginx_logs" or die $!;

my $total = 0;

while (<$fh>) {

    my ($ip, $x1, $x2, $time, $tz, $request, $req, $req2, $status, $size, $referer, $user_agent) = split;

    if ($size ne '"-"') {
        $total += $size;
    }

}

print "Total:  $total\n";
