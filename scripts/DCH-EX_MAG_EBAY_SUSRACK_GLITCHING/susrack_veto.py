#! /usr/bin/env python

from glue import segments
from gwpy.segments import DataQualityFlag
from gwsumm.data import get_timeseries_dict
from scipy import signal
import argparse
import numpy

parser = argparse.ArgumentParser(description='Calculate BLRMS of a channel. Smooth the data using a Savitzky-Golay filter and subtract this smooth data from the BLRMS. Threshold on this subtracted data to find a suitable veto')
parser.add_argument('-s', '--start', type=int, required=True, help='start time')
parser.add_argument('-e', '--end', type=int, required=True, help='end time')
parser.add_argument('-c', '--channel', type=str, default='H1:PEM-EX_MAG_EBAY_SUSRACK_X_DQ', help='channel name (optional)')
parser.add_argument('-sf', '--science', type=str, default='H1:DMT-ANALYSIS_READY:1', help='science flag (optional)')
parser.add_argument('-fl', '--flower', type=float, default='10', help='Lower frequency bandpass (Hz) (optional)')
parser.add_argument('-fu', '--fupper', type=float, default='50', help='Upper frequency bandpass (Hz) (optional)')
parser.add_argument('-st', '--stride', type=float, default='1', help='Stide for the RMS (s) (optional)')

args = parser.parse_args()

# define some varibales 
channel = [args.channel]
pad = 3 # samples to remove after filtering
thresh = 20 # thresholds
order = 3 # polynomial order for smoothing
window = 61 # window length for smoothing (figure ~60seconds is right)

# name xml file
chan = channel[0].replace(':', '_')
segment_file = '%s_THRESHOLD_GT_%s_%s-%s.xml' % (chan.replace('-','_'), thresh, args.start, abs(args.end-args.start))

# grab science segments
active = DataQualityFlag.query_dqsegdb(args.science, args.start, args.end).active

# grab channel data which is only in active segments 
data = get_timeseries_dict(channel, active, frametype='H1_R')

# BLRMS the channel data
blrms = [i.bandpass(args.flower, args.fupper, fstop=[args.flower/2., args.fupper*1.5], filtfilt=False, ftype='butter').crop(i.times.value[0]+pad,i.times.value[-1]-pad).rms(args.stride) for i in data[channel[0]]]

# smooth out the data using Savitzky-Golay filter
smooth_blrms = [signal.savgol_filter(i.value, window, order) for i in blrms]

# subtract the smooth data from the blrms and make all points positive
subtract_blrms = [abs(i - j) for i,j in zip(blrms,smooth_blrms)]

# find all the times which are larger than the threshold and concatenate
time = [j.times.value[j.value > thresh] for j in subtract_blrms]
times = numpy.concatenate(time)

# put times in to segment list and coalesce
segs = segments.segmentlist()
segs.extend([segments.segment(int(t), int(t)+args.stride) for t in times])
segs = segs.coalesce()

# set up the xml file by defining the start and end time of segments
start_time = []
start_time.extend([t[0] for t in segs])
end_time = []
end_time.extend([t[1] for t in segs])

# name the flags based on threshold
flag_name = 'H1:DCH-SUSRACK_GT_%s:1' % (str(thresh))

# put all information in to a DQ flag
flag = DataQualityFlag(flag_name, active=zip(start_time,end_time), known=[[args.start,args.end]])

# write dictionary to xml file
flag.write(segment_file)
