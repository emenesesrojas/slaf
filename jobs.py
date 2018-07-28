
#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Extracts information about jobs from MOAB logs.
# Date: 03/20/15

import sys
import re
import datetime
import time
import os
import glob
from math import *

# execution time limit on Titan
EXECUTION_LIMIT=1460

### CLASSES ###

class Job:
	""" This class represents a job and its attributes """
	def __init__(self, date, nodes, tasks, wallclockTime, waitTime, execution_time):
		self.date = date
		self.nodes = nodes
		self.tasks = tasks
		self.wallclockTime = wallclockTime
		self.waitTime = waitTime
		self.execution_time = execution_time

### FUNCTIONS ###

def generate_jobs(dir_name, outputFileName):
	""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	file_count = 0
	job_count = 0
	cancelled_jobs = 0
	jobs = {}
	pathFileName = []

	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
		for d in dirs:
			for f in glob.iglob(os.path.join(path, d, '*')):
				pathFileName.append(f)
				print (f)

				
	# going through all files in directory
	for file_name in pathFileName:  #os.listdir(dir_name):
		file_count = file_count + 1

		print ("\rAnalyzing file %s" % file_name,
		sys.stdout.flush())

		#job_file_name = dir_name + '/' + file_name

		with open(file_name) as log:
			for event in log:
				columns = event.split()
				if len(columns) < 6:
					continue														# continue if empty event
				eventType = columns[2]
				if eventType != 'job':
					continue														# continue if not job event
				objid = columns[3]
				objEvent = columns[4]

				# checking for a valid job entry
				if len(columns) > 3 and objEvent == 'JOBEND':
					job_count = job_count + 1

					# checking cancelled jobs
					dispatch_time = int(columns[13])
					start_time = int(columns[14])
					if(dispatch_time == 0):
						if(start_time == 0):
							cancelled_jobs = cancelled_jobs + 1
							continue
						else:
							dispatch_time = start_time

					# checking number of requested nodes
					nodes_req = int(columns[5])
					tasks_req = int(columns[6])
					tasks_per_node = int(columns[25])
					if(nodes_req == 0):
						if(tasks_per_node == -1 or tasks_per_node == 0):
							nodes_req = int(ceil(tasks_req/16.0))
						else:
							nodes_req = int(ceil(tasks_req/float(tasks_per_node)))
					wallclock_req = int(columns[9])/60.0							# transforming wallclock time into minutes
					submit_time = int(columns[12])
					wait_time = (dispatch_time - submit_time)/60.0					# transforming wait time into minutes
					completion_time = int(columns[15])
					if(start_time == 0):
						execution_time = (completion_time - dispatch_time)/60.0
					else:
						execution_time = (completion_time - start_time)/60.0			# transforming execution time into minutes
					if(execution_time > EXECUTION_LIMIT):
						print ("--->JOB WITH LONG EXECUTION TIME")
						print ("File: %s, job id: %s, execution time: %f minutes" % (file_name, objid, execution_time))
						execution_time = wallclock_req

					jobs[objid] = Job(file_name, nodes_req, tasks_req, wallclock_req, wait_time, execution_time)
	print ("\r                                                           ",)

	# creating output file
	outputFile = open(outputFileName, 'w')
	outputFile.write("#jobid\tdate\tnodes\ttasks\twallclockTime\twaitTime\texecutionTime\n")
	for key in jobs.keys():
		outputFile.write("%s\t%s\t%d\t%d\t%d\t%f\t%f\n" % (key, jobs[key].date, jobs[key].nodes, jobs[key].tasks, jobs[key].wallclockTime, jobs[key].waitTime,jobs[key].execution_time))
	outputFile.close()

	# stop timer
	finishTime = time.clock()

	# printing summary
	print ("\nSUMMARY:                                          \n \
	%d files analyzed \n \
	%d jobs analyzed \n \
	%d cancelled jobs \n \
	%.3f seconds execution time" \
	% (file_count, job_count, cancelled_jobs, finishTime-startTime))

	return

### MAIN CODE ###
if len(sys.argv) >= 3:
	dirName = sys.argv[1]
	outputFileName = sys.argv[2]
	generate_jobs(dirName, outputFileName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	print ("<directory>: MOAB logs directory")
	print ("<output file>: file name to output job information")
	sys.exit(0)

