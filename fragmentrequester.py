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
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter, A4
#import renderpdf

folderFonts = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'

import unittest
from google.appengine.ext import testbed

from google.appengine.ext import db
from google.appengine.api import users

from edu_objects import *
from external_sources import *
from developer import *
from dal_temp import *
from data.dal import *
from codeanalysis.codeanalysis import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AuthHandler(webapp2.RequestHandler):     
  def get(self, category, subcategory):         
    user = users.get_current_user()         
    if user:             
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))         
    else:             
      greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/"))          
    #2013-01-02 14.22.17.jpg. # TODO: [d]move response to auth.py
    self.response.out.write("<html><body>%s</body></html>" % greeting) #TODO: [d] Use this section to return the fragment to a specific DIV.
    
    
class RedirectRequestHandler(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self, category, subcategory):
    logging.info("Page request: RedirectRequestHandler:" + category + ":" + subcategory)
    handlerByName = category + "_" + subcategory
    uriByName = category + "/" + subcategory #HACK: [i] [refactor] handlerbyname function should identify URI, and return that as a string here to be redirected to.
    if handlerByName in globals():
      logging.info("Page redirection: RedirectRequestHandler:" + uriByName)
      return webapp2.redirect(uriByName)
    else:
      self.response.out.write("Redirect Handler (" + handlerByName + ") not yet defined. Come back later!")

      
      
class ObjectRequestHandler(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self, category, subcategory):
    logging.info("Page request: ObjectRequestHandler:" + category + ":" + subcategory)
    handlerByName = category + "_" + subcategory    
    if handlerByName in globals():
      #TODO: [e] The whole of this if branch needs moving out into a separate object handler - ideally, we should be able to get the type of handler required from the handlerName (or passed as other argument).
      #self.response.out.write("PDFTEST")
      logging.info("PDFStep1")
      text = handlerByName
      logging.info("PDFStep2")
      p = canvas.Canvas(self.response.out, pagesize=A4) # try to find some resources through REPORTLAB and then   http://en.wikipedia.org/wiki/Pdf
      logging.info("PDFStep3")
      #p.drawImage('dog.jpg', 150, 400) #TODO: [d] This is how you return an image dynamically. See reportlab documentation.
      p.drawString(50, 700, 'The text you entered: ' + text)
      logging.info("PDFStep4")
      #p.setFont('Arial', 16)
      #p.drawString(50, 600, 'DarkGarden font loaded from reportlab.zip')
      p.showPage()
      logging.info("PDFStep5")
      self.response.headers['Content-Type'] = 'application/pdf'
      logging.info("PDFStep6")
      self.response.headers['Content-Disposition'] = 'attachment; filename=temppdf.pdf' #Added attachment content-disposition as per Jokob Nielsen's usability recommendation. http://www.useit.com/alertbox/open_new_windows.html 
      logging.info("PDFStep7")
      p.save()
      logging.info("PDFStep8")
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
    logging.info(self.request.path) #TODO: This returns the path requested, so might be a better way of handling this [refactor].
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
      #if methodToCall[0:5] == "PDF!!":
      #  #self.response.out.write("PDFTEST")
      #  self.response.headers['Content-Type'] = 'application/pdf'
      #  p = canvas.Canvas(self.response.out)
      #  p.drawString(100, 750, "Hey, it's easy!.")
      #  p.showPage()
      #  p.save()
      #else:
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
def user_authenticate():
  users.create_logout_url("logout")
  auth_fragment = users.create_login_url("login")
  return '{{ auth_fragment }}'

def admin_datasetexplorer():
  return datasets_plotbydate()

def admin_adddataset():
  return datasets_add_form()
  
def admin_scheduledtasks():
  return '/_ah/admin/cron'
   
def admin_flushdatastore():
  return DAL_FlushDataStore()

def school_context():
  """School Context"""
  """ use schoolcontext in fragments."""
  return "School Context CALLED!"   

def attendance_summary():
  """Attendance within Groups"""
  return CurrentDatasetAttendanceOverview() 

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
  return school_addschool_temp()

def dev_loadtempstrut():
  return tempSchoolSetup()

def dev_addstudenttoschool():
  return "dev_addstudenttoschool CALLED!"   

def dev_listallstudents():
  return DALReturnAllStudents()
  
def dev_pdftemp():
  return "PDF!!"

def dev_unittestoutcomes():
  return "UNIT TEST TEXT FILE HERE"
  
def dev_fonttestpage():
  return fonttestpage()
  
def fragment_schoollist():
  return demo_DALDataStoreQuery()  

def fragment_schoolcount():
  return tempSchoolSetup()
  
def extension_edubase():
  return scrape_edubase()
  
  
def tasks_summary():
  #TODO: [i] Name this semantically. What is it, not how often it runs.
  logging.info("Scheduled task triggered - tasks summary.")
  outcomeCallback = "DAILY" #Outcome 
  retStr = str(datetime.datetime.now()) +  ": " + outcomeCallback
  logging.info(retStr)
  return "Scheduled Task executed: " + retStr

def tasks_weekly():
  #TODO: [i] Name this semantically. What is it, not how often it runs.
  logging.info("Scheduled task triggered - weekly task.")
  outcomeCallback = "WEEKLY" #Outcome 
  retStr = str(datetime.datetime.now()) +  ": " + outcomeCallback
  logging.info(retStr)
  return "Scheduled Task executed: " + retStr
  
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
