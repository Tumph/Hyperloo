import json

def remove_duplicates(input_file, output_file):
    # Load the JSON data
    with open(input_file, 'r') as f:
        courses = json.load(f)

    seen = set()
    unique_courses = []

    # Define key fields for uniqueness check
    key_fields = [
        'course_id', 'course_code', 'course_name',
        'term_name', 'program_name', 'program_id',
        'major_id', 'major_name'
    ]

    for course in courses:
        # Create unique identifier tuple
        identifier = tuple(str(course[field]) for field in key_fields)

        if identifier not in seen:
            seen.add(identifier)
            unique_courses.append(course)

    # Save deduplicated data
    with open(output_file, 'w') as f:
        json.dump(unique_courses, f, indent=4)

# Example usage:
remove_duplicates('syllabi2.json', 'deduplicated_courses.json')
