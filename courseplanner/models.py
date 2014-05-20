from google.appengine.ext import ndb

class DictModel(ndb.Model):
    # TODO redefine to_dict() so that it encodes keys in serializable fashion!
    # to_dict() in ndb.Model is somewhat useless since it doesn't guarantee json
    # serializability
    # or you know... lol it off
    pass

# stubs for all classes with cyclical references
class Offering(DictModel): pass
class Requirement(DictModel): pass
class Req_Box(DictModel): pass
class Req_Course(DictModel): pass
class Candidate_Course(DictModel): pass

#------------------Begin Course Models-------------------#
class Course(DictModel):
    course_num = ndb.StringProperty(required=True)
    course_title = ndb.StringProperty()
    course_desc = ndb.TextProperty()
    rankings_sum = ndb.IntegerProperty()
    rankings_tally = ndb.IntegerProperty()
    hpw_sum = ndb.IntegerProperty()
    hpw_tally = ndb.IntegerProperty()
    offerings = ndb.KeyProperty(Offering, repeated=True)

class Offering(DictModel):
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
class Program_Sheet(DictModel):
    ps_name = ndb.StringProperty()
    req_boxes = ndb.KeyProperty(Req_Box, repeated=True)

# Requirement box such as depth or DB:Hum
class Req_Box(DictModel):
    program_sheet = ndb.KeyProperty(Program_Sheet)
    req_box_name = ndb.StringProperty(required=True)
    min_total_units = ndb.IntegerProperty()
    min_num_courses = ndb.IntegerProperty()
    # TODO(kevin) - structure conditional ops
    conditional_ops = ndb.StringProperty()
    # List of fulfilling courses
    req_courses = ndb.KeyProperty(Req_Course, repeated=True)

# Required Course belonging to a Req_Box (major requirement or GER req)
class Req_Course(DictModel):
    req_box = ndb.KeyProperty(Req_Box)
    req_course_info = ndb.StringProperty()
    min_grade = ndb.FloatProperty()
    min_units = ndb.IntegerProperty()
    allowed_courses = ndb.KeyProperty(Course, repeated=True)
#----------------End Program Sheet Models----------------#

#------------------Begin Student Models------------------#
class Student_Program_Sheet(DictModel):
    program_sheet = ndb.KeyProperty(Program_Sheet, repeated=True)
    allow_double_count = ndb.BooleanProperty()
    cand_courses = ndb.KeyProperty(Candidate_Course, repeated=True)

class Student_Plan(DictModel):
    student_plan_name = nbd.StringProperty()
    student_course_list = ndb.KeyProperty(Candidate_Course, repeated=True)    
    program_sheets = ndb.KeyProperty(Student_Program_Sheet, repeated=True)

class Student(DictModel):
    # Student's google user id 
    student_id = ndb.StringProperty(required=True)
    student_name = ndb.StringProperty()
    academic_plans = ndb.KeyProperty(Student_Plan, repeated=True) 

class Candidate_Course(DictModel):
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
