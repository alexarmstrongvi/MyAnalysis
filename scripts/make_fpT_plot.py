import ROOT
from optparse import OptionParser
from make_stack_plot import Sel, inputFile

def main():
    # User defined variables
    sampleName      = 'data_CENTRAL'
    histList        = {'l_pt_emu':0., 'l_pt_mue':0.}
    variableList    = {'l_pt_emu': 'l_pt[1]','l_pt_mue': 'l_pt[1]'} 
 
    selectionList   = {
        'l_pt_emu': Sel['emu']+ ' && ' + Sel['SRnoJets'],
        'l_pt_mue': Sel['mue']+ ' && ' + Sel['SRnoJets']
    }
    minBin          = 0
    maxBin          = 200

    # Set Batch Mode - don't draw anything as output
    ROOT.gROOT.SetBatch(True)
    
    # Set style settings
    ROOT.gROOT.SetMacroPath('/data/uclhc/uci/user/armstro1/ATLASStyle')
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

    # Setup legend
    leg = ROOT.TLegend(0.55,0.7,0.9,0.85)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    
    # Store variable in histogram
    #sample = inputFile.Get(sampleName)    
    for hist in histList:
        histName = 'hist_%s'%hist
        htemp = ROOT.TH1F(histName,histName,20,minBin,maxBin)
        htemp.Sumw2()
        (inputFile.Get(sampleName)).Draw(variableList[hist]+'>>'+histName, "eventweight*(%s)"%selectionList[hist], 'goff')
        histList[hist] = htemp.Clone()
    
    # Create additional histograms
    histList['f(pT)'] = histList['l_pt_emu'].Clone() 
    histList['f(pT)'].Divide(histList['l_pt_mue'])
    histList['f(pT)'].GetXaxis().SetTitle('l_{1} pT')
    histList['f(pT)'].GetYaxis().SetTitle('#frac{e#mu}{#mue}')
    #histList['f(pT)'].GetYaxis().SetLabelSize(0.1)
    #histList['f(pT)'].GetYaxis().SetTitleSize(0.12)
    #histList['f(pT)'].GetYaxis().SetTitleOffset(0.5)
    
    # Draw canvas
    canvas = ROOT.TCanvas('canvas','canvas',1000,500)
    canvas.SetFillColor(0)
    #canvas.cd()
    
    leg.AddEntry(histList['f(pT)'],'f(pT)','p')

    # Draw histogram
    histList['f(pT)'].Draw('p')
    canvas.Update()
    l = ROOT.TLine(canvas.GetUxmin(),1.0,canvas.GetUxmax(),1.0)
    l.SetLineStyle(3)
    l.Draw()
    # leg.Draw()
    # ROOT.gPad.SetLogy(True)
    # Save and Exit
    canvas.SaveAs('LFV_plot_f(pT).eps') 

if __name__ == '__main__':
    main()
