import json

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
    return information


tweets = []
with open("data/2018-05-18.json", "r") as f:
    for line in f.readlines():
        tweets.append(extractInfo(json.loads(line)))
print(str(len(tweets)) + " tweets")
for tweet in tweets:
    # Do the analysis
    print(tweet)
