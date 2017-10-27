import os,sys,ROOT,math
import time
from collections import OrderedDict, defaultdict
from optparse import OptionParser
import global_variables as G
import copy
BinZ = ROOT.RooStats.NumberCountingUtils.BinomialExpZ

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

LFV = True

# Open up the ROOT file
if LFV: inputFile = ROOT.TFile(G.analysis_run_dir+'LFV.root','READ')
else: inputFile = ROOT.TFile(G.analysis_run_dir+'Stop2L.root','READ')

if inputFile.IsZombie():
    print "Problem opening file ", inputFile

# Global variables for use in other plotting scripts
# Selections used in LFV INT note. Global so it can be used in other plotting scripts

S2L_trigger = '(((pass_HLT_2e12_lhloose_L12EM10VH||pass_HLT_e17_lhloose_mu14||pass_HLT_mu18_mu8noL1)&&treatAsYear==2015)||((pass_HLT_2e17_lhvloose_nod0||pass_HLT_e17_lhloose_nod0_mu14||pass_HLT_mu22_mu8noL1)&&treatAsYear==2016))'
S2L_ptCuts  = 'l_pt[0]>25.&&l_pt[1]>20.&&mll>40.'
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
# Different flaovr lepton triggs
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
    'dilep_trig': '(%s || %s)'%(dilep15_trig, dilep16_trig),
    'singlelep_trig': '(%s || %s)'%(singlelep15_trig,singlelep16_trig),
    'BaseSel'   : 'l_pt[0] >= 45 && l_pt[1] >= 15' 
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS,
    'SymSel'    : 'l_pt[0] >= 20 && l_pt[1] >= 20' 
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS, 
    'OpSel'     : 'l_pt[0] >= 45 && l_pt[1] >= 15' 
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS 
                  + ' && ' + 'dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0',
    'SRwJets'   : 'l_pt[0] >= 35 && l_pt[1] >= 15'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'dphi_l0_met>=1.0 && dphi_l1_met<=0.5 && dphi_ll>=1.0 && dpt_ll>=1.0' 
                  + ' && ' + 'nCentralLJets>=1 && nCentralBJets==0 && nSignalTaus == 0',
    'SRnoJets'  : 'l_pt[0] >= 35 && l_pt[1] >= 15 && ' 
                  + lep_eta_cut + ' && ' + DF_OS  
                  + ' && ' + 'dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0' 
                  + ' && ' + 'nCentralLJets==0 && nCentralBJets==0 && nSignalTaus == 0',
    'emu'       : 'dilep_flav == 0',
    'mue'       : 'dilep_flav == 1',
    'ee'        : 'dilep_flav == 2',
    'mumu'      : 'dilep_flav == 3',
    'base_LFV'      : 'mll>=20 && l_q[0]*l_q[1]<0 && dilep_flav <= 1',
    # Special Cuts for Testing
    'SRwJnoJReq'   : 'l_pt[0] >= 35 && l_pt[1] >= 12'
                  + ' && ' + lep_eta_cut + ' && ' + DF_OS
                  + ' && ' + 'dphi_l0_met>=1.0 && dphi_l1_met<=0.5 && dphi_ll>=1.0 && dpt_ll>=1.0',
    'SRnJnoJReq'  : 'l_pt[0] >= 35 && l_pt[1] >= 12 && ' 
                  + lep_eta_cut + ' && ' + DF_OS  
                  + ' && ' + 'dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0',
    'base_LFV_run1'      : 'mll>=20 && l_q[0]*l_q[1]<0\
                    &&((l_pt[0] >= 12 && l_pt[1] >= 8) && (dilep_flav<=1))',
    'jets_Best' : 'nForwardJets==nForwardJets_ge40',
    }
Sel["single_or_dilep_trig"] = '('+Sel['singlelep_trig']+' || '+Sel['dilep_trig']+')'
trigger_sel_name = 'dilep_trig'
trigger_selection = Sel[trigger_sel_name]

# Define the luminosity you want
luminosity = "36180" # ipb 
#luminosity = "3209" # ipb for data15 
#luminosity = "32971" # ipb for data16
# Main function
def write_or_append(path_name, minutes, outOp):
    file_exists = os.path.exists(path_name)
    if file_exists:
        time_of_mod = os.stat(path_name).st_mtime
        old_file_cut = minutes*60
        old_file = time.time() - time_of_mod > old_file_cut

    if not file_exists or old_file or outOp == 'W':
        return 'w'
    elif outOp == 'A' or outOp == '':
        return 'a'
    else:
        print ("WARNING (write_or_append): "
            + "Unknown file option")
 

def main():
    # User Inputs
    parser = OptionParser()
    parser.add_option('-v','--var',dest='variable',help='variable to plot') 
    parser.add_option('-o','--output',dest='outputOp',default='', help='(W or A) write new file or append to old file')
    (options, args) = parser.parse_args()
    variable = options.variable
    outputOp = options.outputOp
    
    # Run in batch mode
    ROOT.gROOT.SetBatch(True)

    # Set ATLAS style
    setATLASStyle()

    global inputFile

    # Output for yield table
    yield_tbl_path = G.analysis_run_dir+'YieldTable_tmp.txt'
    sig_tbl_path = G.analysis_run_dir+'SigTable_tmp.txt'
    old_file_age = 10  # minutes
    w_or_a_sig = write_or_append(sig_tbl_path, old_file_age, '')
    outputFile_sig = open(sig_tbl_path,w_or_a_sig)
    if outputOp != '':
        outputFile = open(yield_tbl_path,outputOp.lower())

    global luminosity

    # Other options
    blind_sig = False
    mass_window = [100,150]
    output_dir = G.analysis_run_dir+"plots/"
    if LFV:
        plot_name_prefix = "LFV_plot_" # Prefix added to the name of all plots 
        data_sample = 'data_all'   # name of data sample in input file. Should have 'data' in name.   
        signal_sample = 'Signal'
        
    else:
        plot_name_prefix = "Stop2L_plot_" # Prefix added to the name of all plots 
        data_sample = 'data'   # name of data sample in input file. Should have 'data' in name.   

    # Signal Branching Ratio
    BR = '0.01'

    INT_plot_list = [ 
        'l_pt[0]', 'dphi_l0_met', 'dphi_l1_met', 'dphi_ll', 
        'm_coll_emu_SRnoJets',' m_coll_mue_SRnoJets',
        'SRJets_CLge20', 'SRJets_CLge30', 'SRJets_CLge40', 
        'SRJets_CLge50', 'SRJets_CLge60', 
        'm_coll_emu_SRJets', 'm_coll_mue_SRJets']

    # Define the lists for samples, colors, and histogram properties
    if LFV:
        sampleList = OrderedDict([
            ('HWW',0.), ('Wjets',0.), ('Diboson',0.),
            ('Top',0.), ('Ztt_ZttEW',0.), ('Zll_ZEW',0.),
            (data_sample,0.),
            (signal_sample,0.)
            ])
    
        colorList  = {
            data_sample  : ROOT.kBlack ,
            'Wjets'     : ROOT.kBlue ,
            'HWW'       : ROOT.kYellow-9,
            'Top'       : ROOT.kRed+2 ,
            'Diboson'   : ROOT.kAzure+3 ,
            'Ztt_ZttEW' : ROOT.kOrange+2,
            'Ztt_check' : ROOT.kOrange+2,
            'Zll_ZEW'   : ROOT.kOrange-2,
            signal_sample : ROOT.kGreen }
        # Redfine for INT note comparison plots
        if variable in INT_plot_list:
            sampleList = OrderedDict([
                ('HWW',0.), ('Wjets',0.), ('Diboson',0.),
                ('Ztt_ZttEW',0.), ('Zll_ZEW',0.), ('Top',0.), 
                (data_sample,0.),
                (signal_sample,0.) 
                ])
            colorList['Ztt_ZttEW'] = ROOT.kOrange-2
            colorList['Zll_ZEW'] = ROOT.kOrange+2

        legendLabel  = {
            data_sample  : 'Data 2015/2016' ,
            'Wjets'     : 'W+jets' ,
            'HWW'       : 'HWW',         
            'Top'       : 'Top',         
            'Diboson'   : 'Diboson',     
            'Ztt_ZttEW' : 'Ztt_ZttEW', 
            'Ztt_check' : 'Ztautau', 
            'Zll_ZEW'   : 'Zll_ZEW',   
            signal_sample : 'H#rightarrow#taul (344084-91)' }
    else:
        sampleList = OrderedDict([
            ('higgs',0.),
            ('wjets_sherpa',0.),
            ('diboson_sherpa',0.),
            ('ttV',0.),
            ('singletop',0.),
            ('ttbar',0.),
            ('zjets_and_DY',0.),
            ('data',0.),
            ])

        colorList  = {
            'data'              : ROOT.kBlack ,
            'diboson_sherpa'    : ROOT.kAzure+3 ,
            'higgs'             : ROOT.kYellow-9,
            'singletop'         : ROOT.kRed+3 ,
            'ttbar'             : ROOT.kRed+2 ,
            'ttV'               : ROOT.kRed+4 ,
            'wjets_sherpa'      : ROOT.kBlue ,
            'zjets_and_DY'      : ROOT.kOrange-2}

        legendLabel  = {
            'data'              : 'Data 2015/2016' ,
            'diboson_sherpa'    : 'Diboson',
            'higgs'             : 'Higgs',
            'singletop'         : 'Single Top',
            'ttbar'             : 'ttbar',
            'ttV'               : 'ttV',
            'wjets_sherpa'      : 'W+Jets',
            'zjets_and_DY'      : 'Z+Jets'}

    histMaxBin = OrderedDict([ # default is 500
        ('nBaseJets',          40),
        ('nCentralLJets',      20),
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
        ('m_coll',              300),
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
        ('dphi_l0_met',         1.5*ROOT.TMath.Pi()),
        ('dphi_l1_met',         1.5*ROOT.TMath.Pi()),
        ('dphi_ll',             1.5*ROOT.TMath.Pi()),
        ('dpt_ll',              800),
        ('mll_ee',              500),
        ('mll_mumu',            500),
        ('mll_SF',              500),
        ('met',                 500),
        ('dilep_flav',          8)]) 
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
        ('dphi_l0_met', 0),
        ('dphi_l1_met', 0),
        ('dphi_ll',     0),
        ('m_coll',      50)])

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
        'nCentralLJets'         :20,
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
        #('m_coll',Sel['SymSel']),
        ('m_coll_emu_SRnoJets',Sel['SRnoJets']+'&&'+Sel['emu']),
        ('m_coll_mue_SRnoJets',Sel['SRnoJets']+'&&'+Sel['mue']),
        ('m_coll_emu_SRJets',Sel['SRwJets']+'&&'+Sel['emu']),
        ('m_coll_mue_SRJets',Sel['SRwJets']+'&&'+Sel['mue']),
        ('SRJets', Sel['SRwJets']),
        ('SRnJets',Sel['SRnoJets']),
        ('m_coll_emu_SymSel',Sel['SymSel']+'&&'+Sel['emu']),
        ('m_coll_mue_SymSel',Sel['SymSel']+'&&'+Sel['mue']),
        ('mll_ee',Sel['ee']),
        ('mll_mumu',Sel['mumu']),
        ('mll_emu',Sel['emu']),
        ('mll_mue',Sel['mue']),
        ('mll_DF','('+Sel['emu']+'||'+Sel['mue']+')'),
        ('mll_SF', '('+Sel['ee']+'||'+Sel['mumu']+')'),
        ('dphi_l0_met',Sel['SymSel']),
        ('dphi_l1_met',Sel['SymSel']),
        ('dphi_ll',Sel['SymSel']),       
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
        ('l_pt[0]',Sel['SymSel'])
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
        ('mll_emu','mll'),
        ('mll_mue','mll'),
        ('mll_DF','mll'),
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
    if outputOp=='W':
        outputFile.write('Selection\t')
        for sample in sampleList: 
             outputFile.write(sample +'\t+/-\t')
        outputFile.write('\n')

    # Produce Yield Table (optional)
    if outputOp=='W' or outputOp=='A':
        stringTest = ''
        for sel in Sel:
            if Sel[sel] in selectionList[variable]:
                stringTest += sel
                outputFile.write(sel+' ')
        if stringTest == '': outputFile.write('No Selection')        
        outputFile.write('\t')
    
    if w_or_a_sig == 'w':
        outputFile_sig.write("Variable\tBinExpZ Significance\n")
    
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
    cut = ROOT.TCut(Sel['base_LFV'] + ' && ' + trigger_selection)
    for sample in sampleList:
        ttree = inputFile.Get(sample)
        hname = 'hist_%s'%(sample)
        list_name = 'list_%s_%s'%(sample, trigger_sel_name) 
        save_name = G.analysis_run_dir + 'lists/' + list_name + '.root'
        if os.path.isfile(save_name):
            rfile = ROOT.TFile.Open(save_name)
            elist = rfile.Get(list_name)
            ttree.SetEventList(elist)
        else:
            draw_list = '>> ' + list_name
            ttree.Draw(draw_list, cut)
            elist = ROOT.gROOT.FindObject(list_name)
            ttree.SetEventList(elist)
            elist.SaveAs(save_name)
        htemp = ROOT.TH1D(hname,hname,histBinNum[variable],histMinBin[variable],histMaxBin[variable]) # 25 bins from 0 to 500
        htemp.Sumw2() # So that we get the correct errors after normalization
        draw_str = '%s>>%s'%(variableList[variable],hname) 
        sel = '(%s && %s && %s)'%(selectionList[variable],
                                  Sel['base_LFV'],
                                  trigger_selection)
        if data_sample in sample:
            if blind_sig and 'm_coll' in variable: 
                sel += '&& (m_coll<100 || m_coll>150)'
            ttree.Draw(draw_str,sel,'goff')
            sampleList[sample] = copy.copy(htemp)
            sampleList[sample].SetMarkerColor(ROOT.kBlack) 
            sampleList[sample].SetMarkerSize(1)
            sampleList[sample].SetMinimum(0.1)
            sampleList[sample].SetMaximum(histMaxY[variable])
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'p')
        elif signal_sample in sample:
            sel += '*%s*%s*eventweight'%(luminosity, BR) 
            ttree.Draw(draw_str,sel,'goff')
            sampleList[sample] = copy.copy(htemp)
            sampleList[sample].SetLineWidth(2) 
            sampleList[sample].SetLineColor(colorList[sample]) 
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'l')
        else: 
            sel += '*%s*eventweight'%(luminosity)
            ttree.Draw(draw_str,sel,'goff') 
            sampleList[sample] = copy.copy(htemp)
            htemp.SetDirectory(ROOT.NULL)
            sampleList[sample].SetDirectory(0)
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
        write_str = '%*.2f\t%*.2f\t'%(10,integral,10,error)
        if outputOp: outputFile.write(write_str)    
        htemp.Clear()
    # Determine Significance
    bkgd_err = ROOT.Double(0.)
    lw_bnd = totalSM.FindBin(mass_window[0])
    up_bnd = totalSM.FindBin(mass_window[1])
    bkgd_int  = totalSM.IntegralAndError(lw_bnd, up_bnd, bkgd_err)

    print "Background Integral in mass window = ", bkgd_int
    if bkgd_int > 0:
        bkgd_err_frac = bkgd_err/bkgd_int
        sig_int = sampleList[signal_sample].Integral(lw_bnd, up_bnd)
        ZbinSig = BinZ(sig_int,bkgd_int, bkgd_err_frac)
        print "Signal Significance (BinExpZ) = ", ZbinSig
        if w_or_a_sig:
            write_str = "%s\t%.3f\n"%(variable,ZbinSig)
            outputFile_sig.write(write_str)
    if outputOp: outputFile.write('\n')
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
    sampleList[data_sample].Draw('p && same');
    sampleList[signal_sample].Draw('HIST && SAME');
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
    if outputOp: outputFile.close()
    outputFile_sig.close()
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
