#!/bin/bash/env python
from collections import OrderedDict, namedtuple, defaultdict
import ROOT


tag = "n0235"
analysis_dir = "/data/uclhc/uci/user/armstro1/SusyNt/analysis_%s/"%tag
analysis_run_dir = "/data/uclhc/uci/user/armstro1/SusyNt/analysis_%s_run/"%tag
input_files = analysis_dir+'inputs_LFV/'
output_dir = analysis_run_dir+'outputs/'
dsid_dir = analysis_run_dir+'dsid_filelist/'

S2L_trigger = '(((pass_HLT_2e12_lhloose_L12EM10VH||pass_HLT_e17_lhloose_mu14||pass_HLT_mu18_mu8noL1)&&treatAsYear==2015)||((pass_HLT_2e17_lhvloose_nod0||pass_HLT_e17_lhloose_nod0_mu14||pass_HLT_mu22_mu8noL1)&&treatAsYear==2016))'
S2L_ptCuts  = 'l_pt[0]>25.&&l_pt[1]>20.&&MLL>40.'
S2L_isOS    = '(l_q[0]*l_q[1])<0'
S2L_jetVeto = 'nCentralBJets==0 && nForwardJets==0 && nCentralLJets==0'
DF_OS = 'dilep_flav <= 1 && l_q[0]*l_q[1]<0'
SF_OS = 'dilep_flav > 1 && l_q[0]*l_q[1]<0'
lep_eta_cut = 'fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4'

# Same flavor lepton triggers
ee15_trig   = 'pass_HLT_2e12_lhloose_L12EM10VH'
mumu15_trig = 'pass_HLT_mu18_mu8noL1'
ee16_trig   = 'pass_HLT_2e17_lhvloose_nod0'
mumu16_trig = 'pass_HLT_mu22_mu8noL1'
# Different flavor lepton triggs
emu15_trig  = 'pass_HLT_e17_lhloose_mu14'
emu16_trig  = 'pass_HLT_e17_lhloose_nod0_mu14'
# Single lepton triggers
e15_trig    = '(pass_HLT_e24_lhmedium_L1EM20VH || pass_HLT_e60_lhmedium || pass_HLT_e120_lhloose)'
mu15_trig   = '(pass_HLT_mu20_iloose_L1MU15 || pass_HLT_mu50)'
e16_trig    = '(pass_HLT_e26_lhtight_nod0_ivarloose || pass_HLT_e60_lhmedium_nod0 || pass_HLT_e140_lhloose_nod0)'
mu16_trig   = '(pass_HLT_mu26_ivarmedium || pass_HLT_mu50)'
# Triggers with added pT requirements
e15_trig_emu_pT   = '(%s && dilep_flav == 0 && l_pt[0] >= 25)'%e15_trig
mu15_trig_emu_pT  = '(%s && dilep_flav == 0 && l_pt[0] < 25 && l_pt[1] >= 21)'%mu15_trig
e16_trig_emu_pT   = '(%s && dilep_flav == 0 && l_pt[0] >= 27)'%e16_trig
mu16_trig_emu_pT  = '(%s && dilep_flav == 0 && l_pt[0] < 27 && l_pt[1] >= 28)'%mu16_trig
emu15_trig_emu_pT = '(%s && dilep_flav == 0 && 18 <= l_pt[0] && l_pt[0] < 25 && 15 <= l_pt[1] && l_pt[1] < 21)'%emu15_trig
emu16_trig_emu_pT = '(%s && dilep_flav == 0 && 18 <= l_pt[0] && l_pt[0] < 27 && 15 <= l_pt[1] && l_pt[1] < 28)'%emu16_trig
e15_trig_mue_pT   = '(%s && dilep_flav == 1 && l_pt[1] >= 25)'%e15_trig
mu15_trig_mue_pT  = '(%s && dilep_flav == 1 && l_pt[1] < 25 && l_pt[0] >= 21)'%mu15_trig
e16_trig_mue_pT   = '(%s && dilep_flav == 1 && l_pt[1] >= 27)'%e16_trig
mu16_trig_mue_pT  = '(%s && dilep_flav == 1 && l_pt[1] < 27 && l_pt[0] >= 28)'%mu16_trig
emu15_trig_mue_pT = '(%s && dilep_flav == 1 && 18 <= l_pt[1] && l_pt[1] < 25 && 15 <= l_pt[0] && l_pt[0] < 21)'%emu15_trig
emu16_trig_mue_pT = '(%s && dilep_flav == 1 && 18 <= l_pt[1] && l_pt[1] < 27 && 15 <= l_pt[0] && l_pt[0] < 28)'%emu16_trig
# Combined triggers
e15_trig_pT = '(%s || %s)'%(e15_trig_emu_pT, e15_trig_mue_pT)
mu15_trig_pT = '(%s || %s)'%(mu15_trig_emu_pT, mu15_trig_mue_pT)
e16_trig_pT = '(%s || %s)'%(e16_trig_emu_pT, e16_trig_mue_pT)
mu16_trig_pT = '(%s || %s)'%(mu16_trig_emu_pT, mu16_trig_mue_pT)
emu15_trig_pT = '(%s || %s)'%(emu15_trig_emu_pT, emu15_trig_mue_pT)
emu16_trig_pT = '(%s || %s)'%(emu16_trig_emu_pT, emu16_trig_mue_pT)

dilep15_trig      = '(treatAsYear==2015 && %s)'%emu15_trig_pT
dilep16_trig     = '(treatAsYear==2016 && %s)'%emu16_trig_pT
singlelep15_trig = '(treatAsYear==2015 && (%s || %s))'%(e15_trig_pT,mu15_trig_pT)
singlelep16_trig = '(treatAsYear==2016 && (%s || %s))'%(e16_trig_pT,mu16_trig_pT)

Sel = {
    ''             : '1',
    'dilep_trig': '(%s || %s)'%(dilep15_trig, dilep16_trig),
    'singlelep_trig': '(%s || %s)'%(singlelep15_trig,singlelep16_trig),
    'Baseline'  : 'l_pt[0] >= 45 && l_pt[1] >= 15 '
                   + '&& 30 < MLL && MLL < 150 '
                   + '&& nCentralBJets==0 '
                   + '&& (dilep_flav != 0 || (el0_track_pt/el0_clus_pt) < 1.2) ',
    'emu'       : 'dilep_flav == 0',
    'mue'       : 'dilep_flav == 1',
    'ee'        : 'dilep_flav == 2',
    'mumu'      : 'dilep_flav == 3',
    }
Sel['VBF_raw'] = "JetN_g30 >= 2 && j_pt[0] > 40 && Mjj > 400 && DEtaJJ > 3"
Sel['VBF'] = "(%s) && (%s)"%(Sel['Baseline'],Sel['VBF_raw'])
Sel['Optimized'] = "(%s) && !(%s) && DphiLep1MET < 1 && MtLep0 > 50 && MtLep1 < 40 && ((MET+l_pt[1])/l_pt[1]) > 0.5"%(Sel['Baseline'],Sel['VBF_raw'])
trigger_sel_name = 'singlelep_trig'
trigger_selection = Sel[trigger_sel_name]

# Define the luminosity you want
luminosity = "36180" # ipb
#luminosity = "3209" # ipb for data15
#luminosity = "32971" # ipb for data16

# Signal Branching Ratio
BR = '0.01'

histMaxY = {}

HistOp1D = namedtuple('HistOp1D', 'nBinsX, x0, x1, xUnits, xLabel, yLabel')
HistOp1D.__new__.__defaults__= (25,0,-1,'','','Events')

HistOpMap = {
    'RunNumber'       : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Event run number',                  yLabel='Events'),
    'event_number'    : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Event number',                      yLabel='Events'),
    'isMC'            : HistOp1D(nBinsX=5,  x0=-1.5, x1=3.5,   xUnits='',    xLabel='is Monte Carlo',                    yLabel='Events'),
    'eventweight'     : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Event weight',                      yLabel='Events'),
    'dsid'            : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Sample DSID',                       yLabel='Events'),
    'treatAsYear'     : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='treatAsYear',                       yLabel='Events'),
    'nBaseLeptons'    : HistOp1D(nBinsX=11, x0=-0.5, x1=10.5,  xUnits='',    xLabel='N_{baseline leptons}',              yLabel='Events'),
    'nSignalLeptons'  : HistOp1D(nBinsX=11, x0=-0.5, x1=10.5,  xUnits='',    xLabel='N_{signal leptons}',                yLabel='Events'),
    'nBaseTaus'       : HistOp1D(nBinsX=11, x0=-0.5, x1=10.5,  xUnits='',    xLabel='N_{baseline taus}',                 yLabel='Events'),
    'nSignalTaus'     : HistOp1D(nBinsX=11, x0=-0.5, x1=10.5,  xUnits='',    xLabel='N_{signal taus}',                   yLabel='Events'),
    'l_pt'            : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='Lepton p_{T}',                      yLabel='Events'),
    'el0_track_pt'    : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='Leading electron track p_{T}',      yLabel='Events'),
    'el0_clus_pt'     : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='Leading electron cluster p_{T}',    yLabel='Events'),
    'l_eta'           : HistOp1D(nBinsX=20, x0=-3.0, x1=3.0,   xUnits='',    xLabel='Lepton #eta',                       yLabel='Events'),
    'l_phi'           : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='Lepton #phi',                       yLabel='Events'),
    'l_flav'          : HistOp1D(nBinsX=5,  x0=-0.5, x1=4.5,   xUnits='',    xLabel='Lepton flavor (0: e, 1: m)',        yLabel='Events'),
    'l_type'          : HistOp1D(nBinsX=5,  x0=-0.5, x1=4.5,   xUnits='',    xLabel='Lepton type',                       yLabel='Events'),
    'l_origin'        : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Lepton origin',                     yLabel='Events'),
    'l_q'             : HistOp1D(nBinsX=3,  x0=-1.5, x1=1.5,   xUnits='',    xLabel='Lepton charge',                     yLabel='Events'),
    'LepLepSign'      : HistOp1D(nBinsX=3,  x0=-1.5, x1=1.5,   xUnits='',    xLabel='Leptons sign product',              yLabel='Events'),
    'MET'             : HistOp1D(nBinsX=20, x0=0.0,  x1=200.0, xUnits='GeV', xLabel='E_{T}^{miss}',                      yLabel='Events'),
    'METPhi'          : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='MET_{#phi}',                        yLabel='Events'),
    'Lep0Pt'          : HistOp1D(nBinsX=20, x0=0.0,  x1=200.0, xUnits='GeV', xLabel='p_{T}^{leading lep}',               yLabel='Events'),
    'Lep1Pt'          : HistOp1D(nBinsX=20, x0=0.0,  x1=100.0, xUnits='GeV', xLabel='p_{T}^{subleading lep}',            yLabel='Events'),
    'Lep0Eta'         : HistOp1D(nBinsX=20, x0=-3.0, x1=3.0,   xUnits='',    xLabel='#eta^{leading lep}',                yLabel='Events'),
    'Lep1Eta'         : HistOp1D(nBinsX=20, x0=-3.0, x1=3.0,   xUnits='',    xLabel='#eta^{subleading lep}',             yLabel='Events'),
    'Lep0Phi'         : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='#phi^{leading lep}',                yLabel='Events'),
    'Lep1Phi'         : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='#phi^{subleading lep}',             yLabel='Events'),
    'MLep0'           : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='M_{l0}',                            yLabel='Events'),
    'MLep1'           : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='M_{l1}',                            yLabel='Events'),
    'DEtaLL'          : HistOp1D(nBinsX=20, x0=0.0,  x1=6.0,   xUnits='',    xLabel='#Delta#eta_{ll}',                   yLabel='Events'),
    'DphiLL'          : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='#Delta#phi_{ll}',                   yLabel='Events'),
    'drll'            : HistOp1D(nBinsX=20, x0=0.0,  x1=6.0,   xUnits='',    xLabel='#DeltaR_{ll}',                      yLabel='Events'),
    'dilep_flav'      : HistOp1D(nBinsX=5,  x0=-0.5, x1=4.5,   xUnits='',    xLabel='Dilepton flavor',                   yLabel='Events'),
    'isEM'            : HistOp1D(nBinsX=5,  x0=-1.5, x1=3.5,   xUnits='',    xLabel='Dilepton flavor is el mu',          yLabel='Events'),
    'isME'            : HistOp1D(nBinsX=5,  x0=-1.5, x1=3.5,   xUnits='',    xLabel='Dilepton flavor is mu el',          yLabel='Events'),
    'MCollASym'       : HistOp1D(nBinsX=25, x0=0.0,  x1=250.0, xUnits='GeV', xLabel='LFV Collinear Mass m_{coll}',       yLabel='Events'),
    'MtLep0'          : HistOp1D(nBinsX=15, x0=0.0,  x1=250.0, xUnits='GeV', xLabel='m_{T}(l_{0},MET)',                  yLabel='Events'),
    'MtLep1'          : HistOp1D(nBinsX=20, x0=0.0,  x1=140.0, xUnits='GeV', xLabel='m_{T}(l_{1},MET)',                  yLabel='Events'),
    'MLL'             : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='M_{ll}',                            yLabel='Events'),
    'ptll'            : HistOp1D(nBinsX=20, x0=0.0,  x1=200.0, xUnits='GeV', xLabel='pT_{ll}',                           yLabel='Events'),
    'dpt_ll'          : HistOp1D(nBinsX=20, x0=0.0,  x1=150.0, xUnits='GeV', xLabel='#Deltap_{T}^{ll}',                  yLabel='Events'),
    'DphiLep0MET'     : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='#Delta#phi(l_{0},MET)',             yLabel='Events'),
    'DphiLep1MET'     : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='#Delta#phi(l_{1},MET)',             yLabel='Events'),
    'JetN'            : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{base jet}',                      yLabel='Events'),
    'Jet_N2p4Eta25Pt' : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{jet} (p_{T}>25GeV, |#eta|<2.5)', yLabel='Events'),
    'SignalJetN'      : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{sig jets}',                      yLabel='Events'),
    'JetN_g30'        : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{jet} (p_{T}>30GeV)',             yLabel='Events'),
    'nCentralLJets'   : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{CL jet}',                        yLabel='Events'),
    'nCentralBJets'   : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{CB jet}',                        yLabel='Events'),
    'Btag'            : HistOp1D(nBinsX=5,  x0=-1.5, x1=3.5,   xUnits='',    xLabel='B-tagged jet',                      yLabel='Events'),
    'nForwardJets'    : HistOp1D(nBinsX=8,  x0=-0.5, x1=7.5,   xUnits='',    xLabel='N_{F jet}',                         yLabel='Events'),
    'j_pt[0]'         : HistOp1D(nBinsX=20, x0=0.0,  x1=500.0, xUnits='GeV', xLabel='p_{T}^{leading jet}',               yLabel='Events'),
    'j_pt'            : HistOp1D(nBinsX=20, x0=0.0,  x1=500.0, xUnits='GeV', xLabel='Jet p_{T}',                         yLabel='Events'),
    'Mjj'             : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='GeV', xLabel='Dijet mass',                        yLabel='Events'),
    'DEtaJJ'          : HistOp1D(nBinsX=20, x0=0.0,  x1=6.0,   xUnits='',    xLabel='#Delta#eta(j0,j1)',                 yLabel='Events'),
    'j_eta'           : HistOp1D(nBinsX=20, x0=-3.0, x1=3.0,   xUnits='',    xLabel='Jet #eta',                          yLabel='Events'),
    'j_jvt'           : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Jet JVT',                           yLabel='Events'),
    'j_jvf'           : HistOp1D(nBinsX=25, x0=0.0,  x1=-1,    xUnits='',    xLabel='Jet JVF',                           yLabel='Events'),
    'j_phi'           : HistOp1D(nBinsX=30, x0=0.0,  x1=3.15,  xUnits='',    xLabel='Jet #phi',                          yLabel='Events'),
    'j_flav'          : HistOp1D(nBinsX=5,  x0=-0.5, x1=4.5,   xUnits='',    xLabel='Jet flavor (0:NA,1:CL,2:CB,3:F)',   yLabel='Events'),
    'pass_HLT_mu18_mu8noL1'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu18 mu8noL1 trigger bit',                 yLabel='Events'),
    'pass_HLT_2e12_lhloose_L12EM10VH'       : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='2e12 lhloose L12EM10VH trigger bit',       yLabel='Events'),
    'pass_HLT_e17_lhloose_mu14'             : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e17 lhloose mu14 trigger bit',             yLabel='Events'),
    'pass_HLT_mu20_mu8noL1'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu20 mu8noL1 trigger bit',                 yLabel='Events'),
    'pass_HLT_2e15_lhvloose_L12EM13VH'      : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='2e15 lhvloose L12EM13VH trigger bit',      yLabel='Events'),
    'pass_HLT_2e17_lhvloose_nod0'           : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='2e17 lhvloose nod0 trigger bit',           yLabel='Events'),
    'pass_HLT_mu22_mu8noL1'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu22 mu8noL1 trigger bit',                 yLabel='Events'),
    'pass_HLT_e17_lhloose_nod0_mu14'        : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e17 lhloose nod0 mu14 trigger bit',        yLabel='Events'),
    'pass_HLT_e60_lhmedium'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e60 lhmedium trigger bit',                 yLabel='Events'),
    'pass_HLT_e24_lhmedium_L1EM20VH'        : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e24 lhmedium L1EM20VH trigger bit',        yLabel='Events'),
    'pass_HLT_e24_lhmedium_iloose_L1EM18VH' : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e24 lhmedium iloose L1EM18VH trigger bit', yLabel='Events'),
    'pass_HLT_mu20_iloose_L1MU15'           : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu20 iloose L1MU15 trigger bit',           yLabel='Events'),
    'pass_HLT_mu24_imedium'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 imedium trigger bit',                 yLabel='Events'),
    'pass_HLT_mu26_imedium'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu26 imedium trigger bit',                 yLabel='Events'),
    'pass_HLT_e24_lhtight_nod0_ivarloose'   : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e24 lhtight nod0 ivarloose trigger bit',   yLabel='Events'),
    'pass_HLT_e26_lhtight_nod0_ivarloose'   : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e26 lhtight nod0 ivarloose trigger bit',   yLabel='Events'),
    'pass_HLT_e60_lhmedium_nod0'            : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e60 lhmedium nod0 trigger bit',            yLabel='Events'),
    'pass_HLT_e120_lhloose'                 : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e120 lhloose trigger bit',                 yLabel='Events'),
    'pass_HLT_e140_lhloose_nod0'            : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='e140 lhloose nod0 trigger bit',            yLabel='Events'),
    'pass_HLT_mu24_iloose'                  : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 iloose trigger bit',                  yLabel='Events'),
    'pass_HLT_mu24_iloose_L1MU15'           : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 iloose L1MU15 trigger bit',           yLabel='Events'),
    'pass_HLT_mu24_ivarloose'               : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 ivarloose trigger bit',               yLabel='Events'),
    'pass_HLT_mu24_ivarloose_L1MU15'        : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 ivarloose L1MU15 trigger bit',        yLabel='Events'),
    'pass_HLT_mu24_ivarmedium'              : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu24 ivarmedium trigger bit',              yLabel='Events'),
    'pass_HLT_mu26_ivarmedium'              : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu26 ivarmedium trigger bit',              yLabel='Events'),
    'pass_HLT_mu50'                         : HistOp1D(nBinsX=5, x0=-1.5, x1=3.5, xUnits='', xLabel='mu50 trigger bit',                         yLabel='Events')
}


# Set ATLAS style
def setATLASStyle(path="/data/uclhc/uci/user/armstro1/ATLASStyle/"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle()

# Dummy ratio histogram
def dummifyHistogram(histo):
    ratio_histo = histo.Clone();
    ratio_histo.Reset();
    ratio_histo.SetMarkerSize(1.2);
    ratio_histo.SetMarkerStyle(20);
    ratio_histo.SetLineWidth(2);
    ratio_histo.GetYaxis().SetTitle("#frac{Data}{SM}");
    ratio_histo.GetXaxis().SetLabelSize(0.1);
    ratio_histo.GetXaxis().SetLabelOffset(0.02);
    ratio_histo.GetXaxis().SetTitleSize(0.12);
    ratio_histo.GetXaxis().SetTitleOffset(1.);
    ratio_histo.GetYaxis().SetRangeUser(0.001,2);
    ratio_histo.GetYaxis().SetLabelSize(0.1);
    ratio_histo.GetYaxis().SetTitleSize(0.12);
    ratio_histo.GetYaxis().SetTitleOffset(0.5);
    ratio_histo.GetYaxis().SetNdivisions(5);
    return ratio_histo
