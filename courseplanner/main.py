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
import reqs
import cStringIO
import urllib
import sps

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
        add_courses.main()
        #add_majors.main()

class TranscriptHandler(webapp2.RequestHandler):
    @createStudent
    def post(self):
        import parser
        print "calling parser..."
        courseFp = cStringIO.StringIO()
        parser.getTransContent(self.request.body_file.file, courseFp)
        print courseFp.getvalue()
        
        user = users.get_current_user();
        uid = user.user_id()
        
        matchingStudent = Student.query(Student.student_id == uid).get()
        for course in courseFp.getvalue().split("\n"):
            if course == "":
                continue
            splitCourse = course.split("||")
            courseId = splitCourse[0]
            # second term is course title; we should be able to pull from DB
            year = int(splitCourse[2][0:4])
            term = splitCourse[3]
            # fourth term is units attempted; fifth is units earned
            units = int(float(splitCourse[5]))
            grade = ops.gradeToFloat(splitCourse[6])
            matchingCourse = Course.query(Course.course_num == courseId).get()
            if matchingCourse == None:
                print "possible error: no matching class: " + courseId
                continue
            for academicPlan in matchingStudent.academic_plans:
                plan = academicPlan.get()
                alreadyHasCourse = False
                for checkCandCourse in plan.student_course_list:
                    if checkCandCourse.get().course.get().course_num == matchingCourse.course_num:
                        alreadyHasCourse = True
                        break
                if alreadyHasCourse:
                    print "student : " + uid + " already has course: " + matchingCourse.course_num
                    continue
                
                candCourse = Candidate_Course(course=matchingCourse.key, student=matchingStudent.key,
                                    term=term, year=year, grade=grade, units=units)
                candCourse.put()
                plan.student_course_list.append(candCourse.key)
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
    def post(self):
        student_id = users.get_current_user().user_id()
        units = self.request.get('units')
        if units != '':
            units = int(units)
        else: units = None
        grade = self.request.get('grade')
        if grade != '':
            grade = float(grade)
        else: grade = None

        course_key = self.request.get('course_key')

        year = self.request.get('year')
        if year != '':
            year = int(year)
        else: year = None

        term = self.request.get('term')

        self.response.write(add_candidate_course(student_id=student_id,
                                                 course_key=course_key,
                                                 grade=grade,
                                                 units=units,
                                                 year=year,
                                                 term=term))
    @createStudent
    def get(self):
        student_id = users.get_current_user().user_id()
        self.response.write(get_candidate_courses(student_id=student_id))

    @createStudent
    def delete(self, cand_course_key):
        student_id = users.get_current_user().user_id()
        if student_id == '':
            student_id = None
        self.response.write(remove_candidate_course(student_id=student_id,
                                                    cand_course_key=cand_course_key))

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
    def put(self, course_key):
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
        print 'Reached Search Handler'
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
            uid = user.user_id()
        student = Student.query(Student.student_id == uid).get()
        if student == None:
            self.response.write('Error: no matching student record for student: ' + uid)
            return
        else:
            if planid == None or planid == "/": #no argument; just return all plans for student
                # not sure how to return a repeated ndb entity
                #
                print "Listing all plans for " + uid
                planArray = []
                plan = student.academic_plans[0].get()
                for sheetKey in plan.program_sheets:
                    sheet = sheetKey.get()
                    planInfoDict = {}
                    planInfoDict['sps_name'] = sheet.program_sheet.get().ps_name
                    planInfoDict['sps_key'] = sheet.key.urlsafe()
                    planArray.append(planInfoDict)
                self.response.write(json.dumps(planArray))
            else:
                # remove the "/" from planid
                planid = planid[1:]
                print planid

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
            uid = user.user_id()
        title = self.request.get('title')
        print "creating new plan for: " + uid + " with title: " + title

        # first we load the GER program sheet, and add it to a new plan

        GER_SHEET_NAME = "GER-PRE-2015" #TODO: this needs to be changed to the correct value
        
        matchingStudent = Student.query(Student.student_id == uid).get()
        if matchingStudent == None:
            self.response.write('Error: no matching student record for: ' + uid)
            return

        gerSheet = Program_Sheet.query(Program_Sheet.ps_name == GER_SHEET_NAME).get()
        studentGerSheet = Student_Program_Sheet(program_sheet=gerSheet.key,
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
    def get(self, sps_id, cc_id, req_id):
        success, message = reqs.verifyCourseForBox(sps_id, cc_id, req_id)
        print json.dumps(dict(success=success,message=message))
        self.response.write(json.dumps(dict(success=success,message=message)))

class AddCourseToPlanHandler(webapp2.RequestHandler):
    @createStudent
    def post(self, sps_id, cc_id, req_id):
        status = reqs.addCourseForBox(sps_id, cc_id, req_id)
        self.response.status = status
        
    @createStudent
    def delete(self, sps_id, cc_id, req_id):
        status = reqs.deleteCourseForBox(sps_id, cc_id, req_id)
        self.response.status = status
        
class PlanPetitionStatusHandler(webapp2.RequestHandler):
    @createStudent
    def get(self, sps_id, cc_id, req_id):
        success, message = reqs.checkStatusForCourseInBox(sps_id, cc_id, req_id)
        print json.dumps(dict(success=success,message=message))
        self.response.write(json.dumps(dict(success=success,message=message)))
        
class BoxVerificationHandler(webapp2.RequestHandler):
    @createStudent
    def get(self, sps_id, box_id):
        success, message = reqs.verifyBox(sps_id, box_id)
        print json.dumps(dict(success=success,message=message))
        self.response.write(json.dumps(dict(success=success,message=message)))
        
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
        result = get_program_sheet(ps_key=self.request.get('ps_key'))
        outputMessage(self, result)

    @createStudent
    def post(self):
        ps_json = urllib.unquote(self.request.get('ps_json')).decode('utf8') 
        ps_dict = json.loads(ps_json)
        ps_name = ps_dict['ps_name']
        req_box_array = ps_dict['req_boxes']
        result = add_program_sheet(ps_name, req_box_array)
        outputMessage(self, result, False)

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
    def get(self, ps_name_prefix):
        outputMessage(self, get_program_sheet_by_prefix(ps_name_prefix))

class ReqBoxHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_req_box(rb_key = self.request.get('rb_key')))

class ReqCourseHandler(webapp2.RequestHandler):
    @createStudent
    def get(self):
        outputMessage(self, get_req_course(rc_key = self.request.get('rc_key')))

#--------------End Program Sheet Handlers-----------------------#

# returns the student program sheet json object used by the main frontend UI
class SpsHandler(webapp2.RequestHandler):
    @createStudent
    def get(self, sps_key):
        sps_obj = ndb.Key(urlsafe=sps_key).get()
        if sps_obj == None:
            print "invalid sps key: no matching sps found"
            self.response.status = 400
            self.response.write("Invalid S.P.S. key")
            return
            
        sps_dict = sps.getSpsDict(sps_obj, sps_key)
        self.response.write(json.dumps(sps_dict))
    
    @createStudent
    def post(self, ps_key):
        ps_obj = ndb.Key(urlsafe=ps_key).get()
        if ps_obj == None:
            print "invalid program sheet key; no matching program sheet found"
            self.response.status = 400
            self.response.write("Invalid ps key")
            return
        uid = users.get_current_user().user_id()
        allow_double = self.request.get('allow_double_count')
        if allow_double == None or allow_double == "" or "false" in allow_double:
            allow_double = False
        else:
            allow_double = True
        self.response.status = sps.createSpsForProgramSheet(ps_obj, uid, allow_double)
        print "attempted to create new sps; status code: " + self.response.status
        
        
    @createStudent  
    def delete(self, sps_key):
        sps_obj = ndb.Key(urlsafe=sps_key).get()
        if sps_obj == None:
            print "invalid sps key: no matching sps found"
            self.response.status = 400
            self.response.write("Invalid S.P.S. key")
            return

        uid = users.get_current_user().user_id()
        self.response.status = sps.deleteSps(sps_key, uid)

app = webapp2.WSGIApplication([
    ('/setupinitial7', MainHandler), 
    ('/api/trans/upload', TranscriptHandler), # Rush
    ('/api/plan/verify/(.*)/(.*)/(.*)', PlanVerificationHandler), # Rush
    ('/api/plan/verifybox/(.*)/(.*)', BoxVerificationHandler), # Rush
    ('/api/plan/add/(.*)/(.*)/(.*)', AddCourseToPlanHandler), # Rush (also deletes)
    ('/api/plan/petitionstatus/(.*)/(.*)/(.*)', PlanPetitionStatusHandler), # Rush
    ('/api/plan(/.*)?', PlanHandler), # Rush
    ('/api/populate', PopHandler), # Rush
    ('/api/sps/(.+)', SpsHandler),
    ('/api/student', StudentHandler), # Ryan (test function)
    ('/api/student/course/', CandidateCourseHandler), # Ryan
    ('/api/student/course/(.+)', CandidateCourseHandler), # Ryan
    ('/api/course/search/(.*)', CourseSearchHandler), # Ryan
    ('/api/course/(.+)', CourseHandler), # Ryan
    ('/api/programsheet', ProgramSheetHandler), # Kevin
    ('/api/programsheet/search/(.+)', ProgramSheetSearchHandler), # Kevin
    ('/api/programsheet/reqbox', ReqBoxHandler), # Kevin
    ('/api/programsheet/reqbox/reqcourses', ReqCourseHandler) # Kevin
], debug=True)
