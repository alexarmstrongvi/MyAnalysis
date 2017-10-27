#!/bin/env python
""" Loop over events in input root file to print out specific event info"""

################################################################################
# Created by Alex Armstrong
# Oct 26, 2017
# (C) University of California, Irvine
################################################################################

import sys
import argparse
import ROOT

#selection = '1'

trigger_list = ['HLT_mu18_mu8noL1',
                'HLT_2e12_lhloose_L12EM10VH',
                'HLT_e17_lhloose_mu14',
                'HLT_mu20_mu8noL1',
                'HLT_2e15_lhvloose_L12EM13VH',
                'HLT_2e17_lhvloose_nod0',
                'HLT_mu22_mu8noL1',
                'HLT_e17_lhloose_nod0_mu14']

def print_lepton(event):
    """ Print relevent lepton info for an event"""
    print_str = 'Run %d, event %d lepton info: \n'%(event.runNumber,
                                                         event.eventNumber)
    for iii in [0,1]:
        if iii == 0: print_str += '\tLeading    : '
        elif iii == 1: print_str += '\tSubleading : '
        if event.l_flav[iii] == 0: print_str += 'el'
        elif event.l_flav[iii] == 1: print_str += 'mu'
        if event.l_q[iii] == 1: print_str += '+' 
        elif event.l_q[iii] == -1: print_str += '-' 
        print_str += ' '
        print_str += '(pT, eta, phi) = (%.2fGeV, %.2f, %.2f), '%(event.l_pt[iii], 
                                                                 event.l_eta[iii], 
                                                                 event.l_phi[iii])
        print_str += '\n'

    print_str += '\tM_ll = %.2f, '%event.mll
    print_str += 'dR(l0,l1) = %.2f, '%event.drll
    print_str += 'dphi(l0,MET) = %.2f, '%event.dphi_l0_met
    print_str += 'dphi(l1,MET) = %.2f\n'%event.dphi_l1_met

    print_str += '\tDilepton triggers      : '
    if event.pass_HLT_mu18_mu8noL1:
        print_str += 'HLT_mu18_mu8noL1, '
    if event.pass_HLT_2e12_lhloose_L12EM10VH:
        print_str += 'HLT_2e12_lhloose_L12EM10VH, '
    if event.pass_HLT_e17_lhloose_mu14:
        print_str += 'HLT_e17_lhloose_mu14, '
    if event.pass_HLT_mu20_mu8noL1:
        print_str += 'HLT_mu20_mu8noL1, '
    if event.pass_HLT_2e15_lhvloose_L12EM13VH:
        print_str += 'HLT_2e15_lhvloose_L12EM13VH, '
    if event.pass_HLT_2e17_lhvloose_nod0:
        print_str += 'HLT_2e17_lhvloose_nod0, '
    if event.pass_HLT_mu22_mu8noL1:
        print_str += 'HLT_mu22_mu8noL1, '
    if event.pass_HLT_e17_lhloose_nod0_mu14:
        print_str += 'HLT_e17_lhloose_nod0_mu14, '
    print_str = print_str[:-2]
    print_str += '\n'
    
    print_str += '\tSingle lepton triggers : '
    if event.pass_HLT_e60_lhmedium:
        print_str += 'HLT_e60_lhmedium, '
    if event.pass_HLT_e24_lhmedium_L1EM20VH:
        print_str += 'HLT_e24_lhmedium_L1EM20VH, '
    if event.pass_HLT_mu20_iloose_L1MU15:
        print_str += 'HLT_mu20_iloose_L1MU15, '
    if event.pass_HLT_mu26_ivarmedium:
        print_str += 'HLT_mu26_ivarmedium, '
    if event.pass_HLT_mu50:
        print_str += 'HLT_mu50, '
    if event.pass_HLT_e24_lhtight_nod0_ivarloose:
        print_str += 'HLT_e24_lhtight_nod0_ivarloose, '
    if event.pass_HLT_e26_lhtight_nod0_ivarloose:
        print_str += 'HLT_e26_lhtight_nod0_ivarloose, '
    if event.pass_HLT_e60_lhmedium_nod0:
        print_str += 'HLT_e60_lhmedium_nod0, '
    print_str = print_str[:-2]
    print_str += '\n'

    return print_str

def main():
    """ Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input .root file', required=True)
    parser.add_argument('-t', '--tree', help='ttree name', required=True)
    args = parser.parse_args()
    file_name = args.file
    tree_name = args.tree

    ofile_name = '%s_%s.txt'%(file_name.split('/')[-1][:-5], tree_name)
    ofile = open(ofile_name, 'w')
    ifile = ROOT.TFile(file_name,'READ')
    tree = ifile.Get(tree_name)
    for iii, event in enumerate(tree):
        #  TODO: skip if event doesn't pass selection
        ofile.write(print_lepton(event))
        if iii > 10:
            ofile.close()
            sys.exit()
    ofile.close()

if __name__ == '__main__':
    # Only execute when this module is run
    main()
