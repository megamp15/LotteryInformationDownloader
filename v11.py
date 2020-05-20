from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from dateutil.relativedelta import relativedelta, FR
from datetime import date, timedelta


class DownloaderGUI:

    def __init__(self, master):
        self.entry1 = StringVar(master)
        self.entry2 = StringVar(master)
        self.entry3 = StringVar(master)
        self.entry4 = StringVar(master)
        self.sel = StringVar(master)
        self.single_retailer = StringVar(master)

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
            row=0, column=0, sticky="W", padx=(5, 0), pady=(20, 0))

        self.e1 = ttk.Entry(self.file_frame, width=50,
                            textvariable=self.entry1)
        self.e1.grid(row=0, column=1, columnspan=4,
                     sticky="NSEW", pady=(20, 0))

        self.b1 = ttk.Button(self.file_frame, text="Browse",
                             command=self.getFilePath)
        self.b1.grid(row=0, column=5, sticky="NSEW", padx=5, pady=(20, 0))

        ttk.Label(self.file_frame, text="Select Download Folder: ").grid(
            row=1, column=0, sticky="W", padx=5, pady=(0, 20))

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
            row=0, column=0, sticky="E", padx=(75, 0), pady=10)

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
        self.e4.grid(row=0, column=3, sticky="W", padx=(0, 76), pady=10)
        self.e4.bind('<1>', self.placeholder)

        self.sel_frame = ttk.Frame(master, relief=GROOVE)
        self.sel_frame.grid(row=2)

        ttk.Label(self.sel_frame, text="Select download type: ").grid(
            row=0, sticky="E", padx=(135, 0), pady=10)

        self.combobox1 = ttk.Combobox(
            self.sel_frame, textvariable=self.sel)
        self.combobox1.grid(row=0, column=1, sticky="W",
                            padx=(0, 135), pady=10)
        self.combobox1.config(values=('ALL', 'SINGLE'), state="readonly")

        self.start_frame = ttk.Frame(master, relief=GROOVE)
        self.start_frame.grid(row=3)

        self.button = ttk.Button(
            self.start_frame, text="START", command=self.getInfo, state='disabled')
        self.button.grid(row=0, padx=230, pady=10)

        self.single_frame = ttk.Frame(master, relief=GROOVE)
        self.single_frame.grid(row=4)

    def validation(self, *args):
        entry1 = self.entry1.get() != ""
        entry2 = self.entry2.get() != ""
        entry3 = self.entry3.get() != ""
        entry4 = self.entry4.get() != ""
        sel = self.sel.get() != ""
        single_retailer = self.single_retailer.get() != ""

        first_check = entry1 and entry2 and entry3 and entry4 and sel
        second_check = first_check and single_retailer

        if self.sel.get() == "SINGLE":
            self.start_frame.grid_forget()
            self.single_frame.grid(row=4)
            ttk.Label(self.single_frame, text="Select Retailer: ").grid(
                row=0, sticky="E", padx=(153, 0), pady=10)
            self.combobox2 = ttk.Combobox(
                self.single_frame, textvariable=self.single_retailer)
            self.combobox2.grid(row=0, column=1, sticky="W",
                                padx=(0, 157), pady=10)
            self.combobox2.config(values=('TEMP1', 'TEMP2'), state="readonly")
            self.start_frame.grid(row=5)
            if second_check:
                self.button.config(state='normal')
            else:
                self.button.config(state='disabled')

        if self.sel.get() == "ALL":
            self.single_frame.grid_forget()
            if first_check:
                self.button.config(state='normal')

    def getInfo(self):
        print(self.entry1.get())
        print(self.entry2.get())
        print(self.entry3.get())
        print(self.entry4.get())
        print(self.sel.get())

    def getFilePath(self):
        filename = filedialog.askopenfilename(title="Select A File", filetypes=(
            ("excel files", "*.xlsx"), ("all files", "*.*")))
        if filename != "":
            self.e1.insert(0, filename)

    def getDirPath(self):
        dirname = filedialog.askdirectory()
        if dirname != NONE:
            self.e2.insert(0, dirname)

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
    root.title('Lottery Information Downloader')
    DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
