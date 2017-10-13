#1/bin/bash/env python

import os
import glob
import re

def main():
    print "Testing Tools"
    directory_with_subdir = 'LOCAL_inputs_LFV'
    directory_with_files = '/data/uclhc/uci/user/armstro1/SusyNt/analysis_n0232_run/scripts'
    list_of_subdirectories = get_list_of_subdirectories(directory_with_subdir)    
    list_of_files = get_list_of_files(directory_with_files)    
    print list_of_subdirectories
    print list_of_files
    list_of_files = strip_strings_to_substrings(list_of_files,'[aeiou]')
    print list_of_files

# output list of directories in directory
def get_list_of_subdirectories(directory,search_string='*/'):
    if not directory.endswith('/'): directory+='/'
    if not search_string.endswith('/'): search_string += '/'
    subdirectories = [(x.split('/')[-2]+'/') for x in glob.glob(directory+search_string)]
    if len(subdirectories)==0: print "WARNING: %s has no subdirectories"%directory 
    return subdirectories

# output list of files in directory
def get_list_of_files(directory, search_string='*'):
    if not directory.endswith('/'): directory+='/'
    files = [x.split('/')[-1] for x in glob.glob(directory+search_string)]
    if len(files)==0: print "WARNING: %s has no files"%directory
    return files

# strip input string list into substring list
def strip_strings_to_substrings(string_list,substring):
    substring_list = []
    for s in string_list:
        substring_list.append(strip_string_to_substring(s,substring))
    if all(x == '' for x in substring_list): print "WARNING: %s not found in any entry"%substring
    return substring_list

def strip_string_to_substring(string,substring):
    match = re.search(r'%s'%(substring),string)
    if match:
        return match.group()
    else: 
        return ''


if __name__ == '__main__':
    main()
