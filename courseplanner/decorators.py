from google.appengine.api import users
import ops
import models

def createStudent(f):
    def new_f(*args, **kwargs):
        user = users.get_current_user()
        if not ops.__student_exists(user.user_id()):
            s = models.Student(student_id = user.user_id())

            GER_SHEET_NAME = "GERs"
            gerSheet = models.Program_Sheet.query(models.Program_Sheet.ps_name == GER_SHEET_NAME).get()
            studentGerSheet = models.Student_Program_Sheet(program_sheet=gerSheet.key,
                        cand_courses=[], allow_double_count=True)
            studentGerSheet.put()
            splan = models.Student_Plan(student_plan_name = "DefaultPlan", student_course_list=[], program_sheets=[ studentGerSheet.key ])

            splan = models.Student_Plan(student_plan_name = "DefaultPlan", student_course_list=[], program_sheets=[])
            splan.put()
            s.academic_plans.append(splan.key)
            s.put()
        f(*args, **kwargs)
    return new_f
