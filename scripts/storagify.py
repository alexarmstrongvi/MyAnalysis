#!/usr/bin/env python



import glob
import subprocess
import sys
import os
import global_variables as _g

current_filelist_dir = _g.analysis_run_dir+'datasets/SLAC_inputs_LFV/' 
new_filelist_dir = _g.analysis_run_dir+'inputs_LFV_storagified/'

LOCAL = True

if LOCAL:
    replace_txt = "root://atlfax.slac.stanford.edu:1094//atlas/rucio/group.phys-susy:"
    new_txt = "root://${ATLAS_XROOTD_CACHE}//data/uclhc/uci/user/dantrim/susynt_productions/%s/"%_g.tag
else:
    replace_txt = "root://atlfax.slac.stanford.edu:1094/"
    new_txt = "root://atldtn1.slac.stanford.edu/"
    #new_txt = "root://fax.mwt2.org:1094/"

def get_sampledirs(filedir) :
    dirs = glob.glob(filedir + "*")
    return dirs

def make_new_filelist(original_txt_file, sample_name) :

    fname = original_txt_file.split("/")[-1]
    ofname = new_filelist_dir + sample_name + "/" + fname

    mkdir_cmd = "mkdir -p %s%s"%(new_filelist_dir, sample_name)
    subprocess.call(mkdir_cmd, shell=True)

    ofile = open(ofname, 'w')


    inlines = open(original_txt_file).readlines()
    for line in inlines :
        line = line.strip()
        if not line : continue
        if LOCAL:
            if "data" in fname: txt = "data/"
            elif "mc15" in fname: txt = "mc/"
            else: print "Error:", fname
            prefix = new_txt+txt+fname.replace('.txt','_nt/') 
            new_line = line.replace(replace_txt,prefix)
        else:
            new_line = line.replace(replace_txt, new_txt)
        ofile.write(new_line + "\n")
    ofile.close()

def make_new_list_for_sample(sample_dir, sample_name) :

    if not sample_dir.endswith("/") : sample_dir += "/"

    txt_files = glob.glob(sample_dir + "*.txt")
    for txt_file in txt_files :
        make_new_filelist(txt_file, sample_name)

def main() :
    if not os.path.isdir(current_filelist_dir): 
        print "Directory not found: " + current_filelist_dir
        sys.exit()
    print "storagify"

    sample_dirs = get_sampledirs(current_filelist_dir)
    n_total = len(sample_dirs)

    n_current = 1
    for sample_dir in sample_dirs :
        sample_name = sample_dir.split("/")[-1]
        print "storagify    [%d/%d] %s"%(n_current, n_total, sample_name)
        make_new_list_for_sample(sample_dir, sample_name)
        n_current += 1
    print "Files stored at " + new_filelist_dir 
    

#__________________________________________
if __name__ == "__main__" :
    main()
