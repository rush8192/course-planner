from google.appengine.ext import db
import json
from models import *

# Read course listings from json data file and add to datastore. 

def main():
    in_file = open('Data/courses_json', 'r')
    courses = json.loads(in_file.read())
    for course in courses:
        course = courses[course]
        c = Course(course_num = course['course_num'],
                   course_desc = course['course_desc'])
        c.put()
