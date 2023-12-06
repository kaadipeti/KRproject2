import json
import os

file = '/Users/anuragpandit/PycharmProjects/dlproject2/example-argumentation-framework.json'

with open(file, 'r') as infile:
    data = json.load(infile)
    loaded = json.dumps(data, indent=4)
    print(loaded)