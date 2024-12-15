from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .components.side_menu import SideMenu
from datetime import datetime
import time

class InvoiceDetailsPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)

    # Locators
    FROM_DATE_INPUT = (By.ID, "from-date")
    TO_DATE_INPUT = (By.ID, "to-date")
    APPLY_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Apply')]]")

    FROM_DATE_CALENDAR_ICON = (By.XPATH, "//input[@id='from-date']/following-sibling::span[@class='calendar-icon']")
    TO_DATE_CALENDAR_ICON = (By.XPATH, "//input[@id='to-date']/following-sibling::span[@class='calendar-icon']")
    
    CALENDAR_DAY = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@class, '_720kb-datepicker-calendar-day') and not(contains(@class, '_720kb-datepicker-disabled'))]")
    NEXT_MONTH_BUTTON = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[@title='Next']")
    PREV_MONTH_BUTTON = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[@title='Prev']")
    CURRENT_MONTH_YEAR = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//div[contains(@class, '_720kb-datepicker-calendar-header-middle')]")
    YEAR_DROPDOWN = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//div[contains(@class, '_720kb-datepicker-calendar-header-middle')]//a")
    YEAR_OPTION = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@ng-click, 'setNewYear') and text()='{}']")
    # Update the TODAY_BUTTON locator to be specific to the active calendar
    TODAY_BUTTON = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and .//div[contains(@class, '_720kb-datepicker-calendar-month')][contains(text(), 'December')]]//button[contains(@class, 'rw-button--contained')][.//ng-transclude[text()='Today']]")
    
    # Download related locators
    DOWNLOAD_BUTTONS = (By.XPATH, "//tbody//tr//td[not(contains(@class, 'collapse-cell'))]//button[contains(@class, 'rw-button--outlined')]//i[contains(@class, 'fa-download')]/..")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")
    
    def select_date(self, target_date):
        """Helper method to select a date from the calendar"""
        target_month = target_date.strftime("%B")
        target_year = target_date.strftime("%Y")
        target_day = str(target_date.day)

        print(f"Attempting to select date: {target_date.strftime('%m/%d/%Y')}")

        try:
            # Wait for calendar header to be visible
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
            print(f"Current calendar shows: {current_calendar_date.strftime('%m/%d/%Y')}")

            # If year is different, change it first
            if current_calendar_date.year != target_date.year:
                print(f"Changing year from {current_calendar_date.year} to {target_year}")
                # Click year dropdown
                year_dropdown = self.wait.until(
                    EC.element_to_be_clickable(self.YEAR_DROPDOWN)
                )
                self.driver.execute_script("arguments[0].click();", year_dropdown)
                print("Clicked year dropdown")

                time.sleep(1)  # Add small delay for dropdown to fully open

                # Select target year
                year_xpath = f"//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@ng-click, 'setNewYear') and normalize-space(text())='{target_year}']"
                year_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, year_xpath))
                )
                print(f"Found year option: {target_year}")
                self.driver.execute_script("arguments[0].click();", year_option)
                print(f"Selected year: {target_year}")
                time.sleep(1)  # Small delay for calendar update

            # Now navigate months if needed
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
            
            while current_calendar_date.month != target_date.month:
                if current_calendar_date < target_date:
                    print(f"Moving forward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                    next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", next_button)
                else:
                    print(f"Moving backward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                    prev_button = self.wait.until(EC.element_to_be_clickable(self.PREV_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", prev_button)
                time.sleep(1)
                current_month_year = self.wait.until(
                    EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
                ).text.split()
                current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")

            # Select the day
            print(f"Looking for day: {target_day}")
            calendar_days = self.wait.until(
                EC.presence_of_all_elements_located(self.CALENDAR_DAY)
            )
            day_found = False
            for day in calendar_days:
                if day.text == target_day and '_720kb-datepicker-disabled' not in day.get_attribute('class'):
                    self.driver.execute_script("arguments[0].click();", day)
                    print(f"Selected day: {target_day}")
                    day_found = True
                    break
            
            if not day_found:
                print(f"Warning: Day {target_day} not found or not clickable")
                print("Available days:", [day.text for day in calendar_days])

        except Exception as e:
            print(f"Error during date selection: {str(e)}")
            raise

    def set_date_range(self, start_date, end_date):
        """
        Set the date range for invoice details using the calendar picker.
        
        Args:
            start_date (str or datetime): Start date in 'MM/DD/YYYY' format or datetime object
            end_date (str or datetime): End date in 'MM/DD/YYYY' format or datetime object
        """
        # Convert string dates to datetime if needed
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%m/%d/%Y")

        # Select start date
        print("\nSetting FROM date...")
        from_calendar_icon = self.wait.until(
            EC.element_to_be_clickable(self.FROM_DATE_CALENDAR_ICON)
        )
        self.driver.execute_script("arguments[0].click();", from_calendar_icon)
        self.select_date(start_date)

        # Small delay between date selections
        time.sleep(2)

        # For end date, use Today button
        print("\nSetting TO date...")
        to_calendar_icon = self.wait.until(
            EC.element_to_be_clickable(self.TO_DATE_CALENDAR_ICON)
        )
        self.driver.execute_script("arguments[0].click();", to_calendar_icon)
        self.select_date(end_date)


        # today_button = self.wait.until(
        #     EC.element_to_be_clickable(self.TODAY_BUTTON)
        # )
        # self.driver.execute_script("arguments[0].click();", today_button)
        time.sleep(2)

        # Click Apply button
        apply_button = self.wait.until(
            EC.element_to_be_clickable(self.APPLY_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", apply_button)


    def has_no_results(self):
        """
        Check if the 'no results' message is displayed.
        
        Returns:
            bool: True if no results are found, False otherwise
        """
        try:
            # Look for the 'no results' div without ng-hide class
            no_results_locator = (By.XPATH, "//div[contains(@class, 'md-table-body') and not(contains(@class, 'ng-hide'))]//div[contains(@class, 'no-data')]")
            
            # Wait a short time for the element to be visible
            no_results_element = self.wait.until(
                EC.visibility_of_element_located(no_results_locator)
            )
            return "Sorry, no results were found." in no_results_element.text
        except:
            return False

    def download_invoices(self):
        """Click download button for each invoice row and select CSV option"""
        # First check if there are no results
        if self.has_no_results():
            print("No results found - nothing to download")
            return False
        
        try:
            # Find all download buttons in the table
            download_buttons = self.wait.until(
                EC.presence_of_all_elements_located(self.DOWNLOAD_BUTTONS)
            )
            
            print(f"Found {len(download_buttons)} download buttons")
            
            # for i, button in enumerate(download_buttons, 1):
            #     print(f"\nProcessing download button {i}")
            #     self.driver.execute_script("arguments[0].click();", button)
            
            # #     # Wait for and click CSV option
            #     csv_option = self.wait.until(
            #         EC.element_to_be_clickable(self.CSV_DOWNLOAD_OPTION)
            #     )
            #     self.driver.execute_script("arguments[0].click();", csv_option)
            #     time.sleep(1)  # Wait between rows
            
            return True
        except Exception as e:
            print(f"Error during download process: {str(e)}")
            return False