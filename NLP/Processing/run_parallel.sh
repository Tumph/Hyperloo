#!/bin/bash
for i in {0..59}
do
    python treenew.py --input "chunks/syllabi_chunk_$i.json" --output "trees/trees_$i.jsonl" &
done
wait
