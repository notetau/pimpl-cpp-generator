#!/usr/bin/env python

# Copyright (c) 2015 Noto, Yuta
# Released under the MIT license
# http://opensource.org/licenses/mit-license.php

import sys
import os
import re
import argparse
import shlex
sys.path.append(os.path.dirname(__file__) + "/llvm3.6")
import clang.cindex as cl
cl.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-3.6.so')


class PimplGenerator:
    def __init__(self, args):
        self._src_file = args.src_file
        self._target_class = args.target_class
        if self._target_class.startswith('::'):
            self._target_class = self._target_class[2:]
        self._dammy_var_prefix = args.dammy_var_prefix
        self._output_class = args.output_class
        self._pimpl_name = args.pimpl_name
        self._decl_with_def = args.decl_with_def

        self.namespace = []
        self.class_info = None

    def parse(self):
        index = cl.Index.create()
        tu = index.parse(self._src_file, args=['-std=c++11']) # args=None, unsaved_files=None, options = 0
        self._parse(tu.cursor)
        return self.class_info

    def _parse_children(self, cursor):
        for c in cursor.get_children():
            self._parse(c)

    def _get_fullname(self, name):
        name = "::".join(self.namespace + [name])
        m = re.search(r'<', name);
        if m: name = name[:m.start()]
        return name

    def _parse(self, cursor):
        found = False
        if cursor.kind == cl.CursorKind.NAMESPACE:
            self.namespace.append(cursor.displayname)
            self._parse_children(cursor)
            self.namespace.pop()

        elif cursor.kind in {
                cl.CursorKind.CLASS_DECL, cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_TEMPLATE
                }:
            if self._target_class == self._get_fullname(cursor.displayname):
                if not found:
                    self._parse_class(cursor)
                    found = True
                else:
                    raise Exception('multiple found')
            self._parse_children(cursor)
        else:
            self._parse_children(cursor)


    # CLASS PARSER
    def _parse_class(self, cursor):
        #print cursor.displayname
        #print cursor.kind
        #print self._get_token_str(cursor)

        class_info = {
            'constructor_info':[],
            'func_info':[],
            'template_args': [],
            'class_sig': '',
            'class_name': '',
            'class_decl': ''
        }
        cls_sig = self._get_token_str(cursor)
        idx = cls_sig.find(':')
        if idx > 0:
            cls_sig = cls_sig[:idx]
        idx = cls_sig.find('{')
        if idx > 0:
            cls_sig = cls_sig[:idx]

        cls_sig = cls_sig.strip()
        class_info['class_sig'] = cls_sig

        # class name check
        temp_cls_sig = cls_sig.split()
        class_name = temp_cls_sig[-1]
        if not self._target_class.endswith(class_name):
            raise Exception('invalid class name?')

        class_info['class_name'] = class_name
        class_info['class_decl'] = ' '.join(temp_cls_sig[:-1])

        for c in cursor.get_children():
            if c.kind in {cl.CursorKind.TEMPLATE_TYPE_PARAMETER, cl.CursorKind.TEMPLATE_NON_TYPE_PARAMETER}:
                targ_sig = self._get_token_str(c)
                targ_sig = targ_sig.strip().strip(",>").strip()
                targ_name = c.displayname
                if targ_name == '':
                    raise Exception()
                class_info['template_args'].append({'sig': targ_sig, 'name': targ_name})

            elif c.kind in {cl.CursorKind.CXX_METHOD, cl.CursorKind.FUNCTION_TEMPLATE}:
                if c.access_specifier == cl.AccessSpecifier.PUBLIC:
                    self._parse_func(class_info, c)

            elif c.kind == cl.CursorKind.CONSTRUCTOR:
                if c.access_specifier == cl.AccessSpecifier.PUBLIC:
                    self._parse_constructor(class_info, c)

        self.class_info = class_info


    # FUNC PARSER
    def _get_token_str(sef, cursor):
        return ' '.join(map(lambda x:x.spelling, cursor.get_tokens()))

    def _parse_constructor(self, class_info, cursor):
        # print cursor.kind

        func_info = {
            'template_args': [],
            'func_name': cursor.spelling,
            'args':[],
        }

        dammy_count = 0
        for c in cursor.get_children():

            if c.kind == cl.CursorKind.PARM_DECL:
                arg_sig = self._get_token_str(c)
                arg_sig = arg_sig.strip().strip(",)").strip()
                arg_name = c.displayname
                if arg_name == '':
                    arg_name = self._dammy_var_prefix + str(dammy_count)
                    arg_sig += ' ' + arg_name
                    dammy_count += 1
                func_info['args'].append({'sig':arg_sig, 'name':arg_name})

            elif c.kind in {cl.CursorKind.TEMPLATE_TYPE_PARAMETER, cl.CursorKind.TEMPLATE_NON_TYPE_PARAMETER}:
                targ_sig = self._get_token_str(c)
                targ_sig = targ_sig.strip().strip(",>").strip()
                targ_name = c.displayname
                if targ_name == '':
                    raise Exception()
                func_info['template_args'].append({'sig': targ_sig, 'name': targ_name})

        class_info['constructor_info'].append(func_info)

    def _parse_func(self, class_info, cursor):
        func_info = {
            'result': cursor.result_type.spelling,
            'template_args': [],
            'func_name': cursor.spelling,
            'args':[],
            'is_void': cursor.result_type.spelling == 'void',
        }

        dammy_count = 0
        for c in cursor.get_children():
            if c.kind == cl.CursorKind.PARM_DECL:
                arg_sig = self._get_token_str(c)
                arg_sig = arg_sig.strip().strip(",)").strip()
                arg_name = c.displayname
                if arg_name == '':
                    arg_name = self._dammy_var_prefix + str(dammy_count)
                    arg_sig += ' ' + arg_name
                    dammy_count += 1
                func_info['args'].append({'sig':arg_sig, 'name':arg_name})

            elif c.kind in {cl.CursorKind.TEMPLATE_TYPE_PARAMETER, cl.CursorKind.TEMPLATE_NON_TYPE_PARAMETER}:
                targ_sig = self._get_token_str(c)
                targ_sig = targ_sig.strip().strip(",>").strip()
                targ_name = c.displayname
                if targ_name == '':
                    raise Exception()
                func_info['template_args'].append({'sig': targ_sig, 'name': targ_name})

        # print func_info
        class_info['func_info'].append(func_info)

    def _gen_pimpl_func(self, func_info, inline_def=False):
        fcode = ''
        for finfo in func_info:
            if len(finfo['template_args']) != 0:
                fcode += '    template<{0}>\n'.format(
                    ', '.join(map(lambda x: x['sig'], finfo['template_args']))
                )
            fcode += '    {0} {1}({2})'.format(finfo['result'], finfo['func_name'],
                ', '.join(map(lambda x: x['sig'], finfo['args']))
            )

            if inline_def:
                fcode += ' {\n'
                fcode += '        {0}{1}->{2}({3});\n'.format(
                    '' if finfo['is_void'] else 'return ',
                    self._pimpl_name,
                    finfo['func_name'],
                    ', '.join(map(lambda x: x['name'], finfo['args']))
                )
                fcode += '    }'
            else:
                fcode += ';'
            fcode += '\n\n'
        return fcode

    def _gen_pimpl_constructor(self, constructor_info, inline_def=False):
        fcode = ''

        for finfo in constructor_info:
            if len(finfo['template_args']) != 0:
                fcode += '    template<{0}>\n'.format(
                    ', '.join(map(lambda x: x['sig'], finfo['template_args']))
                )

            fcode += '    {0}({1})'.format(self._output_class,
                                             ', '.join(map(lambda x: x['sig'], finfo['args']))
                                             )
            if inline_def:
                fcode += ' : {0}(new {1}({2})) {{}}'.format(self._pimpl_name,
                                                            finfo['func_name'],
                                                            ', '.join(map(lambda x: x['name'], finfo['args']))
                                                            )
            else:
                fcode += ';'

            fcode += '\n\n'

        if len(constructor_info) == 0:
            # create default constructor
            fcode += '    {0}()'.format(self._output_class)
            if inline_def:
                fcode += ' : {0}(new {1}()) {{}}'.format(self._pimpl_name, self._target_class)
            else:
                fcode += ';'
            fcode += '\n\n'
        return fcode

    def _gen_pimpl_def(self, class_info):
        fcode = ''
        for finfo in class_info['constructor_info']:
            if len(finfo['template_args']) != 0:
                fcode += '    template<{0}>\n'.format(
                    ', '.join(map(lambda x: x['sig'], finfo['template_args']))
                )
            fcode += '{0}::{1}({2})'.format(self._output_class,
                                            self._output_class,
                                           ', '.join(map(lambda x: x['sig'], finfo['args']))
                                           )
            fcode += ' : {0}(new {1}({2})) {{}}\n\n'.format(self._pimpl_name,
                                                            finfo['func_name'],
                                                            ', '.join(map(lambda x: x['name'], finfo['args']))
                                                            )
        fcode += '{0}::~{0}() {{ delete {1}; }}\n\n'.format(self._output_class, self._pimpl_name)

        for finfo in class_info['func_info']:
            if len(finfo['template_args']) != 0:
                fcode += 'template<{0}>\n'.format(
                    ', '.join(map(lambda x: x['sig'], finfo['template_args']))
                )
            fcode += '{0} {1}::{2}({3}) {{\n'.format(
                                           finfo['result'],
                                           self._output_class,
                                           finfo['func_name'],
                                           ', '.join(map(lambda x: x['sig'], finfo['args']))
                                           )
            fcode += '    '
            if not finfo['is_void']: fcode += 'return '
            fcode += '{0}->{1}({2});\n'.format(self._pimpl_name,
                                              finfo['func_name'],
                                              ', '.join(map(lambda x: x['name'], finfo['args']))
                                              )
            fcode += '}\n\n'

        return fcode

    def generate_code(self):
        class_info = self.class_info

        code = ''
        code += '{0} {1}{2}'.format(class_info['class_decl'], self._output_class, '')
        code += ' {\n'
        code += 'public:\n'
        code += self._gen_pimpl_constructor(class_info['constructor_info'], self._decl_with_def)
        code += self._gen_pimpl_func(class_info['func_info'], self._decl_with_def)
        code += 'private:\n'
        code += '    class {0};\n'.format(self._target_class)
        code += '    {0}* {1};\n'.format(self._target_class, self._pimpl_name)
        code += '};'

        #outside definitions
        d_code = ''
        if not self._decl_with_def:
            d_code += self._gen_pimpl_def(class_info)

        return (code, d_code)

def parse_args(args=None):
    parser = argparse.ArgumentParser(description='pimpl class generator')
    parser.add_argument('src_file', nargs='?', default='tests/cppsrc/basic1.cpp')
    parser.add_argument('-t', '--target-class', nargs='?', default='Basic2')
    parser.add_argument('-v', '--dammy-var-prefix', nargs='?', default='pimplvar')
    parser.add_argument('-o', '--output-class', nargs='?', default='Basic2Wrap')
    parser.add_argument('--pimpl-name', nargs='?', default='pimpl')
    parser.add_argument('--decl-with-def', action='store_true', default=False)

    if type(args) == str:
        args = shlex.split(args)
    args = parser.parse_args(args)
    return args


if __name__ == '__main__':
    args = parse_args()

    generator = PimplGenerator(args)
    class_info = generator.parse()

    codes = generator.generate_code()
    # output to stdout
    print codes[0]
    print ''
    print codes[1]