import json
import re

def analyze_majors(json_data):
    total_majors = 0
    total_courses = 0
    course_pattern = re.compile(r'^[A-Z]{2,}\d{3}[A-Z]* - ')  # Matches course codes like "CHE102 - "

    for major in json_data:
        total_majors += 1
        courses = major.get('courses', [])

        # Count valid course entries using regex pattern
        course_count = sum(1 for item in courses
                         if isinstance(item, str) and course_pattern.search(item))

        total_courses += course_count

    return total_majors, total_courses

# Load JSON data (replace with your actual file path)
with open('stem_majors.json', 'r') as f:
    data = json.load(f)

majors_count, courses_count = analyze_majors(data)

print(f"Total number of majors: {majors_count}")
print(f"Total number of courses across all majors: {courses_count}")
