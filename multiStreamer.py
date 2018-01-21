#!/usr/bin/python3\
import multiprocessing, time, sys, datetime
import sentiment
import redditStreamer
import twitterStreamer # TODO
import priceStreamer # TODO

# read arguments to choose currency, default to BTC
currency = "bitcoin"
if len(sys.argv) > 1:
    currency = sys.argv[1]
print(" > cryptostreamer: streaming updates related to "+currency)

# get the reddit streamer
redditQueue = multiprocessing.Queue()
redditProcess = multiprocessing.Process(target=redditStreamer.stream_reddit_comments, args=(redditQueue,currency,))
redditProcess.start()

# get the twitter streamer TODO
twitterQueue = multiprocessing.Queue()
twitterProcess = multiprocessing.Process(target=twitterStreamer.stream_tweets, args=(twitterQueue,currency,))
twitterProcess.start()

# get the price streamer TODO
priceQueue = multiprocessing.Queue()
priceProcess = multiprocessing.Process(target=priceStreamer.stream_prices, args=(priceQueue,currency,))
priceProcess.start()

# output to log file!
timeStampAtStart = str(datetime.datetime.now())[:-7]
#logFileName = ("logs/"+currency+"Log_"+timeStampAtStart+".csv").replace(":","-")
logFileName = ("logs/"+currency+"_LOG.csv")
logFile = open(logFileName,'a')
#logFile.write(replyLog)

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
##    redditAvg = sum(redditSens)/len(redditSens) if len(redditSens) > 0 else 0.5
##    twitterAvg = sum(twitterSens)/len(twitterSens)if len(twitterSens) > 0 else 0.5
    while not priceQueue.empty():
        prices = priceQueue.get()

    # print to CSV logfile
    logEntry=str(datetime.datetime.now())[:-7]+";REDDIT;"+str(redditSens)[1:-1]+";TWITTER;"+str(twitterSens)[1:-1]+";PRICE;"+str(prices)[1:-1]+"\n"
    logFile.write(logEntry)
    logFile.flush()
    print(logEntry[:-1])
    
    # output moving average
##    nSentiments = 10
##    redditMvgAvg = str(round(sum(redditSensALL[-nSentiments:])/nSentiments,3)) if len(redditSensALL) > nSentiments else "NaN"
##    twitterMvgAvg = str(round(sum(twitterSensALL[-nSentiments:])/nSentiments,3)) if len(twitterSensALL) > nSentiments else "NaN"
##    print("REDDIT AVG: "+redditMvgAvg.ljust(10)+"TWITTER AVG: "+twitterMvgAvg.ljust(10))
    time.sleep(1)



















