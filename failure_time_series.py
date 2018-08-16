
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

def init_tables(event_day, event_week_2015, event_week_2016):
	""" Initializes tables """
	event_day['00'] = 0
	event_day['01'] = 0
	event_day['02'] = 0
	event_day['03'] = 0
	event_day['04'] = 0
	event_day['05'] = 0
	event_day['06'] = 0
	event_day['07'] = 0
	event_day['08'] = 0
	event_day['09'] = 0
	event_day['10'] = 0
	event_day['11'] = 0
	event_day['12'] = 0
	event_day['13'] = 0
	event_day['14'] = 0
	event_day['15'] = 0
	event_day['16'] = 0
	event_day['17'] = 0
	event_day['18'] = 0
	event_day['19'] = 0
	event_day['20'] = 0
	event_day['21'] = 0
	event_day['22'] = 0
	event_day['23'] = 0
	event_week_2015[1] = 0
	event_week_2015[2] = 0
	event_week_2015[3] = 0
	event_week_2015[4] = 0
	event_week_2015[5] = 0
	event_week_2015[6] = 0
	event_week_2015[7] = 0
	event_week_2015[8] = 0
	event_week_2015[9] = 0
	event_week_2015[10] = 0
	event_week_2015[11] = 0
	event_week_2015[12] = 0
	event_week_2015[13] = 0
	event_week_2015[14] = 0
	event_week_2015[15] = 0
	event_week_2015[16] = 0
	event_week_2015[17] = 0
	event_week_2015[18] = 0
	event_week_2015[19] = 0
	event_week_2015[20] = 0
	event_week_2015[21] = 0
	event_week_2015[22] = 0
	event_week_2015[23] = 0
	event_week_2015[24] = 0
	event_week_2015[25] = 0
	event_week_2015[26] = 0
	event_week_2015[27] = 0
	event_week_2015[28] = 0
	event_week_2015[29] = 0
	event_week_2015[30] = 0
	event_week_2015[31] = 0
	event_week_2015[32] = 0
	event_week_2015[33] = 0
	event_week_2015[34] = 0
	event_week_2015[35] = 0
	event_week_2015[36] = 0
	event_week_2015[37] = 0
	event_week_2015[38] = 0
	event_week_2015[39] = 0
	event_week_2015[40] = 0
	event_week_2015[41] = 0
	event_week_2015[42] = 0
	event_week_2015[43] = 0
	event_week_2015[44] = 0
	event_week_2015[45] = 0
	event_week_2015[46] = 0
	event_week_2015[47] = 0
	event_week_2015[48] = 0
	event_week_2015[49] = 0
	event_week_2015[50] = 0
	event_week_2015[51] = 0
	event_week_2015[52] = 0
	event_week_2016[1] = 0
	event_week_2016[2] = 0
	event_week_2016[3] = 0
	event_week_2016[4] = 0
	event_week_2016[5] = 0
	event_week_2016[6] = 0
	event_week_2016[7] = 0
	event_week_2016[8] = 0
	event_week_2016[9] = 0
	event_week_2016[10] = 0
	event_week_2016[11] = 0
	event_week_2016[12] = 0
	event_week_2016[13] = 0
	event_week_2016[14] = 0
	event_week_2016[15] = 0
	event_week_2016[16] = 0
	event_week_2016[17] = 0
	event_week_2016[18] = 0
	event_week_2016[19] = 0
	event_week_2016[20] = 0
	event_week_2016[21] = 0
	event_week_2016[22] = 0
	event_week_2016[23] = 0
	event_week_2016[24] = 0
	event_week_2016[25] = 0
	event_week_2016[26] = 0
	event_week_2016[27] = 0
	event_week_2016[28] = 0
	event_week_2016[29] = 0
	event_week_2016[30] = 0
	event_week_2016[31] = 0
	event_week_2016[32] = 0
	event_week_2016[33] = 0
	event_week_2016[34] = 0
	event_week_2016[35] = 0
	event_week_2016[36] = 0
	event_week_2016[37] = 0
	event_week_2016[38] = 0
	event_week_2016[39] = 0
	event_week_2016[40] = 0
	event_week_2016[41] = 0
	event_week_2016[42] = 0
	event_week_2016[43] = 0
	event_week_2016[44] = 0
	event_week_2016[45] = 0
	event_week_2016[46] = 0
	event_week_2016[47] = 0
	event_week_2016[48] = 0
	event_week_2016[49] = 0
	event_week_2016[50] = 0
	event_week_2016[51] = 0
	event_week_2016[52] = 0

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
	
	
	init_tables(event_day,event_week_2015,event_week_2016)
		
	
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
						continue
				#else:
					#event_week_2015[week] = 0
					#continue
				
				if week in event_week_2016.keys():
					if year == "2016":
						event_week_2016[week] += 1
						
				#else:
				#	event_week_2016[week] = 0
				
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
	

	#print(event_week_2016.values())
	
	plt.plot(range(len(event_day)),list(day_sort.values()), 'b-', linewidth=1, label='2015-2016 failures')
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
		
	plt.savefig("PLOT_day_2015_2016.pdf")
	print("\nPlot in file: <PLOT_day_2015_2016.pdf>")

 
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
	print("\nPlot in file: <PLOT_week_2015_2016.pdf>")

	
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
	print("\nPlot in file: <PLOT_all_years_week.pdf>")
	
	return 
	
	
if len(sys.argv) >= 2:
	dirName = sys.argv[1]
	outputFileName = "" #sys.argv[2]
	time_series(dirName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	sys.exit(0)