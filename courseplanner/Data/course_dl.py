import urllib2
import urllib
import course_parse
import os
import time

_HTML_DIR = 'course_html/'

# Opens and checks if we are out of results yet.
def open_url(url):
  request = urllib2.Request(url)
  request.add_header('User-agent', 'Mozilla 5.10')
  html_str = urllib2.urlopen(request, timeout=5).read()
  url_valid = course_parse.check_html_validity(html_str)
  return (url_valid, html_str)

# If the file doesn't exist, it will open and download all files
def course_dl(year):
  template_url = 'http://explorecourses.stanford.edu/search?' \
                 'page={}&q=%26&filter-coursestatus-Active=on&' \
                 'view=catalog&collapse=&academicYear=' \
                 + str(year) + str(year + 1)
  page_index = 0
  url_valid = True
  while (url_valid):
    print('Downloading page: ' + str(page_index) + ' in year: ' + str(year))
    file_path = _HTML_DIR + ('%d-%d_%d.html' % (year, year+1, page_index))
    if (os.path.exists(file_path) is False):
      url = template_url.format(page_index)
      (url_valid, html_str) = open_url(url)
      f = open(_HTML_DIR + ('%d-%d_%d.html' % (year, year + 1, page_index)), 'w')
      f.write(html_str)
      f.close()
    page_index += 1
    time.sleep(0.5)
