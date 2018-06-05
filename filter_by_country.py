import json

'''
What is in a tweet:
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
'''


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

for i in range(31):
    with open("data/" + str(i) + ".json", "r") as f:
        for line in f.readlines():
            tweets.append(extractInfo(json.loads(line)))
    print(str(len(tweets)) + " tweets")
with open("data/US.json", "a") as us:
    for tweet in tweets:    
        if tweet["place"]["country_code"] == 'US':
            us.write(json.dumps(tweet) + "\n")

with open("data/AU.json", "a") as au:
    for tweet in tweets:    
        if tweet["place"]["country_code"] == 'AU':
            au.write(json.dumps(tweet) + "\n")

with open("data/HR.json", "a") as hr:
    for tweet in tweets:    
        if tweet["place"]["country_code"] == 'HR':
            hr.write(json.dumps(tweet) + "\n")

with open("data/GB.json", "a") as gb:
    for tweet in tweets:    
        if tweet["place"]["country_code"] == 'GB':
            gb.write(json.dumps(tweet) + "\n")

with open("data/FR.json", "a") as fr:
    for tweet in tweets:    
        if tweet["place"]["country_code"] == 'FR':
            fr.write(json.dumps(tweet) + "\n")             
            






