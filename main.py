from optparse import BadOptionError
import requests
import threading
import sys
from colorama import init as colorama_init

colorama_init()




mealguids = []


colors = ["\033[31m", "\033[91m", "\033[33m", "\033[93m", "\033[32m", "\033[92m", "\033[34m", "\033[36m", "\033[94m", "\033[96m", "\033[35m", "\033[95m"]

def get_rating(food):
    

        good_foods = ["pinaattilettu", "pinaattiletut", "kalaleike", "kalapuikko", "kananugetti",
                      "kananuggetti",
                      "lohkoperuna", "pipari", "kakku", "torttu", "jäätelö", "toiveruoka", "nugetti",
                      "nuggetti",
                      "kebab", "perunamuusi", "perunasose", "tortilla", "taco", "hampurilainen", "burger",
                      "pizza",
                      "pitsa", "lasagnette", "lasagna", "koululaisen kalaleike", "pestopasta", "pasta", "pinaatti", "nakki", "nakkikeitto", "kasvisnakkikeitto", "tomaatti", "pihvi", "possuhöystö", "spagettivuoka", "pasta", "ketsuppi", "tomaattikastike", "chili", "pinaattiohukaiset", "kasvis-jalapenonugetit", "pinaatti-pestopastavuoka"]
        bad_foods = ["härkäpapu", "papu", "sieni", "sosekeitto",
                     "rucola", "kikherne", "parsa",
                     "kaali", "vuohenjuusto", "paprika", "feta", "lanttu",
                     "kesäkurpitsa", "palsternakka", "punajuuri",
                     "tofu", "nokkos", "nokkonen", "juuressose", "herkkusieni", "kanttarelli",
                     "tatti", "purjo", "selleri", "kaalikääryle", "kevätkääryle", "sipuli",
                     "kukkakaali", "lehtikaali", "kookos", "beanit",
                     "falafel", "keitto", "lihakeitto", "juusto", "broileri-juustopasta", "broileri", "juustopasta", "vaalea", "vaaleakastike", "punajuuripihvi", "kikhernepastavuoka", "Italialainen jauhelihakeitto", "papukeitto", "kookos", "kookoscurrykala", "Appelsiinitofu", ""]
        good = 1
        neutral = 1
        bad = 0
        bad_or_good = neutral
        goods = neutrals = bads = 0

        for i in range(len(good_foods)):
            if good_foods[i].lower() in food.lower():
                # print(f"Good food was: {good_foods[i].lower()}")
                goods = goods + 1
            else:
                # print(f"Neutral food was: {good_foods[i].lower()}")
                neutrals = neutrals + 1
        for i in range(len(bad_foods)):
            if bad_foods[i].lower() in food.lower():
                # print(f"Bad food was: {bad_foods[i].lower()}")
                bads = bads + 1
        if goods > bads:
            bad_or_good = good
        if bads > goods:
            bad_or_good = bad
        if bads == goods or neutral > bads and neutral > goods:
            bad_or_good = neutral

        return bad_or_good


urls = ["https://kouluruoka.fi/page-data/menu/espoo_saarnilaaksonkoulu/page-data.json", "https://kouluruoka.fi/page-data/menu/espoo_saarnilaaksonkoulu/2/page-data.json"]

for url in urls:
    r = requests.get(url).json()
    for key in r["result"]["pageContext"]["menu"]["Days"]:
        try:
            for key2 in key["Meals"]:
                foodType = key2["MealType"]
                foodName = key2["Name"]
                guid = key2["MealGuid"]
                ratingHash = requests.get(f"https://kouluruoka.fi/api/likes/?id={guid}").json()["ratingHash"]
                
                foodDict = {"mealGuid": guid,
                            "name": foodName,
                            "ratingHash": ratingHash,
                            "type": get_rating(foodName)}
                mealguids.append(foodDict)
        except Exception as e:
            print(e)
            pass


print(mealguids)


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"}

def send_function(threadnum=0, threadcount=0):
    global data, headers, colors
    a = 0
    while True:
        for count, guid in enumerate(mealguids):
            r = requests.post("https://kouluruoka.fi/api/like", json=guid, headers=headers)
            print(colors[a], f"R Code: {r.code}. botting: {count}/{len(mealguids)}. threadcount: {threadnum}/{threadcount} likes sent: {a * threadcount + threadnum}\n")
            a += 1
            

threads = []
threadcount = 10
for i in range(threadcount):
    t = threading.Thread(target=send_function, args=(i, threadcount))
    t.daemon = True
    threads.append(t)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()




