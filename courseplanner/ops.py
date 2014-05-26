from google.appengine.ext import ndb
import json
import re
from models import *
from google.appengine.api import users

"""
This is where all for CRUD operations will live. Potential list:
    -create_student
    -add_candidate_course
    -remove_candidate_course
    -get_candidate_courses(student_id)
    -add_course_listing
    -remove_course_listing
    -get_master_course_list
    -get_course(by substring of course_num)
    -get_program_sheet(major_id, ps_name)
"""

#------------------------Begin Helper Methods------------------------#
# Helper to print error messages in consistent json format
def ERROR(message):
    return json.dumps({"errorMessage": message})

# Helper to cleanup course number
def __fix_course_num(course_num):
    course_num = course_num.upper()
    n_split = re.split('(\d+)', course_num, 1)
    if len(n_split) < 2:
        return ERROR('Course number must include digits')
    ret = n_split[0].replace(" ", "") + ' '
    for s in n_split[1:]:
        ret += s
    return ret

# Helper to serialize key
def __serialize_key(key):
    return key.id()

# Helper to deserialize key
def __deserialize_key(key_str, entity_kind):
    return Key.from_path(kind=entity_kind, id = key_str)

# Helper to return entity from key_str or None (depends on ndb behavior)
def __entity_from_key_str(key_st, entity_kind):
    key = __deserialize_key(key_str, entity_kind)
    return key.get()

# Checks existence of program sheet, true/false
def __program_sheet_exists(ps_name):
    sheets = Program_Sheet.query(Program_Sheet.ps_name == ps_name).fetch(1)
    if len(sheets) == 0:
        return False
    return True

# Converts Req_Course entity to dictionary, replaces allowed course keys
# with course names
def __get_req_course_dict(rc_key):
    rc_entity = __entity_from_key_str(rc_key)
    if rc_entity is None:
        return 'Cannot find Req_Course'
    rc_dict = rc_entity.to_dict()
    allowed_course_keys = list(rc_dict['allowed_courses'])
    rc_dict['allowed_courses'] = []
    for ac_key in allowed_course_keys:
        ac_entity = __entity_from_key_str(ac_key)
        if ac_entity is None:
            return 'Cannot find course from allowed course list'
        rc_dict['allowed_courses'].append(ac_entity.course_num)
    return rc_dict

# Converts Req_Box entity to dictionary with Req_Courses filled in
def __get_req_box_dict(rb_key):
    rb_entity = __entity_from_key_str(rb_key)
    if rb_entity is None:
        return 'Cannot find Req_Box'
    rb_dict = rb_entity.to_dict()
    req_course_keys = list(rb_dict['req_courses'])
    rb_dict['req_courses'] = []
    for rc_key in req_course_keys:
        req_course_dict = __get_req_course_dict(rc_key)
        if type(req_course_dict) != dict:
            return req_course_dict
        rb_dict['req_courses'].append(req_course_dict)
    return rb_dict

# Converts Program_Sheet to dictionary with Req_Boxes filled in
def __get_ps_dict(ps_name):
    ps = Program_Sheet.query(Program_Sheet.ps_name == ps_name).get()
    if ps == None:
        return 'Program Sheet ' + str(ps_name) + ' does not exist'
    ps_entity = ps[0]
    ps_dict = ps_entity.to_dict()
    req_box_keys = list(ps_dict['req_boxes'])
    ps_dict['req_boxes'] = []
    for rb_key in req_box_keys:
        req_box_dict = __get_req_box_dict(rb_key)
        if type(req_box_dict) != dict:
            return req_box_dict
        ps_dict['req_boxes'].append(req_box_dict)
    return ps_dict

# Fetches course entity
# Returns entity if found, or None
def __get_course_listing_entity(course_num):
    course_num = __fix_course_num(course_num)
    course = Course.query(Course.course_num == course_num).get()
    return course

# Fetches student entity
# Returns student entity(s) if found, or None
def __get_student_entities(student_id, student_name=None):
    student = None
    if student_name is None:
        student = Student.query(Student.student_id == student_id).fetch(1)
    else:
        student = Student.query(Student.student_name == student_name).fetch()
    if len(student) > 0:
        return student
    return None

# True, False if student_id taken
def __student_exists(student_id):
    student = Student.query(Student.student_id == student_id).fetch(1)
    return len(student) > 0

#------------------------End Helper Methods------------------------#

#------------------------Begin Student Methods------------------------#
def create_student():
    user = users.get_current_user()
    if __student_exists(student_id):
        return
    s = Student(student_id = user.user_id())
    # TODO: Add empty course plan (Rush)
    s.put()

def get_student():
    user = users.get_current_user()
    return "{'userID':" + user.user_id() + "}"

# Add course to candidate list for given student, course, grade, units, and req
# Return true if course fulfills the req, false otherwise. Assumes course_req_id
# is valid and for correct major
#
# Parameters:
#    req_course (optional): key for Req_Course the course fulfills. Can have candidate
#       courses without req_course (e.g. taken for interest, or major undecided)
#    force - flag to override errors validating the course.
def add_candidate_course(student_id, course_num, req_course, grade, units, force=False):
    if student_id is None or student_id == '':
        return ERROR('Must provide student_id')
    else:
        student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return ERROR('Student with id ' + str(student_id) + ' not found')
    course = __get_course_listing_entity(course_num)
    if not course:
        return ERROR('Course number ' + str(course_num) + ' not found')
    if units == '':
        units = None
    if req_course:
        req_course_key = __deserialize_key(req_course, Req_Course)
        if not req_course:
            return ERROR('Req_Course key ' + req_course + ' not found.')
        candidate_course = Candidate_Course(course=course.key, req_course=req_course_key,
                                        grade=grade, units=units, student=student.key)
    else:
        candidate_course = Candidate_Course(course=course.key,
                                        grade=grade, units=units, student=student.key)
    # Validate course, req_course pairing
    # TODO: merge with Rush's course validation(?)
    if force or not req_course or course.key in req_course.allowed_courses:
        candidate_course.put()
        return True
    else:
        return ERROR("Course does not fulfill given requirement.")

# Removes course from student's program sheet (in all places that it occurs). Optional
# parameter ps specifies Student_Program_Sheet by key. If not given, course taken off all
# sheets found
def remove_candidate_course(student_id, course_num, ps):
    student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return ERROR('Student with id ' + student_id + ' not found')
    course = __get_course_listing_entity(course_num)
    if not course:
        return ERROR('Course number ' + course_num + ' not found')
    if ps:
        ps_key = __deserialize_key(ps, Student_Program_Sheet)
        candidate_courses = Candidate_Course.query(Candidate_Course.student == student.key,
                                                   Candidate_Course.course == course.key,
                                                   Candidate_Course.student_program_sheet
                                                    == ps_key).fetch()
    else:
        candidate_courses = Candidate_Course.query(Candidate_Course.student == student.key,
                                                   Candidate_Course.course == course.key
                                                   ).fetch()
    for course in candidate_courses:
        course.key.delete()
    return True

# Return all candidate courses associated with student: for now, this is just a set
# of unique course_nums. (Reqs information will be obtained separately when fetching
# student's program sheet).
#
# Returns: json dump or error message
def get_candidate_courses(student_id):
    student = Student.query(Student.student_id == student_id).fetch(1)
    if len(student) > 0: student = student[0]
    else:
        return ERROR('Student with id ' + student_id + ' not found')
    courses = Candidate_Course.query(Candidate_Course.student == student.key).fetch()
    course_dict = dict()
    for course in courses:
        c = course.course.get()
        course_dict[c.course_num] = 1
    return json.dumps(course_dict.keys())

#------------------------End Student Methods------------------------#


#------------------------Begin Course Listing Methods------------------------#

# Add course listing: return error if course_num exists, True otherwise
def add_course_listing(course_num, course_desc, course_title):
    course_num = __fix_course_num(course_num)
    existing = Course.query(Course.course_num == course_num).fetch()
    if len(existing) > 0:
        return ERROR('Course with course number = ' + course_num + ' already exists!')
    course = Course(course_num=course_num, course_desc=course_desc,
                    course_title=course_title)
    course.put()
    return True

# Edit course listing: can change description or title. If either is None, left unaffected
# TODO: more advanced editing e.g. Offerings
def edit_course_listing(course_num, course_desc=None, course_title=None):
    course_num = __fix_course_num(course_num)
    courses = Course.query(Course.course_num == course_num).fetch(1)
    if len(courses) > 0:
        course = courses[0]
        if course_desc:
            course.course_desc = course_desc
        if course_title:
            course.course_title = course_title
        course.put()
        #return json.dumps(course.to_dict())
        return True
    else:
        return ERROR('Course_num ' + course_num + ' not found.')

# Remove course listing - return error if not found, True otherwise
def remove_course_listing(course_num):
    course_num = __fix_course_num(course_num)
    courses = Course.query(Course.course_num == course_num).fetch(1)
    if len(courses) > 0:
        course = courses[0]
        course.key.delete()
        return True
    else:
        return ERROR('Course_num ' + course_num + ' not found.')

# Return json dump of course information by course_num, or error
# if not found.
def get_course_listing(course_num):
    course_listing_entity = __get_course_listing_entity(course_num)
    if (course_listing_entity is None):
        return ERROR('Course_num ' + course_num + ' not found.')
    return json.dumps(course_listing_entity.to_dict())

# Return json list of all course_nums in datastore
def get_master_course_list():
    courses = Course.query().fetch(projection=[Course.course_num])
    course_dict = dict()
    for course in courses:
        course_dict[course.course_num] = 1
    return json.dumps(course_dict.keys())

#------------------------End Course Listing Methods------------------------#


#------------------------Begin Program Sheet Ops------------------------#
"""
Adds a new Program Sheet

Returns:
    True on success
    Error message on failure
"""
def add_program_sheet(ps_name, req_box_array):
    if (__program_sheet_exists(ps_name)):
        return ERROR('Program sheet already exists for ' + str(ps_name) + '.')
    ps_entity = Program_Sheet(ps_name=ps_name)
    for req_box in req_box_array:
        result = add_req_box_to_ps(ps_entity, req_box)
        # Exists Error, Abort
        if (result != True):
            return result
    ps_entity.put()
    return result

"""
Fetches Program Sheet based on name (exact match)

Returns:
    Json dump on success
    Error message on failure
"""
def get_program_sheet(ps_name):
    ps_dict = __get_ps_dict(ps_name)
    if type(ps_dict) != dict:
        return ERROR(ps_dict)
    return json.dumps(ps_dict)

"""
Edits program sheet name given key to program sheet

Returns:
    True on success
    Error message on failure
"""
def edit_program_sheet(ps_key, new_ps_name):
    ps_entity = __entity_from_key_str(ps_key, 'Program_Sheet')
    if ps_entity is None:
        return ERROR('Program sheet not found.')
    ps_entity.ps_name = new_ps_name
    ps_entity.put()
    return True

"""
Deletes program sheet name given key to program sheet
"""
def remove_program_sheet(ps_key):
    ps_entity = __entity_from_key_str(ps_key, 'Program_Sheet')
    if ps_entity is None:
        return
    req_boxes_copy = list(ps_entity.req_boxes)
    for req_box_key in req_boxes_copy:
        remove_req_box_from_ps(req_box_key)
    ps_entity.key.delete()

"""
Creates a Req_Box to link to a Program_Sheet

Requirements:
    min_units must be handled on front end to be an integer str
    min_num_courses must be handled on front end to be an integer str

Returns:
    True on success
    Error message on failure
"""
def add_req_box_to_ps(ps_entity, req_box_dict, ps_key=None):
    if ps_key != None:
        ps_entity = __entity_from_key_str(ps_key, 'Program_Sheet')
        if ps_entity is None: # None if doesn't exist?
            return ERROR('Program sheet does not currently exist.')
    req_box_name = req_box_dict['req_box_name']
    min_units = req_box_dict['min_total_units']
    min_num_courses = req_box_dict['min_num_courses']
    conditional_ops = req_box_dict['conditional_ops']
    rb_entity = Req_Box(program_sheet=ps_entity, req_box_name=req_box_name, \
                      min_total_units=min_units, min_num_courses=min_num_courses, \
                      conditional_ops=conditional_ops)

    req_course_array = req_box_dict['req_courses']
    for req_course in req_course_array:
        result = add_req_course_to_rb(rb_entity, req_course)
        # Exists Error, Abort
        if (result != True):
            return result
    rb_entity.put()
    ps_entity.req_boxes.append(req_box_entity.key())
    ps_entity.put()
    return True

"""
Fetches Required Box based on key (exact match)

Returns:
    Json dump on success
    Error message on failure
"""
def get_req_box(rb_key):
    rb_dict = __get_rb_dict(rb_key)
    if rb_dict is None:
        return ERROR('Required Box not found.')
    return json.dumps(rb_dict)

"""
Edits a Req_Box in a Program_Sheet

Requirements:
    min_units must be handled on front end to be an integer str
    min_num_courses must be handled on front end to be an integer str

Returns:
    True on success
    Error message on failure
"""
def edit_req_box_in_ps(rb_entity, req_box_dict, rb_key=None):
    rb_entity = __entity_from_key_str(rb_key, 'Req_Box')
    if rb_entity is None: # None if doesn't exist?
        return ERROR('Req box does not currently exist.')
    req_box_name = req_box_dict['req_box_dict']
    min_units = req_box_dict['min_units']
    min_num_courses = req_box_dict['min_num_courses']
    conditional_ops = req_box_dict['conditional_ops']
    if req_box_name != None:
        rb_entity.req_box_name = req_box_name
    if min_units != None:
        rb_entity.min_total_units = int(min_units)
    if min_num_courses != None:
        rb_entity.min_num_courses = int(min_num_courses)
    if conditional_ops != None:
        rb_entity.conditional_ops = conditional_ops
    req_box_entity.put()
    return True

"""
Removes a Req_Box reference from a Program_Sheet
and deletes the Req_Box itself
"""
def remove_req_box_from_ps(rb_key):
    rb_entity = __entity_from_key_str(rb_key, 'Req_Box')
    if rb_entity != None: # None if doesn't exist?
        ps_entity = rb_entity.program_sheet.get()
        if ps_entity != None:
            remove_index = -1
            for i in range(len(ps_entity.req_boxes)):
                if ps_entity.req_boxes[i].id() == rb_entity.id():
                    del ps_entity.req_boxes[i]
                    break
            ps_entity.put()
        req_courses_copy = list(rb_entity.req_courses)
        for req_course_key in req_courses_copy:
            remove_req_course_from_rb(req_course_key)
        rb_entity.key.delete()

"""
Adds a Req_Course to link to a Req_Box

Requirements:
    min_units must be handled on front end to be an int str
    min_grade must be handled on front end to be a float str

Returns:
    True on success
    Error message on failure
"""
def add_req_course_to_rb(rb_entity, req_course_dict, rb_key = None):
    if rb_key != None:
        rb_entity = __entity_from_key_str(rb_key, 'Req_Box')
        if rb_entity is None: # None if doesn't exist?
            return ERROR('Required box does not currently exist.')
    req_course_info = req_course_dict['req_course_info']
    min_units = req_course_dict['min_units']
    min_grade = req_course_dict['min_grade']
    allowed_courses = req_course_dict['allowed_courses']

    rc_entity = Req_Course(req_box=rb_entity, req_course_info=req_course_info, \
                           min_units = min_units, min_grade=min_grade)
    for course_name in allowed_courses:
        course_listing = __get_course_listing_entity(course_name)
        if course_listing == None:
            return ERROR('Course ' + course_name + ' does not exist')
        rc_entity.allowed_courses.append(course_listing.key())
    rc_entity.put()
    rb_entity.req_courses.append(rc_entity.key())
    rb_entity.put()
    return True

"""
Fetches Required Course based on key (exact match)

Returns:
    Json dump on success
    Error message on failure
"""
def get_req_course(rc_key):
    rc_dict = __get_rc_dict(rc_key)
    if rc_dict is None:
        return ERROR('Required course not found.')
    return json.dumps(rc_dict)

"""
Adds a Req_Course to link to a Req_Box

Requirements:
    min_grade must be handled on front end to be a float str

Returns:
    True on success
    Error message on failure
"""
def edit_req_course_in_rb(rc_entity, req_course_dict, rc_key = None):
    if (rc_key is not None):
        rc_entity = __entity_from_key_str(rc_key, 'Req_Course')
        if rc_entity is None: # None if doesn't exist?
            return ERROR('Required course does not currently exist.')
    req_course_info = req_course_dict['req_course_dict']
    min_units = req_course_dict['min_units']
    min_grade = req_course_dict['min_grade']
    allowed_courses = req_course_dict['allowed_courses']
    if req_course_info:
        rc_entity.req_course_info = req_course_info
    if min_grade:
        rc_entity.min_grade = float(min_grade)
    if min_units:
        rc_entity.min_units = int(min_units)
    if allowed_courses:
        del rc_entity.allowed_courses[:]
        for course_name in allowed_courses:
            course_listing = __get_course_listing_entity(course_name)
            if course_listing == None:
                return ERROR('Course ' + course_name + ' does not exist')
            rc_entity.allowed_courses.append(course_listing.key())
    req_course_entity.put()
    return True

"""
Removes Req_Course link from a Req_Box and removes Req_Course itself
"""
def remove_req_course_from_rb(rc_key):
    rc_entity = __entity_from_key_str(rc_key, 'Req_Course')
    if rc_entity != None: # None if doesn't exist?
        rb_entity = rc_entity.req_box.get()
        if rb_entity != None:
            remove_index = -1
            for i in range(len(rb_entity.req_courses)):
                if rb_entity.req_courses[i].id() == rc_entity.id():
                    del rb_entity.req_courses[i]
                    break
            rb_entity.put()
        rc_entity.key.delete()
#-------------------------End Program Sheet Ops-------------------------#
