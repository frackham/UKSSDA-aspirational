#!/usr/bin/env python


#***EdSystem***
class EdSystem():
  """
    Singleton class for handling global behaviours of metrics, analyses and overall system administration.
    
    #TODO [d] Add singleton behaviour (not really an issue if never redefined...).
  """
  def __init__(self):
    #TODO: [e] Check status of unit test strut here?
    self.metrics=[]
    self.version = "alpha" #TODO: [d] Get version number here.
    #TODO: [e] On process dataset, update calculationVersion of the Dataset. If calculationVersion != edsystem.version, then recalc dataset?
    self.githublink = "" #TODO: [i] Necessary?
    self.passedUnitTests = False #TODO: [e] Get most recent unit test outcomes (from dev_unittestoutcomes() ).
    self.abstractReportDefinitions = []
    pass
  def __str__(self):
    return ("Education analysis system. Version " + str(self.version) + 
           ". Created by Fraser Rackham (2012). This project can be forked from the Github repository at " +
           str(self.githublink))
  
  def ReportDefinition(self, file):
    if file.extension == ".txt": 
      if file.readline(0) == "UKSSDA REPORT DEFINITION":
        System.ReportDefinitions.append(file) #Does this store it in memory? How does that handle lots of definitions?
        return 1
      else:
        return 0
                      
  def AddReportDefinitionSet(self, folder):
    with folder:
      for file in folder:
        n = self.AddReportDefinition(file) #Returns 0 on fail.
        if n == 0:
          console.logging.debug("Report '" + file.name() +"' (no. " + str(reportCount) + ") failed to add to system object.")      
        reportCount += 1
        successCount += n
      console.logging.debug(str(successCount) + ", out of " + str(reportCount) + " possible files, report definitions added to system.")
    
  def Metric(self, metricname):
    """
    Returns a system defined metric by name
    """
    for metric in self.metrics:
      if metric.name == metricname:
        return metric
    return null
  
  def AddMetric(self, metric):
    """
     Adds an existing metric object to this EdSystem, making it available for use.
    """
    #Check if type is metric here && if already exists...then self.metrics[].append(metric)
    pass
    
    
#***Metric***
class Metric():
  """ Previously called Statistic. 
      Defines a calculation used in the system.
  
  """
  def __init__(self, name, description):
    #TODO: [c] Add owner, referenceURI, prerequisites[], (more next lines-->)
    #      0 or more [object:calculationDescription:returnType:calculationMechanism].
    #     e.g. 5AC [student:returns true if the student has 5 or more GCSEs at C or higher, accounting for XXX: boolean: if student.ValueCount(C+)>5 return true]
    self.name = name
    self.description = description
    pass
  def __str__(self):
    s= self.Name() + ": " + self.Description() + "/n" + \
    "  (Unit test    : Passed/Failed most recent unit tests on DATE)."  + "/n" + \
    "  (Prerequisites: Placehold for prereqs list)."
    return s
    
  def Name(self):
    return self.name
  def Description(self):
    return self.name

#***Analysis***
class Analysis():
  """ Returns the data model required for a representation.
      Note that this is somewhat analagous to the Model in MVC pattern, in that 
      it is representation agnostic.
  """
  def __init__(self, name, description):
    #TODO: [e] Prerequisite metrics.
    self.name = name
    self.description = description
    self.purpose = "TBA"
    pass
    
  def Name(self):
    return self.name
  def Description(self):
    return self.name
    
if __name__ == '__main__':
  System = EdSystem
  print(System)
  """
  for metric in metrics.txt:
    System.AddMetric(metric)
  
  """