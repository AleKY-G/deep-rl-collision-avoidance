#!/bin/bash

s=0

for i in {0..4}; do
    python experiments.py "train" "pnmac" $s $i
    python experiments.py "validate" "pnmac" $s $i
done

