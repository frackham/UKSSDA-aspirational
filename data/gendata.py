from edu_objects import *
import random

#TODO: [e]Replace these strings with values loaded from textfiles on module start (system object? onload of admin console, load these to system.object).

  
def ReturnRandomSchool():  
  #Not really random, just a way of getting a school.
  #TODO: [e] Currently returns first item.
  test_query = School.all()
  for item in test_query.run(limit=1):
    return item

def GenerateRandomStudent():
  """Returns a 'randomly' generated Student object.
  Note that this does not load the object into the datastore"""
  stud = Student()
  stud.name = "Random Student"
  stud.year = 7
  stud.attendance= 100
  return stud
  
def GenerateRandomSchool():
  """Returns a 'randomly' generated School object.
  Note that this does not load the object into the datastore"""
  
  schoolNames = ['A Primary', 'B Primary', 'C Primary', 'D Primary', 'E Primary', 'F Primary', 'G Primary', 'H Primary',
  'A Secondary', 'B Secondary', 'C Secondary', 'D Secondary', 'E Secondary', 'F Secondary', 'G Secondary', 'H Secondary',
  'A Comprehensive', 'B Comprehensive', 'C Comprehensive', 'D Comprehensive', 'E Comprehensive', 'F Comprehensive', 'G Comprehensive', 'H Comprehensive',
  'A School', 'B School', 'C School', 'D School', 'E School', 'F School', 'G School', 'H School',
  'A Academy', 'B Academy', 'C Academy', 'D Academy', 'E Academy', 'F Academy', 'G Academy', 'H Academy',
  ]
  
  
  rSchool = School()
  rSchool.name = random.choice(schoolNames)
  rSchool.description = rSchool.name + " is a " + rSchool.name.split(" ")[1] + " founded in " + str(random.randrange(1700, 2010)) + "."
  return rSchool
  
