#!/bin/bash

#MAKE SURE YOU RUN SPLIT SYLLABI FIRST

for i in {0..59}
do
    python treenew.py --input "errorchunks/syllabi_chunk_$i.json" --output "missedtrees/trees_$i.jsonl" &
done
wait
