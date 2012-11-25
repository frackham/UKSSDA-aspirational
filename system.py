#!/usr/bin/env python

class EdSystem():
  def __init__(self):
    #TODO: Check status of unit test strut here?
    self.metrics=[]
    pass
  
  def Metric(self, metricname):
    """
    Returns a system defined metric by name
    """
    for metric in self.metrics:
      if metric.name == metricname:
        return metric
    return null
  
  def AddMetric(self, metric):
    #Check if type is metric here && if already exists...then self.metrics[].append(metric)
    pass
    
class Metric():
  """ Previously called Statistic. 
      Defines a calculation used in the system.
  
  """
  def __init__(self, name, description):
    #TODO: Add owner, referenceURI, prerequisites[], 
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

class Analysis():
  """ Returns the data model required for a representation.
      Note that this is somewhat analagous to the Model in MVC pattern, in that 
      it is representation agnostic.
  """
  def __init__(self, name, description):
    #TODO: Prerequisite metrics.
    self.name = name
    self.description = name
    pass
    
  def Name(self):
    return self.name
  def Description(self):
    return self.name
    
if __name__ == '__main__':
  System = EdSystem
  """
  for metric in metrics.txt:
    System.AddMetric(metric)
  
  """