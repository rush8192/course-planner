
import sys
import models
from models import Req_Fullfillment
from google.appengine.ext import ndb

def verifyCourseForBox(sps_id, cc_id, req_id):
    sps = ndb.Key(urlsafe=sps_id).get()
    if sps == None:
        print "No matching student program sheet found"
        return __fail("No matching student program sheet found")
    cc = ndb.Key(urlsafe=cc_id).get()
    if cc == None:
        print "No matching candidate course found"
        return __fail("No matching candidate course found")
    req_box = ndb.Key(urlsafe=req_id).get()
    if req_box == None:
        print "No matching requirement box found"
        return __fail("No matching requirement box found")
    
    # check that course is allowed for this box
    allowed = False
    for allowed_course_key in req_box.allowed_courses:
        if allowed_course_key == cc.course:
            allowed = True
            break
    if not allowed:
        print "Course " + str(cc_id) + " not allowed for " + str(req_id)
        return __fail("Course: " + cc.course.get().course_num + " does not fullfill this requirement.")
    
    # check that course hasn't already been added to this Student_Program_Sheet
    if not sps.allow_double_count:
        for cand_course_key in sps.cand_courses:
            if cand_course_key.id() == cc_id:
                print "Course " + str(cc_id) + " is double counted"
                return __fail("Can't double count course: " + cc.course.get().course_num)
    
    # check minimum grade and units
    if cc.units < req_box.min_units:
        print "Course " + str(cc_id) + " does not have enough units"
        return __fail("Course: " + cc.course.get().course_num + " taken for " + str(cc.units) + " units; " + str(req_box.min_units) + " needed")  
    if cc.grade == None or cc.grade < req_box.min_grade:
        print "Course " + str(cc_id) + " has too poor a grade"
        return __fail("Grade received (" + str(cc.grade) + ") is below minimum value of " + str(req_box.min_grade))
        
    return __success()
    
def addCourseForBox(sps_id, cc_id, req_id):
    print "Adding course to box"
    sps = ndb.Key(urlsafe=sps_id).get()
    if sps == None:
        print "No matching student program sheet found"
        return 400
    cc = ndb.Key(urlsafe=cc_id).get()
    if cc == None:
        print "No matching candidate course found"
        return 400
    req_box = ndb.Key(urlsafe=req_id).get()
    if req_box == None:
        print "No matching requirement box found"
        return 400
        
    success, message = verifyCourseForBox(sps_id, cc_id, req_id)
    
    req_f = Req_Fullfillment(req_course=req_box.key, valid=success, error_message=message, program_sheet=sps.key)
    req_f.put()
    cc.reqs_fulfilled.append(req_f.key)
    cc.put()
    sps.cand_courses.append(cc.key)
    sps.put()
    return 200
    
def checkStatusForCourseInBox(sps_id, cc_id, req_id):
    sps = ndb.Key(urlsafe=sps_id).get()
    if sps == None:
        print "No matching student program sheet found"
        return __fail("No matching student program sheet found")
    cc = ndb.Key(urlsafe=cc_id).get()
    if cc == None:
        print "No matching candidate course found"
        return __fail("No matching candidate course found")
    req_box = ndb.Key(urlsafe=req_id).get()
    if req_box == None:
        print "No matching requirement box found"
        return __fail("No matching requirement box found")
        
    for req_f_key in cc.reqs_fulfilled:
        req_f = req_f_key.get()
        if req_f.req_course.urlsafe() == req_id and req_f.program_sheet.urlsafe() == sps_id:
            return req_f.valid, req_f.error_message
            
    print "no candidate course found fulfilling supplied req_course for given plan"
    return False, "Candidate Course is not currently being used for given box"
        
def verifyBox(sps_id, box_id):
    sps = ndb.Key(urlsafe=sps_id).get()
    if sps == None:
        print "No matching student program sheet found"
        return __fail("No matching student program sheet found")
    box = ndb.Key(urlsafe=box_id).get()
    if box == None:
        print "No matching box found"
        return __fail("No matching box found")
        
    boxCourses = []
    print "sps has total courses numbering: " + str(len(sps.cand_courses))
    for cc_key in sps.cand_courses:
        cc = cc_key.get()
        if cc == None or cc.reqs_fulfilled == None:
            continue
        for req_f_key in cc.reqs_fulfilled:
            req_f = req_f_key.get()
            if req_f.req_course.get().req_box.urlsafe() == box.key.urlsafe():
                boxCourses.append(cc_key)
                print "added course: " + cc.course.get().course_num

    totalCourses = len(boxCourses)
    if totalCourses < box.min_num_courses:
        return __fail("Not enough courses in box; have " + str(totalCourses) + ", need " + str(box.min_num_courses))

    totalUnits = 0
    for course_key in boxCourses:
        course = course_key.get()
        totalUnits += course.units
    if totalUnits < box.min_total_units:
        return __fail("Insufficient units in box; have " + str(totalUnits) + ", need " + str(box.min_total_units))
        
    print "units: " + str(totalUnits) + " courses: " + str(totalCourses)
        
    condOpSuccess, message = __validateCondOps(sps, box)
    if not condOpSuccess:
        return __fail(message)
        
    return __success()
        
    
def __validateCondOps(sps, box):
    return True, ""
    
    
       
def __fail(error):
    return False, error
    
def __success():
    return True, ""