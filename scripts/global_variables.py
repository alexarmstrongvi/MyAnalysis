#!/bin/bash/env python
from collections import OrderedDict
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
    ''          : '1',
    'dilep_trig': '(%s || %s)'%(dilep15_trig, dilep16_trig),
    'singlelep_trig': '(%s || %s)'%(singlelep15_trig,singlelep16_trig),
    'Baseline'  : 'l_pt[0] >= 45 && l_pt[1] >= 15' 
                   + '&& 30 < MLL && MLL < 150' 
                   + '&& nCentralBJets==0'
                   + '&& (dilep_flav != 0 || el0_track_pt/el0_clus_pt < 1.2)'
                   + '&& ' + DF_OS,
    'VBF'       : 'JetN_g30 >= 2'
                  + '&& j_pt[0] > 40'
                  + '&& Mjj > 400'
                  + '&& DEtaJJ > 3',
    'BaseSel'   : 'l_pt[0] >= 45 && l_pt[1] >= 15'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS,
    'SymSel'    : 'l_pt[0] >= 20 && l_pt[1] >= 20'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS,
    'OpSel'     : 'l_pt[0] >= 45 && l_pt[1] >= 15'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'DphiLep0MET>=2.5 && DphiLep1MET<=0.7 && DphiLL>=2.3 && dpt_ll>=7.0',
    'SRwJets'   : 'l_pt[0] >= 35 && l_pt[1] >= 15'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'DphiLep0MET>=1.0 && DphiLep1MET<=0.5 && DphiLL>=1.0 && dpt_ll>=1.0'
                  + ' && ' + 'nCentralLJets>=1 && nCentralBJets==0 && nSignalTaus == 0',
    'SRnoJets'  : 'l_pt[0] >= 35 && l_pt[1] >= 15 && '
                  + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'DphiLep0MET>=2.5 && DphiLep1MET<=0.7 && DphiLL>=2.3 && dpt_ll>=7.0'
                  + ' && ' + 'nCentralLJets==0 && nCentralBJets==0 && nSignalTaus == 0',
    'emu'       : 'dilep_flav == 0',
    'mue'       : 'dilep_flav == 1',
    'ee'        : 'dilep_flav == 2',
    'mumu'      : 'dilep_flav == 3',
    'base_LFV'      : DF_OS,
    # Special Cuts for Testing
    'SRwJnoJReq'   : 'l_pt[0] >= 35 && l_pt[1] >= 12'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'DphiLep0MET>=1.0 && DphiLep1MET<=0.5 && DphiLL>=1.0 && dpt_ll>=1.0',
    'SRnJnoJReq'  : 'l_pt[0] >= 35 && l_pt[1] >= 12 && '
                  + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'DphiLep0MET>=2.5 && DphiLep1MET<=0.7 && DphiLL>=2.3 && dpt_ll>=7.0',
    'base_LFV_run1'      : 'MLL>=20 && l_q[0]*l_q[1]<0\
                    &&((l_pt[0] >= 12 && l_pt[1] >= 8) && (dilep_flav<=1))',
    'jets_Best' : 'nForwardJets==nForwardJets_ge40',
    }
Sel['Optimized'] = "!(%s) && DphiLep1MET <= 1 && l_pt[0] > 50 && l_pt[1] < 40 && (MET+l_pt[1])/l_pt[1] > 0.5"%Sel['VBF'] 
trigger_sel_name = 'singlelep_trig'
trigger_selection = Sel[trigger_sel_name]

# Define the luminosity you want
luminosity = "36180" # ipb
#luminosity = "3209" # ipb for data15
#luminosity = "32971" # ipb for data16

# Signal Branching Ratio
BR = '0.01'

histMaxBin = OrderedDict([ # default is 500
    ('nBaseJets',          40),
    ('nCentralLJets',      7),
    ('nCentralBJets',      10),
    ('nForwardJets',       15),
    ('j_pt[0]',             500),
    ('j_pt[1]',             500),
    ('j_pt[2]',             500),
    ('j_pt[3]',             500),
    ('j_pt[0]_Best',       500),
    ('j_pt[1]_Best',       500),
    ('j_pt[2]_Best',       500),
    ('j_pt[3]_Best',       500),
    ('j_jvt',               1.2),
    ('j_jvf',               1.2),
    ('j_flav',              8),
    ('j_flav_Jge20',        8),
    ('j_flav_Jge30',        8),
    ('j_flav_Jge40',        8),
    ('j_flav_Jge50',        8),
    ('j_flav_Jge60',        8),
    ('l0_pt_emu',           500),
    ('l0_pt_mue',           500),
    ('l0_pt_ee',            500),
    ('l0_pt_mumu',          500),
    ('l1_pt_emu',           300),
    ('l1_pt_mue',           300.),
    ('l1_pt_ee',            300),
    ('l1_pt_mumu',          300),
    ('l_pt[0]',             500.),
    ('l_pt[1]',             800.),
    ('l_eta[0]',            3.),
    ('l_eta[1]',            3.),
    ('MCollASym',              300),
    ('m_coll_emu_SRnoJets', 400),
    ('m_coll_mue_SRnoJets', 400),
    ('m_coll_emu_SRJets',   400),
    ('m_coll_mue_SRJets',   400),
    ('SRJets',              400),
    ('SRnJets',             400),
    ('SRJets_noLJetreq',    400),
    ('SRJets_noBJetreq',    400),
    ('SRJets_noJetreq',     400),
    ('SRJets_noJetreqLepreq',     400),
    ('SRnJets_noLJetreq',    400),
    ('SRnJets_noBJetreq',    400),
    ('SRnJets_noJetreq',     400),
    ('SRnJets_noJetreqLepreq',     400),
    ('SRnJets_l0Met',     400),
    ('SRnJets_l1Met',     400),
    ('SRnJets_l0l1',     400),
    ('SRnJets_dPtll',     400),
    ('SRnJets_noJetl0Met',     400),
    ('SRnJets_noJetl1Met',     400),
    ('SRnJets_noJetl0l1',     400),
    ('SRnJets_noJetdPtll',     400),
    ('m_coll_emu_SymSel',   400),
    ('m_coll_mue_SymSel',   400),
    ('DphiLep0MET',         1.5*ROOT.TMath.Pi()),
    ('DphiLep1MET',         1.5*ROOT.TMath.Pi()),
    ('DphiLL',             1.5*ROOT.TMath.Pi()),
    ('DEtaLL',             1.5*ROOT.TMath.Pi()),
    ('dpt_ll',              800),
    ('MLL_ee',              500),
    ('MLL_mumu',            500),
    ('MLL_SF',              500),
    ('met',                 200),
    ('dilep_flav',          8),
    ('l_pt[0]'          ,200),
    ('l_pt[1]'          ,100),
    ('ptll'          ,200),
    ('drll'          ,6),
    ('DphiLL'          ,3.2),
    ('DEtaLL'          ,6)])
for pT in [20,30,40,50,60]:
    histMaxBin['SRJets_CLge%d'%pT] = 400
    histMaxBin['SRnJets_CLge%d'%pT] = 400
    for i in [0,1,2,3]:
       histMaxBin['j_pt[%d]_Jge%d'%(i,pT)] = 500


histMinBin = OrderedDict([ #default is zero
    ('j_jvt',       -0.2),
    ('j_jvf',       -0.2),
    ('l_eta[0]',    -3.),
    ('l_eta[1]',    -3.),
    ('l1_pt_ee',    0),
    ('DphiLep0MET', 0),
    ('DphiLep1MET', 0),
    ('DphiLL',     0),
    ('MCollASym',      50)])

histMaxY = { #default is 300 million
    'j_jvt'             :3*(10**12),
    'j_jvf'             :3*(10**12),
    'm_coll_emu_SRnoJets':800,
    'm_coll_mue_SRnoJets':800,
    'm_coll_emu_SRJets':600,
    'm_coll_mue_SRJets':600,
    'SRJets'         :1200,
    'SRJets_CLge20'  :1200,
    'SRJets_CLge30'  :1200,
    'SRJets_CLge40'  :1200,
    'SRJets_CLge50'  :1200,
    'SRJets_CLge60'  :1200,
    'SRnJets'         :2000,
    'SRnJets_CLge20'  :2000,
    'SRnJets_CLge30'  :2000,
    'SRnJets_CLge40'  :2000,
    'SRnJets_CLge50'  :2000,
    'SRnJets_CLge60'  :2000,
    'SRJets_noLJetreq'  :3500,
    'SRJets_noBJetreq'  :3500,
    'SRJets_noJetreq'   :3500,
    'SRJets_noJetreqLepreq':     3500,
    'SRnJets_noLJetreq'  :2500,
    'SRnJets_noBJetreq'  :2500,
    'SRnJets_noJetreq'   :2500,
    'SRnJets_noJetreqLepreq':     2500,
    'SRnJets_l0Met' :2500,
    'SRnJets_l1Met' :2500,
    'SRnJets_l0l1' :2500,
    'SRnJets_dPtll' :2500,
    'SRnJets_noJetl0Met' :3500,
    'SRnJets_noJetl1Met' :3500,
    'SRnJets_noJetl0l1' :3500,
    'SRnJets_noJetdPtll' :3500,
    'j_pt[0]'          :3*(10**8)
}

histBinNum = { #default is 25
    'nBaseJets'             :40,
    'nCentralLJets'         :7,
    'nCentralBJets'         :10,
    'nForwardJets'          :15,
    'j_pt[0]'               :25,
    'j_pt[1]'               :25,
    'j_pt[2]'               :25,
    'j_pt[3]'               :25,
    'j_jvt'                 :14,
    'j_jvf'                 :14,
    'j_flav'                :8,
    'j_flav_Jge20'          :8,
    'j_flav_Jge30'          :8,
    'j_flav_Jge40'          :8,
    'j_flav_Jge50'          :8,
    'j_flav_Jge60'          :8,
    'MLL_SF'                :25,
    'MLL_ee'                :25,
    'MLL_mumu'              :25,
    'dilep_flav'            :8,
    'DphiLep0MET'           :36,
    'DphiLep1MET'           :36,
    'DphiLL'               :36,
    'm_coll_emu_SRnoJets'   :40,
    'm_coll_mue_SRnoJets'   :40,
    'm_coll_emu_SRJets'     :40,
    'm_coll_mue_SRJets'     :40,
    'SRJets_noLJetreq'      :40,
    'SRJets'                :40,
    'SRnJets'               :40,
    'SRJets_noLJetreq'      :40,
    'SRJets_noBJetreq'      :40,
    'SRJets_noJetreq'       :40,
    'SRJets_noJetreqLepreq' :40,
    'SRnJets_noLJetreq'      :40,
    'SRnJets_noBJetreq'      :40,
    'SRnJets_noJetreq'       :40,
    'SRnJets_noJetreqLepreq' :40,
    'SRnJets_l0Met' :40,
    'SRnJets_l1Met' :40,
    'SRnJets_l0l1' :40,
    'SRnJets_dPtll' :40,
    'SRnJets_noJetl0Met' :40,
    'SRnJets_noJetl1Met' :40,
    'SRnJets_noJetl0l1' :40,
    'SRnJets_noJetdPtll' :40,
    'm_coll_emu_SymSel'     :40,
    'm_coll_mue_SymSel'     :40
}
for pT in [20,30,40,50,60]:
    histBinNum['SRJets_CLge%d'%pT] = 40
    histBinNum['SRnJets_CLge%d'%pT] = 40
    for i in [0,1,2,3]:
       histMaxBin['j_pt[%d]_Jge%d'%(i,pT)] = 40

selectionList = OrderedDict([ #default selection is True
    ('j_jvt','('+Sel['emu'] + '||' + Sel['mue']+')'),
    ('j_jvf','('+Sel['emu'] + '||' + Sel['mue']+')'),
    ('met_None','1.0'),
    ('met_Base',Sel['BaseSel']),
    ('met_Sym',Sel['SymSel']),
    ('met_Op',Sel['OpSel']),
    ('met_SRwJ',Sel['SRwJets']),
    ('met_SRnoJ',Sel['SRnoJets']),
    ('l0_pt_emu',Sel['emu']), #add selection on l1 for MCollASym
    ('l0_pt_mue',Sel['mue']),
    ('l0_pt_ee',Sel['ee']),
    ('l0_pt_mumu',Sel['mumu']),
    ('l1_pt_emu',Sel['emu']),
    ('l1_pt_mue',Sel['mue']),
    ('l1_pt_ee',Sel['ee']),
    ('l1_pt_mumu',Sel['mumu']),
    #('MCollASym',Sel['SymSel']),
    ('m_coll_emu_SRnoJets',Sel['SRnoJets']+'&&'+Sel['emu']),
    ('m_coll_mue_SRnoJets',Sel['SRnoJets']+'&&'+Sel['mue']),
    ('m_coll_emu_SRJets',Sel['SRwJets']+'&&'+Sel['emu']),
    ('m_coll_mue_SRJets',Sel['SRwJets']+'&&'+Sel['mue']),
    ('SRJets', Sel['SRwJets']),
    ('SRnJets',Sel['SRnoJets']),
    ('m_coll_emu_SymSel',Sel['SymSel']+'&&'+Sel['emu']),
    ('m_coll_mue_SymSel',Sel['SymSel']+'&&'+Sel['mue']),
    ('MLL_ee',Sel['ee']),
    ('MLL_mumu',Sel['mumu']),
    ('MLL_emu',Sel['emu']),
    ('MLL_mue',Sel['mue']),
    ('MLL_DF','('+Sel['emu']+'||'+Sel['mue']+')'),
    ('MLL_SF', '('+Sel['ee']+'||'+Sel['mumu']+')'),
    ('DphiLep0MET',Sel['SymSel']),
    ('DphiLep1MET',Sel['SymSel']),
    ('DphiLL',Sel['SymSel']),
    ('l_pt_Wjets_e', 'nSignalLeptons>=1 && l_flav[0]==0 && l_pt[0]>=30'),
    ('l_pt_Wjets_mu','nSignalLeptons>=1 && l_flav[0]==1 && l_pt[0]>=30'),
    ('j_pt[0]','1'),
    ('j_pt[1]','1'),
    ('j_pt[2]','1'),
    ('j_pt[3]','1'),
    ('j_pt[0]_Best', Sel['jets_Best']),
    ('j_pt[1]_Best', Sel['jets_Best']),
    ('j_pt[2]_Best', Sel['jets_Best']),
    ('j_pt[3]_Best', Sel['jets_Best']),
    #('l_pt[0]',Sel['SymSel'])
    ])
for pT in [20,30,40,50,60]:
    selectionList['SRJets_CLge%d'%pT] = Sel['SRwJnoJReq'] \
    + '&& nCentralLJets_ge%d>=1 && nCentralBJets==0'%pT
    selectionList['SRnJets_CLge%d'%pT] = Sel['SRnJnoJReq'] \
    + '&& nCentralLJets_ge%d==0 && nCentralBJets==0'%pT


variableList = OrderedDict([#default variable name is input variable
    ('met_None','met'),
    ('met_Base','met'),
    ('met_Sym','met'),
    ('met_Op','met'),
    ('met_SRwJ','met'),
    ('met_SRnoJ','met'),
    ('m_coll','MCollASym'),
    ('m_coll_emu_SRnoJets','MCollASym'),
    ('m_coll_mue_SRnoJets','MCollASym'),
    ('m_coll_emu_SRJets','MCollASym'),
    ('m_coll_mue_SRJets','MCollASym'),
    ('m_coll_emu_SymSel','MCollASym'),
    ('m_coll_mue_SymSel','MCollASym'),
    ('SRJets'    ,'MCollASym'),
    ('SRnJets'    ,'MCollASym'),
    ('SRJets_CLge20'    ,'MCollASym'),
    ('SRJets_CLge30'    ,'MCollASym'),
    ('SRJets_CLge40'    ,'MCollASym'),
    ('SRJets_CLge50'    ,'MCollASym'),
    ('SRJets_CLge60'    ,'MCollASym'),
    ('SRnJets_CLge20'   ,'MCollASym'),
    ('SRnJets_CLge30'   ,'MCollASym'),
    ('SRnJets_CLge40'   ,'MCollASym'),
    ('SRnJets_CLge50'   ,'MCollASym'),
    ('SRnJets_CLge60'   ,'MCollASym'),
    ('SRJets_noLJetreq', 'MCollASym'),
    ('SRJets_noBJetreq', 'MCollASym'),
    ('SRJets_noJetreq',  'MCollASym'),
    ('SRJets_noJetreqLepreq', 'MCollASym'),
    ('SRnJets_noLJetreq','MCollASym'),
    ('SRnJets_noBJetreq','MCollASym'),
    ('SRnJets_noJetreq', 'MCollASym'),
    ('SRnJets_noJetreqLepreq', 'MCollASym'),
    ('SRnJets_l0Met', 'MCollASym'),
    ('SRnJets_l1Met', 'MCollASym'),
    ('SRnJets_l0l1',  'MCollASym'),
    ('SRnJets_dPtll', 'MCollASym'),
    ('SRnJets_noJetl0Met', 'MCollASym'),
    ('SRnJets_noJetl1Met', 'MCollASym'),
    ('SRnJets_noJetl0l1',  'MCollASym'),
    ('SRnJets_noJetdPtll', 'MCollASym'),
    ('MLL_SF','MLL'),
    ('MLL_ee','MLL'),
    ('MLL_mumu','MLL'),
    ('MLL_emu','MLL'),
    ('MLL_mue','MLL'),
    ('MLL_DF','MLL'),
    ('l_pt_Wjets_e' ,'l_pt[0]'),
    ('l_pt_Wjets_mu','l_pt[0]'),
    ('j_pt[0]_Jge20','j_pt[0]'),
    ('j_pt[1]_Jge20','j_pt[1]'),
    ('j_pt[2]_Jge20','j_pt[2]'),
    ('j_pt[3]_Jge20','j_pt[3]'),
    ('j_pt[0]_Jge30','j_pt[0]'),
    ('j_pt[1]_Jge30','j_pt[1]'),
    ('j_pt[2]_Jge30','j_pt[2]'),
    ('j_pt[3]_Jge30','j_pt[3]'),
    ('j_pt[0]_Jge40','j_pt[0]'),
    ('j_pt[1]_Jge40','j_pt[1]'),
    ('j_pt[2]_Jge40','j_pt[2]'),
    ('j_pt[3]_Jge40','j_pt[3]'),
    ('j_pt[0]_Jge50','j_pt[0]'),
    ('j_pt[1]_Jge50','j_pt[1]'),
    ('j_pt[2]_Jge50','j_pt[2]'),
    ('j_pt[3]_Jge50','j_pt[3]'),
    ('j_pt[0]_Jge60','j_pt[0]'),
    ('j_pt[1]_Jge60','j_pt[1]'),
    ('j_pt[2]_Jge60','j_pt[2]'),
    ('j_pt[3]_Jge60','j_pt[3]'),
    ('j_pt[0]_Best', 'j_pt[0]'),
    ('j_pt[1]_Best', 'j_pt[1]'),
    ('j_pt[2]_Best', 'j_pt[2]'),
    ('j_pt[3]_Best', 'j_pt[3]'),
    ('j_flav_Jge20', 'j_flav'),
    ('j_flav_Jge30', 'j_flav'),
    ('j_flav_Jge40', 'j_flav'),
    ('j_flav_Jge50', 'j_flav'),
    ('j_flav_Jge60', 'j_flav'),
    ('l0_pt_emu','l_pt[0]'),
    ('l0_pt_mue','l_pt[0]'),
    ('l0_pt_ee','l_pt[0]'),
    ('l0_pt_mumu','l_pt[0]'),
    ('l1_pt_emu','l_pt[1]'),
    ('l1_pt_mue','l_pt[1]'),
    ('l1_pt_ee','l_pt[1]'),
    ('l1_pt_mumu','l_pt[1]')])

# Manually set entire x-axis label
SelAxisLabel = {
    'SRJets_noLJetreq'      :"no LJet Requirement",
    'SRJets_noBJetreq'      :"no BJet Requirement",
    'SRJets_noJetreq'       :"no Jet Requirement",
    'SRJets_noJetreqLepreq' :"no Jet Requirement w LepReq",
    'SRnJets_noLJetreq'      :"no LJet Requirement",
    'SRnJets_noBJetreq'      :"no BJet Requirement",
    'SRnJets_noJetreq'       :"no Jet Requirement",
    'SRnJets_noJetreqLepreq' :"no Jet Requirement w LepReq",
    'SRnJets_l0Met' : "#Delta#phi(l0,Met) same as SRJets",
    'SRnJets_l1Met' : "#Delta#phi(l1,Met) same as SRJets",
    'SRnJets_l0l1' :  "#Delta#phi(l0,l1) same as SRJets",
    'SRnJets_dPtll' : "#Deltap#_T(l0,l1) same as SRJets",
    'SRnJets_noJetl0Met' :"#Delta#phi(l0,Met) same as SRJets + no Jetreq",
    'SRnJets_noJetl1Met' :"#Delta#phi(l1,Met) same as SRJets + no Jetreq",
    'SRnJets_noJetl0l1'  :"#Delta#phi(l0,l1) same as SRJets + no Jetreq",
    'SRnJets_noJetdPtll' :"#Deltap#_T(l0,l1) same as SRJets + no Jetreq",
    'j_pt[3]_Jge60'         :'Jets>=60'
}

# Set ATLAS style
def setATLASStyle(path="/home/amete/ATLASStyle/current/"):
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
