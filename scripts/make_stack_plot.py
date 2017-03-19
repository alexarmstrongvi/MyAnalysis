import os,sys,ROOT,math
from collections import OrderedDict
from optparse import OptionParser

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

# Global variables for use in other plotting scripts
# Selections used in LFV INT note. Global so it can be used in other plotting scripts
Sel = {
    'BaseSel'   : 'l_pt[0] >= 45 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'OpSel'     : 'l_pt[0] >= 45 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0 \
                    && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0',
    'SymSel'    : 'l_pt[0] >= 20 && l_pt[1]>=20 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'SRnoJets'  : 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0 \
                    && nCentralLJets==0 && nCentralBJets==0 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'SRwJets'   : 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=1.0 && dphi_l1_met<=0.5 && dphi_ll>=1.0 && dpt_ll>=1.0 \
                    && nCentralLJets>=1 && nCentralBJets==0 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'SRnJnoJReq'  : 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'SRwJnoJReq': 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=1.0 && dphi_l1_met<=0.5 && dphi_ll>=1.0 && dpt_ll>=1.0 \
                    && dilep_flav <= 1 && l_q[0]*l_q[1]<0',
    'emu'       : 'dilep_flav == 0',
    'mue'       : 'dilep_flav == 1',
    'ee'        : 'dilep_flav == 2',
    'mumu'      : 'dilep_flav == 3',
    # Selections for all jets to pass some threshold energy
    'jets_ge20' : 'nCentralLJets==nCentralLJets_ge20 && nCentralBJets==nCentralBJets_ge20 && nForwardJets==nForwardJets_ge20\
                     && nBaseJets-(nCentralBJets + nCentralLJets + nForwardJets)==nNonsignalJets_ge20',
    'jets_ge30' : 'nCentralLJets==nCentralLJets_ge30 && nCentralBJets==nCentralBJets_ge30 && nForwardJets==nForwardJets_ge30\
                     && nBaseJets-(nCentralBJets + nCentralLJets + nForwardJets)==nNonsignalJets_ge30',
    'jets_ge40' : 'nCentralLJets==nCentralLJets_ge40 && nCentralBJets==nCentralBJets_ge40 && nForwardJets==nForwardJets_ge40\
                     && nBaseJets-(nCentralBJets + nCentralLJets + nForwardJets)==nNonsignalJets_ge40',
    'jets_ge50' : 'nCentralLJets==nCentralLJets_ge50 && nCentralBJets==nCentralBJets_ge50 && nForwardJets==nForwardJets_ge50\
                     && nBaseJets-(nCentralBJets + nCentralLJets + nForwardJets)==nNonsignalJets_ge50',
    'jets_ge60' : 'nCentralLJets==nCentralLJets_ge60 && nCentralBJets==nCentralBJets_ge60 && nForwardJets==nForwardJets_ge60\
                     && nBaseJets-(nCentralBJets + nCentralLJets + nForwardJets)==nNonsignalJets_ge60',
    'jets_Best' : 'nForwardJets==nForwardJets_ge40',
    # Selections applied to all plots. Includes dilepton and single lepton triggers
    'dilep_trig':  '1.0'
    #'dilep_trig': '(((pass_HLT_2e12_lhloose_L12EM10VH||pass_HLT_e17_lhloose_mu14||pass_HLT_mu18_mu8noL1)\
    #                &&treatAsYear==2015)\
    #                ||((pass_HLT_2e17_lhvloose_nod0||pass_HLT_e17_lhloose_nod0_mu14||pass_HLT_mu22_mu8noL1)\
    #                &&treatAsYear==2016))',
    'singlelep_trig': '((((pass_HLT_e60_lhmedium || pass_HLT_e24_lhmedium_iloose_L1EM18VH)\
                    ||(pass_HLT_mu20_iloose_L1MU15 || pass_HLT_mu24_imedium || pass_HLT_mu26_imedium))\
                    &&treatAsYear==2015)\
                    ||(((pass_HLT_e24_lhtight_ivarloose_nod0 || pass_HLT_e26_lhtight_ivarloose_nod0 || pass_HLT_e60_lhmedium_nod0)\
                    ||(pass_HLT_mu24_iloose || pass_HLT_mu24_iloose_L1MU15 || pass_HLT_mu24_imedium || pass_HLT_mu26_imedium))\
                    &&treatAsYear==2016))',
    'base'      : 'mll>=20 && l_q[0]*l_q[1]<0\
                    &&(((l_pt[0] >= 20 && l_pt[1] >= 20) && (dilep_flav<=2))\
                    || ((l_pt[0] >= 25 && l_pt[1] >= 12) && (dilep_flav==3)))'
    }
# Open up the ROOT file
inputFile = ROOT.TFile('/data/uclhc/uci/user/armstro1/analysis_n0231_run/LFV.root','READ')

# Define the luminosity you want
luminosity = "35180" # ipb 

# Main function
def main():
    # User Inputs
    parser = OptionParser()
    parser.add_option('-v','--var',dest='variable',help='variable to plot') 
    parser.add_option('-o','--output',dest='outputOp',default='', help='(N or A) output to new file or add to old file')
    (options, args) = parser.parse_args()
    variable = options.variable
    outputOp = options.outputOp
    
    # Run in batch mode
    ROOT.gROOT.SetBatch(True)

    # Set ATLAS style
    setATLASStyle()

    global inputFile

    # Output for yield table
    if outputOp == 'N':   outputFile = open('/data/uclhc/uci/user/armstro1/analysis_n0231_run/YieldTable.txt','w')
    elif outputOp == 'A': outputFile = open('/data/uclhc/uci/user/armstro1/analysis_n0231_run/YieldTable.txt','a')

    global luminosity

    # Other options
    blind_sig = True
    output_dir = "/data/uclhc/uci/user/armstro1/analysis_n0231_run/plots/"
    plot_name_prefix = "LFV_plot_" # Prefix added to the name of all plots 
    data_sample = 'data_all'   # name of data sample in input file. Should have 'data' in name.   
    signal_sample = 'LFVsignal'   #name of signal sample in input file. Should have 'signal' in name.

    # Signal Branching Ratio
    BR = '0.01'

    # Define the lists for samples, colors, and histogram properties
    sampleList = OrderedDict([
        ('LFVsignal',0.),
        ('higgs',0.),
        ('ZV+WW+VVV',0.),
        #('dibosons',0),
        #('tribosons',0),
        ('Z+jets',0.),
        ('tt+Wt',0.),
        #('ttbar',0),
        #('singletop',0),
        #('ttv',0),
        ('W+jets',0.),
        ('data_all',0.)
        ])
    
    colorList  = { 
        'data_all'  : ROOT.kBlack ,
        'higgs'     : ROOT.kYellow-9,
        'tt+Wt'     : ROOT.kRed+2 ,
        'ZV+WW+VVV' : ROOT.kAzure-7 ,
        'ttbar'     : ROOT.kRed+3,
        'singletop' : ROOT.kRed+2,
        'ttv'       : ROOT.kRed+1,
        'dibosons'  : ROOT.kAzure+3,
        'tribosons' : ROOT.kAzure+2,
        'W+jets'    : ROOT.kGray,
        'Z+jets'    : ROOT.kOrange-2,
        'LFVsignal' : ROOT.kGreen }

    legendLabel  = { 
        'data_all'  : 'Data 2015/2016' ,
        'higgs'     : 'Higgs',
        'tt+Wt'     : 'tt+Wt', 
        'ZV+WW+VVV' : 'ZV+WW+VVV',
        'ttbar'     : 'tt',
        'singletop' : 'Single Top',
        'ttv'       : 'ttV',
        'dibosons'  : 'VV',
        'tribosons' : 'VVV',
        'W+jets'    : 'Non-prompt',
        'Z+jets'    : 'Z+jets',
        'LFVsignal' : 'H#rightarrow#taul (344084-91)' }

    histMaxBin = OrderedDict([ # default is 500
        ('nBaseJets',          40),
        ('nCentralLJets',      20),
        ('nCentralBJets',      10),
        ('nForwardJets',       15),
        ('nNonsignalJets_ge20',40),
        ('nCentralLJets_ge20', 20),
        ('nCentralBJets_ge20', 10),
        ('nForwardJets_ge20',  15),
        ('nNonsignalJets_ge30',10),
        ('nCentralLJets_ge30', 20),
        ('nCentralBJets_ge30', 10),
        ('nForwardJets_ge30',  15),
        ('nNonsignalJets_ge40',10),
        ('nCentralLJets_ge40', 20),
        ('nCentralBJets_ge40', 10),
        ('nForwardJets_ge40',  15),
        ('nNonsignalJets_ge50',10),
        ('nCentralLJets_ge50', 20),
        ('nCentralBJets_ge50', 10),
        ('nForwardJets_ge50',  15),
        ('nNonsignalJets_ge60',10),
        ('nCentralLJets_ge60', 20),
        ('nCentralBJets_ge60', 10),
        ('nForwardJets_ge60',  15),
        ('j_pt[0]',             500),
        ('j_pt[1]',             500),
        ('j_pt[2]',             500),
        ('j_pt[3]',             500),
        ('j_pt[0]_Jge20',       500),
        ('j_pt[1]_Jge20',       500),
        ('j_pt[2]_Jge20',       500),
        ('j_pt[3]_Jge20',       500),
        ('j_pt[0]_Jge30',       500),
        ('j_pt[1]_Jge30',       500),
        ('j_pt[2]_Jge30',       500),
        ('j_pt[3]_Jge30',       500),
        ('j_pt[0]_Jge40',       500),
        ('j_pt[1]_Jge40',       500),
        ('j_pt[2]_Jge40',       500),
        ('j_pt[3]_Jge40',       500),
        ('j_pt[0]_Jge50',       500),
        ('j_pt[1]_Jge50',       500),
        ('j_pt[2]_Jge50',       500),
        ('j_pt[3]_Jge50',       500),
        ('j_pt[0]_Jge60',       500),
        ('j_pt[1]_Jge60',       500),
        ('j_pt[2]_Jge60',       500),
        ('j_pt[3]_Jge60',       500),
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
        ('m_coll',              300),
        ('m_coll_emu_SRnoJets', 400),
        ('m_coll_mue_SRnoJets', 400),
        ('m_coll_emu_SRJets',   400),
        ('m_coll_mue_SRJets',   400),
        ('SRJets',              400),
        ('SRJets_CLge20',       400),
        ('SRJets_CLge30',       400),
        ('SRJets_CLge40',       400),
        ('SRJets_CLge50',       400),
        ('SRJets_CLge60',       400),
        ('SRnJets',             400),
        ('SRnJets_CLge20',       400),
        ('SRnJets_CLge30',       400),
        ('SRnJets_CLge40',       400),
        ('SRnJets_CLge50',       400),
        ('SRnJets_CLge60',       400),
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
        ('dphi_l0_met',         1.5*ROOT.TMath.Pi()),
        ('dphi_l1_met',         1.5*ROOT.TMath.Pi()),
        ('dphi_ll',             1.5*ROOT.TMath.Pi()),
        ('dpt_ll',              800),
        ('mll_ee',              500),
        ('mll_mumu',            500),
        ('mll_SF',              500),
        ('met',                 500),
        ('dilep_flav',          8)]) 

    histMinBin = OrderedDict([ #default is zero
        ('j_jvt',       -0.2),
        ('j_jvf',       -0.2),
        ('l_eta[0]',    -3.),
        ('l_eta[1]',    -3.),
        ('l1_pt_ee',    0),
        ('dphi_l0_met', 0),
        ('dphi_l1_met', 0),
        ('dphi_ll',     0),
        ('m_coll',      50)])

    histMaxY = { #default is 300 million 
        'j_jvt'             :3*(10**12),
        'j_jvf'             :3*(10**12),
        'm_coll_emu_SRnoJets':600,
        'm_coll_mue_SRnoJets':600,
        'm_coll_emu_SRJets':400,
        'm_coll_mue_SRJets':400,
        'SRJets'         :1000,
        'SRJets_CLge20'  :1000,
        'SRJets_CLge30'  :1000,
        'SRJets_CLge40'  :1000,
        'SRJets_CLge50'  :1000,
        'SRJets_CLge60'  :1000,
        'SRnJets'         :1500,
        'SRnJets_CLge20'  :1500,
        'SRnJets_CLge30'  :1500,
        'SRnJets_CLge40'  :1500,
        'SRnJets_CLge50'  :1500,
        'SRnJets_CLge60'  :1500,
        'SRJets_noLJetreq'  :3000,
        'SRJets_noBJetreq'  :3000,
        'SRJets_noJetreq'   :3000,
        'SRJets_noJetreqLepreq':     3000,
        'SRnJets_noLJetreq'  :2000,
        'SRnJets_noBJetreq'  :2000,
        'SRnJets_noJetreq'   :2000,
        'SRnJets_noJetreqLepreq':     2000,
        'SRnJets_l0Met' :2000,
        'SRnJets_l1Met' :2000,
        'SRnJets_l0l1' :2000,
        'SRnJets_dPtll' :2000,
        'SRnJets_noJetl0Met' :3000,
        'SRnJets_noJetl1Met' :3000,
        'SRnJets_noJetl0l1' :3000,
        'SRnJets_noJetdPtll' :3000, 
        'j_pt[0]'          :3*(10**8)
    } 

    histBinNum = { #default is 25
        'nBaseJets'             :40,
        'nCentralLJets'         :20,
        'nCentralBJets'         :10,
        'nForwardJets'          :15,
        'nNonsignalJets_ge20'   :40,
        'nCentralLJets_ge20'    :20,
        'nCentralBJets_ge20'    :10,
        'nForwardJets_ge20'     :15,
        'nNonsignalJets_ge30'   :10,
        'nCentralLJets_ge30'    :20,
        'nCentralBJets_ge30'    :10,
        'nForwardJets_ge30'     :15,
        'nNonsignalJets_ge40'   :10,
        'nCentralLJets_ge40'    :20,
        'nCentralBJets_ge40'    :10,
        'nForwardJets_ge40'     :15,
        'nNonsignalJets_ge50'   :10,
        'nCentralLJets_ge50'    :20,
        'nCentralBJets_ge50'    :10,
        'nForwardJets_ge50'     :15,
        'nNonsignalJets_ge60'   :10,
        'nCentralLJets_ge60'    :20,
        'nCentralBJets_ge60'    :10,
        'nForwardJets_ge60'     :15,
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
        'mll_SF'                :25,
        'mll_ee'                :25,
        'mll_mumu'              :25,
        'dilep_flav'            :8,
        'dphi_l0_met'           :36,   
        'dphi_l1_met'           :36,
        'dphi_ll'               :36,
        'm_coll_emu_SRnoJets'   :40,
        'm_coll_mue_SRnoJets'   :40,
        'm_coll_emu_SRJets'     :40,
        'm_coll_mue_SRJets'     :40,
        'SRJets_noLJetreq'      :40,
        'SRJets'                :40,
        'SRnJets'               :40,
        'SRJets_CLge20'          :40,
        'SRJets_CLge30'          :40,
        'SRJets_CLge40'          :40,
        'SRJets_CLge50'          :40,
        'SRJets_CLge60'          :40,
        'SRnJets_CLge20'         :40,
        'SRnJets_CLge30'         :40,
        'SRnJets_CLge40'         :40,
        'SRnJets_CLge50'         :40,
        'SRnJets_CLge60'         :40,
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
    global Sel
    selectionList = OrderedDict([ #default selection is True
        ('j_jvt','('+Sel['emu'] + '||' + Sel['mue']+')'),
        ('j_jvf','('+Sel['emu'] + '||' + Sel['mue']+')'),
        ('met_None','1.0'),
        ('met_Base',Sel['BaseSel']),
        ('met_Sym',Sel['SymSel']),
        ('met_Op',Sel['OpSel']),
        ('met_SRwJ',Sel['SRwJets']),
        ('met_SRnoJ',Sel['SRnoJets']),
        ('l0_pt_emu',Sel['emu']), #add selection on l1 for m_coll
        ('l0_pt_mue',Sel['mue']),
        ('l0_pt_ee',Sel['ee']),
        ('l0_pt_mumu',Sel['mumu']),
        ('l1_pt_emu',Sel['emu']),
        ('l1_pt_mue',Sel['mue']),
        ('l1_pt_ee',Sel['ee']),
        ('l1_pt_mumu',Sel['mumu']),
        ('m_coll',Sel['SymSel']),
        ('m_coll_emu_SRnoJets',Sel['SRnoJets']+'&&'+Sel['emu']),
        ('m_coll_mue_SRnoJets',Sel['SRnoJets']+'&&'+Sel['mue']),
        ('m_coll_emu_SRJets',Sel['SRwJets']+'&&'+Sel['emu']),
        ('m_coll_mue_SRJets',Sel['SRwJets']+'&&'+Sel['mue']),
        ('SRJets', Sel['SRwJets']),
        ('SRnJets',Sel['SRnoJets']),
        ('SRJets_CLge20', Sel['SRwJnoJReq']+'&& nCentralLJets_ge20>=1 && nCentralBJets==0'),
        ('SRJets_CLge30', Sel['SRwJnoJReq']+'&& nCentralLJets_ge30>=1 && nCentralBJets==0'),
        ('SRJets_CLge40', Sel['SRwJnoJReq']+'&& nCentralLJets_ge40>=1 && nCentralBJets==0'),
        ('SRJets_CLge50', Sel['SRwJnoJReq']+'&& nCentralLJets_ge50>=1 && nCentralBJets==0'),
        ('SRJets_CLge60', Sel['SRwJnoJReq']+'&& nCentralLJets_ge60>=1 && nCentralBJets==0'),
        ('SRnJets_CLge20',Sel['SRnJnoJReq']+'&& nCentralLJets_ge20==0 && nCentralBJets==0'),
        ('SRnJets_CLge30',Sel['SRnJnoJReq']+'&& nCentralLJets_ge30==0 && nCentralBJets==0'),
        ('SRnJets_CLge40',Sel['SRnJnoJReq']+'&& nCentralLJets_ge40==0 && nCentralBJets==0'),
        ('SRnJets_CLge50',Sel['SRnJnoJReq']+'&& nCentralLJets_ge50==0 && nCentralBJets==0'),
        ('SRnJets_CLge60',Sel['SRnJnoJReq']+'&& nCentralLJets_ge60==0 && nCentralBJets==0'),
        ('SRJets_noLJetreq',Sel['SRwJnoJReq']+'&&'+'nCentralBJets==0'),
        ('SRJets_noBJetreq',Sel['SRwJnoJReq']+'&&'+'nCentralLJets>=1'),
        ('SRJets_noJetreq',Sel['SRwJnoJReq']),
        ('SRJets_noJetreqLepreq',Sel['SRwJnoJReq']+'&& l_pt[0]<100 && l_pt[1]<100'),
        ('SRnJets_noLJetreq',Sel['SRnJnoJReq']+'&&'+'nCentralBJets==0'),
        ('SRnJets_noBJetreq',Sel['SRnJnoJReq']+'&&'+'nCentralLJets==0'),
        ('SRnJets_noJetreq',Sel['SRnJnoJReq']),
        ('SRnJets_noJetreqLepreq',Sel['SRnJnoJReq']+' && l_pt[0]<100 && l_pt[1]<100'),
        ('SRnJets_l0Met','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.0 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0 && nCentralLJets==0 && nCentralBJets==0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_l1Met','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.5 && dphi_ll>=2.3 && dpt_ll>=7.0 && nCentralLJets==0 && nCentralBJets==0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_l0l1','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=1.0 && dpt_ll>=7.0 && nCentralLJets==0 && nCentralBJets==0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_dPtll','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=1.0 && nCentralLJets==0 && nCentralBJets==0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_noJetl0Met','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=1.0 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_noJetl1Met','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.5 && dphi_ll>=2.3 && dpt_ll>=7.0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_noJetl0l1','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=1.0 && dpt_ll>=7.0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('SRnJets_noJetdPtll','l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=1.0 && dilep_flav <= 1 && l_q[0]*l_q[1]<0'),
        ('m_coll_emu_SymSel',Sel['SymSel']+'&&'+Sel['emu']),
        ('m_coll_mue_SymSel',Sel['SymSel']+'&&'+Sel['mue']),
        ('mll_ee',Sel['ee']),
        ('mll_mumu',Sel['mumu']),
        ('mll_DF','('+Sel['emu']+'||'+Sel['mue']+')'),
        ('mll_SF', '('+Sel['ee']+'||'+Sel['mumu']+')'),
        ('dphi_l0_met',Sel['SymSel']),
        ('dphi_l1_met',Sel['SymSel']),
        ('dphi_ll',Sel['SymSel']),       
        ('j_pt[0]','1'),
        ('j_pt[1]','1'),
        ('j_pt[2]','1'),
        ('j_pt[3]','1'),
        ('j_pt[0]_Jge20',Sel['jets_ge20']),
        ('j_pt[1]_Jge20',Sel['jets_ge20']),
        ('j_pt[2]_Jge20',Sel['jets_ge20']),
        ('j_pt[3]_Jge20',Sel['jets_ge20']),
        ('j_pt[0]_Jge30',Sel['jets_ge30']),
        ('j_pt[1]_Jge30',Sel['jets_ge30']),
        ('j_pt[2]_Jge30',Sel['jets_ge30']),
        ('j_pt[3]_Jge30',Sel['jets_ge30']),
        ('j_pt[0]_Jge40',Sel['jets_ge40']),
        ('j_pt[1]_Jge40',Sel['jets_ge40']),
        ('j_pt[2]_Jge40',Sel['jets_ge40']),
        ('j_pt[3]_Jge40',Sel['jets_ge40']),
        ('j_pt[0]_Jge50',Sel['jets_ge50']),
        ('j_pt[1]_Jge50',Sel['jets_ge50']),
        ('j_pt[2]_Jge50',Sel['jets_ge50']),
        ('j_pt[3]_Jge50',Sel['jets_ge50']),
        ('j_pt[0]_Jge60',Sel['jets_ge60']),
        ('j_pt[1]_Jge60',Sel['jets_ge60']),
        ('j_pt[2]_Jge60',Sel['jets_ge60']),
        ('j_pt[3]_Jge60',Sel['jets_ge60']),
        ('j_pt[0]_Best', Sel['jets_Best']),
        ('j_pt[1]_Best', Sel['jets_Best']),
        ('j_pt[2]_Best', Sel['jets_Best']),
        ('j_pt[3]_Best', Sel['jets_Best']),
        ('j_flav_Jge20', Sel['jets_ge20']),
        ('j_flav_Jge30', Sel['jets_ge30']),
        ('j_flav_Jge40', Sel['jets_ge40']),
        ('j_flav_Jge50', Sel['jets_ge50']),
        ('j_flav_Jge60', Sel['jets_ge60']),
        ('l_pt[0]',Sel['SymSel'])])

    variableList = OrderedDict([#default variable name is input variable
        ('met_None','met'),
        ('met_Base','met'),
        ('met_Sym','met'),
        ('met_Op','met'),
        ('met_SRwJ','met'),
        ('met_SRnoJ','met'),
        ('m_coll_emu_SRnoJets','m_coll'),
        ('m_coll_mue_SRnoJets','m_coll'),
        ('m_coll_emu_SRJets','m_coll'),
        ('m_coll_mue_SRJets','m_coll'),
        ('m_coll_emu_SymSel','m_coll'),
        ('m_coll_mue_SymSel','m_coll'),
        ('SRJets'    ,'m_coll'),
        ('SRnJets'    ,'m_coll'),
        ('SRJets_CLge20'    ,'m_coll'),
        ('SRJets_CLge30'    ,'m_coll'),
        ('SRJets_CLge40'    ,'m_coll'),
        ('SRJets_CLge50'    ,'m_coll'),
        ('SRJets_CLge60'    ,'m_coll'),
        ('SRnJets_CLge20'   ,'m_coll'),
        ('SRnJets_CLge30'   ,'m_coll'),
        ('SRnJets_CLge40'   ,'m_coll'),
        ('SRnJets_CLge50'   ,'m_coll'),
        ('SRnJets_CLge60'   ,'m_coll'),
        ('SRJets_noLJetreq', 'm_coll'),
        ('SRJets_noBJetreq', 'm_coll'),
        ('SRJets_noJetreq',  'm_coll'),
        ('SRJets_noJetreqLepreq', 'm_coll'),
        ('SRnJets_noLJetreq','m_coll'),
        ('SRnJets_noBJetreq','m_coll'),
        ('SRnJets_noJetreq', 'm_coll'),
        ('SRnJets_noJetreqLepreq', 'm_coll'),
        ('SRnJets_l0Met', 'm_coll'),
        ('SRnJets_l1Met', 'm_coll'),
        ('SRnJets_l0l1',  'm_coll'),
        ('SRnJets_dPtll', 'm_coll'), 
        ('SRnJets_noJetl0Met', 'm_coll'),
        ('SRnJets_noJetl1Met', 'm_coll'),
        ('SRnJets_noJetl0l1',  'm_coll'),
        ('SRnJets_noJetdPtll', 'm_coll'),
        ('mll_SF','mll'),
        ('mll_ee','mll'),
        ('mll_mumu','mll'),
        ('mll_DF','mll'),
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
                
    stack      = ROOT.THStack('mcStack','Standard Model')

    # Set the legend
    legend=ROOT.TLegend(0.7,0.6,0.9,0.9)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)

    # Read everything from the file
    print '='*50
    
    #Set Defaults
    if variable not in histMaxBin:    histMaxBin[variable] = 500
    if variable not in selectionList: selectionList[variable] = '1.0' 
    if variable not in histMinBin:    histMinBin[variable] = 0
    if variable not in variableList:  variableList[variable] = variable
    if variable not in histMaxY:      histMaxY[variable] = 3*(10**8)
    if variable not in histBinNum:    histBinNum[variable] = 25

    # Setup output Yield Table
    if outputOp=='N':
        outputFile.write('Selection\t')
        for sample in sampleList: 
            if 'data' in sample: outputFile.write(sample+'\t+/-\t') 
            else: outputFile.write(sample[5:]+'\t+/-\t')
        outputFile.write('\n')

    # Produce Yield Table (optional)
    if outputOp=='N' or outputOp=='A':
        stringTest = ''
        for sel in Sel:
            if Sel[sel] in selectionList[variable]:
                stringTest += sel
                outputFile.write(sel+' ')
        if stringTest == '': outputFile.write('No Selection')        
        outputFile.write('\t')
    
    
    # Create String with Selection Option Labels for plots
    SelectionString = ''
    SelCount = 0
    DFSF = False
    if '('+Sel['ee']+'||'+Sel['mumu']+')' in selectionList[variable]:
        if SelCount==0: SelectionString += 'SF'
        SelCount+=1
        DFSF = True
    elif '('+Sel['emu']+'||'+Sel['mue']+')' in selectionList[variable]: 
        if SelCount==0: SelectionString += 'DF'
        SelCount+=1
        DFSF = True
    for sel in Sel:
        if sel in "ee mumu emu mue" and DFSF: 
            continue
        if Sel[sel] in selectionList[variable]:
            if SelCount==0: SelectionString += sel
            if SelCount>0 : SelectionString += ','+sel
            SelCount+=1
        # Add any manual inputs stored in dictionary
    if variable in list(SelAxisLabel.keys()):
        SelectionString = SelAxisLabel[variable]
        # Default selection name if nothing specified
    if SelectionString == '': SelectionString='all events'        

    # Make Plots
    totalSM = ROOT.TH1D('totalSM','totalSM',histBinNum[variable],histMinBin[variable],histMaxBin[variable]) 
    totalSM.Sumw2()
    for sample in sampleList:
        htemp = ROOT.TH1D('hist_%s'%(sample),'hist_%s'%(sample),histBinNum[variable],histMinBin[variable],histMaxBin[variable]) # 25 bins from 0 to 500
        htemp.Sumw2() # So that we get the correct errors after normalization
        if 'data' in sample:
            if blind_sig and 'm_coll' in variable: 
                (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'(%s && %s && %s && (m_coll<100 || m_coll>150))'%(selectionList[variable],Sel['base'],Sel['dilep_trig']),'goff')
            else:
                (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'(%s && %s && %s)'%(selectionList[variable],Sel['base'],Sel['dilep_trig']),'goff')
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetMarkerColor(ROOT.kBlack) 
            sampleList[sample].SetMarkerSize(1)
            sampleList[sample].SetMinimum(0.1)
            sampleList[sample].SetMaximum(histMaxY[variable])
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'p')
        elif 'signal' in sample:
            (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'%s*%s*eventweight*(%s && %s && %s)'%(luminosity,BR,selectionList[variable],Sel['base'],Sel['dilep_trig']),'goff')
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetLineWidth(2) 
            sampleList[sample].SetLineColor(colorList[sample]) 
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'l')
            
        else: 
            (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'%s*eventweight*(%s && %s && %s)'%(luminosity,selectionList[variable],Sel['base'],Sel['dilep_trig']),'goff') 
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetLineWidth(2) 
            sampleList[sample].SetLineColor(ROOT.kBlack) 
            sampleList[sample].SetFillColor(colorList[sample]) 
            stack.Add(sampleList[sample]) # Add to stack
            totalSM.Add(sampleList[sample]) # Add to totalSM
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'f')
        error    = ROOT.Double(0.)
        integral = sampleList[sample].IntegralAndError(0,-1,error)
        print "%*s = %*.2f +/- %*.2f"%(15,sample,10,integral,10,error) 
        if outputOp != '': outputFile.write('%*.2f\t%*.2f\t'%(10,integral,10,error))    
        htemp.Clear()
    if outputOp != '': outputFile.write('\n')
    print '='*50

    # Draw
    canvas = ROOT.TCanvas('canvas','canvas',500,500)
    canvas.SetFillColor(0)
    topPad = ROOT.TPad('pTop','pTop',0,0.2,1,1)
    topPad.SetBottomMargin(0.15)
    topPad.Draw()
    botPad = ROOT.TPad('pBot','pBot',0,0.0,1,0.3)
    botPad.Draw()
    botPad.SetBottomMargin(0.30)

    # Top Pad
    topPad.cd()
    sampleList[data_sample].Draw('p')
    sampleList[data_sample].GetXaxis().SetLabelOffset(10)
    sampleList[data_sample].GetYaxis().SetTitle('Events')
    stack.Draw('same && hists');
    sampleList[signal_sample].Draw('hist && same')
    sampleList[data_sample].Draw('p && same');
    legend.Draw()
    if ('Jet' not in variable) or ('SR' not in variable): ROOT.gPad.SetLogy(True) 
    ROOT.gPad.RedrawAxis()

    # Bottom Pad
    botPad.cd()
    dummyHisto  = dummifyHistogram(sampleList[data_sample].Clone())
    dummyHisto.GetXaxis().SetTitle('%s (%s)'%(variableList[variable],SelectionString))
    # Get the actual Ratio
    numerator   = ROOT.TH1TOTGraph(sampleList[data_sample])
    denominator = ROOT.TH1TOTGraph(totalSM)
    ratio       = ROOT.myTGraphErrorsDivide(numerator,denominator)
    # Add Error Bars
    inputError  = ROOT.TGraphAsymmErrors(totalSM)
    outputError = ROOT.TGraphAsymmErrors(inputError)
    buildRatioErrorBand(inputError,outputError)

    # Draw
    dummyHisto.Draw("p")
    outputError.Draw("same && E2")
    ratio.Draw("same && p && 0 && 1")
    ROOT.gPad.SetGridy(1)

    # Save
    if outputOp!='': outputFile.close()
    canvas.SaveAs('%s%s%s.eps'%(output_dir,plot_name_prefix,variable)) 

def buildRatioErrorBand(inputGraph, outputGraph):
    outputGraph.SetMarkerSize(0);
    for binN in range(outputGraph.GetN()):
        outputGraph.GetY()[binN] = 1.
        if inputGraph.GetY()[binN] > 0.0001:
            outputGraph.GetEYhigh()[binN]=inputGraph.GetEYhigh()[binN]/inputGraph.GetY()[binN] 
        else:
            outputGraph.GetEYhigh()[binN]= 0. 
        if inputGraph.GetY()[binN] > 0.0001:
            outputGraph.GetEYlow()[binN]=inputGraph.GetEYlow()[binN]/inputGraph.GetY()[binN] 
        else:
            outputGraph.GetEYlow()[binN]= 0. 

        if outputGraph.GetEYlow()[binN] > 1.:
            outputGraph.GetEYlow()[binN] = 1. 
        if outputGraph.GetEYhigh()[binN] > 1.:
            outputGraph.GetEYhigh()[binN] = 1.
        outputGraph.SetMarkerSize(0)
        outputGraph.SetLineWidth(2)
        outputGraph.SetFillStyle(3354)
        outputGraph.SetFillColor(ROOT.kBlack)
        #print 'EYlow: ' + str(outputGraph.GetEYlow()[binN]) + ', EYhigh: ' + str(outputGraph.GetEYhigh()[binN])

if __name__ == "__main__":
    main()
