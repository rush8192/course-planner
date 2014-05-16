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
from google.appengine.ext import db
import add_courses, add_majors, ops
import models

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        #add_courses.main()
        #add_majors.main()
        
        # test datastore features
        ops.create_student('Ryan', 0)
        #ops.get_course_json('CS 106A')
    
class TranscriptHandler(webapp2.RequestHandler):
    def post(self):
        import parser
        print "calling parser..."        
        parser.getTransContent(self.request.body_file.file, self.response)
        
    def get(self):
        self.response.write('only accepts POST requests')
    
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
        matchingStudent = db.GqlQuery("SELECT * FROM Student WHERE student_id IN :1",
                                [ uid ])
        student = matchingStudent.get()
        if student == None:
            self.response.write('Error: no matching student record for student: ' + uid)
        else:
            for plan in student.academic_plans:
                if plan.program_sheets[0].program_sheet.ps_name == planId:
                    self.response.write('Found matching plan: ' + planId + ' for student: ' + uid)
                    # fill in JSON object and return
                    return
        self.response.write('Error: no matching program sheet found with id: ' + planId + ' for student: ' + uid)


    # POST: allows the user to create a new plan for the given major/minor ID field
    def post(self):
        user = users.get_current_user();
        uid = ""
        if (user == None):
            uid = self.request.get('uid')
        else:
            uid = user.nickname()
        print "creating new plan for: " + uid
        planId = self.request.get('plan_id')
        candidateSheet = db.GqlQuery("SELECT * FROM Program_Sheet WHERE ps_name IN :1",
                                [ planId ]).get()
        if candidateSheet == None:
            self.response.write('Error: invalid plan ID')
        else:
            print "found matching plan: " + candidateSheet.ps_name
            plan = Student_Program_Sheet(program_sheet=candidateSheet,
                        cand_courses=[])
            plan.put()
            matchingStudent = db.GqlQuery("SELECT * FROM Student WHERE student_id IN :1",
                                [ uid ]).get()
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
    ('/plan/(.*)', PlanHandler),
    ('/plan/verify', PlanVerificationHandler)
], debug=True)
