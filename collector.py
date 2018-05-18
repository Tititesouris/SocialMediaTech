# coding=utf-8
import json
import time

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = "2TzhW0ynFTRsrMXm0QV7OVnSr"
consumer_secret = "e5KlvERMPDjSIgjbWad5178YjQFizfjXiVUD9FdYNQUFELxqPo"
access_token = "361219031-aYNVhtzauKZ60L6Ehwzo0nUe4guXlwuBtFhYt7Rd"
access_token_secret = "1aoHOXfJutDLktFBDv5oLyvyqosojCCWKaJYL3J740g8k"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

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


class CountryListener(StreamListener):

    def on_data(self, rawData):
        try:
            data = json.loads(rawData)
            if "limit" in data.keys():
                with open("logs/limits", "a") as f:
                    f.write(data["limit"]["timestamp_ms"] + " | " + str(data["limit"]["track"]) + " | " + time.ctime(
                        int(data["limit"]["timestamp_ms"][:-3])) + "\n")
            else:
                if data["geo"] is not None or data["coordinates"] is not None or data["place"] is not None:
                    date = time.strftime("%Y-%m-%d")
                    with open("data/" + date + ".json", "a") as f:
                        f.write(json.dumps(data) + "\n")
            return True
        except BaseException as e:
            with open("logs/exceptions", "a") as f:
                f.write(str(time.time()) + " " + str(e) + "\n")
        return True

    def on_error(self, status):
        print("Error: " + str(status))
        if status == 420:
            return False
        return True


search = set([])
for country, targets in countries.items():
    for target, keywords in targets.items():
        search.update(keywords)
search = list(search)
print("Searching for " + str(search))
twitter_stream = Stream(auth, CountryListener())
twitter_stream.filter(track=search)
