from google.appengine.ext import ndb

class DictModel(ndb.Model):
    # Redefines to_dict() include serialized key of self, as well as keys
    # for all KeyProperties
    def safe_convert_key_list(self, value):
        key_strs = []
        for elem in value:
            if isinstance(elem, ndb.Key):
                elem = elem.urlsafe()
            key_strs.append(elem)
        return key_strs

    def to_dict(self):
        output = ndb.Model.to_dict(self)
        output['key'] = self.key.urlsafe()
        for key, prop in output.iteritems():
            value = getattr(self, key)
            if isinstance(value, ndb.Key):
                output[key] = value.urlsafe()
            elif isinstance(value, list):
                output[key] = self.safe_convert_key_list(value)
        return output

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
    req_course_name = ndb.StringProperty()
    req_course_info = ndb.TextProperty()
    min_grade = ndb.FloatProperty()
    min_units = ndb.IntegerProperty()
    allowed_courses = ndb.KeyProperty(Course, repeated=True)
#----------------End Program Sheet Models----------------#

#------------------Begin Student Models------------------#
class Student_Program_Sheet(DictModel):
    program_sheet = ndb.KeyProperty(Program_Sheet)
    allow_double_count = ndb.BooleanProperty()
    cand_courses = ndb.KeyProperty(Candidate_Course, repeated=True)

class Student_Plan(DictModel):
    student_plan_name = ndb.StringProperty()
    student_course_list = ndb.KeyProperty(Candidate_Course, repeated=True)
    program_sheets = ndb.KeyProperty(Student_Program_Sheet, repeated=True)

class Student(DictModel):
    # Student's google user id
    student_id = ndb.StringProperty(required=True)
    academic_plans = ndb.KeyProperty(Student_Plan, repeated=True)

class Req_Fullfillment(DictModel):
    req_course = ndb.KeyProperty(Req_Course)
    valid = ndb.BooleanProperty()
    error_message = ndb.StringProperty()
    program_sheet = ndb.KeyProperty(Student_Program_Sheet)

class Candidate_Course(DictModel):
    course = ndb.KeyProperty(Course, required=True)
    student = ndb.KeyProperty(Student, required=True)
    student_plan = ndb.KeyProperty(Student_Plan)
    # (optional) requirement that course is being applied to
    reqs_fulfilled = ndb.KeyProperty(Req_Fullfillment, repeated=True)
    term = ndb.StringProperty()
    year = ndb.IntegerProperty()
    grade = ndb.FloatProperty()
    units = ndb.IntegerProperty()
#-------------------End Student Models--------------------#


"""
Object for candidate course:

    Candidate_course.to_dict()
    course.course_num

Object we return for front-end student program sheet:
{
    "ps_name" : ps_name,
    "sps_key" : sps_key,
    "req_boxes" :
        [
            {"req_box_name":req_box_name,
             "req_box_key": req_box_key,
             "min_total_units":min_total_units,
             "min_num_courses":min_num_courses,
             "req_courses": 
                 [
                      {
                       "req_course_name":req_course_name,
                       "req_course_info":req_course_info,
                       "req_course_key":req_course_key,
                       "cand_course_name": cand_course_name,
                       "cand_course_key":cand_course_key,
                       "course_key":course_key,
                       "cand_course_units":cand_course_units,
                       "cand_course_gpa":cand_course_gpa,
                      }
                 ]
            }
        ]
}


"""