#!/bin/bash

for f in *.xls
do
    filename=$(basename "${f}" ".xls")
    xls2csv ${f} > ${filename}.csv
done

