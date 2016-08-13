import recipeshelper

helper = recipeshelper.RecipesHelper()

fat_secret_nutritions = [
    'calories',  # kcal
    'carbohydrate',  # grams
    'protein',  # grams
    'fat',  # grams
    'saturated_fat',  # grams
    'trans_fat',  # grams
    'cholesterol',  # milligrams
    'sodium',  # milligrams
    'potassium',  # milligrams
    'sugar',  # grams
    'fibre'  # grams
]

fat_secret_percents = [
    'vitamin_a',
    'vitamin_c',
    'calcium',
    'iron'
]

men_nutritions_guides = {
    'energy': 8700,  # kilojoules
    'protein':  50,  # grams
    'fat':  70,  # grams
    'carbohydrate':  310,  # grams
    'saturated_fat': 30,  # grams
    'sugar':  90,  # grams
    'sodium':  2.3,  # grams
    'fibre':  30,  # grams
    'cholesterol':  300,  # milligrams
    'potassium':  5000  # milligrams 'iron': 8  # mg
}

women_nutritions_guides = {
    'energy': 8700,  # kilojoules
    'protein':  50,  # grams
    'fat':  70,  # grams
    'carbohydrate':  310,  # grams
    'saturated_fat': 20,  # grams
    'sugar':  90,  # grams
    'sodium':  2.3,  # grams
    'fibre':  25,  # grams
    'cholesterol':  300,  # milligrams
    'potassium':  5000  # milligrams 'iron': 17  # mg
}

'''
   status API example
    {
    "energy": 12,
    "protein":  50,
    "fat":  70,
    "carbohydrate":  93.2,
    "saturated_fat": 30.4,
    "sugar":  90.2,
    "sodium":  42.3,
    "fibre":  30,
    "cholesterol":  76,
    "potassium":  22,
  "vitamin_a": 90,
  "vitamin_c": 10,
  "calcium": 23,
  "iron": 12
}
'''


def meal_id_to_obj(mealid):
    return helper.get_recipe_by_id(mealid)


def meal_to_intakes(sumintakes, meal):
    all_intakes = fat_secret_nutritions + fat_secret_percents
    for intake in all_intakes:
        if intake in meal:
            if intake in sumintakes:
                sumintakes[intake] += meal[intake]
            else:
                sumintakes[intake] = meal[intake]

    return sumintakes


def get_guide(user):
    if 'gender' in user:
        if user['male']:
            return men_nutritions_guides
        else:
            return women_nutritions_guides

    return men_nutritions_guides


def sum_intakes(intakes, user, meals_len):
    new_intakes = {}
    user_guide = get_guide(user)

    for nutrition in user_guide:
        if nutrition in intakes:
            new_intakes[nutrition] = (user_guide[nutrition] / intakes[nutrition]) * 100

    for nutrition in fat_secret_percents:
        if nutrition in intakes:
            new_intakes[nutrition] = intakes[nutrition] / meals_len

    return new_intakes


def status(user):
    if 'daily_meals' not in user:
        return {}

    ids = user['daily_meals']
    meals = map(meal_id_to_obj, ids)
    intakes = reduce(meal_to_intakes, meals, {})

    return sum_intakes(intakes, user, len(user['dail_meals']))
