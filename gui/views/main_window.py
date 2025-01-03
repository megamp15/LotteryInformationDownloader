import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.root = parent
        
        # Initialize StringVar variables with default dates
        default_start_date, default_end_date = self.calculate_default_dates(None)
        self.excel_path = tk.StringVar()
        self.download_path = tk.StringVar()
        self.start_date = tk.StringVar(value=default_start_date)
        self.end_date = tk.StringVar(value=default_end_date)
        self.delete_files = tk.BooleanVar()
        
        # Connect logging to status updates
        self.controller.set_status_callback(self.update_status)
        
        self.init_ui()

    def calculate_default_dates(self, date=None):
        """Calculate default start and end dates.
        Start date is first of previous month.
        End date is the first Saturday after the last day of previous month."""
        d = datetime.today() if date is None else date

        # Calculate the first day of the previous month
        start_date = d - relativedelta(months=1)
        start_date = start_date.replace(day=1)

        # Calculate the last day of the previous month
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        
        # Add days until we reach Saturday (where 5 = Saturday)
        while end_date.weekday() != 5:
            end_date += timedelta(days=1)

        first_day = "{0}/{1}/{2}".format(str(start_date.month).zfill(2), str(start_date.day).zfill(2), start_date.year)
        last_day = "{0}/{1}/{2}".format(str(end_date.month).zfill(2), str(end_date.day).zfill(2), end_date.year)
        
        return first_day, last_day

    def init_ui(self):
        # Configure styles
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))

        # Create frames
        self.create_file_frame()
        self.create_date_frame()
        self.create_action_frame()
        self.create_status_frame()

    def create_file_frame(self):
        file_frame = ttk.LabelFrame(self, text="File Settings")
        file_frame.pack(fill="x", padx=5, pady=5)

        # Excel file selection row
        excel_row = ttk.Frame(file_frame)
        excel_row.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(excel_row, text="Excel File:").pack(side="left")
        ttk.Entry(excel_row, textvariable=self.excel_path, width=50).pack(side="left", padx=5)
        ttk.Button(excel_row, text="Browse", command=self.browse_excel).pack(side="left", padx=2)
        ttk.Button(excel_row, text="Download Template", command=self.download_template).pack(side="left", padx=2)

        # Download directory selection
        dir_row = ttk.Frame(file_frame)
        dir_row.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(dir_row, text="Download Dir:").pack(side="left")
        ttk.Entry(dir_row, textvariable=self.download_path, width=50).pack(side="left", padx=5)
        ttk.Button(dir_row, text="Browse", command=self.browse_dir).pack(side="left", padx=2)

    def create_date_frame(self):
        date_frame = ttk.LabelFrame(self, text="Date Range")
        date_frame.pack(fill="x", padx=5, pady=5)

        # Start date
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(date_frame, textvariable=self.start_date).grid(row=0, column=1, padx=5)

        # End date
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(date_frame, textvariable=self.end_date).grid(row=0, column=3, padx=5)

    def create_action_frame(self):
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=5, pady=5)

        # Delete files checkbox
        ttk.Checkbutton(
            action_frame, 
            text="Delete all files in folder(s)", 
            variable=self.delete_files
        ).pack(side="left", padx=5)

        # Action buttons
        ttk.Button(
            action_frame, 
            text="Start Download", 
            command=self.start_download
        ).pack(side="left", padx=5)
        
        ttk.Button(
            action_frame, 
            text="Stop", 
            command=self.stop_download
        ).pack(side="left", padx=5)
        
        ttk.Button(
            action_frame, 
            text="Help", 
            command=self.show_help
        ).pack(side="right", padx=5)

    def create_status_frame(self):
        status_frame = ttk.LabelFrame(self, text="Status")
        status_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create a frame to hold the text widget and scrollbar
        text_frame = ttk.Frame(status_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Status text - adjust height and width
        self.status_text = tk.Text(text_frame, height=15, width=80, wrap=tk.WORD)
        self.status_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, command=self.status_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.status_text['yscrollcommand'] = scrollbar.set

    def browse_excel(self):
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filename:
            self.excel_path.set(filename)
            self.controller.on_excel_selected(filename)

    def browse_dir(self):
        dirname = filedialog.askdirectory(title="Select Download Directory")
        if dirname:
            self.download_path.set(dirname)
            self.controller.on_dir_selected(dirname)

    def start_download(self):
        if self.validate_inputs():
            self.controller.start_download(
                self.excel_path.get(),
                self.download_path.get(),
                self.start_date.get(),
                self.end_date.get(),
                self.delete_files.get()
            )

    def stop_download(self):
        self.controller.stop_download()

    def show_help(self):
        help_text = """
        Lottery Information Downloader Help:

        1. Select Excel File: Choose the Excel file containing login credentials
        2. Select Download Directory: Choose where to save downloaded files
        3. Enter date range in MM/DD/YYYY format
        4. Click Start Download to begin
        5. Use Stop button to cancel the process

        For more information, please refer to the documentation.
        """
        messagebox.showinfo("Help", help_text)

    def validate_inputs(self):
        if not self.excel_path.get():
            messagebox.showerror("Error", "Please select an Excel file")
            return False
        if not self.download_path.get():
            messagebox.showerror("Error", "Please select a download directory")
            return False
        if not self.validate_dates():
            return False
        return True

    def validate_dates(self):
        try:
            start_date = datetime.strptime(self.start_date.get(), "%m/%d/%Y")
            end_date = datetime.strptime(self.end_date.get(), "%m/%d/%Y")
            if start_date > end_date:
                messagebox.showerror("Error", "Start date must be before end date")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter dates in MM/DD/YYYY format")
            return False
        return True

    def update_status(self, message):
        """Update status text with timestamp and message"""
        self.status_text.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see("end")
        # Force update the GUI
        self.status_text.update_idletasks()

    def download_template(self):
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile="SAMPLE.xlsx",
                title="Save Template Excel File"
            )
            if save_path:
                self.controller.create_template(save_path)
                messagebox.showinfo("Success", f"Template saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save template: {str(e)}") 