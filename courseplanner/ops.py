from google.appengine.ext import ndb
import json
from models import *

# This is where all for CRUD operations will live. Potential list:
#   -create_student
#   -add_course_to_student_list
#   -remove_course_from_student_list
#   -get_student_courses(student_id)

#   -add_course_to_master_list
#   -remove_course_from_master_list
#   -get_course(by substring of course_num)

#   -get_program_sheet(major_id or substring of name)
#   -set_program_sheet(student_id, major_id, track_name?)
#   -add_petition(course_id, course_req_id)

def create_student(name, student_id):
    s = Student(student_name=name, student_id = student_id)
    s.put()

# Add course to candidate list for given student, course, grade, units, and req
# Return true if course fulfills the req, false otherwise. Assumes course_req_id
# is valid and for correct major
def add_course(student_id, course_num, course_req_id, grade, units):
    # fetch single result and extract from array
    student = Student.query(Student.student_id == student_id).fetch(1)[0]
    course = Course.query(Course.course_num == course_num).fetch(1)[0]
    req_course = Req_Course.query(Req_Course.course_req_id == course_req_id).fetch(1)[0]

    candidate_course = Candidate_Course(course=course.key, req_course=req_course.key,
                                        grade=grade, units=units, student=student.key)
    candidate_course.put()

    # Validate course, req_course pairing
    if course.key in req_course.allowed_courses:
        return True
    else:
        return False

# Return dict of course information by course_num
def get_course_dict(course_num):
    # upper case
    course_num = course_num.upper()
    course = Course.query(Course.course_num == course_num).fetch(1)[0]
    return course.to_dict()

# Return json dump of course information by course_num
def get_course_json(course_num):
    course_dict = get_course_dict(course_num)
    if course_dict is not None:
        return json.dumps(course_dict)
    return None
