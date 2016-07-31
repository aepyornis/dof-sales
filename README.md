# dof-sales

### Requirements

* Python3
* Postgres
* xls2csv

### Instructions:

#### Convert the xls files into csvs using xls2csv

On Debian/Ubuntu you can get this utility by installing catdoc:

``` apt-get install catdoc ```

Individually convert them:
```
xls2csv dof_sales_file.xls
```
or use the helper bash script (run this in the same dir with the xls files)

```
./batch_convert_to_csv.sh 
```

#### Python & Postgres Setup

Install Python3 requirement: psycopg2 via pip (globally or in a virtual environment):

 ``` pip3 install psycopg2 ```

Create database if needed:

```
createdb datebaseName
```

#### Insert the files into the db:

```
python3 insert_data.py path/to/dir/with/dof/csv/files "dbname=databaseName user=pgusername"
```

#### Double check the problem lines. 

Converting these xls to csv generates a lot of mysterious blank lines and/or corrupted lines. 
When I did this it was over 20,000 wasted lines!  The script, insert_data.py, saves all lines with errors to a file called "problem_lines.csv"

You can do a quick check to make sure these lines don't accidentally contain any real data:

```
uniq problem_lines.csv
```

If everything's all good, you can remove problem_lines.csv

### Flags

*BBLSalePriceFlag*

1 - sale price above zero

0 - sale price is zero

*BuildingClassCatFlag*

1 - if Building Class Category is 1-8, 11-16, 23

0 - not one of the above codes

*CounterID* 

order of sales in ranking:
    
    1) highest price of sale in period
    2) next highest price
    3) ... and so on

*BBLSalePriceFlag*

1 - highest price sale (counterId == 1) and sale is not zero (BBLSalePriceFlag == 1)

*SalePriceBuildingCatFlag*

1 - highest non-zero sale (1) and buildingClassCatFlag is 1

### Data source

[NYC - DOF](http://www1.nyc.gov/site/finance/taxes/property-rolling-sales-data.page)
