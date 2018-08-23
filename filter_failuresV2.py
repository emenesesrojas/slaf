# Costa Rica High Technology Center (CeNAT)
# Advanced Computing Laboratory
# Elvis Rojas, MSc (erojas@una.cr)
# Esteban Meneses, PhD (esteban.meneses@acm.org)
# Filters failures, following these rules: 
#    Groups the failures related to the same job id together
#    Groups the failures affecting multiple nodes in the same line
#    Ignores node and blade controller heartbeat fault

import sys
import re
import datetime
import time

class FailedJob:
	def __init__(self, line):
		self.line = line
		self.nodes = []
	
def failureFilter(fileName):
	jobs_fail = {}
	formatAlt = '%Y-%m-%d %H:%M:%S'
  
	#size of failure file
	with open(fileName) as f:
		lines = len(f.readlines())
		
	count = 0 
	
	with open(fileName) as f:
		next(f)
		for line in f:
			count = count + 1
			print ("Progress: %d%%"% (count/lines*100),end="\r") 
	
			fields = line.split('|')
			jobid = int(fields[2].strip())
			ftime = fields[3].strip() #before ftime
			#failureTime = time.strptime(ftime, formatAlt)
			#epoch = time.mktime(failureTime)
			category = fields[4].strip()
			reason = fields[5].strip()
			description = fields[6].strip()
			text = fields[7].strip()
	  
			# ignore heartbeat faults
			if "Heartbeat Fault" in description:
				continue
			
			match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)n(\d+)", text)
			if not match:
				match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)", text)
				if match:
					node = match.group(0)
			else:	
				node =  match.group(0)
            
			
			if jobid in jobs_fail and category in jobs_fail[jobid] and description in jobs_fail[jobid][category] and reason in jobs_fail[jobid][category][description]:
				jobs_fail[jobid][category][description][reason].nodes.append(node)
				# print(node)
				print(len(jobs_fail[jobid][category][description][reason].FailedJob.nodes))
			
			entry = FailedJob(line)
			#create entry
			if jobid not in jobs_fail:
				jobs_fail[jobid] = {}
			if category not in jobs_fail[jobid]:
				jobs_fail[jobid][category] = {}
			if description not in jobs_fail[jobid]:
				jobs_fail[jobid][category][description] = {}
			if reason not in jobs_fail[jobid][category][description]:
				jobs_fail[jobid][category][description][reason] = entry
				
	for id in jobs_fail.keys():
		for cat in jobs_fail[id].keys():
			for des in jobs_fail[id][cat].keys():
				for rea in jobs_fail[id][cat][des].keys():
					print(jobs_fail[id][cat][des][rea].line)
					for i in range(len(jobs_fail[id][cat][des][rea].nodes)):
						print("......................"+jobs_fail[id][cat][des][rea].nodes[i])


if len(sys.argv) > 2:
	fileName = sys.argv[1]
	outputFileName =  sys.argv[2]
	file = open(outputFileName, 'w')
	
	file.write("|host name  |Job ID  |   FailTime            |   Category  |  Description   |   StartTime   |   EndTime   |    Nodes")
	failureFilter(fileName)
	file.close()
else:	
	print ("ERROR, usage: %s <file><output file>" % sys.argv[0])
	print ("<file>: Failure log file")
	print ("<output file>: file name to output filtered information")
	sys.exit(0)
