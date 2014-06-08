
import json
import models
import reqs
from google.appengine.ext import ndb

""" returns an object of the following form:
{
    "ps_name" : ps_name,
    "sps_key" : sps_key,
    "req_boxes" :
        [
            {"req_box_name":req_box_name,
             "req_box_key": req_box_key,
             "min_total_units":min_total_units,
             "min_num_courses":min_num_courses,
             "total_units":total_units,
             "num_courses":num_courses,
             "req_courses": 
                 [
                      {
                       "req_course_name":req_course_name,
                       "req_course_info":req_course_info,
                       "req_course_key":req_course_key,
                       "cand_course_name": cand_course_name,
                       "cand_course_key":cand_course_key,
                       "cand_course_units":cand_course_units,
                       "cand_course_gpa":cand_course_gpa,
                       "cand_course_valid":true|false
                       "cand_course_error":error message
                      }
                 ]
            }
        ]
}"""

def getSpsDict(sps, sps_key):
    sps_dict = {}
    sps_dict['ps_name'] = sps.program_sheet.get().ps_name
    sps_dict['sps_key'] = sps_key
    
    rect_box_array = []
    
    for req_box_key in sps.program_sheet.get().req_boxes:
        req_box = req_box_key.get()
    
        req_box_dict = {}
        
        req_box_dict['req_box_name'] = req_box.req_box_name
        req_box_dict['req_box_key'] = req_box_key.urlsafe()
        req_box_dict['min_total_units'] = req_box.min_total_units
        req_box_dict['min_num_courses'] = req_box.min_num_courses
        
        req_course_array = []
        numCourses = 0
        totalUnits = 0
        
        for req_course_key in req_box.req_courses:
            req_course_dict = {}
            req_course = req_course_key.get()
            req_course_dict['req_course_name'] = req_course.req_course_name
            req_course_dict['req_course_info'] = req_course.req_course_info
            req_course_dict['req_course_key'] = req_course_key.urlsafe()
            
            req_cc = None
            for cc_key in sps.cand_courses:
                cc = cc_key.get()
                if cc == None or cc.reqs_fulfilled == None:
                    continue
                for req_f_key in cc.reqs_fulfilled:
                    req_f = req_f_key.get()
                    if req_f == None:
                        continue
                    if req_f.req_course.urlsafe() == req_course_key.urlsafe():
                        req_cc = cc
                        break
                if req_cc != None:
                    break;
            
            if req_cc != None:
                numCourses += 1
                totalUnits += req_cc.units
                valid, message = reqs.checkStatusForCourseInBox(sps_key, req_cc.key.urlsafe(), req_course_key.urlsafe())
            
            req_course_dict['cand_course_name'] = req_cc.course.get().course_num if req_cc != None else ""
            req_course_dict['cand_course_key'] = req_cc.key.urlsafe() if req_cc != None else ""

            req_course_dict['fulfilling'] = {} if req_cc != None else None
            if req_course_dict['fulfilling'] != None:
                req_course_dict['fulfilling']['course_num'] = req_course_dict['cand_course_name']
                req_course_dict['fulfilling']['cand_course_key'] = req_course_dict['cand_course_key']

            req_course_dict['cand_course_units'] = req_cc.units if req_cc != None else 0
            req_course_dict['cand_course_gpa'] = req_cc.grade if req_cc != None else 0
            req_course_dict['cand_course_valid'] = valid if req_cc != None else False
            req_course_dict['cand_course_error'] = message if req_cc != None else ""
            req_course_dict['course_key'] = req_cc.course.urlsafe() if req_cc != None else ""
            
            
            
            req_course_array.append(req_course_dict)
        
        req_box_dict['total_units'] = totalUnits
        req_box_dict['num_courses'] = numCourses
        
        req_box_dict['req_courses'] = req_course_array
        
        rect_box_array.append(req_box_dict)
        
    sps_dict['req_boxes'] = rect_box_array   
    totalGrade = 0
    totalUnits = 0
    for box in sps_dict['req_boxes']:
        for course in box['req_courses']:
            units = course['cand_course_units']
            totalGrade += units * course['cand_course_gpa']
            totalUnits += units
    if totalUnits == 0:
        gpa = 0.0
    else: 
        gpa = totalGrade/totalUnits
    sps_dict['ps_gpa'] = gpa    
    return sps_dict
    
def createSpsForProgramSheet(ps_obj, uid, allow_double):
    user = models.Student.query(models.Student.student_id == uid).get()
    if user == None:
        print "no matching student for sps creation query: " + uid
        return 400
    
    sps_obj = models.Student_Program_Sheet(program_sheet=ps_obj.key, allow_double_count=allow_double,
                                            cand_courses = [])
    sps_obj.put()
    
    plan = user.academic_plans[0].get()
    plan.program_sheets.append(sps_obj.key)
    plan.put()
    return 200
    
def deleteSps(sps_key, uid):
    user = models.Student.query(models.Student.student_id == uid).get()
    if user == None:
        print "no matching student for sps creation query: " + uid
        return 400
    
    sps_key = ndb.Key(urlsafe=sps_key)
    plan = user.academic_plans[0].get()
    plan.program_sheets.remove(sps_key)
    plan.put()
    sps_key.delete()
    return 200
    