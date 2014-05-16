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
from webapp2 import uri_for
import add_courses, add_majors
from ops import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        # add_courses.main()
        # add_majors.main()
        # student = create_student(0, 'Ryan')
        self.response.write(uri_for('get_student', student_id=None, student_name='Ryan'))
    
class TranscriptHandler(webapp2.RequestHandler):
    def post(self):
        import parser
        print "calling parser..."        
        parser.getTransContent(self.request.body_file.file, self.response)
        
    def get(self):
        self.response.write('only accepts POST requests')
        
#------------Horrendous List of CRUD Handlers-----------------#
#-They exist solely to pass parameters to their ops.py method-#
class GetStudentHandler(webapp2.RequestHandler): 
    def get(self):
        student_id = self.request.get('student_id')
        if student_id != '':
            student_id = int(student_id)
        else: student_id = None
        student_name = self.request.get('student_name')
        self.response.write(get_student(student_id, student_name))
    def post(self):
       self.response.write(error('only accepts GET requests'))
        
class CreateStudentHandler(webapp2.RequestHandler): 
    def get(self):
        student_id = self.request.get('student_id')
        if student_id != '':
            student_id = int(student_id)
        else: student_id = None
        student_name = self.request.get('student_name')
        self.response.write(create_student(student_id, student_name))
    def post(self):
       self.response.write(error('only accepts GET requests'))
       
class AddCCHandler(webapp2.RequestHandler): 
    def get(self):
        student_id = self.request.get('student_id')
        if student_id != '':
            student_id = int(student_id)
        else:
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
    def post(self):
       self.response.write(error('only accepts GET requests'))
       
class RemoveCCHandler(webapp2.RequestHandler): 
    def get(self):
        student_id = self.request.get('student_id')
        if student_id != '':
            student_id = int(student_id)
        else:
            student_id = None
        course_num = self.request.get('course_num')
        ps = self.request.get('ps')
        if ps == '':
            ps = None
        self.response.write(remove_candidate_course(student_id=student_id,
                                                    course_num=course_num,
                                                    ps=ps))
    def post(self):
       self.response.write(error('only accepts GET requests'))
       
class AddCourseHandler(webapp2.RequestHandler): 
    def get(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(add_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    def post(self):
       self.response.write(error('only accepts GET requests'))
       
class EditCourseHandler(webapp2.RequestHandler): 
    def get(self):
        course_num = self.request.get('course_num')
        course_desc = self.request.get('course_desc')
        course_title = self.request.get('course_title')
        self.response.write(edit_course_listing(course_num=course_num,
                                                course_desc=course_desc,
                                                course_title=course_title))
    def post(self):
       self.response.write(error('only accepts GET requests'))
       
class RemoveCourseHandler(webapp2.RequestHandler): 
    def get(self):
        course_num = self.request.get('course_num')
        self.response.write(remove_course_listing(course_num=course_num))
    def post(self):
       self.response.write(error('only accepts GET requests'))
              
class GetCourseListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(get_master_course_list())
    def post(self):
       self.response.write(error('only accepts GET requests')) 
       
class GetCourseHandler(webapp2.RequestHandler): 
    def get(self):
        course_num = self.request.get('course_num')
        self.response.write(get_course_listing(course_num=course_num))
    def post(self):
       self.response.write(error('only accepts GET requests')) 
#--------------------End CRUD Handlers-------------------------#
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trans/upload', TranscriptHandler),
    ('/student/get/', GetStudentHandler),
    ('/student/create/', CreateStudentHandler),
    ('/student/add_class/', AddCCHandler),
    ('/student/remove_class/', RemoveCCHandler),
    ('/course/add/', AddCourseHandler),
    ('/course/remove/', RemoveCourseHandler),
    ('/course/edit/', EditCourseHandler),
    ('/course/all/', GetCourseListHandler),
    ('/course/get/', GetCourseHandler)
], debug=True)
