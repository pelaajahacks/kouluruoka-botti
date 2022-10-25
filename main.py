from keep_alive import keep_alive
from rating import get_rating
from colors import reset, colors

keep_alive()

import requests
import threading
import sys
from colorama import init as colorama_init
import asyncio
import aiohttp
import json
import datetime
import random
from json.decoder import JSONDecodeError

import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler("like.logs"),
        # logging.StreamHandler(sys.stdout)
    ]
)


time.sleep(1)

likes = 0
failed = 0

colorama_init()

mealguids = {
    "last-checked": {
        "started": "",
        "finished": ""},
    "mealguids": [
    
    ],
    "skipped_urls": ""
}

ok = "https://kouluruoka.fi/page-data/sq/d/362501671.json"
url_base = "https://kouluruoka.fi/page-data/menu/"

urls = [
]

skipped_urls = []

schools = requests.get(ok).json()

for school in schools["data"]["allAzureJson"]["nodes"]:
    urls.append(url_base+school["WeekMenu"][0]["RestaurantId"]+"/page-data.json")
    urls.append(url_base+school["WeekMenu"][0]["RestaurantId"]+"/2/page-data.json")

print(reset + "[", end="")


#urls = ["https://kouluruoka.fi/page-data/menu/espoo_saarnilaaksonkoulu/page-data.json"]


with open("mealguids.json", "r") as file:
    try:
        file_mealguids = json.loads(file.read())
    except JSONDecodeError:
        print("file empty?")
        file_mealguids = {
            "last-checked": {
                "started": "",
                "finished": ""},
            "mealguids": [
            
            ],
            "skipped_urls": ""
        }
        
        




async def get_menu():
    mealguids["last-checked"]["started"] = str(datetime.datetime.now())
    b = 0
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(urls):
            if b >= len(colors)-1: b = 0
            else: b += 1
            if url not in file_mealguids["skipped_urls"]:
                
                tasks = []
                cant_append = False
                r = None
                counter = 0
                while not r:
                    counter += 1
                    try:
                        r = requests.get(url)
                        print(r, url)
                    except:
                        pass
                    try:
                        if counter > 10 or r.status_code == 404:
                            cant_append = True
                            r = {"segso": "tosi hupsu"}
                    except:
                        pass
                
                
                if not cant_append: 
                    r = r.json()
                    print(colors[b] + "*", end="")
                    sys.stdout.flush()
                    lmaoo = []
                    if r["result"]["pageContext"]["menu"]["Days"] != []:
                        for i, key in enumerate(r["result"]["pageContext"]["menu"]["Days"]):
                                
                            for key2 in key["Meals"]:
                                foodType = key2["MealType"]
                                foodName = key2["Name"]
                                guid = key2["MealGuid"]
                                ratingHash = session.get(
                                    
                                    f"https://kouluruoka.fi/api/likes/?code=caYXsUsWXRJ9qWGkS430nkCLAxrAaDcKT2swb8hJT6cIapHXMC9iBA==&id={guid}"
                                )
                                
                                foodDict = {
                                    "mealGuid": guid,
                                    "name": foodName,
                                    "type": get_rating(foodName)
                                }
                                cant_append = False
                                for mealguid in mealguids["mealguids"]:
                                    if guid == mealguid["mealGuid"]:
                                        cant_append = True
                                        break
                                    
                                
                                lmaoo.append(foodDict)
                                tasks.append(ratingHash)
                                

                    else:
                        cant_append = True
                if not cant_append:
                    
                    responses = await asyncio.gather(*tasks)
                    results = []
                    for response in responses:
                        results.append(await response.json())
                    for a, result in enumerate(results):
                        lmaoo[a]["ratingHash"] = result["ratingHash"]
                        print(lmaoo[a])
                    
                    for lmao in lmaoo:
                        mealguids["mealguids"].append(lmao)
                if cant_append:
                    skipped_urls.append(url)
                cant_append = False
            else:
                #print("Skipped url", url)
                skipped_urls.append(url)
    mealguids["last-checked"]["finished"] = str(datetime.datetime.now())
    for mealguid in file_mealguids["mealguids"]:
        mealguids["mealguids"].append(mealguid)
            
                               
if "y" in input(colors[random.randint(0, len(colors)-1)] + "Do you want to check for new meals to likebot? >>> ").lower():
    asyncio.run(get_menu())
    print(reset + "]")
    mealguids["skipped_urls"] = skipped_urls
    with open("mealguids.json", "w") as file:
        file.write(json.dumps(mealguids, indent=4))
else:
    mealguids = file_mealguids
    



headers = {
    "User-Agent":
    "Goofy ahh uncle like bot kouluruoka.fi on ihan goofy ahh https://segso.net parempi!"
}

mealguids_length = len(mealguids["mealguids"])
def send_function(threadnum=0, threadcount=0):
    global data, headers, colors, likes, failed, mealguids_length
    a = 0
    
    while True:
        try:
            for count, guid in enumerate(mealguids["mealguids"]):
                r = requests.post(
                    "https://kouluruoka.fi/api/like?code=S3iK1RelmyWDSgcLFb0KnR7LPuw5J3xE8H4uP1L-n6QfAzFupAkHfQ==",
                    json=guid,
                    headers=headers)
                success = None
                if guid["type"] == 0: disliked_or_liked = "DISLIKED!"
                else: disliked_or_liked = "LIKED!"
                if r.status_code in (200, 204):
                    likes += 1
                    success = True
                elif r.status_code == 503:
                    failed += 1
                    print("Nyt meni nippuun!")
                    disliked_or_liked = "FAILED!"
                    success = False
                else:
                    failed += 1
                    disliked_or_liked = "FAILED!"
                    success = False
                name = guid["name"].split(",")[0]
                if not success: name = ""
                h = f"{disliked_or_liked} {name} R Code: {r.status_code}. botting: {count}/{mealguids_length}. threadcount: {threadnum}/{threadcount} likes sent: {likes} FAILED: {failed}"
                if r.status_code == 503 or likes % 500 == 0:
                    logging.info(h)
                print(colors[a], h)
                if a >= len(colors) - 1:
                    a = 0
                a += 1
        except Exception as e:
            failed += 1
            logging.info(str(e) + " failed")
            print("hupsu virhe!", e)


threads = []
threadcount = 696
for i in range(threadcount):
    t = threading.Thread(target=send_function, args=(i, threadcount))
    t.daemon = True
    threads.append(t)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
