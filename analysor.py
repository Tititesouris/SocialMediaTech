import json
import os
import re
import numpy as np
from textblob import TextBlob

'''
What is in a tweet:
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
'''

countriesEN = {
    "austria": ["austria"],
    "croatia": ["croatia"],
    "france": ["france"],
    "uk": ["united kingdom", "britain", " uk "],
    "usa": ["united states", "america", " usa "],
}

countries = {
    "austria": {
        "austria": ["österreich"],
        "croatia": ["kroatien"],
        "france": ["frankreich"],
        "uk": ["vereinigtes königreich", "britannien"],
        "usa": ["amerika"],
    },
    "croatia": {
        "austria": ["austrija"],
        "croatia": ["hrvatska"],
        "france": ["francuska"],
        "uk": ["velika britanija"],
        "usa": ["amerika"],
    },
    "france": {
        "austria": ["autriche"],
        "croatia": ["croatie"],
        "france": ["france"],
        "uk": ["royaume-uni", "royaume uni"],
        "usa": ["états-unis", "états uni", "etats-unis", "etats uni", "amérique", "amerique"],
    },
    "uk": countriesEN,
    "usa": countriesEN
}


def cleanText(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def getSentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity


def extractInfo(tweet):
    information = {}
    if "text" in tweet.keys():
        information["text"] = tweet["text"]
    if "coordinates" in tweet.keys():
        try:
            information["coordinates"] = [tweet["coordinates"]["coordinates"][1],
                                          tweet["coordinates"]["coordinates"][0]]
        except TypeError:
            information["coordinates"] = None
    if "place" in tweet.keys():
        try:
            boundingBox = tweet["place"]["bounding_box"]
        except TypeError:
            boundingBox = None
        try:
            name = tweet["place"]["name"]
        except TypeError:
            name = None
        try:
            country = tweet["place"]["country"]
        except TypeError:
            country = None
        try:
            fullName = tweet["place"]["full_name"]
        except TypeError:
            fullName = None
        try:
            countryCode = tweet["place"]["country_code"]
        except TypeError:
            countryCode = None
        information["place"] = {
            "bounding_box": boundingBox,
            "name": name,
            "country": country,
            "full_name": fullName,
            "country_code": countryCode
        }
    if "created_at" in tweet.keys():
        information["created_at"] = tweet["created_at"]
    information["sentiment"] = getSentiment(cleanText(information["text"]))
    return information


def isFromCountry(tweet, country):
    return tweet["place"]["country_code"] == {
        "austria": "AT",
        "croatia": "HR",
        "france": "FR",
        "uk": "GB",
        "usa": "US"
    }[country]


tweets = []

for filename in os.listdir("data/"):
    with open("data/" + filename, "r") as f:
        for line in f.readlines():
            tweets.append(extractInfo(json.loads(line)))
    print(str(len(tweets)) + " tweets")

for tweet in tweets:
    # Do the analysis
    for country, targets in countries.items():
        if isFromCountry(tweet, country):
            for target, keywords in targets.items():
                if any(keyword in tweet["text"] for keyword in keywords):
                    with open("analysed/" + country + "/" + target + ".json", "a") as file:
                        file.write(json.dumps(tweet) + "\n")
