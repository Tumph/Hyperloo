from openai import OpenAI
import json
from tqdm import tqdm
import argparse
import time
import random

client = OpenAI()

def getTree(topics_str):
    retries = 3
    backoff_factor = 1.5

    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a helpful assistant that only responds in JSON. For example:
                    {
                    "name": "Newton's Laws and the causes of motion",
                    "topics": {
                      "topics": [
                        {
                          "name": "Newton's First Law",
                          "topics": [
                            {
                              "name": "Uniform Motion",
                              "topics": [
                                { "name": "Definition", "topics": [] },
                                { "name": "Examples in Daily Life", "topics": [] },
                                { "name": "Graphical Representation", "topics": [] }
                              ]
                            },
                            {
                              "name": "Kinematics",
                              "topics": [
                                { "name": "Distance and Displacement", "topics": [] },
                                { "name": "Speed and Velocity", "topics": [] },
                                { "name": "Equations of Motion", "topics": [] }
                              ]
                            },
                            {
                              "name": "Centripetal Motion",
                              "topics": [
                                { "name": "Definition", "topics": [] },
                                { "name": "Centripetal Force", "topics": [] },
                                { "name": "Examples in Nature and Engineering", "topics": [] }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "Newton's Second Law",
                          "topics": [
                            {
                              "name": "F=ma",
                              "topics": [
                                { "name": "Understanding Force, Mass, and Acceleration", "topics": [] },
                                { "name": "Units and Measurements", "topics": [] },
                                { "name": "Applications in Mechanics", "topics": [] }
                              ]
                            },
                            {
                              "name": "Causes of Motion",
                              "topics": [
                                {
                                  "name": "Forces",
                                  "topics": [
                                    { "name": "Types of Forces", "topics": [] },
                                    { "name": "Free-Body Diagrams", "topics": [] }
                                  ]
                                },
                                {
                                  "name": "Friction",
                                  "topics": [
                                    { "name": "Static vs Kinetic Friction", "topics": [] },
                                    { "name": "Friction in Daily Life", "topics": [] }
                                  ]
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "Newton's Third Law",
                          "topics": [
                            {
                              "name": "Action-Reaction Pairs",
                              "topics": [
                                { "name": "Definition and Explanation", "topics": [] },
                                { "name": "Examples in Nature", "topics": [] },
                                { "name": "Applications in Engineering", "topics": [] }
                              ]
                            },
                            {
                              "name": "Applications of Newton's Third Law",
                              "topics": [
                                { "name": "Rocket Propulsion", "topics": [] },
                                { "name": "Walking and Running Mechanics", "topics": [] }
                              ]
                            }
                          ]
                        }
                      ]
                    }"""},
                    {"role": "user", "content": """Generate a nested JSON object containing a "knowledge tree" describing a certain course. Every course or subject on earth can be diluted down into a knowledge tree, or a tree diagram representing the main topic of the course, then subtopics required to build up to that main topic, and then sub sub topics about each of those subtopics. You will receive a text dump of the syllabus of this course. This syllabus has some parts of it that aren't main topics, subtopics, or anything else. Ignore those, and just get the general essence of what the course is about and what it is trying to teach from the syllabus text dump. You need to organize these course topics into a hierarchical JSON structure.

                    Rules: 1. Create a logical parent-child relationship between broad concepts and specific subtopics 2. Remove duplicate concepts 3. Keep maximum 4 levels of nesting 4. Output exactly in this format:
                    {
                    "name": "Computer Organization and Design",
                    "topics": [
                        {
                        "name": "Digital Logic Design",
                        "topics": [
                            {
                            "name": "Combinational Logic",
                            "topics": []
                            },
                            {
                            "name": "Sequential Logic",
                            "topics": []
                            },
                            {
                            "name": "Basic Components",
                            "topics": []
                            }
                        ]
                        },
                        {
                        "name": "Data Representation and Manipulation",
                        "topics": [
                            {
                            "name": "Number Systems",
                            "topics": [
                                {
                                "name": "Two's Complement",
                                "topics": []
                                },
                                {
                                "name": "IEEE Floating Point",
                                "topics": []
                                }
                            ]
                            }
                        ]
                        },
                        {
                        "name": "Processor Design",
                        "topics": [
                            {
                            "name": "Single-Cycle Control",
                            "topics": []
                            },
                            {
                            "name": "Multi-Cycle Control",
                            "topics": []
                            },
                            {
                            "name": "Data-Path Control",
                            "topics": []
                            },
                            {
                            "name": "Execution of Machine Language",
                            "topics": [
                                {
                                "name": "RISC Machine Language",
                                "topics": []
                                },
                                {
                                "name": "Pipeline Architecture",
                                "topics": []
                                }
                            ]
                            }
                        ]
                        },
                        {
                        "name": "Memory Hierarchy",
                        "topics": [
                            {
                            "name": "Cache Memory",
                            "topics": []
                            },
                            {
                            "name": "Virtual Memory",
                            "topics": []
                            }
                        ]
                        },
                        {
                        "name": "Multi-Processor Systems",
                        "topics": [
                            {
                            "name": "Core Processors",
                            "topics": []
                            }
                        ]
                        },
                        {
                        "name": "ARM Architecture",
                        "topics": []
                        }
                    ]
                    }


                    Yours would be more elaborate, less elaborate, with more or less nesting: your discretion based on the complexity of the subject material. Here is the text dump: "topics":""" + f"{topics_str}" + """

                    Prioritize detail of the lowest layer subtopics, and when deciding if the output is good, think "could I learn everything needed to know about this course just looking at this JSON? As mentioned, respond purely in JSON format. Do not hallucinate.
            """}
                ]
            )
            return (
                completion.choices[0].message.content,
                completion.usage.prompt_tokens,
                completion.usage.completion_tokens,
                completion.usage.total_tokens
            )
        except Exception as e:
            sleep_time = backoff_factor ** attempt + random.uniform(0, 1)
            time.sleep(sleep_time)
            print(f"‼️Exception: + {e}")
            continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--output', required=True, help='Output JSONL file')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        courses = json.load(f)

    json_list = []
    token_counts = {'input': 0, 'output': 0, 'total': 0}
    invalid_courses = []

    for course in tqdm(courses):
        try:
            result, in_tok, out_tok, total_tok = getTree(''.join(course['topics']))
            token_counts['input'] += in_tok
            token_counts['output'] += out_tok
            token_counts['total'] += total_tok

            json.loads(result)  # Validate JSON
            json_list.append({
                "course_id": course['course_id'],
                "course_code": course['course_code'],
                "course_name": course['course_name'],
                "term_name": course['term_name'],
                "program_name": course['program_name'],
                "program_id": course['program_id'],
                "major_id": course['major_id'],
                "major_name": course['major_name'],
                "tree": result
            })
        except Exception as e:
            invalid_courses.append(f"{course['course_code']} - {str(e)}")
            continue

    with open(args.output, 'w') as f:
        for item in json_list:
            json.dump(item, f)
            f.write('\n')

    print(f"Token usage:\nInput: {token_counts['input']}\nOutput: {token_counts['output']}\nTotal: {token_counts['total']}")
    print(f"Failed courses: {invalid_courses}")

if __name__ == '__main__':
    main()
