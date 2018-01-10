"""
Program: make_stack_plot.py
Author: Alex Armstrong <alarmstr@cern.ch>
Copyright: (C) Dec 21st, 2017; University of California, Irvine
Plotting script for stack plots
"""

import os,sys,ROOT,math
from collections import OrderedDict
from argparse import ArgumentParser
import global_variables as G
import copy
BinZ = ROOT.RooStats.NumberCountingUtils.BinomialExpZ

# Global variables for use in other plotting scripts
# Selections used in LFV INT note. Global so it can be used in other plotting scripts

def main():
    # User Inputs
    parser = ArgumentParser()
    parser.add_argument('file',
                      help='Input .root file with different samples')
    parser.add_argument('variable',
                      help='variable to be plotted')
    parser.add_argument('-r', '--region',\
                      default='',\
                      help='region choice from global_variables')
    parser.add_argument('-c', '--channel',\
                      default='',\
                      help='channel choice (ee,emu,mue,mumu)')
    parser.add_argument('--verbose',\
                      action='store_true',\
                      help='Run with additional printouts')
    args = parser.parse_args()

    ifile_name = args.file
    variable = args.variable
    region   = args.region
    channel  = args.channel
    verbose  = args.verbose

    print "\nRunning make_stack_plots..."
    print "Region: %s, Channel: %s, Variable: %s"%(region,channel,variable)

    # Open up the ROOT file
    file_path = G.analysis_run_dir+ifile_name
    if not os.path.exists(file_path):
        print "ERROR :: %s does not exist"%file_path
        sys.exit()
    inputFile = ROOT.TFile(file_path,'READ')
    if not inputFile or inputFile.IsZombie():
        print "ERROR :: Problem opening file ", file_path
        sys.exit()
    # Run in batch mode
    ROOT.gROOT.SetBatch(True)

    # Set ATLAS style
    G.setATLASStyle()

    # Other options
    blind_sig = True
    mass_window = [100,150]
    output_dir = G.analysis_run_dir+"plots/"
    plot_name_prefix = "HiggsLFV_" # Prefix added to the name of all plots

    data_sample = 'data_all'   # name of data sample in input file. Should have 'data' in name.
    signal_sample = 'Signal'

    # Define the lists for samples, colors, and histogram properties
    sampleList = OrderedDict([
        ('Wjets', 0.),
        ('Diboson', 0.),
        ('HWW', 0.),
        ('Top', 0.),
        ('Zll_ZEW', 0.),
        ('Ztt_ZttEW', 0.),
        ('Htt', 0.),
        (data_sample, 0.),
        (signal_sample, 0.)
        ])

    colorList  = {
        data_sample : ROOT.kBlack ,
        'Wjets'     : ROOT.kOrange,
        'HWW'       : ROOT.kBlue+3,
        'Htt'       : ROOT.kRed,
        'Top'       : ROOT.kOrange+2 ,
        'Diboson'   : ROOT.kSpring-6,
        'Ztt_ZttEW' : ROOT.kAzure-5,
        'Zll_ZEW'   : ROOT.kAzure-9,
        signal_sample : ROOT.kGreen }

    legendLabel  = {
        data_sample : 'Data 2015/2016' ,
        'Wjets'     : 'W+jets' ,
        'HWW'       : 'HWW',
        'Htt'       : 'H#rightarrow#tau_{lep}#tau_{lep}',
        'Top'       : 'Top',
        'Diboson'   : 'Di-Boson',
        'Ztt_ZttEW' : 'Z#rightarrow#tau#tau',
        'Zll_ZEW'   : 'Z#rightarrowll',
        signal_sample : 'H#rightarrow#taul (344084-91)' }

    # Set the legend
    legend=ROOT.TLegend(0.5,0.75,0.9,0.9)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetNColumns(2)

    # Read everything from the file
    if verbose: print '='*50

    #Set Defaults
    if variable not in G.HistOpMap:
        G.HistOpMap[variable] = G.HistOp1D(xLabel=variable)

    # Make Plots
    opt = G.HistOpMap[variable]


    stack = ROOT.THStack('mcStack','Standard Model')
    totalSM = ROOT.TH1D('totalSM', 'totalSM', opt.nBinsX, opt.x0, opt.x1)
    totalSM.Sumw2()
    for sample in sampleList:
        sel = '(%s && %s && %s)'%(
            G.Sel[region],G.Sel[channel],G.trigger_selection)

        ttree = inputFile.Get(sample)
        if not ttree:
            print "%s not found in %s"%(sample,ifile_name)
        # Set/Create Event List
       # list_name = 'list_%s_%s_%s_%s'%(
       #         sample,region,channel,G.trigger_sel_name)
       # save_name = G.analysis_run_dir + 'lists/' + list_name + '.root'
       # if os.path.isfile(save_name):
       #     rfile = ROOT.TFile.Open(save_name)
       #     elist = rfile.Get(list_name)
       #     ttree.SetEventList(elist)
       # else:
       #     draw_list = '>> ' + list_name
       #     ttree.Draw(draw_list, ROOT.TCut(sel))
       #     elist = ROOT.gROOT.FindObject(list_name)
       #     ttree.SetEventList(elist)
       #     elist.SaveAs(save_name)

        # Initizlize Histogram
        hname = 'hist_%s'%(sample)
        htemp = ROOT.TH1D(hname,hname, opt.nBinsX, opt.x0, opt.x1)
        htemp.Sumw2() # So that we get the correct errors after normalization
        draw_str = '%s>>%s'%(variable,hname)

        if data_sample in sample:
            if blind_sig and 'm_coll' in variable:
                sel += '&& (m_coll<%d || %d<m_coll)'%(
                    mass_window[0],mass_window[1])
            ttree.Draw(draw_str,sel,'goff')
            sampleList[sample] = copy.copy(htemp)
            sampleList[sample].SetMarkerColor(ROOT.kBlack)
            sampleList[sample].SetMarkerSize(1)
            sampleList[sample].SetMinimum(0.1)
            if variable in G.histMaxY:
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
            sel += '*%s*eventweight'%(G.luminosity);
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
        htemp.Clear()

    # Determine Significance
    bkgd_err = ROOT.Double(0.)
    lw_bnd = totalSM.FindBin(mass_window[0])
    up_bnd = totalSM.FindBin(mass_window[1])
    bkgd_int  = totalSM.IntegralAndError(lw_bnd, up_bnd, bkgd_err)

    if verbose:
        print "Background Integral in mass window = ", bkgd_int
        if bkgd_int > 0:
            bkgd_err_frac = bkgd_err/bkgd_int
            sig_int = sampleList[signal_sample].Integral(lw_bnd, up_bnd)
            ZbinSig = BinZ(sig_int,bkgd_int, bkgd_err_frac)
            print "Signal Significance (BinExpZ) = ", ZbinSig
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

    # Top Pad #
    topPad.cd()
    # Build axis label
    xlabel = opt.xLabel
    if opt.xUnits:
        xlabel += ' [%s]'%opt.xUnits
    ylabel = opt.yLabel
    if opt.x1 > opt.x0:
        bin_size = (opt.x1 - opt.x0)/float(opt.nBinsX)
        ylabel += "/%.2f"%bin_size
        if opt.xUnits:
            ylabel += opt.xUnits
    # Get max y
    mc_max = totalSM.GetMaximum()
    data_max = sampleList[data_sample].GetMaximum()
    if mc_max > data_max:
        max = mc_max
    else:
        max = data_max
    sampleList[data_sample].Draw('p')
    sampleList[data_sample].GetXaxis().SetLabelOffset(10)
    sampleList[data_sample].GetYaxis().SetTitle(ylabel)
    sampleList[data_sample].SetMaximum(1.5*max)
    stack.Draw('same && hists')
    sampleList[data_sample].Draw('p && same')
    sampleList[signal_sample].Draw('HIST && SAME')
    legend.Draw()
    #ROOT.gPad.SetLogy(True)
    ROOT.gPad.RedrawAxis()

    # Bottom Pad
    botPad.cd()
    dummyHisto  = G.dummifyHistogram(sampleList[data_sample].Clone())
    dummyHisto.GetXaxis().SetTitle(xlabel)
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
    canvas.SaveAs('%s%s%s_%s_%s.eps'%(
        output_dir,plot_name_prefix,region,channel,variable))
    #Clean Up
    stack.Clear()
    totalSM.Clear()

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
    # Do not execute main() when script is imported as a module
    main()
