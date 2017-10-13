import ROOT
from optparse import OptionParser
from make_stack_plot import Sel, inputFile
import global_variables as G
import copy
import array
def main():
    # User defined variables
    print "Input file from make_stack_plot.py: " + inputFile.GetName()
    output_directory = G.analysis_run_dir+"plots/"
    sampleName      = 'data_all'
    hist_dict = {
        'l_pt_emu_dilep':{},
        'l_pt_mue_dilep':{},
        'l_pt_emu_singlelep':{},
        'l_pt_mue_singlelep':{},
        'l_pt_emu_both':{},
        'l_pt_mue_both':{}
        }
    var = 'l_pt[1]'
    common_sel = '(%s && %s)'%(Sel['SRnoJets'],Sel['base_LFV'])
    hist_dict['l_pt_emu_dilep']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['emu'],Sel['dilep_trig'])
    hist_dict['l_pt_mue_dilep']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['mue'],Sel['dilep_trig'])
    hist_dict['l_pt_emu_singlelep']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['emu'],Sel['singlelep_trig'])
    hist_dict['l_pt_mue_singlelep']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['mue'],Sel['singlelep_trig'])
    hist_dict['l_pt_emu_both']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['emu'],Sel['single_or_dilep_trig'])
    hist_dict['l_pt_mue_both']['selection'] = '(%s && %s && %s)'%(
        common_sel,Sel['mue'],Sel['single_or_dilep_trig'])
    min_bin          = 0
    max_bin          = 200
    yMin    = 0.6
    yMax    = 1.8
    bin_edges = [min_bin]
    while bin_edges[-1] < 100:
        bin_edges.append(bin_edges[-1]+10.0)
    bin_edges += [120.0, 150.0, max_bin]
    bin_array = array.array('f',sorted(bin_edges))
    # Set Batch Mode - don't draw anything as output
    ROOT.gROOT.SetBatch(True)
    
    # Set style settings
    ROOT.gROOT.SetMacroPath('/data/uclhc/uci/user/armstro1/ATLASStyle')
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

    # Setup legend
    leg = ROOT.TLegend(0.25,0.7,0.5,0.85)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    
    # Store variable in histogram
    #sample = inputFile.Get(sampleName)    
    print "Starting to get Hists"
    for hist, opt in hist_dict.items():
        print "\tGetting " + hist + " (Var = %s)"%var
        histName = 'hist_%s'%hist
        htemp = ROOT.TH1F(histName,histName,len(bin_edges)-1,bin_array)
        htemp.Sumw2()
        draw_str = var+'>>'+histName
        sel = "eventweight*(%s)"%opt['selection']
        ttree = inputFile.Get(sampleName)
        ttree.Draw(draw_str, sel, 'goff')
        opt['hist'] = copy.copy(htemp)
    
    # Create additional histograms
    print "Formatting final plot"
    hist_dict['f(pT)_dilep'] = copy.copy(hist_dict['l_pt_emu_dilep']['hist']) 
    hist_dict['f(pT)_dilep'].Divide(hist_dict['l_pt_mue_dilep']['hist'])
    hist_dict['f(pT)_dilep'].GetXaxis().SetTitle('l_{1} pT')
    hist_dict['f(pT)_dilep'].GetYaxis().SetTitle('#frac{e#mu}{#mue}')
    hist_dict['f(pT)_singlelep'] = copy.copy(hist_dict['l_pt_emu_singlelep']['hist']) 
    hist_dict['f(pT)_singlelep'].Divide(hist_dict['l_pt_mue_singlelep']['hist'])
    hist_dict['f(pT)_singlelep'].SetMarkerColor(4)
    hist_dict['f(pT)_both'] = copy.copy(hist_dict['l_pt_emu_both']['hist']) 
    hist_dict['f(pT)_both'].Divide(hist_dict['l_pt_mue_both']['hist'])
    hist_dict['f(pT)_both'].SetMarkerColor(2)
    hist_dict['f(pT)_dilep'].SetMinimum(yMin)
    hist_dict['f(pT)_dilep'].SetMaximum(yMax)
    
    # Draw canvas
    canvas = ROOT.TCanvas('canvas','canvas',1000,500)
    canvas.SetFillColor(0)
    #canvas.cd()
    
    leg.AddEntry(hist_dict['f(pT)_dilep'],'dilep trig','p')
    leg.AddEntry(hist_dict['f(pT)_singlelep'],'singlelep trig','p')
    leg.AddEntry(hist_dict['f(pT)_both'],'both trig','p')

    # Draw histogram
    hist_dict['f(pT)_dilep'].Draw('p')
    hist_dict['f(pT)_singlelep'].Draw('SAME')
    hist_dict['f(pT)_both'].Draw('SAME')
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
