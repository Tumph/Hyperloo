import json

# Load the JSON file
with open('../../NLP/Processing/chunks/syllabi_chunk_19.json', 'r') as file:
    data = json.load(file)

# Count the number of objects
if isinstance(data, list):
    print(len(data))
else:
    print("The JSON file does not contain an array of objects.")
