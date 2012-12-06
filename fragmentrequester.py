#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import logging
import datetime
import time
import urllib
import webapp2
import os
import jinja2
#import wsgiref.handlers
import sys

sys.path.insert(0, 'reportlab.zip') #enables import of reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter, A4
#import renderpdf
import reportlab
folderFonts = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'

import unittest
from google.appengine.ext import testbed

from google.appengine.ext import db
from google.appengine.api import users

from edu_objects import *
from dal_test import *
from dal import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class ObjectRequestHandler(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self, category, subcategory):
    logging.info("Page request: ObjectRequestHandler:" + category + ":" + subcategory)
    handlerByName = category + "_" + subcategory    
    if handlerByName in globals():
      #TODO: [e] The whole of this if branch needs moving out into a separate object handler - ideally, we should be able to get the type of handler required from the handlerName (or passed as other argument).
      #self.response.out.write("PDFTEST")
      text = handlerByName
      p = canvas.Canvas(self.response.out, pagesize=A4) # try to find some resources through REPORTLAB and then   http://en.wikipedia.org/wiki/Pdf
      #p.drawImage('dog.jpg', 150, 400) #TODO: [d] This is how you return an image dynamically. See reportlab documentation.
      p.drawString(50, 700, 'The text you entered: ' + text)
      #p.setFont('Arial', 16)
      #p.drawString(50, 600, 'DarkGarden font loaded from reportlab.zip')
      p.showPage()
      self.response.headers['Content-Type'] = 'application/pdf'
      self.response.headers['Content-Disposition'] = 'attachment; filename=testpdf.pdf' #Added attachment content-disposition as per Jokob Nielsen's usability recommendation. http://www.useit.com/alertbox/open_new_windows.html 
      p.save()
      #Up to here needs pulling out. All of it assumes a PDF object.
      
      #KEEP THESE TWO COMMENTS.
      #TODO: [e] Add test of object *returned by handler function*, in order to return it using the right methods of self.response().
      #Objecthandler itself only takes an object request, gets the *object* from the function, and returns it *appropriately as according to the object type*.
    else:
      self.response.out.write("Object Handler (" + handlerByName + ") not yet defined. Come back later!")
    
class HTMLRequestHandler(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self, category, subcategory):
    logging.info("Page request: GlobalRequestHandler:" + category + ":" + subcategory)
    #self.response.out.write("!!GlobalRequestHandler from regex!:" + category + ":" + subcategory)
    #self.response.out.write("  Settings:" )
    #self.response.out.write("    Anonymised Mode:" + self.app.config['anonymisedmode'])
    handlerByName = category + "_" + subcategory    
    #self.response.out.write(str(globals()))
    if handlerByName in globals():
      #TODO: [e] Only works if returning a string.
      #Debug mode.
      methodToCall = globals()[handlerByName]() #Returns a string.
      
      #HACK: use first 5 chars to determine response...
      if methodToCall[0:5] == "PDF!!":
        #self.response.out.write("PDFTEST")
        self.response.headers['Content-Type'] = 'application/pdf'
        p = canvas.Canvas(self.response.out)
        p.drawString(100, 750, "Hey, it's easy!.")
        p.showPage()
        p.save()
      else:
        self.response.out.write(methodToCall)
      
       #Live mode
      """try: 
        methodToCall = globals()[handlerByName]()
        self.response.out.write(methodToCall)
      except:
        self.response.out.write("Analysis failed.")"""
    else:
      self.response.out.write("Analysis (" + handlerByName + ") not yet defined. Come back later!")

    """for i in range(1,10):
      time.sleep(1)
      self.response.out.write(i)
    """ 
        
        
def demodata():
  return "dev-analysisloaderdemo CALLED!"
  #return [1,2,3,4,5,6]

    
          
def doDisplayAnalysis(requestHandler, datafunction, completefunction):
  #Display progress bar.
  time.sleep(0.5) #Wait a while (DEBUG).
  data = datafunction()
  requestHandler.response.clear()
  requestHandler.response.out.write(completefunction())
  time.sleep(0.5) #Wait a while (DEBUG).
  

  




  
  
  
  
#result = methodToCall()
#m = globals()['our_class']()

# Get the function that we need to call, and call it
#func = getattr(m, 'function_name')
#func()


#Each analysis needs a function here.        
#NOTE: careful of dashes, they become underscores here.

def admin_datasetexplorer():
  return datasets_plotbydate()

def admin_flushdatastore():
  return DAL_FlushDataStore()

def school_context():
  """School Context"""
  """ use schoolcontext in fragments."""
  return "School Context CALLED!"   


def attendance_groups():
  """Attendance within Groups"""
  return "ATTENDANCE GROUPS CALLED!"   
        
def dev_analysisloaderdemo():
  """May need changing to return a string!"""
  self.response.out.write("1!")
  doDisplayAnalysis(self, demodata, dev_analysisloaderdemo)  
  return ("2!") 
  

def dev_listschools():
  return DALReturnAllSchools()

def dev_addschool():
  return school_addstudent_test()

def dev_loadteststrut():
  return testSchoolSetup()

def dev_addstudenttoschool():
  return "dev_addstudenttoschool CALLED!"   

def dev_listallstudents():
  return DALReturnAllStudents()
  
def dev_pdftest():
  return "PDF!!"

def dev_unittestoutcomes():
  return "UNIT TEST TEXT FILE HERE"
  
def fragment_schoollist():
  return demo_DALDataStoreQuery()  

def fragment_schoolcount():
  return testSchoolSetup()
"""
Menu list:
Admin
		id="admin-schooldetails">    School Details
		id="admin-datasetexplorer">  Dataset Explorer <!-- Visual view of datasets. Add datasets from here (including descriptive only datasets). -->
		id="admin-datasetvalidation">Dataset Validation(?)
		id="admin-usersetup">        User Setup

School
		id="school-context">School Context
		id="school-temp">   Other Analyses
		

Students
		id="students-summary">Students Summary
		id="students-temp">   Other Analyses
		

Attendance
		id="attendance-summary">             Attendance Summary
		id="attendance-groups">              Attendance within Groups
		id="attendance-attainmentthresholds">Attendance against Thresholds
		id="attendance-temp">                Other Analyses
		

Behaviour
		id="behaviour-summary">Behaviour Summary
		id="behaviour-temp">   Other Behaviour Analyses
		

Assessment
		id="assessment-summary">Assessment Summary
		id="assessment-temp">   Other Assessment Analyses
		

Curriculum
		id="curriculum-summary">Curriculum Summary
		id="curriculum-temp">   Other Curriculum Analyses
		

Developer
  	id="dev-testclick">              School List
  	id="dev-ajaxtest">               Ajaxtest
  	id="dev-crudtest">               CRUD test (Data Store)
  	id="dev-qanparse">               QAN parse
  	id="dev-edubasescrape">          Edubase scrape
  	id="dev-addschool">              Add School
  	id="dev-showschools">            Show Schools
  	id="dev-addstudenttoschool">     Add Student to (Fixed) School
  	id="dev-showstudents">           Show Students of Schools
  	id="dev-analysisloaderdemo">     Analysis Loader Demo
		

Extension Demos
  	id="extension-location">Location
  	id="extension-news">    News
  	id="extension-ofsted">  OFSTED
		

Fragments in Progress
  	id="fragment-studentcount">Count(Students)
  	id="fragment-schoolcount">Count(School)
  	id="fragment-schoollist">List(School)
		
 
<li id="documents">Documents



"""







#unittesting
"""
class Case_AEqualsB(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    #policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
  def tearDown(self): self.testbed.deactivate()
  def test_insufficient_cash(self):
    intA = 1
    intB = 2
    with self.assertRaises(bank.InsufficientCash):
      bank.transfer_money('vc', 'brian', 5000000)  
      
"""
