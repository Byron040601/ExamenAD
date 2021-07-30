
import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


###API ########################
ckey = "YxSIuUqv01pxuROAxrvKW1zkS"
csecret = "4HSzn5PvQ9UAsyw0MgzAlQYG5OkofvYQjzhSLcvWVE3ntROHmS"
atoken = "1064745937552195589-gl9Y7hih9w0BjTddHWwD1yjuGL4fAg"
asecret = "lkccuyOeyMmPQdYKAL071hAV4rpb5x1lEtzeP82cKwzJj"
#####################################

class listener(StreamListener):

    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            doc = db.save(dictTweet)
            print ("SAVED" + str(doc) +"=>" + str(data))
        except:
            print("Already exists")
            pass
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

'''========couchdb'=========='''
server = couchdb.Server('http://admin:admin@localhost:5984/')  # ('http://115.146.93.184:5984/')
try:
    db = server.create('juegos_olimpicos')
except:
    db = server['juegos_olimpicos']

'''===============LOCATIONS=============='''

twitterStream.filter(locations=[129.19,31.0,143.53,40.58])
#twitterStream.filter(track=['fortnite', 'freefire'])
