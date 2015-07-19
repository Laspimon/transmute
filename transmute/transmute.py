#! -*-coding:utf8-*-
from __future__ import print_function
import copy

INDEVISIBLE_FORMS = [str, unicode, int, float]

left_form = {
    'key': 'abc123',
    'name': {'first': 'joe', 'last': 'stein'},
    'triples': {1: 3, 2: 6, 3: 9, 4: 12, 5: 15},
    'opposites': [('low','high'),('big','small')]
    }
right_form = {
    'uuid': 'abc123',
    'first_name': 'joe',
    'last_name': 'stein',
    'triple_tuples': [(1, 3), (2, 6), (3, 9), (4, 12), (5, 15)],
    'opposites': [{'first': 'low', 'second': 'high'}, {'first': 'big', 'second': 'small'}]
    }

class TranslationModeller(object):
    """Takes two structures and formulates a translation model.

    Input tree and output tree must share contents, so that the methods below
    can recognize the structures, and how to translate between them."""

    debug = False

    def __init__(self, input_tree, output_tree, debug = False):
        if debug: self.debug = True
        self.left = input_tree
        self.l_structure = []
        self.right = output_tree
        self.r_structure = []

    def get_key_val(self, container, overview = None, navi = None, level = None):
        if overview is None: overview = []
        if navi is None: navi = []
        if level is None: level = 0

        if self.debug: print ('container', container)
        if isinstance(container, dict):
            container, overview, navi, level = self.get_dict(
                    container, overview, navi, level)
        elif isinstance(container, list):
            container, overview, navi, level = self.get_list(
                    container, overview, navi, level)
        elif isinstance(container, tuple):
            container, overview, navi, level = self.get_tuple(
                    container, overview, navi, level)
        return overview, navi

    def get_dict(self, container, overview, navi, level):
        for k,v in container.items():
            if type(v) in INDEVISIBLE_FORMS:
                if self.debug: self.printout(container, overview, navi, level, k, v, 'dict_1')
                overview.append(navi[:] +\
                    [[dict, container.keys(), type(v), v, k]])
                    #[['final', dict, len(container), type(v), len(v), k, v]])
                #print ('|||', [['final', dict, len(container), type(v), len(v), k, v]])                    
            else:
                if self.debug: self.printout(container, overview, navi, level, k, v, 'dict_2')
                level += 1
                navi.append([dict, container.keys(), type(v), len(v), k])
                overview, navi = self.get_key_val(v, overview, navi, level)
                navi = navi[:-1]
                level -= 1
        return container, overview, navi, level

    def get_list(self, container, overview, navi, level):
        for i,v in enumerate(container):
            if type(v) in INDEVISIBLE_FORMS:
                if self.debug: self.printout(container, overview, navi, level, i, v, 'list_1')
                overview.append(navi[:] +\
                    [[list, len(container), type(v), v, i]])
            else:
                if self.debug: self.printout(container, overview, navi, level, i, v, 'list_2')
                level += 1
                navi.append([list, len(container), type(v), len(v), i])
                overview, navi = self.get_key_val(v, overview, navi, level)
                navi = navi[:-1]
                level -= 1
        return container, overview, navi, level

    def get_tuple(self, container, overview, navi, level):
        for i,v in enumerate(container):
            if type(v) in INDEVISIBLE_FORMS:
                overview.append(navi[:] +\
                    [[tuple, len(container), type(v), v, i]]) #!! list -> tuple
                if self.debug: self.printout(container, overview, navi, level, i, v, 'tuple_1')
            else:
                if self.debug: self.printout(container, overview, navi, level, i, v, 'tuple_2')
                level += 1
                navi.append([tuple, len(container), type(v), len(v), i]) #!! list -> tuple
                overview, navi = self.get_key_val(v, overview, navi, level)
                navi = navi[:-1]
                level -= 1
        return container, overview, navi, level

    @staticmethod
    def printout(container, overview, navi, level, key, val, msg):
        level += 1
        print()
        print('____________________________', msg)
        print (container)
        print (key, '\t\t', val)
        #print ('navi ', navi)
        print ('lvl  ', level)
        print('navi:')
        for i,x in enumerate(navi):
            for y in x:
                print (level*'|' + (1+i)*4*' ', y)
        print('overview:')
        for i,x in enumerate(overview):
            for y in x:
                print (level*'#' + (1+i)*4*' ', y)
        print ()

class Transmute(object):
    """Translates data between two forms.

    Initialize with two structures to create translation models, allowing to
    translate data between the two parallel representations.
    """
    debug = False
    def __init__(self, left, right, debug = False):
        if debug: self.debug = True
        self.left_right = TranslationModeller(left_form, right_form, debug)
        self.l_overview, navi = self.left_right.get_key_val(left_form)
        self.right_left = TranslationModeller(right_form, left_form, debug)
        self.r_overview, navi = self.right_left.get_key_val(right_form)

    def convert_to_tuples(self, road, output):
        next_level = output
        for step in road:
            if self.debug: print (road)
            if child_type is tuple:
                next_level[index] = tuple(next_level[index])
            next_level = next_level[index]
        return next_level

    def follow_roadmap(self, road, output):
        next_level = output
        for step in road:
            if self.debug: print (road)
            container_type, container_info, child_type, child_info, index = step
            if container_type is dict:
                next_level = self.open_dict_container(next_level, container_type,
                            container_info, child_type, child_info, index)
            elif container_type is list or container_type is tuple:
                next_level = self.open_list_container(next_level, container_type,
                            container_info, child_type, child_info, index, output)
        return next_level

    def recreate(self, overview, output = None):
        if output is None: output = {}
        for road in overview:
            next_level = self.follow_roadmap(road = road, output = output)
        for road in overview:
            self.convert_to_tuples(road = road, output = output)
        return output

    def test_it(self, l_tree, r_tree):
        l_recreated = self.recreate(self.l_overview)
        if l_recreated == l_tree:
            print (True)
        else:
            print (False)
            print ('|', l_tree)
            print ('|', l_recreated)
        print(4 * '========')
        
        r_recreated = self.recreate(self.r_overview)
        if r_recreated == r_tree:
            print (True)
        else:
            print (False)
            print ('|', r_tree)
            print ('|', r_recreated)
        print(4 * '========')
        print(4 * '========')

    def open_dict_container(self, next_level, container_type, container_info, child_type, child_info, index):
        if len(next_level) == 0:
            for key in container_info:
                if not key in next_level.keys():
                    next_level[key] = None
        if child_type is dict:
            if next_level[index] is None:
                next_level[index] = child_type()
            next_level = next_level[index]
        elif child_type is list:
            if next_level[index] is None:
                next_level[index] = child_type()
            if not index in next_level.keys():
                next_level[index] = child_type()
            next_level = next_level[index]
        elif child_type is str or child_type is unicode:
            next_level[index] = child_info
        elif child_type is int or child_type is float:
            next_level[index] = child_info
        else:
            print('___________fail 1')
        return next_level

    def open_list_container(self, next_level, container_type, container_info, child_type, child_info, index, output = None):
        for x in range(container_info-len(next_level)):
            next_level.append(None)
        self.printout_list(next_level, container_type, container_info, 
                           child_type, child_info, index, output, 'Open List')
        if child_type is list or child_type is tuple:
            if len(next_level) == 0:
                for x in range(container_info):
                    next_level.append(None)
            elif not container_info == len(next_level):
                print ('container_info != len(next_level)')
                for x in range(container_info-len(next_level)):
                    next_level.append(None)
            if next_level[index] is None:
                next_level[index] = []
            next_level = next_level[index]
        elif child_type in [str, unicode, int, float]:
            next_level[index] = child_info
        elif child_type is dict:
            if next_level[index] is None:
                next_level[index] = child_type()
            next_level = next_level[index]
        else:
            print('___________fail 2', child_type)
        self.printout_list(next_level, container_type, container_info, child_type, child_info, index, output, 'Open List')
        return next_level

    def printout_list(self, next_level, container_type, container_info, child_type, child_info, index, output, msg):
        if not self.debug: return
        print()
        print('____________________________', msg)
        print('next_level:    ',     next_level)
        print('container_type:', container_type)
        print('container_info:', container_info)
        print('child_type:    ', child_type)
        print('child_info:    ', child_info)
        print('index:         ', index)
        print('output:        ', output)
        print ()


#modeller = TranslationModeller(left_form, right_form, False)
#for x in modeller.get_key_val(left_form, [], [], 0):
#    print (x)

print ('left\n', left_form)
print ('right\n', right_form)
print()

left_form = {'opposites': [('low','high'),('big','small')]}
right_form = {'opposites': [{'first': 'low', 'second': 'high'}, {'first': 'big', 'second': 'small'}]}

example = Transmute(left_form, right_form, False)
example.test_it(left_form, right_form)

left_form = {
    'key': 'abc123',
    'name': {'first': 'joe', 'last': 'stein'},
    'triples': {1: 3, 2: 6, 3: 9, 4: 12, 5: 15},
    'opposites': [('low','high'),('big','small')]
    }
right_form = {
    'uuid': 'abc123',
    'first_name': 'joe',
    'last_name': 'stein',
    'triple_tuples': [(1, 3), (2, 6), (3, 9), (4, 12), (5, 15)],
    'opposites': [{'first': 'low', 'second': 'high'}, {'first': 'big', 'second': 'small'}]
    }

example = Transmute(left_form, right_form, False)
example.test_it(left_form, right_form)


