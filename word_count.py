# create a Flask microservice to input a list the words and returns the list of words with the word count.
# It exposes a POST API for the following operations.
# • POST /wordcount

from flask import Flask
from flask import request

app=Flask(__name__)

@app.route("/wordcount",methods=["POST"])
def wordcount():
    words=request.form["words"]
    wordlist=words.split(",")
    return "<p>The words are {0} and the word count is {1}</p>".format(wordlist,len(wordlist))