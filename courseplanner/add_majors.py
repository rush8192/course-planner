from google.appengine.ext import ndb
import json
from models import *

# Read majors from json data file and add to datastore. 
# For now, single dummy major with CS106A as only req

def main():
    m = Major(major_id=0, major_name='CS', track_name='AI')
    course = Course.query(Course.course_num == 'CS 106A').fetch(1)[0]
    c = Req_Course(course_req_id = 0, allowed_courses = [course.key])
    m.put()
    c.put()
