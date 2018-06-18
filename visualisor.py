import os
import json

data = {}
counts = {}
selfImage = {}
othersImage = {}
for country in os.listdir("analysed/"):
    counts[country] = {}
    selfImage[country] = {"score": 0, "negative": 0, "positive": 0, "neutral": 0}
    othersImage[country] = {}
    for filename in os.listdir("analysed/" + country):
        with open("analysed/" + country + "/" + filename, "r") as f:
            target = filename.strip(".json")
            counts[country][target] = 0
            othersImage[country][target] = {"score": 0, "negative": 0, "positive": 0, "neutral": 0}
            for line in f:
                counts[country][target] += 1
                polarity = float(json.loads(line)["sentiment"]["polarity"])
                if target == country:
                    selfImage[country]["score"] += polarity
                    selfImage[country]["negative" if polarity < 0 else "positive" if polarity > 0 else "neutral"] += 1
                else:
                    othersImage[country][target]["score"] += polarity
                    othersImage[country][target]["negative" if polarity < 0 else "positive" if polarity > 0 else "neutral"] += 1
data["counts"] = counts
data["self_image"] = selfImage
data["others_image"] = othersImage
with open("visualisations/data.json", "w+") as file:
    file.write(json.dumps(data) + "\n")
