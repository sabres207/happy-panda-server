import recipeshelper

helper = recipeshelper.RecipesHelper()

higher_nutritions = [
    'calories',  # kcal
    'carbohydrate',  # grams
    'protein',  # grams
    'saturated_fat',  # grams
    'trans_fat',  # grams
    'cholesterol',  # milligrams
    'sodium',  # milligrams
    'potassium',  # milligrams
    'sugar',  # grams
    'fibre'  # grams
]

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
    'calories': 2500,
    'protein':  50,  # grams
    'fat':  70,  # grams
    'carbohydrate':  310,  # grams
    'saturated_fat': 23,  # grams
    'sugar':  90,  # grams
    'sodium':  2300,  # milligrams
    'fibre':  30,  # grams
    'cholesterol':  300,  # milligrams
    'potassium':  5000  # milligrams 'iron': 8  # mg
}

women_nutritions_guides = {
    'calories': 2000,
    'protein':  46,  # grams
    'fat':  70,  # grams
    'carbohydrate':  310,  # grams
    'saturated_fat': 23,  # grams
    'sugar':  90,  # grams
    'sodium':  2300,  # milligrams
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
        servings = {}
        try:
            servings = meal['serving_sizes']['serving']
        except:
            servings = {}

        if intake in servings:
            if intake in sumintakes:
                sumintakes[intake] += float(servings[intake])
            else:
                sumintakes[intake] = float(servings[intake])

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
            # print nutrition, user_guide[nutrition], intakes[nutrition], (intakes[nutrition] / user_guide[nutrition]) * 100
            new_intakes[nutrition] = (intakes[nutrition] / user_guide[nutrition]) * 100

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

    return sum_intakes(intakes, user, len(user['daily_meals']))


#def compare_dishes(dish, other_dish):