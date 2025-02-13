# split_syllabi.py
import json
import math
import os

def split_json(input_file, chunks=60):
    with open(input_file, 'r') as f:
        data = json.load(f)

    total = len(data)
    chunk_size = math.ceil(total / chunks)

    os.makedirs('errorchunks', exist_ok=True)

    for i in range(chunks):
        start = i * chunk_size
        end = (i+1) * chunk_size
        chunk = data[start:end]

        with open(f'errorchunks/syllabi_chunk_{i}.json', 'w') as f:
            json.dump(chunk, f)

if __name__ == '__main__':
    split_json('missedjsons/missed_syllabi.json', 60)
