import json

# Read the JSONL file and process each line
input_file = "Hyperloo/graph/test.jsonl"
output_file = "output.json"

parsed_courses = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        course = json.loads(line)
        
        # Convert "tree" field from a string to a proper nested JSON object
        if "tree" in course and isinstance(course["tree"], str):
            try:
                course["tree"] = json.loads(course["tree"].replace("\\n", "").replace("\\", ""))
            except json.JSONDecodeError:
                print(f"Error parsing tree for course {course['course_id']}")
                course["tree"] = {}
        
        parsed_courses.append(course)

# Save the cleaned JSON data
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(parsed_courses, f, indent=4)

print(f"Processed {len(parsed_courses)} courses and saved to {output_file}")
