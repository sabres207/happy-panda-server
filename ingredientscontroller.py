from fatsecret import Fatsecret
import sys
import json
method = sys.argv[1]
argument = sys.argv[2]

fs = Fatsecret("21a6cd97e2644a00a7fc7c7d7ae00527", "392dba9edc6b40fe8ef11f860f9043f9")

with open("ingrid.txt", "w+") as f_out:
    result = getattr(fs, method)(argument)
    result_json = json.dumps(result)
    f_out.write(result_json)
