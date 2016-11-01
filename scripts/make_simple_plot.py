import os,sys,ROOT,math
from collections import OrderedDict

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

# Main function
def main():
    # Run in batch mode
    ROOT.gROOT.SetBatch(True)

    # Set ATLAS style
    setATLASStyle()

    # Open up the ROOT file
    inputFile = ROOT.TFile('/data/uclhc/uci/user/amete/analysis_n0228_run/EWK2L/hfts/HFT_COMBINED_13TeV.root','READ')

    # Define the luminosity you want
    luminosity = "25000." # In the file above eventweight is calcualted for 1 pb-1, so multiply it w/ 25k gives 25 fb-1

    # Define the selection you want to apply
    selection = "l_flav[0]!=l_flav[1]"      # here you can simply define a TCut based on the variables you have in your file, i.e. select = "mll>40." etc.    

    # Define the variable you want to plot
    variable = "mll"   # Again this should be in the ROOT file above

    # Define the list of backgrounds, their colors and the stack
    sampleList = OrderedDict([('Data',0.),('W',0.),('Z',0.),('higgs',0.),('VVV',0.),('VV',0.),('ttv',0.),('singletop',0.),('ttbar',0.)])
    colorList  = { 'Data' : ROOT.kBlack , 'ttbar' : ROOT.kAzure-9 , 'singletop' : ROOT.kOrange-3 , 'ttv' : ROOT.kRed+1 , 'VV' : ROOT.kSpring+1 , 'VVV' : ROOT.kSpring+3 , 'higgs' : ROOT.kBlue+1 , 'W' : ROOT.kGray , 'Z' : ROOT.kYellow-9 }
    stack      = ROOT.THStack('mcStack','Standard Model')

    # Set the legend
    legend=ROOT.TLegend(0.7,0.6,0.9,0.9)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)

    # Read everything from the file
    print '='*50
    totalSM = ROOT.TH1F('totalSM','totalSM',25,0,500) # 25 bins from 0 to 500 -> It should be possible to get this guy from the stack too
    totalSM.Sumw2()
    for sample in sampleList:
        htemp = ROOT.TH1F('hist_%s'%(sample),'hist_%s'%(sample),25,0,500) # 25 bins from 0 to 500
        htemp.Sumw2() # So that we get the correct errors after normalization
        if 'Data' in sample:
            (inputFile.Get('%s_CENTRAL'%(sample))).Draw('%s>>hist_%s'%(variable,sample),'(%s)'%(selection),'goff')
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetMarkerColor(ROOT.kBlack) 
            # Fill the legend
            legend.AddEntry(sampleList[sample],sample,'p')
        else: 
            (inputFile.Get('%s_CENTRAL'%(sample))).Draw('%s>>hist_%s'%(variable,sample),'%s*eventweight*(%s)'%(luminosity,selection),'goff') 
            sampleList[sample] = htemp.Clone()
            sampleList[sample].SetLineWidth(2) 
            sampleList[sample].SetLineColor(ROOT.kBlack) 
            sampleList[sample].SetFillColor(colorList[sample]) 
            stack.Add(sampleList[sample]) # Add to stack
            totalSM.Add(sampleList[sample]) # Add to totalSM
            # Fill the legend
            legend.AddEntry(sampleList[sample],sample,'f')
        error    = ROOT.Double(0.)
        integral = sampleList[sample].IntegralAndError(0,-1,error)
        print "%*s = %*.2f +/- %*.2f"%(10,sample,10,integral,10,error) 
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

    # Top Pad
    topPad.cd()
    sampleList['Data'].Draw('p');
    sampleList['Data'].GetXaxis().SetLabelOffset(10)
    sampleList['Data'].GetYaxis().SetTitle('Events')
    stack.Draw('same && hists');
    sampleList['Data'].Draw('p && same');
    legend.Draw()
    ROOT.gPad.SetLogy(True)
    ROOT.gPad.RedrawAxis()

    # Bottom Pad
    botPad.cd()
    dummyHisto  = dummifyHistogram(sampleList['Data'].Clone())
    dummyHisto.GetXaxis().SetTitle('%s'%(variable))
    # Get the actual Ratio
    numerator   = ROOT.TH1TOTGraph(sampleList['Data'])
    denominator = ROOT.TH1TOTGraph(totalSM)
    ratio       = ROOT.myTGraphErrorsDivide(numerator,denominator)
    # Draw
    dummyHisto.Draw("p")
    ratio.Draw("same && p && 0 && 1")
    ROOT.gPad.SetGridy(1)

    # Save
    canvas.SaveAs('Test_plot.png'); # can also store .pdf , .eps etc.

if __name__ == "__main__":
    main()
