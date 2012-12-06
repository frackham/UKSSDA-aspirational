#!/usr/bin/env python
#

from google.appengine.ext import db
from google.appengine.api import users


#DATASET, SCHOOLCOLL, SCHOOL, STUDENTCOLL, STUDENT
#TODO: [e] Use...-- https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses
#...to set correct data types.

#TODO: [i] Use ReferenceProperty for one to many relationship. https://developers.google.com/appengine/articles/modeling

class Dataset(db.Model):
  """Models an individual School entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  dateOfReference = db.DateTimeProperty()# Indicates the date that the dataset refers to. This is what shows on the timeline!
  datasetShortName = db.StringProperty(default='Unnamed Dataset')
  datasetDescription = db.StringProperty(default='No description added for this dataset.',multiline=True)
  datasetStatus = db.StringProperty(default='placeholder') #TODO: [e] Manage lifecycle of dataset from non-existent (impossible by definition), to placeholder, to minimal, to incomplete, to complete.
  #TODO: [e] add fields: assessmentType [estimates, targets, results, current-working, current-possible(?).
  datasetTags = db.StringProperty(default='placeholder') #TODO: [d] Tags would be single line comma separated. Does that make it parseable or not? Ber in mind that few datasets though, mainly internally used.
  datasetLog = db.StringProperty(default='placeholder') #TODO: [e] Does History/Log need to be an additional object (would be under OO paradigm) , or is it ok as a long string object that will be handled separately later? Probably would use this on other objects (e.g. School), so maybe...
  
class DatasetSource(db.Model):
  """ Indicates the source of the data for a specific data area for a given dataset. """
  dataset = db.Dataset # TODO: [c] This is the parent dataset. Each dataset will have multiple datasetsources
  domainArea = string  # TODO: [e] DatasetSource.domainareas are Assessment, Behaviour, Attendance, Staff, Premises etc.
  sourceType string  #TODO: [e] sourcetype is either "new" (new dataset source file...stored as string object in this object?), "inherit", "peryear (where we'll need to define these per year (targetYear != All).
  inheritSource = db.Dataset  #TODO: [e] Inherit dataset. Is this nullable, or should it be the parent dataset as default?
  fileSource = file #TODO: [d] Ideally, keep data with the dataset. Thus export of dataset = 'for each dataset source, save to file'.
  targetYear = string(?) #TODO: [e] 
  sourceYear = string(?) #TODO: [e] Usually empty, but exists so that you can inherit Y7 data at start of Y8.

class School(db.Model):
  """Models an individual School entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  schoolName = db.StringProperty(default='')
  schoolDescription = db.StringProperty(default='',multiline=True)
  #TODO: [e] headteacher (staff or string), postcode, address (long string for now), urn, schooltype, ofstedinspections{date, judgement pairs), nextearliestinspection.

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
  #TODO: [e] add attendance, classes (arr)
  #TODO: [e] add summary assessment values for proof.
  #TODO: [d] add proper assessment.
  #TODO: [d] add other attendance values.
  
class Staff(db.Model):
  """Models an individual Staff entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  staffName = db.StringProperty(default='')
  #TODO: [e] add classes (arr)

class Feedback(db.Model):
  """ To use as class storing feedback from users. """
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  userID = db.StringProperty(default='') #Check this one. See GApps Reference.
  feedbackContent = db.StringProperty(default='')
  feedbackType = db.StringProperty(default='Annotation') #To allow multiple types of feedback system to co-exist.
  """TODO: [i] Types: 
       Annotation (personal annotation on a specific dataset analysis).
       Comment (Response to a feedback section).
       Reply (Comment with parent Comment?).
       Message ().
       SystemFeedback (Feedback sent through an explicit feedback system).
  """
  
  pass
 
  
#TODO: [i] NEXT STEP: How to put in the school? What is the key for? How to retrieve?
def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

  
