from google.appengine.ext import db
import json
from models import *

# This is where all for CRUD operations will live. Potential list: 
#   -create_student
#   -add_course
#   -remove_course
#   -get_course(by substring of course_num)
#   -get_student_courses(student_id)
#   -get_major(major_id or substring of name)
#   -set_major(student_id, major_id, track_name?)
#   -set_track(student_id, major_id, track_name)
#   -add_petition(course_id, course_req_id)
 

def create_student(name, student_id, major_id):
    q = db.GqlQuery("SELECT * FROM Major WHERE major_id = :1", major_id)
    for m in q.run(limit=1):
        major = m
    s = Student(name=name, student_id = student_id, major=major)
    s.put()
    
# Add course to candidate list for given student, course, grade, units, and req
# Return true if course fulfills the req, false otherwise. Assumes course_req_id
# is valid and for correct major
def add_course(student_id, course_num, course_req_id, grade, units):
    q = db.GqlQuery("SELECT * FROM Student WHERE student_id = :1", student_id)
    # get first (should be only) result: does it have to be this ugly?
    student = [s for s in q.run()][0]
    
    q = db.GqlQuery("SELECT * FROM Course WHERE course_num = :1", course_num)
    course = [c for c in q.run()][0]
    
    q = db.GqlQuery("SELECT * FROM Req_Course WHERE course_req_id = :1",
                    course_req_id)
    req_course = [c for c in q.run()][0]
    
    candidate_course = Candidate_Course(course=course, req_course=req_course, grade=grade,
                                         units=units, student=student)
    candidate_course.put()
    
    # Validate course, req_course pairing
    if course.key() in req_course.allowed_courses:
        return True
    else:
        return False                                

# return JSON dump of course by course_num        
def get_course(course_num):
    # upper case
    course_num = course_num.upper()
    q = db.GqlQuery("SELECT * FROM Course WHERE course_num = :1", course_num)          
    course = [c for c in q.run()][0]
    return json.dumps(course.to_dict())
