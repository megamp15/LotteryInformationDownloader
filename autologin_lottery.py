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
    chromeOptions.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
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
        time.sleep(3)
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
            time.sleep(3)
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
            time.sleep(3)
    except:
        print("ERROR: STATEMENT SUMMARY CSV DOWNLOAD")
        driver.close()


# Close the chrome webdriver with a 2second delay to make sure all other processes were completed
def close_driver():
    time.sleep(2)
    driver.quit()


def create_folder(dir, df, retailer=""):
    if retailer == "":
        df_usernames = df['COMPANY']
        dir_list = os.listdir(dir)
        for i in df_usernames:
            if i.strip() not in dir_list:
                os.mkdir(dir+"/"+i.strip())
    else:
        dir_list = os.listdir(dir)
        if retailer.strip() not in dir_list:
            os.mkdir(dir+"/"+retailer.strip())


def delete_files(dir, df, retailer=""):
    if retailer == "":
        df_usernames = df['COMPANY']
        for i in df_usernames:
            del_file_dir = dir + "\\" + i
            del_file_list = os.listdir(del_file_dir)
            for f in del_file_list:
                os.remove(del_file_dir + "\\" + f)
    else:
        del_file_dir = dir + "\\" + retailer
        del_file_list = os.listdir(del_file_dir)
        for f in del_file_list:
            os.remove(del_file_dir + "\\" + f)


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


class DownloaderGUI:
    # Creates the GUI interface with Labels, Entry Fields, Comboboxes, and Buttons
    def __init__(self, master):
        # Edits for the main root tkinter window
        master.title('Lottery Information Downloader')
        master.resizable(False, False)

        # Styling the Labels and Buttons for better viewing
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.layout('TNotebook.Tab', [])

        # Created a invisible notebook to hold hidden frames in the background
        self.tabs = ttk.Notebook(master)
        self.main_tab = ttk.Frame(self.tabs)

        # Variables that are used with trace.
        self.entry1 = StringVar(self.main_tab)
        self.entry2 = StringVar(self.main_tab)
        self.entry3 = StringVar(self.main_tab)
        self.entry4 = StringVar(self.main_tab)
        self.sel = StringVar(self.main_tab)
        self.single_retailer = StringVar(self.main_tab)
        self.delete = IntVar(self.main_tab)
        self.error = False
        # The variables are updated everytime the user types in the entry fields or selects an option in the combobox
        self.entry1.trace("w", self.validation)
        self.entry2.trace("w", self.validation)
        self.entry3.trace("w", self.validation)
        self.entry4.trace("w", self.validation)
        self.sel.trace("w", self.validation)
        self.single_retailer.trace("w", self.validation)
        self.delete.trace("w", self.validation)

        # Getting the file and folder directory frame with Browse button
        self.file_frame = ttk.Frame(self.main_tab, relief=FLAT)
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

        # The start and end date frame with entry fields.
        # Developed a simple placeholder for the entry fields to show the layout of the input.
        self.date_frame = ttk.Frame(self.main_tab, relief=FLAT)
        self.date_frame.grid(row=1)

        self.dates = self.placeholder_dates()
        ttk.Label(self.date_frame, text="Start Date: ").grid(
            row=0, column=0, sticky="E", padx=(69, 0), pady=10)

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

        # The select frame to select if all companies in the excel file should have there lottery downloaded or you can choose to do a single one.
        self.sel_frame = ttk.Frame(self.main_tab, relief=FLAT)
        self.sel_frame.grid(row=2)

        ttk.Label(self.sel_frame, text="Select download type: ").grid(
            row=0, sticky="E", padx=(45, 0), pady=10)

        self.combobox1 = ttk.Combobox(
            self.sel_frame, textvariable=self.sel)
        self.combobox1.grid(row=0, column=1, sticky="W",
                            padx=(0, 30), pady=10)
        self.combobox1.config(values=('ALL', 'SINGLE'), state="readonly")

        self.checkbutton = ttk.Checkbutton(
            self.sel_frame, text="Delete all files in folder(s)", variable=self.delete, onvalue=1, offvalue=0)
        self.checkbutton.grid(row=0, column=2, sticky="E",
                              padx=(0, 43), pady=10)

        # The start frame for the start button which iniates the backend silenium to get the data from the website
        # And end button to end the downloader at anytime.
        self.start_frame = ttk.Frame(self.main_tab, relief=FLAT)
        self.start_frame.grid(row=3)

        self.button = ttk.Button(
            self.start_frame, text="START", command=lambda: self.getInfo(master), state='disabled')
        self.button.grid(row=0, padx=(158, 0), pady=10)

        self._exit = 0  # Used for closing the webdriver
        self.end_button = ttk.Button(
            self.start_frame, text="END", command=lambda: self.exit_GUI(master), state='disabled')
        self.end_button.grid(row=0, column=1, padx=(60, 160), pady=10)

        # The exit frame for the help, error, and exit button.
        self.exit_frame = ttk.Frame(self.main_tab, relief=FLAT)
        self.exit_frame.grid(row=4)

        self.help_button = ttk.Button(
            self.exit_frame, text="HELP", command=self.help_sel)
        self.help_button.grid(row=0, padx=(95, 0), pady=10)

        self.error_button = ttk.Button(
            self.exit_frame, text="ERROR", command=self.error_sel, state='disabled')
        self.error_button.grid(row=0, column=1, padx=(50, 50), pady=10)

        self.exit_button = ttk.Button(
            self.exit_frame, text="EXIT", command=lambda: self.exit_GUI(master, 1))
        self.exit_button.grid(row=0, column=2, padx=(0, 95), pady=10)

        # The single frame is for the selection of a specific company if the user selects single in the above select frame.
        self.single_frame = ttk.Frame(self.main_tab, relief=FLAT)
        self.single_frame.grid(row=5)

        # shows the errors of the program for a given retailer if there are any.
        self.errors_list = []
        self.error_tab = ttk.Frame(self.tabs)

        # The main_tab is the first frame in the invisble notebook.
        self.tabs.add(self.main_tab)
        # The erros tab is the second frame in the invisible notebook
        self.tabs.add(self.error_tab)
        self.tabs.grid(row=0)

    # Used in conjuction with the trace variables to do certain actions if a certain variable(s) are updated
    def validation(self, *args):
        # Checks if certain entry fields are not empty
        entry1 = self.entry1.get() != ""
        entry2 = self.entry2.get() != ""
        entry3 = self.entry3.get() != ""
        entry4 = self.entry4.get() != ""
        sel = self.sel.get() != ""
        single_retailer = self.single_retailer.get() != ""

        # Condensed into single boolean variables for easier checks below
        error_check = entry1 and entry2 and entry3 and entry4 or self.error
        first_check = entry1 and entry2 and entry3 and entry4 and sel
        second_check = first_check and single_retailer

        # Checks if the length of the entries is 10 characters which is the length of the date format
        if len(self.entry3.get()) == 10:
            self.check_dates(self.entry3.get())
        if len(self.entry4.get()) == 10:
            self.check_dates(self.entry4.get())

        # If single is selected we insert the single frame with the combobox for selecting a retailer/company before the start button frame.
        # Show a warning if the other fields are not filled out before selecting all or single
        if self.sel.get() == "SINGLE":
            if not error_check:
                messagebox.showwarning(title="Lottery Information Downloader",
                                       message="Please finish filling in the appropriate information above!")
                self.error = True
            else:
                if first_check:
                    # Removes the start and exit frames
                    self.start_frame.grid_forget()
                    self.exit_frame.grid_forget()
                    # Inserts the single frame with the combobox for choosing a single retailer
                    self.single_frame.grid(row=5)
                    ttk.Label(self.single_frame, text="Select Retailer: ").grid(
                        row=0, sticky="E", padx=(153, 0), pady=10)
                    self.combobox2 = ttk.Combobox(
                        self.single_frame, textvariable=self.single_retailer)
                    self.combobox2.grid(row=0, column=1, sticky="W",
                                        padx=(0, 159), pady=10)
                    self.combobox2.config(values=get_retailers(
                        self.data), state="readonly")
                    # Insert the start and exit frame after the single frame
                    self.start_frame.grid(row=6)
                    self.exit_frame.grid(row=7)
                    # Enabling/Disabling the start and end buttons once all fields are filled in
                    if second_check:
                        self.button.config(state='normal')
                        self.end_button.config(state='normal')
                    else:
                        self.button.config(state='disabled')
                        self.end_button.config(state='disabled')
        # If all is selected we check if all other fields are filled in and then change the button's state to normal so it can be clicked, otherwise a warning messagebox is shown.
        if self.sel.get() == "ALL":
            if not error_check:
                messagebox.showwarning(title="Lottery Information Downloader",
                                       message="Please finish filling in the appropriate information above!")
                self.error = True
            else:
                self.single_frame.grid_forget()
                if first_check:
                    self.button.config(state='normal')

    # Gets the lottery info by calling the loop function in a thread so that is can work in the background without interfering with the tkinter gui loop
    # Once the thread is finished we show a messagebox that the program is completed and then destroy the tkinter GUI to end the program completely.
    def getInfo(self, master):
        self.button.config(state='disabled')
        if self.sel.get() == "ALL":
            create_folder(self.dirname, self.data)
            if self.delete.get() == 1:
                delete_files(self.dirname, self.data)
            x = Thread(target=self.loop, args=(self.dirname, self.data,
                                               self.entry3.get(), self.entry4.get(), master,))
        if self.sel.get() == "SINGLE":
            create_folder(self.dirname, self.data, self.single_retailer.get())
            if self.delete.get() == 1:
                delete_files(self.dirname, self.data,
                             self.single_retailer.get())
            x = Thread(target=self.loop, args=(self.dirname, self.data,
                                               self.entry3.get(), self.entry4.get(), master, self.single_retailer.get(),))
        x.start()  # Start the thread
        self._exit = 1  # Used for ending the webdriver at anytime

    # Function that asks the user to select an excel file.
    def getFilePath(self):
        self.filename = filedialog.askopenfilename(title="Select A File", filetypes=(
            ("excel files", "*.xlsx"), ("all files", "*.*")))
        if self.filename != "":
            if self.filename[-5:] != ".xlsx":
                messagebox.showwarning(title="Lottery Information Downloader",
                                       message="Please select a file ending in .xlsx!")
            else:
                self.data = get_data(self.filename)
                self.e1.insert(0, self.filename)

    # Function that asks the user to select an download directory.
    # Checks if the excel file has been selected first otherwise we get a warning messagebox
    def getDirPath(self):
        if self.entry1.get() == "":
            messagebox.showwarning(title="Lottery Information Downloader",
                                   message="Please select an excel file ending in .xlsx first!")
        else:
            dirname = filedialog.askdirectory()
            if dirname != NONE:
                self.e2.insert(0, dirname)
                self.dirname = dirname

    # Once the start and end date entry fields are clicked the entry fields are cleared.
    def placeholder(self, event):
        if event.widget.get() == self.dates[0] or event.widget.get() == self.dates[1]:
            event.widget.delete(0, END)

    # Computes the first day of the last month given today's date for the start date.
    # Computes the last saturday of the final week of the last month given today's date for the end date. If the last week runs into the next month that is fine.
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

    # Checks the inputted dates in the start date and end date entry fields, sends a warning message if a incorrect date format is found
    def check_dates(self, date_config):
        for idx, i in enumerate(date_config):
            if idx == 2 or idx == 5:
                try:
                    if i != "/":
                        messagebox.showwarning(title="Lottery Information Downloader",
                                               message="Please type a correct date in the format day/month/year - 00/00/0000")
                        break
                except:
                    messagebox.showwarning(title="Lottery Information Downloader",
                                           message="Please type a correct date in the format day/month/year - 00/00/0000")
                    break
            else:
                try:
                    if not (isinstance(int(i), int)):
                        messagebox.showwarning(title="Lottery Information Downloader",
                                               message="Please type a correct date in the format day/month/year - 00/00/0000")
                        break
                except:
                    messagebox.showwarning(title="Lottery Information Downloader",
                                           message="Please type a correct date in the format day/month/year - 00/00/0000")
                    break

    # The loop that goes through the data frame and uses the data to call the auto_download function to download the csv files for the clients.
    def loop(self, path, df, date_start, date_end, master, single=""):
        msg = 0
        self.error_count = 0
        self.end_loop = 1
        if single == "":
            # Hard coded range for now.
            for i in range(len(df["USERNAME"])):
                if self.end_loop:
                    user_name = df["USERNAME"][i].strip()
                    password = df["PASSWORD"][i].strip()
                    retailer_num = str(df["RETAILER NUMBER"][i]).strip()
                    folder = df["COMPANY"][i].strip()
                    try:
                        auto_download(user_name, password, path, folder,
                                      retailer_num, date_start, date_end)
                        msg = 1
                    except:
                        msg = 0
                        self.errors_list.append(
                            "ERROR in: " + str(df["COMPANY"][i]))
        else:
            for i in range(len(df["COMPANY"])):
                if self.end_loop:
                    if single == df["COMPANY"][i].strip():
                        user_name = df["USERNAME"][i].strip()
                        password = df["PASSWORD"][i].strip()
                        retailer_num = str(df["RETAILER NUMBER"][i]).strip()
                        folder = df["COMPANY"][i].strip()
                        try:

                            auto_download(user_name, password, path, folder,
                                          retailer_num, date_start, date_end)
                            msg = 1
                        except:
                            msg = 0
                            self.errors_list.append(
                                "ERROR in: "+str(df["COMPANY"][i]))

        # Creates the fields inside the error tab if there are any errors and enables the error button to be clickable
        # If the program is run again without closing the entire interface the error tab is updated if any new errors are found
        if len(self.errors_list):
            self.temp_frame = ttk.Frame(self.error_tab, relief=FLAT)
            self.temp_frame.grid(row=self.error_count)
            for i in range(len(self.errors_list)):
                text = self.errors_list[i]

                self.error_text = ttk.Label(self.temp_frame, text=text)
                self.error_text.grid(row=i)
            self.mainScreenBtn = ttk.Button(self.temp_frame, text="Back to Main Screen",
                                            command=self.main_sel)
            self.mainScreenBtn.grid(row=len(self.errors_list))
            self.error_button.config(state='normal')

        # Reenabling the start button once program is done with all or single if we wish to do more downloads
        self.button.config(state='normal')
        self._exit = 0  # used for ending the webdriver at anytime

        # Shows the completion or error message
        if msg:
            messagebox.showinfo(
                title="Lottery Information Downloader", message="Program Completed Successfully!")
        else:
            messagebox.showwarning(
                title="Lottery Information Downloader", message="An ERROR OCCURED!")

    # Exits the web driver if we are in the middle of downloading and exits the GUI depending on the conditions.
    def exit_GUI(self, master, end=0):
        if end:
            master.destroy()
        if self._exit:
            driver.close()
            # End the for loops in the self.loop function to end the auto downloader for all or single
            self.end_loop = 0

    # Select the main tab in the notebook window
    # Delete the selected frame in the notebook - Used with the help tab in the notebook due to its different size
    def main_sel(self, hid=0):
        if hid:
            for item in self.tabs.winfo_children():
                if str(item) == self.tabs.select():
                    item.destroy()
                    break
        self.tabs.select(0)

    # Select error tab
    def error_sel(self):
        self.tabs.select(1)

    # Creates the help tab and adds it as the third notebook tab
    # Then selects the help tab.
    def help_sel(self):
        self.help_tab = ttk.Frame(self.tabs, relief=FLAT)
        self.tabs.add(self.help_tab)
        text = Text(self.help_tab, width=76, height=20, wrap=WORD)
        text.grid(row=0)
        self.scroll = ttk.Scrollbar(
            self.help_tab, orient=VERTICAL, command=text.yview)
        self.scroll.grid(row=0, column=1, sticky='ns')
        text.config(font=("Arial", 13), padx=25)
        text['yscrollcommand'] = self.scroll.set
        text.insert('1.0',

                    """This automated script retrieves pack inventory, packs activated, and statement summaries \nfor a given amount of time from the Texas Retailer Lottery Website. 
        \nHow to use the Lottery Information Downloader:
        \n1. Select the excel file with all the client(s) information.
        \n    Look at the dummy excel file for more information on how to setup the excel file.
        \n2. Select the download folder where you would like the lottery files.
        \n    A folder with the retailer name is created in the directory chosen with the downloaded \n    lottery files inside.
        \n3. Enter Start and End date in the month/day/year or 00/00/0000 format.
        \n    Note: If you click the entry fields for the dates the placeholder dates will be removed.
        \n4. Click the Start Button to begin the automatic download. 
        \n5. Once completed a pop up message will appear that will inform you that the program is   
        \n    complete. Click the Exit button to end the entire program.
        \n\nInformation on each Button:
        \n - Start Button  = Start the Automatic Downloader. 
        \n                         Clickable once all the appropriate fields are filled in.
        \n - End Button   = End the Automatic Downloader at anytime without closing the interface. 
        \n                         Can view errors if there are any.
        \n - Help Button  = Recieve Information about the Program. 
        \n - Error Button = Clickable when there is an error. Otherwise no error was found. 
        \n - Exit Button   = Exit the downloader and interface. 
        \n                        Cannot view errors if there are any.
        """)
        text.config(state="disable")
        ttk.Button(self.help_tab, text="Back to Main Screen",
                   command=lambda: self.main_sel(1)).grid(row=1, column=0)
        self.tabs.select(2)


# Main Loop
def main():
    root = Tk()
    DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
