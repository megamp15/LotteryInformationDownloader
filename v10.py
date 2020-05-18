# IMPORTS
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from getpass import getpass
import pandas as pd
import os
import time
import math

# Configure the chrome driver settings.
# Specifically we change the download prefrence to a specific folder in the Lottery directory
# Configure webDriverwait for the chrome webdriver named driver to wait for the elements for 120 seconds max


def configDriver(folder):
    global driver, wait
    chromeOptions = Options()
    chromeOptions.add_experimental_option(
        "prefs",
        {
            # "download.default_directory": "C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\retailLotteryDownloader\\Lottery\\"
            # + folder
            "download.default_directory": folder
        },
    )
    chromeOptions.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        options=chromeOptions,
        executable_path="C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\retailLotteryDownloader\\webDrivers\\chromedriver.exe",
    )
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 120)


# Loads the Lottery website and types in the username and clicks the login button
# A different page is loaded where we type in the password and click the second login button
def login(user_name, password):
    # Chrome webDriver opens the lottery website with the link
    driver.get("https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome")

    # Waits for the user_name textbox to load on the website and then type the user_name parameter into the textbox
    try:
        username_textbox = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_textbox.send_keys(user_name)
    except:
        print("ERROR: USERNAME TEXTBOX")
        driver.close()

    # Waits for the button to load on the website and then click the log in button.
    try:
        first_login_button = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn"))
        )
        first_login_button[0].submit()
    except:
        print("ERROR: FIRST LOGIN BUTTON")
        driver.close()

    # Waits for the password textbox to load on the website and then type the password parameter into the textbox
    try:
        password_textbox = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_textbox.send_keys(password)
    except:
        print("ERROR: PASSWORD TEXTBOX")
        driver.close()

    # Waits for the button to load on the website and then click the log in button.
    try:
        second_login_button = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn"))
        )
        second_login_button[0].submit()
    except:
        print("ERROR: SECOND LOGIN BUTTON")
        driver.close()


# Configure the drop down menus and the textboxes for start and end date
def config_selects(retailer_num, date_start, date_end):
    driver.get("https://tx-lsp.lotteryservices.com/lsptx/auth/viewreports")

    # Waits for the retailer dropdown to load on the website and then select the correct retailer by retailer number
    try:
        retailer = Select(
            wait.until(EC.presence_of_element_located((By.ID, "retailerId")))
        )
        retailer.select_by_value(retailer_num)
    except:
        print("ERROR: RETAILER DROP-DOWN")
        driver.close()

    # Waits for the startInvoiceDate textbox/calendar to load on the website and then types the date_start variable from the parameters passed in
    try:
        start_date = wait.until(
            EC.presence_of_element_located((By.ID, "startInvoiceDate"))
        )
        start_date.send_keys(date_start)
    except:
        print("ERROR: START INVOICE DATE")
        driver.close()

    # Waits for the endInvoiceDate textbox/calendar to load on the website and then types the date_end variable from the parameters passed in
    try:
        end_date = wait.until(
            EC.presence_of_element_located((By.ID, "endInvoiceDate")))
        end_date.send_keys(date_end)
    except:
        print("ERROR: END INVOICE DATE")
        driver.close()

    # Waits for the Report Category dropdown to load on the website and then select All Categories option
    try:
        report_category = Select(
            wait.until(EC.presence_of_element_located(
                (By.ID, "subCategoryCd")))
        )
        report_category.select_by_value("-1")
    except:
        print("ERROR: Selecting ALL CATEGORIES")
        driver.close()


# Downloads the last week of the date_start month csv file from the table in the pack inventory option.
def pack_inventory(date_start):
    # Waits for the ReportName Category dropdown to load on the website and then select the Pack Inventory option
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("2")
    except:
        print("ERROR: SELECTING PACK INVENTORY")
        driver.close()

    # Waits for the the table that has the download link to load on the website
    try:
        date = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@id='rptTable']/tbody/tr/td[2]")
            )
        )
        # Get the indices of all dates that are in the date_start month and not in the date_end month. EX) date_start = 04/01/2020 then indices will have all dates that are in 04 April.
        # The order of the dates is backwards due to how it is displayed on the Lottery Website
        indices = [i for i, d in enumerate(date) if date_start[:2] in d.text]
    except:
        print("ERROR: TABLE - DATES - PACK INVENTORY")
        driver.close()

    # Waits for the the csv div elements that are clickable to load on the website.
    # We click the csv div element that is first in the indicies list because we want the last csv file in the date_start month.
    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        csv[indices[0]].click()
        time.sleep(1)
    except:
        print("ERROR: PACK INVENTORY CSV DOWNLOAD")
        driver.close()


# Downloads all the csv files from the table in the packs activated option.
def packs_Activated():
    # Waits for the ReportName Category dropdown to load on the website and then select the Packs Activated option
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("4")
    except:
        print("ERROR: SELECTING PACKS ACTIVATED")
        driver.close()

    # Waits for the the csv div elements that are clickable to load on the website.
    # We click all csv files in reverse order because we want the downloads to be in correct time order.
    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        for i in range(len(csv) - 1, -1, -1):
            csv[i].click()
            # Time delay for the program due to the lag of download to the correct file.
            time.sleep(1)
    except:
        print("ERROR: PACK ACTIVATED CSV DOWNLOAD")
        driver.close()


# Downloads all the csv files in the date_start month from the table in the Statement Summary option.
def statement_sum(date_start):
    # Waits for the ReportName Category dropdown to load on the website and then select the Statement Summary option
    try:
        report_name = Select(
            wait.until(EC.presence_of_element_located((By.ID, "reportName")))
        )
        report_name.select_by_value("17")
    except:
        print("ERROR: SELECTING STATEMENT SUMMARY")
        driver.close()

    # Waits for the the table that has the download link to load on the website
    try:
        date = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@id='rptTable']/tbody/tr/td[2]")
            )
        )
        # Get the indices of all dates that are in the date_start month and not in the date_end month. EX) date_start = 04/01/2020 then indices will have all dates that are in 04 April.
        # The order of the dates is backwards due to how it is displayed on the Lottery Website so we use the indicies.reverse() to reverse the order.
        indices = [i for i, d in enumerate(date) if date_start[:2] in d.text]
        indices.reverse()
    except:
        print("ERROR: TABLE - DATES - STATEMENT SUMMARY")
        driver.close()

    # Waits for the the csv div elements that are clickable to load on the website.
    # We click all csv files in normal order because we reversed the order of the indices so the downloads are in the correct time order already.
    try:
        csv = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "downloadcsv"))
        )
        for i in indices:
            csv[i].click()
            time.sleep(1)
    except:
        print("ERROR: STATEMENT SUMMARY CSV DOWNLOAD")
        driver.close()


# Close the chrome webdriver with a 2second delay to make sure all other processes were completed
def close_driver():
    time.sleep(2)
    driver.close()


def create_folder(Lottery_dir, retailer_name, date_start):
    Month = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR", "05": "MAY", "06": "JUN",
             "07": "JUL", "08": "AUG", "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}
    path = Lottery_dir+"\\"+retailer_name+"\\" + \
        Month[date_start[:2]]+"-"+date_start[6:]
    print(path)
    os.mkdir(path)
    return path
# Configure the filepath to the current directory, the Lottery directory and all Files/directories in the Lottery Directory


def config_filePath():
    cur = os.getcwd()
    Lottery_dir = cur + "\\" + "Lottery"
    filelist = os.listdir(Lottery_dir)
    return cur, Lottery_dir, filelist


# Delete all files in each directory in lottery
def clean_lottery_folders(filelist, Lottery_dir):
    for x in filelist:
        del_file_dir = Lottery_dir + "\\" + x
        del_file_list = os.listdir(del_file_dir)
        for f in del_file_list:
            os.remove(del_file_dir + "\\" + f)


# def create_folder(Lottery_dir, retailer_name, date_start){
#     print(date_start[7:])
#     {"01":"JAN"}
#     path = Lottery_dir+"\\"+retailer_name+"\\"+date_start[:2]
#     os.mkdir(path)
# }
# Create a data frame from the excel file to visualize contents and sort by user_name (emails).


def get_data(cur):
    df = pd.read_excel(cur + "\\hidden.xlsx")
    df.sort_values(by=["USERNAME"], inplace=True)
    df = df.reset_index()
    return df


# Main function that initates the webdriver, login, select options, and download all csv files.
def auto_download(user_name, password, folder, retailer_num, close_window, date_start, date_end):
    # date_start = "04/01/2020"
    # date_end = "05/02/2020"
    configDriver(folder)
    login(user_name, password)
    config_selects(retailer_num, date_start, date_end)
    pack_inventory(date_start)
    packs_Activated()
    statement_sum(date_start)
    if close_window:
        close_driver()


# The loop that goes through the data frame and uses the data to call the auto_download function to download the csv files for the clients.
# def loop(df):
#     # Hard coded range for now.
#     for i in range(len(df["USERNAME"])):
#         user_name = df["USERNAME"][i].strip()
#         password = df["PASSWORD"][i].strip()
#         retailer_num = str(df["RETAILER NUMBER"][i]).strip()
#         folder = df["COMPANY"][i].strip()
#         try:
#             auto_download(user_name, password, folder, retailer_num, True)
#         except:
#             print("ERROR in:", df["COMPANY"][i])
#             pass


# main function that calls all above functions. We configure the file path and call clean_lottery if we want to.
# We get the excel file and make a data frame and pass that to loop to continue with the rest of the download functions.
def main():
    del_lottery = False
    path = config_filePath()
    if del_lottery:
        # clean_lottery_folders(path[2], path[1])
        pass
    data = get_data(path[0])
    # loop(data)
    date = [str(i).zfill(2) for i in range(1, 13)]
    date_start_1 = [i+"/01/2019" for i in date]
    date_2 = [str(i).zfill(2) for i in range(1, 6)]
    date_start_2 = [i+"/01/2020" for i in date_2]
    date_start = date_start_1+date_start_2
    print(date_start)
    date_end = ['01/31/2019', '02/28/2019', '03/31/2019', '04/30/2019', '05/31/2019', '06/30/2019', '07/31/2019', '08/31/2019',
                '09/30/2019', '10/31/2019', '11/30/2019', '12/31/2019', '01/31/2020', '02/29/2020', '03/31/2020', '04/30/2020', '05/31/2020']
    print(date_end)

    # date_start = "06/01/2019"
    # date_end = "06/31/2019"
    # for i in range(len(date_start)):
    #     ds = date_start[i]
    #     de = date_end[i]
    #     f = create_folder(path[1], "NB - Springtime", ds)
    #     auto_download("nareshbc@gmail.com", "T786110.", f,
    #                   "183316", True, ds, de)
    f = create_folder(path[1], "NB - Springtime", "02/01/2020")
    auto_download("nareshbc@gmail.com", "T786110.", f,
                  "183316", True, "02/01/2020", "02/29/2020")

    f = create_folder(path[1], "NB - Springtime", "11/01/2019")
    auto_download("nareshbc@gmail.com", "T786110.", f,
                  "183316", True, "11/01/2019", "11/30/2019")


if __name__ == "__main__":
    main()
