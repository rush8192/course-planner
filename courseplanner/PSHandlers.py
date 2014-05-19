import webapp2
from ops import *

"""
Class exclusively for Program Sheet Handlers to clean up code
"""

def __str_to_int(str):
    if str == '':
        return 0
    else:
        return int(str)

def __str_to_float(str):
    if str == '':
        return 0
    else:
        return float(str)

class ProgramSheetHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(get_program_sheet(ps_name = self.request.get('ps_name')))
    def post(self):
        self.response.write(add_program_sheet(ps_name = self.request.get('ps_name')))
    def patch(self):
        ps_key = self.request.get('ps_key')
        new_ps_name = self.request.get('ps_name')
        self.response.write(edit_program_sheet(ps_key, new_ps_name))
    def delete(self):
        ps_key = self.request.get('ps_key')
        self.response.write(remove_program_sheet(ps_key))

class ReqBoxHandler(webapp2.RequestHandler):
    def post(self):
        ps_key = self.request.get('ps_key')
        req_box_name = self.request.get('req_box_name')
        min_units = __str_to_int(self.request.get('min_units'))
        min_num_courses = __str_to_int(self.request.get('min_num_courses'))
        conditional_ops = self.request.get('conditional_ops')
        if conditional_ops == '':
          conditional_ops = None
        self.response.write(add_req_box_to_ps(ps_key, req_box_name, \
                                              min_units, min_num_courses, \
                                              conditional_ops))
    def patch(self):
        rb_key = self.request.get('rb_key')
        req_box_name = self.request.get('req_box_name')
        if req_box_name == '':
          req_box_name = None

        min_units = self.request.get('min_units')
        if min_units == '':
            min_units = None
        else:
            min_units = __str_to_int(min_units)

        min_num_courses = self.request.get('min_num_courses')
        if min_num_courses == '':
            min_num_courses = None
        else:
            __str_to_int(min_num_courses)
        conditional_ops = self.request.get('conditional_ops')
        if conditional_ops == '':
          conditional_ops = None
        self.response.write(edit_req_box_in_ps(rb_key, req_box_name, \
                                              min_units, min_num_courses, \
                                              conditional_ops))
    def delete(self):
        rb_key = self.request.get('rb_key')
        self.response.write(remove_req_box_from_ps(rb_key))

class ReqCourseHandler(webapp2.RequestHandler):
    def post(self):
        rb_key = self.request.get('rb_key')
        req_course_name = self.request.get('req_course_name')
        min_units = __str_to_int(self.request.get('min_units'))
        min_grade = __str_to_float(self.request.get('min_grade'))
        allowed_courses = self.request.get('allowed_courses_ops')
        self.response.write(add_req_course_to_rb(rb_key, req_course_name, \
                                                 min_units, min_grade, \
                                                 allowed_courses))
    def patch(self):
        rc_key = self.request.get('rc_key')
        req_course_name = self.request.get('req_course_name')
        if req_course_name == '':
          req_course_name = None

        min_units = self.request.get('min_units')
        if min_units == '':
            min_units = None
        else:
            min_units = __str_to_int(min_units)

        min_grade = self.request.get('min_grade')
        if min_grade == '':
            min_grade = None
        else:
            __str_to_float(min_grade)
        allowed_courses = self.request.get('allowed_courses')
        if allowed_courses == '':
          allowed_courses = None
        self.response.write(edit_req_course_in_rb(rc_key, req_course_info, \
                                                  min_units, min_grade, \
                                                  allowed_courses))
    def delete(self):
        rc_key = self.request.get('rc_key')
        self.response.write(remove_req_course_from_rb(rc_key))
