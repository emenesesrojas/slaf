
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
from datetime import date, timedelta, datetime as dt
import calendar as cl

def init_tables(event_hour_day, event_week, event_month):
	""" Initializes tables """
	event_hour_day['00'] = 0
	event_hour_day['01'] = 0
	event_hour_day['02'] = 0
	event_hour_day['03'] = 0
	event_hour_day['04'] = 0
	event_hour_day['05'] = 0
	event_hour_day['06'] = 0
	event_hour_day['07'] = 0
	event_hour_day['08'] = 0
	event_hour_day['09'] = 0
	event_hour_day['10'] = 0
	event_hour_day['11'] = 0
	event_hour_day['12'] = 0
	event_hour_day['13'] = 0
	event_hour_day['14'] = 0
	event_hour_day['15'] = 0
	event_hour_day['16'] = 0
	event_hour_day['17'] = 0
	event_hour_day['18'] = 0
	event_hour_day['19'] = 0
	event_hour_day['20'] = 0
	event_hour_day['21'] = 0
	event_hour_day['22'] = 0
	event_hour_day['23'] = 0
	event_week['Monday'] = 0
	event_week['Tuesday'] = 0
	event_week['Wednesday'] = 0
	event_week['Thursday'] = 0
	event_week['Friday'] = 0
	event_week['Saturday'] = 0
	event_week['Sunday'] = 0
	event_month['01'] = 0
	event_month['02'] = 0
	event_month['03'] = 0
	event_month['04'] = 0
	event_month['05'] = 0
	event_month['06'] = 0
	event_month['07'] = 0
	event_month['08'] = 0
	event_month['09'] = 0
	event_month['10'] = 0
	event_month['11'] = 0
	event_month['12'] = 0

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
	
def time_series(file_name):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	file_count = 0
	line_count = 0
	pathFileName = []
	event_hour_day = {}
	event_week = {}
	event_month = {}
	format = '%Y-%m-%d %H:%M:%S'
	init = False
	startTime = time.clock()
    
	init_tables(event_hour_day,event_week,event_month)

	# going through all files in directory
	#for file_name in pathFileName:  
	file_count += 1
	line_count = 0
	count_event = 0
	
	with open(file_name) as log:
		line_count += 1
		if line_count == 1:
			next(log)
		for line in log:
			item = line.split("|")
			
			d = item[3][2:-17].strip()+item[3][7:-14].strip()+item[3][10:-11].strip()
			week = datetime.date(int(item[3][2:-17].strip()), int(item[3][7:-14].strip()), int(item[3][10:-11].strip())).isocalendar()[1]
			month = item[3][7:-14].strip()
			year = item[3][2:-17].strip()
			#Day of week
			f = dt.strptime(item[3].strip(),format)
			day_of_week = cl.day_name[f.weekday()] 
			#Hour of day
			hd = item[3].strip()
			hour_day = hd[10:13].strip()
				
			if hour_day in event_hour_day.keys():
				event_hour_day[hour_day] += 1
		
			if month in event_month.keys():
				event_month[month] += 1
				
			if day_of_week in event_week.keys():
				event_week[day_of_week] += 1
				continue
				
	###########################################################################################3333
	plt.style.use('seaborn-whitegrid')
	fig = plt.figure()
	fig, axs = plt.subplots(2,3,figsize=(13, 7))
		
	print("Processing failures graphic by month:  Graphic 1 of 3")	
	data = [event_month['01'],event_month['02'],event_month['03'],event_month['04'],event_month['05'],event_month['06'],event_month['07'],event_month['08'],event_month['09'],event_month['10'],event_month['11'],event_month['12']]
	axs[0,0].set_xticks(np.arange(1,13, 1))
	axs[0,0].bar(range(1,13,1),data)
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	axs[0,0].set_xlabel('Months')
	axs[0,0].set_ylabel('Count of failures')
	axs[0,0].set_title('Failures by Month ' + year)
	
	#############################################################
	print("Processing failures graphic by day:  Graphic 2 of 3")
	
	m = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	list_names = []
	for i in m:
		list_names.append(i[:2])
	
	data = [event_week['Monday'],event_week['Tuesday'],event_week['Wednesday'],event_week['Thursday'],event_week['Friday'],event_week['Saturday'],event_week['Sunday']]
	axs[0,1].set_xticklabels(list_names)
	axs[0,1].set_xticks(np.arange(1,8, 1))
	axs[0,1].bar(range(1,8,1),data)
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	axs[0,1].set_xlabel('Day of week')
	axs[0,1].set_ylabel('Count of failures')
	axs[0,1].set_title('Failures by day of week ' + year)
	
	############################################################
	print("Processing failures graphic by hour: Graphic 3 of 3")
	data = [event_hour_day['00'],event_hour_day['01'],event_hour_day['02'],event_hour_day['03'],event_hour_day['04'],event_hour_day['05'],event_hour_day['06'],event_hour_day['07'],event_hour_day['08'],event_hour_day['09'],event_hour_day['10'],event_hour_day['11'],event_hour_day['12'],event_hour_day['13'],event_hour_day['14'],event_hour_day['15'],event_hour_day['16'],event_hour_day['17'],event_hour_day['18'],event_hour_day['19'],event_hour_day['20'],event_hour_day['21'],event_hour_day['22'],event_hour_day['23']]	
	#axs[0,2].set_yticks(np.arange(0,max(event_hour_day.values())+5, 5))
	axs[0,2].bar(range(1,25,1),data)
	plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
	axs[0,2].set_xlabel('Hour of day')
	axs[0,2].set_ylabel('Count of failures')
	axs[0,2].set_title('Failures by hour of day ' + year)
	plt.xticks([2.4,6.4,10.4,14.4,18.4,22.4], ['2','6','10','14','18','22'])
	
	
	plt.savefig("PLOT_failure_HourDay_week_month_"+year+".pdf")
	print("Plot in file: <PLOT_failure_HourDay_week_month_"+year+".pdf>")	
	
	
if len(sys.argv) >= 3:
	dirName = sys.argv[1]
	failure_year = sys.argv[2]
	time_series(dirName)
else:
	print ("ERROR, usage: %s <imput failure file> <year>" % sys.argv[0])
	sys.exit(0)