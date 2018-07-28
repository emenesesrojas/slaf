#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Correlates failure events with job events using the job ID as a key.

import sys
import re
import datetime
import time
import matplotlib.pyplot as plt
import os
from math import *

# execution time limit on Titan
EXECUTION_LIMIT=1450

### CLASSES ###

class Job:
	""" This class represents a failed job and its attributes """
	def __init__(self, date, nodes, tasks, wallclockTime, waitTime, execution_time, failure_type):
		self.date = date
		self.nodes = nodes
		self.tasks = tasks
		self.wallclockTime = wallclockTime
		self.waitTime = waitTime
		self.execution_time = execution_time
		self.failure_type = failure_type

### FUNCTIONS ###

def failureJob(fileName, dirName, outputFileName):
	""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	timeFormat = '%m/%d/%y %H:%M %p'
	formatAlt = '%Y-%m-%d %H:%M:%S'
	dayFormat = '%a_%b_%d_%Y'
	count = 0
	missing = 0
	jobs = {}
	cancelled_jobs = 0
	DaysToSearch = []

	# start timer
	startTime = time.clock()
	
	#size of failure file
	with open(fileName) as f:
		lines = len(f.readlines())
	f.close()

	# going through all entries in the file
	with open(fileName) as f:
		next(f)																			# skipping first line (header)
		for line in f:
			# getting jobid and time for each failure
			count = count + 1
			fields = line.split('|')													# separating fields
			jobid = fields[2].strip()													# reading job ib
			dateAndTime = fields[3].strip()												# reading time
			failure_type = fields[4].strip()
			try:
				currentDate = datetime.datetime.strptime(dateAndTime, timeFormat)
			except ValueError:
				try:
					currentDate = datetime.datetime.strptime(dateAndTime, formatAlt)
				except ValueError:					
					print ("ERROR with date ", dateAndTime)
					sys.exit(0)

			DaysToSearch.append(str(currentDate.month).zfill(2) +"/"+ str(currentDate.day).zfill(2))
			
			oneDayBefore = currentDate - datetime.timedelta(days=1)
			DaysToSearch.append(str(oneDayBefore.month).zfill(2)+"/"+str(oneDayBefore.day).zfill(2))
			
			twoDayBefore = currentDate - datetime.timedelta(days=2)
			DaysToSearch.append(str(twoDayBefore.month).zfill(2)+"/"+str(twoDayBefore.day).zfill(2))
			
			oneDayAfter = currentDate + datetime.timedelta(days=1)
			DaysToSearch.append(str(oneDayAfter.month).zfill(2)+"/"+str(oneDayAfter.day).zfill(2))
			
			twoDayAfter = currentDate + datetime.timedelta(days=2)
			DaysToSearch.append(str(twoDayAfter.month).zfill(2)+"/"+str(twoDayAfter.day).zfill(2))

			# looking for the corresponding log file in the MOAB directory
			for fecha in DaysToSearch:	
				jobFileName = dirName + fecha
				
				#for determine if the patch exist and if the file contains data 
				#if os.path.isdir(dirName[:-1]) == False:
				#	continue
				if os.stat(jobFileName).st_size == 0:
					continue
				
				#Progress of excecution
				print ("Progress: %d%%, Failure Analized: %d, Count missing ID: %d, Search on: %s "% (count/lines*100, count, missing, jobFileName),end="\r") 
				sys.stdout.flush()

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
						objEvent = columns[4]
						if len(columns) > 3 and jobid == objid and (objEvent == 'JOBEND' or objEvent == 'JOBCANCEL'):

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
								print ("File: %s, job id: %s, execution time: %f minutes" % (jobFileName[2:], objid, execution_time))
								execution_time = wallclock_req
							flag = True
							DaysToSearch.clear()
							if not jobid in jobs:
								#ORIGINAL jobs[objid] = Job(parts[1], nodes_req, tasks_req, wallclock_req, wait_time, execution_time, failure_type)
								jobs[objid] = Job(jobFileName[-5:], nodes_req, tasks_req, wallclock_req, wait_time, execution_time, failure_type)
							break	

					if not flag:
						missing = missing + 1
	
		# stop timer
		finishTime = time.clock()

		# creating output file
		outputFile = open(outputFileName, 'w')
		outputFile.write("#jobid\tdate\tnodes\ttasks\twallclockTime\twaitTime\texecutionTime\n")
		for key in jobs.keys():
			outputFile.write("%s\t%s\t%d\t%d\t%d\t%f\t%f\t%s\n" % (key, jobs[key].date, jobs[key].nodes, jobs[key].tasks, jobs[key].wallclockTime, jobs[key].waitTime,jobs[key].execution_time,jobs[key].failure_type))
		outputFile.close()
	
		# printing summary
		print ("\nSUMMARY:\n\t%d failures analyzed \n\t%d job ids missing \n\t%.2f %% correlation reliability\n\t%.3f seconds execution time" % (count, missing, (count-missing)/float(count)*100.0, finishTime-startTime))
	
	return

### MAIN CODE ###
if len(sys.argv) >= 4:
	fileName = sys.argv[1]
	dirName = sys.argv[2]
	outputFileName = sys.argv[3]
	failureJob(fileName, dirName, outputFileName)
else:
	print ("ERROR, usage: %s <file> <directory> <output file>" % sys.argv[0])
	print ("<file>: failure log file")
	print ("<directory>: MOAB logs directory")
	print ("<output file>: file name to output failed-job information")
	sys.exit(0)

