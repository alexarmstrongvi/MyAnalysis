#!/bin/bash/env python

import ROOT
import global_variables as G
from make_stack_plot import Sel, luminosity
import collections
#import tabulate

inputFile = ROOT.TFile(G.analysis_run_dir+'LFV.root','READ')
backgrounds = ['data_all', 'HWW', 'Wjets', 'Diboson',
           'Top', 'Ztt_ZttEW', 'Zll_ZEW']
#ttree = inputFile.Get('data_all')
trigger = collections.OrderedDict([
    ('Selected Events' , '1'),
    ('only SingleLep' , '(%s && !(%s))'%(Sel['singlelep_trig'],Sel['dilep_trig'])),
    ('only Dilep' , '(!(%s) && %s)'%(Sel['singlelep_trig'],Sel['dilep_trig'])),
    ('both' , '(%s && %s)'%(Sel['singlelep_trig'],Sel['dilep_trig'])),
    ('neither' , '!(%s || %s)'%(Sel['singlelep_trig'],Sel['dilep_trig']))
    ])
total_events = None
init_list = [0]*(len(trigger))
nEvents = [[[0, 0.0] for j in range(len(trigger))] for k in range (2)]
#hist = ROOT.TH1D('hist','hist',100,0,4)
for sample in backgrounds:
    print 'Looping over ', sample
    ttree = inputFile.Get(sample)
    if sample == 'data_all': idx = 0
    else: idx = 1
    for counter, (trig_name, sel) in enumerate(trigger.items()):
        sel = '%s && %s'%(sel,Sel['base_LFV'])
        nEvents[idx][counter][0] += int(ttree.Draw('1 >> ',sel,'goff'))
        total_events = nEvents[idx][0][0]
        n_events = nEvents[idx][counter][0]
        perc = n_events/float(total_events)*100.0
        nEvents[idx][counter][1] = '%.2f%%'%perc
        print "\t%15s: %d/%d = %.2f%%"%(trig_name,n_events,total_events,perc)
    print "done"
#print tabulate.tabulate(nEvents)
print nEvents

