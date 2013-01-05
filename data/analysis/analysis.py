def verifyStatistic(statistic):
	"""if statistic is a statistic object, return same. else get statistic"""
	return statistic

def getStatisticOfDatasets(statistic, datasets):
	""" returns statistics for one or more datasets for all schools in datasets """
	"""asuumes acting on school!"""
	#currently assumes 1 school.
	thisDataset = datasets[0]
	thisSchool = thisDataset.Schools[0] #get school(s) of datasets.
	
	#get statistic definition from system. from statisticString.
	#	if statistic is a string, replace with statistic object.
	vStatistic =verifyStatistic(statistic)
	#currently assumes Average Attendance.
	lst=[] #return array.
	schools = [] 
	
	schools.append(thisSchool)
	
	for sch in schools:
		lst.append(getStatisticOfSchool(vStatistic, sch)
		
	pprint(lst)

def getStatisticOfSchool(statistic, school):
	
	vStatistic = verifyStatistic(statistic)
	