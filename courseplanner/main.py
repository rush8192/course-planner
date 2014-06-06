#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
import add_courses, add_majors, ops
from models import Student, Program_Sheet
from webapp2 import uri_for
from ops import *
from PSHandlers import *
from decorators import *
import cStringIO

def outputMessage(self, result, send_data_back=True):
    if send_data_back:
        if 'errorMessage' not in json.loads(result):
            self.response.write(result)
        else:
            self.response.write('404 Error: ' + json.loads(result)['errorMessage'])
            self.response.set_status(404)
    else:
        if type(result) is str and 'errorMessage' in json.loads(result):
            self.response.write('404 Error: ' + json.loads(result)['errorMessage'])
            self.response.set_status(404)

class MainHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        #add_courses.main()
        add_majors.main()

class TranscriptHandler(webapp2.RequestHandler):
    @createStudent
    def post(self):
        import parser
        print "calling parser..."
        courseFp = cStringIO.StringIO()
        parser.getTransContent(self.request.body_file.file, courseFp)
        print courseFp.getvalue()
        
        user = users.get_current_user();
        uid = "rush8192"
        #uid = user.nickname()
        
        matchingStudent = Student.query(Student.student_id == uid).get()
        print matchingStudent
        for course in courseFp.getvalue().split("\n"):
            if course == "":
                continue
            splitCourse = course.split("||")
            courseId = splitCourse[0]
            # second term is course title; we should be able to pull from DB
            year = splitCourse[2]
            term = splitCourse[3]
            # fourth term is units attempted; fifth is units earned
            units = splitCourse[5]
            grade = splitCourse[6]
            matchingCourse = Course.query(Course.course_num == courseId).get()
            if matchingCourse == None:
                print "possible error: no matching class: " + courseId
                continue
                for academicPlan in matchingStudent.academic_plans:
                    plan = academicPlan.get()
                    candCourse = Candidate_Course(course=matchingCourse.key, student=matchingStudent.key,
                                    term=term, year=year, grade=grade, units=units)
                    candCourse.put()
                    plan.append(candCourse.key)
                    plan.put()
                    print "added course : " + courseId + " for student plan " + plan.student_plan_name
            

    @createStudent
    def get(self):
        self.response.write('only accepts POST requests')

#---------------Student/Course CRUD Handlers-------------------#
class StudentHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        self.response.write(get_student())

class CandidateCourseHandler(webapp2.RequestHandler):
    @createStudent
    def post(self, course_key):
        student_id = users.get_current_user().user_id()
        units = self.request.get('units')
        if units != '':
            units = int(units)
        else: units = None
        grade = self.request.get('grade')
        if grade != '':
            grade = float(grade)
        else: grade = None
        student_plan = self.request.get('student_plan')
        if student_plan == '': student_plan = None
        self.response.write(add_candidate_course(student_id=student_id,
                                                 course_key=course_key,
                                                 grade=grade,
                                                 units=units,
                                                 student_plan=student_plan))
    @createStudent
    def get(self):
        student_id = users.get_current_user().user_id()
        self.response.write(get_candidate_courses(student_id=student_id))

    @createStudent
    def delete(self, course_key):
        student_id = users.get_current_user().user_id()
        if student_id == '':
            student_id = None
        course_num = self.request.get('course_num')
        student_plan = self.request.get('student_plan')
        if student_plan == '': student_plan = None
        self.response.write(remove_candidate_course(student_id=student_id,
                                                    course_key=course_key,
                                                    student_plan=student_plan))

class CourseHandler(webapp2.RequestHandler):
    @createStudent
    def get(self, course_key):
        result = get_course_listing(course_key=course_key)
        outputMessage(self, result)

    @createStudent
    def post(self, course_num):
        course_json = self.request.get('course_json')
        course_dict = json.loads(course_json)
        course_desc = course_dict['course_desc']
        course_title = course_dict['course_title']
        outputMessage(self, add_course_listing(course_num=course_num,
                                         course_desc=course_desc,
                                         course_title=course_title), False)
    @createStudent
    #TODO: make webapp2 support patch. But we're probably never using this
    def patch(self, course_key):
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(edit_course_listing(course_key=course_key,
                                                course_desc=course_desc,
                                                course_title=course_title))
    @createStudent
    def delete(self, course_key):
        self.response.write(remove_course_listing(course_key=course_key))

class CourseSearchHandler(webapp2.RequestHandler):
    @createStudent
    def get(self, prefix):
        if len(prefix) > 0:
            self.response.write(get_course_listing_by_prefix(prefix))

#----------------End Student/Course Handlers-----------------#


# Class that handles creating and returning student's plans
class PlanHandler(webapp2.RequestHandler):

    # GET: fetch a student's plan for a given major/minor (could this match multiple entries?)
    # planid contains the string that comes after "/plan" in the url
    @createStudent
    def get(self, planid):
        user = users.get_current_user();
        uid = ""
        if (user == None):
            uid = self.request.get('uid')
        else:
            uid = user.nickname()
        student = Student.query(Student.student_id == uid).get()
        if student == None:
            self.response.write('Error: no matching student record for student: ' + uid)
            return
        else:
            if planid == None or planid == "/": #no argument; just return all plans for student
                # not sure how to return a repeated ndb entity
                #
                print "Listing all plans for " + uid
                self.response.write( student.academic_plans )
                pass
            else:
                # remove the "/" from planid
                planid = planid[1:]
                print planid

                # not sure if this is correct syntax for iterating through ndb
                # repeated property; documentation is somewhat suspect online
                for planKey in student.academic_plans:
                    # compare planKey to the planId passed in; not sure
                    # if this is correct way to compare the key values
                    print "looking at key: " + str(planKey.get().key.urlsafe())
                    print "plan id: " + str(planid)
                    if str(planKey.get().key.urlsafe()) == str(planid):
                        # method should return the matching student plan
                        print "Found matching plan : " + planid + " for " + uid
                        self.response.write(planKey.get().to_dict())
                        return 
                self.response.write('Error: no matching program sheet found with id: ' + planid + ' for student: ' + uid)

    # POST: allows the user to create a new plan for the given major/minor ID field
    @createStudent
    def post(self, pathname):
        user = users.get_current_user();
        uid = ""
        if (user == None):
            uid = self.request.get('uid')
        else:
            uid = user.nickname()
        title = self.request.get('title')
        print "creating new plan for: " + uid + " with title: " + title

        # first we load the GER program sheet, and add it to a new plan

        GER_SHEET_NAME = "GER-PRE-2015" #TODO: this needs to be changed to the correct value
        
        matchingStudent = Student.query(Student.student_id == uid).get()
        if matchingStudent == None:
            self.response.write('Error: no matching student record for: ' + uid)
            return

        gerSheet = Program_Sheet.query(Program_Sheet.ps_name == GER_SHEET_NAME).get()
        studentGerSheet = Student_Program_Sheet(program_sheet=[gerSheet.key],
                        cand_courses=[], allow_double_count=True)
        studentGerSheet.put()
        studentPlan = Student_Plan(student_plan_name=title, student_course_list=[], program_sheets=[ studentGerSheet.key ])
        studentPlan.put()
        matchingStudent.academic_plans.append(studentPlan.key)
        matchingStudent.put()
        print "created new plan for student: " + uid + " with id: " + str(studentPlan.key.urlsafe())
        self.response.set_status(201)
        #return the created plan
        self.response.write(studentPlan.to_dict())

class PlanVerificationHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        print "unimplemented"
        
# populates a few sample users into the db for testing purposes
class PopHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        stubStudents = [ "rush8192", "kshin" ]
        for student in stubStudents:
            matchingStudent = Student.query(Student.student_id == student).get()
            if matchingStudent == None:
                studentObj = Student(student_id=student,academic_plans=[])
                studentObj.put()
                print "populated db with student: " + student
        
#--------------Begin Program Sheet Handlers-----------------------#

def __str_to_int(str):
    if str == '':
        return 0
    else:
        return int(str)

def __str_to_float(str):
    if str == '':
        return 0
    else:
        return float(str)

class ProgramSheetHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_program_sheet(ps_key=self.request.get('ps_key')))

    @createStudent
    def post(self):
        ps_dict = json.loads(self.request.get('ps_json'))
        print ps_dict
        ps_name = ps_dict['ps_name']
        req_box_array = ps_dict['req_boxes']
        outputMessage(self, add_program_sheet(ps_name, req_box_array), False)

    @createStudent
    # ProgramSheet exist verifier
    def put(self):
        ps_name = self.request.get('ps_name')
        outputMessage(self, program_sheet_exists(ps_name), send_data_back=True)

    @createStudent
    def delete(self):
        ps_name = self.request.get('ps_name')
        outputMessage(self, remove_program_sheet(ps_name), False)

class ProgramSheetSearchHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_program_sheet_by_prefix(ps_name_prefix= self.request.get('ps_name_prefix')))

class ReqBoxHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_req_box(rb_key = self.request.get('rb_key')))

class ReqCourseHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_req_course(rc_key = self.request.get('rc_key')))

#--------------End Program Sheet Handlers-----------------------#

app = webapp2.WSGIApplication([
    ('/setupinitial7', MainHandler), 
    ('/api/trans/upload', TranscriptHandler), # Rush
    ('/api/plan(/.*)?', PlanHandler), # Rush
    ('/api/populate', PopHandler), # Rush
    ('/api/plan/verify', PlanVerificationHandler), # Rush
    ('/api/student', StudentHandler), # Ryan (test function)
    ('/api/student/course', CandidateCourseHandler), # Ryan
    ('/api/student/course/(.+)', CandidateCourseHandler), # Ryan
    ('/api/course/search/(.*)', CourseSearchHandler), # Ryan
    ('/api/course/(.+)', CourseHandler), # Ryan
    ('/api/programsheet', ProgramSheetHandler), # Kevin
    ('/api/programsheet/search', ProgramSheetSearchHandler), # Kevin
    ('/api/programsheet/reqbox', ReqBoxHandler), # Kevin
    ('/api/programsheet/reqbox/reqcourses', ReqCourseHandler) # Kevin
], debug=True)
