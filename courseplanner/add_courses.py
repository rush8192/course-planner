from google.appengine.ext import db
import json
from models import *

# Read course listings from json data file and add to datastore.

def main():
    in_file = open('Data/courses_json', 'r')
    courses = json.loads(in_file.read())
    for course_id in courses:
        course = courses[course_id]
        # Add General Course Information
        c = Course(course_num = course['course_num'],
                   course_desc = course['course_desc'],
                   rankings_sum = course['rankings_sum'],
                   rankings_tally = course['rankings_tally'],
                   hpw_sum =  course['hpw_sum'],
                   hpw_tally = course['hpw_tally'])

        # Add Information about each Offering for a Course
        for offering in course['offering']:
            if type(offering['reqs']) != list:
              offering['reqs'] = []
            if type(offering['instructors']) != list:
              offering['instructors'] = []
            if type(offering['term']) != list:
              offering['term'] = []
            c.course_title = offering['course_title']
            o = Offering(term = offering['term'],
                         grading = offering['grading'],
                         instructors = offering['instructors'],
                         reqs = offering['reqs'],
                         year = offering['year'],
                         units = offering['units'],
                         course = c.key)
            o.put()
        c.put()
        break
