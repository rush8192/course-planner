from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class Course(DictModel):
    course_num = db.StringProperty()
    course_desc = db.TextProperty()
    
class Offering(DictModel):
    course_title = db.StringProperty(required=True)
    term = db.ListProperty(item_type=str)
    grading = db.StringProperty
    instructors = db.ListProperty(item_type=str)
    reqs = db.ListProperty(item_type=str)
    year = db.StringProperty
    units = db.ListProperty(item_type=int)
    course = db.ReferenceProperty(Course, collection_name='offerings')
        
class Major(DictModel):
    major_id = db.IntegerProperty(required=True)
    major_name = db.StringProperty(required=True)
    track_name = db.StringProperty(required=True)

class Req_Box(DictModel):
    major = db.ReferenceProperty(Major, collection_name='req_boxes')
    req_id = db.IntegerProperty(required=True)
    req_box_name = db.StringProperty(required=True)
    min_total_units = db.IntegerProperty()
    min_num_courses = db.IntegerProperty() 
    # TODO - structure conditional ops
    conditional_ops = db.StringProperty()
    # List of Req_Course: (0/1):many relationship
    req_courses = db.ListProperty(db.Key)
    
    
class Grad_Req(DictModel):
    req_name = db.StringProperty()
    # List of Req_Course: (0/1):many relationship
    req_courses = db.ListProperty(db.Key)
    candidate_course = db.ReferenceProperty(Course)
    candidate_course_units = db.IntegerProperty()    
    
# Required Course belonging either to a Req_Box (major requirement)
# or Grad_Req (GER)    
class Req_Course(DictModel):
    course_req_id = db.IntegerProperty()
    display_title = db.StringProperty()
    course_req_type = db.StringProperty()
    min_grade = db.FloatProperty()
    # TODO - structure force error
    force_error = db.StringProperty()
    # many-to-many courses to requirement fulfilled
    allowed_courses = db.ListProperty(db.Key)

    
class Student(DictModel):
    student_id = db.IntegerProperty(required=True)
    name = db.StringProperty()
    major = db.ReferenceProperty(Major)

class Candidate_Course(DictModel):
    course = db.ReferenceProperty(Course)
    req_course = db.ReferenceProperty(Req_Course)
    grade = db.FloatProperty()
    units = db.IntegerProperty()
    # each student has many candidate courses
    student = db.ReferenceProperty(Student, collection_name='courses')

