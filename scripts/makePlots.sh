#!/bin/bash

## Run the block below to get all the regions for the yield table
#python make_stack_plot.py -v 'met_None' -o 'N'
#python make_stack_plot.py -v 'met_Base' -o 'A'
#python make_stack_plot.py -v 'met_Sym' -o 'A'
#python make_stack_plot.py -v 'met_Op' -o 'A'
#python make_stack_plot.py -v 'met_SRwJ' -o 'A'
#python make_stack_plot.py -v 'met_SRnoJ' -o 'A'
#
## Run these 4 blocks to get INT note plots 
python make_stack_plot.py -v 'l_pt[0]' &
#python make_stack_plot.py -v 'dphi_l0_met'
#python make_stack_plot.py -v 'dphi_l1_met'
#python make_stack_plot.py -v 'dphi_ll'
#python make_stack_plot.py -v 'm_coll_emu_SRnoJets'
#python make_stack_plot.py -v 'm_coll_mue_SRnoJets'
#python make_stack_plot.py -v 'm_coll_emu_SRJets'
#python make_stack_plot.py -v 'm_coll_mue_SRJets'
##python make_stack_plot.py -v 'm_coll_emu_SymSel' # Not in INT note
##python make_stack_plot.py -v 'm_coll_mue_SymSel' # Not in INT note 
#
#python make_stack_plot.py -v 'l0_pt_emu' 
#python make_stack_plot.py -v 'l0_pt_mue' 
#python make_stack_plot.py -v 'l0_pt_ee' 
#python make_stack_plot.py -v 'l0_pt_mumu' 
#python make_stack_plot.py -v 'l1_pt_emu' 
#python make_stack_plot.py -v 'l1_pt_mue' 
#python make_stack_plot.py -v 'l1_pt_ee' 
#python make_stack_plot.py -v 'l1_pt_mumu'

#python make_comparison_plot.py -v 'l_pt' -i 'data' -s 'SymSel'
#python make_comparison_plot.py -v 'l_pt' -i 'MC' -s 'SymSel'
#python make_comparison_plot.py -v 'l0_pt' -i 'data' -s 'SymSel'
#python make_comparison_plot.py -v 'l0_pt' -i 'MC' -s 'SymSel'
#python make_comparison_plot.py -v 'l1_pt' -i 'data' -s 'SymSel'
#python make_comparison_plot.py -v 'l1_pt' -i 'MC' -s 'SymSel'
#
#python make_comparison_plot.py -v 'l_pt' -i 'data' -s 'OpSel'
#python make_comparison_plot.py -v 'l_pt' -i 'MC' -s 'OpSel'
#python make_comparison_plot.py -v 'l0_pt' -i 'data' -s 'OpSel'
#python make_comparison_plot.py -v 'l0_pt' -i 'MC' -s 'OpSel'
#python make_comparison_plot.py -v 'l1_pt' -i 'data' -s 'OpSel'
#python make_comparison_plot.py -v 'l1_pt' -i 'MC' -s 'OpSel'
#
#python make_fpT_plot.py

# Extra variables
python make_stack_plot.py -v 'l_pt[1]' &
#python make_stack_plot.py -v 'l_eta[0]'
#python make_stack_plot.py -v 'l_eta[1]'
python make_stack_plot.py -v 'dpt_ll' &
python make_stack_plot.py -v 'm_coll' 
python make_stack_plot.py -v 'mll' &
#python make_stack_plot.py -v 'met'
python make_stack_plot.py -v 'nBaseJets' & 
python make_stack_plot.py -v 'nCentralLJets' &
python make_stack_plot.py -v 'nCentralBJets' &
python make_stack_plot.py -v 'nForwardJets' &
#python make_stack_plot.py -v 'j_jvt'
#python make_stack_plot.py -v 'j_jft'
python make_stack_plot.py -v 'dilep_flav' &
wait
echo "Done!"
