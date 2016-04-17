#Used to fetch live stream data from twitter.
#To get credentials: "https://dev.twitter.com/apps"

import oauth2 as oauth
import urllib2 as urllib
import json
from pprint import pprint
import sys


def twitter_track(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
    url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    response = opener.open(url, encoded_post_data)

    return response


def getData(mode, topn, search_criteria):
	
    parameters = []

    #returns an infinite stream of tweets, hence the need to ^C to break out of the for loop
    #use the first URL to get all sort of tweets
    if mode=='live track':
		print "Tracking..."
		#url = "https://stream.twitter.com/1/statuses/sample.json"
		url = "https://stream.twitter.com/1.1/statuses/filter.json?track=" + search_criteria #track one subject
		response = twitter_track(url, "GET", parameters)
		for line in response:
			text = line.strip()
			
			#"line" has all the Json file for the tweet, containing all tweet information (id, time, user info and so on..)
			#but since I only care about the message, I'm doing some very basic string manipulation where I find the "text"
			#key and the following key (called "source") and get everything in between
			#there is clearly room for improvement here - but it works for my simple use case			
			s= str.find(text,"text")
			e =str.find(text,"source")
			print text[s+7:e-3]
			print ""


    elif mode=="topN":#will return TOP N tweets on the subject
		#tweet_count = '&count='+str(topn)    # tweets/page
		#queryparams = '?q=Microsoft&lang=en'+tweet_count
		queryparams = '?q=%s&lang=en&count=%s' %(search_criteria, topn)

		url = "https://api.twitter.com/1.1/search/tweets.json" + queryparams

		#Ignoring the "parameters" variable - quite easy to use the URL
		response = twitter_track(url, "GET", parameters)
		data = json.load(response)#contains all N tweets
		#pprint(data) # data is a dictionary
		for tweet in data["statuses"]:
			print tweet["text"]

#TO DO:
#clean unnecessary characters, ex: URLS are coming like: http:\/\/t.co\/RC1Z7IaMu5
#Look for the "lang" tag inside the "user" tag to filter by language - currently all languages are being fetched

if __name__ == '__main__':
    #Options:
    #live track: Track Function where all tweets or a single search criteria can be tracked in real-time
    #            Tweets do not repeat, second parameter ignored
    #topN: Displays last N tweets on the subject#
	
	if len(sys.argv) ==1:
		print "Please Inform the search term. Exiting..."
		sys.exit()
	
	#This is not on Git. Substitute the 3 lines bellow with your key
	from KeyHolder import KeyHolderMain
	k = KeyHolderMain()
	api_key, api_secret, access_token_key, access_token_secret = k.getAPiKeys()

	_debug = 0

	oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
	oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

	signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
	http_method = "GET"
	http_handler  = urllib.HTTPHandler(debuglevel=_debug)
	https_handler = urllib.HTTPSHandler(debuglevel=_debug)
	
	getData("live track",10, sys.argv[1])

