#!/bin/bash/env python
import os
import sys
import subprocess
import commands
import global_variables as G
import python_tools as tools
import collections

# Configuration Settings
local_file_dir = '/data/uclhc/uci/user/dantrim/susynt_productions/n0235/'
old_file_dir = G.analysis_dir + 'LOCAL_inputs_LFV/'

def main():
    # Get list of local files
    old_root_files = get_root_file_dict(old_file_dir)
    missing_old_files = collections.defaultdict(list)
    stable_old_files = collections.defaultdict(list)
    for key, val in old_root_files.items():
        if not os.path.isfile(key):
            missing_old_files[val].append(key) 
        else:
            stable_old_files[val].append(key)
    with open('incomplete_samples.txt','w') as ofile:
        for sample in sorted(list(missing_old_files.keys())):
            ofile.write(sample+'\n')
    with open('complete_samples.txt','w') as ofile:
        for sample in sorted(list(stable_old_files.keys())):
            if sample not in missing_old_files:
                ofile.write(sample+'\n')
    print "Created incomplete and complete sample txt files."
def get_root_file_dict(dir_with_files):
    counter = 0
    root_files = {}
    for sample_dir in tools.get_list_of_subdirectories(dir_with_files):
        sample_dir = dir_with_files + sample_dir
        for dataset_dir in tools.get_list_of_files(sample_dir):
            if dataset_dir.endswith('.txt'):
                dataset_str = dataset_dir[:-4] 
            else:
                print "Unexpected directory name: ", dataset_dir
                sys.exit()
            dataset_dir = sample_dir + dataset_dir
            with open(dataset_dir,'r') as f:
                for line in f.readlines():
                    file_name = line.strip().split('}')[-1][1:]
                    if counter < 4:
                        print "Test file_name: ", file_name
                        counter += 1
                    if file_name in root_files:
                        print "WARNING: %s stored in %s and %s. Overwriting"%(
                                file_name,root_files[file_name],dataset_str)
                    root_files[file_name] = dataset_str
    print '\n'
    return root_files

    # Get list of rucio search terms
if __name__ == '__main__':
    main()

