
import json

with open("Hyperloo/scrapers/coursescraper/stem_majors.json", "r") as file:
    data = json.load(file)


result = []

for i in data:
    result.append(i["major_name"])
    
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)
