import os,sys,ROOT,math
import time
from collections import OrderedDict, defaultdict
from optparse import OptionParser
import global_variables as G
import copy
BinZ = ROOT.RooStats.NumberCountingUtils.BinomialExpZ


# Open up the ROOT file
inputFile = ROOT.TFile(G.analysis_run_dir+'LFV.root','READ')

if inputFile.IsZombie():
    print "Problem opening file ", inputFile

# Global variables for use in other plotting scripts
# Selections used in LFV INT note. Global so it can be used in other plotting scripts

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
    G.setATLASStyle()

    # Output for yield table
    yield_tbl_path = G.analysis_run_dir+'YieldTable_tmp.txt'
    sig_tbl_path = G.analysis_run_dir+'SigTable_tmp.txt'
    old_file_age = 10  # minutes
    w_or_a_sig = write_or_append(sig_tbl_path, old_file_age, '')
    outputFile_sig = open(sig_tbl_path,w_or_a_sig)
    if outputOp != '':
        outputFile = open(yield_tbl_path,outputOp.lower())

    # Other options
    blind_sig = False
    mass_window = [100,150]
    output_dir = G.analysis_run_dir+"plots/"
    plot_name_prefix = "LFV_plot_" # Prefix added to the name of all plots

    data_sample = 'data_all'   # name of data sample in input file. Should have 'data' in name.
    signal_sample = 'Signal'

    INT_plot_list = [
        'l_pt[0]', 'dphi_l0_met', 'dphi_l1_met', 'dphi_ll',
        'm_coll_emu_SRnoJets',' m_coll_mue_SRnoJets',
        'SRJets_CLge20', 'SRJets_CLge30', 'SRJets_CLge40',
        'SRJets_CLge50', 'SRJets_CLge60',
        'm_coll_emu_SRJets', 'm_coll_mue_SRJets']

    # Define the lists for samples, colors, and histogram properties
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

    stack      = ROOT.THStack('mcStack','Standard Model')

    # Set the legend
    legend=ROOT.TLegend(0.7,0.6,0.9,0.9)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)

    # Read everything from the file
    print '='*50

    #Set Defaults
    if variable not in G.histMaxBin:    G.histMaxBin[variable] = 500
    if variable not in G.selectionList: G.selectionList[variable] = '1.0'
    if variable not in G.histMinBin:    G.histMinBin[variable] = 0
    if variable not in G.variableList:  G.variableList[variable] = variable
    if variable not in G.histMaxY:      G.histMaxY[variable] = 3*(10**8)
    if variable not in G.histBinNum:    G.histBinNum[variable] = 25

    # Setup output Yield Table
    if outputOp == 'W':
        outputFile.write('Selection\t')
        for sample in sampleList:
             outputFile.write(sample +'\t+/-\t')
        outputFile.write('\n')

    # Produce Yield Table (optional)
    if outputOp=='W' or outputOp=='A':
        stringTest = ''
        for sel in G.Sel:
            if G.Sel[sel] in G.selectionList[variable]:
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
    if '('+G.Sel['ee']+'||'+G.Sel['mumu']+')' in G.selectionList[variable]:
        if SelCount==0: SelectionString += 'SF'
        SelCount+=1
        DFSF = True
    elif '('+G.Sel['emu']+'||'+G.Sel['mue']+')' in G.selectionList[variable]:
        if SelCount==0: SelectionString += 'DF'
        SelCount+=1
        DFSF = True
    for sel in G.Sel:
        if sel in "ee mumu emu mue" and DFSF:
            continue
        if G.Sel[sel] in G.selectionList[variable]:
            if SelCount==0: SelectionString += sel
            if SelCount>0 : SelectionString += ','+sel
            SelCount+=1
        # Add any manual inputs stored in dictionary
    if variable in list(G.SelAxisLabel.keys()):
        SelectionString = G.SelAxisLabel[variable]
        # Default selection name if nothing specified
    if SelectionString == '': SelectionString='all events'

    # Make Plots
    totalSM = ROOT.TH1D('totalSM','totalSM',G.histBinNum[variable],G.histMinBin[variable],G.histMaxBin[variable])
    totalSM.Sumw2()
    cut = ROOT.TCut(G.Sel['base_LFV'] + ' && ' + G.trigger_selection)
    for sample in sampleList:
        ttree = inputFile.Get(sample)
        hname = 'hist_%s'%(sample)
        list_name = 'list_%s_%s'%(sample, G.trigger_sel_name)
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
        htemp = ROOT.TH1D(hname,hname,G.histBinNum[variable],G.histMinBin[variable],G.histMaxBin[variable]) # 25 bins from 0 to 500
        htemp.Sumw2() # So that we get the correct errors after normalization
        draw_str = '%s>>%s'%(G.variableList[variable],hname)
        sel = '(%s && %s && %s)'%(G.selectionList[variable],
                                  G.Sel['base_LFV'],
                                  G.trigger_selection)
        if data_sample in sample:
            if blind_sig and 'm_coll' in variable:
                sel += '&& (m_coll<100 || m_coll>150)'
            ttree.Draw(draw_str,sel,'goff')
            sampleList[sample] = copy.copy(htemp)
            sampleList[sample].SetMarkerColor(ROOT.kBlack)
            sampleList[sample].SetMarkerSize(1)
            sampleList[sample].SetMinimum(0.1)
            sampleList[sample].SetMaximum(G.histMaxY[variable])
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'p')
        elif signal_sample in sample:
            sel += '*%s*%s*eventweight'%(G.luminosity, G.BR)
            ttree.Draw(draw_str,sel,'goff')
            sampleList[sample] = copy.copy(htemp)
            sampleList[sample].SetLineWidth(2)
            sampleList[sample].SetLineColor(colorList[sample])
            # Fill the legend
            legend.AddEntry(sampleList[sample],legendLabel[sample],'l')
        else:
            sel += '*%s*eventweight'%(G.luminosity)
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
    dummyHisto  = G.dummifyHistogram(sampleList[data_sample].Clone())
    dummyHisto.GetXaxis().SetTitle('%s (%s)'%(G.variableList[variable],SelectionString))
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
