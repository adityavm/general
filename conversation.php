<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<title>Conversation | See how it started!</title>
	<script type="text/javascript" charset="utf-8">
		var odd = "", count = 0;
		function tweet(tweet){
					var t = eval(tweet), e = document.getElementById('conversation');

						tweet_text = t.text;
						user_icon = t.user.profile_image_url;

						/* this is SO not right, but fuck it, it's 1:30 in the morning */
						e.innerHTML += "<div class='tweet "+ odd.toString() +"'>\
							<img src='"+ user_icon +"'/><div class='text'>"+ tweet_text +"</div>\
						</div><div class='clear'></div>";

						if(t.in_reply_to_status_id){
							var head = document.getElementsByTagName('head')[0], script = document.createElement('script');

								script.src = 'http://twitter.com/statuses/show/' + t.in_reply_to_status_id + '.json?callback=tweet';
								script.type = 'text/javascript';

								head.appendChild(script);
						} else 
							if(count == 0)
								e.innerHTML += "<br/><br/><p class='note'>Err, I couldn't find any more tweets. Sure this was a conversation?</p>";

						odd = (odd  == "") ? "odd" : "";
						count++;
				}

		function limit(limit){//just so people know how many more tweets they can get — Peoplearedumb™
			var l = eval(limit);
			var fd = (l.reset_time_in_seconds * 1000 - (new Date()).getTime());
			document.getElementById('limit').innerHTML += "Remaining calls: " + l.remaining_hits + ", Reset in about " + Math.floor(fd/1000/60) + " minutes";
		}
	</script>
	<style type="text/css" media="screen">
		body {
			text-align: center;
		}
		
		h1, h4 {
			font-family: "Lucida Grande", sans-serif;
		}
		
		h1 {
			color: #5D89DB;
			margin-bottom: 7px;
		}
		
		h4 {
			margin-top: 0px;
			color: #666;
		}
		
		a {
			color: #333;
			font: 11pt "Lucida Grande", "Tahoma", sans-serif;
			text-decoration: none;
		}
		
		a:hover {
			color: #4164B5;
		}
		
		#conversation {
			width: 400px;
			margin: 0 auto;
			text-align: center;
		}
		
		.tweet {
			float: left;
			width: 180px;
			border-top: 1px solid #CCC;
		}
		
			.tweet img {
				float: left;
				margin: 0 0 0 -55px;
			}
		
		.odd {
			float: right;
		}
		
			.odd img {
				float: right;
				margin: 0 -55px 0 0;
			}
		
		.tweet .text {
			font: 10pt "Lucida Grande", "Tahoma", sans-serif;
			padding: 0 5px 5px;
			line-height: 1.5em;
			text-align: left;
		}
		
			.odd .text {
				text-align: right;
			}
			
		#limit {
			font: 10pt "Lucida Grande", "Tahoma", sans-serif;
			color: #444;
			text-align: right;
			opacity: 0.8;
			position: fixed;
			bottom: 0;
			width: 98%;
			padding: 4px 0;
		}
		
			#limit .tip {
				display: none;
				background: #F5F5F5;
				color: #3F6BB4;
				padding: 8px 4px;
				font: 10pt "Lucida Grande", "Tahoma", sans-serif;
				float: right;
				width: 300px;
			}
			
			#limit:hover .tip {
				display: block;
			}
		
		.clear {
			clear: both;
		}
		
		/* ****** */
		
		input[type='text']{
			padding: 4px;
			border: 1px solid #CCC;
			font: 12pt "Lucida Grande", "Tahoma", sans-serif;
			width: 400px;
			text-align: center;
			color: #222;
		}
		
		input[type='submit']{
			visibility: hidden;
			background: #507399;
			padding: 4px 2px;
			color: white;
			font: 11pt "Lucida Grande", "Tahoma", sans-serif;
		}
		
		p {
			font: 11pt "Lucida Grande", "Tahoma", sans-serif;
			color: #444;
			width: 300px;
			line-height: 1.5em;
			margin: 10px auto;
			padding: 8px 4px;
		}
		
		p.note {
			background: #FC6;
			color: #222;
		}
	</style>
</head>
<body>
	<h1>Conversation</h1>
	<h4>See how it started!</h4>
	<div id='conversation'></div>
	<? if(isset($_GET['tweet'])): $url = end(explode('/', strip_tags($_GET['tweet'])));	?>
		<script src='http://twitter.com/statuses/show/<?=$url?>.json?callback=tweet'></script>
	<? else: ?>
		<br/><br/>
		<form action='?' method='GET'>
			<input type='text' name='tweet'/><br/>
			<p>Enter the URL of the last tweet in a conversation, press 'Enter', and I'll get the whole conversation up till that tweet for you!</p>
			<input type='submit' value='What was it?'/>
		</form>
	<? endif; ?>
	</div>
	<? if(isset($_GET['tweet'])){ ?><br/><br/><a href="/code/conversation">Another conversation?</a><? } ?>
	<div id='limit'>
		<div class='tip'>When this reaches 0, you will not be able to fetch any more conversations till the API limit is reset. The more tweets in a conversation, the faster this reduces</div>
		<div class='clear'></div>
		<script src="http://twitter.com/account/rate_limit_status.json?callback=limit"></script>
	</div>
</body>
</html>
