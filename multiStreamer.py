#!/usr/bin/python3\
import multiprocessing, time, sys, datetime
import sentiment
import redditStreamer
import twitterStreamer
import priceStreamer

# read arguments to choose currency, default to BTC
currency = "bitcoin"
if len(sys.argv) > 1:
    currency = sys.argv[1]
print(" > cryptostreamer: streaming updates related to "+currency)

# get the reddit streamer
redditQueue = multiprocessing.Queue()
redditProcess = multiprocessing.Process(target=redditStreamer.stream_reddit_comments, args=(redditQueue,currency,))
redditProcess.start()

# get the twitter streamer
twitterQueue = multiprocessing.Queue()
twitterProcess = multiprocessing.Process(target=twitterStreamer.stream_tweets, args=(twitterQueue,currency,))
twitterProcess.start()

# get the price streamer
priceQueue = multiprocessing.Queue()
priceProcess = multiprocessing.Process(target=priceStreamer.stream_prices, args=(priceQueue,currency,))
priceProcess.start()

# output to log file!
timeStampAtStart = str(datetime.datetime.now())[:-7]
logFileName = ("logs/"+currency+"_LOG.csv")
logFile = open(logFileName,'a')

# stream all the things!
blockNumber = 0
redditSensALL = []
twitterSensALL = []
prices = []

while True:
    redditSens = []
    twitterSens = []
    while not redditQueue.empty():
        comment = redditQueue.get()
        redditAPIsen = sentiment.APIsen(comment)
        redditSens.append(round(redditAPIsen,3))
        redditSensALL.append(round(redditAPIsen,3))
    while not twitterQueue.empty():
        tweet = twitterQueue.get()
        twitterAPIsen = sentiment.APIsen(tweet)
        twitterSens.append(round(twitterAPIsen,3))
        twitterSensALL.append(round(twitterAPIsen,3))
    while not priceQueue.empty():
        prices = priceQueue.get()

    # print to CSV logfile
    logEntry=str(datetime.datetime.now())[:-7]+";REDDIT;"+str(redditSens)[1:-1]+";TWITTER;"+str(twitterSens)[1:-1]+";PRICE;"+str(prices)[1:-1]+"\n"
    logFile.write(logEntry)
    logFile.flush()
    print(logEntry[:-1])

    time.sleep(1)



















