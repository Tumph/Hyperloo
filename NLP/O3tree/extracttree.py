import json

def extract_and_convert_tree(input_file):
    """
    Extracts the 'tree' string from each object in the input file and converts it into a JSON object.

    Parameters:
    input_file (str): Path to the input file (trees.jsonl).

    Returns:
    list: A list of JSON objects representing the extracted trees.
    """
    extracted_trees = []

    with open(input_file, 'r') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue

            try:
                # Load each line as a JSON object
                obj = json.loads(line)

                # Extract the 'tree' string
                tree_str = obj.get('tree', '')

                # Check if 'tree' string is not empty
                if tree_str:
                    try:
                        # Convert the 'tree' string into a JSON object
                        tree_json = json.loads(tree_str)

                        # Append the converted tree to the list
                        extracted_trees.append(tree_json)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing tree JSON: {e}")
                        print(f"Problematic tree string: {tree_str}")
                else:
                    print("Empty 'tree' string encountered.")
            except json.JSONDecodeError as e:
                print(f"Error loading JSON object: {e}")
                print(f"Problematic line: {line}")

    return extracted_trees

def main():
    input_file = 'trees.jsonl'
    extracted_trees = extract_and_convert_tree(input_file)

    # Optionally, print or save the extracted trees
    for i, tree in enumerate(extracted_trees):
        print(f"Tree {i+1}:")
        print(json.dumps(tree, indent=4))
        print()  # Empty line for readability

if __name__ == "__main__":
    main()
