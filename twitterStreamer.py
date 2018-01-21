import langid, tweepy

cryptoTagsLookup = {
"bitcoin":["bitcoin","btc","xbt"],
"ethereum":["ethereum","ether","ETH"],
"litecoin":["litecoin","LTC"],
"ripple":["ripple","XRP"],
"bitcoin cash":["bitcoincash","bitcoin cash","BCH"]
}

# check if a tweet is in english
def isEnglish(tweet):
    if str(langid.classify(tweet)[0]) == 'en':
        return True
    return False

# remove links
def sanitise(tweet):
    bits = tweet.split()
    out = ""
    for bit in bits:
        if "http" in bit or "@" in bit or "#" in bit or "&" in bit or len(bit) > 15 or "$" in bit or "£" in bit or "RT:" in bit:
            continue
        else:
            out = out + bit + " "
    return out[:-1]


# define this class... black magic if you ask me
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, queue=None):
        tweepy.StreamListener.__init__(self, api=api)
        self.queue = queue
        self.ntweets = 0

    def on_status(self, status):
        self.ntweets += 1
        if hasattr(status, 'extended_tweet'):
            text = status.extended_tweet['full_text']
        else:
            text = status.text
        text = sanitise(text)
        if isEnglish(text):
            self.queue.put(text)
            #print("TWEET: "+text)

# this function makes the stream you want and starts it...
def stream_tweets(queue, currency):
    while True:
        try:
            # set some auth parameters
            auth = tweepy.OAuthHandler('ZrNFQqhrU6wDwNIHVO9aNq4Tr', 'UqrATAvSXVomDbK5xCsJtuDm9TgI6F7SEOWTMO7lq2uxCQTDAT')
            auth.set_access_token('954779253576491010-UrmAPcTp3ilQQKVhInm1bOuhZ9FIsO0', 'WIDH89P6lTyguhEHyIt04VfrhaVY2VhuSVMYVy2pbLTXb')

            # initialise the API
            myapi = tweepy.API(auth)
            keywords = cryptoTagsLookup[currency]
            print(" > Streaming tweets related to: " + str(keywords))

            myStreamListener = MyStreamListener(queue=queue)
            myStream = tweepy.Stream(auth=myapi.auth, listener=myStreamListener)
            myStream.filter(track=keywords)
        except Exception as e:
            print(str(e))

