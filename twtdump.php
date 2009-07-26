<?
	$i = 0;
	$U = "USERNAME"; $P = "PASSWORD";
	while($i<32):
		$json = json_decode(file_get_contents("http://$U:$P@twitter.com/statuses/user_timeline.json?page=$i"), true);
		$j = 0;
		while($j<count($json)):
			file_put_contents('tweets.txt', file_get_contents("tweets.txt") . $json[$j]['text'] . "\n");
			$j++;
		endwhile;
		$i++;
	endwhile;
?>