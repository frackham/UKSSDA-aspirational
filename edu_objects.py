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

from google.appengine.ext import db
from google.appengine.api import users


#DATASET, SCHOOLCOLL, SCHOOL, STUDENTCOLL, STUDENT
#Use...
# -- https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses
#...to set correct data types.

#NEXT: Use ReferenceProperty for one to many relationship. https://developers.google.com/appengine/articles/modeling

class Dataset(db.Model):
  """Models an individual School entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  dateOfReference = db.DateTimeProperty()
  datasetShortName = db.StringProperty(default='Unnamed Dataset')
  datasetDescription = db.StringProperty(default='No description added for this dataset.',multiline=True)

class School(db.Model):
  """Models an individual School entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  schoolName = db.StringProperty(default='')
  schoolDescription = db.StringProperty(default='',multiline=True)

class StudentColl(db.Model):
  """Models an collection of Student entities with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  studentCollName = db.StringProperty(default='')
  studentCollDescription = db.StringProperty(default='',multiline=True)

class Student(db.Model):
  """Models an individual Student entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  studentName = db.StringProperty(default='')
  studentYear = db.IntegerProperty(default=0)
  
  
class feedback():
  """ to useas class storing feedback fro  users  """
  pass
 
  
#TODO: NEXT STEP: How to put in the school? What is the key for? How to retrieve?
def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

  
