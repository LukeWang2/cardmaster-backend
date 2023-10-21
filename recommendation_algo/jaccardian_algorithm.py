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
        occupation,
        travelFrequency == "true",
        travelInterest == "true",
        creditScore,
        income,
        budget,
    )

    # Get the number of rows in csv file (not using pandas b/c it can't deal w/ binary numbers)
    fobj = open("bin_users.csv")
    nRows = len(fobj.readlines()) - 1
    fobj.close()

    fobj = open("bin_users.csv")
    data = csv.DictReader(fobj)

    # Create arrays for user similarity and their credit card tastes
    sim_cards = np.zeros((len(cards), nRows))
    user_sims = np.zeros((len(cards), nRows))

    for idx, row in enumerate(data):
        binary = bitarray(row["fingerprint"])
        fprintbinary = bitarray(fprint)
        # Find the differences between the two user's
        differences = binary ^ fprintbinary
        num_differences = differences.count(1)
        # Calculate user similarity
        user_similarity = 1 - (num_differences / 4)
        # Populate arrays
        for i in range(len(cards)):
            sim_cards[i][idx] = row[cards[i]]
            user_sims[i][idx] = user_similarity

    recommends = {}
    # Get all relevant points and apply linear regression
    for j in range(len(cards)):
        x = user_sims[j].reshape((-1, 1))
        y = sim_cards[j]
        model = LinearRegression().fit(x, y)
        # Recommend card if there's over 50% chance that they will like it based
        # on similar users
        recommends[cards[j]] = bool((model.intercept_ + model.coef_) > 0.5)
    fobj.close()
    return recommends


if __name__ == "__main__":
    app.run(port=os.getenv("PORT", 8000))
