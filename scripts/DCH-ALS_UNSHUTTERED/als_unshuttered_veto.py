#! /usr/bin/env python

"""Grab data from the ALS X/Y channels and idetify times when left
unshuttered in locked time
"""

from glue import segments
from gwpy.segments import DataQualityFlag
from gwsumm.data import get_timeseries_dict
import argparse
import numpy

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-s', '--start', type=int, required=True, help='start time')
parser.add_argument('-e', '--end', type=int, required=True, help='end time')
parser.add_argument('-ln', '--low-noise', type=str, 
                    default='H1:DMT-GRD_ISC_LOCK_NOMINAL:1', 
                    help='low noise flag (optional)')
parser.add_argument('-t', '--threshold', type=float, default=0.01,
                    help='Threshold to set on ALS channels. This is a +/- '
                         'value (optional)')
parser.add_argument('-st', '--stride', type=float, default=1, 
                    help='Stide for the flag (s) (optional)')

args = parser.parse_args()

# Define the ALS channels needed
channels = ['H1:ALS-X_TR_A_LF_OUT16','H1:ALS-Y_TR_A_LF_OUT16']

# Define the segment file name and flag name
segment_file = 'H1_ALS_UNSHUTTERED_%s-%s.xml' % (args.start, 
                                                 abs(args.end-args.start))
flag_name = 'H1:DCH-ALS_UNSHUTTERED:1'

# Find times when the low noise flag is active
active = DataQualityFlag.query_dqsegdb(args.low_noise, args.start, 
                                       args.end).active

# Grab ALS channel data only during low noise time
als = get_timeseries_dict(channels, active, frametype='H1_R')

# Define empty segment list
segs = segments.segmentlist()

# loop over channels and find times when the timseries of each channel strays
# +/- threshold
for c in channels:

    # Find times when the timeseries > threshold
    time1 = [j.times[j.value > args.threshold] for j in als[c]]
    time1 = numpy.concatenate(time1)
    # Find times when the timeseries < -threshold
    time2 = [j.times[j.value < -1*args.threshold] for j in als[c]]
    time2 = numpy.concatenate(time2)
    # Concatenate the two sets of times
    times = numpy.concatenate([time1.value,time2.value], axis=0)

    # Extend the segment list to include the most recent times when a 
    # channel is above/below threshold band
    segs.extend([segments.segment(int(t), int(t)+args.stride) for t in times])

# Coalesce the segment list 
segs = segs.coalesce()

# Set up the xml file. Here we are making a list of all the start and end 
# times of the segments separately
start_time = []
start_time.extend([t[0] for t in segs])
end_time = []
end_time.extend([t[1] for t in segs])
 
# Put all the times in to a DQ flag and write to xml file
flag = DataQualityFlag(flag_name, active=zip(start_time,end_time), 
                       known=[[args.start,args.end]])
flag.write(segment_file)
