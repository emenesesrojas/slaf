
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
from datetime import date, timedelta
from scipy.fftpack import fft, ifft

def init_tables(event_hour, event_day, event_week, event_month):
	""" Initializes tables """
	
	for i in range(1, 26281):
		event_hour[i] = 0
	
	for i in range(1,1096):
		event_day[i] = 0
	
	
	for i in range(1,157):
		event_week[i] = 0
		
	for i in range(1,37):
		event_month[i] = 0
			
def time_series(dir_name):
	#""" Reads a failure log file and correlates job IDs with MOAB log files in the directory """
	dayFormat = '%a_%b_%d_%Y'
	format = '%Y-%m-%d %H:%M:%S'
	file_count = 0
	line_count = 0
	count_event = 0
	pathFileName = []
	event_hour = {}
	event_day = {}
	event_week = {}
	event_month = {}
	init = False
	# start timer
	startTime = time.clock()
	
    #get all files of the year
	for path, dirs, files in os.walk(dir_name):
			for f in files:
				pathFileName.append(f)
	
	pathFileName = sorted(pathFileName)
	
	init_tables(event_hour, event_day, event_week,event_month)
	
	# going through all files in directory
	for file_name in pathFileName:  
		skip_header = 0
		file_count += 1
		print("\nPrcessing year %d. File: %s" % (file_count,file_name),end="\r")
		
		count_event = 0
		file_name = dir_name + file_name
		
		with open(file_name) as log:
			skip_header += 1
				
			if skip_header == 1:
				next(log)
			for line in log:
				line_count += 1
			
			
				item = line.split("|")
				
				hour_day = int(item[3].strip()[11:-6])
				
				day_month = int(item[3].strip()[8:-9])
				day_year = datetime.datetime.strptime(item[3].strip(),'%Y-%m-%d %H:%M:%S').timetuple().tm_yday
				
				month = int(item[3].strip()[5:-12])
				year = int(item[3].strip()[:-15])
				
				#week of year
				week = datetime.date(year, month, day_month).isocalendar()[1]
				
				if file_count == 1:
					pos_w = pos_m = pos_d =  0
					pos_h = (day_year - 1) * 24
				if file_count == 2:
					pos_d = 365
					pos_w = 52
					pos_m = 12
					pos_h = (365 + (day_year - 1)) * 24
				if file_count == 3:
					pos_d = 730
					pos_w = 104
					pos_m = 24
					pos_h = (730 + (day_year - 1)) * 24
				
				
				# #print(str(hour_day))
				pos_hour_array = pos_h + int(hour_day) 	
				
				if pos_hour_array in event_hour.keys():
					event_hour[pos_hour_array] += 1
					count_event += 1
				else:
					print("no encontrado")
					
				pos_day_array = pos_d + int(day_year) 				
				if pos_day_array in event_day.keys():
					event_day[pos_day_array] += 1
				
				pos_week_array = pos_w + int(week) 				
				if pos_week_array	 in event_week.keys():
					event_week[pos_week_array] += 1
				
				pos_month_array = pos_m + int(month) 				
				if pos_month_array	 in event_month.keys():
					event_month[pos_month_array] += 1
				
				
	#print(event_hour)
	print(count_event)
	
	print("Line count: "+str(line_count))
	
	print("\nPrcessing %d year of 3"% file_count)	
	
	
	#fig, ax = plt.subplots(4, 1,figsize=(8, 7))
	
	
	#event = list(event_day.values())
	event = list(event_hour.values())
	
	
	#normalization around zero
	mw = np.mean(event)
	event = event - mw

	fig, ax = plt.subplots(4, 1)

	#############################################################
	#FFT
	#number of sample points
	N = len(event)
	#Sampling frequency of signal (time unit = year)
	fs = 168
	#Period (in years) between each sample collected
	T = 1/fs 
	#create x-axis for time length of signal
	x = np.linspace(0, N*T, N)

	#create array that corresponds to values in signal
	#y = list(event.values())#df

	#perform FFT on signal
	yf = fft(event)

	#Vector of frequencies (using just half of the spectrum)
	xf = np.linspace(0.0, fs/2.0, N//2 +1)

	#plot results

	#Time domain plot------------------------------------------
	x = np.linspace(0.0, N, N)
	ax[0].plot(x, event, linewidth=0.9)
	ax[0].grid()
	ax[0].set_xlabel('Weeks')
	ax[0].set_ylabel('Failure Count')
	#ax[0].set_xscale("log")
#----------------------------------------------------------
	#############################################################


	#Frequency domain plot-------------------------------------
	nyf = (2/N) * np.abs(yf[0:N//2 +1]) #normalized coefficients
	phase_y = np.angle(yf[0:N//2 +1]) 
	
	ax[1].plot(xf, nyf, linewidth=0.9) 
	ax[1].grid()
	ax[1].set_xlabel('Frequency (hz)')
	ax[1].set_ylabel(r'Spectral Magnitude')

	#Highlight the 3 coefficients with maximum values
	maxY = np.argsort(nyf)
	maxY = maxY[::-1]

	ax[1].plot(xf[maxY[0]], nyf[maxY[0]], 'ro')
	ax[1].text(xf[maxY[0]] * 1.04, nyf[maxY[0]] * 0.95, str(round(xf[maxY[0]],2)) + 'hz=' + str(round(1.0/xf[maxY[0]],2)) + 'years', fontsize=12)
	ax[1].plot(xf[maxY[1]], nyf[maxY[1]], 'go')
	ax[1].text(xf[maxY[1]] * 1.04, nyf[maxY[1]] * 0.95, str(round(xf[maxY[1]],2)) + 'hz=' + str(round(1.0/xf[maxY[1]],2)) + 'years', fontsize=12) 
	ax[1].plot(xf[maxY[2]], nyf[maxY[2]], 'bo') 
	ax[1].text(xf[maxY[2]] * 1.04, nyf[maxY[2]] * 0.95, str(round(xf[maxY[2]],2)) + 'hz=' + str(round(1.0/xf[maxY[2]],2)) + 'years', fontsize=12)
	ax[1].set_xscale("log")
	#----------------------------------------------------------

	#Plot sinusoidals on top of time data
	ax[2].plot(x, event, linewidth=0.9)

	sin1 = 50 * np.cos(x*2.0*np.pi*xf[maxY[0]]/fs + phase_y[maxY[0]])
	ax[2].plot(x, sin1, 'r',linewidth=0.2)


	sin2 = 50 * np.cos(x*2.0*np.pi*xf[maxY[1]]/fs  + phase_y[maxY[1]])
	ax[2].plot(x, sin2, 'g',linewidth=0.2)

	sin3 = 50 * np.cos(x*2.0*np.pi*xf[maxY[2]]/fs + phase_y[maxY[2]])
	ax[2].plot(x, sin3, 'b',linewidth=0.2)
	#ax[2].set_xscale("log")
	
	sum_sin = sin1 + sin2 + sin3
	ax[3].plot(x, event, 'g',linewidth=0.2)
	ax[3].plot(x, sum_sin, 'r',linewidth=0.2)
	#ax[3].set_xscale("log")
	
	plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
	plt.savefig("PLOT_FFT_ZERO.pdf")
	plt.close('all')
	
	# #############################################################
	# y = list(event_week.values())
	# N = len(event_week)
	# x = np.linspace(0.0, N, N)
	# ax[0].plot(x, y, label = 'signal', linewidth=0.9)
	# ax[0].grid()
	# ax[0].set_xlabel('Weeks')
	# ax[0].set_ylabel('Failure Count')
	
	# #############################################################
	# #FFT
	# #number of sample points
	# N = len(event_week)
	
	# Fs = 52
	# #frequency of signal (in days)
	#	 T = 1/Fs
	# #create x-axis for time length of signal
	# x = np.linspace(0, N*T, N)
	# #create array that corresponds to values in signal
	# y = list(event_week.values())#df
	# print(y)

	# #perform FFT on signal
	# yf = fft(y)
	# #create new x-axis: frequency from signal
	# xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
	# #plot results
	# ax[1].plot(xf, 2.0/N * np.abs(yf[0:N//2]), label = 'signal', linewidth=0.9)
	# ax[1].grid()
	# ax[1].set_xlabel('Frequency (weeks)')
	# ax[1].set_ylabel(r'Spectral Amplitude')
	
	# #############################################################
	# y = list(event_day.values())
	# N = len(event_day)
	# x = np.linspace(0.0, N, N)
	# ax[2].plot(x, y, label = 'signal', linewidth=0.9)
	# ax[2].grid()
	# ax[2].set_xlabel('Days')
	# ax[2].set_ylabel('Failure Count')
	
	
	# #############################################################
	# y = list(event_day.values())#df
	# N = len(event_day)
	# Fs = 7
	# T = 1/Fs
	# x = np.linspace(0, N*T, N)
	# print(y)

	# yf = fft(y)
	# xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
	# ax[3].plot(xf, 2.0/N * np.abs(yf[0:N//2]), label = 'signal', linewidth=0.9)
	# ax[3].grid()
	# ax[3].set_xlabel('	Frequency (days)')
	# ax[3].set_ylabel(r'Spectral Amplitude')
	
	
	
	# plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.65, wspace=0.35)
	# plt.savefig("PLOT_FFT.pdf")
	# print("\nPlot in file: <PLOT_day_2015_2016.pdf>")

	
	return 
	
	
if len(sys.argv) >= 2:
	dirName = sys.argv[1]
	outputFileName = "" #sys.argv[2]
	time_series(dirName)
else:
	print ("ERROR, usage: %s <directory> <output file>" % sys.argv[0])
	sys.exit(0)