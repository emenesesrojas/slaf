#!/usr/bin/env python

# Costa Rica High Technology Center (CeNAT)
# Advanced Computing Laboratory
# Esteban Meneses, PhD (esteban.meneses@acm.org)
# Correlates failure events with job events using the job ID as a key.

import sys
import re
import datetime
import time
import os

### FUNCTIONS ###

def correlateFailureJob(fileName, dirName, reportName):
	""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	timeFormat = '%m/%d/%y %H:%M %p'
	formatAlt = '%Y-%m-%d %H:%M:%S'
	dayFormat = '%a_%b_%d_%Y'
	count = 0
	missing = 0

	# open output file
	outputFile = open(reportName, 'w')

	# start timer
	startTime = time.clock()

	# going through all entries in the file
	with open(fileName) as f:
		next(f)																			# skipping first line (header)
		for line in f:

			# getting jobid and time for each failure
			count = count + 1
			fields = line.split('|')													# separating fields
			jobid = fields[2].strip()													# reading job ib
			dateAndTime = fields[3].strip()												# reading time
			try:
				currentDate = datetime.datetime.strptime(dateAndTime, timeFormat)
			except ValueError:
				try:
					currentDate = datetime.datetime.strptime(dateAndTime, formatAlt)
				except ValueError:					
					print("ERROR with date %s in line %s" % (dateAndTime,line))
					sys.exit(0)

			print("\r%d failures analyzed" % (count), end="")
			sys.stdout.flush()

			# looking for the corresponding log file in the MOAB directory
			jobFileName = dirName + "/events." + currentDate.strftime(dayFormat) 
			with open(jobFileName) as log:
				flag = False
				next(log)
				for event in log:
					columns = event.split()
					if len(columns) < 6:
						continue														# continue if empty event
					eventType = columns[2]
					if eventType != 'job':
						continue														# continue if not job event
					objid = columns[3]
					event_type = columns[4]
					nodes = columns[5]
					if len(columns) > 3 and jobid == objid and (event_type == 'JOBEND' or event_type == 'JOBCANCEL'):
						flag = True
						break	
				if not flag:
					outputFile.write("Job ID %s not found in MOAB logs\n" % (jobid))
					missing = missing + 1
	
		# close output file
		outputFile.close()

		# stop timer
		finishTime = time.clock()
	
		# printing summary
		print("\nSUMMARY:\n\t%d failures analyzed \n\t%d job ids missing \n\t%.2f %% correlation reliability\n\t%.3f seconds execution time \nReport in file %s" % (count, missing, (count-missing)/float(count)*100.0, finishTime-startTime, reportName))
	
	return

### MAIN CODE ###
if len(sys.argv) >= 3:
	fileName = sys.argv[1]
	dirName = sys.argv[2]
	if len(sys.argv) == 4:
		reportName = sys.argv[3]
	else:
		reportName = 'log.txt'
	correlateFailureJob(fileName, dirName, reportName)
else:
	print("ERROR, usage: %s <file> <directory> [<report>]\n<file>: failure log file\n<directory>: MOAB logs directory\n<report>: output file with stats about the analysis; by default it is named log.txt" % sys.argv[0])
	sys.exit(0)

