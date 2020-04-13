import os
import random
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


NO_OPEN_SLOTS = "No doorstep delivery windows are available for"


def check_slots(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(60)
    "nextButton-announce"

    while True:
        driver.refresh()
        time.sleep(5)
        print("refreshed")

        try:
            # Ensure we're in checkout page, will raise error if not
            driver.find_element_by_id("shippingOptionFormId")
            
            check_days(driver, 0)
            button_next = driver.find_element_by_id("nextButton-announce")
            button_next.click()
            time.sleep(random.randint(5, 10))
            check_days(driver, 4)

        except WebDriverException as e:
            print(e)
            continue

        time.sleep(random.randint(15, 30))


def check_days(driver, offset):
    for i in range(offset, offset + 4):
        date_ = "{}-{:02d}-{:02d}".format(date.today().year, date.today().month, date.today().day + i)
        button_id = "date-button-{}-announce".format(date_)

        print("Checking slots on {}".format(date_))

        button = driver.find_element_by_id(button_id)
        button.click()
        time.sleep(1)

        if NO_OPEN_SLOTS not in driver.page_source:
            print("SLOTS OPEN on {}!".format(date_))
            os.system('say "Slots for delivery opened!"')
            time.sleep(1800)
            exit(0)


check_slots("https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1")
