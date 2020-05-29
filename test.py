# import os

# def config_filePath():
#     cur = os.getcwd()
#     Lottery_dir = cur + "\\" + "Lottery"
#     filelist = os.listdir(Lottery_dir)
#     return cur, Lottery_dir, filelist


# def create_folder(Lottery_dir, retailer_name, date_start):
#     Month = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR", "05": "MAY", "06": "JUN",
#              "07": "JUL", "08": "AUG", "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}
#     path = Lottery_dir+"\\"+retailer_name+"\\" + \
#         Month[date_start[:2]]+"-"+date_start[6:]
#     os.mkdir(path)


# data = config_filePath()
# create_folder(data[1], "NB - Springtime", "05/01/2019")


# from tkinter import *
# from tkinter import ttk


# class downloaderGUI:

#     def __init__(self, master):
#         self.file_frame = ttk.Frame(master)
#         ttk.Label(self.file_frame, text="Enter Excel File and Folder details.")
#         ttk.Label(self.file_frame, text="Select the Excel File")
#         ttk.Label(self.file_frame, text="Select Download Folder:")


# def main():
#     root = Tk()
#     GUI = downloaderGUI(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()

# root = Tk()
# root.title('Lottery Information Downloader')

# file_frame = ttk.Frame(root, relief=GROOVE)
# file_frame.grid(row=0)

# l1 = ttk.Label(file_frame, text="Select Excel File: ")
# l1.grid(row=0, column=0, sticky="W", padx=(5, 0), pady=(20, 0))

# e1 = ttk.Entry(file_frame, width=50)
# e1.grid(row=0, column=1, columnspan=4, sticky="NSEW", pady=(20, 0))

# b1 = ttk.Button(file_frame, text="Browse")
# b1.grid(row=0, column=5, sticky="NSEW", padx=5, pady=(20, 0))


# l2 = ttk.Label(file_frame, text="Select Download Folder: ")
# l2.grid(row=1, column=0, sticky="W", padx=5, pady=(0, 20))

# e2 = ttk.Entry(file_frame, width=50)
# e2.grid(row=1, column=1, columnspan=4, sticky="NSEW", pady=(0, 20))

# b2 = ttk.Button(file_frame, text="Browse")
# b2.grid(row=1, column=5, sticky="NSEW", padx=5, pady=(0, 20))

# date_frame = ttk.Frame(root, relief=GROOVE)
# date_frame.grid(row=1)
# l3 = ttk.Label(date_frame, text="Start Date: ")
# l3.grid(row=0, column=0, sticky="E", padx=(75, 0), pady=10)

# e3 = ttk.Entry(date_frame, width=20)
# e3.grid(row=0, column=1, sticky="W", padx=(0, 15), pady=10)

# l4 = ttk.Label(date_frame, text="End Date: ")
# l4.grid(row=0, column=2, sticky="E", pady=10)

# e4 = ttk.Entry(date_frame, width=20)
# e4.grid(row=0, column=3, sticky="W", padx=(0, 76), pady=10)

# sel_frame = ttk.Frame(root, relief=GROOVE)
# sel_frame.grid(row=2)

# l5 = ttk.Label(sel_frame, text="Select download type:")
# l5.grid(row=0, sticky="E", padx=(137, 0), pady=10)

# type_DL = StringVar()
# combobox1 = ttk.Combobox(sel_frame, textvariable=type_DL)
# combobox1.grid(row=0, column=1, sticky="W", padx=(0, 137), pady=10)
# combobox1.config(values=('ALL', 'SINGLE'))

# start_frame = ttk.Frame(root, relief=GROOVE)
# start_frame.grid(row=3)

# button = ttk.Button(start_frame, text="START")
# button.grid(row=0, padx=230, pady=10)


# root.mainloop()
# from dateutil.relativedelta import relativedelta, FR
# from datetime import date, timedelta
# # d = date.today()
# # td = timedelta(days=d.day-1)
# # first_day = d-td

# # td2 = timedelta(days=31-d.day)
# # last_day = d+td2
# # while ((last_day).month != d.month):
# #     last_day -= timedelta(days=1)

# # # print(first_day)
# # # print(last_day)

# d = date.today()-relativedelta(months=1)
# # d = date(2020, 12, 13)-relativedelta(months=1)

# first_day = d-relativedelta(days=d.day-1)
# print(first_day)
# print("{0}/{1}/{2}".format(str(first_day.month).zfill(2), str(first_day.day).zfill(2), first_day.year))

# temp_d= d+relativedelta(day=31, weekday=FR(-1))+relativedelta(weeks=1, days=1)
# if temp_d.day != 7:
#     last_day = d+relativedelta(day=31, weekday=FR(-1)) + \
#         relativedelta(weeks=1, days=1)
# else:
#     last_day = d+relativedelta(day=31, weekday=FR(-1))+ \
#         relativedelta(days=1)
# print(last_day)
# print("{0}/{1}/{2}".format(str(last_day.month).zfill(2), str(last_day.day).zfill(2), last_day.year))

# from fake_useragent import UserAgent
# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)
