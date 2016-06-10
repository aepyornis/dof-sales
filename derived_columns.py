import util
from collections import Counter

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


def add_bldg_class_cat_short(row):
    bldg_class = row['BuildingClassCategory']
    if bldg_class:
        row['BuildingClassCatShort'] = int(bldg_class[0:2])
    else:
        row['BuildingClassCatShort'] = None


def add_bldg_class_flag(row):
    if row['BuildingClassCatShort'] in [1,2,3,4,5,6,7,8,11,12,13,14,15,16,23]:
        row['BuildingClassCatFlag'] = 1
    else:
        row['BuildingClassCatFlag'] = 0


def add_derived_columns(row, count_map):
    add_bbl(row)
    add_bbl_count(row, count_map)
    add_sale_price_flag(row)
    add_bldg_class_cat_short(row)
    add_bldg_class_flag(row)


def highest_sale_for_that_day(rows, row):
   that_days_sales = [x for x in rows if x['SaleDate'] == row['SaleDate'] and x['bbl'] == row['bbl']]
   return sorted(that_days_sales, key=lambda k: k['SalePrice'], reverse=True)[0]['SalePrice']


def remove_duplicate_sales_on_same_day(rows):
   """
   Some tax lots, for whatever reason, contain multiple sales listed for the same day.
   This function picks the highest price sale for that day and removes the rest.
   """
   already_in = set()

   def approve_highest(row):
      if (row['bbl'], row['SalePrice'], row['SaleDate']) in already_in:
         return False
      else:
         if row['SalePrice'] == highest_sale_for_that_day(rows, row):
            already_in.add((row['bbl'], row['SalePrice'], row['SaleDate']))
            return True
         else:
            return False
   
   return list(filter(approve_highest, rows))

   
# if there is only one sale, counter id is 1
# if there is more than one sale, counter id is the ranking in order of the sales by sale price
# where 1 is the highest price.
def counter_id(rows):
    for row in rows:
        if row['SaleCount'] == 1:
            row['CounterId'] = 1
        else:
            sales = [x for x in rows if x['bbl'] == row['bbl']]
            sorted_sales = sorted(sales, key=lambda k: k['SalePrice'], reverse=True)
            dates = [row['SaleDate'] for row in sorted_sales]
            row['CounterId'] = (dates.index(row['SaleDate']) + 1)
    return rows


def add_bbl_sp_flag(row):
    if row['SalePriceFlag'] == 1 and row['CounterId'] == 1:
        row['BBLSalePriceFlag'] = 1
    else:
        row['BBLSalePriceFlag'] = 0


def add_bbl_sp_bldg_cat_flag(row):
    if row['SalePriceFlag'] == 1 and row['CounterId'] == 1 and row['BBLSalePriceFlag'] == 1:
        row['SalePriceBuildingCatFlag'] = 1
    else:
        row['SalePriceBuildingCatFlag'] = 0


def bbl_sp_flag(rows):
    for row in rows:
        add_bbl_sp_flag(row)
        add_bbl_sp_bldg_cat_flag(row)
    return rows
