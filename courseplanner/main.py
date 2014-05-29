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

def outputMessage(self, result):
    if 'errorMessage' not in json.loads(result):
        self.response.write(result)
    else:
        self.response.write('404 Error')
        self.response.set_status(404)

class MainHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        add_courses.main()
        # add_majors.main()
        # student = create_student(0, 'Ryan')
        #self.response.write(uri_for('get_student', student_id=None, student_name='Ryan'))

class TranscriptHandler(webapp2.RequestHandler):
    @createStudent
    def post(self):
        import parser
        print "calling parser..."
        parser.getTransContent(self.request.body_file.file, self.response)

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
    def post(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        units = self.request.get('units')
        if units != '':
            units = int(units)
        else: units = None
        grade = self.request.get('grade')
        if grade != '':
            grade = float(grade)
        else: grade = None
        course_num = self.request.get('course_num')
        force = self.request.get('force')
        if force == 'True':
            force = True
        else: force = False
        units = self.request.get('units')
        req_course = self.request.get('req_course')
        self.response.write(add_candidate_course(student_id=student_id,
                                                 course_num=course_num,
                                                 req_course=req_course,
                                                 grade=grade,
                                                 units=units,
                                                 force=force))
    @createStudent
    def get(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        self.response.write(get_candidate_courses(student_id=student_id))

    @createStudent
    def delete(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        course_num = self.request.get('course_num')
        ps = self.request.get('ps')
        if ps == '':
            ps = None
        self.response.write(remove_candidate_course(student_id=student_id,
                                                    course_num=course_num,
                                                    ps=ps))

class CourseHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        course_num = self.request.get('course_num')
        result = get_course_listing(course_num=course_num)
        outputMessage(self, result)

    @createStudent
    def post(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(add_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    @createStudent
    def put(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(edit_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    @createStudent
    def delete(self):
        course_num = self.request.get('course_num')
        self.response.write(remove_course_listing(course_num=course_num))

class CourseSearchHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        course_num_prefix = self.request.get('course_num_prefix')
        if len(course_num_prefix) > 0:
            self.response.write(get_course_listing_by_prefix(course_num_prefix))

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
                    print "looking at key: " + str(planKey.get().key.id())
                    print "plan id: " + str(planid)
                    if str(planKey.get().key.id()) == str(planid):
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
        print "created new plan for student: " + uid + " with id: " + str(studentPlan.key.id())
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
                
        add_majors.main()
            
        
        

app = webapp2.WSGIApplication([
    ('/setupinitial7', MainHandler), 
    ('/api/trans/upload', TranscriptHandler), # Rush
    ('/api/plan(/.*)?', PlanHandler), # Rush
    ('/api/populate', PopHandler), # Rush
    ('/api/plan/verify', PlanVerificationHandler), # Rush
    ('/api/student', StudentHandler), # Ryan (test function)
    ('/api/student/course', CandidateCourseHandler), # Ryan
    ('/api/course', CourseHandler), # Ryan
    ('/api/course/search', CourseSearchHandler), # Ryan
    ('/api/programsheet', ProgramSheetHandler), # Kevin
    ('/api/programsheet/reqbox', ReqBoxHandler), # Kevin
    ('/api/programsheet/reqbox/reqcourses', ReqCourseHandler) # Kevin
], debug=True)
