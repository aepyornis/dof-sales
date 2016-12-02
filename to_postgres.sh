#!/bin/bash
# use: bash to_postgres.sh "path/to/xls/dir" 

source ./env.sh

execute_sql schema.sql

python3 xls_to_csv.py $1 - | execute_sql_cmd "COPY dof_sales(Borough,  Neighborhood,  BuildingClassCategory,  TaxClassAtPresent,  Block,  Lot,  EaseMent,  BuildingClassAtPresent,  Address,  ApartmentNumber,  ZipCode,  ResidentialUnits,  CommercialUnits, TotalUnits, LandSquareFeet,  GrossSquareFeet,  YearBuilt,  TaxClassAtTimeOfSale,  BuildingClassAtTimeOfSale,  SalePrice, SaleDate, bbl) FROM STDIN WITH (FORMAT CSV, HEADER TRUE);"
