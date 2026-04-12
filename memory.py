import json

FILE_PATH = "memory.json"

def save_error(entry):
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_memory():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []