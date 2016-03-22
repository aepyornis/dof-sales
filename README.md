# dof-sales

### Technologies:

* Python3
* Postgres
* xls2csv

### Instructions:

1) Convert the xls files into csvs using xls2csv.

On Debian/Ubuntu you can get this utility by install catdoc:

``` apt-get install catdoc ```

Individually convert them:
```
xls2csv dof_sales_file.xls
```
or use the helper bash script (run this in the same dir with the xls files)

```
./batch_convert_to_csv.sh 
```

2) Python & Postgres Setup

Install Python3 requirement: psycopg2 via pip (globally or in a virtual environment):

 ``` pip install psycopg2 ```

Export the connection environment variable:

``` export DOF_SALES_DB_CONNECTION='dbname=databaseName user=pgusername' ```

Create database:

```
createdb datebaseName
```

3) Insert the files into the db:

```
python3 insert_data.py path/to/dir/with/dof/csv/files
```

4) Double check the problem lines. 

Converting these xls to csv generates a lot of mysterious blank lines and/or corrupted lines. 
When I did this it was over 20,000 wasted lines!  The script, insert_data.py, saves all lines with errors to a file called "problem_lines.csv"

You can do a quick check to make sure these lines don't accidentally contain any real data:

```
uniq problem_lines.csv
```

If everything's all good, you can remove problem_lines.csv

