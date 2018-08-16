#!/usr/bin/env python

# Costa Rica High Technology Center (CeNAT)
# Advanced Computing Laboratory
# Elvis Rojas, MSc (erojas@una.cr)
# Esteban Meneses, PhD (esteban.meneses@acm.org)
# Extracts mean-time-between-failures (MTBF) from the failure log, optionally filtered by the value of a field

import sys
import re
import datetime
import time
import matplotlib as mtl
mtl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss
from scipy.stats import norm
import scipy.special



### FUNCTIONS ###

def readFile(fileName,outputFile, delta, column=0, value=0):
	""" Reads a file and returns a list with the MTBF """
	mtbf = []
	countList = []
	formatAlt = '%m/%d/%y %H:%M %p'
	date_format = '%Y-%m-%d %H:%M:%S'
	previousDate = 0
	count = 0

	# with open(fileName) as row:
		# lines = len(row.readlines())
	
	# row.close()
	
	file = open(outputFile, 'w')
	
	with open(fileName) as f:
		f.seek(0)
		for line in f:
			if count == 0:
			    file.write(line)
			count += 1

			#print ("Progress: %d%%" % (count/lines*100), end = "\r")
			#sys.stdout.flush()

			if count == 1:
				continue
			fields = line.split('|')
			#print("++++++++++++++++++++++=%s - %d"%(fields[3].strip(),count))
			dateAndTime = fields[3].strip()
			
			if column != 0 and fields[column] != value:
				continue
			try:
				currentDate = datetime.datetime.strptime(dateAndTime, date_format)
			except ValueError:
				try:
					currentDate = datetime.datetime.strptime(dateAndTime, formatAlt)
				except ValueError:
					print("ERROR on line %d with date %s" % (count,dateAndTime))
					sys.exit(0)
			if previousDate == 0:
				previousDate = currentDate
				continue
			diff = currentDate - previousDate
			diff_seconds = diff.days*24*60*60 + diff.seconds
			if diff_seconds < 0:
				print("ERROR: negative event time difference in line %d" % count)
				sys.exit()
				
			#if diff_seconds < delta:
			#	continue
			
			print("%d"% diff_seconds)
			mtbf.append(diff_seconds)
			
			#time_format = time.strptime(fields[3].strip(), '%Y-%m-%d %H:%M:%S')
			#time_epoch = time.mktime(time_format)
			
			
			countList.append(count)
			file.write(str(diff_seconds)+"\n")
			previousDate = currentDate
		file.close()
	return (mtbf, countList)
	
if len(sys.argv) == 4:
	fileName = sys.argv[1]
	outputFile = sys.argv[2]
	delta = int(sys.argv[3])
	(data, countList) = readFile(fileName,outputFile, delta)
else:
	print("ERROR, usage: %s <input file> <output file> <delta> <bins> <output file> [<column> <value>] " % sys.argv[0])
	print("<input file>: failure log file")
	print("<output file>: PDF file name for figure")
	print("<delta>: minimum difference in seconds between failures")
	sys.exit(0)

np.random.seed(19680801)

x = np.linspace(min(data), max(data), len(data))#np.sort(data)
mu = np.mean(x)
sigma = np.std(x)
n_bins = 30

fig, ax = plt.subplots(figsize=(8, 4))


#data manipulation for plot
d = []
for i in data:
	if int(i) != 0:
		d.append(i)

data = np.sort(d)
mu = np.mean(data, keepdims = True)
sigma = np.std(data)

plt.xscale('log')
################################################
#Data plot
y = np.arange(1, len(data)+1)/len(data)
plt.plot(data, y, 'g-', linewidth=1, label="Data")

################################################
#Exponential plot
loc,scale=ss.expon.fit(data)
y = ss.expon.cdf(data, loc, scale)
plt.plot(data, y, 'c:', label="Exponential")
################################################

#lognormal plot
logdata = np.log(data)
estimated_mu, estimated_sigma = ss.norm.fit(logdata)
scale = estimated_mu
s = estimated_sigma 
cdf = (1+scipy.special.erf((np.log(data)-scale)/(np.sqrt(2)*s)))/2 #ss.lognorm.cdf(data, s, scale) 
plt.plot(data, cdf, 'm-.', linewidth=1, label="Lognormal") 
#################################################
#Weibull

shape, loc, scale = ss.weibull_min.fit(data, floc=0)
wei = ss.weibull_min(shape, loc, scale) # shape, loc, scale - creates weibull object
x = np.linspace(np.min(data), np.max(data), len(data))
plt.plot(x, wei.cdf(x),'r--',linewidth=1, label="Weibull")

#################################################
plt.xlabel('Time Between Failures (seconds)')
plt.ylabel('Cumulative probability')
plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
plt.savefig("PLOT_2016.pdf")



