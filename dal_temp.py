import logging
import random
from datetime import datetime
from google.appengine.ext import db
from edu_objects import *
from data.dal import *
from data.gendata import *

#For file upload.
from google.appengine.ext import blobstore 
from google.appengine.ext.webapp import blobstore_handlers 

def getCurrentDataset():
  #dal_temp returns a default dataset. In actual DAL, this should return the current dataset in use.
  dataset =  Dataset(key_name="Demo Dataset")
  return dataset 
  
def CurrentDatasetAttendanceOverview():
  retString = "<p>Attendance Overview</p>"
  dataset = getCurrentDataset()
  test_query = Student.all()
  test_query.ancestor(dataset)
  totAtt = 0
  students = 0
  for item in test_query.run():
    students += 1
    totAtt+=item.attendance
    retString+="<p>Att: "+str(item.attendance) +"</p>" 
  retString+="<p>Att average: "+str(totAtt/students) +"</p>"   
  return retString
  

@db.transactional
def tempSchoolSetup():
  retString = ""
  
  datasetRefDate = (datetime(2000,1,1))
  dataset =  Dataset(key_name="Demo Dataset", dateOfReference=datasetRefDate) #datasetShortName, datasetDescription.
  dataset.put()

  schoolA = School(key_name="Test School A", parent=dataset, name="Test School A", description="Descrip here for school A.")
  schoolA.put()
  schoolB = School(key_name="Test School B", parent=dataset, name="Test School B", description="Descrip here for school B.")
  schoolB.put()
  schoolC = School(key_name="Test School C", parent=dataset, name="Test School C", description="Descrip here for school C.")
  schoolC.put()
  #A is mixed, B is girls, C is boys.
  schools     =[schoolA, schoolB, schoolC]
  schoolCounts=[10,      10,      10]
  retString= "<p>List of schoolA's students. </p>"
  currentSchoolPuts =[] #See http://googleappengine.blogspot.co.uk/2009/06/10-things-you-probably-didnt-know-about.html .
  for n in range(1, len(schools)):
    x = schoolCounts[n]
    for i in range(1, x):
      studKey = "GenStudKey-" + str(i) + "-" + str(n) 
      thisSchool = schools[n]
      thisStud = Student(parent = thisSchool, key_name=str(studKey), name = "Student " + str(i), year = random.randint(7,11), attendance=random.uniform(0.0,100.0))
      try:
        currentSchoolPuts.append(thisStud)
        #thisStud.put()
      except:
        retString+= "<p>Failed to add: (" + str(thisStud.key()) + ") " + thisStud.name + "</p>"      
    db.put(currentSchoolPuts) #Add all appended students in the current school.
  """   studB = Student(key_name="0994493", name = "Jim Jones", year = 7)
    studB.put()
    studC = Student(parent = thisSchool, key_name="099753", name = "Sally Stephenson", year = 8)
    studC.put()
  """
  
  test_query = Student.all()
  test_query.ancestor(dataset)
  
  retString+="<p>"+str(schoolA.name) +"</p>"
  for item in test_query.run(limit=50):
    retString+= "<p>(" + str(item.key()) + "). Name: " + str(item.name) + ", Attendance: " + str(item.attendance) + "</p>"
  #memcache.flush_all()
  return retString

def DALReturnAllSchools():
  test_query = School.all()
  retString = "<p>Schools (max 50):</p>"
  for item in test_query.run(limit=50):
    retString+="<p> "+str(item.name) +"</p>" 
  return retString

def DALReturnAllStudents():
  q = db.GqlQuery("SELECT * FROM Student")
  retString = "<p>Students (max 50):</p>"
  for item in q.run(limit=50):
    retString+="<p>ParentName: " + str(item.parent().name) + ", Name: " + str(item.name) + ", Attendance: " + str(item.attendance) + "</p>" 
  return retString

def datasets_plotbydate():
  q = db.GqlQuery("SELECT * FROM Dataset")
  retString = "<p>Datasets (max 50):</p>"
  retString += "  <img src=\"/img/dataset_explorer.jpg\" alt=\"alt text\" height=\"184\" width=\"326\" />"
  dataJSON = []
  bFound = False
  for item in q.run(limit=50):
    bFound = True
    retString+="<p>"+str(item.dateOfReference) +"</p>"
    dataJSON.append(item.dateOfReference)
  retString+="<div id=\"chart1\"><p id=\"chartdata\">dataJSON:"
  for row in dataJSON:
    retString+= str(row)
  retString+="</p></div>"

  if bFound: #Only lists if there are results to list.
    #Extension. List schools by dataset.
    q = db.GqlQuery("SELECT * FROM Dataset LIMIT 1")
    dataset = q.get()
    retString += "<p>" + str(dataset.key()) +"</p>" #dataset.datasetShortName != dataset.name....!
    retString+="<div id=\"schoolsindataset\"><p>Schools in dataset</p>"
    qq = db.GqlQuery("SELECT * FROM School WHERE ANCESTOR IS :1", dataset.key())
    for item in qq.run(limit=50):
      retString += "<p class=\"school\">"
      retString += str(item.name)
      retString += "</p>"
    retString+="</div>"
  else:
    retString+="<p>No results found</p>"
  return retString

def datasets_add_form():
  retString =  "<div id=\"adminformwrapper\"><h3>Create dataset:</h3>"
  retString += "<form>"
  #Initial dataset information.
  retString += " <p>Dataset Name: <input type=\"text\" name=\"datasetName\"></p>"
  retString += " <p>Dataset Description: <input type=\"text\" name=\"datasetDescription\"></p>"
  retString += "  <div id=\"dataset-parameters\">"
  
  retString += "  </div>"
  retString += "  <div id=\"dataset-datasources\">"
  retString += "  <img src=\"/img/dataset_creation.jpg\" alt=\"alt text\" height=\"184\" width=\"326\" />"
  retString += "  <h4>Data Sources</h4>"
  retString += "    <div class=\"circle-12px circle-color-empty icon-attendance\"></div><div class=\"dataset-datasource\">"
  retString += "     <p>Attendance: <span class=\"datasource-pathvalue\" id=\"datasource-pathvalue-attendance\"></span><input id=\"datasource-browsebutton-attendance\" type=\"button\" value=\"Browse\" onclick=\"formButtonClick_Browse(this.id)\"><span class=\"datasource-validationvalue\" id=\"datasource-validationvalue-attendance\"></span></p>"
  retString += "    </div>"
  retString += "    <div class=\"circle-12px circle-color-green icon-behaviour\"></div><div class=\"dataset-datasource\">"
  retString += "     <p>Behaviour: <input type=\"button\" value=\"Browse\"></p>"
  retString += "    </div>"
  retString += "    <div class=\"circle-12px circle-color-red icon-timetable\"></div><div class=\"dataset-datasource\">"
  retString += "     <p>Timetable: <input type=\"button\" value=\"Browse\"></p>"
  retString += "    </div>"
  retString += "    <div class=\"circle-12px circle-color-amber icon-timetable\"></div><div class=\"dataset-datasource\">"
  retString += "     <p>Attendance: <input type=\"button\" value=\"Browse\"></p>"
  retString += "    </div>"
  
  #See http://twitter.github.com/bootstrap/javascript.html#modals for bootstrap modal template.
  retString += "    <br/>      "
  #Button to trigger modal
  retString += "    <a href=\"#myModal\" role=\"button\" class=\"btn\" data-toggle=\"modal\">Launch demo modal</a> "
  retString += "    <br/>      "
  retString += "  <div id=\"myModal\" class=\"modal hide fade\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"myModalLabel\" aria-hidden=\"true\">     "
  retString += "   <div class=\"modal-header\">    "
  retString += "     <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>    "
  retString += "     <h3>Modal header</h3>  "
  retString += "   </div>  "
  retString += "   <div class=\"modal-body\">    "
  retString += "     <p>One fine body...</p>  "
  retString += "   </div>  "
  retString += "   <div class=\"modal-footer\">    "
  retString += "     <a href=\"#\" class=\"btn\">Close</a>    "
  retString += "     <a href=\"#\" class=\"btn btn-primary\">Save changes</a>  "
  retString += "   </div>"
  retString += "  </div>"
  retString += "    <div class=\"dataset-datasource\">"
  retString += "     <p>Modal demo above: <input type=\"button\" value=\"Browse\"></p>"
  retString += "    </div>"

  
  
  
  
  retString += "  </div>"
  retString += "</form>"
  
  retString += "</form>"
  retString += "</div>"
  return retString

def datasets_add_form_submitted():
  retString =  "<div id=\"adminformwrapper\"><p>Create dataset:</p>"
  retString += "<form>"
  retString += ""
  retString += "</form>"
  retString += "</div>"
  return retString
  
def school_addschool_temp():
  #TODO: Change name of function, incorrect!
  returnString = ""
  #thisSchool = School()
  #thisSchool.name = "GCS"
  #thisSchool.schoolDescription = 
	#	So, a school, huh?
	#
  thisSchool = GenerateRandomSchool()
  thisSchool.parent= db.GqlQuery("SELECT KEY FROM Dataset").get() #Adds to most recent dataset.
	
  returnString += "<p>" + str(thisSchool) + "</p>"    		
  logging.info("Page request: Add School:")
  School_Create(thisSchool) #Adds to datastore.
  schools = db.GqlQuery("SELECT * "
                      "FROM School")
  for school in schools:
    returnString += '<p><b>%s</b> exists: </p>' % school.name
  return returnString


  
def students_ofSchool(eSchool):
  returnString=""
  q = db.query_descendants(eSchool) 
  for s in q.run(limit=50):
    returnString+= "<p>"+str(s)+ "</p>"

def demo_DALDataStoreQuery():
  s="Query: "
  for p in DAL_DataStoreQuery_DoWrapper():
    s += str(p)
  return s
                                        


def DAL_DataStoreQuery_DoWrapper(sGQLQueryString = "SELECT * from School",
                                 thisLimit = 5):
  """
  Whole wrapper for a Datastore query.
  Assumes global db object imported from google.appengine.ext
  """
  q = db.GqlQuery(sGQLQueryString)
  return q.run(limit=thisLimit)


def DAL_FlushDataStore():
  #Hacky...this will likely fail when we reach more objects.
  models = ['Student', 'School', 'Dataset'] #Add any more items here.
  for i in range(1, len(models)):
    q = db.GqlQuery("SELECT * FROM "+ models[i])
    s="<p>Flushing...</p>"
    for item in q.run():
      sKey = str(item.key())
      try:
        item.delete()
        s+= "<p>" + models[i] + " deleted: [" + sKey + "]</p>"
      except:
        s+= "<p>" + models[i] + " delete *failed*: [" + sKey + "]</p>"
        
  s+="<p>...flushed.</p>"
  return s
 
"""   
def DAL_PutFilestream(fFile):
  class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):   
    def post(self):     
      upload_files = self.get_uploads('file')  # 'file' is file upload field in the form     
      blob_info = upload_files[0]     
      self.redirect('/serve/%s' % blob_info.key())
"""
