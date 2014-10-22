#Copyright (C) 2014, Simon Dooms

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#from twitter import *
from twitter import *
import sys

class Backbone:
    t = None

    def __init__(self):
        #Twitter API v1.1 needs oAuth
        token = '327039781-0mljdsIiAZ0EV6ZqsLJXCOKjuhLrwZ3xFCUx4269'
        token_secret = 'r9T1w5ENSGpP9KBnApqTEsaXWe0Ja49TTw20NR4h416GS'
        con_key = '6clMQc5LA3irCE7JSgM3AC0jL'
        con_secret = 'vDFGq7hrwrUgTfRmvui59dMdABNtGg1lwaN14SMdphvMyBToTv'
        try:
            self.t = Twitter(auth=OAuth(token, token_secret, con_key, con_secret))
        except:
            print 'Error connecting to twitter'
            sys.exit()

    def search_user_timeline(self,query, since, tl_user_id):
        print "searching in timeline of user with id: " + str(tl_user_id)
        tweets = list()
        the_max_id = None
        the_max_id_oneoff = None
        new_since_id = since

        res = self.t.statuses.user_timeline(user_id = tl_user_id, count = 1000)
	#res = self.t.statuses.home_timeline(user_id=tl_user_id,count = 1000)
        num_results = len(res)
        print 'Found ' + str(num_results) + ' tweets from fucking timeling'
        for d in res:
	    if not all(x.lower() in d['text'].lower() for x in query.split()):
		if "rated" in d['text']:
			print query
			print d['text']
		continue
            tweets.append(d)
            tweetid = d['id']

            if new_since_id < tweetid:
                new_since_id = tweetid

        print 'Found ' + str(len(tweets)) + ' tweets.'
        return tweets, new_since_id

    def searchTweets(self, query, since):
        tweets = list()
        the_max_id = None #start with empty max
        the_max_id_oneoff = None
        new_since_id = since

        number_of_iterations = 0
        while (number_of_iterations <= 100):
            number_of_iterations += 1
            count = 200 #maximum number of tweets allowed in one result set
            #try:
            if the_max_id != None:
                the_max_id_oneoff = the_max_id -1
                    #798959545 ermirss
                    #res = self.t.users.search(q=query, result_type='recent', count=count,since_id=since,max_id=the_max_id_oneoff)
                res = self.t.search.tweets(q=query, result_type='recent', count=count,since_id=since,max_id=the_max_id_oneoff)
            else:
                res = self.t.search.tweets(q=query, result_type='recent', count=count,since_id=since)
            #except:
            #    print 'Error searching for tweets'
            #    return tweets, new_since_id

            try:
                #Extract the tweets from the results
                num_results = len(res['statuses'])
                print '  Found ' + str(num_results) + ' tweets.'
                for d in res['statuses']:
                    tweets.append(d)
                    tweetid = d['id']
                    if the_max_id == None or the_max_id > tweetid:
                        the_max_id = tweetid

                    if new_since_id < tweetid:
                        new_since_id = tweetid

                #end the while loop if no more tweets were found
                if len(res['statuses']) == 0:
                    break
                #break #for debug (quits after 1 iteration of count tweets)
            except ValueError:
                print 'Error ', sys.exc_info()[0]
                traceback.print_exc(file=sys.stdout)
                return tweets, new_since_id
        return tweets, new_since_id
