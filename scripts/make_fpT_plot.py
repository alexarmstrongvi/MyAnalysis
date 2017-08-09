import ROOT
from optparse import OptionParser
from make_stack_plot import Sel, inputFile

def main():
    # User defined variables
    print "Input file from make_stack_plot.py: " + inputFile.GetName()
    output_directory = "/data/uclhc/uci/user/armstro1/analysis_n0235_run/plots/"
    sampleName      = 'data_all'
    histList        = {'l_pt_emu_dilep':0., 'l_pt_mue_dilep':0.,'l_pt_emu_singlelep':0., 'l_pt_mue_singlelep':0.}
    variableList    = {'l_pt_emu_dilep': 'l_pt[1]','l_pt_mue_dilep': 'l_pt[1]','l_pt_emu_singlelep': 'l_pt[1]','l_pt_mue_singlelep': 'l_pt[1]'} 
 
    selectionList   = {
        'l_pt_emu_dilep': Sel['emu'] + ' && ' + Sel['SRnoJets'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['dilep_trig'],
        'l_pt_mue_dilep': Sel['mue'] + ' && ' + Sel['SRnoJets'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['dilep_trig'],
        'l_pt_emu_singlelep': Sel['emu'] + ' && ' + Sel['SRnoJets'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['singlelep_trig'],
        'l_pt_mue_singlelep': Sel['mue'] + ' && ' + Sel['SRnoJets'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['singlelep_trig'],
        #'l_pt_emu_dilep': Sel['emu'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['dilep_trig'],
        #'l_pt_mue_dilep': Sel['mue'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['dilep_trig'],
        #'l_pt_emu_singlelep': Sel['emu'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['singlelep_trig'],
        #'l_pt_mue_singlelep': Sel['mue'] + ' && ' + Sel['base_LFV'] + ' && ' + Sel['singlelep_trig'],
    }
    minBin          = 0
    maxBin          = 200
    yMin    = 0.6
    yMax    = 1.8

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
    print "Starting to get Hists"
    for hist in histList:
        print "\tGetting " + hist + " (Var = %s)"%variableList[hist]
        histName = 'hist_%s'%hist
        htemp = ROOT.TH1F(histName,histName,20,minBin,maxBin)
        htemp.Sumw2()
        (inputFile.Get(sampleName)).Draw(variableList[hist]+'>>'+histName, "eventweight*(%s)"%selectionList[hist], 'goff')
        histList[hist] = htemp.Clone()
    
    # Create additional histograms
    print "Formatting final plot"
    histList['f(pT)_dilep'] = histList['l_pt_emu_dilep'].Clone() 
    histList['f(pT)_dilep'].Divide(histList['l_pt_mue_dilep'])
    histList['f(pT)_dilep'].GetXaxis().SetTitle('l_{1} pT')
    histList['f(pT)_dilep'].GetYaxis().SetTitle('#frac{e#mu}{#mue}')
    histList['f(pT)_singlelep'] = histList['l_pt_emu_singlelep'].Clone() 
    histList['f(pT)_singlelep'].Divide(histList['l_pt_mue_singlelep'])
    histList['f(pT)_singlelep'].SetMarkerColor(4)#ROOT.kBlue);
    #histList['f(pT)'].GetYaxis().SetLabelSize(0.1)
    #histList['f(pT)'].GetYaxis().SetTitleSize(0.12)
    #histList['f(pT)'].GetYaxis().SetTitleOffset(0.5)
    histList['f(pT)_dilep'].SetMinimum(yMin)
    histList['f(pT)_dilep'].SetMaximum(yMax)
    
    # Draw canvas
    canvas = ROOT.TCanvas('canvas','canvas',1000,500)
    canvas.SetFillColor(0)
    #canvas.cd()
    
    leg.AddEntry(histList['f(pT)_dilep'],'f(pT) dilep trig','p')
    leg.AddEntry(histList['f(pT)_singlelep'],'f(pT) singlelep trig','p')

    # Draw histogram
    histList['f(pT)_dilep'].Draw('p')
    histList['f(pT)_singlelep'].Draw('SAME')
    canvas.Update()
    l = ROOT.TLine(canvas.GetUxmin(),1.0,canvas.GetUxmax(),1.0)
    l.SetLineStyle(3)
    l.Draw()
    leg.Draw()
    # ROOT.gPad.SetLogy(True)
    # Save and Exit
    canvas.SaveAs('%sLFV_plot_f(pT).eps'%output_directory) 

if __name__ == '__main__':
    main()
