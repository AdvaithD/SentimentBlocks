import sys, praw

# crypto subreddits
"""
allBitcoinSubs = ["Bitcoin","bitcoin_uncensored","BitcoinAUS","BitcoinBeginners","BitcoinCA","BitcoinDayTrade","BitcoinMarkets","BitcoinMining","BitcoinSerious","BitcoinThoughts","BitcoinUK"]
cryptosubsLookupALL = {
"bitcoin":allBitcoinSubs,
"ethereum":["ethereum","EtherMining","ETHInsider","ethtrader"],
"litecoin":["litecoin","LitecoinMarkets","litecoinmining"],
"ripple":["ripple"],
"bitcoin cash":["btc","bitcoincash","bch"]+allBitcoinSubs,
}
"""

# crypto trading subreddits
cryptosubsLookup = {
"bitcoin":["BitcoinDayTrade","BitcoinMarkets"],
"ethereum":["ethtrader"],
"litecoin":["LitecoinMarkets"]
}


# function to return a streamable subreddit
def streamableSubreddit(currency="bitcoin"):

    # set up reddit script application with login info
    reddit = praw.Reddit(client_id="9REB6eZzDsH03g",
            client_secret="RHbs-1YOoA7PBARuWg9fvzqquzk",
            password="pw4hcTERNARY1337",
            user_agent='cryptostreamer',
            username="SeeminglyAppropriate")

    # check connection and login success
    print(" > cryptostreamer: Testing Reddit connection...")
    username = str(reddit.user.me())
    print(" > cryptostreamer: Logged in as /u/"+username)

    # get combined subreddit
    cryptosubs = cryptosubsLookup[currency]
    subName = ""
    for cryptosub in cryptosubs:
        subName = subName+cryptosub+"+"
    subName = subName[:-1]
    print(" > cryptostreamer: using combined subreddits: "+subName)
    return reddit.subreddit(subName)

# remove links
def sanitise(commentBody):
    bits = commentBody.split()
    out = ""
    for bit in bits:
        if "http" in bit:
            continue
        else:
            out = out + bit + " "
    return out[:-1]

# comment stream
def stream_reddit_comments(queue,currency):
    while True:
        try:
            subreddit = streamableSubreddit(currency)
            for comment in subreddit.stream.comments():
                queue.put(sanitise(comment.body))
        except Exception as e:
            print(str(e))





