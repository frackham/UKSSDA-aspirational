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
import urllib
import webapp2
import os
import jinja2

from google.appengine.ext import db
from google.appengine.api import users


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

        
class DevSchoolList(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self):
    logging.info("Page request: DevSchoolList")
    str=""
    for name in os.environ.keys():
      str += ("%s = %s<br />\n" % (name, os.environ[name]))
    self.response.out.write("!!get!!" + str)
    logging.info("Page write: DevSchoolList")

    
class CRUDTest_GDS(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("!!post!!")
  def get(self):
    logging.info("Page request: CRUDTest_GDS")
    #self.response.out.write("!!crud!")
    CRUDVal = "TEST"
    template_values = {
            'crudval': CRUDVal,
            'anonymisedmode': self.app.config.get('anonymisedmode')
        }
    template = jinja_environment.get_template('fragment1.html')
    self.response.out.write(template.render(template_values))   
    logging.info("Page write: CRUDTest_GDS")
    
def fonttestpage():
  retString = "<h3>Font test</h3>"
  #retString += "  <img src=\"/img/dataset_explorer.jpg\" alt=\"alt text\" height=\"184\" width=\"326\" />"
  testString = "A quick brown fox yadda yaddah jumping."
  retString+="<table class=\"fonttable\">"
  retString+=" <tr><td>Arial</td><td><span class=\"arial\">"+ testString +"</span></td></tr>"
  retString+=" <tr><td>Georgia</td><td><span class=\"georgia\">"+ testString +"</span></td></tr>"
  retString+=" <tr><td>Helvetica</td><td> <span class=\"helvetica\">"+ testString +" </span></td></tr>"
  retString+=" <tr><td>Verdana</td><td> <span class=\"verdana\">"+ testString +" </span></td></tr>"
  retString+=" <tr><td>Courier</td><td> <span class=\"courier\">"+ testString +" </span></td></tr>"

  retString+=" <tr><td></td><td></td></tr>"
  retString+=" <tr><td>Roboto</td><td> <span class=\"roboto\">"+ testString +" </span></td></tr>"
  retString+=" <tr><td>Quicksand</td><td> <span class=\"quicksand\">"+ testString +" </span></td></tr>"
  
  retString+=" <tr><td></td><td></td></tr>" 
  retString+=" <tr><td>Serif</td><td> <span class=\"serif\">"+ testString +" </span></td></tr>"
  retString+=" <tr><td>Sans Serif</td><td> <span class=\"sansserif\">"+ testString +" </span></td></tr>"
  retString+=" <tr><td>Monospace</td><td> <span class=\"monospace\">"+ testString +" </span></td></tr>"
  retString+="</table>"
  return retString