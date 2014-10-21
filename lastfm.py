#Copyright (C) 2014, Simon Dooms

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from backbone import Backbone
from datetime import datetime
import re
import json
import glob
import os

def extractTitleArtistFromTweet(text):
    pattern = 'I.*listening to (.*) by (.*) http.*'
    m = re.search(pattern,text)
    if m == None:
        print 'extraction failed for text: ' + str(text)
        return -1,-1
    songtitle = m.group(1).replace('"', '')
    artist = m.group(2).replace('"', '')
    return songtitle, artist

def extractDataFromTweet(tweet):
    user = ''
    songtitle = ''
    timestamp = ''
    #user
    user = tweet['user']['id']
    screen_name = tweet['user']['screen_name']
    #timestamp
    timestamp = tweet['created_at']
    the_time = datetime.strptime(timestamp.replace(' +0000',''), '%a %b %d %H:%M:%S %Y')
    timestamp = (the_time-datetime(1970,1,1)).total_seconds()
    timestamp = int(timestamp)
    #item
    songtitle, artist = extractTitleArtistFromTweet(tweet['text'])
    return user, screen_name, songtitle, artist, timestamp

def extractDataset(tweets):
    dataset = list()
    for tweet in tweets:
        try:
            user, screen_name, songtitle, artist, timestamp = extractDataFromTweet(tweet)
            if user == -1 or screen_name == -1 or songtitle == -1 or artist == -1 or timestamp == -1:
                continue
            dataset.append((user, screen_name, songtitle, artist, timestamp))
        except:
            continue
    return dataset

def writeDataset(dataset, filename):
    lines = list()
    for ((user, screen_name, songtitle, artist, timestamp)) in dataset:
        line = str(user) + ',' + str(screen_name) + ',' + songtitle + ',' + artist +  ',' + str(timestamp) + '\n'
        line = line.encode('UTF-8')
        lines.append(line)
    with file(filename, 'a') as outfile:
        outfile.writelines(lines)

def writeTweets(tweets, filename):
    line = json.dumps(tweets, ensure_ascii = False).encode('UTF-8')
    with file(filename, 'w') as outfile:
        outfile.writelines(line)

def get_since_id(path, state, user_id = -1):
    since_id  = 1
    for infile in glob.glob( os.path.join(path, "base_tweets_*.json" if state == 1 else "tweets_"+str(user_id)+"_"+"*.json") ):
        pattern = 'base_tweets_([0-9]*).json' if state == 1 else 'tweets_'+str(user_id)+"_"+'([0-9]*).json'
        p = re.compile(pattern,re.M | re.I)
        matches = p.findall(infile)
        id = int(matches[0])
        #keep maximum id
        since_id = max(id, since_id)
    return since_id

def partial_update(dataset_path, data_path, backbone):
    since_id = get_since_id(dataset_path, 1)
    tweets, new_since_id = backbone.searchTweets("a new favorite +soundcloud",since_id)
    dump_result(tweets, new_since_id, dataset_path, data_path, "base_tweets_")

def fully_update(dataset_path, base_data_path, data_path, backbone):
    s = []
    with open(dataset_path+"/"+base_data_path,'r') as f:
        for line in f:
            s.append(line.split(',')[0])
    s = set(s)
    for user_id in s:
        since_id = get_since_id("dataset/lastfm",0,user_id)
        if since_id != 1:
            continue
        try:
            tweets, new_since_id = backbone.search_user_timeline("I'm listening to via @lastfm",since_id, user_id)
            dataset = extractDataset(tweets)
            writeDataset(dataset, dataset_path + '/' + data_path)
            writeTweets(tweets, dataset_path + "/" + "tweets_"+str(user_id)+"_" + str(new_since_id) + '.json')
        except TwitterHTTPError:
            time.sleep(60*15)
            continue

def dump_result(tweets, new_since_id, dataset_path, data_path, prefix = "base_tweets_"):
    dataset = extractDataset(tweets)
    writeDataset(dataset, dataset_path + '/' + data_path)
    writeTweets(tweets, dataset_path + "/" + prefix + str(new_since_id) + '.json')


if __name__ == "__main__":
    b = Backbone()
    partial_update("dataset/lastfm","base_listens.dat",b)
