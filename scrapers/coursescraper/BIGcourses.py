
import json

def count_majors_with_many_topics(json_data):
    try:
        data = json.loads(json_data)
        return sum(1 for major in data if len(major.get('courses', [])) > 200)
    except json.JSONDecodeError:
        print("Invalid JSON format")
        return 0

# Example usage
with open('stem_majors2.json', 'r') as f:
    data = f.read()
    result = count_majors_with_many_topics(data)
    print(f"Majors with >100 topics: {result}")
