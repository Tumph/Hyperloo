from openai import OpenAI


client = OpenAI()

topics_str = "Tools and Techniques for Software Development Winter 2025"
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are a helpful assistant that only responds in JSON. For example:
        {
          "name": "Newton's Laws and the causes of motion",
          "topics": [
            {
              "name": "Newton's First Law",
              "topics": [
                {
                  "name": "Uniform Motion",
                  "topics": []
                },
                {
                  "name": "Kinematics",
                  "topics": []
                },
                {
                  "name": "Centripetal Motion",
                  "topics": []
                }
              ]
            },
            {
              "name": "Newton's Second Law",
              "topics": [
                {
                  "name": "F=ma",
                  "topics": []
                },
                {
                  "name": "Causes of Motion",
                  "topics": [
                    {
                      "name": "Forces",
                      "topics": []
                    },
                    {
                      "name": "Friction",
                      "topics": []
                    }
                  ]
                }
              ]
            },
            {
              "name": "Newton's Third Law",
              "topics": []
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
print(completion.choices[0].message.content)
