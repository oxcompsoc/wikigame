# Stores the list of links for an article in a local JSON
import json, os

def path(name):
    name = ("".join([x for x in name if x.isalnum() or x.isspace() or x == '_']))
    return os.path.join("cache", name + ".json")

def put(name, links):
    if not os.path.exists("cache"):
        os.makedirs("cache")
    with open(path(name), 'w') as f:
        json.dump(links, f)

def get(name):
    p = path(name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None

def get_deadends():
    ds = get("_deadends")
    deadends = set()
    if ds:
        for d in ds: deadends.add(d)
    return deadends

def put_deadends(deadends):
    put("_deadends", list(deadends))
