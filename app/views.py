from flask import Flask, render_template, jsonify, make_response, url_for, request
import sqlite3
import json
import urllib2
import urllib
import sys
import base64

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import re
from nltk.corpus import stopwords
import numpy as np

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
    # get user input
    user_input = request.form['query']
    all_text = user_input.split()
    print user_input

    # run though azure APIs
    azure_sentiment, azure_key_phrases = azure_text_analytics.getOutput(request.form['query'])
    azure_key_phrases = manual_filter.runFilter(all_text, azure_key_phrases)

    # run through gideon model
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


    # run though arpit model
    pkl_file = open('arpit_model.pkl', 'rb')
    pkl_file_vec = open('vec.pkl', 'rb')
    model = pickle.load(pkl_file)
    vec = pickle.load(pkl_file_vec)
    pkl_file.close()
    pkl_file_vec.close()
    df = pd.read_csv("../full_output_full.csv")
    df.wiki = df.wiki.map(lambda x: str(x).replace('\n', ' '))
    df = df[pd.notnull(df[df.columns[2]])]
    df = df[df[df.columns[2]] != '']
    df = df[df[df.columns[2]] != 'nan']
    df['wiki'] = df.wiki.apply(lambda x: x.lower().strip())
    df['Best Entity literalString'] = df['Best Entity literalString'].apply(lambda x: x.lower().strip())  
    df['wiki'] = df['wiki'].map(lambda x: re.sub(r'[^\x00-\x7F]','',str(x)))
    df2 = pd.DataFrame(np.dot(model,np.transpose(vec.transform([user_input]).toarray())))
    df2['disease'] = df['Best Entity literalString']
    df2.columns = ['score', 'disease']

    diseases = df2.sort('score', ascending=[0])[['score, disease']]   

    return render_template('dashboard.html', text_analytics = json.dumps(azure_key_phrases), search_query=json.dumps(all_text), azure_sentiment = (azure_sentiment*100), severity=severity, diseases=diseases[:5])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
