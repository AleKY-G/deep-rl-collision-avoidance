#!/bin/bash

for i in {0..5}; do
  for s in {0..2}; do
    python experiments.py "train" "pnmac" $s $i
    python experiments.py "validate" "pnmac" $s $i
  done
done

for i in {0..5}; do
  for s in {0..2}; do
    python experiments.py "train" "rw_shape" $s $i
    python experiments.py "validate" "rw_shape" $s $i
  done
done

for i in {0..3}; do
  for s in {0..2}; do
    python experiments.py "train" "int_behavior" $s $i
    python experiments.py "validate" "int_behavior" $s $i
  done
done
