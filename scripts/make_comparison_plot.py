import os,sys,ROOT,math
from collections import OrderedDict
from optparse import OptionParser
from make_stack_plot import Sel, setATLASStyle, inputFile, luminosity

# Dummy ratio histogram
def dummifyHistogram(histo):
    ratio_histo = histo.Clone();
    ratio_histo.Reset();
    ratio_histo.SetMarkerSize(1.2);
    ratio_histo.SetMarkerStyle(20);
    ratio_histo.SetLineWidth(2);
    ratio_histo.GetYaxis().SetTitle("#frac{emu}{mue}");
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

# Main function
def main():
    # User Input
    parser = OptionParser()
    parser.add_option('-v','--var',dest='variable',help='variable to plot')    
    parser.add_option('-i','--input',dest='inputType',help='data or MC input',default='data')
    parser.add_option('-s','--selection',dest='selection',help='event selection',default='SymSel')
    (options, args) = parser.parse_args()
    variable = options.variable
    inputType = options.inputType
    selection = options.selection
    yMin = 1*(10**-1)
    yMax = 1*(10**5)
    # Run in batch mode
    ROOT.gROOT.SetBatch(True)

    # Set ATLAS style
    setATLASStyle()

    # Define the sample
    # select the TTrees from the inputfile that you want to run over
    if inputType == 'data':
        sample = ['data_all']
    elif inputType == 'MC':
        #sample = ['mc15_higgs','mc15_dibosons','mc15_zjets','mc15_ttbar','mc15_wjets','mc15_tribosons','mc15_singletop','mc15_ttv']
        sample = ['higgs','ZV+WW+VVV','Z+jets','tt+Wt','W+jets']
    else: print 'ERROR: unrecognized input type. Choose \"data\" or \"MC\"' 

    # Define the variable you want to plot
    # Again this should be in the ROOT file above
    if variable == 'l1_pt':
        plotList = ['l1_pt_emu','l1_pt_mue']
    elif variable == 'l0_pt':
        plotList = ['l0_pt_emu','l0_pt_mue']
    elif variable == 'l_pt':
        plotList = ['e_pt','mu_pt']
    else: 
        print "ERROR: undefined variable" 

    histList = OrderedDict([
        ('l0_pt_emu',0.),
        ('l0_pt_mue',0.),
        ('l1_pt_emu',0.),
        ('l1_pt_mue',0.),
        ('e_pt',0.),
        ('mu_pt',0.)])
    histMaxBin = OrderedDict([("",0.)]) #defualt is 500
    histMinBin = OrderedDict([ #default is zero
    ]) 
    if selection == 'SymSel':
        selectionList = OrderedDict([ #default selection is True
            ('l0_pt_emu',Sel['SymSel']+"&&"+Sel['emu']),
            ('l0_pt_mue',Sel['SymSel']+"&&"+Sel['mue']),
            ('l1_pt_emu',Sel['SymSel']+"&&"+Sel['emu']),
            ('l1_pt_mue',Sel['SymSel']+"&&"+Sel['mue']),
            ('e_pt',Sel['SymSel']+"&& l_flav==0"),
            ('mu_pt',Sel['SymSel']+"&& l_flav==1")])
    elif selection == "OpSel":
        selectionList = OrderedDict([ #default selection is True
            ('l0_pt_emu',Sel['OpSel']+" && "+Sel['emu']),
            ('l0_pt_mue',Sel['OpSel']+" && "+Sel['mue']),
            ('l1_pt_emu',Sel['OpSel']+" && "+Sel['emu']),
            ('l1_pt_mue',Sel['OpSel']+" && "+Sel['mue']),
            ('e_pt',Sel['OpSel']+"&& l_flav==0"),
            ('mu_pt',Sel['OpSel']+"&& l_flav==1")])
    else: print 'ERROR: undefined selection option. Choose \"SymSel\" or \"OpSel\"'
 
    histColor = {
        'l0_pt_emu':ROOT.kBlue,
        'l0_pt_mue':ROOT.kRed,
        'l1_pt_emu':ROOT.kBlue,
        'l1_pt_mue':ROOT.kRed, 
        'e_pt':ROOT.kBlue,
        'mu_pt':ROOT.kRed                 
        }
    variableList = OrderedDict([#default variable name is the same as histList key
        ('l0_pt_emu','l_pt[0]'),
        ('l0_pt_mue','l_pt[0]'),
        ('l1_pt_emu','l_pt[1]'),
        ('l1_pt_mue','l_pt[1]'), 
        ('e_pt','l_pt'),
        ('mu_pt','l_pt')]) 
       
    # Set the legend
    legend=ROOT.TLegend(0.7,0.6,0.9,0.9)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)

    # Read everything from the file
    print '='*50

    for hist in plotList:
        #define loop variables
        if hist not in variableList: 
            variableList[hist] = hist
        if hist not in selectionList:
            selectionList[hist] = 1.0
        if hist not in histMinBin:
            histMinBin[hist] = 0
        if hist not in histMaxBin:
            histMaxBin[hist] = 500.
        
        htemp = ROOT.TH1F('hist_%s'%(hist),'hist_%s'%(hist),25,histMinBin[hist],histMaxBin[hist])
        htemp.Sumw2() # So that we get the correct errors after normalization
        for sam in sample:
            #print 'Running over %s sample'%sam
            samhist = ROOT.TH1F('samHist','samHist',25,histMinBin[hist],histMaxBin[hist])
            samhist.Sumw2()
            if inputType == 'data':
                (inputFile.Get(sam)).Draw('%s>>samHist'%(variableList[hist]),'(%s)'%(selectionList[hist]),'goff')
            else:
                (inputFile.Get(sam)).Draw('%s>>samHist'%(variableList[hist]),'%s*eventweight*(%s && %s)'%(luminosity,selectionList[hist],Sel['trigger']),'goff')
            htemp.Add(samhist)
            samhist.Clear()
        histList[hist] = htemp.Clone()
        histList[hist].SetMarkerColor(histColor[hist])
        histList[hist].SetMinimum(yMin)
        #histList[hist].SetMaximum(yMax) 
        error    = ROOT.Double(0.)
        integral = histList[hist].IntegralAndError(0,-1,error)
        print "%*s = %*.2f +/- %*.2f"%(10,hist,10,integral,10,error)
        htemp.Clear()
    
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
    topPad.cd()

    legend.AddEntry(histList[plotList[0]],plotList[0],'p')
    histList[plotList[0]].Draw('p');
    histList[plotList[0]].GetXaxis().SetLabelOffset(10)
    histList[plotList[0]].GetYaxis().SetTitle('Events')
    numerator   = ROOT.TH1TOTGraph(histList[plotList[0]])
    denominator = ROOT.TH1TOTGraph(histList[plotList[0]])
    dummyHisto = dummifyHistogram(histList[plotList[0]].Clone())

    legend.AddEntry(histList[plotList[1]],plotList[1],'p')
    histList[plotList[1]].Draw('p && HIST && same');
    dummyHisto  = None
    denominator = None
    dummyHisto  = dummifyHistogram(histList[plotList[1]].Clone()) 
    # Get the actual Ratio
    denominator = ROOT.TH1TOTGraph(histList[plotList[1]])
    ratio       = ROOT.myTGraphErrorsDivide(numerator,denominator)
    botPad.cd()

    dummyHisto.GetXaxis().SetTitle('%s'%(variableList[plotList[0]]))
    # Draw
    dummyHisto.Draw("p")
    ratio.Draw("same && p && 0 && 1")
    ROOT.gPad.SetGridy(1)
    topPad.cd()
    legend.Draw()
    ROOT.gPad.SetLogy(True)
    ROOT.gPad.RedrawAxis()
    # Save
    canvas.SaveAs('/data/uclhc/uci/user/armstro1/analysis_n0231_run/plots/LFV_plot_%s_%s_%s.eps'%(variableList[plotList[0]],inputType,selection)); # can also store .pdf , .eps etc.
    canvas.Close()

if __name__ == "__main__":
    main()
