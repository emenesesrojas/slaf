#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Extracts information about jobs from MOAB logs.
# Date: 04/04/15

import sys
import re
import datetime
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from math import *

### FUNCTIONS ###

def init_tables(hour_table, day_table, month_table):
	""" Initializes tables """
	hour_table['00'] = 0
	hour_table['01'] = 0
	hour_table['02'] = 0
	hour_table['03'] = 0
	hour_table['04'] = 0
	hour_table['05'] = 0
	hour_table['06'] = 0
	hour_table['07'] = 0
	hour_table['08'] = 0
	hour_table['09'] = 0
	hour_table['10'] = 0
	hour_table['11'] = 0
	hour_table['12'] = 0
	hour_table['13'] = 0
	hour_table['14'] = 0
	hour_table['15'] = 0
	hour_table['16'] = 0
	hour_table['17'] = 0
	hour_table['18'] = 0
	hour_table['19'] = 0
	hour_table['20'] = 0
	hour_table['21'] = 0
	hour_table['22'] = 0
	hour_table['23'] = 0
	day_table['Sun'] = 0
	day_table['Mon'] = 0
	day_table['Tue'] = 0
	day_table['Wed'] = 0
	day_table['Thu'] = 0
	day_table['Fri'] = 0
	day_table['Sat'] = 0
	month_table['Jan'] = 0
	month_table['Feb'] = 0
	month_table['Mar'] = 0
	month_table['Apr'] = 0
	month_table['May'] = 0
	month_table['Jun'] = 0
	month_table['Jul'] = 0
	month_table['Aug'] = 0
	month_table['Sep'] = 0
	month_table['Oct'] = 0
	month_table['Nov'] = 0
	month_table['Dec'] = 0

def generate(dir_name, output_dir_name):
	""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	file_count = 0
	job_count = 0
	hour_table = {}
	day_table = {}
	month_table = {}

	init_tables(hour_table,day_table,month_table)

	# start timer
	startTime = time.clock()

	# going through all files in directory
	for file_name in os.listdir(dir_name):
		file_count = file_count + 1

		print "\rAnalyzing file %s" % file_name,
		sys.stdout.flush()

		# getting day and month
		parts = file_name.split('.')
		day = parts[1].split('_')[0]
		month = parts[1].split('_')[1]

		job_file_name = dir_name + '/' + file_name
		
		with open(job_file_name) as log:
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
				if len(columns) > 3 and objEvent == 'JOBSUBMIT':
					job_count = job_count + 1
					job_time = columns[0]
					hour = job_time.split(':')[0]
#					print "->%s %s %s<-" % (hour,day,month)
					hour_table[hour] = hour_table[hour] + 1
					day_table[day] = day_table[day] + 1
					month_table[month] = month_table[month] + 1

	print "\r                                                           ", 
	
	# creating output file
	output_file_name = output_dir_name + '/' + 'workload_hour_distribution.pdf'
	data = [hour_table['00'],hour_table['01'],hour_table['02'],hour_table['03'],hour_table['04'],hour_table['05'],hour_table['06'],hour_table['07'],hour_table['08'],hour_table['09'],hour_table['10'],hour_table['11'],hour_table['12'],hour_table['13'],hour_table['14'],hour_table['15'],hour_table['16'],hour_table['17'],hour_table['18'],hour_table['19'],hour_table['20'],hour_table['21'],hour_table['22'],hour_table['23'],]
	plt.clf()
	plt.rc('font', family='serif')
	plt.rc('font', serif='Times New Roman')
	plt.rc('font', size=24)
	index = np.arange(24)
	plt.bar(index, data)
	plt.xlabel('Hour of the Day')
	plt.xticks([2.4,6.4,10.4,14.4,18.4,22.4], ['2','6','10','14','18','22'])
	plt.ylabel('Number of Jobs')
	plt.savefig(output_file_name,bbox_inches='tight')
	output_file_name = output_dir_name + '/' + 'workload_hour_distribution.txt'
	output_file_txt = open(output_file_name, 'w')
	output_file_txt.write('#HOUR JOBS\n')
	output_file_txt.write('\n'.join(map(lambda x,y: str(x) + ' ' + str(y), range(24), data)))
	output_file_txt.close()
	
	output_file_name = output_dir_name + '/' + 'workload_day_distribution.pdf'
	data = [day_table['Sun'],day_table['Mon'],day_table['Tue'],day_table['Wed'],day_table['Thu'],day_table['Fri'],day_table['Sat']]
	plt.clf()
	plt.rc('font', family='serif')
	plt.rc('font', serif='Times New Roman')
	plt.rc('font', size=24)
	plt.bar(range(7), data)
	plt.xticks([0.4,1.4,2.4,3.4,4.4,5.4,6.4], ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
	plt.xlabel('Day of the Week')
	plt.ylabel('Number of Jobs')
	plt.savefig(output_file_name,bbox_inches='tight')
	output_file_name = output_dir_name + '/' + 'workload_day_distribution.txt'
	output_file_txt = open(output_file_name, 'w')
	output_file_txt.write('#DAY JOBS\n')
	output_file_txt.write('\n'.join(map(lambda x,y: str(x) + ' ' + str(y), range(7), data)))
	output_file_txt.close()
	
	output_file_name = output_dir_name + '/' + 'workload_month_distribution.pdf'
	data = [month_table['Jan'],month_table['Feb'],month_table['Mar'],month_table['Apr'],month_table['May'],month_table['Jun'],month_table['Jul'],month_table['Aug'],month_table['Sep'],month_table['Oct'],month_table['Nov'],month_table['Dec']]
	plt.clf()
	plt.rc('font', family='serif')
	plt.rc('font', serif='Times New Roman')
	plt.rc('font', size=24)
	plt.bar(range(12), data)
	plt.xticks([0.4,1.4,2.4,3.4,4.4,5.4,6.4,7.4,8.4,9.4,10.4,11.4], ['1','2','3','4','5','6','7','8','9','10','11','12'])
	plt.xlabel('Month of the Year')
	plt.ylabel('Number of Jobs')
	plt.savefig(output_file_name,bbox_inches='tight')
	output_file_name = output_dir_name + '/' + 'workload_month_distribution.txt'
	output_file_txt = open(output_file_name, 'w')
	output_file_txt.write('#MONTH JOBS\n')
	output_file_txt.write('\n'.join(map(lambda x,y: str(x) + ' ' + str(y), range(12), data)))
	output_file_txt.close()
	
	# stop timer
	finishTime = time.clock()

	# printing summary
	print "\nSUMMARY:                                          \n \
	%d files analyzed \n \
	%d jobs analyzed \n \
	%.3f seconds execution time" \
	% (file_count, job_count, finishTime-startTime)
	
	return

### MAIN CODE ###
if len(sys.argv) >= 3:
	dir_name = sys.argv[1]
	output_dir_name = sys.argv[2]
	generate(dir_name, output_dir_name)
else:
	print "ERROR, usage: %s <directory> <output directory>" % sys.argv[0]
	print "<directory>: MOAB logs directory"
	print "<output directory>: directory to output frequency distributions"
	sys.exit(0)

