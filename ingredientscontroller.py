from fatsecret import Fatsecret

fs = Fatsecret("21a6cd97e2644a00a7fc7c7d7ae00527", "392dba9edc6b40fe8ef11f860f9043f9")

fs.foods_search("tofu")

dir(fs)