<?
	header("Content-type:text/plain");
	require "idna_convert.class.php"; # get from > http://j.mp/phpidna
	
	$last_count = file_get_contents('lastFetch');
	$tweets = json_decode(file_get_contents("http://USERNAME:PASSWORD@twitter.com/statuses/friends_timeline.json?since_id=$last_count&count=50"), true);

	if(!isset($tweets[0]))
		die('No new tweets');
	
	file_put_contents('lastFetch', $tweets[0]['id']); # this script hates me
	
	$blacklist_users = array('baxiabhishek', 'ossguy', 'madguy000', 'hiway', 'the_hindu');
	$blacklist_domains = array('twitpic', 'ow.ly', 'techcrunch', 'last.fm', 'jsmag', 'ibnlive', 'spymaster', 'plazes', 'brightkite', 'gyaan');
	$stopwords = explode(',', file_get_contents('stopwords'));
	$IDN = new idna_convert();
	
	foreach($tweets as $tweet):
		if(in_array($tweet['user']['screen_name'], $blacklist_users))
			continue;
		
		$s = str_ireplace("/\n|\r/", "", $tweet['text']);
		$dup = $s; # to generate tags later on
		preg_match_all("/(?:http|https)\:\/\/(\S+)/", $s, $match);
		
		if(count($match[0]) != 0): # make the call
			
			# first get the URL endpoint
			$ch = curl_init($IDN->encode($match[0][0]));
				curl_setopt_array($ch, array(
											CURLOPT_FOLLOWLOCATION => 1,
											CURLOPT_TIMEOUT => 1,
											CURLOPT_NOBODY => 1
										));
			curl_exec($ch);
			$url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
			
			# get title / yay for YQL
			$url_title_json = json_decode(file_get_contents("http://query.yahooapis.com/v1/public/yql?q=". urlencode("SELECT * FROM html WHERE url=\"$url\" AND xpath=\"//title\"") ."&format=json"));
				$url_title = $url_title_json->query->results->title;
			
			$host = parse_url($url);
				$host = str_ireplace(array(".com", ".org", ".net", ".in", "www."), "", $host['host']);

			if(in_array($host, $blacklist_domains))
				continue;
			
			foreach($stopwords as $word):
				$dup = preg_replace("/\b$word\b/i", "", $dup);
			endforeach;
			
			$dup = preg_replace("/[^\w\s]/", "", preg_replace("/(?:http|https)\:\/\/(\S+)/", "", $dup)); # one line baby!
			$tags_string = strtolower(preg_replace(array("/\+{1,}/", "/\+$/"), array('+', ''), implode('+', explode(' ', $dup))));
			
			echo $match[0][0] . "\n" . $url . "\n" . $tags_string . "\n";

			$delicious = file_get_contents("https://USERNAME:PASSWORD@api.del.icio.us/v1/posts/add?url=". urlencode($url) ."&description=". urlencode($url_title) ."&extended=" . urlencode($s) ."&tags=tweet-mark+" . $tweet['user']['screen_name'] . "+" . $tags_string);
			
			echo $delicious . "\n\n";
		endif;
	endforeach;

	echo file_get_contents('tweetMarksError');
?>