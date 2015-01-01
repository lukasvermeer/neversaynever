# Johan envisioned a Twitter bot that introduces people who say "X, said no one ever" to people who've said X.
# So Lukas made a thing that does something like that. It updates somewhat regularly. Maybe.
# Based on https://twitter.com/jugander/status/534178436453900288

import tweepy, re, sys, getopt, time, json

SNOE_STRING = ' #saidnooneever'
COUNT = 100
COUNT_REPLY = 10
LOOP = False
LOOP_DELAY = 60
CHECKED = {}
   
try:
    if '-k' not in sys.argv[1:]:
	raise Exception('Missing CONSUMER_KEY argument')
    if '-s' not in sys.argv[1:]:
	raise Exception('Missing CONSUMER_SECRET argument')
    opts, args = getopt.getopt(sys.argv[1:],"lk:s:f:")
except:
    print '___SNOE.py -k CONSUMER_KEY -s CONSUMER_SECRET [-f FILE -l]'
    print '	-k: Twitter API CONSUMER_KEY (required)'
    print '	-s: Twitter API CONSUMER_SECRET (required)'
    print '	-f: ignore tweets collected in FILE'
    print '	-l: loop-mode.'
    sys.exit(2)

for opt, arg in opts:
    if opt == '-k':
	CONSUMER_KEY = arg
    if opt == '-s':
	CONSUMER_SECRET = arg
    if opt == '-f':
	f = open(arg, 'r')
	for line in f:
	    CHECKED[int(json.loads(line)['tweet_id'])] = True
    if opt == '-l':
        LOOP = True

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

while True:
    twts = api.search(q=SNOE_STRING, include_entities=True, count=COUNT)
    for s in twts:
        t = re.match('^(.*)'+SNOE_STRING+'(.*)$', s.text, flags=re.IGNORECASE) # Limit to tweets ending with hashtag.
        rt = re.match('^RT (.*)$', s.text) # Skip RT's.
        at = re.match('^.?@(.*)$', s.text) # Skip @-replies.
        if t and not rt and not at and s.id not in CHECKED:
	    CHECKED[s.id] = True
            snoes = api.search(q='\"'+t.group(1)+'\"', count=COUNT_REPLY) # Find matching tweets.
            for es in snoes:
                m = re.match('^(.*)'+t.group(1)+'(.*)$', es.text, flags=re.IGNORECASE)
                nope = re.match('^(.*)'+SNOE_STRING+'(.*)$', es.text, flags=re.IGNORECASE)
                nort = re.match('^RT (.*)$', es.text, flags=re.IGNORECASE) # Skip RT's.
                if m and not nope and not nort:
                    out = {
                            'tweet_id': str(s.id),
                            'tweet_user': s.user.screen_name,
                            'tweet_text': s.text,
                            'tweet_url': 'http://twitter.com/' + s.user.screen_name + '/status/' + str(s.id),
			    'response_id': str(es.id),
                            'response_user': es.user.screen_name,
                            'response_text': es.text,
			    'response_url': 'http://twitter.com/' + es.user.screen_name + '/status/' + str(es.id)
                        }
                    print json.dumps(out, sort_keys=True)
		    sys.stdout.flush()
    if not LOOP: break
    time.sleep(LOOP_DELAY)
