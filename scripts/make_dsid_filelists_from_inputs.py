#!/bin/bash/env python

import os
import python_tools as Tools
import global_variables as _g

directory_with_inputs = _g.analysis_dir+'inputs_LFV/'
output_directory = _g.analysis_run_dir+'dsid_filelist/'

def main():
    print "Creating DSID Filelists" 
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    sample_groupings = Tools.get_list_of_subdirectories(directory_with_inputs)
    grouping_names = [x[:-1] for x in sample_groupings]
    for group_dir in grouping_names:       
        samples = Tools.get_list_of_files(directory_with_inputs+group_dir)
        DSIDs = Tools.strip_strings_to_substrings(samples,'[1-9][0-9][0-9][0-9][0-9][0-9]')
        ofile = open(output_directory+group_dir+'.txt','w+')
        for dsid in DSIDs: ofile.write(dsid+'\n')
        ofile.close()
        print "\t%3i DSIDs for %20s written to %s"%(len(DSIDs),group_dir,output_directory.split('/')[-2])

if __name__ == '__main__':
    main()
