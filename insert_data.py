"""
Inserts DOF rolling sales data into postgres
use: python3 insert_data.py path/to/csv/dir/ "dbname=your_db_name user=your_pg_username"
"""
import util
import derived_columns
import os
import sys
import csv
import glob
import copy
import psycopg2

csv_dir = sys.argv[1]
db_connection_string = sys.argv[2]

conn = psycopg2.connect(db_connection_string)
cur = conn.cursor()

total = 0
errors = []
field_errors = 0


def csv_file_list(dir):
    return glob.glob(dir + '/*.csv')

def create_table(cur, tablename):
    cur.execute('DROP TABLE IF EXISTS ' + tablename)
    with open('schema.sql', 'r') as f:
        sql = f.read()
        cur.execute(sql)

def get_headers():
    with open('headers.txt', 'r') as f:
        return f.read().replace('\n', '').split(',')


def insert_row(row):
    query = util.make_query('sales', row)[0]
    data = util.make_query('sales', row)[1]
    try:
        cur.execute(query, data)
        conn.commit()
        global total
        total += 1
    except Exception as e:
        print(str(row))
        raise


# string -> dict
def bbl_count(csv_file):
    count_map = {}  # key -> count map
    with open(csv_file, 'r') as f:
        util.skip(5, f)
        headers = get_headers()
        csvreader = csv.DictReader(f, fieldnames=headers)
        for row in csvreader:
            if len(row) == 21:
                try:
                    bbl = util.bbl(row['Borough'], row['Block'], row['Lot'])
                except (ValueError,TypeError) as e:
                    print(e)
                    print(row)
                if bbl in count_map:
                    count_map[bbl] += 1
                else:
                    count_map[bbl] = 1
            else:
                print('there are not 21 columns in row: ' + str(row))
    return count_map


# def process_row(row, count_map):
#     global errors
#     try:
#         if len(row) == 21:
#             derived_columns.add_derived_columns(row, count_map)
#             insert_row(row)
#             conn.commit()
#             global total
#             total += 1
#         else:
#             errors.append(row)
#     except Exception as e:
#         errors.append(row)

def handle_field_error(row, e):
    print(key + "," + row[key])
    print(e)
    global field_errors
    field_errors += 1
    row[key] = None

# Does type_casting
lookup = util.sql_type_dir('schema.sql')
def process_fields(row):
    for key in row:
        try:
            row[key] = util.type_cast(key, row[key], lookup)
        except ValueError as e:
            handle_field_error(row, e)

def process_row(row, count_map):
    try:
        if len(row) == 21:
            derived_columns.add_derived_columns(row, count_map)
            process_fields(row)
            return row
        else:
            return None
    except Exception as e:
        
        return None
    

# string -> list
def file_to_list(csv_file):
    global errors
    count_map = bbl_count(csv_file)
    rows = []
    with open(csv_file, 'r') as f:
        util.skip(5, f)
        headers = get_headers()
        csvreader = csv.DictReader(f, fieldnames=headers)
        for row in csvreader:
            _row = process_row(row, count_map)
            if _row:
                rows.append(_row)
            else:
                errors.append(row)
    return rows
    

if __name__ == "__main__":
    create_table(cur, 'sales')
    for csv_file in csv_file_list(csv_dir):
        print('processing ' + csv_file)
        rows = file_to_list(csv_file)
        rows_without_duplicates = derived_columns.remove_duplicate_sales_on_same_day(rows)
        rows_with_counter_id = derived_columns.counter_id(rows_without_duplicates)
        rows_with_sp_flag = derived_columns.bbl_sp_flag(rows_with_counter_id)
        for row in rows_with_sp_flag:
            insert_row(row)
        # print(bbl_count(csv_file))
    print('total inserted: ' + str(total))
    print('fields with errors: ' + str(field_errors))
    print('lines with errors: ' + str(len(errors)))
    
    with open('problem_lines.csv', 'w') as f:
        for line in errors:
            f.write(str(line) + "\n")
    print('problem_lines.csv saved!')

