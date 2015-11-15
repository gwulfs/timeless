from flask import Flask, render_template, jsonify, make_response, url_for, request
import sqlite3
import json
import urllib2
import urllib
import sys
import base64

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
from nltk.corpus import stopwords

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
    user_input = request.form['query']
    all_text = user_input.split()
    print user_input
    azure_sentiment, azure_key_phrases = azure_text_analytics.getOutput(request.form['query'])
    azure_key_phrases = manual_filter.runFilter(all_text, azure_key_phrases)

    df = pd.read_csv('final_join.csv')
    pkl_file = open('model.pkl', 'rb')
    model = pickle.load(pkl_file)
    pkl_file.close()
    vect = TfidfVectorizer()

    df.wiki = df.wiki.map(lambda x: re.sub(r'[^\x00-\x7F]','',str(x)))

    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    user_input = pattern.sub('', user_input)
    df[pd.notnull(df['wiki'])]

    vect = TfidfVectorizer(min_df=10, ngram_range=(1, 2))
    vect.fit_transform(df.wiki)

    severity = model.predict_proba(vect.transform([user_input]))[0][0] * 100

    return render_template('dashboard.html', text_analytics = json.dumps(azure_key_phrases), search_query=json.dumps(all_text), azure_sentiment = (azure_sentiment*100), severity=severity)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
