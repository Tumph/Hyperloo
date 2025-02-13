import re
import json
from pathlib import Path

def process_parallel_output():
    # Initialize totals and storage
    input_total = output_total = total_total = 0
    failed_courses = []

    try:
        # Read the output file
        output_path = Path('../parallel_output.txt')
        content = output_path.read_text()

        # Extract token usage with regex
        token_pattern = r'Token usage:\s*Input: (\d+)\s*Output: (\d+)\s*Total: (\d+)'
        token_matches = re.findall(token_pattern, content)

        # Calculate token totals
        for inp, outp, tot in token_matches:
            input_total += int(inp)
            output_total += int(outp)
            total_total += int(tot)

        # Extract failed courses with regex
        failed_pattern = r'Failed courses: (\[.*?\])'
        failed_matches = re.findall(failed_pattern, content)

        # Process failed courses
        for entry in failed_matches:
            try:
                # Normalize quotes for JSON parsing
                normalized = entry.replace("'", '"')
                courses = json.loads(normalized)
                failed_courses.extend(courses)
            except json.JSONDecodeError:
                continue

        # Write results to file
        with open('misses_courses.txt', 'w') as f:
            f.write(f"Total Input Tokens: {input_total}\n")
            f.write(f"Total Output Tokens: {output_total}\n")
            f.write(f"Total Tokens: {total_total}\n\n")
            f.write("Failed Courses:\n" + '\n'.join(failed_courses))

        return input_total, output_total, total_total, failed_courses

    except FileNotFoundError:
        print(f"Error: File {output_path} not found")
        return None

# Execute the processing
results = process_parallel_output()
