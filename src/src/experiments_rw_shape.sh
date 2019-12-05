#!/bin/bash

s=0

for i in {0..4}; do
  python experiments.py "train" "rw_shape" $s $i
  python experiments.py "validate" "rw_shape" $s $i
done
