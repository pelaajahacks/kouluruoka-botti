def get_rating(food):

    good_foods = [
        "pinaattilettu", "pinaattiletut", "kalaleike", "kalapuikko",
        "kananugetti", "kananuggetti", "lohkoperuna", "pipari", "kakku",
        "torttu", "jäätelö", "toiveruoka", "nugetti", "nuggetti", "kebab",
        "perunamuusi", "perunasose", "tortilla", "taco", "hampurilainen",
        "burger", "pizza", "pitsa", "lasagnette", "lasagna",
        "koululaisen kalaleike", "pestopasta", "pasta", "pinaatti", "nakki",
        "nakkikeitto", "kasvisnakkikeitto", "tomaatti", "pihvi", "possuhöystö",
        "spagettivuoka", "pasta", "ketsuppi", "tomaattikastike", "chili",
        "pinaattiohukaiset", "kasvis-jalapenonugetit",
        "pinaatti-pestopastavuoka", "kebabkastike"
    ]
    bad_foods = [
        "härkäpapu", "papu", "sieni", "sosekeitto", "rucola", "kikherne",
        "parsa", "kaali", "vuohenjuusto", "paprika", "feta", "lanttu",
        "kesäkurpitsa", "palsternakka", "punajuuri", "tofu", "nokkos",
        "nokkonen", "juuressose", "herkkusieni", "kanttarelli", "tatti",
        "purjo", "selleri", "kaalikääryle", "kevätkääryle", "kukkakaali",
        "lehtikaali", "kookos", "beanit", "falafel", "keitto", "lihakeitto",
        "juusto", "broileri-juustopasta", "broileri", "juustopasta", "vaalea",
        "vaaleakastike", "punajuuripihvi", "kikhernepastavuoka",
        "Italialainen jauhelihakeitto", "papukeitto", "kookos",
        "kookoscurrykala", "Appelsiinitofu", "Quorn-makaronilaatikko", "Quorn", "Taco-broilerivuoka", "broilerivuoka", "Mifu", "Mifu-pinaattikiusaus", "Mifu-pinaatti", "kiusaus", "possuhöystö", "possu", "höystö"
    ]
    hard_coded = ["Quorn"]
    bad = 0
    neutral = 1
    good = 1
    goods = neutrals = bads = 0
    bad_or_good = neutrals

    for good_food in good_foods:
        if good_food.lower() in food.lower(): goods = goods + 1
        else: neutrals = neutrals + 1
    for bad_food in bad_foods:
        if bad_food.lower() in food.lower(): bads += 1

    for hard_coded_food in hard_coded:
        if hard_coded_food.lower() in food.lower(): bads += 999999
    if goods > bads: bad_or_good = good
    if bads > goods: bad_or_good = bad
    if bads == goods or neutral > bads and neutral > goods:
        bad_or_good = neutral

    return bad_or_good