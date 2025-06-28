import json

def read_json(path):
    try:
        with open(f"./Data/{path}.json", "r") as f:
            return json.load(f)
        
    except Exception as ex:
       print(f"Something went wrong - Error: {ex}")


def write_json(path, var):
    try:
        with open(f"./Data/{path}.json", "w") as f:
            json.dump(var, f, indent = 2)
            return True
        
    except Exception as ex:
       print(f"Something went wrong - Error: {ex}")
       return False