import numpy as np
from bitarray import bitarray
import csv, os
from flask import Flask, request
from userToBin import userToBin
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

cards = ["card1", "card2"]


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    {"occupation":occupation
    "travelFrequency":travelFrequency
    "travelInterest":travelInterest
    "creditScore":creditScore
    "income":income
    "budget":budget
    }
    """
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.json
    else:
        return "Not JSON"
    occupation = data.get("occupation")
    travelFrequency = data.get("travelFrequency")
    travelInterest = data.get("travelInterest")
    creditScore = data.get("creditScore")
    income = data.get("income")
    budget = data.get("budget")

    fprint = userToBin(
        occupation, travelFrequency, travelInterest, creditScore, income, budget
    )

    fobj = open("bin_users.csv")

    nRows = len(fobj.readlines()) - 1
    fobj.close()

    fobj = open("bin_users.csv")
    data = csv.DictReader(fobj)
    sim_cards = np.zeros((len(cards), nRows))
    user_sims = np.zeros((len(cards), nRows))
    print(sim_cards, user_sims)
    for idx, row in enumerate(data):
        binary = bitarray(row["fingerprint"])
        fprintbinary = bitarray(fprint)
        differences = binary ^ fprintbinary
        num_differences = differences.count(1)
        user_similarity = 1 - (num_differences / 4)
        for i in range(len(cards)):
            sim_cards[i][idx] = row[cards[i]]
            user_sims[i][idx] = user_similarity
    recommends = {}
    for j in range(len(cards)):
        x = user_sims[j].reshape((-1, 1))
        y = sim_cards[j]
        model = LinearRegression().fit(x, y)
        recommends[cards[j]] = bool((model.intercept_ + model.coef_) > 0.5)
    fobj.close()
    return recommends


if __name__ == "__main__":
    app.run(port=os.getenv("PORT", 8000))

# cards = ["card1", "card2"]  # TODO gen list of cards

# fprint = userToBin("midCareer", True, True, "great", "55000", "200")
# fobj = open("bin_users.csv")

# nRows = len(fobj.readlines()) - 1
# fobj.close()

# fobj = open("bin_users.csv")
# data = csv.DictReader(fobj)
# sim_cards = np.zeros((len(cards), nRows))
# user_sims = np.zeros((len(cards), nRows))
# print(sim_cards, user_sims)
# for idx, row in enumerate(data):
#     binary = bitarray(row["fingerprint"])
#     fprintbinary = bitarray(fprint)
#     differences = binary ^ fprintbinary
#     num_differences = differences.count(1)
#     user_similarity = 1 - (num_differences / 4)
#     for i in range(len(cards)):
#         sim_cards[i][idx] = row[cards[i]]
#         user_sims[i][idx] = user_similarity
# recommends = {}
# for j in range(len(cards)):
#     x = user_sims[j].reshape((-1, 1))
#     y = sim_cards[j]
#     model = LinearRegression().fit(x, y)
#     recommends[cards[j]] = bool((model.intercept_ + model.coef_) > 0.5)
# print(recommends)
# fobj.close()
