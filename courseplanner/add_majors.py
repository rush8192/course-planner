from google.appengine.ext import ndb
import json
from models import *

# Read majors from json data file and add to datastore.
# For now, single dummy major with CS106A as only req

def main():
    #m = Major(major_id=0, major_name='CS', track_name='AI')
    #course = Course.query(Course.course_num == 'CS 106A').fetch(1)[0]
    #c = Req_Course(course_req_id = 0, allowed_courses = [course.key])
    #m.put()
    #c.put()
    __add_gers()


# Adds the program sheet for GERs (only applies to class of 2015 and earlier)
def __add_gers():
    gerPlan = 'GERs'
    gerSheet = Program_Sheet.query(Program_Sheet.ps_name == gerPlan).get()
    if gerSheet == None:
        import json
        gerSheetJson = json.load(open("Data/old_req_json"))
        gerSheet = Program_Sheet(ps_name = gerSheetJson['ps_name'])
        gerSheetKey = gerSheet.put()
        for boxJson in gerSheetJson['req_boxes']:
            print "creating box: " + boxJson['req_box_name']
            boxModel = Req_Box(program_sheet=gerSheetKey, req_box_name=boxJson['req_box_name'],
                                min_total_units=boxJson['min_total_units'], min_num_courses=boxJson['min_num_courses'],
                                req_courses=[])
            boxModelKey = boxModel.put()
            gerSheet.req_boxes.append(boxModelKey)
            for reqCourseJson in boxJson['req_courses']:
                print "creating course box: " + reqCourseJson['req_course_info']
                reqCourse = Req_Course(req_box = boxModelKey, req_course_name = reqCourseJson['req_course_name'], req_course_info = reqCourseJson['req_course_info'],
                                        min_grade=reqCourseJson['min_grade'], min_units=reqCourseJson['min_units'])
                reqCourseKey = reqCourse.put()
                boxModel.req_courses.append(reqCourseKey)
                for courseTitle in reqCourseJson['allowed_courses']:
                    #print "adding course to box: " + courseTitle
                    courseModel = Course.query(Course.course_num == courseTitle).get()
                    if courseModel != None:
                        reqCourse.allowed_courses.append(courseModel.key)
                    #else:
                        #print "no matching course object for: " + courseTitle
                reqCourse.put()
            boxModel.put()
        gerSheet.put()
