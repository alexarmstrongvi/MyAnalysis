#!/bin/bash/env python
"""
Program: text_to_latex_table.py
Author: Alex Armstrong <alarmstr@cern.ch>
Copyright: (C) Dec 21st, 2017; University of California, Irvine
"""

import os
import sys
from argparse import ArgumentParser
from collections import defaultdict, namedtuple
from tabulate import tabulate
import python_tools as tools

# Higgs LFV column configuration
REGION_COL = 0
CHANNEL_COL = 1
SAMPLE_COL = 2
VALUE_COL = 3
ERROR_COL = 4
EMU_LABEL = 'emu'
MUE_LABEL = 'mue'

def get_tex_string(sample_map, region):
    caption  = 'Yields of the \\mu\\tau_{e} and e\\tau_{\\mu} channels '\
               'for the '+region+' selection. '\
               'BR(H \\rightarrow \\mu\\tau_{e}) and '\
               'BR(H \\rightarrow e\\tau_{\\mu}) are assumed to be 1%.'

    tex_str  = '\\begin{frame}{%s Region Yields}\n'%region
    tex_str += '    \\begin{table}[]\n'
    tex_str += '        \\tiny\n'
    tex_str += '        \centering\n'
    tex_str += '        \caption{%s}\n'%caption
    tex_str += '        \label{%s_yields}\n'%region
    tex_str += '        \\begin{tabular}{|l|l|l|}\n'
    tex_str += '            \hline\n'
    tex_str += '            \multirow{2}{*}{Samples}      & \multicolumn{2}{l|}{%s Selections} \\\\ \cline{2-3}\n'%region
    tex_str += '                                          & $\\mu\\tau_{e}$ & $e\\tau_{\\mu}$ \\\\ \hline \hline\n'
    for sample, val in sample_map.iteritems():
        tex_str += '            %*s & $%*.1f\pm%*.1f$ & $%*.1f\pm%*.1f$ \\\\ \hline\n'%(
                                35, sample, 7, val.mue_v, 7, val.mue_e, 7, val.emu_v, 7, val.emu_e)

    #tex_str += '            $H\\rightarrow\\tau\\tau$        & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            $H\\rightarrow WW$             & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            $Z\\rightarrow\\tau\\tau$+jets   & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            $Z\\rightarrow ee,\\mu\\mu$+jets & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            $t\\bar{t}$                    & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            Diboson                       & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            Fake Leptons                  & $1\pm1$         & $1\pm1$     \\\\ \hline \hline\n'
    #tex_str += '            Total Background              & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            Total LFV Signal              & $1\pm1$         & $1\pm1$     \\\\ \hline\n'
    #tex_str += '            Data                          & $1\pm1$         & $1\pm1$     \\\\ \hline \hline\n'
    tex_str += '        \end{tabular}\n'
    tex_str += '    \end{table}\n'
    tex_str += '\end{frame}\n'
    return tex_str


def LaTeXify_HiggsLFV(table, args):
    """ Build string of latex yield tables for Higgs LFV """
    #------------------------------------------------------------------------->>
    # Separate into maps for each region
    region_map = defaultdict(dict)
    lfv_row = namedtuple('lfv_row', 'mue_v, mue_e, emu_v, emu_e')
    for row in table:
        region  = row[REGION_COL]
        channel = row[CHANNEL_COL]
        sample  = row[SAMPLE_COL]
        value   = row[VALUE_COL]
        error   = row[ERROR_COL]

        if region not in region_map:
            region_map[region][sample] = lfv_row(0, 0, 0, 0)

        if channel == MUE_LABEL:
            region_map[region].mue_v = value
            region_map[region].mue_e = error
        elif channel == EMU_LABEL:
            region_map[region].emu_v = value
            region_map[region].emu_e = error

    #------------------------------------------------------------------------->>
    # Make string of all tables
    ltx_str = '\n'
    for region, region_tbl in region_map.iteritems():
        ltx_str += 'Yields for the {0} selection '\
                   'are shown in Table \\ref{{{0}_yields}}.\n'.format(region)
        ltx_str += get_tex_string(region_tbl, region)
        ltx_str += '\n'

    return ltx_str

def LaTeXify(table, args):
    """ Turn input """
    if args.HiggsLFV:
        return LaTeXify_HiggsLFV(table, args)
    if args.no_header:
        return tabulate(table, tablefmt="latex")
    return tabulate(table, headers='firstrow', tablefmt="latex")

#----------------------------------------------------------------------------->>
# =================================== MAIN ===================================
#----------------------------------------------------------------------------->>
def main():
    """ Main function """
    parser = ArgumentParser()
    parser.add_argument('file',
                        help='first txt file with sample names')
    parser.add_argument('-d', '--delimiter',
                        default=',',
                        help='delimiter used in input file')
    parser.add_argument('--HiggsLFV',
                        action='store_true',
                        help='Higgs LFV style yield table')
    parser.add_argument('--no_header',
                        action='store_true',
                        help='Do not add headers to table')
    parser.add_argument('-o', '--output',
                        default='',
                        help='output file name')
    args = parser.parse_args()

    #------------------------------------------------------------------------->>
    # Checks
    if not os.path.exists(args.file):
        print 'No such file %s'%args.file
        sys.exit()

    #------------------------------------------------------------------------->>
    # Set output name
    output_name = args.output
    if not output_name:
        name = args.file0.strip().split('/')[-1].split('.')[-2]
        output_name = '%s_Latexified'%(name)

    #------------------------------------------------------------------------->>
    # Prepare table for LaTeXification
    with open(args.file, 'r') as ifile, open(output_name, 'w') as ofile:
        table = [x for x in ifile.readlines() if x]
        table = [x.strip().split(args.delimiter) for x in table]
        table = [x for x in table if len(x) > 1]
        # Checks
        if len(table) == 1:
            print "ERROR :: Input file only has one row"
            sys.exit()
        elif not tools.good_matrix_shape(table):
            print "ERROR :: Differing number of elements per row"
            sys.exit()
        if len(table[0]) == 1:
            print "ERROR :: Input file only has one element per row"
            sys.exit()

        tbl_str = LaTeXify(table, args)
        ofile.write(tbl_str)


if __name__ == "__main__":
    # Do not execute main() when script is imported as a module
    main()
