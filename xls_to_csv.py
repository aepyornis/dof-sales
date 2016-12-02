"""
Converts xls to csv
use: python3 xls_to_csv.py /path/to/dir/with/xls outfile.csv
"""
import xlrd
import sys
import csv
import glob
import os

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


# input: <csvwriter>, str
def file_to_csv(csvwriter, xls_path):
    book = xlrd.open_workbook(xls_path)
    print("Processing: {0}".format(book.sheet_names()[0]))
    sheet = book.sheet_by_index(0)
    rows = sheet.get_rows()
    for x in range(5):
        next(rows) # remove first five rows
    for r in rows:
        row = tuple(map(cell_converter, r))
        row_bbl = (row[0], row[4], row[5])
        csvwriter.writerow(row + bbl_helper(*row_bbl))


def main():
    with open(out_file_path, 'w') as f:
        csvwriter = csv.writer(f, delimiter=',', quotechar='"')
        for xls in glob.glob(os.path.join(xls_dir_path, '*.xls')):
            file_to_csv(csvwriter, xls)

if __name__ == '__main__':
    xls_dir_path = sys.argv[1]
    out_file_path = sys.argv[2]
    main()
