import accounts
import praw
import sys
import datetime

r = praw.Reddit('Rammus OK Bot by /u/Xwerve and /u/liquidized')
username = accounts.rammus_ok_bot_user
password = accounts.rammus_ok_bot_pass
subreddit = r.get_subreddit('leagueoflegends')
comment_subreddits = 'leagueoflegends'
r.login(username, password)
posts = subreddit.get_new()
comments = r.get_comments(comment_subreddits)
key_phrase = ['ok', 'ok.', 'taunt']
key_words = ['rammus', 'spiky armadillo']
comment_ids = []
post_ids = []

while True:
	if len(comment_ids) > 100:
		comment_ids.pop(0)
	try:
		comment = next(comments)
		post = next(posts)
	except StopIteration:
		posts = subreddit.get_new()
		comments = r.get_comments('leagueoflegends')
		comment = next(comments)
		post = next(posts)
	except:
 		os.execv(__file__, sys.argv)
	for phrase in key_phrase:
		if phrase == str(comment).lower() and str(comment.author) != username and str(comment.id) not in comment_ids:
			print(comment, 'posted by', comment.author)
			comment.upvote()
			comment_ids.append(str(comment.id))
			comment.reply('ok')
	for word in key_words:
		if word in str(comment).lower() and str(comment.author) != username and str(comment.id) not in comment_ids:
			current_time = datetime.datetime.now().time()
			print(comment, 'posted by', comment.author, 'at', current_time.isoformat())
			comment.upvote()
			comment_ids.append(str(comment.id))
			comment.reply('ok')
	for word in key_words:
		if (word in str(post).lower() or word in str(post.selftext).lower()) and str(post.id) not in post_ids:
			current_time = datetime.datetime.now().time()
			try:
				print(post, 'posted by', post.author, 'at', current_time.isoformat())
				post.upvote()
				post_ids.append(str(post.id))
				post.add_comment('ok')
			except praw.errors.APIException:
				print("POST TOO OLD")

