from google.appengine.ext import db
import json
from models import *

# Read majors from json data file and add to datastore. 
# For now, single dummy major with CS106A as only req

def main():
    m = Major(major_id=0, major_name='CS', track_name='AI')
    q = db.GqlQuery("SELECT * FROM Course WHERE course_num = :1", "CS 106A")
    course = [c for c in q.run()][0].key()
    c = Req_Course(course_req_id = 0, allowed_courses = [course])
    m.put()
    c.put()
