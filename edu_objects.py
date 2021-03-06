#!/usr/bin/env python
#

from google.appengine.ext import db
from google.appengine.api import users


#DATASET, SCHOOLCOLL, SCHOOL, STUDENTCOLL, STUDENT
#TODO: [e] Use...-- https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses
#...to set correct data types.

#TODO: [i] Use ReferenceProperty for one to many relationship. https://developers.google.com/appengine/articles/modeling

#TODO: [d] Look at whether properties should be ProperCase instead of camelCase, so that calls are like Dataset.Name() instead of Dataset.name().

class Dataset(db.Model):
  """Models an individual School entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  dateOfReference = db.DateTimeProperty(auto_now_add=True)# Indicates the date that the dataset refers to. This is what shows on the timeline! #TODO: [e] Default dataset dateofreference is now(). Using auto_now_add=True for the moment.
  shortName = db.StringProperty(default='Unnamed Dataset')
  description = db.StringProperty(default='No description added for this dataset.',multiline=True)
  status = db.StringProperty(default='Placeholder') #TODO: [e] Manage lifecycle of dataset from non-existent (impossible by definition), to placeholder (default), to minimal, to incomplete, to complete.
  #TODO: [e] add fields: assessmentType [estimates, targets, results, current-working, current-possible(?).
  tags = db.StringProperty(default='') #TODO: [d] Tags would be single line comma separated. Does that make it parseable or not? Ber in mind that few datasets though, mainly internally used.
  log = db.StringProperty(default='') #TODO: [e] Does History/Log need to be an additional object (would be under OO paradigm) , or is it ok as a long string object that will be handled separately later? Probably would use this on other objects (e.g. School), so maybe...
  
class DatasetSource(db.Model):
  """ Indicates the source of the data for a specific data area for a given dataset. """
  dataset = db.ReferenceProperty(Dataset, verbose_name="Parent Dataset", collection_name='dataSources') 
  domainArea = db.StringProperty(default='Not set')  #TODO: [e] DatasetSource.domainareas are Assessment, Behaviour, Attendance, Staff, Premises etc.
  sourceType = db.StringProperty(default='Not set')  #TODO: [e] sourcetype is either "new" (new dataset source file...stored as string object in this object?), "inherit", "peryear (where we'll need to define these per year (targetYear != All).
  inheritSource = db.ReferenceProperty(Dataset, verbose_name="Inheriting-From Dataset", collection_name='sourcesThatInherit')  #TODO: [e] Inherit dataset. Is this nullable, or should it be the parent dataset as default? See https://developers.google.com/appengine/articles/modeling 
  #fileSource = file #TODO: [d] Ideally, keep data with the dataset. Thus export of dataset = 'for each dataset source, save to file'. See https://developers.google.com/appengine/docs/python/blobstore/blobinfoclass
  #TODO: [c] A DatasetSource can only inherit from EITHER inheritSource OR fileSource. Filesource should take priority. When either is changed, entity should be verified.
  targetYear = db.DateTimeProperty() #TODO: [e] target 
  sourceYear = db.DateTimeProperty() #TODO: [e] Usually empty, but exists so that you can inherit Y7 data at start of Y8.

class School(db.Model):
  """Models an individual School entry with appropriate properties.
  Most of the properties match with Edubase field descriptions.
  """
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  name = db.StringProperty(default='Empty School Name')
  description = db.StringProperty(default='Empty School Description.',multiline=True)
  #TODO: [e] headteacher (staff or string), postcode, address (long string for now), urn, schooltype, ofstedinspections{date, judgement pairs), nextearliestinspection.
  urn = db.IntegerProperty(default=0) #TODO: [e] School URN may need to be different number type (Int long enough?).
  dateOpened = db.DateTimeProperty(required = False)
  localAuthorityNumber  = db.IntegerProperty(required = False) #TODO: Split this from the LA string returned (split(val, " ")(0) = Number, (1) = Name)
  localAuthorityName = db.StringProperty(default='Empty')  
  establishmentNumber  = db.IntegerProperty(required = False) 
  headteacherString = db.StringProperty(default='Empty') 
  phaseOfEducation = db.StringProperty(default='Empty') 
  establishmentType = db.StringProperty(default='Empty')
  schoolSponsor = db.StringProperty(default='Empty') 
  ageRange = db.StringProperty(default='Empty') #TODO: [i] Break this down into min age and max age.
  gender = db.StringProperty(default='Empty') # TODO: Build validation check. If gender is Boys or Girls, and has Girls or Boys respectively, throw error.
  religiousCharacter = db.StringProperty(default='Empty')
  schoolCapacity = db.IntegerProperty(required = False)
  lastCensusRollCount = db.IntegerProperty(required = False) # (Total Number of Children) on Edubase.
  specialClasses = db.StringProperty(default='Empty')
  hasBoarders = db.StringProperty(default='Empty')
  nurseryProvider = db.StringProperty(default='Empty')
  inSpecialMeasures = db.StringProperty(default='Empty')
  freshStart = db.StringProperty(default='Empty')
  trustFlag = db.StringProperty(default='Empty')
  ukPRN = db.IntegerProperty(required = False)
  urbanRuralString = db.StringProperty(default='Empty')
  sixthForm = db.StringProperty(default='Empty')
 
#TODO: [e] Exclude libraries from tests.
#TODO: [c] Move School_Test to tests folder
#How to execute test suite: http://stackoverflow.com/questions/3160551/is-there-a-way-to-get-pythons-nose-module-to-work-the-same-in-main-and-on-t
#Convention for naming test files/classes etc.: http://stackoverflow.com/questions/1457104/nose-unable-to-find-tests-in-ubuntu/1457852#1457852
import unittest
class School_Tests(unittest.TestCase):
  def __init__(self):    
    self.modelCreatedUsingDefaults  = School()
    self.modelExpectedUsingDefaults = School(name='Empty School Name', description='Empty School Description.', urn=0)
  def test_model_created_using_defaults_matches_expected_defaults(self): 
    self.assertEquals(self.modelCreatedUsingDefaults, self.modelExpected)

class Student_Tests(unittest.TestCase):
  def __init__(self):    
    self.modelCreatedUsingDefaults  = Student()
    #self.modelExpectedUsingDefaults = Student(name='Empty School Name', description='Empty School Description.', urn=0) #TODO: Test against defaults [test].
  def test_model_created_using_defaults_matches_expected_defaults(self): 
    self.assertEquals(self.modelCreatedUsingDefaults, self.modelExpected)
  def test_attendance_not_below_0(self): 
    self.assertAbove(self.modelCreatedUsingDefaults.attendance, 0)  
  def test_attendance_not_above_100(self): 
    self.assertBelow(self.modelCreatedUsingDefaults.attendance, 100)  

def doUnitTests():
  pass
    

#---Up to here.

class StudentColl(db.Model):
  """Models an collection of Student entities with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  name = db.StringProperty(default='Unnamed Student Collection')
  description = db.StringProperty(default='Empty Student Collection Description.',multiline=True)
  students = []

class Student(db.Model):
  """Models an individual Student entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  name = db.StringProperty(default='')
  year = db.IntegerProperty(default=0)
  currentSchool = db.StringProperty(default='')
  #TODO: [d] add other attendance values.
  attendance = db.FloatProperty(required = False) # Handled this way so that can have null attendance
  attendance_lates = db.FloatProperty(required = False) 
  attendance_AEA = db.FloatProperty(required = False) #AEA is approved educational absence.
  attendance_authabsence = db.FloatProperty(required = False) 
  attendance_unauthabsence = db.FloatProperty(required = False) 
  
  assessment_has5AA = db.BooleanProperty(default=False)
  assessment_has5AC = db.BooleanProperty(default=False)
  assessment_has5AG = db.BooleanProperty(default=False)
  assessment_has1AG = db.BooleanProperty(default=False)
  
  group_isFSM  = db.BooleanProperty(default=False)
  group_isEAL  = db.BooleanProperty(default=False)
  group_SEN  = db.StringProperty(default='N')
  
  #TODO: [e] add attendance, classes (arr)
  #TODO: [e] add summary assessment values for proof.
  #TODO: [e] add proper assessment.
  
class StudentCategory(db.Model):
  categoryName = db.StringProperty(required = True)
  categoryValue = db.StringProperty(default = 'False')
 
class Staff(db.Model):
  """Models an individual Staff entry with appropriate property."""
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  name = db.StringProperty(default='')
  #TODO: [e] add classes (arr).
  #TODO: [i] add manualSubjects (arr)? How do we account for non-specialists? If teaching, it is not necessarily their subject. Need separate subject profile for each staff member (e.g. Teacher Departments).

class Feedback(db.Model):
  """ To use as class storing feedback from users. """
  dateAdded = db.DateTimeProperty(auto_now_add=True)
  dateUpdated = db.DateTimeProperty(auto_now=True)
  ownerUserID = db.StringProperty(default='') #TODO: [d] Check this one. See GApps Reference.
  feedbackContent = db.StringProperty(default='')
  feedbackType = db.StringProperty(default='Annotation') #To allow multiple types of feedback system to co-exist.
  """TODO: [i] Types: 
       Annotation (personal annotation on a specific dataset analysis).
       Comment (Response to a feedback section).
       Reply (Comment with parent Comment?).
       Message ().
       SystemFeedback (Feedback sent through an explicit feedback system).
  """
 
  
#TODO: [i] NEXT STEP: How to put in the school? What is the key for? How to retrieve?
def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

  
