#!/bin/bash

cmd="s/##CD##/${1}/"

echo "COPY (
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
    WHERE cd = ##CD##
    order by SalePrice desc
    limit 15
)
TO STDOUT (FORMAT CSV, HEADER FALSE);" | 
    perl -pe $cmd | 
    psql -U michael -d june_rolling_sales
