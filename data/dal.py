import logging
from google.appengine.ext import db
from edu_objects import *




#Upload file
# http://blog.notdot.net/2009/9/Handling-file-uploads-in-App-Engine

# Memcache:
# https://developers.google.com/appengine/docs/python/memcache/usingmemcache?hl=en
# Don't want ot cache everything...

#TO ADD LIST: (CRUD)
# CreateOBJECT
# ReadOBJECT
# UpdateOBJECT
# DeleteOBJECT
#   Create group of OBJECTs (pass in array?). Not handled by ancestor?


def School_Create(cSchool):
  logging.info("DAL: School_Create function.")
  #Note that we cannot amend a key_name after it has been set, so this assumes that the school has already had a key set. 
  
  #VALIDATE HERE.  
  if cSchool.schoolName:    
    #CREATE LOGIC HERE
    cSchool.put() #If school already exists, should replace.
    logging.info("DAL: Created School. (" + cSchool.name + ")")
    logging.debug("School entry: " + str(cSchool))
  else:
    logging.info("DAL: Could not create school. (" + str(cSchool) + ")") #Assumes passed object has a str method defined.
