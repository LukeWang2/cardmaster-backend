import pandas as pd, numpy as np
from bitarray import bitarray
from flask import Flask, request
from userToBin import userToBin
from sklearn.linear_model import LinearRegression

app = Flask(__name__)


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

    users = pd.read_csv("bin_users.csv")
    sim_cards = np.ndarray((len(users.columns) - 2, len(users)))
    for idx, row in users.iterrows():
        binary = bitarray(row["fingerprint"])
        fprintbinary = bitarray(fprint)
        differences = binary ^ fprintbinary
        num_differences = differences.count(1)
        user_similarity = 1 - (num_differences / 4)
        for i in range(len(users.columns)):
            sim_cards = users.iloc[:, i + 2]
