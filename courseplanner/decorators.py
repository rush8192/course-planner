from google.appengine.api import users
import ops
import models

def createStudent(f):
    def new_f(*args, **kwargs):
        user = users.get_current_user()
        if not ops.__student_exists(user.user_id()):
            s = models.Student(student_id = user.user_id())
            splan = models.Student_Plan(student_plan_name = "")
            splan.put()
            s.academic_plans.append(splan.key)
            s.put()
        f(*args, **kwargs)
    return new_f