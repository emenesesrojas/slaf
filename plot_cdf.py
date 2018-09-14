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

def readFile(fileName,outputFile):
	""" Reads a file and returns a list with the MTBF """
	mtbf = []
	countList = []
	formatAlt = '%m/%d/%y %H:%M %p'
	date_format = "%Y-%m-%d %H:%M:%S"
	previousDate = 0
	count = 0
	
	outputFile_data = outputFile[:-4]
	outputFile_data = outputFile_data + ".txt"
	
	file = open(outputFile_data, 'w')
	
	with open(fileName) as f:
		#f.seek(0)
		for line in f:
			if count == 0:
			    file.write(line)
			count += 1

			if count == 1:
				continue
			fields = line.split('|')
			#print("++++++++++++++++++++++=%s - %d"%(fields[3].strip(),count))
			
			dateAndTime = fields[3].strip()
			# print("contador: "+str(count))
			# print(fields)
			# print("linea: " + line)
			# print("Fecha: " + dateAndTime)
			
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
			
			#print("Dif seconds: %d count: %d "% (diff_seconds, count))
			mtbf.append(diff_seconds)	
			
			countList.append(count)
			file.write(str(diff_seconds)+"\n")
			previousDate = currentDate
		file.close()
	return (mtbf, countList)
	
if len(sys.argv) == 3:
	fileName = sys.argv[1]
	outputFile = sys.argv[2]
	(data, countList) = readFile(fileName,outputFile)
else:
	print("ERROR, usage: %s <input file> <output file>" % sys.argv[0])
	print("<input file>: failure log file")
	print("<output file>: PDF file name for plot ")
	sys.exit(0)

np.random.seed(19680801)

x = np.linspace(min(data), max(data), len(data))#np.sort(data)
mu = np.mean(x)
sigma = np.std(x)
n_bins = 30

fig, ax = plt.subplots(figsize=(4, 3))


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
plt.plot(data, y, 'b-', linewidth=1.5, label="Data")

################################################
#Exponential plot
loc,scale=ss.expon.fit(data)
y = ss.expon.cdf(data, loc, scale)
plt.plot(data, y,linestyle='-.',color="0.30", linewidth=0.9, label="Exponential")
################################################

#lognormal plot
logdata = np.log(data)
estimated_mu, estimated_sigma = ss.norm.fit(logdata)
scale = estimated_mu
s = estimated_sigma 
cdf = (1+scipy.special.erf((np.log(data)-scale)/(np.sqrt(2)*s)))/2 #ss.lognorm.cdf(data, s, scale) 
plt.plot(data, cdf, linestyle =':', color= "0.30", linewidth=1.2, label="Lognormal") 

#################################################
#Weibull

shape, loc, scale = ss.weibull_min.fit(data, floc=0)
wei = ss.weibull_min(shape, loc, scale) # shape, loc, scale - creates weibull object
x = np.linspace(np.min(data), np.max(data), len(data))
plt.plot(x, wei.cdf(x),'r--',linewidth=0.9, label="Weibull")
plt.legend(edgecolor="black",prop={'size': 8})
#################################################
plt.xlabel('Time Between Failures (seconds)')
plt.ylabel('Cumulative Probability')
#plt.legend(framealpha=1,shadow=True, borderpad = 1, fancybox=True)
plt.tight_layout()
plt.savefig(outputFile)
plt.savefig(outputFile[:-4]+".png")



