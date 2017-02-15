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
                    && (dilep_flav == 0 || dilep_flav == 1) && l_q[0]*l_q[1]<0',
    'OpSel'     : 'l_pt[0] >= 45 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && (dilep_flav == 0 || dilep_flav == 1) && l_q[0]*l_q[1]<0 \
                    && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0',
    'SymSel'    : 'l_pt[0] >= 20 && l_pt[1]>=20 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && (dilep_flav == 0 || dilep_flav == 1) && l_q[0]*l_q[1]<0',
    'SRnoJets'  : 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=2.5 && dphi_l1_met<=0.7 && dphi_ll>=2.3 && dpt_ll>=7.0 \
                    && nCentralLJets == 0 && nCentralBJets==0 \
                    && (dilep_flav == 0 || dilep_flav == 1) && l_q[0]*l_q[1]<0',
    'SRwJets'   : 'l_pt[0] >= 35 && l_pt[1] >= 12 && fabs(l_eta[0]) <= 2.4 && fabs(l_eta[1]) <= 2.4 \
                    && dphi_l0_met>=1.0 && dphi_l1_met<=0.5 && dphi_ll>=1.0 && dpt_ll>=1.0 \
                    && nCentralLJets >= 1 && nCentralBJets==0 \
                    && (dilep_flav == 0 || dilep_flav == 1) && l_q[0]*l_q[1]<0',
    'trigger'   : '(((pass_HLT_2e12_lhloose_L12EM10VH||pass_HLT_e17_lhloose_mu14||pass_HLT_mu18_mu8noL1)\
                        &&treatAsYear==2015)\
                  ||((pass_HLT_2e17_lhvloose_nod0||pass_HLT_e17_lhloose_nod0_mu14||pass_HLT_mu22_mu8noL1)\
                        &&treatAsYear==2016))',
    'emu'       : 'dilep_flav == 0',
    'mue'       : 'dilep_flav == 1',
    'ee'        : 'dilep_flav == 2',
    'mumu'      : 'dilep_flav == 3',
    'base'      : 'mll>=20 && l_q[0]*l_q[1]<0\
                    &&(((l_pt[0] >= 20 && l_pt[1] >= 20) && (dilep_flav<=2))\
                    || ((l_pt[0] >= 25 && l_pt[1] >= 12) && (dilep_flav==3)))\
                    &&(((pass_HLT_2e12_lhloose_L12EM10VH||pass_HLT_e17_lhloose_mu14||pass_HLT_mu18_mu8noL1)\
                    &&treatAsYear==2015)\
                     ||((pass_HLT_2e17_lhvloose_nod0||pass_HLT_e17_lhloose_nod0_mu14||pass_HLT_mu22_mu8noL1)\
                    &&treatAsYear==2016))',
# && (nSignalJets==0 || j_pt>=40')
}

# Open up the ROOT file
inputFile = ROOT.TFile('/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/LFV_CENTRAL.root','READ')

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
    if outputOp == 'N':   outputFile = open('/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/YieldTable.txt','w')
    elif outputOp == 'A': outputFile = open('/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/YieldTable.txt','a')

    global luminosity

    # Other options
    blind_sig = True
    output_dir = "/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/plots/"
    plot_name_prefix = "LFV_plot_" # Prefix added to the name of all plots 
    data_sample = 'data_CENTRAL'   # name of data sample in input file   
    signal_sample = 'mc15_LFVsignal_CENTRAL'   #name of signal sample in input file

    # Signal Branching Ratio
    BR = '0.01'

    # Define the lists for samples, colors, and histogram properties
    sampleList = OrderedDict([
        ('mc15_LFVsignal_CENTRAL',0.),
        ('mc15_higgs_CENTRAL',0.),
        ('mc15_ZV+WW+VVV_CENTRAL',0.),
        #('mc15_dibosons_CENTRAL',0),
        #('mc15_tribosons_CENTRAL',0),
        ('mc15_zjets_CENTRAL',0.),
        ('mc15_tt+Wt_CENTRAL',0.),
        #('mc15_ttbar_CENTRAL',0),
        #('mc15_singletop_CENTRAL',0),
        #('mc15_ttv_CENTRAL',0),
        ('mc15_wjets_CENTRAL',0.),
        ('data_CENTRAL',0.)
        ])
    
    colorList  = { 
        'data_CENTRAL'           : ROOT.kBlack ,
        'mc15_higgs_CENTRAL'     : ROOT.kYellow-9,
        'mc15_tt+Wt_CENTRAL'     : ROOT.kRed+2 ,
        'mc15_ZV+WW+VVV_CENTRAL' : ROOT.kAzure-7 ,
        'mc15_ttbar_CENTRAL'     : ROOT.kRed+3,
        'mc15_singletop_CENTRAL' : ROOT.kRed+2,
        'mc15_ttv_CENTRAL'       : ROOT.kRed+1,
        'mc15_dibosons_CENTRAL'  : ROOT.kAzure+3,
        'mc15_tribosons_CENTRAL' : ROOT.kAzure+2,
        'mc15_wjets_CENTRAL'     : ROOT.kGray,
        'mc15_zjets_CENTRAL'     : ROOT.kOrange-2,
        'mc15_LFVsignal_CENTRAL' : ROOT.kGreen }

    legendLabel  = { 
        'data_CENTRAL'           : 'Data 2015/2016' ,
        'mc15_higgs_CENTRAL'     : 'Higgs',
        'mc15_tt+Wt_CENTRAL'     : 'tt+Wt', 
        'mc15_ZV+WW+VVV_CENTRAL' : 'ZV+WW+VVV',
        'mc15_ttbar_CENTRAL'     : 'tt',
        'mc15_singletop_CENTRAL' : 'Single Top',
        'mc15_ttv_CENTRAL'       : 'ttV',
        'mc15_dibosons_CENTRAL'  : 'VV',
        'mc15_tribosons_CENTRAL' : 'VVV',
        'mc15_wjets_CENTRAL'     : 'Non-prompt',
        'mc15_zjets_CENTRAL'     : 'Z+jets',
        'mc15_LFVsignal_CENTRAL' : 'H#rightarrow#taul (344084-91)' }

    histMaxBin = OrderedDict([ # default is 500
        ('nBaseJets',           40),
        ('nCentralLJets',       20),
        ('nCentralBJets',       10),
        ('nForwardJets',        15),
        ('j_pt[0]',             500),
        ('j_pt[1]',             500),
        ('j_pt[2]',             500),
        ('j_pt[3]',             500),
        ('j_jvt',               1.2),
        ('j_jvf',               1.2),
        ('j_flav',              8),
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
        'm_coll_emu_SRnoJets':1000,
        'm_coll_mue_SRnoJets':1200,
        'm_coll_emu_SRJets':1000,
        'm_coll_mue_SRJets':1000
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
        'm_coll_emu_SymSel'     :40,
        'm_coll_mue_SymSel'     :40
    }
    global Sel
    selectionList = OrderedDict([ #default selection is True
        ('nBaseJets',           '1.0'),
        ('nCentralLJets',       '1.0'),
        ('nCentralBJets',       '1.0'),
        ('nForwardJets',        '1.0'),
        ('j_jvt','('+Sel['mue'] + '||' + Sel['emu']+')'),
        ('j_jvf','('+Sel['mue'] + '||' + Sel['emu']+')'),
        ('met_None','1.0'),
        ('met_Base',Sel['BaseSel']),
        ('met_Sym',Sel['SymSel']),
        ('met_Op',Sel['OpSel']),
        ('met_SRwJ',Sel['SRwJets']),
        ('met_SRnoJ',Sel['SRnoJets']),
        ('l0_pt_emu',Sel['emu']),
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
        ('m_coll_emu_SymSel',Sel['SymSel']+'&&'+Sel['emu']),
        ('m_coll_mue_SymSel',Sel['SymSel']+'&&'+Sel['mue']),
        ('mll_ee',Sel['ee']),
        ('mll_mumu',Sel['mumu']),
        ('mll_DF','('+Sel['emu']+'||'+Sel['mue']+')'),
        ('mll_SF', '('+Sel['ee']+'||'+Sel['mumu']+')'),
        ('dphi_l0_met',Sel['SymSel']),
        ('dphi_l1_met',Sel['SymSel']),
        ('dphi_ll',Sel['SymSel']),       
        ('j_pt[0]','j_flav>=0'),
        ('j_pt[1]','j_flav>=0'),
        ('j_pt[2]','j_flav>=0'),
        ('j_pt[3]','j_flav>=0'),
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
        ('mll_SF','mll'),
        ('mll_ee','mll'),
        ('mll_mumu','mll'),
        ('mll_DF','mll'),
        ('l0_pt_emu','l_pt[0]'),
        ('l0_pt_mue','l_pt[0]'),
        ('l0_pt_ee','l_pt[0]'),
        ('l0_pt_mumu','l_pt[0]'),
        ('l1_pt_emu','l_pt[1]'),
        ('l1_pt_mue','l_pt[1]'),
        ('l1_pt_ee','l_pt[1]'),
        ('l1_pt_mumu','l_pt[1]')]) 

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
    if SelectionString == '': SelectionString='all events'        

    # Make Plots
    totalSM = ROOT.TH1D('totalSM','totalSM',histBinNum[variable],histMinBin[variable],histMaxBin[variable]) 
    totalSM.Sumw2()
    for sample in sampleList:
        htemp = ROOT.TH1D('hist_%s'%(sample),'hist_%s'%(sample),histBinNum[variable],histMinBin[variable],histMaxBin[variable]) # 25 bins from 0 to 500
        htemp.Sumw2() # So that we get the correct errors after normalization
        if 'data' in sample:
            if blind_sig and 'm_coll' in variable: 
                (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'(%s && %s && (m_coll<100 || m_coll>150))'%(selectionList[variable],Sel['base']),'goff')
            else:
                (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'(%s && %s)'%(selectionList[variable],Sel['base']),'goff')
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetMarkerColor(ROOT.kBlack) 
            sampleList[sample].SetMarkerSize(1)
            sampleList[sample].SetMinimum(0.1)
            sampleList[sample].SetMaximum(histMaxY[variable])
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'p')
        elif 'signal' in sample:
            (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'%s*%s*eventweight*(%s && %s)'%(luminosity,BR,selectionList[variable],Sel['base']),'goff')
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetLineWidth(2) 
            sampleList[sample].SetLineColor(colorList[sample]) 
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'l')
            
        else: 
            (inputFile.Get(sample)).Draw('%s>>hist_%s'%(variableList[variable],sample),'%s*eventweight*(%s && %s)'%(luminosity,selectionList[variable],Sel['base']),'goff') 
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
    if ('Jets' not in variable) or ('m_coll' not in variable): ROOT.gPad.SetLogy(True) 
    ROOT.gPad.RedrawAxis()

    # Bottom Pad
    botPad.cd()
    dummyHisto  = dummifyHistogram(sampleList[data_sample].Clone())
    dummyHisto.GetXaxis().SetTitle('%s (%s)'%(variableList[variable],SelectionString))
    # Get the actual Ratio
    numerator   = ROOT.TH1TOTGraph(sampleList[data_sample])
    denominator = ROOT.TH1TOTGraph(totalSM)
    ratio       = ROOT.myTGraphErrorsDivide(numerator,denominator)
    # Draw
    dummyHisto.Draw("p")
    ratio.Draw("same && p && 0 && 1")
    ROOT.gPad.SetGridy(1)

    # Save
    if outputOp!='': outputFile.close()
    canvas.SaveAs('%s%s%s.eps'%(output_dir,plot_name_prefix,variable)) 

if __name__ == "__main__":
    main()
