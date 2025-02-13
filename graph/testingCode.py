from neo4j import GraphDatabase
import json

# Neo4j connection details
URI = "bolt://localhost:7687"  # Update if necessary
USERNAME = "neo4j"
PASSWORD = "hyperloo"

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# Function to create nodes and relationships recursively
def insert_topic(tx, parent_name, topic):
    topic_name = topic["name"]

    # Create topic node
    tx.run(
        "MERGE (t:Topic {name: $topic_name})",
        topic_name=topic_name
    )

    # Create relationship if there's a parent
    if parent_name:
        tx.run(
            """
            MATCH (p:Topic {name: $parent_name}), (c:Topic {name: $topic_name})
            MERGE (p)-[:HAS_SUBTOPIC]->(c)
            """,
            parent_name=parent_name,
            topic_name=topic_name
        )

    # Recursively insert subtopics
    for subtopic in topic["topics"]:
        insert_topic(tx, topic_name, subtopic)

# Load JSON file
with open("./small.json", "r") as file:
    data = json.load(file)

# Insert data into Neo4j using execute_write()
with driver.session() as session:
    session.execute_write(insert_topic, None, data)

# Close connection
driver.close()
