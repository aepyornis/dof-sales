"""
CSV->Postgres parsing utilities
"""
import datetime


# 06-03-15
# input format: mm-dd-yy
# datetime.date(year, month, day)
def date_format(datestring):
    datelist = datestring.split('-')
    month = int(datelist[0])
    day = int(datelist[1])
    year = int("20" + datelist[2])
    return datetime.date(year, month, day)


def type_cast(key, val, lookup):
    datatype = lookup[key].strip()
    if key == 'SaleCount':
        return val
    elif val.strip() == '':
        return None
    elif datatype == 'text':
        return val.strip()
    elif 'char' in datatype:
        return val.strip()
    elif datatype == 'integer' or datatype == 'bigint' or datatype == 'smallint':
        return int(val.strip())
    elif datatype == 'money':
        return val.strip().replace('$', '')
    elif datatype == 'boolean':
        if val.strip():
            return True
        else:
            return False
    elif datatype == 'date':
        return date_format(val.strip())
    else:
        raise Exception('Type Cast Error - ' + datatype)


def lot_length_helper(lot):
    if len(lot) < 5:
        return lot.zfill(4)
    else:
        print(lot + " is more than 5 chars long!")
        return '0000'


def bbl(boro, block, lot):
    if boro == '' and lot == '' and block == '':
        return 'blank'
    elif len(boro) != 1:
        raise ValueError("Borough, " + boro + " is longer than one char")
    else:
        updated_lot = lot_length_helper(lot)
        bbl =  boro + block.zfill(5) + updated_lot
        return bbl


def sql_type_dir(sql_file):
    d = {}
    with open(sql_file, 'r') as f:
        for line in f:
            if ')' not in line or 'char' in line:
                key = line.strip().replace(',', '').split(' ')[0]
                val = ' '.join(line.strip().replace(',', '').split(' ')[1:])
                d[key] = val
    return d

def skip(lines, f):
    for x in range(lines):
        next(f)

def placeholders(num):
    text = '('
    for x in range(num):
        if x < (num - 1):
            text += '%s, '
        else:
            text += '%s)'

    return text


def make_query(tablename, row):
    fieldnames = []
    values = []
    for key in row:
        fieldnames.append(key)
        values.append(row[key])
    query = "INSERT INTO " + tablename + " " + str(tuple(fieldnames))
    query += " values " + placeholders(len(fieldnames))
    query = query.replace("'", "")
    return (query, tuple(values))


def sql_type_dir(sql_file):
    d = {}
    with open(sql_file, 'r') as f:
        for line in f:
            if ')' not in line or 'char' in line:
                key = line.strip().replace(',', '').split(' ')[0]
                val = ' '.join(line.strip().replace(',', '').split(' ')[1:])
                d[key] = val
    return d



