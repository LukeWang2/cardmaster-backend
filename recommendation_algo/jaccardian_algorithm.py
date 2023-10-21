# Similarity of users
"""
Data representation:
travel freq
travel interest
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
"""elite - occupation:mid-career,business owner,executive ; credit score: great,exellent ; income:high ; budget:high"""

# Binary representation of user's associated tags
user_fingerprint = ""

# Tags: student (based on occupation),
# business (based on occupation),
# travels (based on travel freq and travel interest),
# cash back (everyone),
# elite (based on occupations, credit score, income, budget),
# store (recommended to everyone; user filters out whether or not they want to see it)


# Card recommendations based on similar users
