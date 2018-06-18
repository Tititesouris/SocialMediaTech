import json
import os
import re

from textblob import TextBlob
from textblob_de import TextBlobDE as TextBlobDE
from textblob_fr import PatternTagger as TaggerFR, PatternAnalyzer as AnalyzerFR
from polyglot.text import Text

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


def getSentiment(tweet, language):
    if language == "en":
        analysis = TextBlob(tweet)
        return {"polarity": analysis.sentiment.polarity, "subjectivity": analysis.sentiment.subjectivity}
    elif language == "de":
        analysis = TextBlobDE(tweet)
        return {"polarity": analysis.sentiment.polarity, "subjectivity": analysis.sentiment.subjectivity}
    elif language == "hr":
        analysis = Text(tweet)
        return {"polarity": analysis.polarity, "subjectivity": 0}
    elif language == "fr":
        analysis = TextBlob(tweet, pos_tagger=TaggerFR(), analyzer=AnalyzerFR())
        return {"polarity": analysis.polarity, "subjectivity": analysis.subjectivity}
    elif language == "und":  # Undefined
        try:
            analysis = Text(tweet)
            return {"polarity": analysis.polarity, "subjectivity": 0}
        except Exception:
            return None
    return None


def extractInfo(tweet):
    information = {}
    if not all(key in tweet.keys() for key in ["text", "lang", "user"]):
        return None
    information["text"] = tweet["text"]
    try:
        information["user_id"] = tweet["user"]["id"]
        information["user"] = tweet["user"]["name"]
    except Exception:
        return None
    information["lang"] = (tweet["lang"] + "-").split("-")[0]
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
            return None
        information["place"] = {
            "bounding_box": boundingBox,
            "name": name,
            "country": country,
            "full_name": fullName,
            "country_code": countryCode
        }
    else:
        return None

    information["created_at"] = tweet["created_at"] if ("created_at" in tweet.keys()) else None
    sentiment = getSentiment(information["text"], information["lang"])
    if sentiment is None:
        return None
    information["sentiment"] = sentiment
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
            tweet = extractInfo(json.loads(line))
            if tweet is not None:
                tweets.append(tweet)
    print(str(len(tweets)) + " tweets")

goodTweets = []
for tweet in tweets:
    for country, targets in countries.items():
        if isFromCountry(tweet, country):
            for target, keywords in targets.items():
                if any(keyword in tweet["text"] for keyword in keywords):
                    tweet["origin"] = country
                    tweet["target"] = target
                    goodTweets.append(tweet)

print(str(len(goodTweets)) + " tweets left")
for i in range(len(goodTweets) - 1, -1, -1):
    if [re.sub("https?:\/\/.*\b", "", goodTweets[i]["text"]), goodTweets[i]["user_id"]] in [
        [re.sub("https?:\/\/.*\b", "", tweet["text"]), tweet["user_id"]] for index, tweet in
        enumerate(goodTweets) if index != i
    ]:
        goodTweets.pop(i)

print(str(len(goodTweets)) + " tweets left")
for tweet in goodTweets:
    with open("analysed/" + tweet["origin"] + "/" + tweet["target"] + ".json", "a") as file:
        file.write(json.dumps(tweet) + "\n")
