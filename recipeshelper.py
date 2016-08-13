from fatsecret import Fatsecret


class RecipesHelper(object):

    def __init__(self, consumer_key="21a6cd97e2644a00a7fc7c7d7ae00527",
                 consumer_secret="392dba9edc6b40fe8ef11f860f9043f9"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.fatty = Fatsecret(self.consumer_key, consumer_secret)

    def get_recipe_by_id(self, recipe_id):
        try:
            recipe_dict = self.fatty.recipe_get(recipe_id)
            return recipe_dict
        except Exception:
            return {}