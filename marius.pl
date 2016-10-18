#!/usr/bin/perl
use v5.14;
use warnings;

use Data::Dumper qw/Dumper/;
use Encode;
use Digest::MD5 qw/md5_hex/;
use File::Slurp;
use HTML::TreeBuilder;
use List::MoreUtils qw/uniq/;
use MediaWiki::API;
use Storable qw/thaw freeze/;

my $mw = MediaWiki::API->new;
$mw->{config}->{api_url} = 'https://en.wikipedia.org/w/api.php';

sub get_random_article_title {
	my $articles = $mw->list({
		action  => 'query',
		list    => 'random',
		rnlimit => 1,
		rnnamespace => 0,
	}, {max => 1}) or die $mw->{error}->{code} . ': ' . $mw->{error}->{details};

	my ($article) = @$articles;
	$article->{title};
}

sub get_article {
	my ($title) = @_;
	my $md5 = md5_hex (encode 'UTF-8', $title);
	my $file = "botcache/$md5";
	if (-f $file) {
		thaw scalar read_file $file
	} else {
		my $data = $mw->get_page({title => $title});
		write_file $file, freeze $data;
		$data
	}
}

sub find_links_in {
	my ($article) = @_;
	my $text = $article->{'*'};
	my @links = $text =~ /\[\[([^]|#]+)\]\]/g;
	@links = grep {
		!/^[A-z]*:/i || /^Category:/i
	} @links;
	uniq @links;
}

my $start = get_random_article_title;
my @queue = $start;
my (%prev, %used);

my %pregen_paths = (
	lc 'Philosophy' => <<'EOF',
Colin McGinn
University of Oxford
Department of Computer Science, University of Oxford
EOF
	lc 'United Kingdom' => <<'EOF',
Latin
University of Oxford
Department of Computer Science, University of Oxford
EOF
	lc 'London' => <<'EOF',
United Kingdom
University of Oxford
Department of Computer Science, University of Oxford
EOF
	lc 'Department of Computer Science, University of Oxford' => '',
	lc 'Coordinated Universal Time' => <<'EOF',
Greenwich Mean Time
London
United Kingdom
University of Oxford
Department of Computer Science, University of Oxford
EOF
	lc 'Latin' => <<'EOF' # Kindly suggested by Joe
University of Oxford
Department of Computer Science, University of Oxford
EOF
);

$pregen_paths{lc 'Category:Member states of the United Nations'} =
  $pregen_paths{lc 'United States'} =
  $pregen_paths{lc 'London'};

$pregen_paths{lc 'England'} = $pregen_paths{lc 'United Kingdom'};

my %dest = map { $_ => 1 } keys %pregen_paths;

sub finish {
	my ($cur) = @_;
	my @result = lc $cur;
	while ($prev{$result[0]}) {
		unshift @result, $prev{$result[0]}
	}
	say encode 'UTF-8', join "\n", @result;
	print encode 'UTF-8', $pregen_paths{lc $result[-1]};
	exit
}

while (@queue) {
	my $cur = shift @queue;
	next unless $cur;
	if ($dest{lc $cur}) {
		finish $cur;
	}
	next if $used{$cur};
	say STDERR encode 'UTF-8', "# $cur";
	$used{$cur} = 1;
	my @links = find_links_in get_article $cur;
	@links = grep { !$used{$_} } @links;
	for (@links) {
		if ($dest{lc $_}) {
			$prev{lc $_} = lc $cur;
			finish $_
		}
	}
	my $nr = 5;
	while ($nr && @links) {
		my $candidate = shift @links;
		my $art = get_article $candidate;
		next unless $art->{'*'};
		next if $art->{'*'} =~ /^#REDIRECT/i;
		push @queue, $candidate;
		$prev{lc $candidate} = lc $cur;
		$nr--;
	}
}
