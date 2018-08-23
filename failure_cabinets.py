
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

def init_tables(cabinet_2015,cabinet_2016,blade_2015,blade_2016, node_2015, node_2016, cabinet_total_count):
	""" Initializes tables """
	
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
	
	cabinet_2015 = {}
	cabinet_2016 = {}
	cabinet_total_count = {}
	year_text = ""
	
	init = False
	# start timer
	startTime = time.clock()
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
	
	
	init_tables(cabinet_2015,cabinet_2016,blade_2015, blade_2016, node_2015, node_2016, cabinet_total_count)		
	
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
				year = item[3][2:-17].strip()		
				
				#extrac blade-cabinet[node]
				match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)n(\d+)", item[8].strip())
				if not match:
					match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)", item[8].strip())
					if match:
						node_exist = False
						cabinet = match.group(0)
				else:	
					cabinet =  match.group(0)
				
				if not match:
				   continue
					
				#extract data
				cabinet = cabinet.split("-") #example c17-2xxxxxx
				cabinet_column = int(cabinet[0][1:].strip())  #extract c17
				cabinet_row = int(cabinet[1][:1]) #extract 2
				
				
				
				#extract cabinet
				if node_exist == True:
					node = cabinet[1][-2:] #extract node number

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
	cabinets_matrix1 = np.zeros((25, 8))
	cabinets_matrix2 = np.zeros((8, 25))
	
	for i,c1 in zip(range(25), cabinet_total_count.keys()):
		for j,c2 in zip(range(8),cabinet_total_count[c1].keys()):
			cabinets_matrix1[i][j]  = cabinet_total_count[c1][c2]
			cabinets_matrix2[j][i]  = cabinet_total_count[c1][c2]
	# print(cabinets_matrix1)
	# print("////////////////////////////////////////////////////////////")
	# print(cabinets_matrix2)		
	
	#################################################################
	#PLOT count of cabinets
	print("\nPrcessing PLOT ...")	
	sns.set()
	fig, ax = plt.subplots(figsize=(8, 6))
	#im = ax.imshow(cabinets_matrix2,cmap="magma_r")
	from matplotlib.colors import ListedColormap
	ax = ax = sns.heatmap(cabinets_matrix2,linewidths=0.1)
	
	
	
	#ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
	#ax.tick_params(which="minor", bottom=False, left=False)
	
	plt.axis("tight")
	
	# Create colorbar
	#cbar = ax.figure.colorbar(im, ax=ax, cmap="magma_r")
	#cbar.ax.set_ylabel("Failure count", rotation=-90, va="bottom")
	
	rows = ["0","1","2","3","4","5","6","7"]
	cols = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
	ax.set_xticks(np.arange(len(cols)))
	ax.set_yticks(np.arange(len(rows)))
	ax.set_xticklabels(cols)
	ax.set_yticklabels(rows)
	plt.ylabel('Cabinet row')
	plt.xlabel('Cabinet Column')
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