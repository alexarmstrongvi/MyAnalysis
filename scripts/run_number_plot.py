#!/bin/bash/env

import ROOT
import python_tools as tools
import csv
import sys, os
import global_variables as G
from make_stack_plot import Sel, e15_trig, mu15_trig, e16_trig, mu16_trig
count = 0
# -----------------------+
# Parameters 
data_files_dir = G.output_dir+"outputs/"
luminosity_per_run_file = G.analysis_run_dir+"lumitable.csv"
save_name = G.analysis_run_dir+"plots/run_number.pdf"
selections = ""
run_num_col = 0
lumi_col = 6
ttree_name = "superNt"

selection = mu16_trig 
#Sel['singlelep_trig'] + " && " + Sel['base_LFV'] 

print "Making Run Number Plot..."
# -----------------------+
# Get list of root files
if not os.path.isdir(data_files_dir):
    print "Directory not found: " + data_files_dir
if not os.path.exists(luminosity_per_run_file):
    print "File not found: " + luminosity_per_run_file
data_file_list = tools.get_list_of_files(data_files_dir,'CENTRAL_physics_Main_*')

# -----------------------+
# Get map of luminosity per run
print "\tGetting Luminosity CSV file"
run_lumi = {}
with open(luminosity_per_run_file,'r') as lumi_csv:
    lumi_reader = csv.reader(lumi_csv,delimiter=',')
    for row in lumi_reader:
        run = row[run_num_col]
        if not run.isdigit(): continue
        run_lumi[run] = float(row[lumi_col])

# -----------------------+
# Map for run number event multiplicityrun_num_list = []
run_num_list = []
run_value_list = []

# -----------------------+
# Loop over root files
print "\tGetting Root Files"
for ii, data_file_name in enumerate(data_file_list):
    # -----------------------+
    # Get TTree in Root file 
    tfile = ROOT.TFile(data_files_dir+data_file_name,"r")
    ttree = tfile.Get(ttree_name)
    # -----------------------+
    # Get run number 
    run_number = ""
    for event in ttree: 
        run_number = str(event.runNumber) 
        break
    if run_number not in run_lumi:
        print "\t%d not found in csv file"%run_number
        continue
    # -----------------------+
    # Draw hist with all events
    draw_cmd = "isMC>>hist_%s"%data_file_name
    tmp_hist = ROOT.TH1I("hist_%s"%data_file_name,"hist_%s"%data_file_name,4,-1,2)
    ttree.Draw(draw_cmd,selection,'goff')

    # -----------------------+
    # Get integral of all events 
    N = tmp_hist.Integral()/run_lumi[run_number]
        
    # -----------------------+
    # Store N_events in map with Run Number
    run_num_list.append(run_number)
    run_value_list.append(N)

    # -----------------------+
    # Progress printout
    if ii % 10 == 0:
        print "\t\t%d/%d Data Files Processed"%(ii,len(data_file_list))
# -----------------------+
# Create TGraph that will take map entries as input
print "\tMaking Histogram"
n_entries = len(run_num_list)
run_hist = ROOT.TH1F("data_runs","data_runs",n_entries,0,n_entries)
for idx in range(n_entries):
    run_hist.SetBinContent(idx+1,run_value_list[idx])
    run_hist.GetXaxis().SetBinLabel(idx+1,run_num_list[idx])

# -----------------------+
# Create TCanvas 
print "\tDrawing to Canvas"
canvas = ROOT.TCanvas("c1","Data Runs",10,10,4000,500)
canvas.SetBatch(ROOT.kTRUE)
canvas.SetGrid()
print "\tSetting Style"
run_hist.SetMarkerStyle(3)
run_hist.SetMarkerColor(2)
print "\t Drawing"
run_hist.Draw('P')
print '\t Saving'
canvas.SaveAs(save_name)
