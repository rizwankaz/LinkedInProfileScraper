"""
LinkedIn Job Scraper, Rizwan Kazi
Version 1 - April 2023
This script relies upon the packages selenium (version 4.2.0) and beautifulsoup(version 1.1.0).
This script will not work with any other versions of selenium or BS.
"""
#Call necessary packages.
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

#At the time being, .txt seemed to be the best format for results. So, create your .txt file.
f = open("output.txt","w")

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
path = "wherever your chromedriver is"
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get("https://www.linkedin.com/login")

#Log in with your email and password for LinkedIn.
username = "yourusername"
password = "yourpassword"
driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_css_selector('.btn__primary--large').click()

# Wait for login to complete.
time.sleep(30)

#Navigate to the page of the profiles we want to scrape and begin the scraping process.
profile_list = "list of profiles"
for profile in profile_list:
    driver.get(profile)
    time.sleep(5)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
#We print, and if we can't, we report the error.
    try:
        intro = soup.find('div', {'class': 'pv-text-details__left-panel'}) 
        name_loc = intro.find("h1")
        name = name_loc.get_text().strip()
        heading_loc = intro.find("div", {'class': 'text-body-medium'})
        heading = heading_loc.get_text().strip()
        try:
            containers = soup.find_all('div', {'class': 'pvs-list__outer-container'})
            experience = containers[3]
            job_loc = experience.find_all('div', {'class':'display-flex flex-wrap align-items-center full-height'})
            company_loc = experience.find_all('span', {'class':'t-14 t-normal'})
            date_loc = experience.find_all('span', {'class':'t-14 t-normal t-black--light'})
            job0 = job_loc[0].get_text().strip()
            job1 = job_loc[1].get_text().strip()
            job2 = job_loc[2].get_text().strip()
            company0 = company_loc[0].get_text().strip()
            company1 = company_loc[1].get_text().strip()
            company2 = company_loc[2].get_text().strip()
            date0 = date_loc[0].get_text().strip()
            date1 = date_loc[1].get_text().strip()
            date2 = date_loc[2].get_text().strip()
            print(name, "," , heading, "," , job0, "," , company0, ",", date0, ",", job1, ",", company1, ",", date1, ",", job2,",", company2,",",date2, ",", profile, file=f)
        except:
                print(name,",",heading,",",profile,file=f)
    except:
        print("Invalid link:", profile, file=f)

driver.quit()
f.close()
#That's it! The .txt file will be in the working directory; simply search up jdmba.txt on your device.
#Note: LinkedIn's API duplicates the job, company, and date strings, so they will show up twice. This requires manual cleanings.
