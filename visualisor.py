import os
import json
import matplotlib.pyplot as plt
import numpy as np

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
countries = ["Austria", "Croatia", "France", "United Kingdom", "USA"]
colors = ["green", "brown", "blue", "purple", "red"]
OneToFive = [1, 2, 3, 4, 5]

plt.title("Number of tweets about countries per country")
plt.xlabel("Country of origin")
plt.ylabel("Number of tweets")
plt.xticks(OneToFive, countries)

x = [[data["counts"][country][target] if country in data["counts"].keys() and target in data["counts"][
    country].keys() else 0 for country in countryKeys] for target in countryKeys]

for i in range(len(x)):
    if i > 0:
        plt.bar(OneToFive, x[i], barWidth, bottom=x[i - 1], color=colors[i])
    else:
        plt.bar(OneToFive, x[i], barWidth, color=colors[i])

plt.legend(countries)
plt.savefig("visualisations/count_tweets")

# TODO
# For each country get score and divide by (number of pos + number of neg), compare this number between countries, and then see if the order is similar to the happiness report, see if the differences are similar as well


exit()
N = 5
men_means = (20, 35, 30, 35, 27)
men_std = (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std)

women_means = (25, 32, 34, 20, 25)
women_std = (3, 5, 2, 3, 3)
rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

plt.show()
