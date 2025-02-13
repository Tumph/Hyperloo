import json
import re

def filter_missed_syllabi():
    """Filter syllabi using clean course code extraction"""
    try:
        # Extract ONLY course codes from messy file
        with open('misses_courses.txt', 'r') as f:
            course_code_pattern = re.compile(r'^([A-Z]{2,})\s(\d{3}[A-Z]?)')
            target_codes = []

            # Skip header lines until "Failed Courses:"
            found_header = False
            for line in f:
                line = line.strip()
                if "Failed Courses:" in line:
                    found_header = True
                    continue
                if found_header and line:
                    # Extract course code from lines like "SYDE 252 - Expecting value..."
                    match = course_code_pattern.match(line.split('-')[0].strip())
                    if match:
                        code = f"{match.group(1)} {match.group(2)}"
                        target_codes.append(code)

        print(f"Cleaned target codes: {target_codes[:10]}... (total: {len(target_codes)})")

        # Load syllabi data
        with open('../../../scrapers/scrapesyllabus/syllabi.json', 'r') as f:
            all_syllabi = json.load(f)

        # Match cleaned codes
        matched = [s for s in all_syllabi
                 if s.get('course_code') in target_codes]

        # Save results
        with open('missed_syllabi.json', 'w') as f:
            json.dump(matched, f, indent=2)

        print(f"Matched {len(matched)} syllabi")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    filter_missed_syllabi()
