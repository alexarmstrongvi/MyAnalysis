#!/bin/bash
file="LFV.root"
regions="Baseline VBF Optimized"
#regions="Optimized"
channels="emu mue"
#channels="emu"
variables="MCollASym"
#variables="Lep0Pt"
#variables="$variables Lep1Pt"
#variables="$variables MET"
#variables="$variables DEtaLL"
#variables="$variables DphiLL"
#variables="$variables drll"
#variables="$variables MtLep0"
#variables="$variables MtLep1"
#variables="$variables ptll"
#variables="$variables dpt_ll"
#variables="$variables Jet_N2p4Eta25Pt"
#variables="$variables j_pt[0]"
for var in $variables; do
    for reg in $regions; do
        for ch in $channels; do
            python make_stack_plot.py "$file" "$var" -r "$reg" -c "$ch" &
        done
    done
done
