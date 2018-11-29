import logging

from flask import Flask, render_template, request, redirect, url_for

import requests
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

from google.appengine.ext import ndb
import tweepy
import time

class Twitter(ndb.Model):
    tweet_id = ndb.StringProperty()
    tweet_text = ndb.StringProperty()
    favorite_count = ndb.IntegerProperty()
    retweet_count = ndb.IntegerProperty()

consumer_key = "##############"
consumer_secret = "#################"
access_token = "####################"
access_token_secret = "################"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

app = Flask(__name__)



# [START form]
@app.route('/form',methods=['GET'])
def form():
    return render_template('form.html')
# [END form]

@app.route('/display',methods=['GET'])
def display():
    query_data = Twitter.query().fetch()
    #time.sleep(3)
    return render_template('display.html', data=query_data)

@app.route('/search_datastore_retrieve_form', methods=['POST'])
def search_datastore_retrieve_form():
    #import pdb; pdb.set_trace()
    tweet_text = request.form['tweet_text']
    result = Twitter.query().fetch()
    flag=0
    if result:
        for data in result:
            if data.tweet_text.replace(' ','').lower().find(tweet_text.replace(' ','').lower()) > -1:
                tweet_id= data.tweet_id
                tweet_text= data.tweet_text
                tweet_favorite_count= data.favorite_count
                tweet_retweet_count= data.retweet_count
                flag=1
                return render_template('datastore_retrieve_form.html',tweet_id=tweet_id, tweet_text=tweet_text, tweet_favorite_count=tweet_favorite_count, tweet_retweet_count=tweet_retweet_count)
    if flag==0:
        return render_template('search_error_form.html')

# [START submitted]
@app.route('/submitted_form', methods=['POST'])
@app.route('/error_form', methods=['POST'])
@app.route('/datastore_retrieve_form', methods=['POST'])
def submitted_form():
    #import pdb; pdb.set_trace()
    tweet_id = request.form['tweet_id']
    query = Twitter.query(Twitter.tweet_id == tweet_id)
    if query.fetch(1):
        for data in query.fetch(1):
            tweet_id= data.tweet_id
            tweet_text= data.tweet_text
            tweet_favorite_count= data.favorite_count
            tweet_retweet_count= data.retweet_count
            return render_template('datastore_retrieve_form.html',tweet_id=tweet_id, tweet_text=tweet_text, tweet_favorite_count=tweet_favorite_count, tweet_retweet_count=tweet_retweet_count)
    else:
        try:
            tweet = api.get_status(tweet_id) # id_list is the list of tweet ids
            time.sleep(2)
            tweet_text= tweet.text
            tweet_favorite_count= tweet.favorite_count
            tweet_retweet_count= tweet.retweet_count
            #task_key = datastore_client.key(kind, tweet_id)
            #task = datastore.Entity(key=task_key)
            task=Twitter()
            task.tweet_id=tweet_id
            task.tweet_text=tweet_text
            task.retweet_count=tweet_retweet_count
            task.favorite_count=tweet_favorite_count
            task.put()
            #print "###############",k
            return render_template('submitted_form.html',tweet_id=tweet_id, tweet_text=tweet_text, tweet_favorite_count=tweet_favorite_count, tweet_retweet_count=tweet_retweet_count)
        except:
            return render_template('error_form.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    #print e
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]