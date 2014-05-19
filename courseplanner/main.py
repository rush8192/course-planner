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
from google.appengine.api import users
from google.appengine.ext import ndb
import add_courses, add_majors, ops
from models import Student, Program_Sheet
from webapp2 import uri_for
from ops import *
from PSHandlers import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        add_courses.main()
        # add_majors.main()
        # student = create_student(0, 'Ryan')
        #self.response.write(uri_for('get_student', student_id=None, student_name='Ryan'))
    
class TranscriptHandler(webapp2.RequestHandler):
    def post(self):
        import parser
        print "calling parser..."        
        parser.getTransContent(self.request.body_file.file, self.response)
        
    def get(self):
        self.response.write('only accepts POST requests')
        
#---------------Student/Course CRUD Handlers-------------------#
class StudentHandler(webapp2.RequestHandler): 
    def get(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        student_name = self.request.get('student_name')
        if student_name == '':
            student_name = None
        self.response.write(get_student(student_id, student_name))
    def post(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        student_name = self.request.get('student_name')
        if student_name == '':
            student_name = None
        self.response.write(create_student(student_id, student_name))
        
class CandidateCourseHandler(webapp2.RequestHandler): 
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
    def get(self):
        student_id = self.request.get('student_id')
        if student_id == '':
            student_id = None
        self.response.write(get_candidate_courses(student_id=student_id))
        
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
    def get(self):
        course_num = self.request.get('course_num')
        self.response.write(get_course_listing(course_num=course_num))    
    def post(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(add_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    def put(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(edit_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    def delete(self):
        course_num = self.request.get('course_num')
        self.response.write(remove_course_listing(course_num=course_num))

class CourseListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(get_master_course_list())
        
#----------------End Student/Course Handlers-----------------#


# Class that handles creating and returning student's plans
class PlanHandler(webapp2.RequestHandler):

    # GET: fetch a student's plan for a given major/minor (could this match multiple entries?)
    def get(self, planid):
        user = users.get_current_user();
        uid = ""
        if (user == None):
            uid = self.request.get('uid')
        else:
            uid = user.nickname()
        matchingStudent = Student.query(Student.student_id == 5)
        student = matchingStudent.get()
        if student == None:
            self.response.write('Error: no matching student record for student: ' + uid)
            return
        else:
            for plan in student.academic_plans:
                if plan.program_sheets[0].program_sheet.ps_name == planId:
                    self.response.write('Found matching plan: ' + planId + ' for student: ' + uid)
                    # fill in JSON object and return
                    return
        self.response.write('Error: no matching program sheet found with id: ' + planId + ' for student: ' + uid)


    # POST: allows the user to create a new plan for the given major/minor ID field
    def post(self, pathname):
        user = users.get_current_user();
        uid = ""
        if (user == None):
            uid = self.request.get('uid')
        else:
            uid = user.nickname()
        print "creating new plan for: " + uid
        planId = self.request.get('plan_id')
        candidateSheet = Program_Sheet.query(Program_Sheet.ps_name == planId).get()
        if candidateSheet == None:
            self.response.write('Error: invalid plan ID: ' + planId + '\n')
            return
        else:
            print "found matching plan: " + candidateSheet.ps_name
            plan = Student_Program_Sheet(program_sheet=candidateSheet,
                        cand_courses=[])
            plan.put()
            matchingStudent = Student.query(Student.student_id == uid).get()
            if matchingStudent == None:
                self.response.write('Error: no matching student record for: ' + uid)
            else:
                student.academic_plans.program_sheets.append(plan)
                student.put()
                self.response.write('created new plan successfully for : ' + candidateSheet.ps_name)
    
class PlanVerificationHandler(webapp2.RequestHandler):
    def get(self):
        print "unimplemented"
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trans/upload', TranscriptHandler),
    ('/student/', StudentHandler),
    ('/student/course/', CandidateCourseHandler),
    ('/course/', CourseHandler),
    ('/course/all/', CourseListHandler),    
    ('/plan/(.*)', PlanHandler),
    ('/plan/verify', PlanVerificationHandler),
    ('/programsheet/', ProgramSheetHandler),
    ('/programsheet/reqbox/', ReqBoxHandler),
    ('/programsheet/reqbox/reqcourses', ReqCourseHandler)
], debug=True)
