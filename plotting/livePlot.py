#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy, sys, datetime


PERIOD = 60*30
CUR_PERIOD = 60*10


# dem lists tho
dates = []
redSen = []
twitSen = []
priceUSD = []
priceBTC = []

# read data
# inputDataFileName = 'plotTesting\ethereumLog_2018-01-21 02-50-34.csv'
inputDataFileName = sys.argv[1]
currency = sys.argv[2]
nlines = 0 # num of lines already read

# datetime from string
def gimmeDatetime(dateString):
    datetime_object = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    return datetime_object

# extract data from CSV
def update_input():
    global nlines
    inputDataFile = open(inputDataFileName, 'r')
    for line in inputDataFile.readlines()[nlines:]:
        nlines += 1
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
            if len(priceUSD) < 1:
                priceUSD.append(12000)
                priceBTC.append(0.1)                
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
def matchUp(list1, list2):
    xs, ys = [], []
    for i in range(0,len(list1)):
        entry1 = list1[i]
        entry2 = list2[i]
        if numpy.isnan(entry2):
            continue
        else:
            xs.append(entry1)
            ys.append(entry2)
    return xs, ys


# some moving averages calculated here
twiAvg = []
redAvg = []
usdAvg = []
btcAvg = []

def updateMovingAverageSentiment(period):
    if nlines < period:
        return

    nlinesadded = nlines - len(twiAvg) - period
    for i in range(max(period, nlines-nlinesadded), nlines):
        twiConcat = [num for block in twitSen[i-period:i] for num in block]
        redConcat = [num for block in redSen[i-period:i] for num in block]
        # print(twiConcat)
        # print(redConcat)

        if len(twiConcat) > 0:
            twiAvg.append(numpy.mean(twiConcat))
        else: #if there are no events in the last period just put in a NaN
            twiAvg.append(numpy.nan)
        if len(redConcat) > 0:
            redAvg.append(numpy.mean(redConcat))
        else:
            redAvg.append(numpy.nan)

def updateMovingAverage(period):
    if nlines < period:
        return

    nlinesadded = nlines - len(usdAvg) - period
    for i in range(max(period, nlines-nlinesadded), nlines):
        usdAvg.append(numpy.mean(priceUSD[i-period:i]))
        btcAvg.append(numpy.mean(priceBTC[i-period:i]))


# import data

update_input()
updateMovingAverage(CUR_PERIOD)
updateMovingAverageSentiment(PERIOD)

print("LENGTH OF FEED")
print(len(twitSen))
print(nlines)

# start plottin it

btc_color = 'b'
usd_color = 'g'
red_color = '#f57c00'
twi_color = '#1DA1F2'

fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(9, 7))

plt.suptitle(currency + " - Live", fontsize=14)

ax3 = ax2.twinx()
ax1 = ax.twinx()

btcPlot, = ax1.plot(dates[CUR_PERIOD:], btcAvg, color=btc_color)
usdPlot, = ax.plot(dates[CUR_PERIOD:], usdAvg, color=usd_color)

twix, twiy = matchUp(dates[PERIOD:], twiAvg)
redx, redy = matchUp(dates[PERIOD:], redAvg)
twiPlot, = ax2.plot(twix, twiy, color=twi_color)
redPlot, = ax3.plot(redx, redy, color=red_color)


ax.tick_params(axis='y', colors=usd_color)
ax1.tick_params(axis='y', colors=btc_color)
ax2.tick_params(axis='y', colors=twi_color)
ax3.tick_params(axis='y', colors=red_color)

ax.set_ylabel("USD", color=usd_color)
ax1.set_ylabel("BTC", color=btc_color)
ax2.set_ylabel("Twitter", color=twi_color)
ax3.set_ylabel("Reddit", color=red_color)

print("FINISHED INIT")

# and move it!
def animate(i):
    global usdPlot, twiPlot, redPlot

    print("UPDATING VALUES...")
    update_input()
    updateMovingAverage(CUR_PERIOD)
    updateMovingAverageSentiment(PERIOD)

    print("UPDATED VALUES")

    usdPlot.set_data(dates[CUR_PERIOD:], usdAvg)
    print("RESET Dollar")
    btcPlot.set_data(dates[CUR_PERIOD:], btcAvg)
    print("RESET Bitcoin")
    twix, twiy = matchUp(dates[PERIOD:], twiAvg)
    redx, redy = matchUp(dates[PERIOD:], redAvg)
    print(str(len(twix)) + ", " + str(len(twiy)))
    print(str(len(redx)) + ", " + str(len(redy)))
    twiPlot.set_data(twix, twiy)
    print("RESET Twitter")
    redPlot.set_data(redx, redy)
    print("RESET Reddit")

    print("DONE")

    return [usdPlot, btcPlot, twiPlot, redPlot]


anim = animation.FuncAnimation(fig, animate, interval=1000, repeat=False, blit=False)

plt.show()
