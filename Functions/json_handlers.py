import json

def read_json(path):
    try:
        with open(path, 'r', encoding="UTF-8") as f:
            return json.load(f)
    except:
        return {}

def write_json(path, data):

    old_data = read_json(path)
    data.update(old_data)

    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data,f,indent=2)
