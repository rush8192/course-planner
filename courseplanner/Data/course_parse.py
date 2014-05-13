from bs4 import BeautifulSoup
import json
import os
import re

def check_html_validity(html_str):
  soup = BeautifulSoup(html_str)
  courses = soup.findAll('div', {'class' :'courseInfo'})
  if courses is None or len(courses) == 0:
    return False
  return True

# Soup and parse course number
def parsed_course_number(course):
  course_num = course.find('span', {'class': 'courseNumber'}).renderContents()
  return course_num.replace(':', '')

# Soup and parse course title
def parsed_course_title(course):
  course_title = course.find('span', {'class': 'courseTitle'}).renderContents()
  return course_title

# Soup and parse course description
# Verify that hyperlinks were properly parsed (Rush)
def parsed_course_desc(course):
  course_desc = course.find('div', {'class':'courseDescription'}).renderContents()
  course_desc = re.sub('<[^<]+?>', '', course_desc)
  return course_desc

# Soup and parse course attributes
# terms: course_terms (array of str)
# units: course_units (array of int)
# grading: course_grading (str)
# instructors: course_instructor (array of str)
# reqs: course_reqs (array of str)
def parsed_course_attr(course):
  course_attr_dict = {}
  # Initialization
  course_attr_dict['terms'] = []
  course_attr_dict['units'] = []
  course_attr_dict['grading'] = ''
  course_attr_dict['instructors'] = []
  course_attr_dict['reqs'] = []

  course_attrs = course.findAll('div', {'class':'courseAttributes'})
  course_attr_blob = ''
  # Begin Parse
  for course_attr in course_attrs:
    course_attr_blob += course_attr.renderContents() + "|"
  course_attr_strings = course_attr_blob.split('|')
  for attr_str in course_attr_strings:
    if ('Terms: ' in attr_str):
      terms = attr_str.replace('Terms: ', '').strip()
      terms = terms.split(', ')
      course_attr_dict['terms'] = terms
    elif ('Units: ' in attr_str):
      units = attr_str.replace('Units: ', '').strip()
      units = units.split('-')
      for i in range(len(units)):
        units[i] = int(units[i].strip())   
      if (len(units) > 1):
        temp_units = []
        unit = units[0]
        while (unit != units[-1]):
          temp_units.append(unit)
          unit += 1
        units = temp_units
      course_attr_dict['units'] = units
    elif ('Grading: ' in attr_str):
      grading = attr_str.replace('Grading: ', '').strip()
      course_attr_dict['grading'] = grading
    # Get rid of document.write issues
    elif ('Instructors:' in attr_str):
      instructors = attr_str.replace('Instructors:', '').strip()
      instructors = instructors.split(';')
      for i in range(len(instructors)):
        instructors[i] = re.sub('<[^<]+?>', '', instructors[i])
        instructors[i] = instructors[i].strip()
        instructors[i] = instructors[i].replace('\n', '')
        instructors[i] = instructors[i].replace('\t', '')
        instructors[i] = instructors[i].replace('\r', '')
        course_attr_dict['instructors'] = instructors
    elif ('UG Reqs: ' in attr_str):
      reqs = attr_str.replace('UG Reqs: ', '').strip()
      reqs = reqs.split(', ')
      course_attr_dict['reqs'] = reqs
  return course_attr_dict

# For repeated course offerings through many years
def create_course_offering_dict(year, terms, units, grading, instructors, reqs, title):
  offering_dict = {}
  offering_dict['course_title'] = title
  offering_dict['year'] = year
  offering_dict['term'] = terms
  offering_dict['units'] = units
  offering_dict['grading'] = grading
  offering_dict['instructors'] = instructors
  offering_dict['reqs'] = reqs
  return offering_dict

# Basic Entry in JSON Array
def create_course_dict(num, desc, offering_dict):
  course_dict = {}
  course_dict['course_num'] = num
  course_dict['course_desc'] = desc
  course_dict['offering'] = [offering_dict]
  course_dict['rankings_sum'] = 0
  course_dict['rankings_tally'] = 0
  course_dict['hpw_sum'] = 0
  course_dict['hpw_tally'] = 0
  return course_dict

def create_json_array(html_dir):
  courses_json_dict = {}
  for subdir, dirs, files in os.walk(html_dir):
    count = 0
    for html_file in files:
      print count
      count += 1
      if '.html' in html_file:
        f = open(html_dir + html_file, 'r')
        soup = BeautifulSoup(f.read())
        f.close()
        courses = soup.findAll('div', {'class' : 'courseInfo'})
        for course in courses:
          course_year = html_file[0:9] # (str)
          course_num = parsed_course_number(course) # str
          course_title = parsed_course_title(course) # str
          course_desc = parsed_course_desc(course) # str
          course_attr = parsed_course_attr(course)
          course_terms = course_attr['terms'] # array(str)
          # Lower and upper bound on units
          course_units = course_attr['units'] # array(int)
          course_grading = course_attr['grading'] # str
          course_instructors = course_attr['instructors'] # array(str)
          course_reqs = course_attr['reqs'] # array(str)

          course_offering_dict = create_course_offering_dict(course_year, \
                                 course_terms, course_units, course_grading, \
                                 course_instructors, course_reqs, course_title)
          if course_num in courses_json_dict:
            offering_array = courses_json_dict[course_num]['offering']
            offering_array.append(course_offering_dict)
          else:
            courses_json_dict[course_num] = create_course_dict(course_num, \
                                            course_desc, \
                                            course_offering_dict)
  json_str = json.dumps(courses_json_dict)
  with open('courses_json', 'w') as outfile:
    outfile.write(json_str)

def parse_html_to_json(html_dir, filename):
  json_object_array = create_json_array(html_dir)
  f = open(filename, 'w')
  f.write(json.dumps(json_object_array))
  f.close()
