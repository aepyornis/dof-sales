"""
Converts xls to csv

use: python3 xls_to_csv.py /path/to/dir/with/xls outfile.csv

to write to stdout instead of a file use:  '-' or  'STDOUT' 
"""
import xlrd
import sys
import csv
import glob
import os
from type_info import type_info

def cell_converter(cell):
    if cell.ctype == 0:
        return ""
    elif cell.ctype == 1:
        return cell.value.strip()
    elif cell.ctype == 2:
        return int(cell.value)
    elif cell.ctype == 3:
        return xlrd.xldate.xldate_as_datetime(cell.value, 0)
    else:
        return cell.value


# int, int, int -> tuple
def bbl_helper(boro, block, lot):
    boro, block, lot = [str(x) for x in (boro, block, lot)]
    if len(boro) != 1:
        raise ValueError("Borough, " + boro + " is longer than one char")
    if len(block) > 5:
        raise ValueError(lot + " is more than 4 chars long!")
    if len(lot) > 4:
        raise ValueError(lot + " is more than 5 chars long!")
    return (boro + block.zfill(5) + lot.zfill(4), )


def int_helper(x):
    """
    Converts input to integer. Value can contain '-' instead of null.
    """
    try:
        if isinstance(x, int):
            return x
        elif x == '-' or x is None or x.strip() == '':
            return None
        elif '.' in x:
            return int(x.split('.')[0])
        else:
            return int(x)
    except ValueError:
        return None

def type_caster(row):
    """
    converts rows into correct type
    """
    out = []
    for index, val in enumerate(row):
        if type_info[index][1] == 'int':
            out.append(int_helper(val))
        else:
            out.append(val)
    return out


def add_bbl_to_row(row):
    bbl = (row[0], row[4], row[5])
    return row + bbl_helper(*bbl)


def process_row(r):
    """
    Prepares row for file writing by doing three things:
      1) converts from xlrd object to normal python data type
      2) adds bbl
      3) type converting (checks if integer)
    """
    row = tuple(map(cell_converter, r))
    row_with_bbl = add_bbl_to_row(row)
    return type_caster(row_with_bbl)


# input: <csvwriter>, str
def file_to_csv(csvwriter, xls_path):
    book = xlrd.open_workbook(xls_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.get_rows()
    for x in range(5):
        next(rows) # remove first five rows
    for r in rows:
        csvwriter.writerow(process_row(r))


def process_xls_dir(csvwriter, xls_dir_path):
    """
    input: <csv.writer>, str
    Calls file_to_csv for each xls file in the directory
    """
    for xls in glob.glob(os.path.join(xls_dir_path, '*.xls')):
        file_to_csv(csvwriter, xls)


def main(xls_dir_path, out_file_path):
    if out_file_path == '-' or out_file_path.upper() == 'STDOUT':
        csvwriter = csv.writer(sys.stdout, delimiter=',', quotechar='"')
        process_xls_dir(csvwriter, xls_dir_path)
    else:
        with open(out_file_path, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',', quotechar='"')
            process_xls_dir(csvwriter, xls_dir_path)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
