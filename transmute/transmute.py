#! -*-coding:utf8-*-
from __future__ import print_function

INDEVISIBLE_FORMS = [str, unicode, int, float]
debug = False


def printout(container, overview, navi, level, key, val, msg):
    pass

def retrieve_list(container, overview, navi, level):
    pass

def retrieve_tuple(container, overview, navi, level):
    pass

def retrieve_dict(container, overview, navi, level):
    pass

def retrieve_key_val(container, overview = None, navi = None, level = None):
    if overview is None: overview = []
    if navi is None: navi = []
    if level is None: level = 0
    if debug: print ('container', container)
    if type(container) in [str, unicode, int, float]:
        overview.append(navi[:] + [[str, container]])
        overview.append(
            navi[:] + [['final', list, len(container), type(v), len(v), i, v]])
    elif type(container) is list:
        container, overview, navi, level = retrieve_list(
            container, overview, navi, level)
    elif type(container) is tuple:
        container, overview, navi, level = retrieve_tuple(
            container, overview, navi, level)
    elif isinstance(container, dict):
        container, overview, navi, level = retrieve_dict(
            container, overview, navi, level)
    else:
        print('Error: Type unknown.')
    return overview, navi

def open_dict_container(next_level, container_type, container_info, child_type, child_info, index):
    pass

def printout_list(next_level, container_type, container_info, child_type, child_info, index, output, msg):
    if not debug: return
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

def open_list_container(next_level, container_type, container_info, child_type, child_info, index, output = None):
    pass

def follow_roadmap(road, output):
    pass

def finalize(items = None, next_level = None):
    pass

def recreate(overview, output = None):
    pass


