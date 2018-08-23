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
		self.nodes = {}
	
def failureFilter(fileName, outputFileName):
	jobs_fail = {}
	#formatAlt = '%Y-%m-%d %H:%M:%S'
	file = open(outputFileName, 'w')

	#size of failure file
	with open(fileName) as f:
		lines = len(f.readlines())
		
	count = 0 
	file.write("| hostname | job_id  | fail_time           | category | reason | description                      | text                                                                                                                                  | jf_id   |		nodes\n")
	with open(fileName) as f:
		next(f)
		for line in f:
			count = count + 1
			print ("Progress: %d%%"% (count/lines*100),end="\r") 
	
			fields = line.split('|')
			jobid = int(fields[2].strip())
			#ftime = fields[3].strip() 
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
            
			if node != '':
				if jobid in jobs_fail and category in jobs_fail[jobid] and description in jobs_fail[jobid][category] and reason in jobs_fail[jobid][category][description]:
					if node not in jobs_fail[jobid][category][description][reason].nodes.keys():
						jobs_fail[jobid][category][description][reason].nodes[node]={}
					
			entry = FailedJob(line)
			#create entry
			if jobid not in jobs_fail:
				jobs_fail[jobid] = {}
			if category not in jobs_fail[jobid]:
				jobs_fail[jobid][category] = {}
			if description not in jobs_fail[jobid][category]:
				jobs_fail[jobid][category][description] = {}
			if reason not in jobs_fail[jobid][category][description]:
				jobs_fail[jobid][category][description][reason] = entry
				jobs_fail[jobid][category][description][reason].nodes[node] = {}
	
	entry_nodes = ""
	for id in jobs_fail.keys():
		for cat in jobs_fail[id].keys():
			for des in jobs_fail[id][cat].keys():
				for rea in jobs_fail[id][cat][des].keys():
					#for i in jobs_fail[id][cat][des][rea].nodes.keys():
					#	entry_nodes = entry_nodes +  i #jobs_fail[id][cat][des][rea].nodes[i].keys()
					##print("##################################################################")
					entry_nodes = "|"+" ".join(jobs_fail[id][cat][des][rea].nodes.keys()) +"\n"#" ".join(jobs_fail[id][cat][des][rea].nodes.keys()) + "\n"
					# print(jobs_fail[id][cat][des][rea].line.strip() + entry_nodes)
					# sys.exit()
					file.write(jobs_fail[id][cat][des][rea].line.strip() + entry_nodes)
	file.close()

if len(sys.argv) > 2:
	fileName = sys.argv[1]
	outputFileName =  sys.argv[2]
	failureFilter(fileName, outputFileName)
	
else:	
	print ("ERROR, usage: %s <file><output file>" % sys.argv[0])
	print ("<file>: Failure log file")
	print ("<output file>: file name to output filtered information")
	sys.exit(0)
