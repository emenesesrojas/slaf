
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
	
def init_tables(event_day_hard,event_day_soft,event_week_hard_2015,event_week_soft_2015,event_week_hard_2016,event_week_soft_2016):
	""" Initializes tables """
	event_day_hard['00'] = 0
	event_day_hard['01'] = 0
	event_day_hard['02'] = 0
	event_day_hard['03'] = 0
	event_day_hard['04'] = 0
	event_day_hard['05'] = 0
	event_day_hard['06'] = 0
	event_day_hard['07'] = 0
	event_day_hard['08'] = 0
	event_day_hard['09'] = 0
	event_day_hard['10'] = 0
	event_day_hard['11'] = 0
	event_day_hard['12'] = 0
	event_day_hard['13'] = 0
	event_day_hard['14'] = 0
	event_day_hard['15'] = 0
	event_day_hard['16'] = 0
	event_day_hard['17'] = 0
	event_day_hard['18'] = 0
	event_day_hard['19'] = 0
	event_day_hard['20'] = 0
	event_day_hard['21'] = 0
	event_day_hard['22'] = 0
	event_day_hard['23'] = 0
	event_day_soft['00'] = 0
	event_day_soft['01'] = 0
	event_day_soft['02'] = 0
	event_day_soft['03'] = 0
	event_day_soft['04'] = 0
	event_day_soft['05'] = 0
	event_day_soft['06'] = 0
	event_day_soft['07'] = 0
	event_day_soft['08'] = 0
	event_day_soft['09'] = 0
	event_day_soft['10'] = 0
	event_day_soft['11'] = 0
	event_day_soft['12'] = 0
	event_day_soft['13'] = 0
	event_day_soft['14'] = 0
	event_day_soft['15'] = 0
	event_day_soft['16'] = 0
	event_day_soft['17'] = 0
	event_day_soft['18'] = 0
	event_day_soft['19'] = 0
	event_day_soft['20'] = 0
	event_day_soft['21'] = 0
	event_day_soft['22'] = 0
	event_day_soft['23'] = 0

	event_week_hard_2015[1] = 0
	event_week_hard_2015[2] = 0
	event_week_hard_2015[3] = 0
	event_week_hard_2015[4] = 0
	event_week_hard_2015[5] = 0
	event_week_hard_2015[6] = 0
	event_week_hard_2015[7] = 0
	event_week_hard_2015[8] = 0
	event_week_hard_2015[9] = 0
	event_week_hard_2015[10] = 0
	event_week_hard_2015[11] = 0
	event_week_hard_2015[12] = 0
	event_week_hard_2015[13] = 0
	event_week_hard_2015[14] = 0
	event_week_hard_2015[15] = 0
	event_week_hard_2015[16] = 0
	event_week_hard_2015[17] = 0
	event_week_hard_2015[18] = 0
	event_week_hard_2015[19] = 0
	event_week_hard_2015[20] = 0
	event_week_hard_2015[21] = 0
	event_week_hard_2015[22] = 0
	event_week_hard_2015[23] = 0
	event_week_hard_2015[24] = 0
	event_week_hard_2015[25] = 0
	event_week_hard_2015[26] = 0
	event_week_hard_2015[27] = 0
	event_week_hard_2015[28] = 0
	event_week_hard_2015[29] = 0
	event_week_hard_2015[30] = 0
	event_week_hard_2015[31] = 0
	event_week_hard_2015[32] = 0
	event_week_hard_2015[33] = 0
	event_week_hard_2015[34] = 0
	event_week_hard_2015[35] = 0
	event_week_hard_2015[36] = 0
	event_week_hard_2015[37] = 0
	event_week_hard_2015[38] = 0
	event_week_hard_2015[39] = 0
	event_week_hard_2015[40] = 0
	event_week_hard_2015[41] = 0
	event_week_hard_2015[42] = 0
	event_week_hard_2015[43] = 0
	event_week_hard_2015[44] = 0
	event_week_hard_2015[45] = 0
	event_week_hard_2015[46] = 0
	event_week_hard_2015[47] = 0
	event_week_hard_2015[48] = 0
	event_week_hard_2015[49] = 0
	event_week_hard_2015[50] = 0
	event_week_hard_2015[51] = 0
	event_week_hard_2015[52] = 0
	event_week_hard_2016[1] = 0
	event_week_hard_2016[2] = 0
	event_week_hard_2016[3] = 0
	event_week_hard_2016[4] = 0
	event_week_hard_2016[5] = 0
	event_week_hard_2016[6] = 0
	event_week_hard_2016[7] = 0
	event_week_hard_2016[8] = 0
	event_week_hard_2016[9] = 0
	event_week_hard_2016[10] = 0
	event_week_hard_2016[11] = 0
	event_week_hard_2016[12] = 0
	event_week_hard_2016[13] = 0
	event_week_hard_2016[14] = 0
	event_week_hard_2016[15] = 0
	event_week_hard_2016[16] = 0
	event_week_hard_2016[17] = 0
	event_week_hard_2016[18] = 0
	event_week_hard_2016[19] = 0
	event_week_hard_2016[20] = 0
	event_week_hard_2016[21] = 0
	event_week_hard_2016[22] = 0
	event_week_hard_2016[23] = 0
	event_week_hard_2016[24] = 0
	event_week_hard_2016[25] = 0
	event_week_hard_2016[26] = 0
	event_week_hard_2016[27] = 0
	event_week_hard_2016[28] = 0
	event_week_hard_2016[29] = 0
	event_week_hard_2016[30] = 0
	event_week_hard_2016[31] = 0
	event_week_hard_2016[32] = 0
	event_week_hard_2016[33] = 0
	event_week_hard_2016[34] = 0
	event_week_hard_2016[35] = 0
	event_week_hard_2016[36] = 0
	event_week_hard_2016[37] = 0
	event_week_hard_2016[38] = 0
	event_week_hard_2016[39] = 0
	event_week_hard_2016[40] = 0
	event_week_hard_2016[41] = 0
	event_week_hard_2016[42] = 0
	event_week_hard_2016[43] = 0
	event_week_hard_2016[44] = 0
	event_week_hard_2016[45] = 0
	event_week_hard_2016[46] = 0
	event_week_hard_2016[47] = 0
	event_week_hard_2016[48] = 0
	event_week_hard_2016[49] = 0
	event_week_hard_2016[50] = 0
	event_week_hard_2016[51] = 0
	event_week_hard_2016[52] = 0
	event_week_soft_2015[1] = 0
	event_week_soft_2015[2] = 0
	event_week_soft_2015[3] = 0
	event_week_soft_2015[4] = 0
	event_week_soft_2015[5] = 0
	event_week_soft_2015[6] = 0
	event_week_soft_2015[7] = 0
	event_week_soft_2015[8] = 0
	event_week_soft_2015[9] = 0
	event_week_soft_2015[10] = 0
	event_week_soft_2015[11] = 0
	event_week_soft_2015[12] = 0
	event_week_soft_2015[13] = 0
	event_week_soft_2015[14] = 0
	event_week_soft_2015[15] = 0
	event_week_soft_2015[16] = 0
	event_week_soft_2015[17] = 0
	event_week_soft_2015[18] = 0
	event_week_soft_2015[19] = 0
	event_week_soft_2015[20] = 0
	event_week_soft_2015[21] = 0
	event_week_soft_2015[22] = 0
	event_week_soft_2015[23] = 0
	event_week_soft_2015[24] = 0
	event_week_soft_2015[25] = 0
	event_week_soft_2015[26] = 0
	event_week_soft_2015[27] = 0
	event_week_soft_2015[28] = 0
	event_week_soft_2015[29] = 0
	event_week_soft_2015[30] = 0
	event_week_soft_2015[31] = 0
	event_week_soft_2015[32] = 0
	event_week_soft_2015[33] = 0
	event_week_soft_2015[34] = 0
	event_week_soft_2015[35] = 0
	event_week_soft_2015[36] = 0
	event_week_soft_2015[37] = 0
	event_week_soft_2015[38] = 0
	event_week_soft_2015[39] = 0
	event_week_soft_2015[40] = 0
	event_week_soft_2015[41] = 0
	event_week_soft_2015[42] = 0
	event_week_soft_2015[43] = 0
	event_week_soft_2015[44] = 0
	event_week_soft_2015[45] = 0
	event_week_soft_2015[46] = 0
	event_week_soft_2015[47] = 0
	event_week_soft_2015[48] = 0
	event_week_soft_2015[49] = 0
	event_week_soft_2015[50] = 0
	event_week_soft_2015[51] = 0
	event_week_soft_2015[52] = 0
	event_week_soft_2016[1] = 0
	event_week_soft_2016[2] = 0
	event_week_soft_2016[3] = 0
	event_week_soft_2016[4] = 0
	event_week_soft_2016[5] = 0
	event_week_soft_2016[6] = 0
	event_week_soft_2016[7] = 0
	event_week_soft_2016[8] = 0
	event_week_soft_2016[9] = 0
	event_week_soft_2016[10] = 0
	event_week_soft_2016[11] = 0
	event_week_soft_2016[12] = 0
	event_week_soft_2016[13] = 0
	event_week_soft_2016[14] = 0
	event_week_soft_2016[15] = 0
	event_week_soft_2016[16] = 0
	event_week_soft_2016[17] = 0
	event_week_soft_2016[18] = 0
	event_week_soft_2016[19] = 0
	event_week_soft_2016[20] = 0
	event_week_soft_2016[21] = 0
	event_week_soft_2016[22] = 0
	event_week_soft_2016[23] = 0
	event_week_soft_2016[24] = 0
	event_week_soft_2016[25] = 0
	event_week_soft_2016[26] = 0
	event_week_soft_2016[27] = 0
	event_week_soft_2016[28] = 0
	event_week_soft_2016[29] = 0
	event_week_soft_2016[30] = 0
	event_week_soft_2016[31] = 0
	event_week_soft_2016[32] = 0
	event_week_soft_2016[33] = 0
	event_week_soft_2016[34] = 0
	event_week_soft_2016[35] = 0
	event_week_soft_2016[36] = 0
	event_week_soft_2016[37] = 0
	event_week_soft_2016[38] = 0
	event_week_soft_2016[39] = 0
	event_week_soft_2016[40] = 0
	event_week_soft_2016[41] = 0
	event_week_soft_2016[42] = 0
	event_week_soft_2016[43] = 0
	event_week_soft_2016[44] = 0
	event_week_soft_2016[45] = 0
	event_week_soft_2016[46] = 0
	event_week_soft_2016[47] = 0
	event_week_soft_2016[48] = 0
	event_week_soft_2016[49] = 0
	event_week_soft_2016[50] = 0
	event_week_soft_2016[51] = 0
	event_week_soft_2016[52] = 0

def time_series(dir_name, outputFileName):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	file_count = 0
	line_count = 0
	pathFileName = []
	event_day_hard = {}
	event_day_soft = {}
	event_week_hard_2015 = {}
	event_week_soft_2015 = {}
	event_week_hard_2016 = {}
	event_week_soft_2016 = {}
	
	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
				
	init_tables(event_day_hard,event_day_soft,event_week_hard_2015,event_week_soft_2015,event_week_hard_2016,event_week_soft_2016)

	# going through all files in directory
	for file_name in pathFileName:  
		file_count += 1
		line_count = 0
		print("\nPrcessing %d year of 2 - Processing 0 plots of 4"% file_count)
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
				category = item[4].strip()
				
				#############################################################
				#DAY
				if d in event_day_hard.keys():
					if category == "hardware":
						event_day_hard[d] += 1
				#else:
				#	event_day_hard[d] = 0
				
				if d in event_day_soft.keys():
					if category == "software":
						event_day_soft[d] += 1
				#else:
				#	event_day_soft[d] = 0
					
				#############################################################
				#WEEK HARDWARE YEAR
				if week in event_week_hard_2015.keys():
					if year == "2015":
						if category == "hardware":
							event_week_hard_2015[week] += 1
						if category == "software":
							event_week_soft_2015[week] += 1
						continue
				#else:
				#	event_week_hard_2015[week] = 0
				#	event_week_soft_2015[week] = 0
				#	continue
					
				#WEEK SOFTWARE YEAR
				if week in event_week_soft_2016.keys():
					if year == "2016":
						if category == "hardware":
							event_week_hard_2016[week] += 1
						if category == "software":
							event_week_soft_2016[week] += 1
				#else:
				#	event_week_soft_2016[week] = 0
				#	event_week_hard_2016[week] = 0
	
	print("\nPrcessing %d year of 2 - Processing 1 plots of 4"% file_count)			
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Days')
	plt.ylabel('Count of failures')
	plt.title('Failures by day 2015-2016 ')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	
	day_soft_sort = collections.OrderedDict(sorted(event_day_soft.items()))
	day_hard_sort = collections.OrderedDict(sorted(event_day_hard.items()))
	plt.plot(range(len(event_day_soft)),list(day_soft_sort.values()), 'b-', linewidth=1, label='2015-2016 software failures ')
	plt.plot(range(len(event_day_hard)),list(day_hard_sort.values()), 'r-', linewidth=1, label='2015-2016 hardware failures')
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("PLOT_day_allyear_category.pdf")
	print("\nPlot in file: <PLOT_day_allyear_category.pdf>")
	
	print("\nPrcessing %d year of 2 - Processing 2 plots of 4"% file_count)
		
	plt.clf()
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Weeks')
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2015')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.xticks(np.arange(0, 54, 2))
	plt.plot(range(len(event_week_soft_2015)),list(event_week_soft_2015.values()), 'b-', linewidth=1, label="2015 Software failures")
	plt.plot(range(len(event_week_hard_2015)),list(event_week_hard_2015.values()), 'r--', linewidth=1, label="2015 Hardware failures")
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("CATEGORY_PLOT_week_2015_lines.pdf")
	print("\nPlot in file: <CATEGORY_PLOT_week_2015_lines.pdf>")
	
	print("\nPrcessing %d year of 2 - Processing 3 plots of 4"% file_count)
	plt.clf()
	plt.style.use('seaborn-whitegrid')	
	plt.xlabel('Weeks')
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2016 ')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.xticks(np.arange(0, 54, 2))
	plt.plot(range(len(event_week_soft_2016)),list(event_week_soft_2016.values()), 'b-', linewidth=1, label="2016 Software failures")
	plt.plot(range(len(event_week_hard_2016)),list(event_week_hard_2016.values()), 'r--', linewidth=1, label="2016 Hardware failures")
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("CATEGORY_PLOT_week_2016_lines.pdf")
	print("\nPlot in file: <CATEGORY_PLOT_week_2016_lines.pdf>")

	print("ERROR------------------------------------------------------------------------------------------------------------")
	print("\nPrcessing %d year of 2 - Processing 4 plots of 4"% file_count)
	plt.clf()
	plt.xlabel('Weeks')
	ax = plt.gca()
	ax.tick_params(axis = 'x', which = 'major', labelsize = 6)
	plt.ylabel('Count of failures')
	plt.title('Failures by week 2015 to 2016 ')
	plt.xticks(np.arange(0, 108, 4))
	plt.plot(range(len(event_week_soft_2015)+len(event_week_soft_2016)),list(event_week_soft_2015.values())+list(event_week_soft_2016.values()), 'b-', linewidth=1, label="2015-2016 Software failures")
	plt.plot(range(len(event_week_hard_2015)+len(event_week_hard_2016)),list(event_week_hard_2015.values())+list(event_week_hard_2016.values()), 'r:', linewidth=1, label="2015-2016 Hardware failures")
	
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	plt.savefig("CATEGORY_PLOT_all_years_week.pdf")
	print("\nPlot in file: <CATEGORY_PLOT_all_years_week.pdf>")

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