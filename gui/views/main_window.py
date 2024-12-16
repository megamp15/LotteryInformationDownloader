import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

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

        # Excel file selection
        ttk.Label(file_frame, text="Excel File:").grid(row=0, column=0, padx=5, pady=5)
        self.excel_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.excel_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_excel).grid(row=0, column=2, padx=5)

        # Download directory selection
        ttk.Label(file_frame, text="Download Dir:").grid(row=1, column=0, padx=5, pady=5)
        self.download_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.download_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_dir).grid(row=1, column=2, padx=5)

    def create_date_frame(self):
        date_frame = ttk.LabelFrame(self, text="Date Range")
        date_frame.pack(fill="x", padx=5, pady=5)

        # Start date
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = tk.StringVar(value="MM/DD/YYYY")
        ttk.Entry(date_frame, textvariable=self.start_date).grid(row=0, column=1, padx=5)

        # End date
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = tk.StringVar(value="MM/DD/YYYY")
        ttk.Entry(date_frame, textvariable=self.end_date).grid(row=0, column=3, padx=5)

    def create_action_frame(self):
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=5, pady=5)

        # Action buttons
        ttk.Button(action_frame, text="Start Download", command=self.start_download).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Stop", command=self.stop_download).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Help", command=self.show_help).pack(side="right", padx=5)

    def create_status_frame(self):
        status_frame = ttk.LabelFrame(self, text="Status")
        status_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Status text
        self.status_text = tk.Text(status_frame, height=10, width=60)
        self.status_text.pack(padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
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
                self.end_date.get()
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
        # Add more validation as needed
        return True

    def update_status(self, message):
        self.status_text.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see("end") 