#! /usr/bin/env python

from glue import segments
from gwpy.segments import DataQualityFlag
from gwsumm.data import get_timeseries_dict
import argparse
import numpy

parser = argparse.ArgumentParser(description='Take the BLRMS channel of a seismometer and threshold on this channel. In this instance the best witness was found to be ITMY Z 0.03-0.1Hz')
parser.add_argument('-s', '--start', type=int, required=True, help='start time')
parser.add_argument('-e', '--end', type=int, required=True, help='end time')
parser.add_argument('-c', '--channel', type=str, default='L1:ISI-GND_STS_ITMY_Z_BLRMS_30M_100M.rms', help='channel name (optional)')
parser.add_argument('-sf', '--science', type=str, default='L1:DMT-ANALYSIS_READY:1', help='science flag (optional)')
parser.add_argument('-st', '--stride', type=float, default='60', help='Stide for the flag (s) (optional)')

args = parser.parse_args()

# set up channel name for grabbing data
channel = ['%s,m-trend' % args.channel]

# Threshold used to generate this flag
thresh = 190 #nm/s

# set up segment file name
chan = channel[0].replace(':', '_')
segment_file = 'L1_EARTHQUAKE_GT_%s_%s-%s.xml' % (thresh, args.start, abs(args.end-args.start))

# name the DQ flag
optic = channel[0].split('_')[2]
flag_name = 'L1:DCH-EQ_%s_GT_%s:1' % (optic, thresh)

# grab all observing (or whatever is defined) time
active = DataQualityFlag.query_dqsegdb(args.science, args.start, args.end).active

# grab only data for the STS channel in observing time
data = get_timeseries_dict(channel, active, frametype='L1_M')

# find times above threshold
time = [j.times[j > thresh] for j in data[channel[0]]]
times = numpy.concatenate(time)

# put all times above threshold in to segments
segs = segments.segmentlist()
segs.extend([segments.segment(int(t.value), int(t.value)+args.stride) for t in times])
segs = segs.coalesce()

# set up the xml file by making a list of the start and end times of the flag
start_time = []
start_time.extend([t[0] for t in segs])
end_time = []
end_time.extend([t[1] for t in segs])

# put in to dq flag object
flag = DataQualityFlag(flag_name, active=zip(start_time,end_time), known=[[args.start,args.end]])

# write flag to xml
flag.write(segment_file)
