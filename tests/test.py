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

def setup_module(module):
    # static library path for travis ci (trusty)
    pimplgen.cl.Config.set_compatibility_check(False)
    pimplgen.cl.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-3.4.so.1')

TEST_PARAMETER = [
    # 0
    ({
        'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
        'target_class': 'Basic1',
        'output_class': 'TBasic1'
    },
    {'class_decl': 'template < typename U = int > struct',
     'class_name': 'Basic1',
     'class_sig': 'template < typename U = int > struct Basic1',
     'constructor_info': [],
     'func_info': [{'args': [{'name': 'x', 'sig': 'float x'}], 'const': False, 'func_name': 'foo', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'pimplvar0', 'sig': 'int pimplvar0'}, {'name': 'y', 'sig': 'float y'}, {'name': 'pimplvar1', 'sig': 'double pimplvar1'}], 'const': False, 'func_name': 'bar', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'z', 'sig': 'int z = ( 42 )'}], 'const': False, 'func_name': 'baz', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False},
                   {'args': [], 'const': False, 'func_name': 'qux', 'is_void': False, 'restrict': False, 'result': 'double', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 't', 'sig': 'T t'}], 'const': False, 'func_name': 'norf', 'is_void': False, 'restrict': False, 'result': 'T', 'template_args': [{'name': 'T', 'sig': 'typename T'}, {'name': 'N', 'sig': 'long N'}], 'volatile': False}],
     'template_args': [{'name': 'U', 'sig': 'typename U = int'}]}
    ),
    # 1
    ({
        'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
        'target_class': 'Basic2',
        'output_class': 'TBasic2'
    },
    {'class_decl': 'struct',
     'class_name': 'Basic2',
     'class_sig': 'struct Basic2',
     'constructor_info': [],
     'func_info': [{'args': [], 'const': False, 'func_name': 'bar', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'x', 'sig': 'int x'}], 'const': False, 'func_name': 'baz', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': False}],
     'template_args': []}
    ),
    # 2
    (),
    # 3
    ( {
        'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
        'target_class': 'Basic4',
        'output_class': 'TBasic4'
    },
    {'class_decl': 'struct',
     'class_name': 'Basic4',
     'class_sig': 'struct Basic4',
     'constructor_info': [],
     'func_info': [{'args': [{'name': 'x', 'sig': 'float x'}], 'const': False, 'func_name': 'foo', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'x', 'sig': 'float x'}], 'const': False, 'func_name': 'foofoo', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': False},
                   {'args': [], 'const': False, 'func_name': 'bar', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': True},
                   {'args': [{'name': 'a', 'sig': 'char a'}], 'const': True, 'func_name': 'baz', 'is_void': False, 'restrict': False, 'result': 'int', 'template_args': [], 'volatile': False},
                   {'args': [], 'const': True, 'func_name': 'qux', 'is_void': False, 'restrict': False, 'result': 'double', 'template_args': [], 'volatile': True}],
     'template_args': []}
    ),
    # 4
    ( {
     'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
     'target_class': 'a::Basic5',
     'output_class': 'TBasic5'
    },
    {'class_decl': 'struct',
     'class_name': 'Basic5',
     'class_sig': 'struct Basic5',
     'constructor_info': [],
     'func_info': [{'args': [{'name': 'x', 'sig': 'float x'}], 'const': False, 'func_name': 'foo', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False}],
     'template_args': []}
    ),
    # 5
    ( {
     'src_file': BASE_DIR + '/cppsrc/basic1.cpp',
     'target_class': 'a::b::Basic6',
     'output_class': 'TBasic6'
    },
    {'class_decl': 'struct',
     'class_name': 'Basic6',
     'class_sig': 'struct Basic6',
     'constructor_info': [],
     'func_info': [{'args': [{'name': 'x', 'sig': 'int x'}], 'const': False, 'func_name': 'foo', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'b5', 'sig': 'Basic5 & b5'}], 'const': False, 'func_name': 'bar', 'is_void': True, 'restrict': False, 'result': 'void', 'template_args': [], 'volatile': False},
                   {'args': [{'name': 'other', 'sig': 'const Basic6 & other'}], 'const': False, 'func_name': 'operator=', 'is_void': False, 'restrict': False, 'result': 'a::b::Basic6 &', 'template_args': [], 'volatile': False}],
     'template_args': []}
    )
]

def check_pattern(idx):
    pattern = TEST_PARAMETER[idx]
    command = '{src_file} -t {target_class} -o {output_class}'.format(**pattern[0])
    args = pimplgen.parse_args(command)
    generator =  pimplgen.PimplGenerator(args)
    class_info = generator.parse()
    eq_(pattern[1], class_info)

def test_0() : check_pattern(0)
def test_1() : check_pattern(1)
def test_3() : check_pattern(3)
def test_4() : check_pattern(4)
def test_5() : check_pattern(5)

def run_pattern(idx):
    pattern = TEST_PARAMETER[idx]
    command = '{src_file} -t {target_class} -o {output_class}'.format(**pattern[0])
    args = pimplgen.parse_args(command)
    generator =  pimplgen.PimplGenerator(args)
    class_info = generator.parse()

    pprint.pprint(class_info, width=300)
    print '/////////////////////////////////////////////////////////////////////'
    codes = generator.generate_code()
    print codes[0]
    print ''
    print codes[1]

if __name__ == '__main__':
    setup_module(None)
    run_pattern(5)
