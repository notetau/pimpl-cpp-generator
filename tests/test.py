# Copyright (c) 2015 Noto, Yuta
# Released under the MIT license
# http://opensource.org/licenses/mit-license.php

import sys
import os
import pprint

sys.path.append(os.path.dirname(__file__) + '/..')
import pimplgen
from nose.tools import ok_, eq_

BASE_DIR = os.path.dirname(__file__)

def check_info(command, answer):
    args = pimplgen.parse_args(command)
    generator =  pimplgen.PimplGenerator(args)
    class_info = generator.parse()

    eq_(answer, class_info)


def gen_class_info(command):
    args = pimplgen.parse_args(command)
    generator =  pimplgen.PimplGenerator(args)
    class_info = generator.parse()
    return class_info


def test_basic1():
    args = {
        'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
        'target_class': 'Basic1',
        'output_class': 'TBasic1,'
    }
    cmd = '{src_file} -t {target_class} -o {output_class}'.format(**args)
    answer = {'class_decl': 'template < typename U = int > struct',
             'class_name': 'Basic1',
             'class_sig': 'template < typename U = int > struct Basic1',
             'constructor_info': [],
             'func_info': [{'args': [{'name': 'x', 'sig': 'float x'}], 'func_name': 'foo', 'is_void': False, 'result': 'int', 'template_args': []},
                           {'args': [{'name': 'pimplvar0', 'sig': 'int pimplvar0'}, {'name': 'y', 'sig': 'float y'}, {'name': 'pimplvar1', 'sig': 'double pimplvar1'}],
                            'func_name': 'bar',
                            'is_void': True,
                            'result': 'void',
                            'template_args': []},
                           {'args': [{'name': 'z', 'sig': 'int z = ( 42 )'}], 'func_name': 'baz', 'is_void': True, 'result': 'void', 'template_args': []},
                           {'args': [], 'func_name': 'qux', 'is_void': False, 'result': 'double', 'template_args': []},
                           {'args': [{'name': 't', 'sig': 'T t'}], 'func_name': 'norf', 'is_void': False, 'result': 'T', 'template_args': [{'name': 'T', 'sig': 'typename T'}, {'name': 'N', 'sig': 'long N'}]}],
             'template_args': [{'name': 'U', 'sig': 'typename U = int'}]}
    check_info(cmd, answer)

def test_basic2():
    args = {
        'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
        'target_class': 'Basic2',
        'output_class': 'TBasic2,'
    }
    cmd = '{src_file} -t {target_class} -o {output_class}'.format(**args)
    answer = {'class_decl': 'struct',
             'class_name': 'Basic2',
             'class_sig': 'struct Basic2',
             'constructor_info': [],
             'func_info': [{'args': [], 'func_name': 'bar', 'is_void': True, 'result': 'void', 'template_args': []},
                           {'args': [{'name': 'x', 'sig': 'int x'}], 'func_name': 'baz', 'is_void': False, 'result': 'int', 'template_args': []}],
             'template_args': []}
    check_info(cmd, answer)

if __name__ == '__main__':
    test_basic2()
    # pprint.pprint(answer, width=200)
