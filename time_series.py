
#!/usr/bin/env python

# University of Pittsburgh
# Center for Simulation and Modeling
# Esteban Meneses
# Date: 03/20/15

import sys
import re
import datetime
import time
import os
import glob
from math import *
import matplotlib as mtl
mtl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss
from collections import defaultdict
import collections
	
def time_series(dir_name, outputFileName):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	file_count = 0
	line_count = 0
	pathFileName = []
	event_day = {}
	event_week_2015 = {}
	event_week_2016 = {}
	
	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
				
	# going through all files in directory
	for file_name in pathFileName:  
		line_count = 0
		#print ("Progress: %d%%, Analyzing file %s, file_count: %d" % (file_count/len(files), file_name, file_count),end="\r")
		#sys.stdout.flush()
		conunt_event = 0
		file_name = dir_name + file_name
		
		with open(file_name) as log:
			line_count += 1
			if line_count == 1:
				next(log)
			for line in log:
				item = line.split("|")
				
				d = item[3][2:-17].strip()+item[3][7:-14].strip()+item[3][10:-11].strip()
				week = datetime.date(int(item[3][2:-17].strip()), int(item[3][7:-14].strip()), int(item[3][10:-11].strip())).isocalendar()[1]
				year = item[3][2:-17].strip()
				
				if d in event_day.keys():
					event_day[d] += 1
				else:
					event_day[d] = 0
				
			
				if week in event_week_2015.keys():
					if year == "2015":
						event_week_2015[week] += 1
				else:
					event_week_2015[week] = 0
					continue
					
				if week in event_week_2016.keys():
					if year == "2016":
						event_week_2016[week] += 1
				else:
					event_week_2016[week] = 0
				
					
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Days')
	plt.ylabel('Count of failures')
	plt.title('Failures by day 2015-2016 ')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	day_sort = collections.OrderedDict(sorted(event_day.items()))
	plt.plot(range(len(event_day)),list(day_sort.values()), 'b-', linewidth=1, label='2015-2016 failures')
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
		
	plt.savefig("PLOT_day.pdf")
    
    
	plt.clf()
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Weeks')
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2015-2016 ')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.xticks(np.arange(0, 54, 2))
	plt.plot(range(len(event_week_2015)),list(event_week_2015.values()), 'b-', linewidth=1, label="2015 failures")
	plt.plot(range(len(event_week_2016)),list(event_week_2016.values()), 'r--', linewidth=1, label="2016 failures")
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("PLOT_two_lines.pdf")
    
	plt.clf()
	plt.xlabel('Weeks')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2015 to 2016 ')
	plt.xticks(np.arange(0, 108, 4))
	plt.plot(range(len(event_week_2015)+len(event_week_2016)),list(event_week_2015.values())+list(event_week_2016.values()), 'b-', linewidth=1, label="2015-2016 failures")
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("PLOT_one_line.pdf")


	return 
	
	
if len(sys.argv) >= 3:
	dirName = sys.argv[1]
	outputFileName = sys.argv[2]
	time_series(dirName, outputFileName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	print ("<directory>: Filter failure directory")
	print ("<output file>: file name to output plot information")
	sys.exit(0)