
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
from datetime import date, timedelta

def full_dates(year1, year2, dictionary):
	dates_full_year = []
	d1 = date(int(year1), 1, 1)  	# start date
	d2 = date(int(year2), 12, 31)   # end date
	delta = d2 - d1         		# timedelta
	for i in range(delta.days + 1):
		r = str(d1 + timedelta(i))
		f = r[:4]+r[5:7]+r[8:10]
		print(f)
		dictionary[f] = 0
	#print(len(dictionary))
	return dictionary
	
def time_series(dir_name):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	file_count = 0
	line_count = 0
	pathFileName = []
	event_day = {}
	event_week_2015 = {}
	event_week_2016 = {}
	init = False
	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
	
	
	# going through all files in directory
	for file_name in pathFileName:  
		file_count += 1
		line_count = 0
		print("\nPrcessing %d year of 2 - Processing 0 plots of 4"% file_count)
		count_event = 0
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
				
				#initialize all key dates of a range to avoid null dates	
				if init == False:
					event_day = full_dates(2015,2016, event_day).copy()
					init = True
				
				if d in event_day.keys():
					event_day[d] += 1
				#else:
				#	event_day[d] = 0
				
			
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
				
	print("\nPrcessing %d year of 2 - Processing 1 plots of 3"% file_count)	
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Days')
	plt.ylabel('Count of failures')
	plt.title('Failures by day 2015-2016 ')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	day_sort = collections.OrderedDict(sorted(event_day.items()))
	plt.xticks(np.arange(0, 730, 30))
	plt.figure(figsize=(12,4)) 
	

	print(event_day)
	plt.plot(range(len(event_day)),list(day_sort.values()), 'b-', linewidth=1, label='2015-2016 failures')
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
		
	plt.savefig("PLOT_day.pdf")
    
	print("\nPrcessing %d year of 2 - Processing 2 plots of 3"% file_count)	
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
	plt.savefig("PLOT_week_2015_2016.pdf")
	
	print("\nPrcessing %d year of 2 - Processing 3 plots of 3"% file_count)	
	
	plt.clf()
	plt.xlabel('Weeks')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2015 to 2016 ')
	plt.xticks(np.arange(0, 108, 4))
	plt.plot(range(len(event_week_2015)+len(event_week_2016)),list(event_week_2015.values())+list(event_week_2016.values()), 'b-', linewidth=1, label="2015-2016 failures")
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("PLOT_all_years_week.pdf")
	return 
	
	
if len(sys.argv) >= 2:
	dirName = sys.argv[1]
	outputFileName = "" #sys.argv[2]
	time_series(dirName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	sys.exit(0)