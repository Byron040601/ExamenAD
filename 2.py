
import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


###API ########################
ckey = "******"
csecret = "******"
atoken = "******"
asecret = "*******"
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

twitterStream.filter(track=['juegos', 'olimpicos'])
