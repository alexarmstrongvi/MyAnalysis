"""
Program: make_yield_table.py
Author: Alex Armstrong <alarmstr@cern.ch>
Copyright: (C) Dec 8th, 2017; University of California, Irvine
"""
from argparse import ArgumentParser
from collections import namedtuple
import ROOT
import global_variables as G


# Configure
data_sample_name = 'data_all'
signal_sample_name = 'Signal'
output_file_name = 'YieldTable.txt'

def main():
    """ Make yield table """
    # User input
    parser = ArgumentParser()
    parser.add_argument('file',
                      help='Input .root file with different samples')
    parser.add_argument('samples',
                      help='csv list of samples for the yield table')
    parser.add_argument('-r', '--regions',\
                      default='',\
                      help='csv list of regions for the yield table')
    parser.add_argument('-c', '--channels',\
                      default='',\
                      help='csv list of channels for the yield table')
    parser.add_argument('-b', '--blind_regions',\
                      default='',\
                      help='csv list of blinded regions')
    args = parser.parse_args()

    ifile_name = args.file
    sample_list  = [x.strip() for x in args.samples.split(",")]
    region_list  = [x.strip() for x in args.regions.split(",")]
    channel_list = [x.strip() for x in args.channels.split(",")]
    blind_list   = [x.strip() for x in args.blind_regions.split(",")]

    # Initialize
    ifile = ROOT.TFile(ifile_name, 'READ')
    if not ifile or ifile.IsZombie():
        print "ERROR :: Unable to open %s"%ifile
    hname = 'hist'
    draw_str = 'isMC>>%s'%hname
    ofile = open(output_file_name, 'w')
    ofile.write("YieldTable\n")
    ofile.write("Region,Channel,Sample,Yield,Uncertainty\n")
    Yields = namedtuple('Yields',['value','error'])

    #------------------------------------------------------------------------->>
    # Main looper
    for region in region_list:
        print '\n\n============================================'
        for channel in channel_list:
            print 'Region: %s, Channel: %s'%(region, channel)
            yield_dict = {}
            mc_total = Yields(value=0,error=0)
            for sample in sample_list:
                # Set variables
                ttree = ifile.Get(sample)
                if not ttree:
                    print 'ERROR :: %s not found in %s'%(sample, ifile_name)
                selection = '(%s && %s && %s)'%(
                        G.Sel[region], G.Sel[channel], G.trigger_selection)
                hist = ROOT.TH1D(hname, hname, 3, -0.5, 2.5)

                # Get event yields
                if signal_sample_name in sample:
                    selection += '*%s*%s*eventweight'%(G.luminosity, G.BR)
                elif data_sample_name in sample:
                    if region in blind_list:
                        print "Blinding ", region
                        selection = '0'
                else:
                    selection += '*%s*eventweight'%(G.luminosity)
                ttree.Draw(draw_str, selection, 'goff')
                error = ROOT.Double(0.)
                integral = hist.IntegralAndError(0, -1, error)

                # Store results
                if integral > 0:
                    print "%*s = %*.2f +/- %*.2f"%(
                            15, sample, 10, integral, 10, error)
                    ofile.write('%s,%s,%s,%f,%f\n'%(
                        region, channel, sample, integral, error))
                else:
                    print "Integral  = ", integral
                    print "%*s = %*s +/- %*s"%(15, sample, 10, '-', 10, '-')
                    ofile.write('%s,%s,%s,-,-\n'%(
                        region, channel, sample))

                yield_dict[sample] = Yields(value=integral, error=error)
                if data_sample_name not in sample and signal_sample_name not in sample:
                    mc_zip = zip(mc_total, yield_dict[sample])
                    tmp_sum = [sum(x) for x in mc_zip]
                    # Convert list into namedtuple
                    mc_total = Yields._make(tmp_sum)
                hist.Clear()
            yield_dict['MC_total'] = mc_total
            print "%*s = %*.2f +/- %*.2f"%(
                    15,'MC Total', 10, mc_total.value, 10, mc_total.error)
            ofile.write('%s,%s,MC_total,%f,%f\n'%(
                region, channel, mc_total.value, mc_total.error))
            data_yield = float(yield_dict[data_sample_name].value)
            yield_dict['data_MC_ratio'] = data_yield / mc_total.value 
            print "%*s = %.4f"%(15,'MC/Data',yield_dict['data_MC_ratio'])
            ofile.write('%s,%s,Data/MC,%f,-\n'%(
                region, channel, yield_dict['data_MC_ratio']))
    print "\n...Output written to", output_file_name
    ofile.close()

if __name__ == '__main__':
    # Do not run main when imported as module
    main()
