import os
import json

courses_dict = json.loads(open('courses_json', 'r').read())
old_req_dict = {'GER:DB-Hum':[], 'GER:DB-Math':[], 'GER:DB-SocSci':[], 'GER:DB-EngrAppSci':[], \
           'GER:DB-NatSci':[], 'GER:EC-EthicReas':[], 'GER:EC-GlobalCom':[], 'GER:EC-AmerCul':[], \
           'GER:EC-Gender':[], 'GER:IHUM-1':[], 'GER:IHUM-2':[], 'GER:IHUM-3':[], 'Language':[], 'Writing1':[], \
           'Writing2':[], 'WritingSLE':[]}

new_req_dict = {'WAY-A-II':[], 'WAY-AQR':[], 'WAY-CE':[], 'WAY-ED':[], 'WAY-ER':[], \
           'WAY-FR':[], 'WAY-SI':[], 'WAY-SMA':[], 'THINK':[]}


def populate_req_dicts():
    uncounted_reqs = 0
    for course_key in courses_dict:
        course = courses_dict[course_key]
        for offering in course['offering']:
            for req in offering['reqs']:
                req = str(req)
                req = req.strip()
                req = req.replace(' ', '')
                if req in old_req_dict:
                    old_req_dict[req].append(course['course_num'])  
                elif req in new_req_dict:
                    new_req_dict[req].append(course['course_num'])  
                else:
                    uncounted_reqs += 1
    print 'Uncounted Reqs: '+ str(uncounted_reqs)
    for key in old_req_dict:
        print key + ': ' + str(len(old_req_dict[key]))
    for key in new_req_dict:
        print key + ': ' + str(len(new_req_dict[key]))

def create_old_req_ihum_pwr_json():
    json_dict = {}
    json_dict['req_name'] = 'Graduation Requirements (Class of 2015 and Before)'
    json_dict['allow_double_count'] = 'y'
    json_dict['conditional_ops'] = ''

    req_boxes_json_array = []
    req_boxes = ['DB', 'EC', 'IHUM', 'Language', 'Writing']
    for req_box_name in req_boxes:
        req_box_dict = {}
        req_box_dict['req_box_name'] = req_box_name
        req_box_dict['min_total_units'] = 0
        if 'DB' in req_box_name:
            req_box_dict['min_num_courses'] = 5
        if 'EC' in req_box_name:
            req_box_dict['min_num_courses'] = 2
        if 'IHUM' in req_box_name:
            req_box_dict['min_num_courses'] = 3
        if 'Language' in req_box_name:
            req_box_dict['min_num_courses'] = 1
        if 'Writing' in req_box_name:
            req_box_dict['min_num_courses'] = 2
        req_box_dict['req_box_courses'] = []
        req_boxes_json_array.append(req_box_dict)

    for key in old_req_dict:
        if 'DB' in key:
            req_courses_array = req_boxes_json_array[0]['req_box_courses']
        if 'EC' in key:
            req_courses_array = req_boxes_json_array[1]['req_box_courses']
        if 'IHUM' in key:
            req_courses_array = req_boxes_json_array[2]['req_box_courses']
        if 'Language' in key:
            req_courses_array = req_boxes_json_array[3]['req_box_courses']
        if 'Writing' in key and 'SLE' not in key:
            req_courses_array = req_boxes_json_array[4]['req_box_courses']
        req_courses_dict = {}
        req_courses_dict['req_course_info'] = key
        req_courses_dict['min_req_units'] = 0
        req_courses_dict['min_req_grade'] = 1.7
        req_courses_dict['allowed_course_list'] = old_req_dict[key]
        req_courses_array.append(req_courses_dict)

    json_dict['ps_req_boxes'] = req_boxes_json_array

    f = open('old_req_json', 'w')
    json_str = json.dumps(json_dict, indent=2, sort_keys=True)
    f.write(json_str)
    f.close()

if __name__ == '__main__':
    populate_req_dicts()
    create_old_req_ihum_pwr_json()