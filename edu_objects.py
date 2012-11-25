#!/usr/bin/env python
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
  
  
class Feedback(db.Model):
  """ To use as class storing feedback from users. """
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  userID = db.StringProperty(default='') #Check this one. See GApps Reference.
  feedbackContent = db.StringProperty(default='')
  feedbackType = db.StringProperty(default='Annotation') #To allow multiple types of feedback system to co-exist.
  """Types: 
       Annotation (personal annotation on a specific dataset analysis).
       Comment (Response to a feedback section).
       Reply (Comment with parent Comment?).
       Message ().
       SystemFeedback (Feedback sent through an explicit feedback system).
  """
  
  pass
 
  
#TODO: NEXT STEP: How to put in the school? What is the key for? How to retrieve?
def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

  
