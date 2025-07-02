#!/bin/sh

for n in $(seq 0 1 1000)
do
    echo "$n"
    make test
done
exit