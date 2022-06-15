import argparse
import time

import csv
import re

from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import datetime

e = datetime.datetime.now()



with open('./linkedin_credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]



def _login(browser, email, password):
    browser.get("https://www.linkedin.com")
    browser.maximize_window()
    browser.find_element_by_name("session_key").send_keys(email)
    browser.find_element_by_name("session_password").send_keys(password)
    browser.find_element_by_class_name('sign-in-form__submit-button').click()
    time.sleep(3)




def profileCollect(browser,listProfile):
    
    profiles = browser.find_elements_by_class_name("reusable-search__result-container")
    for profile in profiles:
        item = profile.find_element_by_class_name("app-aware-link").get_attribute('href')
        listProfile.append(item)
    return listProfile

def pageLoad(browser,pages,listProfile):
    for i in range(0,pages):
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        profileCollect(browser,listProfile)
        print(f"In {i+1} page {len(listProfile)} profile's found")
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Next']"))).click()
        except:
            break


def ProfileidCollect(listProfile):
    with open(f'./profileid/{e.day}_{e.month}_{e.year}_{e.hour}_{e.minute}_profile_id.csv', 'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in listProfile:
                writer.writerow([i])

def profileDataCollect(browser,listProfile):

    
    
    postBigDict = list()
    # return postBigDict
              
    for it,profile in enumerate(listProfile):
        browser.get(profile)
        try:
            name  = browser.find_element_by_xpath("*//main/div/section/div[2]/div[2]/div[1]/div[1]/h1").text
        except:
            name = "Not Found"
        try:
            company = browser.find_element_by_xpath("//div[@aria-label='Current company']").text
        except:
            company = "Not Found"
        try:
            about = browser.find_element_by_class_name("inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14").text.strip()
            try:
                match = re.search(r'[\w\.-]+@[\w\.-]+', about)
                mail = match.group(0)
            except:
                mail = "Not found"
        except:
            about = "Not Found"
            mail = "Not Found"
        try:
            browser.find_element_by_class_name("ember-view.link-without-visited-state.cursor-pointer.text-heading-small.inline-block.break-words").click()
            time.sleep(1)
            
            try:
                se_mail = browser.find_element_by_xpath("//section[@class='pv-contact-info__contact-type ci-email']/div").text
                time.sleep(1)
                
            except:
                se_mail = "Not Found"
        except:
            se_mail = "Not Found"

        postDict = dict()
        postDict['Name'] = name
        postDict['Company'] = company
        postDict['About'] = about
        postDict['Email'] = mail
        postDict['Linkedin'] = profile
        postDict['Second Email']=se_mail
        postBigDict.append(postDict)
        print(f"{it+1} profile  data collected Next is processing")
    with open(f'./data/{e.day}_{e.month}_{e.year}_{e.hour}_{e.minute}_profile_data.csv', 'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
           #writer.writerow(['Post', 'Link', 'Image', 'Comments', 'Reaction'])
            writer.writerow(['Name', 'Company', 'about','Email','Linkedin','Second Email'])
            for post in postBigDict:
                writer.writerow([post['Name'], post['Company'],post['About'],post['Email'],post['Linkedin'],post['Second Email']])



def extract(page, numOfPage):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    # chromedriver should be in the same folder as file
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=option)
    _login(browser, EMAIL, PASSWORD)
    browser.get(page)

    listProfile = []
    print("=======================================================================")
    print("=======================================================================")
    print("==============================Start Page Load==========================")
    pageLoad(browser,numOfPage,listProfile)
    print("==============================Stop Page Load===========================")
    print("=======================================================================")
    print("=======================================================================")
    print("==============================Start Data Collection====================")
    ProfileidCollect(listProfile)
    print("=======================================================================")
    print("=======================================================================")
    profileDataCollect(browser,listProfile)
    print("==============================Stop Data Collection====================")
    print("=======================================================================")
    print("=======================================================================")
    
    


if __name__ == "__main__":
    pageName = input("Enter a linkedin page that you start scrape:\n")
    pageNumber = int(input("enter number of page that you scrape: \n")) 

    postBigDict = extract(page=pageName, numOfPage=pageNumber)

    print("Finished")
