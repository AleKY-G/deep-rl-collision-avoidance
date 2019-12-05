#!/bin/bash

s=0

for i in {0..3}; do
  python experiments.py "train" "int_behavior" $s $i
  python experiments.py "validate" "int_behavior" $s $i
done
