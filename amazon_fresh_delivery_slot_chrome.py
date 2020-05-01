import os
import random
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException


NO_OPEN_SLOTS = "No doorstep delivery windows are available for"


def check_slots(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(60)

    while True:
        driver.refresh()
        time.sleep(5)
        print("refreshed")

        try:
            check_days(driver, 0)
            # button_next = driver.find_element_by_id("nextButton-announce")
            # button_next.click()
            time.sleep(random.randint(5, 9))
            # check_days(driver, 4)

        except WebDriverException as e:
            if "shippingOptionFormId" in str(e):
                print("Attempting navigate to the Amazon Fresh's delivery slot selection page. "
                      "If error continues, try to navigate there manually.")
                handle_logout(driver)
                time.sleep(random.randint(5, 10))

            else:
                print(e)
            continue

        time.sleep(random.randint(30, 50))


def check_days(driver, offset):
    for i in range(offset, offset + 3):
        date_ = "{}-{:02d}-{:02d}".format(date.today().year, date.today().month, date.today().day + i)
        button_id = "date-button-{}-announce".format(date_)

        print("Checking slots on {}".format(date_))

        try:
            button = driver.find_element_by_id(button_id)
            button.click()
            time.sleep(random.randint(3, 7))
        except:
            pass

        if NO_OPEN_SLOTS not in driver.page_source:
            print("SLOTS OPEN on {}!".format(date_))
            os.system('say "Slots for delivery may have opened"')
            print('Continue checking? yes | no')
            answer = raw_input()
            if answer.lower() == "yes":
                continue
            else:
                exit(0)


def handle_logout(driver):

    if "Sign in to your account" in driver.page_source:
        print("Signing in...")
        sign_in = driver.find_element_by_partial_link_text("Sign in")
        sign_in.click()

    if "Email (phone for mobile accounts)" in driver.page_source:
        print("Entering email...")
        email = driver.find_element_by_id("ap_email")
        email.send_keys(os.environ.get("email"))
        cont = driver.find_element_by_id("continue")
        cont.click()

    if "Password" in driver.page_source:
        print("Entering password...")
        passwd = driver.find_element_by_id("ap_password")
        passwd.send_keys(os.environ.get("passwd"))
        sign_in = driver.find_element_by_id("signInSubmit")
        sign_in.click()

    if "Checkout Amazon Fresh Cart" in driver.page_source:
        print("Clicking checkout button...")
        button_box = driver.find_element_by_id("sc-fresh-buy-box")
        checkout = button_box.find_element_by_class_name("a-button-inner")
        checkout.click()
        time.sleep(5)
        cont = driver.find_element_by_partial_link_text("Continue")
        cont.click()

    if "Before you checkout" in driver.page_source:
        cont = driver.find_element_by_partial_link_text("Continue")
        cont.click()

    if "We're sorry we are unable to fulfill your entire order" in driver.page_source:
        cont = driver.find_element_by_partial_link_text("Continue")
        cont.click()
        time.sleep(5)


check_slots("https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1")
