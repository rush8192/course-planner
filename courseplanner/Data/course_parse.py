from bs4 import BeautifulSoup

def check_html_validity(html_str):
  soup = BeautifulSoup(html_str)
  courses = soup.findAll('div', {'class' :'courseInfo'})
  if courses is None or len(courses) == 0:
    return False
  return True

