import util

def add_bbl(row):
   row['bbl'] = util.bbl(row['Borough'], row['Block'], row['Lot']) 

def sale_price_flag(row):
    if int(row['SalePrice'].strip()) > 0:
        return 1
    else:
        return 0

def add_sale_price_flag(row):
    row['SalePriceFlag'] = sale_price_flag(row)


def add_bbl_count(row, count_map):
    row['SaleCount'] = count_map[row['bbl']]


def add_derived_columns(row, count_map):
    add_bbl(row)
    add_bbl_count(row, count_map)
    # add_sale_price_flag(row)




# SalePriceFlag smallint,        
