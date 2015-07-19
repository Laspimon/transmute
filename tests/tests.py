#! -*-coding:utf8-*-
from __future__ import print_function

from transmute.transmute import retrieve_key_val, retrieve_dict, recreate, INDEVISIBLE_FORMS


left_form = {'key': 'abc123'}
right_form = {'uuid': 'abc123'}
specific_input = {'key': 'defghi'}
specific_output = {'uuid': 'defghi'}

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

def test_retrieve_dict():
    in_container, in_overview, in_navi, in_level = left_form, [], [], 0
    out_container, out_overview, out_navi, out_level = retrieve_dict(in_container, in_overview, in_navi, in_level)

    in_container, in_overview, in_navi, in_level = nested_1, [], [], 0
    out_container, out_overview, out_navi, out_level = retrieve_dict(in_container, in_overview[:], in_navi[:], in_level)
    expect_overview = [[
        [dict, ['1lvl'], dict, 1, '1lvl'],
        [dict, ['2lvl'], dict, 3, '2lvl'],
        [dict, {'3lvla': 'a', '3lvlb': 'b', '3lvlc': 'c'}]
        ]]
    if (out_container, out_overview, out_navi, out_level) == (in_container, expect_overview, [], 0):
        print ('Good')
    else:
        for i, in_out in enumerate(((in_container, out_container), (expect_overview, out_overview), (in_navi, out_navi), (in_level, out_level))):
            if not in_out[0] == in_out[1]:
                print (i, '>', in_out[0])
                print (i, '<', in_out[1])

    in_container, in_overview, in_navi, in_level = nested_2, [], [], 0
    out_container, out_overview, out_navi, out_level = retrieve_dict(in_container, in_overview[:], in_navi[:], in_level)
    expect_overview = [[
        [dict, ['1x'], dict, 2, '1x'], [dict, ['2x', '2y'], dict, 3, '2x'], 
        [dict, {'3xa': 'a', '3xb': 'b', '3xc': 'c'}]], 
        [
            [dict, ['1x'], dict, 2, '1x'], 
            [dict, ['2x', '2y'], dict, 3, '2y'], 
            [dict, {'3yc': 'c', '3yb': 'b', '3ya': 'a'}]
        ]]
    if (out_container, out_overview, out_navi, out_level) == (in_container, expect_overview, [], 0):
        print ('Good')
    else:
        for i, in_out in enumerate(((in_container, out_container), (expect_overview, out_overview), (in_navi, out_navi), (in_level, out_level))):
            if not in_out[0] == in_out[1]:
                print (i, '>', in_out[0])
                print (i, '<', in_out[1])


def test_retrieve_key_val(input_tree):
    a,b = retrieve_key_val(input_tree)
    


def test_it(input_tree):
    return
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


#test_it(nested_1)
#test_it(nested_2)

test_retrieve_dict()
test_retrieve_key_val(left_form)
