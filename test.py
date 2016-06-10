import unittest
from derived_columns import *
from datetime import date

class Test_highest_sale_for_that_day(unittest.TestCase):
    
    def test_highest_sale_for_that_day(self):
        rows  = [
            {'bbl': '1', 'SalePrice': 10, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '1', 'SalePrice': 20, 'SaleDate': date(2015, 1, 1)}
        ]

        self.assertEqual(highest_sale_for_that_day(rows, rows[0]), 20)
        self.assertEqual(highest_sale_for_that_day(rows, rows[2]), 20)
        self.assertEqual(highest_sale_for_that_day(rows, rows[1]), 80)


class Test_remove_duplicate_sales_on_same_day(unittest.TestCase):

    def test_removes_duplicates(self):
        rows = [
            {'bbl': '1', 'SalePrice': 10, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '1', 'SalePrice': 20, 'SaleDate': date(2015, 1, 1)}
        ]
        _rows = remove_duplicate_sales_on_same_day(rows)
        self.assertEqual(len(_rows), 2)
        self.assertEqual(_rows, [
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '1', 'SalePrice': 20, 'SaleDate': date(2015, 1, 1)}
        ])

    def test_picks_only_one_even_when_price_is_the_same(self):
        rows = [
            {'bbl': '1', 'SalePrice': 10, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '1', 'SalePrice': 20, 'SaleDate': date(2015, 1, 1)}
        ]
        _rows = remove_duplicate_sales_on_same_day(rows)
        self.assertEqual(len(_rows), 2)
        self.assertEqual(_rows, [
            {'bbl': '2', 'SalePrice': 80, 'SaleDate': date(2015, 1, 1)},
            {'bbl': '1', 'SalePrice': 20, 'SaleDate': date(2015, 1, 1)}
        ])

class Test_counter_id(unittest.TestCase):

    def test_counterid_equals_one_if_salecount_is_one(self):
        rows = [
            {'bbl':'1', 'SaleCount': 1}, 
            {'bbl':'2', 'SaleCount': 1}
        ]
        self.assertEqual(counter_id(rows),[
            {'bbl': '1', 'SaleCount': 1, 'CounterId': 1}, 
            {'bbl': '2', 'SaleCount': 1,'CounterId': 1}
        ])
    
    # def test_counterid_ranks_sale_price(self):
    #     rows = [
    #         {'bbl': '1', 'SalePrice': 10},
    #         {'bbl': '1', 'SalePrice': 20},
    #         {'bbl': '1', 'SalePrice': 15},
    #         {'bbl': '2', 'SalePrice': 200},
    #         {'bbl': '3', 'SalePrice': 2},
    #         {'bbl': '3', 'SalePrice': 3},
    #     ]
    #     _rows = counter_id(rows)
        
    #     self.assertEqual(_rows, [
    #         {'bbl': '1', 'SalePrice': 10, 'CounterId': 3},
    #         {'bbl': '1', 'SalePrice': 20, 'CounterId': 1},
    #         {'bbl': '1', 'SalePrice': 15, 'CounterId': 2},
    #         {'bbl': '2', 'SalePrice': 200, 'CounterId': 1},
    #         {'bbl': '3', 'SalePrice': 2, 'CounterId': 1},
    #         {'bbl': '3', 'SalePrice': 3, 'CounterId': 2}
    #     ])

if __name__ == '__main__':
    unittest.main()

