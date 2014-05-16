from google.appengine.ext import ndb

# stubs for all classes with cyclical references
class Offering(ndb.Model): pass
class Requirement(ndb.Model): pass
class Req_Box(ndb.Model): pass
class Req_Course(ndb.Model): pass

#------------------Begin Course Models-------------------#
class Course(ndb.Model):
    course_num = ndb.StringProperty(required=True)
    course_title = ndb.StringProperty()
    course_desc = ndb.TextProperty()
    rankings_sum = ndb.IntegerProperty()
    rankings_tally = ndb.IntegerProperty()
    hpw_sum = ndb.IntegerProperty()
    hpw_tally = ndb.IntegerProperty()
    offerings = ndb.KeyProperty(Offering, repeated=True)

class Offering(ndb.Model):
    course = ndb.KeyProperty(Course)
    # repeated=True gives list of Strings
    term = ndb.StringProperty(repeated=True)
    grading = ndb.StringProperty()
    instructors = ndb.StringProperty(repeated=True)
    reqs = ndb.StringProperty(repeated=True)
    year = ndb.StringProperty()
    units = ndb.IntegerProperty(repeated=True)
#---------------------End Course Models--------------------#

#----------------Begin Program Sheet Models----------------#
# Program sheet for a major/GER/minor: Contains 1+ Req_Boxes
class Program_Sheet(ndb.Model):
    ps_name = ndb.StringProperty()
    major_id = ndb.IntegerProperty()
    req_boxes = ndb.KeyProperty(Req_Box, repeated=True)

# Requirement box such as depth or DB:Hum
class Req_Box(ndb.Model):
    program_sheet = ndb.KeyProperty(Program_Sheet)
    req_box_name = ndb.StringProperty(required=True)
    min_total_units = ndb.IntegerProperty()
    min_num_courses = ndb.IntegerProperty()
    # TODO(kevin) - structure conditional ops
    conditional_ops = ndb.StringProperty()
    # List of fulfilling courses
    req_courses = ndb.KeyProperty(Req_Course, repeated=True)

# Required Course belonging to a Req_Box (major requirement or GER req)
class Req_Course(ndb.Model):
    req_box = ndb.KeyProperty(Req_Box)
    req_course_title = ndb.StringProperty()
    course_req_type = ndb.StringProperty()
    min_grade = ndb.FloatProperty()
    # Many-to-many courses to requirement fulfilled
    allowed_courses = ndb.KeyProperty(Course, repeated=True)
#----------------End Program Sheet Models----------------#

#------------------Begin Student Models------------------#
class Candidate_Course(ndb.Model): pass

class Student_Program_Sheet(ndb.Model):
    program_sheet = ndb.KeyProperty(Program_Sheet, repeated=True)
    allow_double_count = ndb.BooleanProperty()
    cand_courses = ndb.KeyProperty(Candidate_Course, repeated=True)

class Student_Plan(ndb.Model):
    program_sheets = ndb.KeyProperty(Student_Program_Sheet, repeated=True)

class Student(ndb.Model):
    student_id = ndb.IntegerProperty(required=True)
    student_name = ndb.StringProperty()
    student_course_list = ndb.KeyProperty(Candidate_Course, repeated=True)
    academic_plans = ndb.KeyProperty(Student_Plan, repeated=True) 

class Candidate_Course(ndb.Model):
    course = ndb.KeyProperty(Course, required=True)
    student = ndb.KeyProperty(Student, required=True)
    student_program_sheet = ndb.KeyProperty(Student_Program_Sheet)
    # (optional) requirement that course is being applied to
    req_course = ndb.KeyProperty(Req_Course)
    term = ndb.StringProperty()
    year = ndb.IntegerProperty()
    grade = ndb.FloatProperty()
    units = ndb.IntegerProperty()
    allow_petition = ndb.StringProperty()
#-------------------End Student Models--------------------#
