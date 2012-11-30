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
    self.githublink = ""
    self.passedUnitTests = False #TODO: [d] Get version number here.
    pass
  def __str__(self):
    return ("Education analysis system. Version " + str(self.version) + 
           ". Created by Fraser Rackham (2012). This project can be forked from the Github repository at " +
           str(self.githublink))
    
    
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