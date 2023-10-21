import pandas as pd, csv, numpy as np

"""
CSV Format

username,travelFreq,travelInterest,occupation,income,creditScore,budget
"""

# Similarity of users
"""
Data representation:
travel freq: bool
travel interest: bool
occupations- student, early professional, mid-career, business owner, freelance, executive, unemployed 
credit score- poor, fair, good, great, excellent
income
budget
tags

liked cards
disliked cards
"""

"""student - occupation:student"""
"""business - occupation:business owner,freelance,executive"""
"""travel - moderate-high travel freq; moderate-high travel interest"""
"""elite - occupation:mid-career,business owner,executive ; credit score: great,exellent ; income:100 000+ ; budget:100+"""
users = pd.read_csv("users.csv")
fobj = open("bin_users.csv", "a")
fieldnames = [
    "username",
    "fingerprint",
]  # TODO fill this in
refined_users = csv.DictWriter(fobj, fieldnames=fieldnames)
refined_users.writeheader()
occupations = [
    "student",
    "earlyProfessional",
    "midCareer",
    "businessOwner",
    "freelance",
    "executive",
    "unemployed",
]
credit_ranges = ["poor", "fair", "good", "great", "excellent"]

for (
    idx,
    row,
) in users.iterrows():
    user_fingerprint = ""
    # Binary representation of user's associated tags
    # [student,business,travel,elite]
    user_fingerprint += str(int(row["occupation"] == occupations[0]))
    user_fingerprint += str(int(row["occupation"] in occupations[3:6]))
    user_fingerprint += str(int(row["travelFrequency"] or row["travelInterest"]))
    user_fingerprint += str(
        int(
            (row["occupation"] in occupations[2:4] + [occupations[5]])
            or row["creditScore"] in credit_ranges[3:]
            or row["income"] >= 100000
            or row["budget"] >= 100
        )
    )

    # Dump into another csv file
    refined_users.writerow([row["username"], user_fingerprint])


# occupation:mid-career,business owner,executive ; credit score: great,exellent ; income:100 000+ ; budget:100+

# Tags: student (based on occupation),
# business (based on occupation),
# travels (based on travel freq and travel interest),
# cash back (everyone),
# elite (based on occupations, credit score, income, budget),
# store (recommended to everyone; user filters out whether or not they want to see it)


# Card recommendations based on similar users
