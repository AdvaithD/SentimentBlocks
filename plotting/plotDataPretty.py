#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy, sys, datetime
import smooth

# dem lists tho
dates = []
redSen = []
twitSen = []
priceUSD = []
priceBTC = []

inputCurrency = sys.argv[1] # "ethereum" or "bitcoin"

# read data
inputDataFileName = "../logs/" + inputCurrency + "_LOG.csv"
inputDataFile = open(inputDataFileName,'r')

# datetime from string
def gimmeDatetime(dateString):
    datetime_object = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    return datetime_object

# extract data from CSV
for line in inputDataFile:
    data = line.split(";") #date,REDDIT,sens,TWITTER,sens,PRICE,prices
    dates.append(gimmeDatetime(data[0]))
    if data[2] != '':
        redSen.append([float(i) for i in data[2].split(",")])
    else:
        redSen.append([])
    if data[4] != '':
        twitSen.append([float(i) for i in data[4].split(",")])
    else:
        twitSen.append([])
    if len(data[6].split(",")) < 2:
        priceUSD.append(priceUSD[-1])
        priceBTC.append(priceBTC[-1])
    else:
        priceUSD.append(float(data[6].split(",")[0].strip()))
        priceBTC.append(float(data[6].split(",")[1].strip()))

# debug output
"""
print(dates)
print(redSen)
print(twitSen)
print(priceUSD)
print(priceBTC)
"""
# function to remove mismatched points
def matchUp(list1,list2):
    out = [[],[]]
    for i in range(0,len(list1)):
        entry1 = list1[i]
        entry2 = list2[i]
        if numpy.isnan(entry2):
            continue
        else:
            out[0].append(entry1)
            out[1].append(entry2)
    return out

# get mean of a bunch of sentiments
def processSentiment(sentiments):
    out = []
    curr = 0
    for s in sentiments:
        if len(s) > 0:
            curr = numpy.mean(s)
        out.append(curr)
    return out

# average the last N block sentiments
def movingAverageSentiment(secondBlocks,period):
    lastNblocks = secondBlocks[0:period] # start with the first N blocks
    averages = [] # store the averages
    for i in range(0,period): # N seconds at the beginning have no average
        averages.append(numpy.nan) # pad averages with nan in the beginning
    for secondBlock in secondBlocks[period:]: # loop over every 1-second block in the period of N seconds
        sentimentsToAverage = [] # to hold all the sentiments from the period
        for block in lastNblocks: # loop over every block in the period
            for sentiment in block: # loop over each block's sentiments
                sentimentsToAverage.append(sentiment) # store sentiment
        avgSentiment = numpy.mean(sentimentsToAverage) # average all the sentiments from the period
        averages.append(avgSentiment) # store average for this block
        lastNblocks = lastNblocks[1:] # remove first block from moving period
        lastNblocks.append(secondBlock) # add the last block to the moving period
    return averages # return a list of averages for every single 1-second block

# averages before and after
def movingAverageSentimentMIRRORORIG(sentiments,period):
    averages = []
    for i in range(0,period/2):
        averages.append(numpy.nan)
    for i in range(0,len(sentiments)-period):
        sens_tot = 0
        sens_num = 0
        for j in range(0, period):
            for s in sentiments[i+j]:
                sens_tot = sens_tot + s
                sens_num = sens_num + 1
        if sens_num > 0:
            averages.append(sens_tot/sens_num)
        else:
            averages.append(0)
    for i in range(len(averages), len(sentiments)):
        averages.append(numpy.nan)
    return averages

# get d/dt
def derivative(ys, window):
    res = []
    for i in range(0, window):
        res.append(numpy.nan)
    for i in range(window, len(ys)-window):
        res.append(float(ys[i+window]-ys[i-window])/(2*window))
    for i in range(0, window):
        res.append(numpy.nan)
    return res

# get float from time
def time_to_float(t):
    return float((t-datetime.datetime(2018,1,1)).total_seconds())

############################
# START PLOTTING ###########
############################
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
fig, ax = plt.subplots()
ax.set_xlabel("Date", fontsize=20)

def MAKE_PLOT_1(): # shows reddit & twitter, smoothed, on top of their 30min averaged sentiments, and priceUSD
    date_floats = map(time_to_float, dates)
    if inputCurrency == "bitcoin":
        ax.set_ylabel("BTC value in USD", fontsize=20)
        priceUSD_smooth = smooth.savitzky_golay(numpy.array(priceUSD), 1201, 3) # SG filter on USD price
        #d_priceUSD_smooth = derivative(priceUSD_smooth, 10)
        ax.plot(dates,priceUSD,color="#333333",linewidth=3,alpha=0.2)
        ax.plot(dates,priceUSD_smooth,color="#333333",linewidth=3)
    else:
        ax.set_ylabel("ETH value in BTC", fontsize=20)
        priceBTC_smooth = smooth.savitzky_golay(numpy.array(priceBTC), 1201, 3) # SG filter on USD price
        ax.plot(dates,priceBTC,color="#333333",linewidth=3,alpha=0.2)
        ax.plot(dates,priceBTC_smooth,color="#333333",linewidth=3)

    # reddit
    redSen_avg = movingAverageSentiment(redSen, 1800)
    redDates_new = matchUp(dates,redSen_avg)[0]
    redSen_new = matchUp(dates,redSen_avg)[1]
    redSen_smooth = smooth.savitzky_golay(numpy.array(redSen_new), 1201, 3) # SG filter on reddit
    axR = ax.twinx()
    axR.plot(redDates_new,redSen_new,color="#FF4500",linewidth=3,alpha=0.2)
    axR.plot(redDates_new,redSen_smooth,color="#FF4500",linewidth=3)
    axR.tick_params(axis='y', colors='#FF4500')
    axR.set_ylabel("Sentiment", fontsize=20)

    # twitter
    twitSen_avg = movingAverageSentiment(twitSen, 1800)
    twitDates_new = matchUp(dates,twitSen_avg)[0]
    twitSen_new = matchUp(dates,twitSen_avg)[1]
    twitSen_smooth = smooth.savitzky_golay(numpy.array(twitSen_new), 1201, 3) # SG filter on twitter
    axT = ax.twinx()
    axT.plot(twitDates_new,twitSen_new,color="#1DA1F2",linewidth=3,alpha=0.2)
    axT.plot(twitDates_new,twitSen_smooth,color="#1DA1F2",linewidth=3)
    axT.tick_params(axis='y', colors='#1DA1F2')

MAKE_PLOT_1()
plt.show()
