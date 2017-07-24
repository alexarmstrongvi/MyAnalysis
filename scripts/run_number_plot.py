#!/bin/bash/env

import ROOT
import python_tools as tools
import csv
# -----------------------+
# Parameters 
data_files_dir = ""
luminosity_per_run_file = ""
run_num_col = 0
lumi_col = 6
ttree_name = "superNt"


# -----------------------+
# Get list of root files
data_file_list = tools.get_list_of_files(data_files_dir)

# -----------------------+
# Get map of luminosity per run
run_lumi = {}
with open(luminosity_per_run_file,'r') as lumi_csv:
    lumi_reader = csv.reader(lumi_csv,delimiter=',')
    for row in lumi_reader:
        run = row[run_num_col]
        if not run.isdigit(): continue
        run_lumi[run] = row[lumi_col]

# -----------------------+
# Map for run number event multiplicity
run_num_list = []
run_value_list = []

# -----------------------+
# Loop over root files
for data_file_name in data_file_list:
    # -----------------------+
    # Get TTree in Root file 
    tfile = ROOT.TFile(data_files_dir+data_file_name,"r")
    ttree = tfile.Get(ttree_name)

    # -----------------------+
    # Get run number 
    run_number = ttree.Get("runNumber") #is Get right?
    run_number = str(run_number)
    # -----------------------+
    # Draw hist with all events
    tmp_hist = ROOT.TH1I("hist_%s"%data_file_name,"hist_%s"%data_file_name,4,-1,2)
    ttree.Draw("isMC>>hist_%s"%data_file_name,,'goff')

    # -----------------------+
    # Get integral of all events 
    N = tmp_hist.Integral()/run_lumi[run_number]
        
    # -----------------------+
    # Store N_events in map with Run Number
    run_num_list.append(run_number)
    run_value_list.append(N)

# -----------------------+
# Create TGraph that will take map entries as input
n_entries = len(run_num_list)
run_hist = ROOT.TH1I("data_runs","data_runs",n_entries,0,n_entries)
for idx in range(n_entries):
    run_hist.SetBinContent(idx,run_value_list[idx])
    run_hist.GetXAxis().SetBinLabel(idx,run_num_list[idx])

# -----------------------+
# Create TCanvas 
canvas = ROOT.TCanvas("c1","Data Runs",10,10,2000,500)
canvas.SetGrid()
run_hist.Draw("P")
