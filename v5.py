from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from getpass import getpass
import os
import time


def configDriver(folder):
    global driver, wait
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
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 120)


def login(user_name, password):
    driver.get("https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome")

    try:
        username_textbox = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_textbox.send_keys(user_name)
    except:
        print("DIDNT WORK 1")

    try:
        first_login_button = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn"))
        )
        first_login_button[0].submit()
    except:
        print("DIDNT WORK 2")

    try:
        password_textbox = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_textbox.send_keys(password)
    except:
        print("DIDNT WORK 3")

    try:
        second_login_button = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn"))
        )
        second_login_button[0].submit()
    except:
        print("DIDNT WORK 4")


def config_selects(retailer_num, date_start, date_end):
    driver.get("https://tx-lsp.lotteryservices.com/lsptx/auth/viewreports")

    try:
        retailer = Select(
            wait.until(EC.presence_of_element_located((By.ID, "retailerId")))
        )
        retailer.select_by_value(retailer_num)
    except:
        print("DIDNT WORK 5")

    try:
        start_date = wait.until(
            EC.presence_of_element_located((By.ID, "startInvoiceDate"))
        )
        start_date.send_keys(date_start)
    except:
        print("DIDNT WORK 6")

    try:
        end_date = wait.until(
            EC.presence_of_element_located((By.ID, "endInvoiceDate")))
        end_date.send_keys(date_end)
    except:
        print("DIDNT WORK 7")

    try:
        report_category = Select(
            wait.until(EC.presence_of_element_located(
                (By.ID, "subCategoryCd")))
        )
        report_category.select_by_value("-1")
    except:
        print("DIDNT WORK 8")


def pack_inventory(date_start):
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("2")
    except:
        print("DIDNT WORK 9")

    try:
        date = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@id='rptTable']/tbody/tr/td[2]")
            )
        )
        indices = [i for i, d in enumerate(date) if date_start[:2] in d.text]
    except:
        print("DIDNT WORK 10")

    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        csv[indices[0]].click()
        # time.sleep(1)
    except:
        print("DIDNT WORK 11")


def packs_Activated():
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("4")
    except:
        print("DIDNT WORK 12")

    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        for i in range(len(csv) - 1, -1, -1):
            csv[i].click()
            # time.sleep(1)
    except:
        print("DIDNT WORK 13")


def statement_sum(date_start):
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("17")
    except:
        print("DIDNT WORK 14")

    try:
        date = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@id='rptTable']/tbody/tr/td[2]")
            )
        )
        indices = [i for i, d in enumerate(date) if date_start[:2] in d.text]
        indices.reverse()
    except:
        print("DIDNT WORK 15")

    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        for i in indices:
            csv[i].click()
            # time.sleep(1)
    except:
        print("DIDNT WORK 16")


def close_driver():
    time.sleep(3)
    driver.close()


def clean_lottery_folders():
    # Delete all files in all folders in lottery
    cur = os.getcwd()
    Lottery_dir = cur + "\\" + "Lottery"
    filelist = os.listdir(Lottery_dir)
    for x in filelist:
        del_file_dir = Lottery_dir + "\\" + x
        del_file_list = os.listdir(del_file_dir)
        for f in del_file_list:
            os.remove(del_file_dir + "\\" + f)


def main():
    user_name = input("Enter your username: ")
    password = getpass("Enter your password: ")
    folder = input("Enter folder: ")
    retailer_num = input("Enter retailer number: ")
    close_window = True
    date_start = "04/01/2020"
    date_end = "05/02/2020"
    del_lottery = True
    close_window = True

    if del_lottery:
        clean_lottery_folders()
    configDriver(folder)
    login(user_name, password)
    config_selects(retailer_num, date_start, date_end)
    pack_inventory(date_start)
    packs_Activated()
    statement_sum(date_start)
    if close_window:
        close_driver()


if __name__ == "__main__":
    main()
