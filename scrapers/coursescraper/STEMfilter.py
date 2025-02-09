import json
import re

def filter_stem_majors(input_file, output_file):
    # Expanded STEM keywords with regex patterns
    stem_patterns = [
        r'\b(computer|comp)\b',
        r'\bscience\b',
        r'\bengineer\w*',  # Matches engineering, engineer, etc.
        r'\bphysics\b',
        r'\bmath\w*',      # Matches math, mathematics, etc.
        r'\bapplied\s+(math|science|physics)\b'
    ]

    with open(input_file, 'r') as f:
        data = json.load(f)

    # Process nested structure from scraping code
    filtered_majors = []
    for major in data:
        if any(re.search(pattern, major.get('major_name', '').lower())
               for pattern in stem_patterns):
            # Filter courses within STEM majors
            filtered_courses = [
                course for course in major['courses']
                if any(re.search(pattern, course[1].lower())
                      for pattern in stem_patterns)
            ]
            major['courses'] = filtered_courses
            filtered_majors.append(major)

    with open(output_file, 'w') as f:
        json.dump(filtered_majors, f, indent=2)

    return len(data) - len(filtered_majors)


# Example usage:
removed_count = filter_stem_majors('course2.json', 'stem_majors.json')
print(f"Removed {removed_count} non-STEM entries")
