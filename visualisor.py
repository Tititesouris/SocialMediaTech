import os
import json
import matplotlib.pyplot as plt

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
            if country != target:
                othersImage[country][target] = {"score": 0, "negative": 0, "positive": 0, "neutral": 0}
            for line in f:
                counts[country][target] += 1
                polarity = float(json.loads(line)["sentiment"]["polarity"])
                if target == country:
                    selfImage[country]["score"] += polarity
                    selfImage[country]["negative" if polarity < 0 else "positive" if polarity > 0 else "neutral"] += 1
                else:
                    othersImage[country][target]["score"] += polarity
                    othersImage[country][target][
                        "negative" if polarity < 0 else "positive" if polarity > 0 else "neutral"] += 1
data["counts"] = counts
data["self_image"] = selfImage
data["others_image"] = othersImage
with open("visualisations/data.json", "w+") as file:
    file.write(json.dumps(data) + "\n")

# Display settings
barWidth = 0.35
countryKeys = ["austria", "croatia", "france", "uk", "usa"]
countries = ["Austria", "Croatia", "France", "the UK", "the USA"]
colors = ["green", "brown", "blue", "purple", "red"]
OneToFive = [(i + 1) * (barWidth * 4) for i in range(5)]
happinessReport = [7.139, 5.321, 6.489, 6.814, 6.886]

# Counts for each country for each target

x = [[data["counts"][country][target] if country in data["counts"].keys() and target in data["counts"][
    country].keys() else 0 for country in countryKeys] for target in countryKeys]

for i in range(len(x)):
    if i > 0:
        plt.bar(OneToFive, x[i], barWidth, bottom=x[i - 1], color=colors[i])
    else:
        plt.bar(OneToFive, x[i], barWidth, color=colors[i])

plt.title("Number of tweets about countries per country")
plt.xlabel("Country of origin")
plt.ylabel("Number of tweets")
plt.xticks(OneToFive, countries)
plt.legend(countries)
plt.savefig("visualisations/count_tweets")

# What do countries think of themselves

x = [[data["self_image"][country][aspect] if country in data["self_image"].keys() else 0 for country in countryKeys] for
     aspect in ["positive", "negative", "neutral"]]

fig, ax = plt.subplots()
ax.bar([x - barWidth for x in OneToFive], x[0], barWidth, color="green")
ax.bar([x for x in OneToFive], x[1], barWidth, color="red")
ax.bar([x + barWidth for x in OneToFive], x[2], barWidth, color="blue")

plt.title("Number of tweets with sentiment per country about themselves")
plt.xlabel("Country")
plt.ylabel("Number of tweets")
plt.xticks(OneToFive, countries)
plt.legend(["Positive", "Negative", "Neutral"])
plt.savefig("visualisations/self_image")

# Comparison with World Happiness Report

x = [10 * data["self_image"][country]["score"] / (
        data["self_image"][country]["positive"] + data["self_image"][country]["negative"]) if country in data[
    "self_image"].keys() else 0 for country in countryKeys]

fig, ax = plt.subplots()
ax.bar([x - barWidth / 2 for x in OneToFive], x, barWidth, color="blue")
ax.bar([x + barWidth / 2 for x in OneToFive], happinessReport, barWidth, color="green")

plt.title("Happiness from tweets compared to the World Happiness Report")
plt.xlabel("Country")
plt.ylabel("Happiness score")
plt.xticks(OneToFive, countries)
plt.legend(["Happiness from tweets", "World Happiness Report"])
plt.savefig("visualisations/happiness_report")

# What do countries think of each other

for i, country in enumerate(countryKeys):
    countryKeysWithoutThisOne = countryKeys[:]
    countryKeysWithoutThisOne.pop(i)
    countriesWithoutThisOne = countries[:]
    countriesWithoutThisOne.pop(i)
    x = [[data["others_image"][country][target][aspect] if country in data["others_image"].keys() and target in
                                                           data["others_image"][country].keys() else 0 for target in
          countryKeysWithoutThisOne] for aspect in ["positive", "negative", "neutral"]]

    fig, ax = plt.subplots()
    ax.bar([x - barWidth for x in OneToFive[:-1]], x[0], barWidth, color="green")
    ax.bar([x for x in OneToFive[:-1]], x[1], barWidth, color="red")
    ax.bar([x + barWidth for x in OneToFive[:-1]], x[2], barWidth, color="blue")

    plt.title("Number of tweets with sentiment from " + countries[i] + " about other countries")
    plt.xlabel("Country")
    plt.ylabel("Number of tweets")
    plt.xticks(OneToFive[:-1], countriesWithoutThisOne)
    plt.legend(["Positive", "Negative", "Neutral"])
    plt.savefig("visualisations/others_image_" + country)
