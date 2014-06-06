from google.appengine.api import users
import ops
import models

def createStudent(f):
    def new_f(*args, **kwargs):
        user = users.get_current_user()
        if not ops.__student_exists(user.user_id()):
            s = models.Student(student_id = user.user_id())
            s.put()
        f(*args, **kwargs)
    return new_f