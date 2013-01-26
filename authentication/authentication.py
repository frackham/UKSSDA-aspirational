
from google.appengine.api import users

def prepareNavigation(nav):
  nav["admin"] = ""
  nav["school"] = ""
  nav["student"] = ""
  nav["attendance"] = ""
  nav["behaviour"] = ""
  nav["assessment"] = ""
  nav["curriculum"] = ""
  nav["developer"] = ""
  nav["extension"] = ""
  nav["fragmentsinprogress"] = ""
  nav["documents"] = ""

def buildNavigation(nav):
  user = users.get_current_user()
  nav["admin"] = nav_admin() # if matches!      
  nav["school"] = nav_school()           
  nav["student"] =  nav_student()     
  nav["attendance"] =  nav_attendance()          
  nav["behaviour"] =  nav_behaviour()          
  nav["assessment"] =  nav_assessment()            
  nav["curriculum"] =  nav_curriculum()         
  nav["developer"] =  nav_developer()         
  nav["extension"] =  nav_extension()  
  nav["fragmentsinprogress"] = nav_fragmentsinprogress()  
  nav["documents"] = nav_documents()  
  
  
def nav_admin():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large\"></i>Admin</a>
          	<ul>
          		<li class=\"primarynav\" id=\"admin-schooldetails\">    <a href=\"#\">School Details</a></li>
          		<li class=\"primarynav\" id=\"admin-datasetexplorer\">  <a href=\"#\">Dataset Explorer</a></li> <!-- #TODO: [e] Visual view of datasets. Add datasets from here (including descriptive only datasets). Consider using http://timeline.verite.co/  -->
          		<li class=\"primarynav\" id=\"admin-datasetvalidation\"><a href=\"#\">Dataset Validation(?)</a></li>
          		<li class=\"primarynav\" id=\"admin-adddataset\">       <a href=\"#\">Create New Dataset</a></li>
          		<li class=\"primarynav\" id=\"admin-usersetup\">        <a href=\"#\">User Setup</a></li>
          		<li class=\"primarynav\" id=\"admin-flushdatastore\">   <a href=\"#\">Flush Data Store</a></li>
          	</ul>	
          </li>"""     
          
          
          
          
def nav_school():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-home icon-large strategic\"></i>School</a>
        	<ul>
        		<li class=\"primarynav\" id=\"school-context\"><a href=\"#\">School Context</a></li>
        		<li class=\"primarynav\" id=\"school-temp\">   <a href=\"#\">Other Analyses</a></li>
        	</ul>	
        </li>"""
        
def nav_student():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-group icon-large operational\"></i>Students</a>
        	<ul>
        		<li class=\"primarynav\" id=\"students-summary\"><a href=\"#\">Students Summary</a></li>
        		<li class=\"primarynav\" id=\"students-temp\">   <a href=\"#\">Other Analyses</a></li>
        	</ul>	
        </li>"""
        
def nav_attendance():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-check icon-large tactical\"></i>Attendance</a>
        	<ul>
        		<li class=\"primarynav\" id=\"attendance-summary\">             <a href=\"#\">Attendance Summary</a></li>
        		<li class=\"primarynav\" id=\"attendance-groups\">              <a href=\"#\">Attendance within Groups</a></li>
        		<li class=\"primarynav\" id=\"attendance-attainmentthresholds\"><a href=\"#\">Attendance against Thresholds</a></li>
        		<li class=\"primarynav\" id=\"attendance-temp\">                <a href=\"#\">Other Analyses</a></li>
        	</ul>	
        </li>"""

def nav_behaviour():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-fire icon-large tactical\"></i>Behaviour</a>
        	<ul>
        		<li class=\"primarynav\" id=\"behaviour-summary\"><a href=\"#\">Behaviour Summary</a></li>
        		<li class=\"primarynav\" id=\"behaviour-temp\">   <a href=\"#\">Other Behaviour Analyses</a></li>
        	</ul>	
        </li>"""
        
def nav_assessment():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large tactical\"></i>Assessment</a>
        	<ul>
        		<li class=\"primarynav\" id=\"assessment-summary\"><a href=\"#\">Assessment Summary</a></li>
        		<li class=\"primarynav\" id=\"assessment-temp\">   <a href=\"#\">Other Assessment Analyses</a></li>
        	</ul>	
        </li>"""
        
def nav_curriculum():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large tactical\"></i>Curriculum</a>
        	<ul>
        		<li class=\"primarynav\" id=\"curriculum-summary\"><a href=\"#\">Curriculum Summary</a></li>
        		<li class=\"primarynav\" id=\"curriculum-temp\">   <a href=\"#\">Other Curriculum Analyses</a></li>
        	</ul>	
        </li>"""
        
def nav_developer():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large\"></i>Developer</a>
        	<ul>
          	<li class=\"primarynav\" id=\"dev-listschools\">            <a href=\"#\">School List</a></li>
            <li id=\"dev-scheduledtasks\">   <a href=\"/_ah/admin/cron\">Scheduled Tasks</a></li>
          	<li class=\"primarynav\" id=\"dev-ajaxtemp\">               <a href=\"#\">Ajaxtest</a></li>
          	<li class=\"primarynav\" id=\"dev-loadtempstrut\">          <a href=\"#\">Load test strut</a></li>
          	<li class=\"primarynav\" id=\"dev-qanparse\">               <a href=\"#\">QAN parse</a></li>
          	<li class=\"primarynav\" id=\"dev-edubasescrape\">          <a href=\"#\">Edubase scrape</a></li>
          	<li class=\"primarynav\" id=\"dev-addschool\">              <a href=\"#\">Add School</a></li>
          	<li class=\"primarynav\" id=\"dev-addstudenttoschool\">     <a href=\"#\">Add Student to (Fixed) School</a></li>
          	<li class=\"primarynav\" id=\"dev-listallstudents\">        <a href=\"#\">Show Students of Schools</a></li>
          	<li class=\"primarynav\" id=\"dev-analysisloaderdemo\">     <a href=\"#\">Analysis Loader Demo</a></li>
          	<li class=\"primarynav objectReturn\" id=\"dev-pdftemp\">   <a href=\"#\">Render PDF Demo</a></li>
          	<li class=\"primarynav\" id=\"dev-unittestoutcomes\">       <a href=\"#\">Unit Test Results</a></li>
          	<li class=\"primarynav\" id=\"dev-fonttestpage\">           <a href=\"#\">Font Test Page</a></li>
          	<li class=\"primarynav\" id=\"dev-fileuploaddownload\">     <a href=\"#\">File upload and download</a></li>
        	</ul>	
        </li>"""
        
def nav_extension():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large\"></i>Extension Demos</a>
        	<ul>
          	<li class=\"primarynav\" id=\"extension-location\"><a href=\"#\">Location</a></li>
          	<li class=\"primarynav\" id=\"extension-news\">    <a href=\"#\">News</a></li>
          	<li class=\"primarynav\" id=\"extension-ofsted\">  <a href=\"#\">OFSTED</a></li>
          	<li class=\"primarynav\" id=\"extension-edubase\">  <a href=\"#\">Edubase</a></li>
        	</ul>	
        </li>"""
        
def nav_fragmentsinprogress():
  return """<li><a href=\"#\"><i class=\"primarynavicon icon-cogs icon-large\"></i>Fragments in Progress</a>
        	<ul>
          	<li class=\"primarynav\" id=\"fragment-studentcount\"><a href=\"#\">Count(Students)</a></li>
          	<li class=\"primarynav\" id=\"fragment-schoolcount\"><a href=\"#\">Count(School)</a></li>
          	<li class=\"primarynav\" id=\"fragment-schoollist\"><a href=\"#\">List(School)</a></li>
        	</ul>	
        </li>""" 
        
def nav_documents():
  return """<li id=\"documents\"><a href=\"#\"><i class=\"primarynavicon icon-inbox icon-large strategic\"></i>Documents</a></li>"""