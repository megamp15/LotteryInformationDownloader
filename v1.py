from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import os
import pandas as pd
import time

# user_name = input("Enter your username: ")
# password = getpass("Enter your password: ")

# date1 = "04/01/2020"
# date2 = "05/02/2020"

# options = webdriver.ChromeOptions()
# options.add_argument(
#     "download.default_directory=C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\Lottery\\AKU - Groves Super Stop"
# )
# driver = webdriver.Chrome(
#     options=options,
#     executable_path="C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\webDrivers\\chromedriver.exe",
# )
cur = os.getcwd()
Lottery_dir = cur + "\\" + "Lottery"
filelist = os.listdir(Lottery_dir)


df = pd.read_excel(cur + "\\hidden.xlsx")
# print(df)
df.sort_values(by=["USERNAME"], inplace=True)
df = df.reset_index()
print(df)

for i in df["COMPANY"]:
    if i in filelist:
        print(i)


def auto_download(user_name, password, retailer_num, close_window):
    date1 = "04/01/2020"
    date2 = "05/02/2020"
    chromeOptions = Options()
    chromeOptions.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\Lottery\\AKU - Groves Super Stop"
        },
    )

    driver = webdriver.Chrome(
        options=chromeOptions,
        executable_path="C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\webDrivers\\chromedriver.exe",
    )

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome")
    time.sleep(1)
    username_textbox = driver.find_element_by_id("username")
    first_login_button = driver.find_elements_by_class_name("btn")

    username_textbox.send_keys(user_name)
    first_login_button[0].submit()

    password_textbox = driver.find_element_by_id("password")
    second_login_button = driver.find_elements_by_class_name("btn")

    password_textbox.send_keys(password)
    second_login_button[0].submit()

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/auth/viewreports")
    # time.sleep(1)
    retailer = Select(driver.find_element_by_id("retailerId"))
    retailer.select_by_value("retailer_num")

    start_date = driver.find_element_by_id("startInvoiceDate")
    end_date = driver.find_element_by_id("endInvoiceDate")

    start_date.send_keys(date1)
    end_date.send_keys(date2)

    report_category = Select(driver.find_element_by_id("subCategoryCd"))
    report_category.select_by_value("-1")

    # Pack Inventory
    time.sleep(1)
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("2")

    time.sleep(2)
    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    count = 0
    for i in date:
        if i.text[:2] == date1[:2]:
            # csv[count].click()
            break
        count += 1

    # Pack Activated
    time.sleep(1)
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("4")

    time.sleep(2)
    csv = driver.find_elements_by_class_name("downloadcsv")

    for i in range(len(csv) - 1, -1, -1):
        time.sleep(0.5)
        # csv[i].click()

    # Statement Summary
    time.sleep(1)
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("17")

    time.sleep(2)
    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    idx = []
    count = 0
    for i in date:
        if i.text[:2] == date1[:2]:
            idx.append(count)
        count += 1
    idx.reverse()
    for i in idx:
        time.sleep(0.5)
    # csv[i].click()
    if close_window:
        time.sleep(5)
        driver.close()


i = 0
while i <= 23:
    user_name = df["USERNAME"][i]
    password = df["PASSWORD"][i]
    retailer_num = df["RETAILER NUMBER"][i]
    while df["USERNAME"][i] == df["USERNAME"][i + 1]:
        i += 1
        # auto_download(user_name, password, df["RETAILER NUMBER"][i], False)
        print("IN LOOP")
    else:
        # auto_download(user_name, password, retailer_num, True)
        i += 1
        print("OUT LOOP")
