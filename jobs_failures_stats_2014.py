#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Correlates failure events with job events using the job ID as a key.

import sys
import re
import datetime
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import numpy as np
from math import *
from datetime import date, timedelta, datetime as dt
import calendar as cl

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
def check_string(substring, string):
    if substring in string:
        return True
    return False

def change_month(month):
	if month == "01":
		return "Jan"
	if month == "02":
		return "Feb"
	if month == "03":
		return "Mar"
	if month == "04":
		return "Apr"
	if month == "05":
		return "May"
	if month == "06":
		return "Jun"
	if month == "07":
		return "Jul"
	if month == "08":
		return "Aug"
	if month == "09":
		return "Sep"
	if month == "10":
		return "Oct"
	if month == "11":
		return "Nov"
	if month == "12":
		return "Dec"
	
	
	
def failureJob(fileName, dirName, outputFileName, year):
	""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	timeFormat = '%m/%d/%y %H:%M %p'
	formatAlt = '%Y-%m-%d %H:%M:%S'
	dayFormat = '%a_%b_%d_%Y'
	count = 0
	missing = 0
	fail_found = 0
	jobs = {}
	jobs_time_execution = {}
	bl = 0
	
	jobs_nodes_req = {}
	jobs_node_affected = {}
	jobs_node_failure = []
	jobs_node_req_count = []
	
	cancelled_jobs = 0
	DaysToSearch = []
	
	#initialize array of nodes
	for i in range(7):
		jobs_node_failure.append(0)
		jobs_node_req_count.append(0)
		
	#initialize for count jobs by time
	for i in range(19):
		jobs_time_execution[i] = 0
		jobs_nodes_req[i] = 0
		jobs_node_affected[i] = 0
		
	jobs_time_execution[20] = 0
	jobs_time_execution[30] = 0
	jobs_time_execution[40] = 0
	jobs_time_execution[50] = 0
	jobs_time_execution[100] = 0
	jobs_time_execution[150] = 0
	jobs_time_execution[200] = 0
	jobs_time_execution[250] = 0
	jobs_time_execution[300] = 0
	jobs_time_execution[350] = 0
	jobs_time_execution[400] = 0
	jobs_time_execution[450] = 0
	jobs_time_execution[500] = 0
	jobs_time_execution[550] = 0
	jobs_time_execution[600] = 0
	
	
	jobs_nodes_req[20]  = jobs_node_affected[20]  = 0
	jobs_nodes_req[30]  = jobs_node_affected[30]  = 0
	jobs_nodes_req[40]  = jobs_node_affected[40]  = 0
	jobs_nodes_req[50]  = jobs_node_affected[50]  = 0
	jobs_nodes_req[100] = jobs_node_affected[100] = 0
	jobs_nodes_req[150] = jobs_node_affected[150] = 0
	jobs_nodes_req[200] = jobs_node_affected[200] = 0
	jobs_nodes_req[250] = jobs_node_affected[250] = 0
	jobs_nodes_req[300] = jobs_node_affected[300] = 0
	jobs_nodes_req[350] = jobs_node_affected[350] = 0
	jobs_nodes_req[400] = jobs_node_affected[400] = 0
	jobs_nodes_req[450] = jobs_node_affected[450] = 0
	jobs_nodes_req[500] = jobs_node_affected[500] = 0
	jobs_nodes_req[550] = jobs_node_affected[550] = 0
	jobs_nodes_req[600] = jobs_node_affected[600] = 0
	

	# start timer
	startTime = time.clock()
	
	check_output = open("check_output", 'w')
						
	#size of failure file
	with open(fileName) as f:
		lines = len(f.readlines())
	
	# going through all entries in the file
	with open(fileName) as f:
		next(f)  # skipping first line (header)
		for line in f:
			# getting jobid and time for each failure
			count = count + 1
			fields = line.split('|')													# separating fields
			jobid = fields[2].strip()													# reading job ib
			dateAndTime = fields[3].strip()												# reading time
			failure_type = fields[4].strip()
			description  = fields[6].strip()
			
			nodes = fields[9].strip().split()
			
			try:
				currentDate = datetime.datetime.strptime(dateAndTime, timeFormat)
			except ValueError:
				try:
					currentDate = datetime.datetime.strptime(dateAndTime, formatAlt)
				except ValueError:					
					print ("ERROR with date ", dateAndTime)
					sys.exit(0)
			
			#Day of week
			f = dt.strptime(str(currentDate),formatAlt)
			day_week = cl.day_name[f.weekday()] 
			m = str(currentDate.month).zfill(2)
			d = str(currentDate.day).zfill(2)
			f = 	"events." + day_week[:3] +"_"+ change_month(m) + "_" + d + "_2014" 
			DaysToSearch.append(f)
			
			oneDayBefore = currentDate - datetime.timedelta(days=1)
			f = dt.strptime(str(oneDayBefore),formatAlt)
			day_week = cl.day_name[f.weekday()] 
			m = str(oneDayBefore.month).zfill(2)
			d = str(oneDayBefore.day).zfill(2)
			f = "events." + day_week[:3] +"_"+ change_month(m) + "_" + d + "_2014" 
			DaysToSearch.append(f)
			
			twoDayBefore = currentDate - datetime.timedelta(days=2)
			f = dt.strptime(str(twoDayBefore),formatAlt)
			day_week = cl.day_name[f.weekday()] 
			m = str(twoDayBefore.month).zfill(2)
			d = str(twoDayBefore.day).zfill(2)
			f = "events." + day_week[:3] +"_"+ change_month(m) + "_" + d + "_2014" 
			DaysToSearch.append(f)
			
			oneDayAfter = currentDate + datetime.timedelta(days=1)
			f = dt.strptime(str(oneDayAfter),formatAlt)
			day_week = cl.day_name[f.weekday()] 
			m = str(oneDayAfter.month).zfill(2)
			d = str(oneDayAfter.day).zfill(2)
			f = "events." + day_week[:3] +"_"+ change_month(m) + "_" + d + "_2014" 
			DaysToSearch.append(f)
			
			twoDayAfter = currentDate + datetime.timedelta(days=2)
			f = dt.strptime(str(twoDayAfter),formatAlt)
			day_week = cl.day_name[f.weekday()] 
			m = str(twoDayAfter.month).zfill(2)
			d = str(twoDayAfter.day).zfill(2)
			f = "events." + day_week[:3] +"_"+ change_month(m) + "_" + d + "_2014" 
			DaysToSearch.append(f)
			
			flag = False
			# looking for the corresponding log file in the MOAB directory
			for fecha in DaysToSearch:	
				if flag == False:
					jobFileName = dirName + fecha
					
					
					#for determine if the patch exist and if the file contains data 
						# if os.path.isdir(jobFileName.strip()) == False:
							# print("Patch error")
							# continue
					if os.stat(jobFileName).st_size == 0:
						print("File error")
						continue				
					#Progress of excecution
					print ("Progress: %d%%, Failure Analized: %d, Failure found: %d, Count missing ID: %d, Search on: %s "% (count/lines*100, count,fail_found, missing, jobFileName),end="\r")
					with open(jobFileName) as log:
						if flag == False:
							for event in log:
								
								# if not event.strip():
									# continue
									
								columns = event.split()
								
								if len(columns) < 6:
									continue
									
								eventType = columns[2]
								
								objid = columns[3]
								objEvent = columns[4]
								if len(columns) < 6 or eventType != 'job':# continue if empty event # continue if not job event
									continue														
								if jobid == objid and columns[4] == 'JOBEND':  
									###########################################################				
									columns_check = event.split()
												
									try:
										dispatch_time = int(columns[13])
									except ValueError:
										dispatch_time = 0
										print("\nAsigned value 0 to dispatch_time")
									
									try:
										start_time = int(columns[14]) 
									except ValueError:
										start_time = 0
										print("\nAsigned value 0 to start_time")
										
									if(dispatch_time == 0):
										if(start_time == 0):
											cancelled_jobs = cancelled_jobs + 1
											continue
										else:
											dispatch_time = start_time
											
									# checking number of requested nodes
									try:
										nodes_req = int(columns[5])
										#print("Nodes req: "+str(nodes_req))
									except ValueError:
										nodes_req = 0
										print("\nAsigned value 0 to nodes_req")
										
									try:
										tasks_req = int(columns[6])
									except ValueError:
										tasks_req = 0
										print("\nAsigned value 0 to tasks_req")
										
									try:
										tasks_per_node = int(columns[25])
										#print("Task per node: "+str(tasks_per_node))
									except ValueError:
										tasks_per_node = 0
										print("\nAsigned value 0 to tasks_per_node")
										
									if(nodes_req == 0):
										if(tasks_per_node == -1 or tasks_per_node == 0):
											nodes_req = int(ceil(tasks_req/16.0))
										else:
											nodes_req = int(ceil(tasks_req/float(tasks_per_node)))
									#print("Nodes req 2: "+str(nodes_req))
									wallclock_req = int(columns[9])/60.0							# transforming wallclock time into minutes
									
									try:
										submit_time = int(columns[12])
									except ValueError:
										submit_time = 0
										print("\nAsigned value 0 to submit_time")
									
									wait_time = (dispatch_time - submit_time)/60.0					# transforming wait time into minutes
									#print("Wait time: "+str(wait_time))
									try:
										completion_time = int(columns[15])
									except ValueError:
										completion_time = 0
										print("\nAsigned value 0 to completetion_time")
									
									if(start_time == 0):
										execution_time = (completion_time - dispatch_time)/60.0
									else:
										execution_time = (completion_time - start_time)/60.0			# transforming execution time into minutes
									
									if int(execution_time) == 0:
										print("entro\nID:"+ jobid + "star t:"+columns[14])
										print("entro\nID:"+ jobid + "complete t:"+columns[15])
										print("Execution: "+ str(execution_time))
										print("Execution R: "+ str(int(execution_time)))
										print("/////////////////////////////////////")
									
									#COUNT NODES REQ BY JOBS
									if nodes_req == 1:
										jobs_node_req_count[0] += 1
									if nodes_req == 2:
										jobs_node_req_count[1] += 1
									if nodes_req == 3:
										jobs_node_req_count[2] += 1
									if nodes_req == 4:
										jobs_node_req_count[3] += 1
									if nodes_req == 5:
										jobs_node_req_count[4] += 1
									if nodes_req == 6:
										jobs_node_req_count[5] += 1
									if nodes_req > 7:
										jobs_node_req_count[6] += 1
									
									#COUNT NODES AFFECTED BY FAILURES JOBS
									nodes_afected_by_failure = int(len(nodes))
									
									if nodes_afected_by_failure == 1:
										jobs_node_failure[0] += 1
									if nodes_afected_by_failure == 2:
										jobs_node_failure[1] += 1
									if nodes_afected_by_failure == 3:
										jobs_node_failure[2] += 1
									if nodes_afected_by_failure == 4:
										jobs_node_failure[3] += 1
									if nodes_afected_by_failure == 5:
										jobs_node_failure[4] += 1
									if nodes_afected_by_failure == 6:
										jobs_node_failure[5] += 1
									if nodes_afected_by_failure > 7:
										jobs_node_failure[6] += 1
									
									#COUNT JOBS BY EXECUTION TIME
									if int(execution_time) in jobs_time_execution:
										jobs_time_execution[int(execution_time)] += 1
									else:
										if int(execution_time) > 19 and int(execution_time) < 30:
											jobs_time_execution[20] += 1
										if int(execution_time) > 29 and int(execution_time) < 40:
											jobs_time_execution[30] += 1
										if int(execution_time) > 39 and int(execution_time) < 50:
											jobs_time_execution[40] += 1
										if int(execution_time) > 49 and int(execution_time) < 100:
											jobs_time_execution[50] += 1
										if int(execution_time) > 99 and int(execution_time) < 150:
											jobs_time_execution[100] += 1
										if int(execution_time) > 149 and int(execution_time) < 200:
											jobs_time_execution[150] += 1	
										if int(execution_time) > 199 and int(execution_time) < 250:
											jobs_time_execution[200] += 1
										if int(execution_time) > 249 and int(execution_time) < 300:
											jobs_time_execution[250] += 1
										if int(execution_time) > 299 and int(execution_time) < 350:
											jobs_time_execution[300] += 1
										if int(execution_time) > 349 and int(execution_time) < 400:
											jobs_time_execution[350] += 1
										if int(execution_time) > 399 and int(execution_time) < 450:
											jobs_time_execution[400] += 1
										if int(execution_time) > 449 and int(execution_time) < 500:
											jobs_time_execution[450] += 1
										if int(execution_time) > 499 and int(execution_time) < 550:
											jobs_time_execution[500] += 1
										if int(execution_time) > 549 and int(execution_time) < 600:
											jobs_time_execution[550] += 1
										if int(execution_time) >= 600:
											jobs_time_execution[600] += 1

										
									if int(execution_time) in jobs_nodes_req:
										jobs_nodes_req[int(execution_time)] += nodes_req
									else:
										if int(execution_time) > 19 and int(execution_time) < 30:
											jobs_nodes_req[20] += nodes_req
										if int(execution_time) > 29 and int(execution_time) < 40:
											jobs_nodes_req[30] += nodes_req
										if int(execution_time) > 39 and int(execution_time) < 50:
											jobs_nodes_req[40] += nodes_req
										if int(execution_time) > 49 and int(execution_time) < 100:
											jobs_nodes_req[50] += nodes_req
										if int(execution_time) > 99 and int(execution_time) < 150:
											jobs_nodes_req[100] += nodes_req
										if int(execution_time) > 149 and int(execution_time) < 200:
											jobs_nodes_req[150] += nodes_req	
										if int(execution_time) > 199 and int(execution_time) < 250:
											jobs_nodes_req[200] += nodes_req
										if int(execution_time) > 249 and int(execution_time) < 300:
											jobs_nodes_req[250] += nodes_req
										if int(execution_time) > 299 and int(execution_time) < 350:
											jobs_nodes_req[300] += nodes_req
										if int(execution_time) > 349 and int(execution_time) < 400:
											jobs_nodes_req[350] += nodes_req
										if int(execution_time) > 399 and int(execution_time) < 450:
											jobs_nodes_req[400] += nodes_req
										if int(execution_time) > 449 and int(execution_time) < 500:
											jobs_nodes_req[450] += nodes_req
										if int(execution_time) > 499 and int(execution_time) < 550:
											jobs_nodes_req[500] += nodes_req
										if int(execution_time) > 549 and int(execution_time) < 600:
											jobs_nodes_req[550] += nodes_req
										if int(execution_time) >= 600:
											jobs_nodes_req[600] += nodes_req
									
									if int(execution_time) in jobs_node_affected:
										jobs_node_affected[int(execution_time)] += int(nodes_afected_by_failure)
									else:
										if int(execution_time) > 19 and int(execution_time) < 30:
											jobs_node_affected[20] += int(nodes_afected_by_failure)
										if int(execution_time) > 29 and int(execution_time) < 40:
											jobs_node_affected[30] += int(nodes_afected_by_failure)
										if int(execution_time) > 39 and int(execution_time) < 50:
											jobs_node_affected[40] += int(nodes_afected_by_failure)
										if int(execution_time) > 49 and int(execution_time) < 100:
											jobs_node_affected[50] += int(nodes_afected_by_failure)
										if int(execution_time) > 99 and int(execution_time) < 150:
											jobs_node_affected[100] += int(nodes_afected_by_failure)
										if int(execution_time) > 149 and int(execution_time) < 200:
											jobs_node_affected[150] += int(nodes_afected_by_failure)	
										if int(execution_time) > 199 and int(execution_time) < 250:
											jobs_node_affected[200] += int(nodes_afected_by_failure)
										if int(execution_time) > 249 and int(execution_time) < 300:
											jobs_node_affected[250] += int(nodes_afected_by_failure)
										if int(execution_time) > 299 and int(execution_time) < 350:
											jobs_node_affected[300] += int(nodes_afected_by_failure)
										if int(execution_time) > 349 and int(execution_time) < 400:
											jobs_node_affected[350] += int(nodes_afected_by_failure)
										if int(execution_time) > 399 and int(execution_time) < 450:
											jobs_node_affected[400] += int(nodes_afected_by_failure)
										if int(execution_time) > 449 and int(execution_time) < 500:
											jobs_node_affected[450] += int(nodes_afected_by_failure)
										if int(execution_time) > 499 and int(execution_time) < 550:
											jobs_node_affected[500] += int(nodes_afected_by_failure)
										if int(execution_time) > 549 and int(execution_time) < 600:
											jobs_node_affected[550] += int(nodes_afected_by_failure)
										if int(execution_time) >= 600:
											jobs_node_affected[600] += int(nodes_afected_by_failure)
																
									
									if(execution_time > EXECUTION_LIMIT):
										print ("--->JOB WITH LONG EXECUTION TIME")
										print ("File: %s, job id: %s, execution time: %f minutes" % (jobFileName[2:], objid, execution_time))
										execution_time = wallclock_req
									flag = True
									fail_found = fail_found + 1
									DaysToSearch.clear()
									#print("Encontrado")
									if not jobid in jobs:
										jobs[objid] = Job(jobFileName[-5:], nodes_req, tasks_req, wallclock_req, wait_time, execution_time, failure_type)
									break
			if not flag:
				missing = missing + 1
				# print ("--------------------------------------")
				# print("Job id: "+jobid)
				# print("Obj id: "+objid)
				# print("data: "+ dateAndTime)
				# print ("--------------------------------------")
				#sys.exit()
		check_output.close()
		# stop timer
		finishTime = time.clock()

		###########################################################################################
		###########################################################################################
		
		#PLOT THE DATA 
		fig = plt.figure()
		fig, axs = plt.subplots(2,2,figsize=(8, 5))
		
		print("\nProcessing plots 1")
		
		data = []
		for key in sorted(jobs_time_execution.keys()):	
			data.append(jobs_time_execution[key])
		
		print(data)
		print("jobs node affected----------------------------------")
		print(jobs_time_execution)
		
		
		axs[0,0].bar(range(0,34,1), data,color=['blue'],width=.5)
		axs[0,0].tick_params(axis = 'x',  labelsize = 6.3)
		axs[0,0].tick_params(axis = 'y',  labelsize = 7)
		axs[0,0].set_xlim(-1,35, auto=False)
		axs[0,0].set_xlabel('Execution Time (Minutes)')
		axs[0,0].set_ylabel('Jobs')
		axs[0,0].set_title('')
		axs[0,0].set_xticklabels(['0','','2','','4','','6','','8','','10','','12','','14','','16','','18','','20+','','40+','','100+','','200+','','300+','','400+','','500+','','600+'],rotation = 45)
		axs[0,0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])
		axs[0,0].legend(edgecolor="black",prop={'size': 7})
		
		#axs[0,0].set_ylim([1,max(jobs_time_execution)])
		
		###########################################################################################
		###########################################################################################
		print("\nProcessing plots 2")
		
		fail_node = []
		for key in sorted(jobs_node_affected.keys()):	
			fail_node.append(jobs_node_affected[key])

		
		node_req = []
		for key in sorted(jobs_nodes_req.keys()):	
			node_req.append(jobs_nodes_req[key])
		
		barWidth = 0.35
		r1 = np.arange(0,34,1)
		r2 = [x + 0.01 + barWidth for x in r1]
	
		axs[0,1].set_xlabel('Execution Time (Minutes)')
		axs[0,1].set_ylabel('Node Count')
		axs[0,1].set_title('')
		ax = plt.gca()
		axs[0,1].bar(r1,fail_node,width=barWidth, label="Failed Nodes",color=['blue'], align="edge",log = True)
		axs[0,1].bar(r2,node_req,width=barWidth, label="Requested Nodes",color=['red'], align="edge", log = True)
		axs[0,1].set_ylim([1,max(node_req)+500])
		
		axs[0,1].tick_params(axis = 'x', labelsize = 6.3)
		axs[0,1].tick_params(axis = 'y',  labelsize = 7)
		
		axs[0,1].set_xlim(-1,35, auto=False)
		axs[0,1].set_xticklabels(['0','','2','','4','','6','','8','','10','','12','','14','','16','','18','','20+','','40+','','100+','','200+','','300+','','400+','','500+','','600+'],rotation = 45)
		axs[0,1].set_xticks([0.3,1.3,2.3,3.3,4.3,5.3,6.3,7.3,8.3,9.3,10.3,11.3,12.3,13.3,14.3,15.3,16.3,17.3,18.3,19.3,20.3,21.3,22.3,23.3,24.3,25.3,26.3,27.3,28.3,29.3,30.3,31.3,32.3,33.3,34.3])
		axs[0,1].legend(edgecolor="black",prop={'size': 8},bbox_to_anchor=(0,1.02,1,0.2), loc="lower center", borderaxespad=0, ncol=2)
		
		plt.subplots_adjust(top=0.92, bottom=0.08, left=0.1, right=0.95, hspace=0.35, wspace=0.25)
		plt.savefig("PLOT_count_jobs_by_time_execution_2014.pdf")
		print("\nPLOT_count_jobs_by_time_execution_2014.pdf>")
		
		plt.clf() 
		fig = plt.figure()
		fig, axs = plt.subplots(2,3,figsize=(15, 8))
		
		print("\nProcessing plots 3")
		print(jobs_node_failure)
		print("------------------------------------------")
		print(jobs_node_req_count)
		
		r1 = np.arange(1,8,1)
		r2 = [x + 0.02 + barWidth for x in r1]
		barWidth = 0.3
		axs[0,0].bar(r1,jobs_node_failure,width=barWidth,label="Failure nodes",color=['blue'],log=True, align="edge")
		axs[0,0].bar(r2,jobs_node_req_count,width=barWidth,label="Requested nodes",color=['red'],log=True,align="edge")
		axs[0,0].set_xlabel('Nodes Affected')
		axs[0,0].set_ylabel('Jobs count')
		axs[0,0].set_title('')
		axs[0,0].set_xticklabels(['1','2','3','4','5','6','>7'])
		axs[0,0].set_xticks([1.15,2.15,3.15,4.15,5.15,6.15,7.15])
		axs[0,0].legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)

		
		plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.95, hspace=0.25, wspace=0.25)
		plt.savefig("PLOT_count_nodes_affected_by_failure_jobs_2014.pdf")
		print("\nPLOT_count_nodes_affected_by_failure_jobs.pdf_2014.pdf>")
		# creating output file
		outputFile = open(outputFileName, 'w')
		outputFile.write("jobid\tdate\tnodes req\ttasks req\twallclockTime\twaitTime\texecutionTime\n")
		for key in jobs.keys():
			outputFile.write("%s\t%s\t%d\t%d\t%d\t%f\t%f\t%s\n" % (key, jobs[key].date, jobs[key].nodes, jobs[key].tasks, jobs[key].wallclockTime, jobs[key].waitTime,jobs[key].execution_time, failure_type))
		outputFile.close()
	
		# printing summary
		print ("\nSUMMARY:\n\t%d failures analyzed \n\t%d job ids missing \n\t%.2f %% correlation reliability\n\t%.3f seconds execution time" % (count, missing, (count-missing)/float(count)*100.0, finishTime-startTime))
	
	return

### MAIN CODE ###
if len(sys.argv) >= 5:
	fileName = sys.argv[1]
	dirName = sys.argv[2]
	outputFileName = sys.argv[3]
	year = sys.argv[4]
	failureJob(fileName, dirName, outputFileName, year)
else:
	print ("ERROR, usage: %s <file> <directory> <output file>" % sys.argv[0])
	print ("<file>: failure log file")
	print ("<directory>: MOAB logs directory")
	print ("<output file>: file name to output failed-job information")
	print ("<year>: year for data processing")
	
	sys.exit(0)

