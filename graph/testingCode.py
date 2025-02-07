from py2neo import Graph, Node, Relationship
graph = Graph("bolt://localhost:7687", auth=("neo4j", "hyperloo"))

# Example nested dictionary
org_chart = {
    "President1": {
        "CFO1": {
            "Global Investments VP1": {},
            "Internal Audits VP1": {}
        },
        "CTO1": {
            "Global Cloud VP1": {},
            "VP of Automations1": {
                "Head of RPA Team1": {}
            }
        }
    }
}

def create_nodes(data, parent=None):
    for title, subordinates in data.items():
        node = Node("Employee", title=title)
        graph.create(node)
        
        if parent:
            relationship = Relationship(parent, "MANAGES", node)
            graph.create(relationship)
        
        create_nodes(subordinates, node)

# Start creating nodes from the root
create_nodes(org_chart)
# ```

# This code will create nodes for each employee in the hierarchy and establish "MANAGES" relationships between them. The nested structure is preserved through these relationships.

# To query the data:

# ```python
# Example query to find all employees managed by the CTO
query = """
MATCH (cto:Employee {title: 'CTO'})-[:MANAGES*]->(subordinate)
RETURN subordinate.title
"""
results = graph.run(query)
for record in results:
    print(record["subordinate.title"])
