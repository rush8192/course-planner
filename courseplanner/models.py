from google.appengine.ext import ndb

class Offering(ndb.Model): pass
class Course(ndb.Model):
    course_num = ndb.StringProperty(required=True)
    course_desc = ndb.TextProperty()
    rankings_sum = ndb.IntegerProperty()
    rankings_tally = ndb.IntegerProperty()
    hpw_sum = ndb.IntegerProperty()
    hpw_tally = ndb.IntegerProperty()
    offerings = ndb.KeyProperty(Offering, repeated=True)

class Offering(ndb.Model):
    course = ndb.KeyProperty(Course)
    course_title = ndb.StringProperty(required=True)
    # repeated=True gives list of Strings
    term = ndb.StringProperty(repeated=True)
    grading = ndb.StringProperty()
    instructors = ndb.StringProperty(repeated=True)
    reqs = ndb.StringProperty(repeated=True)
    year = ndb.StringProperty()
    units = ndb.IntegerProperty(repeated=True)

class Req_Box(ndb.Model): pass
class Major(ndb.Model):
    major_id = ndb.IntegerProperty(required=True)
    major_name = ndb.StringProperty(required=True)
    track_name = ndb.StringProperty(required=True)
    req_boxes = ndb.KeyProperty(Req_Box, repeated=True)

# Requirement box for major requirements
class Req_Box(ndb.Model):
    major = ndb.KeyProperty(Major)
    req_id = ndb.IntegerProperty(required=True)
    req_box_name = ndb.StringProperty(required=True)
    min_total_units = ndb.IntegerProperty()
    min_num_courses = ndb.IntegerProperty()
    # TODO - structure conditional ops
    conditional_ops = ndb.StringProperty()
    # List of Req_Course: (0/1):many relationship
    req_courses = ndb.KeyProperty(repeated=True)

# GER
class Grad_Req(ndb.Model):
    req_name = ndb.StringProperty()
    # List of Req_Course: (0/1):many relationship
    req_courses = ndb.KeyProperty(repeated=True)
    candidate_course = ndb.KeyProperty(Course)
    candidate_course_units = ndb.IntegerProperty()

# Required Course belonging either to a Req_Box (major requirement)
# or Grad_Req (GER)
class Req_Course(ndb.Model):
    course_req_id = ndb.IntegerProperty()
    display_title = ndb.StringProperty()
    course_req_type = ndb.StringProperty()
    min_grade = ndb.FloatProperty()
    # TODO - structure force error
    force_error = ndb.StringProperty()
    # many-to-many courses to requirement fulfilled
    allowed_courses = ndb.KeyProperty(repeated=True)

class Candidate_Course(ndb.Model): pass
class Student(ndb.Model):
    student_id = ndb.IntegerProperty(required=True)
    name = ndb.StringProperty()
    major = ndb.KeyProperty(Major)
    courses = ndb.KeyProperty(Candidate_Course, repeated=True)

class Candidate_Course(ndb.Model):
    course = ndb.KeyProperty(Course)
    req_course = ndb.KeyProperty(Req_Course)
    grade = ndb.FloatProperty()
    units = ndb.IntegerProperty()
    # each student has many candidate courses
    student = ndb.KeyProperty(Student)

