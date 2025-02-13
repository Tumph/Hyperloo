from openai import OpenAI
import json
from tqdm import tqdm
client = OpenAI()


global input_tokens, output_tokens, total_tokens

def getTree(topics_str):
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

    # Print only the text response

    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens

    return completion.choices[0].message.content, input_tokens, output_tokens, total_tokens



invalid_jsons_list = []
in1 = 0
out = 0
total = 0

json_list = []

with open('../../scrapers/scrapesyllabus/syllabi.json', 'r') as f:
    courses = json.load(f)


for idx, course in tqdm(enumerate(courses)):
    funcout = getTree(''.join(course['topics']))
    currentjson = funcout[0]
    in1 += funcout[1]
    out += funcout[2]
    total += funcout[3]


    if currentjson is None:
        print("‼️ currentjson is None")
    else:
        try:
            json.loads(currentjson)
            print("✅ Valid JSON")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            invalid_jsons_list.append(f"{course['course_code']}, {course['major_name']}")
            continue


    print(f"API Response: {currentjson}")
    json_list.append({
        "course_id": course['course_id'],
        "course_code": course['course_code'],
        "course_name": course['course_name'],
        "term_name": course['term_name'],
        "program_name": course['program_name'],
        "program_id": course['program_id'],
        "major_id": course['major_id'],
        "major_name": course['major_name'],
        "tree": currentjson
    })

    with open('trees.jsonl', 'w') as f:
        for item in json_list:
            json.dump(item, f)
            f.write('\n')
        print("💾 Saved")


print(f"Total input tokens: {in1}")
print(f"Total output tokens: {out}")
print(f"Total total tokens: {total}")
print(invalid_jsons_list)
