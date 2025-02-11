System message
--------------
```
You are a helpful assistant that only responds in JSON. For example:
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
}
```

Prompt
------
```
Generate a nested JSON object containing a "knowledge tree" describing a certain course. Every course or subject on earth can be diluted down into a knowledge tree, or a tree diagram representing the main topic of the course, then subtopics required to build up to that main topic, and then sub sub topics about each of those subtopics. You will receive a text dump of the syllabus of this course. This syllabus has some parts of it that aren't main topics, subtopics, or anything else. Ignore those, and just get the general essence of what the course is about and what it is trying to teach from the syllabus text dump. You need to organize these course topics into a hierarchical JSON structure.

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


Yours would be more elaborate, less elaborate, with more or less nesting: your discretion based on the complexity of the subject material. Here is the text dump:         "topics": [
            "Tools and Techniques for Software Development Winter 2025",
            "08:30AM - 10:20AM MC 3003",
            "10:30AM - 12:20PM MC 3003",
            "E. Ciklabakkal",
            "E. Ciklabakkal",
            "08:30AM - 10:20AM MC 4042",
            "E. Ciklabakkal",
            "10:30AM - 12:20PM MC 4042",
            "08:30AM - 10:20AM MC 3003",
            "10:30AM - 12:20PM MC 4060",
            "02:30PM - 04:20PM MC 4060",
            "E. Ciklabakkal",
            "10:30AM - 12:20PM MC 3003",
            "This course introduces students to tools and techniques useful in the software development lifecycle.",
            "Students learn to navigate and leverage commands and utilities in the Linux Command Line Shell.",
            "Students gain experience in version control software, writing scripts to automate tasks, and creating effective test cases to identify bugs.",
            "Students also gain experience in using built-in support for version control, testing, debugging, build automation, etc. in integrated development environments (IDEs).",
            "Interact with the Linux Operating System using a command line shell and gain familiarity with commands, utilities and tools.",
            "Create scripts to automate tasks and increase productivity while working on a software project.",
            "Design test cases and automate the testing process to check a program for functional correctness and incorrect memory usage.",
            "Use version control systems to share, contribute, manage and track code.",
            "Separately compile code modules and leverage build automation tools to do so efficiently.",
            "Module 0: Linux Shell, a first look",
            "Module 2: Testing and Debugging",
            "Module 9: Debugging",
            "Each lab consists of a number of lab problems.",
            "Each lab problem has two associated values, a lower one called the pass threshold and a higher one called the completion threshold.",
            "Special note on test cases: if a lab question asks you to submit test cases, you must create these tests yourself.",
            "Do not directly copy code from GenAI.",
            "Do not ask GenAI for a step-by-step breakdown of how to solve a lab problem.",
            "In particular:",
            "Please inform of us these at the start of the course."
        ]

Prioritize detail of the lowest layer subtopics, and when deciding if the output is good, think "could I learn everything needed to know about this course just looking at this JSON? As mentioned, respond purely in JSON format. Do not hallucinate.
```
