import json
from rating import get_rating

with open("mealguids.json", "r") as file:
    mealguids = json.loads(file.read())

for count, mealguid in enumerate(mealguids["mealguids"]):
    mealguids["mealguids"][count]["type"] = get_rating(mealguid["name"])


with open("mealguids.json", "w") as file:
    file.write(json.dumps(mealguids, indent=4))
