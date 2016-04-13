import sys
#import json
#import operator

def main():    
    if len(sys.argv) == 3:
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
    else: #default parameters for testing
        sent_file = open("AFINN-111.txt")
        tweet_file = open("microsoft.txt")


    #load 1 word dictionary
    scores = {}
    for line in sent_file:
        term, score  = line.split("\t") 
        scores[term] = int(score)

    #missing_scores = {} #not using this at the moment
    ranked_tweets = {}

    for line in tweet_file:
        line= line.strip()
        if line=="":#ignore blank lines
            next

        #print line
        tweet_score = 0
        try:
            words = line.split()
            #as per "GetTwitterData.py"'s notes, the last element is always the
            #tweet's URL, so we dont need it
            words = words[:-1]

            for word in words:
                if not (word.startswith('http') and word.startswith('#') and word.startswith('@') ):
                    tweet_score += scores.get(word, 0)

            if tweet_score !=0:
                ranked_tweets[line] = tweet_score

        except KeyError:
            continue

    print "Number of tweets scored: "+str(len(ranked_tweets))
    d = dict((k, v) for k, v in ranked_tweets.items() if v > 0)
    print "    Positive Tweets:: "+str(len(d))
    d = dict((k, v) for k, v in ranked_tweets.items() if v < 0)
    print "    Negative Tweets:: "+str(len(d))

    print ""
    print ""


    print "Top 10 Best tweets: "
    for key, value in sorted(ranked_tweets.iteritems(), key=lambda (k,v): (v,k), reverse=True)[0:9]:
        print "   %s: %s" % (key, value)

    print " "
    print " "

    print "Top 10 Worst tweets: "
    for key, value in sorted(ranked_tweets.iteritems(), key=lambda (k,v): (v,k))[0:9]:
        print "   %s: %s" % (key, value)


if __name__ == '__main__':
    main()
