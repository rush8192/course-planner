import course_dl as CD
import course_parse as CP

if __name__ == '__main__':
  #CD.course_dl(2010)
  #CD.course_dl(2011)
  #CD.course_dl(2012)
  #CD.course_dl(2013)
  CP.parse_html_to_json('course_html/', 'courses_json')
