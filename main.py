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
            guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(10)

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


        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user = users.get_current_user()
            user_name = user.nickname()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'


        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            'header_title': str(app_title) + ": " + str(app_referer_type),
            'app_title': "<h1 class=\"title\" id=\"" + app_referer_HTMLid + "\">" + str(app_title) + ": " + str(app_referer_type) + "</h1>",
            'user_name': user_name,
            'livelink':livelink,
            'app_type_environment': app_referer_type,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        logging.info("Page write: MainPage")

        
class Guestbook(webapp2.RequestHandler):
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
      webapp2.Route('/dev/ajaxtest', handler=DevSchoolList, name = 'DevSchoolList'),
      webapp2.Route('/dev/crudtest', handler=CRUDTest_GDS, name = 'CRUDTest_GDS'),
      webapp2.Route('/<:(admin|assessment|school|student|behaviour|curriculum|attendance|dev|extensions|fragment)>/<:[a-z]*>', handler=GlobalRequestHandler, name='analysis'),      
      webapp2.Route('/<:dev>/<:addschool>', handler=GlobalRequestHandler, name = 'addschool'),
      ], config=config)
System = EdSystem 


def main():
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
    main()
