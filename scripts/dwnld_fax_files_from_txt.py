#!/bin/env python

################################################################################
# This script downloads all the sample given in an input .txt file
#
# REQUIREMENTS BEFORE RUNNING:
#   localSetupFax
#   grid proxy (voms-init-proxy -voms atlas)
#
# alarmstr@cern.ch
# October 2017
# (C) University of California, Irvine
################################################################################
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', 
                        help = 'Input .txt file containing sample container names',
                        required = True)
    inputs = parser.parse_args()
    ifile = inputs.file

    if not os.path.isfile(ifile):
        print 'File not found: ', ifile
        sys.exit()
        
    input_containers = []
    for line in open(ifile).readlines():
        input_containers.append(line.strip())

    print "Checking that FAX is set-up"
    if os.environ.get('STORAGEPREFIX') == None :
        print "STORAGEPREFIX environment variable is empty!"
        print "You must call 'localSetupFAX' before calling this script."
        sys.exit()

    for container in input_containers





if __name__ = '__main__':
    main()
