import json
import re

def analyze_courses(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    course_counter = {}
    all_courses = []
    unique_courses = set()
    pattern = re.compile(r'^[A-Z]{2,}\d{3}[A-Z]* - .+ \(\d\.\d{2}\)$')

    for major in data:
        major_name = major['major_name']
        valid_courses = []

        # Process each course group in the major
        for group in major['courses']:
            if isinstance(group, list) and len(group) >= 2:
                course_entry = group[1]  # Course is always in position 1
                if pattern.match(course_entry):
                    valid_courses.append(course_entry)
                    unique_courses.add(course_entry)

        course_counter[major_name] = len(valid_courses)
        all_courses.extend(valid_courses)

    return {
        'total_courses': len(all_courses),
        'courses_per_major': course_counter,
        'unique_courses': len(unique_courses)
    }

# Execution Example
results = analyze_courses('stem_majors.json')
print("\nCourses per Major:")
for major, count in results['courses_per_major'].items():
    print(f"{major}: {count}")
print(f"\nUnique Courses: {results['unique_courses']}")
print(f"Total Courses: {results['total_courses']}")
