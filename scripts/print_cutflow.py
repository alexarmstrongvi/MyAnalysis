#!/bin/bash/env python
""" Prints cutflow for input root file
    using hard-coded selections 
    """
import ROOT
import global_variables as G
from argparse import ArgumentParser
from make_stack_plot import Sel 
from collections import OrderedDict

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 3001;")

def main():
    # User Inputs
    parser = ArgumentParser(description='Get input root file')
    parser.add_argument('ifile', default='', help='Input root file')
    args = parser.parse_args()
    
    print args.ifile
    # Get File and Tree
    ifile = ROOT.TFile(args.ifile,"READ")
    itree = ifile.Get('superNt')
    
    # Dummy Histogram
    hist = ROOT.TH1F("tmp_hist","tmp_hist",2,-0.5,1.5)
    draw_hist = "isMC >> tmp_hist"
    
    # Selection List
    selection_dict = OrderedDict([
        ('trigger', Sel['singlelep_trig']),
        ('opp-sign', 'l_q[0]*l_q[1]<0'),
        ('mll >= 20', 'mll >= 20'),
        ('opp-flav', 'dilep_flav <= 1'),
        ('pt0 >= 35', 'l_pt[0] >= 35'),
        ('pt1 >= 15', 'l_pt[1] >= 15' ),
        ('jet-veto', 'nCentralLJets==0 && nCentralBJets==0'),
        ('dphi-l0l1', 'dphi_ll>=2.3'),
        ('dphi-l1met', 'dphi_l1_met<=0.7')
    ])

    # Cutflow 
    cutflow = OrderedDict()
    selection = '1'
    print "Running with no selection"
    cutflow['None'] = itree.Draw(draw_hist,selection,'goff')
    #cutflow["None"] = hist.Integral(0,-1)
    
    for key, sel in selection_dict.items():
        selection += ' && ' + sel
        cutflow[key] = itree.Draw(draw_hist,selection, 'goff')
        print "%15s\t%d"%(key,cutflow[key])
        #print "%15s\t%d"%(key,hist.Integral(0,-1))
        #cutflow[key] = hist.Integral(0,-1)

    print cutflow
    
if __name__ == '__main__':
    main()

