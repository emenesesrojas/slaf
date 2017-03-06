#!/usr/bin/env python

# Costa Rica High Technology Center (CeNAT)
# Advanced Computing Laboratory
# Esteban Meneses, PhD (esteban.meneses@acm.org)
# Extracts mean-time-between-failures (MTBF) from the failure log, optionally filtered by the value of a field

import sys
import re
import datetime
import matplotlib.pyplot as plt
import numpy as np

### FUNCTIONS ###

def readFile(fileName, delta, column=0, value=0):
	""" Reads a file and returns a list with the MTBF """
	mtbf = []
	format = '%m/%d/%y %H:%M %p'
	formatAlt = '%Y-%m-%d %H:%M:%S'
	previousDate = 0
	count = 0
	with open(fileName) as f:
		for line in f:
			count += 1
			if count == 1:
				continue
			fields = line.split('|')
			dateAndTime = fields[3].strip()
			if column != 0 and fields[column] != value:
				continue
			try:
				currentDate = datetime.datetime.strptime(dateAndTime, format)
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
			if diff.seconds < delta:
				continue
			mtbf.append(diff.seconds)
			previousDate = currentDate	
	return mtbf

### MAIN CODE ###
#DEBUG print 'Number of arguments:', len(sys.argv), 'arguments.'
#DEBUG print 'Argument List:', str(sys.argv)

if len(sys.argv) == 5:
	fileName = sys.argv[1]
	outputFile = sys.argv[2]
	delta = int(sys.argv[3])
	bins = int(sys.argv[4])
	mtbf = readFile(fileName,delta)
elif len(sys.argv) == 7:
	fileName = sys.argv[1]
	outputFile = sys.argv[2]
	delta = int(sys.argv[3])
	bins = int(sys.argv[4])
	column = int(sys.argv[5]) - 1
	value = sys.argv[6]
	mtbf = readFile(fileName,delta,column,value)
else:
	print("ERROR, usage: %s <input file> <output file> <delta> <bins> [<column> <value>]" % sys.argv[0])
	print("<input file>: failure log file")
	print("<output file>: PDF file name for figure")
	print("<delta>: minimum difference in seconds between failures")
	print("<bins>: number of bins in the histogram")
	print("<column>: field in the failure log file to filter records")
	print("<value>: value of the field for filtering")
	sys.exit(0)

# plotting MTBF
plt.title('Mean Time Between Failures (MTBF)')
plt.hist(mtbf, bins)
plt.xlabel('Seconds')
plt.ylabel('Count')
plt.savefig(outputFile)
#plt.show()
