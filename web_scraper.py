import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class Scraping():
    def __init__(self):
        pass

    @staticmethod
    def scrape_url(url):
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        try:
            wait = WebDriverWait(driver, timeout=5)
            wait.until(EC.presence_of_element_located((By.ID, "course-list")))
        except:
            raise LookupError("The element with ID 'course-list' is not found.")
        
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        courses = []
        for course in soup.find_all('div', class_='col-md-6 mb-3'):
            course_name = course.find('h5', class_='course-card__name').text
            course_hour = course.find_all('span', {'class':'mr-2'})[0].text
            course_summary = course.select('div.course-card__summary p')[0].text
            course_total_module = course.find_all('div', class_= 'course-card__info-item')[0].find_all('span')[0].contents[0]
            course_level = course.find('span', attrs={'class': None}).text
            
            try:
                course_rating = course.find_all('span', {'class':'mr-2'})[1].text
            except IndexError:
                course_rating = ''

            try:
                course_total_students = course.find_all('span', {'class':'mr-3'})[1].get_text()
            except:
                course_total_students = ''

            courses.append(
                {
                    'Course Name': course_name,
                    'Learning Hour': course_hour,
                    'Rating': course_rating,
                    'Level': course_level,
                    'Summary': course_summary,
                    'Total Modules': course_total_module,
                    'Total Students': course_total_students
                }
            )
        driver.quit()
        return courses

if __name__ == "__main__":
    url = 'https://www.dicoding.com/academies/list'
 
    data = Scraping.scrape_url(url)
 
    with open('dicoding_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
