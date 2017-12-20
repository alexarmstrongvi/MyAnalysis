import global_variables as G
file1_name = 'completed_files.txt'
file2_name = 'missing.txt'
ifile1 = open('%s/outputs/%s'%(G.analysis_run_dir,file1_name),'r')
ifile2 = open('%s/outputs/%s'%(G.analysis_run_dir,file2_name),'r')
ofile = open('%s/outputs/missing2.txt'%G.analysis_run_dir, 'w')

dsid_list = ifile1.readlines() 
for dsid in ifile2.readlines():
    if dsid in dsid_list:
        continue
    ofile.write('%s'%dsid)
ofile.close()
