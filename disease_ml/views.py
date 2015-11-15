from flask import Flask, render_template, jsonify, make_response, url_for, request
import sqlite3
import json
import urllib2
import urllib
import sys
import base64

from Azure import AzureTextAnalytics

azureTextAnalytics = AzureTextAnalytics()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results", methods = ['POST'])
def results():
    #return request.form['query']
    searchTerms = azureTextAnalytics.getOutput(request.form['query'])
    return render_template('results.html', textAnalytics = json.dumps(searchTerms[0].split()), searchQuery=json.dumps(request.form['query'].split()))
