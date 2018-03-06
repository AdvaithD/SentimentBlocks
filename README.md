# SentimentBlocks

There is an extensive online community of cryptocurrency investors, both long-term holders and daytraders, discussing price movements online, 24/7. Most major cryptocurrencies have dedicated subreddits for trading discussion, and these public text posts are ripe for analysis. SentimentBlocks is a program built in 24 hours for [HackCambridge Ternary](https://ternary.devpost.com/) for streaming comments from crypto-trading subreddits and Twitter tags, providing second-by-second sentiment tracking for a desired cryptocurrency.

## [See it in action for Ethereum](https://www.youtube.com/embed/wXkV4K7ivEk)

# What we did

We used the Reddit API (via the `praw` Python wrapper) to stream comments from specific cryptocurrency trading subreddits (such as [r/BitcoinDayTrade](https://www.reddit.com/r/BitcoinDayTrade), [r/BitcoinMarkets](https://www.reddit.com/r/BitcoinMarkets), [r/ethtrader](https://www.reddit.com/r/ethtrader) or [r/LitecoinMarkets](https://www.reddit.com/r/LitecoinMarkets)) relevant to a particular currency specified by the user. Similarly, we used the `tweepy` Python library to stream tweets from across Twitter with relevant tags, e.g. [#Bitcoin](https://twitter.com/search?q=%23bitcoin) or [$BTC](https://twitter.com/search?q=%24BTC).

After some cleaning, it is very easy to perform sentiment analysis on these text strings with the help of third party libraries or APIs like the Microsoft Cognitive Services [Text Analytics API](https://azure.microsoft.com/en-gb/services/cognitive-services/text-analytics).

The program offers several functions for aggregating, average and/or smoothing this data, allowing more volatile second-by-second granularity or smoother, overall mood tracking. Included are also several plotting scripts, including a dynamic animated feed, which can be run in conjunction with the stream to maintain a display that constantly updates with the sentiment of Twitter and Reddit along with the price of a currency in USD and BTC.

To try out the program, take a look at these [iPython notebooks](https://sentimentblocks-jamcowl.notebooks.azure.com/nb/tree), hosted on Microsoft Azure Cloud Services.

# Results and Comments

It is interesting to see when the sentiments of Reddit and Twitter correlate strongly with each other, hinting at a real objective change in the market. It is also interesting to watch sentiment swing on one platform before a similar change appears on the other, as if the good or bad news is slow to propagate between them. Over the 7-8 hours of active deployment we achieved during the hackathon, there were several periods when Reddit sentiment lagged behind that of Twitter by 10-30 minutes, and other periods where the precise opposite was true.

Generally the communities seem to be more reactive than proactive and seem just to be helplessly watching the market as prices fluctuate. However, there were a few pre-emptive swings in sentiment which matched a later swing in price, suggesting there remains the possibility to extract tradable signals, given the right statistical techniques.
