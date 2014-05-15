#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import add_courses, add_majors, ops

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to CoursePlanner!')
        # Add courses and majors to datastore on start up
        #add_courses.main()
        #add_majors.main()
        
        # test datastore features
        ops.create_student('Ryan', 0)
        #ops.get_course_json('CS 106A')
    
class TranscriptHandler(webapp2.RequestHandler):
    def post(self):
        import parser
        print "calling parser..."        
        parser.getTransContent(self.request.body_file.file, self.response)
        
    def get(self):
        self.response.write('only accepts POST requests')
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trans/upload', TranscriptHandler)
], debug=True)
