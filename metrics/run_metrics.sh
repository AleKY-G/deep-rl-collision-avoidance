#!/bin/bash

ps=(0 .01 .03 .0 .1 .2 .3)

for p in "${ps[@]}"; do
  python metrics.py $p
done

