import accounts
import praw
import sys
import datetime
import random

username = accounts.amumu_bot_user
password = accounts.amumu_bot_pass
subreddits = 'redditdebuggingspace'

r = praw.Reddit('Amumu Bot by /u/Xwerve and /u/liquidized')
def initialize():
	r.login(username, password)

initialize()
comment_ids = []
post_ids = []
scanned_ids = []

##### Triggers and Responses of Amumu_bot in lower case #######
pre_responses = ["Let me give you a hug.", "Let's be friends forever.", "Would you like to be friends?", "Come play with me."]
sad_responses = ["I sense that you are sad. "+response for response in pre_responses]
yes_responses = ["I thought you'd never pick me. (づ｡◕‿‿◕｡)づⒽⓤⒼ♥"]
no_responses = ["Awww. :(", "Hey, come back! ;___;"]
yes_triggers = ["ok", "yes", "yeah", "yea", "okay", "yep", "let's be friends", "yee", "i love you", " ya ", " ye ", "sure", "all right", "alright", "i want to be your friend", "hug me", "i love hugs", "<3", "i want a hug", "give me a hug", "come here", "/hug", "*hug"]
no_triggers = ["no ", "no, " "nope", "naw ", "sorry", "don't want you", "go away", "fuck off", "one wants to play with you"]
sad_triggers = ["i'm depressed", "i am depressed", "i'm sad", ":'(", "i am lonely", 
"i'm lonely", "i have no friends", "i want friends", "i'm crying", " :'(", "sad amumu", ";_;", " )':", ";__;", "i need a hug"]
########################################################################################

def reply_2_comments(comment, triggers, responses):
	commenttext = comment.body.lower()
	has_trigger = any(trigger in commenttext for trigger in triggers)
	if has_trigger and str(comment.author) != username and comment.id not in comment_ids:
		comment_ids.append(comment.id)
		reply0 = random.choice(responses)
		comment.reply(reply0)
		current_time = datetime.datetime.now().time()
		print('Bot replied to comment', comment, 'posted by', comment.author, 'at', current_time.isoformat())
		return True
	else:
		return False

def has_replied(comment): #check if the scanned comment is a response to an Amumu_bot's comment and respond to it accordingly.
	parent_id = comment.parent_id
	parent_comment = r.get_info(None, parent_id, None) 
	if type(parent_comment) == praw.objects.Comment: #in case parent_comment is not a Comment object.
		commenttext = parent_comment.body
		has_trigger = any(trigger in commenttext for trigger in sad_responses)
		if str(parent_comment.author).lower() == username.lower() and has_trigger:
			reply_2_comments(comment, yes_triggers, yes_responses) or reply_2_comments(comment, no_triggers, no_responses)
		else:
			reply_2_comments(comment, sad_triggers, sad_responses)
	else:
		reply_2_comments(comment, sad_triggers, sad_responses)

### main ###
for raw_comment in praw.helpers.comment_stream(r, subreddits, limit=25, verbosity=0): #go through a stream of new comments in subreddit.
	if len(comment_ids) > 200:
		comment_ids.pop(0)
	if len(scanned_ids) > 300:
		scanned_ids.pop(0)
	if raw_comment.id not in scanned_ids:
		scanned_ids.append(raw_comment.id)
		has_replied(raw_comment)



