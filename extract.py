#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Extract failures from the failure log using a list of job ids.

import sys
import re
import datetime
import time
import matplotlib.pyplot as plt
from numpy import *

### FUNCTIONS ###

def extract(failure_file_name, filter_file_name, output_file_name):
	""" Reads the failure log file and extracts only the failures in the filter file """

	# data structures
	job_id_set = {}
	count = 0

	# start timer
	startTime = time.clock()

	# collecting the set of job ids
	with open(filter_file_name) as f:
		for line in f:
			fields = line.split(' ')
			job_id = fields[0].strip()
			job_id_set[job_id] = 1

	# traversing the list of failures
	output_file = open(output_file_name, 'w')
	output_file.write("hostname\tjob_id\tfail_time\tcategory\treason\tdescription\ttext\n")
	with open(failure_file_name) as f:
		next(f)																			# skipping first line (header)
		for line in f:
			fields = line.split('|')													# separating fields
			job_id = fields[2].strip()													# reading job ib
			if(job_id in job_id_set.keys()):
				count = count + 1
				job_id_set.pop(job_id,None)
				output_file.write(line)

	output_file.close()

	# checking for remaining job ids
	for key in job_id_set.keys():
		print key
	
	# stop timer
	finishTime = time.clock()

	print "%d jobs analyzed in %.3f seconds" % (count, finishTime-startTime)	
	return

### MAIN CODE ###
if len(sys.argv) >= 4:
	failure_file_name = sys.argv[1]
	filter_file_name = sys.argv[2]
	output_file_name = sys.argv[3]
	extract(failure_file_name, filter_file_name, output_file_name)
else:
	print "ERROR, usage: %s <failure log file> <filtered failure file> <output file>" % sys.argv[0]
	print "<failure log file>: dumps from Titan's failure database"
	print "<filtered failure file>: file with filtered list of failures"
	print "<output file>: output file with list of failures"

	sys.exit(0)

