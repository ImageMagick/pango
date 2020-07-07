#!/usr/bin/python

from __future__ import print_function, division, absolute_import
import sys
import os.path
from collections import OrderedDict


header = []
ranges = OrderedDict()

def load_data(filename, prefix=""):
        global header, ranges
        f = open(filename)
        lines = f.readlines()
        for line in lines:
                if not line.startswith("#"):
                        break
                header.append(line)

        for line in lines:
	        line = line.strip()
	        if not line or line[0] == '#':
		        continue
	        rang, typ = [s.strip() for s in line.split('#')[0].split(';')[:2]]
	        typ = prefix + typ

	        rang = [int(s, 16) for s in rang.split('..')]
	        if len(rang) > 1:
		        start, end = rang
	        else:
		        start = end = rang[0]

	        if typ not in ranges:
		        ranges[typ] = []
	        if ranges[typ] and ranges[typ][-1][1] == start - 1:
		        ranges[typ][-1] = (ranges[typ][-1][0], end)
	        else:
		        ranges[typ].append((start, end))


def onecondition(start, end):
        condition = ''
        if start == end:
                condition = 'wc == 0x' + format(start, '04X')
        elif start < end:
                condition = '(' + 'wc >= 0x' + format(start, '04X') + ' && ' + 'wc <= 0x' + format(end, '04X') + ')'
        return condition


# print out the numbers in compact form
def print_if_branch(ranges):
        conditions = []
        for start, end in ranges:
                condition = onecondition(start, end)
                conditions.append(condition)
        statement = "||\n".join(conditions)
        print("if (%s)" % statement)
        print("\treturn TRUE;")
        print("return FALSE;")


def print_one_line(start, end):
        if start < end:
                outline = 'if (' + onecondition(start, end) + ')'
                print(outline)

def print_ranges(ranges):
        if 4 >= len(ranges):
                conditions = []
                for start, end in ranges:
                        conditions.append(onecondition(start, end))

                statement = " ||\n".join(conditions)
                print('if (' + statement + ')')
                print('\treturn TRUE;')
                return

        start = ranges[0][0]
        end = ranges[-1][1]
        print_one_line(start, end)
        print('{')
        print_balanced_search(ranges)
        print('}')


# print if branch like 4-way balanced search
def print_balanced_search(ranges):
        if 4 >= len(ranges):
                print_ranges(ranges)
                print("return FALSE;")
                return

        length = len(ranges)
        step = int(length / 4)
        first = step
        second = int(length * 2 / 4)
        third = second + step

        newranges = ranges[0:first]
        print_ranges(newranges)

        newranges = ranges[first:second]
        print_ranges(newranges)

        newranges = ranges[second:third]
        print_ranges(newranges)

        newranges = ranges[third:]
        print_ranges(newranges)

        print("return FALSE;")


def print_table():
        global header, ranges
        print("/* == Start of generated table == */")
        print("/*")
        print(" * The following tables are generated by running:")
        print(" *")
        print(" *   ./gen-break-table.py SentenceBreakProperty.txt IndicSyllabicCategory.txt EastAsianWidth.txt | indent")
        print(" *")
        print(" * on files with these headers:")
        print(" *")
        for l in header:
	        print(" * %s" % (l.strip()))
        print(" */")
        print()
        print("#ifndef PANGO_BREAK_TABLE_H")
        print("#define PANGO_BREAK_TABLE_H")
        print()
        print("#include <glib.h>")
        print()

        for typ,s in ranges.items():
	        if typ not in ['STerm',
	                       'Virama',
	                       'Vowel_Dependent',
	                       'Consonant_Prefixed',
	                       'Consonant_Preceding_Repha']: continue
	        print()
	        print("static inline gboolean _pango_is_%s (gunichar wc)" % typ)
	        print("{")
	        print_balanced_search(sorted(s))
	        print("}")

        s = ranges["EastAsian_F"] + ranges["EastAsian_W"] + ranges["EastAsian_H"]
        print("static inline gboolean _pango_is_EastAsianWide (gunichar wc)")
        print("{")
        print_balanced_search(sorted(s))
        print("}")

        print()
        print("#endif /* PANGO_BREAK_TABLE_H */")
        print()
        print("/* == End of generated table == */")


if __name__ == "__main__":
        if len (sys.argv) != 4:
	        print("usage: ./gen-break-table.py SentenceBreakProperty.txt IndicSyllabicCategory.txt EastAsianWidth.txt | indent", file=sys.stderr)
	        sys.exit (1)

        load_data(sys.argv[1])
        load_data(sys.argv[2])
        load_data(sys.argv[3], "EastAsian_")
        print_table()