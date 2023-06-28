# Aum Patel
# 5/25/23
# This code is designed to scrape lionpath to see if an available spot opens in Carabello's Lab
# Class Number 22875, but can be edited to any class you want
# Just adjusts the variables shown below

# Imports all the necessary documents
# Need to download selenium and twilio libraries
# https://www.selenium.dev/documentation/webdriver/getting_started/
# https://www.twilio.com/docs/libraries/python
# This code is written for firefox so it's drivers also need to be downloaded (geckodriver)

# Make sure to set up windows task scheduler to run this code at your desired interval
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
from twilio.rest import Client

# Twilio account id and token
account_sid = "YOUR SID" # YOUR SID
auth_token = "YOUR TOKEN" # YOUR TOKEN
twilio_num = "YOUR TWILIO NUM" # NUMBER ASSOCIATED WITH TWILIO ACCT in +1 format
your_phone_num = "NUM TO TEXT" # YOUR PHONE NUMBER in +1 format

# Enter classes information here
# Phys 212 lab as an example, but can be editable
term = "2238" # Fall term 2023
campus = 'HB' # Harrisburg campus (UP is University Park)
subject = 'PHYS' # Physics
courseNum = '212' # PHYS 212
classNum = '22875' # Thursday lab section (Find it on left column of class list)

def main():
    try:
        # Sets up the headless browser
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)

        # Opens up the public lion path website on firefox
        browser.get('https://public.lionpath.psu.edu/psp/CSPRD/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?PORTALPARAM_PTCNAV=HC_CLASS_SEARCH_GBL&EOPP.SCNode=HRMS&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Self%20Service&EOPP.SCPTfname=CO_EMPLOYEE_SELF_SERVICE&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_CLASS_SEARCH_GBL&IsFolder=false')

        time.sleep(3) # uses this time to load website (may need to inc depending on machine)
        # Sets the browser to iframe so we can navigate the dynamic website
        frame_ref = browser.find_element(By.XPATH, '//*[@id="ptifrmtgtframe"]')
        iframe = browser.switch_to.frame(frame_ref)

        # Selects the fall term
        termDropdown = Select(browser.find_element(By.ID, "CLASS_SRCH_WRK2_STRM$35$"))
        # Fall Term change number below for different terms
        termDropdown.select_by_value(term)

        time.sleep(3)
        # Changes campus, subject and types in course number
        campusDropdown = Select(browser.find_element(By.ID, "SSR_CLSRCH_WRK_CAMPUS$0"))
        campusDropdown.select_by_value(campus)

        time.sleep(3)
        subjectDropdown = Select(browser.find_element(By.ID, "SSR_CLSRCH_WRK_SUBJECT_SRCH$2"))
        # Subject field
        subjectDropdown.select_by_value(subject)

        # Unchecks open classes only
        showOpenClasses = browser.find_element(By.ID, "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$6")
        showOpenClasses.click()

        # Course number
        courseNumBox = browser.find_element(By.ID, "SSR_CLSRCH_WRK_CATALOG_NBR$3")
        courseNumBox.send_keys(courseNum + Keys.ENTER)

        # We are in the next webpage now and want to find the class

        # clicks on the section to find enrollment total and available seats
        time.sleep(3)
        # Finds the element by class number and clicks on it
        section = browser.find_element(By.LINK_TEXT, classNum)
        section.click()

        # Gets enrollment total and available seats
        time.sleep(3)
        enrollTotal = int(browser.find_element(By.ID, "SSR_CLS_DTL_WRK_ENRL_TOT").text)
        availableSeats = int(browser.find_element(By.ID, "SSR_CLS_DTL_WRK_AVAILABLE_SEATS").text)


        # If available seats is 1 or more then it sends you an alert via text
        if availableSeats >= 1:
            # Set environment variables for your credentials
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f"{subject} {courseNum} ALERT:\nAvailable Seats: {availableSeats}\nEnrollment Total: {enrollTotal}",
            from_=twilio_num,
            to= your_phone_num)
            print(message.sid)

        else:
            # Closes the browser
            browser.quit()

    
    # Alerts you via text if any exceptions were raised
    except Exception as e:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body=f"{subject} {courseNum} ALERT: Exception has been raised\nException:{type(e)}",
        from_= twilio_num,
        to= your_phone_num)
        print(message.sid)

if __name__ == '__main__':
    main()