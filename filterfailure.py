import sys
import re
import datetime
import time

# to filter the failures in the log files
# group the failures related to the same job id together
# for the same job id, group the failures affecting multiple nodes in the same line
# ignore node heartbeat fault

class FailedJob:
  def __init__(self, failureType, epoch):
    self.failureType = failureType
    self.startTime = epoch
    self.endTime = epoch
    self.nodes = []
    self.toPrint = True
  def updateTime(self, epoch):
    if self.startTime > epoch:
      self.startTime = epoch
    if self.endTime < epoch:
      self.endTime = epoch


def failureFilter(fileName):
  jobs = {}
  formatAlt = '%Y-%m-%d %H:%M:%S'
  with open(fileName) as f:
    next(f)
    for line in f:
	    fields = line.split('|')
	    jobid = int(fields[2].strip())
	  
	    ftime = fields[3].strip()
	    failureTime = time.strptime(ftime, formatAlt)
	    epoch = time.mktime(failureTime)
	    category = fields[4].strip()
	    user = fields[5].strip()
	    reason = fields[6].strip()
	    text = fields[7].strip()
	  
	    #ignore heartbeat faults
	    if "Heartbeat Fault" in reason:
		    continue
	    if(reason == "GPU XID"):
		    #get the number
		    match = re.search(r"GPU Xid (\d+)", text)
		    reason = match.group(0)
	  
	    node = ''
	    #find the node related with the failure
	    #for HT Lockup, no node information is reported
	    match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)n(\d+)", text)
	    if not match:
		    match = re.search(r"c(\d+)-(\d+)c(\d+)s(\d+)", text)
		    if match:
			    node = match.group(0)
	    else:	
		    node =  match.group(0)
	  
	    entry = FailedJob(reason, epoch)
	    #create entry
	    if jobid not in jobs:
		    jobs[jobid] = {}
	    if category not in jobs[jobid]:
		    jobs[jobid][category] = {}
	    if reason not in jobs[jobid][category]:
		    jobs[jobid][category][reason] = FailedJob(reason, epoch)
	    else:
		    jobs[jobid][category][reason].updateTime(epoch)

	    if node != '':
		    if node not in jobs[jobid][category][reason].nodes:
		       jobs[jobid][category][reason].nodes.append(node);
	  
	    #ignore user related errors
	    #if reason == "Out of Memory":
	    #jobs[jobid]['software'][reason].toPrint = False
	    #continue
	    #if reason == "GPU Xid 31":
	    #jobs[jobid]['software'][reason].toPrint = False
	    if user == 'user':
		    jobs[jobid][category][reason].toPrint = True
	    else:	 
		    jobs[jobid][category][reason].toPrint = False
  return jobs

def printEntry(jobid, category, reason, nodes, startTime, endTime):
  out = []
  out.append(str(jobid))
  out.append(category)
  out.append(reason)
  out.append(str(startTime))
  out.append(str(endTime))
  out.append(" ".join(jobs[jobid][category][reason].nodes))
  print ("\t".join(out))
  file.write("\n")
  file.write(str(out))

def checkRedundant(key1, key2, table):
  if key1 in table and key2 in table:
    if table[key1].toPrint and table[key2].toPrint:
        node1 = table[key1].nodes[0]
        node2 = table[key2].nodes[0]
        if node1 == node2:
	        return True
  return False
     	

def outputAll(jobs):
  for jobid in jobs:
    for category in jobs[jobid]:
      for reason in jobs[jobid][category]:
	      if jobs[jobid][category][reason].toPrint:
	      #if reason == "GPU Xid 31" or reason == "Out of Memory":
	      #if reason == "Out of Memory":
	          printEntry(jobid, category, reason, jobs[jobid][category][reason].nodes, jobs[jobid][category][reason].startTime, jobs[jobid][category][reason].endTime)

def output(jobs):
  for jobid in jobs:
    #cross check, if the same node reports both software and hardware
    #failures, remove the software failure entry
    if len(jobs[jobid]) == 2:
        hardfailure_nodes = []
        #both hardware and software failures reported
        for reason in jobs[jobid]['hardware']:
	        hardfailure_nodes.extend(jobs[jobid]['hardware'][reason].nodes)
      
        softwareFailures = jobs[jobid]['software']
        for reason in softwareFailures:
	        remove = True
	        nl = list(jobs[jobid]['software'][reason].nodes)
	        for node in nl:
	            if node not in hardfailure_nodes:
	                remove = False
	            else:
	                if node in jobs[jobid]['software'][reason].nodes:
	                    jobs[jobid]['software'][reason].nodes.remove(node)

	        if remove:
	            jobs[jobid]['software'][reason].toPrint = False
	  
    #check redundant software failures
    if 'software' in jobs[jobid] and len(jobs[jobid]['software']) > 1:
        key1 = 'GPU BUS'
        key2 = 'GPU Xid 62'
        if checkRedundant(key1, key2, jobs[jobid]['software']):
	        jobs[jobid]['software'][key2].toPrint = False
    
    #check redundant hardware failures
    if 'hardware' in jobs[jobid] and len(jobs[jobid]['hardware']) > 1:
        key1 = 'GPU DBE'
        key2 = 'GPU DPR'
        if checkRedundant(key1, key2, jobs[jobid]['hardware']):
	        jobs[jobid]['hardware'][key2].toPrint = False
    
	
    outputAll(jobs)
	
if len(sys.argv) > 1:
  fileName = sys.argv[1]
  file = open("filter_failure_2015_filterfailure.txt", 'w')
  file.write("[Job ID  |  Category  |  Reason   |   StartTime   |   EndTime   |    Nodes]")
  jobs = failureFilter(fileName)
  outputAll(jobs)
  file.close()
  print("Output file: filterfailure_out.txt")
else:	
  print ("ERROR, usage: %s <file>" % sys.argv[0])
  print ("<file>: output from failurejob.py")
  sys.exit(0)
