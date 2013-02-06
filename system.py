#!/usr/bin/env python
import logging
import main
import os, os.path, linecache

#***EdSystem***
class EdSystem():
  """
    Singleton class for handling global behaviours of metrics, analyses and overall system administration.
    #TODO: [e] Technically a singleton by convention only. Nothing enforces a single EdSystem (though only the one referenced in main.py will be accessible globally).
    Also exhibits Facade behaviour.
  """
  def __init__(self):
    #TODO: [e] Check status of unit test strut here?
    self.metrics=[]
    self.version = "alpha" #TODO: [d] Get version number here.
    #TODO: [e] On process dataset, update calculationVersion of the Dataset. If calculationVersion != edsystem.version, then recalc dataset?
    self.githublink = "https://github.com/frackham/UKSSDA-aspirational" #TODO: [i] Necessary?
    self.passedUnitTests = False #TODO: [e] Get most recent unit test outcomes (from dev_unittestoutcomes() ).
    self.abstractReportDefinitions = {}  #Dictionary of name:reportfile text pairings.
    self.rootPath = "." #Root application path.
    #logging.info(str(os.listdir(self.rootPath)))
    #x = self.filesCount(self.rootPath)
    #logging.info("There are " + str(x) + " files in rootPath")
    self.debugMode = False
    logging.info("SYSTEM object created")
    self.AddReportDefinitionSet(os.path.join(self.rootPath, "analysistemplates", "templates")) #This loads all the template analyses.
    pass
  def __str__(self):
    return ("Education analysis system. Version " + str(self.version) + 
           ". Created by Fraser Rackham (2012). This project can be forked from the Github repository at " +
           str(self.githublink))
  
  def filesCount(self, path):
    i = 0
    for (path, dirs, files) in os.walk(path):
      i += 1
    return i
           
  def debugMode(bool = True):
    if bool:
      self.debugMode = True
    else: 
      self.debugMode = False
        
  def SetCurrentFileBlob(self, BlobKey):
    self.currentblobkey = BlobKey         
  
  def GetCurrentFileBlob(self):
    return self.currentblobkey
               
  def Analysis(self, name): 
    if self.abstractReportDefinitions[name]: #If named analysis exists in System().
      analysisObject = Analysis(name, '') # TODO: [d] Blank '' desription at moment. Define in template file.
      #self.abstractReportDefinitions[name]
      state = "new"
      variables =[]
      html = []
      query = "SELECT * FROM Student LIMIT 3" #default.
      for line in self.abstractReportDefinitions[name]:
        line = line.rstrip() 
        #Get current location.
        if line == "VARIABLES:": #note colon at end of line state name.
          state = "VARIABLES"
        elif line == "HTML:": #note colon at end of line state name.
          state = "HTML"
        elif line == "QUERY:": #note colon at end of line state name.
          state = "QUERY"
        else:
          pass
        #Process depending on current location state.
        if state == "VARIABLES":
          if line != "VARIABLES" and line != "":
            variables.append(line.rstrip())
        elif state == "HTML":
          if line != "HTML" and line != "":
            html.append(line.rstrip())
        elif state == "QUERY":
          if line != "QUERY" and line != "":
            query = line.rstrip()
        else:
          pass
        logging.info(state + ": " + line)
      analysisObject.variables= variables
      #logging.info(name + ":variables:" + str(variables))
      analysisObject.html = html
      analysisObject.query= query
      #logging.info(name + ":html:" + str(html))
      return analysisObject  
    else:
      logging.info("Could not find " + name + " in system.abstractReportDefinitions.")
      return False
      
    
  def AddReportDefinition(self, path, file):
    logging.info("Checking if potential report definition '" + str(file) + "' is a text file... [" + file[-4:] + "]")
    if file[-4:] == ".txt": 
      logging.info("Attempting to add report definition for '" + str(file) + "'.")
      with open(os.path.join(path, file)) as f:
        firstLine = f.readline().rstrip()
        secondLine = f.readline().rstrip()
        #logging.info(str(firstLine ))
        if firstLine == "UKSSDA REPORT DEFINITION":
          templateName = secondLine 
          #logging.info(templateName)
          self.abstractReportDefinitions[templateName] = f.readlines() 
          #logging.info(self.abstractReportDefinitions[templateName])
          return 1
        else:
          return 0
                      
  def AddReportDefinitionSet(self, sTemplatepath):
    logging.info("Report templates are located in: " + sTemplatepath)
    nCount=0
    for (path, dirs, files) in os.walk(sTemplatepath):
      for name in files:
        logging.info(name)
        nCount += self.AddReportDefinition(path, name)
    logging.info(str(nCount) + " analysis templates added to system: " + str(self.abstractReportDefinitions))
  
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
  def __init__(self, name, description = '', variables = [], html=''):
    #TODO: [e] Prerequisite metrics.
    self.name = name
    self.description = description
    self.purpose = "TBA"
    self.variables = variables
    self.html = html
    pass
    
  def Name(self):
    return self.name
  def Description(self):
    return self.description
    
if __name__ == '__main__':
  System = EdSystem
  print(System)
  """
  for metric in metrics.txt:
    System.AddMetric(metric)
  
  """     
