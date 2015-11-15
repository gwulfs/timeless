from flask import Flask, render_template, jsonify, make_response, url_for, request
import sqlite3
import json
import urllib2
import urllib
import sys
import base64

from Azure import AzureTextAnalytics
from manual_filter import ManualFilter

azure_text_analytics = AzureTextAnalytics()
manual_filter = ManualFilter()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results", methods = ['POST'])
def results():
    #return request.form['query']
    user_input = request.form['query'].split()
    azure_sentiment, azure_key_phrases = azure_text_analytics.getOutput(request.form['query'])
    azure_key_phrases = manual_filter.runFilter(user_input, azure_key_phrases)
    return render_template('dashboard.html', text_analytics = json.dumps(azure_key_phrases), search_query=json.dumps(user_input), azure_sentiment = (azure_sentiment*100))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
