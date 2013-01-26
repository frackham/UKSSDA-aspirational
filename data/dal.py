import logging
from google.appengine.ext import db
from edu_objects import *
from persistence.filehandler import *



#Upload file
# http://blog.notdot.net/2009/9/Handling-file-uploads-in-App-Engine

# Memcache:
# https://developers.google.com/appengine/docs/python/memcache/usingmemcache?hl=en
# Don't want to cache everything...do want to use manual caching via Dataset.Cache

#TO ADD LIST: (CRUD)
# CreateOBJECT
# ReadOBJECT
# UpdateOBJECT
# DeleteOBJECT
#   Create group of OBJECTs (pass in array?). Not handled by ancestor? Under Expert GRASP Model, should be handled by parent collection.


def School_Create(cSchool):
  logging.info("DAL: School_Create function.")
  #Note that we cannot amend a key_name after it has been set, so this assumes that the school has already had a key set. 
  #Note that this doesn't add a dataset.
  
  #VALIDATE HERE.  
  if cSchool.name:    
    #CREATE LOGIC HERE
    cSchool.put() #If school already exists, should replace.
    logging.info("DAL: Created School. (" + cSchool.name + ")")
    logging.debug("School entry: " + str(cSchool))
  else:
    logging.info("DAL: Could not create school. (" + str(cSchool) + ")") #Assumes passed object has a str method defined.

def School_Read(SchoolName):
  pass    

def School_Update(cSchool):
  pass

def School_Delete(cSchool):
  logging.info("DAL: School_Delete function.")
  pass
      
def Student_Create(cStudent):
  logging.info("DAL: Student_Create function.")
  #Note that we cannot amend a key_name after it has been set, so this assumes that the school has already had a key set. 
  #Note that this doesn't add a dataset.
  
  #VALIDATE HERE.  
  if cStudent.name:    
    #CREATE LOGIC HERE
    cSchool.put() #If Student already exists, should replace.
    logging.info("DAL: Created Student. (" + cStudent.name + ")")
    logging.debug("Student entry: " + str(cStudent))
  else:
    logging.info("DAL: Could not create school. (" + str(cSchool) + ")") #Assumes passed object has a str method defined.

def Student_Read(StudentName):
  pass    

def Student_Update(cStudent):
  pass

def Student_Delete(cStudent):
  logging.info("DAL: Student_Delete function.")
  pass