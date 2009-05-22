<?
	# wanted to use Python for this, but I'll need to install
	# simpleJSON and stuff, so it's just quicker with PHP at this point
	header("Content-type:text/plain");
	
	$last_count = file_get_contents('lastFetch');
	$tweets = json_decode(file_get_contents("http://TWITTER_USERNAME:TWITTER_PASSWORD@twitter.com/statuses/friends_timeline.json?since_id=$last_count&count=50"), true);
	$id = $tweets[0]['id'];
	$blacklist_users = array();
	$blacklist_domains = array();
	
	foreach($tweets as $tweet):
		if(in_array($tweet['user']['screen_name'], $blacklist))
			continue;
		
		$s = $tweet['text'];
		preg_match_all("/(?:http|https)\:\/\/(\S+)/", $s, $match);
		if(count($match[0]) != 0): # make the call
			
			# first get the URL endpoint
			$ch = curl_init($match[0][0]);
				curl_setopt_array($ch, array(
											CURLOPT_FOLLOWLOCATION => 1,
											CURLOPT_TIMEOUT => 1,
											CURLOPT_NOBODY => 1
										));
			curl_exec($ch);
			$url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
			$host = parse_url($url);
				$host = str_ireplace(array(".com", ".org", ".net"), "", $host['host']);

			if(in_array($host, $domains))
				continue;
				
			//echo $match[0][0] . "\n" . $url . "\n\n";

			$delicious = file_get_contents("https://DELICIOUS_USERNAME:DELICIOUS_PASSWORD@api.del.icio.us/v1/posts/add?url=". urlencode($url) ."&description=" . urlencode($s) . "&tags=tweet-mark+" . $tweet['user']['screen_name']);
			$return = simplexml_load_string($delicious);
			if($return->attributes()->code != 'done')
				file_put_contents('tweetMarksError', "$s\n" . $return->attributes()->code . "\n\n");
		endif;
	endforeach;
	
	file_put_contents('lastFetch', $id);
	echo file_get_contents('tweetMarksError');
?>