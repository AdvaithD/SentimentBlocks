# -*- coding: utf-8 -*-

import http.client, urllib
import json

# USAGE

# documents = [
#    { 'id': '1', 'language': 'en', 'text': 'I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable.' },
#    { 'id': '2', 'language': 'es', 'text': 'Este ha sido un dia terrible, llegué tarde al trabajo debido a un accidente automobilistico.' }
#]
# result1 = GetSentiment("hello there")
# => 0.97887
#
# result2 = GetSentimentBatch(documents)
# => [{'score': 0.954, 'id': '1'}, {'score': 0.024, 'id': '2'}]

# Replace the accessKey string value with your valid access key.
accessKey = 'a5a404da80c14f7dbb7fa453621fa2db'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your access keys.
# For example, if you obtained your access keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial access keys are generated in the westcentralus region, so if you are using
# a free trial access key, you should not need to change this region.
from textblob import TextBlob as tt
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'

def GetSentimentBatch(documents):
    "Gets the sentiments for a set of documents and returns the information."

    docs = { 'documents': documents}

    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection(uri)
    body = json.dumps (docs)
    conn.request("POST", path, body, headers)
    response = conn.getresponse()
    res = json.loads(response.read())['documents']
    return res

def GetSentiment(string):
    "Gets the sentiment for one document"

    docs = [{'id':'1', 'language': 'en', 'text':string}]
    res = GetSentimentBatch(docs)
    if len(res) == 0:
        return -1
    return res[0]['score']

def APIsen(string):
    pol = tt(string).sentiment.polarity
    return pol #(pol+1.0)/2.0













