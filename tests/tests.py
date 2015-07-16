#! -*-coding:utf8-*-
from __future__ import print_function

from transmute.transmute import retrieve_key_val, retrieve_dict, recreate, 

def test_it(input_tree):
    print(input_tree)
    a,b = retrieve_key_val(input_tree)
    recreated = recreate(a)
    if recreated == input_tree: 
        print (True)
    else: 
        print (False, recreated)
    print(4*'========')
    print(4*'========')
    print()    


nested_1 = {
    '1lvl': {
        '2lvl': {
            '3lvla': 'a', 
            '3lvlb': 'b', 
            '3lvlc': 'c' 
        }}}

nested_2 = {
    '1x': {
        '2x': {
            '3xa': 'a', 
            '3xb': 'b', 
            '3xc': 'c' 
        },
        '2y': {
            '3ya': 'a', 
            '3yb': 'b', 
            '3yc': 'c' 
        }}}

test_it(nested_1)
test_it(nested_2)

