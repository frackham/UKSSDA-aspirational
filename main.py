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
import datetime
import logging
import urllib
import webapp2
import jinja2
import os
from developer import *
from fragmentrequester import *
from system import *

from mail.relativeimport import relimport_demo
relimport_demo() #TODO: [e] Use this pattern to refactor project. 

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db
from google.appengine.api import users

   

class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        logging.info("Page request: MainPage")
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Greeting.all().ancestor(
            guestbook_key(guestbook_name)).order('-date') #TODO: [i] Remove.
        greetings = greetings_query.fetch(10) #TODO: [i] Remove.

        user_name = "Anonymous User"
      
        app_title = "Secondary School Analysis"
        app_uri = "Unknown URI"
        app_referer_type = ""
        n=0
        for name in os.environ.keys():
          n+=1
          s = "" + name
          if "HTTP_REFERER" in s:
            app_uri = os.environ[name]

        app_uri = os.environ.get('SERVER_NAME')
        if "localhost" in app_uri:
          app_referer_type = "Local development"
          app_referer_HTMLid = "localtitle"
          livelink = "<li><a href=\"http://fr-testapp.appspot.com/\">This App Live (Application)</a></li>"
        else:
          app_referer_type = "Live environment"
          app_referer_HTMLid = "livetitle"
          livelink = "" #no need to link to live app if

        nav = {}
        nav['admin'] = ""
        accessrights = []
        bUserExists = False
        #Auth process: (1) Get user access rights through login (if not logged in, login).
        if users.get_current_user():
            bUserExists = True
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user = users.get_current_user()
            user_name = user.nickname()
            
            #TODO: [c] Here, get user access rights (currently adding admin rights to all logged in users) from a group in datastore. Most likely move whole function to auth library.
            user.accessrights = accessrights #Note accessrights is tuple, nav is dict.
            user.accessrights.append("admin")
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        #Auth process: (2) Append appropriate nav based on access rights.
        bDoAdmin = False #HACK: [e] Separate variable for each nav group? No thanks, [refactor] on move to separate auth layer.
        if app_referer_type == "Local development": 
          bDoAdmin = True
        if bUserExists: 
          if "admin" in user.accessrights: 
            bDoAdmin = True
        if bDoAdmin:
          nav["admin"] = """<li><a href=\"#\">Admin</a>
          	<ul>
          		<li class=\"primarynav\" id=\"admin-schooldetails\">    <a href=\"#\">School Details</a></li>
          		<li class=\"primarynav\" id=\"admin-datasetexplorer\">  <a href=\"#\">Dataset Explorer</a></li> <!-- #TODO: [e] Visual view of datasets. Add datasets from here (including descriptive only datasets). Consider using http://timeline.verite.co/  -->
          		<li class=\"primarynav\" id=\"admin-datasetvalidation\"><a href=\"#\">Dataset Validation(?)</a></li>
          		<li class=\"primarynav\" id=\"admin-adddataset\">       <a href=\"#\">Create New Dataset</a></li>
          		<li class=\"primarynav\" id=\"admin-usersetup\">        <a href=\"#\">User Setup</a></li>
          		<li class=\"primarynav\" id=\"admin-scheduledtasks\">   <a href=\"#\">Scheduled Tasks</a></li>
          		<li class=\"primarynav\" id=\"admin-flushdatastore\">   <a href=\"#\">Flush Data Store</a></li>
          	</ul>	
          </li>"""     
            
            
            
            
            
        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            'nav_access_admin': nav["admin"],
            'header_title': str(app_title) + ": " + str(app_referer_type),
            'app_title': "<h1 class=\"title\" id=\"" + app_referer_HTMLid + "\">" + str(app_title) + ": " + str(app_referer_type) + "</h1>",
            'user_name': user_name,
            'livelink':livelink,
            'app_type_environment': app_referer_type,
        }
        
        logging.debug(" Nav access: Admin Block == " + nav["admin"])
        
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        logging.info("Page write: MainPage")

        
class Guestbook(webapp2.RequestHandler): #TODO: [i] Remove.
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))



bAnonymisedMode = "True" #Get this from user settings. If usertype is admin or school user, then False. If not part of the school staff, should be anonymised...
config = {'anonymisedmode': bAnonymisedMode} #Use this to pass global config values to the route handlers.
	




#Match dev routes manually, as these will often be routed to different handlers.
app = webapp2.WSGIApplication([
      webapp2.Route('/', handler=MainPage, name = ''),
      #webapp2.Route('/login', handler=Login, name = 'Login'), #Comment this line out to skip login to anonymous. 
      webapp2.Route('/dev/ajaxtest', handler=DevSchoolList, name = 'DevSchoolList'),
      webapp2.Route('/dev/crudtest', handler=CRUDTest_GDS, name = 'CRUDTest_GDS'),
      webapp2.Route('/<:(admin)>/<:(scheduledtasks)>', handler=RedirectRequestHandler, name = 'admin-scheduledtasks'),
      webapp2.Route('/<:(dev)>/<:(pdftemp)>', handler=ObjectRequestHandler, name = 'objectrequest'),
      webapp2.Route('/<:(admin|assessment|school|student|behaviour|curriculum|attendance|dev|extension|fragment)>/<:[a-z]*>', handler=HTMLRequestHandler, name='analysis'),      
      webapp2.Route('/<:dev>/<:addschool>', handler=HTMLRequestHandler, name = 'addschool'),
      ], config=config)
System = EdSystem  #TODO: [i] Consider which aspects of this file need moving to the system object.


def main():  #TODO: [i] This is not being called - mainpage is doing all this, handled by the routing. Look at what should be part of this, and remove unnecessary parts [refactor].
    # Set the logging level in the main function
    # See the section on Requests and App Caching for information on how
    # App Engine reuses your request handlers when you specify a main function
    app_uri = os.environ.get('SERVER_NAME')
    logging.info("*******Main*******")
    if "localhost" in app_uri:
      app_referer_type = "Local development"
      logging.getLogger().setLevel(logging.DEBUG)
      logging.debug("*DEBUG Logging set*")
    else:
      app_referer_type = "Live environment"
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
  logging.info("Start.")
  main()
