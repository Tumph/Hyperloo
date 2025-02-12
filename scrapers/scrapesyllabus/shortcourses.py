import json

# Load the JSON data from file
with open('syllabi.json', 'r') as f:
    courses = json.load(f)

# Find courses with less than 5 topics

for course in courses:
    if 'topics' in course and len(course['topics']) < 5:
        print(f"{course['course_code']}: {course['course_name']}")
