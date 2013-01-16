#!/usr/bin/env python


#***EdSystem***
class AbstractReport():
  """
    Class that.
    Should be semantic and content-based, not stylistic.
  """
  def __init__(self, name):
    #TODO: [e] Check status of unit test strut here?
    self.version = "alpha" #TODO: [d] Get version number here.
    self.prerequisites = []
    self.actions = [] #List of instructions, e.g. "Title()". As simple as possible.
    self.name = name
  def __str__(self):
    return self.name
  
  def AddAction(self, actionText):
    self.actions.append(actionText)

class OutputGenerator():
  """
    Base class for types of Report Generator (e.g. ExcelGenerator), which take an AbstractReport object and output the designated file type.
  """
  def __str__(self):

class AbstractionItemTemplate():
  def __init__(self, name):
    #TODO: [e] Check status of unit test strut here?
    self.name = name
  def __str__(self):
    return self.name

class ReportTextObject(AbstractionItemTemplate):
  def __init__(self, name, text):
    #TODO: [d] Text object should have definable styles here? Or a way to define them? Have a think, as don't really want to need to style...
    self.name = name

"""
AbstractReport object:
 Definition for the model for a report.
 
AbstractionItem
 e.g. Text, GraphContainer(GraphData, GraphImage), Image, 

OutputReport object:
 base class
 
ExcelGenerator:
 (defines how to convert from AbstractReport to Excel output.
  
PDFGenerator:
 (defines how to convert from AbstractReport to Excel output.
 
ODTGenerator:
 (defines how to convert from AbstractReport to ODT output.

ODSGenerator:
 (defines how to convert from AbstractReport to ODT output.
 
ODTGenerator:
 (defines how to convert from AbstractReport to ODT output.

TextGenerator:
 (defines how to convert from AbstractReport to Excel output.

HTML5Generator:
 (defines how to convert from AbstractReport to Excel output.

AbstractReport.fromTextFile(filename)


"""
if __name__ == '__main__':
  logging.info("Reportin demo.")
  analysisExample = AbstractReport("Example")
  #Set up the items:
  # Header text: <page>
  # Title:  
  # Text intro.
  # Table of data.
  # Chart image of data (type of chart?).
  # Text outro.
  # Footer text
  
  analysisExample.