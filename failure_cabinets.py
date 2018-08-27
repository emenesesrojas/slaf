
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
import seaborn as sns
from datetime import date, timedelta, datetime as dt
import calendar as cl

def init_tables(cabinet_2015,cabinet_2016,blade_2015,blade_2016, node_2015, node_2016, cabinet_total_count, cabinet_week, cabinet_day):
	""" Initializes tables """
	
	cabinet_week['Monday'] = {}
	cabinet_week['Tuesday'] = {}
	cabinet_week['Wednesday'] = {}
	cabinet_week['Thursday'] = {}
	cabinet_week['Friday'] = {}
	cabinet_week['Saturday'] = {}
	cabinet_week['Sunday'] = {}
	
	cabinet_day[1] = {}
	cabinet_day[2] = {}
	cabinet_day[3] = {}
	cabinet_day[4] = {}
	cabinet_day[5] = {}
	cabinet_day[6] = {}
	cabinet_day[7] = {}
	cabinet_day[8] = {}
	cabinet_day[9] = {}
	cabinet_day[10] = {}
	cabinet_day[11] = {}
	cabinet_day[12] = {}
	cabinet_day[13] = {}
	cabinet_day[14] = {}
	cabinet_day[15] = {}
	cabinet_day[16] = {}
	cabinet_day[17] = {}
	cabinet_day[18] = {}
	cabinet_day[19] = {}
	cabinet_day[20] = {}
	cabinet_day[21] = {}
	cabinet_day[22] = {}
	cabinet_day[23] = {}
	cabinet_day[24] = {}
	cabinet_day[25] = {}
	cabinet_day[26] = {}
	cabinet_day[27] = {}
	cabinet_day[28] = {}
	cabinet_day[29] = {}
	cabinet_day[30] = {}
	cabinet_day[31] = {}

	
	cabinet_2015[0] = {}
	cabinet_2015[1] = {}
	cabinet_2015[2] = {}
	cabinet_2015[3] = {}
	cabinet_2015[4] = {}
	cabinet_2015[5] = {}
	cabinet_2015[6] = {}
	cabinet_2015[7] = {}
	cabinet_2015[8] = {}
	cabinet_2015[9] = {}
	cabinet_2015[10] = {}
	cabinet_2015[11] = {}
	cabinet_2015[12] = {}
	cabinet_2015[13] = {}
	cabinet_2015[14] = {}
	cabinet_2015[15] = {}
	cabinet_2015[16] = {}
	cabinet_2015[17] = {}
	cabinet_2015[18] = {}
	cabinet_2015[19] = {}
	cabinet_2015[20] = {}
	cabinet_2015[21] = {}
	cabinet_2015[22] = {}
	cabinet_2015[23] = {}
	cabinet_2015[24] = {}
	
	cabinet_2016[0] = {}
	cabinet_2016[1] = {}
	cabinet_2016[2] = {}
	cabinet_2016[3] = {}
	cabinet_2016[4] = {}
	cabinet_2016[5] = {}
	cabinet_2016[6] = {}
	cabinet_2016[7] = {}
	cabinet_2016[8] = {}
	cabinet_2016[9] = {}
	cabinet_2016[10] = {}
	cabinet_2016[11] = {}
	cabinet_2016[12] = {}
	cabinet_2016[13] = {}
	cabinet_2016[14] = {}
	cabinet_2016[15] = {}
	cabinet_2016[16] = {}
	cabinet_2016[17] = {}
	cabinet_2016[18] = {}
	cabinet_2016[19] = {}
	cabinet_2016[20] = {}
	cabinet_2016[21] = {}
	cabinet_2016[22] = {}
	cabinet_2016[23] = {}
	cabinet_2016[24] = {}

	cabinet_total_count[0] = {}
	cabinet_total_count[1] = {}
	cabinet_total_count[2] = {}
	cabinet_total_count[3] = {}
	cabinet_total_count[4] = {}
	cabinet_total_count[5] = {}
	cabinet_total_count[6] = {}
	cabinet_total_count[7] = {}
	cabinet_total_count[8] = {}
	cabinet_total_count[9] = {}
	cabinet_total_count[10] = {}
	cabinet_total_count[11] = {}
	cabinet_total_count[12] = {}
	cabinet_total_count[13] = {}
	cabinet_total_count[14] = {}
	cabinet_total_count[15] = {}
	cabinet_total_count[16] = {}
	cabinet_total_count[17] = {}
	cabinet_total_count[18] = {}
	cabinet_total_count[19] = {}
	cabinet_total_count[20] = {}
	cabinet_total_count[21] = {}
	cabinet_total_count[22] = {}
	cabinet_total_count[23] = {}
	cabinet_total_count[24] = {}
	
def f_cabinets(dir_name):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	file_count = 0
	line_count = 0
	pathFileName = []
	
	node_2015 = {}
	node_2015 = {}
	node_2016 = {}
	
	blade_2015 = {}
	blade_2016 = {}
	
	cabinet_day = {}
	cabinet_week = {}
	cabinet_2015 = {}
	cabinet_2016 = {}
	cabinet_total_count = {}
	year_text = ""
	format = '%Y-%m-%d %H:%M:%S'
	
	
	init = False
	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
	
	
	init_tables(cabinet_2015,cabinet_2016,blade_2015, blade_2016, node_2015, node_2016, cabinet_total_count,cabinet_week,cabinet_day)		
	
	# going through all files in directory
	for file_name in pathFileName:  
		file_count += 1
		line_count = 0
		print("\nPrcessing %d year "% file_count)
		year_text = year_text +"_"+ str(2014 + file_count)
		count_event = 0
		file_name = dir_name + file_name
		
		
		with open(file_name) as log:
			line_count += 1
			if line_count == 1:
				next(log)
			for line in log:
				cabinet = ""
				node_exist = True
			
				item = line.split("|")
				year = item[3].strip()[:-15]
				#day_name
				day = int(item[3].strip()[8:-9])
				#Day of week
				f = dt.strptime(item[3].strip(),format)
				day_of_week = cl.day_name[f.weekday()] 
				
				all_nodes = item[9].strip().split()
				for an in all_nodes: 
					match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)n(\d+)", an)
					if not match:
						match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)", an)
						if match:
							cabinet = match.group(0)
					else:	
						cabinet =  match.group(0)
						
					#extract data
					cabinet = cabinet.split("-") #example c17-2xxxxxx
					cabinet_column = int(cabinet[0][1:].strip())  #extract c17
					cabinet_row = int(cabinet[1][:1]) #extract 2
					node = cabinet[1][-2:] #extract node number

					#count cabinets by day
					if cabinet_column not in cabinet_day[day]:
						cabinet_day[day][cabinet_column] = 1
					else:
						cabinet_day[day][cabinet_column] += 1
					
					#count cabinets by week
					if cabinet_column not in cabinet_week[day_of_week]:
						cabinet_week[day_of_week][cabinet_column] = 1
					else:
						cabinet_week[day_of_week][cabinet_column] += 1
					
					
					if cabinet_column not in cabinet_total_count:
						cabinet_total_count[cabinet_column] = {}	
					if cabinet_row not in cabinet_total_count[cabinet_column]:
						cabinet_total_count[cabinet_column][cabinet_row] = 1
					else:
						cabinet_total_count[cabinet_column][cabinet_row] += 1
					
					if year == "2015":
						if cabinet_column not in cabinet_2015:
							cabinet_2015[cabinet_column] = {}
						if cabinet_row not in cabinet_2015[cabinet_column]:
							cabinet_2015[cabinet_column][cabinet_row] = 1
						else:
							cabinet_2015[cabinet_column][cabinet_row] += 1
							continue
				
					if year == "2016":
						if cabinet_column not in cabinet_2016:
							cabinet_2016[cabinet_column] = {}
						if cabinet_row not in cabinet_2016[cabinet_column]:
							cabinet_2016[cabinet_column][cabinet_row] = 1
						else:
							cabinet_2016[cabinet_column][cabinet_row] += 1
							
	#control data
	print(cabinet_2015)
	print("////////////////////////////////////////////////////////////")
	print(cabinet_2016)
	print("////////////////////////////////////////////////////////////")
	print(cabinet_total_count)
	print("////////////////////////////////////////////////////////////")
	
	
	#Matrix to contanis data 
	cabinets_matrix_two_years = np.zeros((8, 25))
	cabinets_matrix_2015 = np.zeros((8, 25))
	cabinets_matrix_2016 = np.zeros((8, 25))
	cabinets_matrix_week = np.zeros((7, 25))
	cabinets_matrix_day = np.zeros((31, 25))
	
	
	#Total count
	for i,c1 in zip(range(25), cabinet_total_count.keys()):
		for j,c2 in zip(range(8),cabinet_total_count[c1].keys()):
			cabinets_matrix_two_years[j][i]  = cabinet_total_count[c1][c2]
	
	#2015 count
	for i,c1 in zip(range(25), cabinet_2015.keys()):
		for j,c2 in zip(range(8),cabinet_2015[c1].keys()):
			cabinets_matrix_2015[j][i]  = cabinet_2015[c1][c2]
	
	#2016 count
	for i,c1 in zip(range(25), cabinet_2015.keys()):
		for j,c2 in zip(range(8),cabinet_2016[c1].keys()):
			cabinets_matrix_2016[j][i]  = cabinet_2016[c1][c2]

	print("WEEK////////////////////////////////////////////////////////////")		
	print(cabinet_week)
	print("////////////////////////////////////////////////////////////")
	
	#total count cabinet failures by week
	for c1 in cabinet_week.keys():
		if c1 == "Monday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[0][j]  = cabinet_week[c1][c2]
		if c1 == "Tuesday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[1][j]  = cabinet_week[c1][c2]
		if c1 == "Wednesday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[2][j]  = cabinet_week[c1][c2]
		if c1 == "Thursday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[3][j]  = cabinet_week[c1][c2]
		if c1 == "Friday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[4][j]  = cabinet_week[c1][c2]
		if c1 == "Saturday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[5][j]  = cabinet_week[c1][c2]
		if c1 == "Sunday":
			for j,c2 in zip(range(25),cabinet_week[c1].keys()):
				cabinets_matrix_week[6][j]  = cabinet_week[c1][c2]
	
	print("MATRIX WEEK////////////////////////////////////////////////////////////")
	print(cabinets_matrix_week)
	# for i,c1 in zip(range(7), cabinet_week.keys()):
		# for j,c2 in zip(range(25),cabinet_week[c1].keys()):
			# cabinets_matrix_week[i][j]  = cabinet_week[c1][c2]
			
	print("DAY////////////////////////////////////////////////////////////")
	print(cabinet_day)
	print("////////////////////////////////////////////////////////////")
	
	#total count cabinet failures by day
	for i,c1 in zip(range(31), cabinet_day.keys()):
		for j,c2 in zip(range(25),cabinet_day[c1].keys()):
			cabinets_matrix_day[i][j]  = cabinet_day[c1][c2]
		
	#################################################################
	#PLOT count of cabinets
	
	fig = plt.figure()
	fig, axs = plt.subplots(2,3,figsize=(15, 8))
	
	sns.set()
	rows = ["0","1","2","3","4","5","6","7"]
	cols = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
	
	#plot heatmap count 2015
	print("\nPrcessing PLOT 1")
	ax = sns.heatmap(cabinets_matrix_2015,cmap="YlGnBu", linewidths=0.1, ax = axs[0,0])
	ax.invert_yaxis()
	axs[0,0].axis("tight")
	axs[0,0].set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5])
	axs[0,0].set_yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5])
	axs[0,0].set_xticklabels(cols,fontsize=7)
	axs[0,0].set_yticklabels(rows)
	axs[0,0].set_title('2015')
	axs[0,0].set_ylabel('Cabinet row')
	axs[0,0].set_xlabel('Cabinet Column')
	
	#plot heatmap count 2016
	print("\nPrcessing PLOT 2")
	ax = sns.heatmap(cabinets_matrix_2016,cmap="YlGnBu", linewidths=0.1, ax = axs[0,1])
	ax.invert_yaxis()
	axs[0,1].axis("tight")
	axs[0,1].set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5])
	axs[0,1].set_yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5])
	axs[0,1].set_xticklabels(cols,fontsize=7)
	axs[0,1].set_yticklabels(rows)
	axs[0,0].set_title('2016')
	axs[0,1].set_ylabel('Cabinet row')
	axs[0,1].set_xlabel('Cabinet Column')
	
	#plot heatmap count 2015-2016
	print("\nPrcessing PLOT 3")		
	ax = sns.heatmap(cabinets_matrix_two_years,cmap="YlGnBu", linewidths=0.1, ax = axs[0,2])
	ax.invert_yaxis()
	axs[0,2].axis("tight")
	axs[0,2].set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5])
	axs[0,2].set_yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5])
	axs[0,2].set_xticklabels(cols,fontsize=7)
	axs[0,2].set_yticklabels(rows)
	axs[0,0].set_title('2015-2016')
	axs[0,2].set_ylabel('Cabinet row')
	axs[0,2].set_xlabel('Cabinet Column')
	
	
	#plot heatmap count 2015-2016 cabinet failures by week
	print("\nPrcessing PLOT 4")
	rows = ["Mon","Tue","wed","Thu","Fri","Sat","Sun"]
	ax = sns.heatmap(cabinets_matrix_week,cmap="YlGnBu", linewidths=0.1, ax = axs[1,0])
	# ax.invert_yaxis()
	axs[1,0].axis("tight")
	axs[1,0].set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5])
	axs[1,0].set_yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5])
	axs[1,0].set_xticklabels(cols,fontsize=7)
	axs[1,0].set_yticklabels(rows)
	axs[1,0].set_title('2015-2016 by week')
	axs[1,0].set_ylabel('Day of week')
	axs[1,0].set_xlabel('Cabinet Column')
	
	#plot heatmap count 2015-2016 cabinet failures by day
	print("\nPrcessing PLOT 5")
	rows = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
	ax = sns.heatmap(cabinets_matrix_day,cmap="YlGnBu", linewidths=0.1, ax = axs[1,1])
	# ax.invert_yaxis()
	axs[1,1].axis("tight")
	axs[1,1].set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5])
	axs[1,1].set_yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5])
	axs[1,1].set_xticklabels(cols,fontsize=7)
	axs[1,1].set_yticklabels(rows,fontsize=7)
	axs[1,1].set_title('2015-2016 by day')
	axs[1,1].set_ylabel('Day')
	axs[1,1].set_xlabel('Cabinet Column')
	
	
	fig.tight_layout()
	plt.savefig("PLOT_failure_cabinets_" + year_text +".pdf")
	print("\nPlot in file: <PLOT_failure_cabinets"+ year_text +".pdf>")
	
	# ##############################################################################
	return 
	
	
if len(sys.argv) >= 2:
	dirName = sys.argv[1]
	outputFileName = "" #sys.argv[2]
	f_cabinets(dirName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	sys.exit(0)