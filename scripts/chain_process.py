import glob
import sys
import shutil
import os

import ROOT as r


#output_filename = "mc15_higgs"
#output_filelist = ["data","mc15_ttbar","mc15_singletop","mc15_ttv","mc15_higgs","mc15_dibosons","mc15_tribosons","mc15_wjets","mc15_zjets"]
output_filelist = ["data","mc15_tt+Wt","mc15_higgs","mc15_ZV+WW+VVV","mc15_wjets","mc15_zjets","mc15_LFVsignal"]
directory_with_inputs = "/data/uclhc/uci/user/armstro1/analysis_n0228/inputs_LFV/"
directory_with_files = "/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/outputs/"
missing_dsid = open(directory_with_files+'missing.txt','w')

def get_dsids(filelist) :
    """
    expects single column data, with
    each entry a 6 digit dsid
    """
    out_dsids = []
    lines = open(filelist).readlines()
    for line in lines :
        if not line : continue
        if len(line) > 10 or len(line) < 3: continue
        line = line.strip()
        out_dsids.append(int(line))
    return out_dsids

def get_files(dsid_list, directory) :

    all_files = glob.glob(directory + "CENTRAL*.root")
    process_files = []
    for dsid in dsid_list :
        iii = 0
        for root_file in all_files :
            if str(dsid) in root_file :
                process_files.append(root_file)
                break # move to next dsid 
            iii += 1
        if iii == len(all_files): 
            missing_dsid.write(str(dsid)+"\n")
    return process_files

def main() :

    if os.path.isdir(directory_with_inputs+'missingSamples'):
        shutil.rmtree(directory_with_inputs+'missingSamples')
    os.makedirs(directory_with_inputs+'missingSamples')
    for filename in output_filelist:
        print "Running over " + filename
        filelist = "./dsid_filelist/%s_filelist.txt"%filename
        dsids = get_dsids(filelist)
        print "\tFound %d dataset ids"%len(dsids)
        
        #missing_dsid.write("\n"+"="*10+" Sample:  "+filename+"  "+"="*10+"\n\n")
        root_files = get_files(dsids, directory_with_files)
        print "\tFound %d root files for the process"%len(root_files)

        if len(root_files) != len(dsids) :
            print "\tERROR Did not find expected number of files!"
            #sys.exit()
        chain = r.TChain("superNt","superNt")
        for root_f in root_files :
            chain.Add(root_f)
        
        output_file = r.TFile("/data/uclhc/uci/user/armstro1/analysis_n0228_run/LFV/%s_CENTRAL.root"%filename,"RECREATE")
        chain.SetName("%s_CENTRAL"%filename)
        chain.Write()
        #chain.CloneTree(-1,"fast");
        output_file.Write() 
        print "\tProcess tree has %d total entries"%chain.GetEntries()

if __name__ == '__main__':
    main()
