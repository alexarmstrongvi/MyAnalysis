"""
Program: make_yield_table.py
Author: Alex Armstrong <alarmstr@cern.ch>
Copyright: (C) Dec 8th, 2017; University of California, Irvine
"""
from optparse import OptionParser
import ROOT
import tabulate
import global_variables as G


# Configure
data_sample_name = 'data_all'
signal_sample_name = 'Signal'

def main():
    """ Make yield table """
    # User input
    parser = OptionParser()
    parser.add_option('-f', '--file',
                      required=True,
                      help='Input .root file with different samples')
    parser.add_option('-s', '--samples',
                      required=True,
                      help='csv list of samples for the yield table')
    parser.add_option('-r', '--regions',
                      default='',
                      help='csv list of regions for the yield table')
    parser.add_option('-c', '--channels',
                      default='',
                      help='csv list of channels for the yield table')
    options, args = parser.parse_args()

    ifile_name = options.file
    sample_list  = [x.strip() for x in options.samples.split(",")]
    region_list  = [x.strip() for x in options.regions.split(",")]
    channel_list = [x.strip() for x in options.channels.split(",")]

    # Initialize
    ifile = ROOT.TFile(ifile_name, 'READ')
    if not ifile or ifile.IsZombie():
        print "ERROR :: Unable to open %s"%ifile
    hname = 'hist'
    draw_str = 'isMC>>%s'%hname
    ofile = open('YieldTable.txt', 'w')

    # Main looper
    for region in region_list:
        for channel in channel_list:
            print '\n\n============================================'
            print 'Region: %s\n Channel: %s'%(region, channel)
            yield_dict = {}
            mc_total = [0, 0]
            for sample in sample_list:
                # Set variables
                ttree = ifile.Get(sample)
                selection = '%s && %s'%(G.Sel[region], G.Sel[channel])
                hist = ROOT.TH1D(hname, hname, 3, -0.5, 2.5)

                # Get event yields
                ttree.Draw(draw_str, selection, 'goff')
                error = ROOT.Double(0.)
                integral = hist.IntegralAndError(0, -1, error)

                # Store results
                print "%*s = %*.2f +/- %*.2f"%(15, sample, 10, integral, 10, error)
                yield_dict[sample] = [integral, error]
                if data_sample_name not in sample and signal_sample_name not in sample:
                    mc_zip = zip(mc_total, yield_dict[sample])
                    mc_total = [sum(x) for x in mc_zip]
                hist.Clear()
            yield_dict['MC_total'] = mc_total
            data_yield = float(yield_dict[data_sample_name])
            yield_dict['MC_data_ratio'] = mc_total[0] / data_yield
            ofile.write('\n\n============================================')
            ofile.write('Region: %s\n Channel: %s'%(region, channel))
            ofile.write(tabulate.tabulate(yield_dict))
    ofile.close()

if __name__ == '__main__':
    # Do not run main when imported as module
    main()
