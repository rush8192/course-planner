from google.appengine.ext import ndb
import json
import re
from models import *

# This is where all for CRUD operations will live. Potential list:
#   -create_student
#   -add_candidate_course
#   -remove_candidate_course
#   -get_candidate_courses(student_id)

#   -add_course_listing
#   -remove_course_listing
#   -get_master_course_list
#   -get_course(by substring of course_num)

#   -get_program_sheet(major_id, ps_name)

# Helper to print error messages in consistent json format
def error(message):
    return json.dumps({"errorMessage": message})
 
# Helper to cleanup course number    
def fix_course_num(course_num):
    course_num = course_num.upper()
    n_split = re.split('(\d+)', course_num, 1)
    if len(n_split) < 2:
        return error('Course number must include digits')
    ret = n_split[0].replace(" ", "") + ' '
    for s in n_split[1:]:
        ret += s
    return ret    
    
def create_student(student_id, student_name):
    s = Student(student_id = student_id, student_name = student_name)
    # TODO: Add empty course plan (Rush)
    s.put()
    return json.dumps(s.to_dict())

def get_student(student_id, student_name):
    if student_id is not None:
        student = Student.query(Student.student_id == student_id).fetch(1)
        if len(student) > 0: 
            return json.dumps(student[0].to_dict())
        else:
            return error('Student with id ' + str(student_id) + ' not found')
    else:
        student = Student.query(Student.student_name == student_name).fetch()
        if len(student) > 0: 
            return json.dumps([s.to_dict() for s in student])
        else:
            return error('Student with name ' + str(student_name) + ' not found')
    
# Add course to candidate list for given student, course, grade, units, and req
# Return true if course fulfills the req, false otherwise. Assumes course_req_id
# is valid and for correct major
#
# Parameters:
#    req_course (optional): key for Req_Course the course fulfills. Can have candidate
#       courses without req_course (e.g. taken for interest, or major undecided) 
#    force - flag to override errors validating the course.
def add_candidate_course(student_id, course_num, req_course, grade, units, force=False):
    if student_id is None or student_id == '':
        return error('Must provide student_id')
    else:
        student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return error('Student with id ' + str(student_id) + ' not found')
    course = Course.query(Course.course_num == course_num).fetch(1)
    if len(course) > 0:
        course = course[0]
    else: 
        return error ('Course number ' + str(course_num) + ' not found')
    if units == '':
        units = None
    if req_course:
        candidate_course = Candidate_Course(course=course.key, req_course=req_course,
                                        grade=grade, units=units, student=student.key)
    else:
        candidate_course = Candidate_Course(course=course.key,
                                        grade=grade, units=units, student=student.key)  
    # Validate course, req_course pairing
    # TODO: merge with Rush's course validation(?)
    if force or not req_course or course.key in req_course.allowed_courses:
        candidate_course.put()
        #return json.dumps(candidate_course.to_dict(excludes=[course, student]))
    else:
        return error("Course does not fulfill given requirement.")
 
# Removes course from student's program sheet (in all places that it occurs). Optional
# parameter ps specifies Student_Program_Sheet by key. If not given, course taken off all
# sheets found
def remove_candidate_course(student_id, course_num, ps):
    student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return error('Student with id ' + student_id + ' not found')
    course = Course.query(Course.course_num == course_num).fetch(1)
    if len(course) > 0: course = course[0]
    else:
        return error ('Course number ' + course_num + ' not found')
    if ps: 
        candidate_courses = Candidate_Course.query(Candidate_Course.student == student.key, 
                                                   Candidate_Course.course == course.key,
                                                   Candidate_Course.student_program_sheet 
                                                    == ps).fetch()
    else:
        candidate_courses = Candidate_Course.query(Candidate_Course.student == student.key,
                                                   Candidate_Course.course == course.key
                                                   ).fetch()
    for course in candidate_courses:
        course.key.delete()          

# Return all candidate courses associated with student: for now, this is just a set
# of unique course_nums. (Reqs information will be obtained separately when fetching
# student's program sheet).
def get_candidate_courses(student_id):
    student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return error('Student with id ' + student_id + ' not found')
    courses = Candidate_Course.query(student == student.key).fetch()
    course_dict = dict()
    for course in courses:
        course_dict[course.course_num] = 1
    return json.dumps(course_dict.keys())

# Add course listing: only course_num required
def add_course_listing(course_num, course_desc, course_title):
    course_num = fix_course_num(course_num)
    existing = Course.query(Course.course_num == course_num).fetch()
    if len(existing) > 0:
        return error('Course with course number = ' + course_num + ' already exists!')
    course = Course(course_num=course_num, course_desc=course_desc, 
                    course_title=course_title)
    course.put()
    return json.dumps(course)
    
# Edit course listing: can change description or title. If either is None, left unaffected    
# TODO: more advanced editing e.g. Offerings
def edit_course_listing(course_num, course_desc, course_title):
    course_num = fix_course_num(course_num)
    courses = Course.query(Course.course_num == course_num).fetch(1)
    if len(courses) > 0:
        course = courses[0]
        if course_desc:
            course.course_desc = course_desc
        if course_title:
            course.course_title = course_title
        course.put()
        #return json.dumps(course.to_dict())
        return True
    else:
        return error('Course_num ' + course_num + ' not found.')           
 
def remove_course_listing(course_num):
    course_num = fix_course_num(course_num)
    courses = Course.query(Course.course_num == course_num).fetch(1)
    if len(courses) > 0:
        course = courses[0]
        course.key.delete()
    else:
        return error('Course_num ' + course_num + ' not found.')

# Return json dump of course information by course_num
def get_course_listing(course_num):
    course_num = fix_course_num(course_num)
    courses = Course.query(Course.course_num == course_num).fetch(1)
    if len(courses) > 0:
        return json.dumps(courses[0].to_dict())
    else:
        return error('Course ' + course_num + ' not found.')
    
# Return list of all course_nums in datastore
def get_master_course_list():
    courses = Course.query().fetch(projection=[Course.course_num])
    course_dict = dict()
    for course in courses:
        course_dict[course.course_num] = 1
    return json.dumps(course_dict.keys())  
    
        
# Get program sheet by either major_id or ps_name. For now, only exact matches
def get_program_sheet(major_id, ps_name):
    if major_id is not None:
        sheets = Program_Sheet.query(Program_Sheet.major_id == major_id).fetch(1)
        message = error('Major_id' + str(major_id) + 'not found.')
    else:
        sheets = Program_Sheet.query(Program_Sheet.ps_name == ps_name).fetch(1)
        message = error('Program sheet named ' + str(ps_name) + ' not found.')
    if len(sheets) == 0:
        return message
    else:
        return json.dumps(sheets[0])   
