import util
import derived_columns
import os
import sys
import csv
import glob
import copy
import psycopg2

db_connection_string = os.environ['DOF_SALES_DB_CONNECTION']
csv_dir = sys.argv[1]

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


lookup = util.sql_type_dir('schema.sql')
def insert_row(row):
    for key in row:
        try:
            row[key] = util.type_cast(key, row[key], lookup)
        except ValueError as e:
            print(key + "," + row[key])
            print(e)
            global field_errors
            field_errors += 1
            row[key] = None
    query = util.make_query('sales', row)[0]
    data = util.make_query('sales', row)[1]
    try:
        cur.execute(query, data)
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


def process_row(row, count_map):
    global errors
    try:
        if len(row) == 21:
            derived_columns.add_derived_columns(row, count_map)
            insert_row(row)
            conn.commit()
            global total
            total += 1
        else:
            errors.append(row)
    except Exception as e:
        errors.append(row)


def copy_data(csv_file):
    count_map = bbl_count(csv_file)
    with open(csv_file, 'r') as f:
        util.skip(5, f)
        headers = get_headers()
        csvreader = csv.DictReader(f, fieldnames=headers)
        for row in csvreader:
            process_row(row, count_map)

if __name__ == "__main__":
    create_table(cur, 'sales')
    for csv_file in csv_file_list(csv_dir):
        print('processing ' + csv_file)
        copy_data(csv_file)
        # print(bbl_count(csv_file))
    print('total inserted: ' + str(total))
    print('fields with errors: ' + str(field_errors))
    print('lines with errors: ' + str(len(errors)))
    
    with open('problem_lines.csv', 'w') as f:
        for line in errors:
            f.write(str(line) + "\n")
    print('problem_lines.csv saved!')

