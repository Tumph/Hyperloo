import json

with open('stem_majors.json', 'r') as f:
    data = json.load(f)


majors = 0
courses = 0

for major in data:
    print(f"Major: {major['major_name']}")
    majors+=1

    for course in major['courses']:
        courses+=1


print(f"Total majors: {majors}")
print(f"Total courses: {courses}")
