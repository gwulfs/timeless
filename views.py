from flask import Flask, render_template, jsonify, make_response
import sqlite3
import json

from azureml import Workspace
from keys import azure_key

import urllib2
import urllib
import sys
import base64
import json

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('index.html')

@app.route("/table")
def table():
    account_key = azure_key
    input_text = 'I am feeling sick'
    base_url = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/'
    creds = base64.b64encode('AccountKey:' + account_key)
    headers = {'Content-Type':'application/json', 'Authorization':('Basic '+ creds)}
    params = { 'Text': input_text}

    key_phrases_url = base_url + '/GetKeyPhrases?' + urllib.urlencode(params)
    req = urllib2.Request(key_phrases_url, None, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)

    return render_template('table.html', data=obj['KeyPhrases'][0])
