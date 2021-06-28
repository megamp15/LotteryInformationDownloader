# IMPORTS
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from dateutil.relativedelta import relativedelta, FR
from datetime import date, timedelta
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
# import threading
from threading import Thread
import sys
from fake_useragent import UserAgent
# Configure the chrome driver settings.
# Specifically we change the download prefrence to a specific folder in the Lottery directory
# Configure webDriverwait for the chrome webdriver named driver to wait for the elements for 120 seconds max


def configDriver(dir, folder):
    temp = dir+"/"+folder
    path = temp.replace('/', '\\')
    global driver, wait
    chromeOptions = Options()
    ua = UserAgent()
    userAgent = ua.random

    chromeOptions.add_experimental_option(
        "prefs",
        {
            "download.default_directory": path
        },
    )
    chromeOptions.add_experimental_option("detach", True)
    chromeOptions.add_argument(f'--user-agent={userAgent}')
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
    driver.quit()


def create_folder(dir, df):
    df_usernames = df['COMPANY']
    dir_list = os.listdir(dir)
    for i in df_usernames:
        if i.strip() not in dir_list:
            os.mkdir(dir+"/"+i.strip())


# Create a data frame from the excel file to visualize contents and sort by user_name (emails).
def get_data(p):
    df = pd.read_excel(p)
    df.sort_values(by=["USERNAME"], inplace=True)
    df = df.reset_index()
    return df


def get_retailers(df):
    return tuple([i.strip() for i in df['COMPANY']])


# Main function that initates the webdriver, login, select options, and downloads all csv files.
def auto_download(user_name, password, path, folder, retailer_num, date_start, date_end):
    configDriver(path, folder)
    login(user_name, password)
    config_selects(retailer_num, date_start, date_end)
    pack_inventory(date_start)
    packs_Activated()
    statement_sum(date_start)
    close_driver()


# The loop that goes through the data frame and uses the data to call the auto_download function to download the csv files for the clients.
def loop(path, df, date_start, date_end, master, single=""):
    if single == "":
        # Hard coded range for now.
        for i in range(len(df["USERNAME"])):
            user_name = df["USERNAME"][i].strip()
            password = df["PASSWORD"][i].strip()
            retailer_num = str(df["RETAILER NUMBER"][i]).strip()
            folder = df["COMPANY"][i].strip()
            try:
                auto_download(user_name, password, path, folder,
                              retailer_num, date_start, date_end)
            except:
                print("ERROR in:", df["COMPANY"][i])
                pass
        # messagebox.showinfo(
        #     title="Lottery Information Downloader", message="Program Completed!")
        # master.destroy()
    else:
        for i in range(len(df["COMPANY"])):
            if single == df["COMPANY"][i].strip():
                user_name = df["USERNAME"][i].strip()
                password = df["PASSWORD"][i].strip()
                retailer_num = str(df["RETAILER NUMBER"][i]).strip()
                folder = df["COMPANY"][i].strip()
                try:
                    auto_download(user_name, password, path, folder,
                                  retailer_num, date_start, date_end)
                    # messagebox.showinfo(
                    #     title="Lottery Information Downloader", message="Program Completed!")
                    # master.destroy()
                except:
                    print("ERROR in:", df["COMPANY"][i])
                    pass
    return True


class DownloaderGUI:

    def __init__(self, master):

        master.title('Lottery Information Downloader')
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))

        self.entry1 = StringVar(master)
        self.entry2 = StringVar(master)
        self.entry3 = StringVar(master)
        self.entry4 = StringVar(master)
        self.sel = StringVar(master)
        self.single_retailer = StringVar(master)
        self.error = False

        self.entry1.trace("w", self.validation)
        self.entry2.trace("w", self.validation)
        self.entry3.trace("w", self.validation)
        self.entry4.trace("w", self.validation)
        self.sel.trace("w", self.validation)
        self.single_retailer.trace("w", self.validation)

        # First File Frame
        self.file_frame = ttk.Frame(master, relief=GROOVE)
        self.file_frame.grid(row=0)

        ttk.Label(self.file_frame, text="Select Excel File: ").grid(
            row=0, column=0, sticky="W", padx=(2, 0), pady=(20, 0))

        self.e1 = ttk.Entry(self.file_frame, width=50,
                            textvariable=self.entry1)
        self.e1.grid(row=0, column=1, columnspan=4,
                     sticky="NSEW", pady=(20, 0))

        self.b1 = ttk.Button(self.file_frame, text="Browse",
                             command=self.getFilePath)
        self.b1.grid(row=0, column=5, sticky="NSEW", padx=5, pady=(20, 0))

        ttk.Label(self.file_frame, text="Select Download Folder: ").grid(
            row=1, column=0, sticky="W", padx=(2, 0), pady=(0, 20))

        self.e2 = ttk.Entry(self.file_frame, width=50,
                            textvariable=self.entry2)
        self.e2.grid(row=1, column=1, columnspan=4,
                     sticky="NSEW", pady=(0, 20))

        self.b2 = ttk.Button(self.file_frame, text="Browse",
                             command=self.getDirPath)
        self.b2.grid(row=1, column=5, sticky="NSEW", padx=5, pady=(0, 20))

        self.date_frame = ttk.Frame(master, relief=GROOVE)
        self.date_frame.grid(row=1)

        self.dates = self.placeholder_dates()
        ttk.Label(self.date_frame, text="Start Date: ").grid(
            row=0, column=0, sticky="E", padx=(70, 0), pady=10)

        self.e3 = ttk.Entry(self.date_frame, width=20,
                            textvariable=self.entry3)

        self.e3.insert(0, self.dates[0])
        self.e3.grid(row=0, column=1, sticky="W", padx=(0, 15), pady=10)
        self.e3.bind('<1>', self.placeholder)

        ttk.Label(self.date_frame, text="End Date: ").grid(
            row=0, column=2, sticky="E", pady=10)

        self.e4 = ttk.Entry(self.date_frame, width=20,
                            textvariable=self.entry4)
        self.e4.insert(0, self.dates[1])
        self.e4.grid(row=0, column=3, sticky="W", padx=(0, 79), pady=10)
        self.e4.bind('<1>', self.placeholder)

        self.sel_frame = ttk.Frame(master, relief=GROOVE)
        self.sel_frame.grid(row=2)

        ttk.Label(self.sel_frame, text="Select download type: ").grid(
            row=0, sticky="E", padx=(135, 0), pady=10)

        self.combobox1 = ttk.Combobox(
            self.sel_frame, textvariable=self.sel)
        self.combobox1.grid(row=0, column=1, sticky="W",
                            padx=(0, 138), pady=10)
        self.combobox1.config(values=('ALL', 'SINGLE'), state="readonly")

        self.start_frame = ttk.Frame(master, relief=GROOVE)
        self.start_frame.grid(row=3)

        self.button = ttk.Button(
            self.start_frame, text="START", command=lambda: self.getInfo(master), state='disabled')
        self.button.grid(row=0, padx=(231, 234), pady=10)

        self.single_frame = ttk.Frame(master, relief=GROOVE)
        self.single_frame.grid(row=4)

    def validation(self, *args):
        entry1 = self.entry1.get() != ""
        entry2 = self.entry2.get() != ""
        entry3 = self.entry3.get() != ""
        entry4 = self.entry4.get() != ""
        sel = self.sel.get() != ""
        single_retailer = self.single_retailer.get() != ""
        error_check = entry1 and entry2 and entry3 and entry4 or self.error
        first_check = entry1 and entry2 and entry3 and entry4 and sel
        second_check = first_check and single_retailer

        if self.sel.get() == "SINGLE":
            if not error_check:
                messagebox.showwarning(title="Lottery Information Downloader",
                                       message="Please finish filling in the appropriate information above!")
                self.error = True
            else:
                if first_check:
                    self.start_frame.grid_forget()
                    self.single_frame.grid(row=4)
                    ttk.Label(self.single_frame, text="Select Retailer: ").grid(
                        row=0, sticky="E", padx=(153, 0), pady=10)
                    self.combobox2 = ttk.Combobox(
                        self.single_frame, textvariable=self.single_retailer)
                    self.combobox2.grid(row=0, column=1, sticky="W",
                                        padx=(0, 159), pady=10)
                    self.combobox2.config(values=get_retailers(
                        self.data), state="readonly")
                    self.start_frame.grid(row=5)
                    if second_check:
                        self.button.config(state='normal')
                    else:
                        self.button.config(state='disabled')

        if self.sel.get() == "ALL":
            if not error_check:
                messagebox.showwarning(title="Lottery Information Downloader",
                                       message="Please finish filling in the appropriate information above!")
                self.error = True
            else:
                self.single_frame.grid_forget()
                if first_check:
                    self.button.config(state='normal')

    def getInfo(self, master):

        if self.sel.get() == "ALL":
            x = Thread(target=loop, args=(self.dirname, self.data,
                                          self.entry3.get(), self.entry4.get(), master, "",))
        if self.sel.get() == "SINGLE":
            x = Thread(target=loop, args=(self.dirname, self.data,
                                          self.entry3.get(), self.entry4.get(), master, self.single_retailer.get(),))
        x.start()
        x.join()
        messagebox.showinfo(
            title="Lottery Information Downloader", message="Program Completed!")
        master.destroy()

    def getFilePath(self):
        self.filename = filedialog.askopenfilename(title="Select A File", filetypes=(
            ("excel files", "*.xlsx"), ("all files", "*.*")))
        if self.filename != "":
            self.data = get_data(self.filename)
            self.e1.insert(0, self.filename)

    def getDirPath(self):
        if self.entry1.get() == "":
            messagebox.showwarning(title="Lottery Information Downloader",
                                   message="Please select an excel file ending in .xlsx first!")
        else:
            dirname = filedialog.askdirectory()
            if dirname != NONE:
                self.e2.insert(0, dirname)
                self.dirname = dirname
                create_folder(self.dirname, self.data)

    def placeholder(self, event):
        event.widget.delete(0, END)

    def placeholder_dates(self):
        d = date.today()-relativedelta(months=1)
        first_day = d-relativedelta(days=d.day-1)
        temp_d = d+relativedelta(day=31, weekday=FR(-1)) + \
            relativedelta(weeks=1, days=1)
        if temp_d.day != 7:
            last_day = d+relativedelta(day=31, weekday=FR(-1)) + \
                relativedelta(weeks=1, days=1)
        else:
            last_day = d+relativedelta(day=31, weekday=FR(-1)) + \
                relativedelta(days=1)
        first_day = "{0}/{1}/{2}".format(str(first_day.month).zfill(
            2), str(first_day.day).zfill(2), first_day.year)
        last_day = "{0}/{1}/{2}".format(str(last_day.month).zfill(2),
                                        str(last_day.day).zfill(2), last_day.year)
        return first_day, last_day


def main():
    root = Tk()
    DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()