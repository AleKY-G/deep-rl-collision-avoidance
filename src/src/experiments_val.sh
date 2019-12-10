#!/bin/bash

s=0

for i in {0..4}; do
    python experiments.py "validate" "pnmac" $s $i
done

for i in {0..4}; do
    python experiments.py "validate" "rw_shape" $s $i
done

for i in {0..3}; do
    python experiments.py "validate" "int_behavior" $s $i
done

