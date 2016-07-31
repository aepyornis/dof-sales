#!/bin/bash

rm sales.csv
touch sales.csv

psql -d june_rolling_sales -c "COPY (
    SELECT sales.*, 
    p.lat,
    p.lng,
    p.council,
    p.cd,
    p.address as pluto_address,
    p.landuse,
    p.allzoning1,
    p.builtfar,
    p.residfar,
    p.assessland,
    p.assesstotal 
    FROM sales
    LEFT JOIN pluto_16v1 as p on sales.bbl = p.bbl
    limit 0) TO STDOUT (FORMAT CSV, HEADER TRUE);" >> sales.csv

for i in `seq 101 112` `seq 201 212` `seq 301 318` `seq 401 414` `seq 501 503`;
do
    printf '.'
    ./top_sales_for_cd.sh $i >> sales.csv
done

printf '\n'
