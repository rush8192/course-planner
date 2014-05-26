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
        ps_name = self.request.get('ps_name')
        req_box_array = json.loads(self.request.get('req_boxes'))
        self.response.write(add_program_sheet(ps_name, req_box_array))
    def put(self):
        ps_key = self.request.get('ps_key')
        new_ps_name = self.request.get('ps_name')
        self.response.write(edit_program_sheet(ps_key, new_ps_name))
    def delete(self):
        ps_key = self.request.get('ps_key')
        self.response.write(remove_program_sheet(ps_key))

class ReqBoxHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(get_program_sheet(rb_key = self.request.get('rb_key')))
    # Note POST is always called with ps_key
    def post(self):
        ps_key = self.request.get('ps_key')
        req_box_dict = json.loads(self.request.get('req_box'))
        self.response.write(add_req_box_to_ps(ps_entity=None, ps_key=ps_key, \
                                              req_box_dict=req_box_dict))
    def put(self):
        rb_key = self.request.get('rb_key')
        req_box_dict = self.request.get('req_box_dict')
        for key in req_box_dict:
            if req_box_dict[key] == '':
                req_box_dict[key] = None
        self.response.write(edit_req_box_in_ps(rb_entity=None, rb_key=rb_key, \
                                               req_box_dict=req_box_dict))
    def delete(self):
        rb_key = self.request.get('rb_key')
        self.response.write(remove_req_box_from_ps(rb_key))

class ReqCourseHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(get_program_sheet(rc_key = self.request.get('rc_key')))
    # Note POST is always called with rb_key
    def post(self):
        rb_key = self.request.get('rb_key')
        req_course_dict = json.loads(self.request.get('req_course'))
        self.response.write(add_req_course_to_rb(rb_entity=None, rb_key=rb_key, \
                                                 req_course_dict=req_course_dict))
    def put(self):
        rc_key = self.request.get('rc_key')
        req_course_dict = json.loads(self.request.get('req_course_dict'))
        for key in req_course_dict:
            if req_course_dict[key] == '':
                req_course_dict[key] = None
        self.response.write(edit_req_course_in_rb(rc_entity=None, rc_key=rc_key, \
                                                  req_course_dict=req_course_dict))
    def delete(self):
        rc_key = self.request.get('rc_key')
        self.response.write(remove_req_course_from_rb(rc_key))
