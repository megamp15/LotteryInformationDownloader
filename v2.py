from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import os
import time

# TODO: FIX TIME DELAYS FOR THE FUNCTION BELOW. TRY USING ASYNC OR AWAIT FUNC IN PYTHON


def auto_download(user_name, password, folder, retailer_num, close_window):
    date_start = "04/01/2020"
    date_end = "05/02/2020"

    chromeOptions = Options()
    chromeOptions.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\Lottery\\"
            + folder
        },
    )
    chromeOptions.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        options=chromeOptions,
        executable_path="C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\webDrivers\\chromedriver.exe",
    )

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome")
    time.sleep(2.5)
    username_textbox = driver.find_element_by_id("username")
    first_login_button = driver.find_elements_by_class_name("btn")

    username_textbox.send_keys(user_name)
    first_login_button[0].submit()
    time.sleep(1.5)

    password_textbox = driver.find_element_by_id("password")
    second_login_button = driver.find_elements_by_class_name("btn")

    password_textbox.send_keys(password)
    second_login_button[0].submit()
    time.sleep(1.5)

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/auth/viewreports")
    time.sleep(2.5)
    retailer = Select(driver.find_element_by_id("retailerId"))
    retailer.select_by_value(retailer_num)

    start_date = driver.find_element_by_id("startInvoiceDate")
    end_date = driver.find_element_by_id("endInvoiceDate")

    start_date.send_keys(date_start)
    end_date.send_keys(date_end)

    report_category = Select(driver.find_element_by_id("subCategoryCd"))
    report_category.select_by_value("-1")
    time.sleep(2.5)

    # Pack Inventory
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("2")
    time.sleep(2.5)

    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    count = 0
    for i in date:
        if i.text[:2] == date_start[:2]:
            csv[count].click()
            time.sleep(1.75)
            break
        count += 1

    # Pack Activated
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("4")
    time.sleep(2.5)

    csv = driver.find_elements_by_class_name("downloadcsv")

    for i in range(len(csv) - 1, -1, -1):
        csv[i].click()
        time.sleep(1.75)

    # Statement Summary
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("17")
    time.sleep(2.5)

    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    idx = []
    count = 0
    for i in date:
        if i.text[:2] == date_start[:2]:
            idx.append(count)
        count += 1
    idx.reverse()
    for i in idx:
        csv[i].click()
        time.sleep(1.75)

    if close_window == True:
        time.sleep(2.5)
        driver.close()


user_name = input("Enter your username: ")
password = getpass("Enter your password: ")
folder = input("Enter folder: ")
retailer_num = input("Enter retailer number: ")
close_window = True

auto_download(user_name, password, folder, retailer_num, close_window)
