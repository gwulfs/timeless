import json
import urllib2
import urllib
import sys
import base64

class AzureTextAnalytics:
    def __init__(self):
        self.account_key = 'I9AbzJHdjgs7nzU8DEo3wynQ/yrJ0unYY+Qw6qD8mOg'
    def getOutput(self, input_text):
        base_url = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/v1'
        creds = base64.b64encode('AccountKey:' + self.account_key)
        headers = {'Content-Type':'application/json', 'Authorization':('Basic '+ creds)}
        params = { 'Text': input_text}
        sentiment_url = base_url + '/GetSentiment?' + urllib.urlencode(params)
        req = urllib2.Request(sentiment_url, None, headers)
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        key_phrases_url = base_url + '/GetKeyPhrases?' + urllib.urlencode(params)
        req = urllib2.Request(key_phrases_url, None, headers)
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        return obj['KeyPhrases']
