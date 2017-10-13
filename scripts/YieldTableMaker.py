#!/bin/bash/env python

import sys
import argparse
import collections
import tabulate
import ROOT
import global_variables as g
BinZ = ROOT.RooStats.NumberCountingUtils.BinomialExpZ

# Get User Inputs
parser = argparse.ArgumentParser()
parser.add_argument('file_name', help='input file name  with yield table values (tab separated)')
parser.add_argument('-o', '--output', default='LatexYieldTable.tex', dest='ofile')
args = parser.parse_args()
tbl_dict = {}
col_to_sample = {}
first_row_header = 'Selection'
data_name = 'data_all'
sig_name = 'Signal'
n_col = 8
table_rows = collections.OrderedDict([
    ('HWW' , 'HWW'),
    ('Wjets' , 'W+Jets'),
    ('Diboson' , 'VV'),
    ('Top' , 'Top'),
    ('Ztt_ZttEW' , 'Ztautau'),
    ('Zll_ZEW' , 'Zll'),
    (data_name , 'Data' ),
    (sig_name , 'Signal'),
    ('MC total' , 'MC total'),
    ('Data/MC' , 'Data/MC'),
    ('Data-MC' , 'Data-MC'),
    ('Diff/unc' , 'Diff/unc')
    #('ZbinSig' , 'ZbinSig')
    ])
table_cols = collections.OrderedDict([
    ('No Selection', 'Triggers Only'),
    ('BaseSel', 'Base'),
    ('SymSel', 'Symmetric'),
    ('OpSel BaseSel', 'Optimal'),
    ('SRwJets', 'SR w/ Jets'),
    ('SRnoJets', 'SR w/o Jets')
    ])

def col_finder(i): return 1+2*i

with open(args.file_name, 'r') as f:
    for count, line in enumerate(f.readlines()):
        row = [x.strip() for x in line.strip().split('\t')]
        if count == 0:
            for i in range(n_col):
                col = col_finder(i)
                sample = row[col]
                tbl_dict[sample] = collections.defaultdict(lambda: (0,0))
                col_to_sample[col] = sample
            tbl_dict['MC total'] = collections.defaultdict(lambda: (0,0))
            tbl_dict['Data/MC'] = {} 
            tbl_dict['Data-MC'] = {} 
            tbl_dict['Diff/unc'] = {}
            #tbl_dict['ZbinSig'] = {}
        else:
            selection = row[0]
            for i in range(n_col):
                col = col_finder(i)
                sample = col_to_sample[col]
                yld = float(row[col])
                unc = float(row[col+1])
                tbl_dict[sample][selection] = yld, unc 
                if sample not in {data_name, sig_name}:
                    zip_tuple = zip(tbl_dict['MC total'][selection],(yld, unc))
                    sum_tuple = tuple(x+y for x,y in zip_tuple)
                    tbl_dict['MC total'][selection] = sum_tuple 
	        data = tbl_dict[data_name][selection]
	        signal = tbl_dict[sig_name][selection]
	        MC = tbl_dict['MC total'][selection]
            tbl_dict['Data/MC'][selection] = data[0]/MC[0]
            yld, unc = data[0] - MC[0], data[1] + MC[1]
            tbl_dict['Data-MC'][selection] = yld, unc 
            tbl_dict['Diff/unc'][selection] = yld/unc
            #tbl_dict['ZbinSig'][selection] = BinZ(signal[0],yld,unc/yld) 
latex_tbl = []
tbl_headers = [x for key, x in table_cols.items()]

for row, sample in table_rows.items():
    tmp_row = [sample]
    for col in table_cols:
        ii = tbl_dict[row][col]
        if type(ii) is tuple:
            entry = "%.1f +/- %.1f"%(ii[0],ii[1])
        elif type(ii) is str:
            entry = ii
        elif row == 'Data/MC':
            entry = '%.1f%%'%(ii*100)
        else: 
            entry = '%.2f'%ii
        tmp_row.append(entry)
    latex_tbl.append(tmp_row)

print tabulate.tabulate(latex_tbl, headers = tbl_headers)
tmp_file = '%stmp_%s'%(g.analysis_run_dir,args.ofile) 
with open(tmp_file,'w') as ofile:
    ofile.write(tabulate.tabulate(latex_tbl, headers = tbl_headers, tablefmt='latex'))
    ofile.close()
tmp_file = open(tmp_file,'r')
ofile_path = '%s%s'%(g.analysis_run_dir,args.ofile) 
with open(ofile_path,'w') as ofile:
    ofile.write('\\documentclass{article}\n')
    ofile.write('\\usepackage{geometry}\n')
    ofile.write('\\geometry{landscape}\n')
    ofile.write('\\begin{document}\n')
    ofile.write('\\begin{table}[]\n')
    ofile.write('\\small\n')
    ofile.write('\\centering\n')
    for line in tmp_file.readlines():
        first_word = line.split()[0].strip()
        if first_word == '\\hline': continue
        elif first_word == '&':
            ofile.write('%s \\hline \\hline\n'%line.strip())
        elif first_word in ['Zll', 'MC', 'Diff/unc']:
            ofile.write('%s \\hline\n'%line.strip())
        else:
            ofile.write('%s\n'%line.strip())
    ofile.write('\\end{table}\n')
    ofile.write('\\end{document}\n')
    ofile.close()
    print 'Created ', ofile_path

  
