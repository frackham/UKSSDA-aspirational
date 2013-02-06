import logging
import random
from datetime import datetime
from google.appengine.ext import db
from edu_objects import *
from data.dal import *
from data.gendata import *
from string import Template
from registry import System
from reporting.communications import *

#For file upload.
from google.appengine.ext import blobstore 
from google.appengine.ext.webapp import blobstore_handlers 

def getCurrentDataset():
  #dal_temp returns a default dataset. In actual DAL, this should return the current dataset in use.
  dataset =  Dataset(key_name="Demonstration Dataset")
  return dataset 

def AnalysisPlaceholder(model, renderType = 'HTML'):
  """Given a model, returns a rendering"""
  dbg = System().debugMode
  retString = "<h3>Attendance Overview</h3>"
  #logging.info(str(model))
  returns = model[1] #Dictionary, retrieve returns by name.
  students = model[0]
  
  if returns['average attendance'] < 85:
    retString += alertMessageHTML("Average attendance is below 85%", "Warning")
  if returns['persistent absentee percentage'] > 30:
    retString += alertMessageHTML("Proportion of persistent absentees is above 30%", "Error")
  elif returns['persistent absentee percentage'] > 20:
    retString += alertMessageHTML("Proportion of persistent absentees is above 20%", "Warning")

  for item in students:
    if dbg:
      retString+="<p>Att: "+str(item.attendance) +", from school " +str(item.currentSchool)+ "</p>" 
    pass
  retString+="<p>Att average: " + str(returns['average attendance']) +"</p>"   
  retString+="<p>Number of persistent absentees: " + str(returns['persistent absentee count']) +"</p>"   
  retString+="<p>Percentage of persistent absentees: " + str(returns['persistent absentee percentage']) +"</p>"   
 
  return retString
  
def modelFromQuery(query):
  totAtt = 0
  students = 0
  persAbs = 0
  persAtt=0
  persAbsPct=0
  model = []
  modelobjects = []
  returns = {} #Dictionary, retrieve returns by name.
  
  for item in query.run():
    students += 1
    attendance = item.attendance  #Retrieve once from dataset object.
    
    #Store objects #TODO: [e] Should be storing business object from BAL.
    modelobjects.append(item) 
    
    #Process data.
    totAtt+=attendance
    
    if attendance < 85:
      persAbs += 1
      persAtt += attendance  
    
  #Summative data processing.  
  avAtt = totAtt/students
  if persAbs> 0: 
    persAbsPct = (persAtt/persAbs)
  
  #Store data returns in model.
  returns['student count'] = students
  returns['total attendance'] = totAtt 
  returns['average attendance'] = avAtt  
  returns['persistent absentee count'] = persAbs
  returns['persistent absentee percentage'] = persAbsPct
  
  model = [modelobjects, returns] #first item of model is list of objects, after that is returns dictionary.
  return model
  
def CurrentDatasetAttendanceOverview():
  #(0) With current analysis object.
  #(1) Get dataset.
  dataset = getCurrentDataset()
  #(2) Query.
  query = Student.all() #TODO:[e] Review. Not optimal. Have each analysis define a query.
  query.ancestor(dataset)  
    
  #(3) Create model.
  model = modelFromQuery(query)
  
  #(4) Pass model to analysis, and retrieve return.
  retString = AnalysisPlaceholder(model)#System.Analysis['Attendance']
  return retString
  
def CurrentDatasetAttendanceOverview_FromAnalysisObject(analysisObjectName):
  #(0) With current analysis object.
  analysisObject = System().Analysis(analysisObjectName)
  #(1) Get dataset.
  dataset = getCurrentDataset()
  #(2) Query.
  queryString = analysisObject.query 
  q = db.GqlQuery(queryString)

  #(3) Create model.
  model = modelFromQuery(q) #HACK: [c] CURRENTLY NOT coming from analysis object.
  
  #(4) Pass model to analysis, and retrieve return.
  retString = AnalysisPlaceholder(model)#System.Analysis['Attendance']
  #logging.info(analysisObjectName)
  #logging.info(queryString)
  #logging.info(str(model))
  return retString

    

@db.transactional
def tempSchoolSetup():
  retString = ""
  
  datasetRefDate = (datetime(2013,1,1))
  dataset =  Dataset(key_name="Demonstration Dataset", dateOfReference=datasetRefDate) #datasetShortName, datasetDescription.
  dataset.put()

  schoolA = School(key_name="YellowTreeDrive", 
                   parent=dataset, 
                   name="Yellow Tree Drive", 
                   description="Secondary school generated based on average profile of school in RAISEonline unvalidated 2012.", 
                   ageRange="11-16",
                   urn=306455, 
                   dateOpened= datetime(2011,9,1),
                   localAuthorityName = 'Richmond Upon Thames',
                   localAuthorityNumber = 316,
                   schoolCapacity=1200)
                   
  schoolA.put() #Adds the school

  schools     =[schoolA]
  schoolCounts=[1000]
  retString= "<p>List of YTD's students. </p>"
  currentSchoolPuts =[] #See http://googleappengine.blogspot.co.uk/2009/06/10-things-you-probably-didnt-know-about.html .
  logging.info(str(len(schools)) + " + length of schools")
  for n in range(0, len(schools)):
    x = schoolCounts[n-1]
    thisSchool = schools[n-1]
    thisSchoolName = thisSchool.name
    logging.info("school no: " + str(n))
    logging.info(str(thisSchool))
    for i in range(1, x):
      studKey = "GenStudKey-" + str(i) + "-" + str(n) 
      thisStud = Student(parent = thisSchool, 
                         currentSchool = thisSchoolName,
                         key_name=str(studKey), 
                         name = "Student " + str(i), 
                         year = random.randint(7,11))
      if random.randint(0,100) < 25: 
        thisStud.group_isFSM = True
      if random.randint(0, 100)<15:
        thisStud.attendance=random.uniform(0.0,100.0)
      else:
        thisStud.attendance=random.uniform(80.0,100.0)
        
      if random.randint(0,100) < 20: 
        thisStud.group_isEAL = True
        
      SENInt = random.randint(0,100)
      if SENInt  < 5: 
        thisStud.group_SEN = "S"                            
      elif SENInt  < 12: 
        thisStud.group_SEN = "P"                            
      elif SENInt  < 25: 
        thisStud.group_SEN = "A"                            
      else:
        thisStud.group_SEN = "N" 
        
      AssessInt = random.randint(0,100)  
      #logging.info("AssessInt: " + str(AssessInt))
      if AssessInt < 25: 
        thisStud.assessment_has5AA = True
        thisStud.assessment_has5AC = True
        thisStud.assessment_has5AG = True
      elif AssessInt < 60: 
        thisStud.assessment_has5AC = True
        thisStud.assessment_has5AG = True 
      elif AssessInt < 95: 
        thisStud.assessment_has5AG = True 
      else: 
        pass #Not 5AG.
                                       
      try:
        currentSchoolPuts.append(thisStud)
        #thisStud.put()
      except:
        retString+= "<p>Failed to add: (" + str(thisStud.key()) + ") " + thisStud.name + "</p>"      
    db.put(currentSchoolPuts) #Add all appended students in the current school.

  
  test_query = Student.all()
  test_query.ancestor(dataset)
  
  retString+="<p>"+str(schoolA.name) +"</p>"
  for item in test_query.run(limit=1000):
    retString+= "<p>(" + str(item.key()) + "). Name: " + str(item.name) + ", Year Group: " + str(item.year) +", Attendance: " + str(item.attendance) + ", Groups: FSM=" + str(item.group_isFSM) + ", SEN=" + str(item.group_SEN) + ", EAL=" + str(item.group_isEAL) + ", 5AA=" + str(item.assessment_has5AA) +  "</p>"
  #memcache.flush_all()
  return retString

@db.transactional
def tempDatasetFromFiles():
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
  retString += "     <p>Modal body...</p>  "
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

 
def SchoolContextDashboard():
  #(0) With current analysis object.
  #analysisObject = System().Analysis(analysisObjectName)
  #(1) Get dataset.
  dataset = getCurrentDataset()
  logging.info("school context")
  #(2) Query.
  queryString = "SELECT * FROM School" 
  q = db.GqlQuery(queryString)

  #(3) Create model.
  #model = modelFromQuery(q) #HACK: [c] CURRENTLY NOT coming from analysis object.
  totAtt = 0
  students = 0
  persAbs = 0
  persAtt=0
  
  for school in q.run():
    q2 = db.GqlQuery("SELECT * FROM Student WHERE ANCESTOR IS :1", school.key())
    for student in q2.run():
      
      students +=1
      attendance = student.attendance  #Retrieve once from dataset object.
      
      #Store objects #TODO: [e] Should be storing business object from BAL.
      #modelobjects.append(item) 
    
      #Process data.
      totAtt+=attendance
    
      if attendance < 85:
        persAbs += 1
        persAtt += attendance  
    
  #Summative data processing.  
  avAtt = totAtt/students
  if persAbs == 0:
    persAbsPct = 0
  else:
    persAbsPct = (persAtt/persAbs)*100
  
  #(4) Pass model to analysis, and retrieve return.
  retString = "<h3>" + school.name + ": Context</h3>"
  retString+= "<div id=\"dashboardchart\">"  "</div>"
  retString+= "<script type=\"text/javascript\">"
  retString+= "var r = Raphael(document.getElementById('dashboardchart'), 640, 480);"
  #// Creates a single series barchart at 10, 10
  #// width 300, height 220, data: [10,20,30,40]
  retString+= "var max_val = 50;"
  thisList = [[persAtt, avAtt]]
  retString+= "r.barchart(80, 200, 420, 320, " +str(thisList)+");"
  retString+= "axis = r.axis(85,230,310,null,null,4,2,['% PA', '% Attendance'], '|', 0);"
  retString+= "axis.label(['% PA', '% Attendance']);"
  retString+= "axis.text.attr({font:\"12px Arial\", \"font-weight\": \"regular\", \"fill\": \"#000000\"});"
  #retString+= " // show y-axis by setting orientation to 1"
  retString+= "axis2 = r.axis(40,230,300,0,400,10,1);"
  retString+= "</script>" 
  
  
  #logging.info(analysisObjectName)
  logging.info(retString)
  return retString

    
  
def CurrentAssessmentOverview():
  #(0) With current analysis object.
  #(1) Get dataset.
  students = 0
  FiveAA = 0
  FiveAC = 0
  FiveAG = 0
  dataset = getCurrentDataset()
  #(2) Query.
  queryString = "SELECT * FROM School" 
  q = db.GqlQuery(queryString)

  for school in q.run():
    q2 = db.GqlQuery("SELECT * FROM Student WHERE ANCESTOR IS :1", school.key())

    
    #(3) Create model.
    for item in q2.run():
      students += 1
      logging.info(str(item.assessment_has5AA))
      #attendance = item.attendance  #Retrieve once from dataset object.  
      
      #Process data.
      if item.assessment_has5AA:
        FiveAA+= 1  
      if item.assessment_has5AC:
        FiveAC+= 1  
      if item.assessment_has5AG:
        FiveAG+= 1  

    
     
  
  #(4) Pass model to analysis, and retrieve return.

  retString = "<h3>" + school.name + ": Assessment Overview</h3>"
  retString+= "<div id=\"dashboardchart\">"  "</div>"
  retString+= "<script type=\"text/javascript\">"
  retString+= "var r = Raphael(document.getElementById('dashboardchart'), 640, 480);"
  #// Creates a single series barchart at 10, 10
  #// width 300, height 220, data: [10,20,30,40]
  retString+= "var max_val = 50;"
  logging.info(str(students) + ", " + str(FiveAA) + ", "+str(FiveAC) + ", "+str(FiveAG) + ".")
  retString+= "r.barchart(40, 10, 320, 220, [["+str(FiveAA)+","+str(FiveAC)+","+str(FiveAG)  +"]]);"
  retString+= "axis = r.axis(85,230,310,null,null,4,2,['5AA', '5AC', '5AG'], '|', 0);"
  retString+= "axis.text.attr({font:\"12px Arial\", \"font-weight\": \"regular\", \"fill\": \"#333333\"});"
  #retString+= " // show y-axis by setting orientation to 1"
  retString+= "axis2 = r.axis(40,230,300,0,400,10,1);"
  retString+= "</script>" 
  return retString  
  
def GroupQuery(groupType, sCriteria, sValue):
  #http://jsfiddle.net/arosen/uz2Bw/
  return  "SELECT * FROM Student WHERE " + sCriteria + "=" + sValue