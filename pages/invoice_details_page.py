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
    CALENDAR_DAY = (By.XPATH, "//a[contains(@class, '_720kb-datepicker-calendar-day')]")
    NEXT_MONTH_BUTTON = (By.XPATH, "//a[@title='Next']")
    PREV_MONTH_BUTTON = (By.XPATH, "//a[@title='Prev']")
    CURRENT_MONTH_YEAR = (By.CLASS_NAME, "_720kb-datepicker-calendar-header-middle")
    YEAR_DROPDOWN = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar-header-middle')]//a")
    YEAR_OPTION = (By.XPATH, "//a[contains(@ng-click, 'setNewYear') and text()='{}']")
    # TODAY_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Today')]]")

    def select_date(self, target_date):
        """Helper method to select a date from the calendar"""
        target_month = target_date.strftime("%B")
        target_year = target_date.strftime("%Y")
        target_day = str(target_date.day)

        print(f"Attempting to select date: {target_date.strftime('%m/%d/%Y')}")

        # Wait for calendar header to be visible
        current_month_year = self.wait.until(
            EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
        ).text.split()
        current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
        print(f"Current calendar shows: {current_calendar_date.strftime('%m/%d/%Y')}")

        # If year is different, change it first
        if current_calendar_date.year != target_year:
            print(f"Changing year from {current_calendar_date.year} to {target_year}")
            # Click year dropdown
            year_dropdown = self.wait.until(
                EC.element_to_be_clickable(self.YEAR_DROPDOWN)
            )
            self.driver.execute_script("arguments[0].click();", year_dropdown)
            print("Clicked year dropdown")

            # Select target year
            year_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@ng-click, 'setNewYear') and text()='{target_year}']"))
            )
            self.driver.execute_script("arguments[0].click();", year_option)
            print(f"Selected year: {target_year}")
            time.sleep(0.5)  # Small delay for calendar update

        # Now navigate months if needed
        current_month_year = self.wait.until(
            EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
        ).text.split()
        
        while current_calendar_date.month != target_date.month:
            if current_calendar_date < target_date:
                print(f"Moving forward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_MONTH_BUTTON))
                self.driver.execute_script("arguments[0].click();", next_button)
            else:
                print(f"Moving backward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                prev_button = self.wait.until(EC.element_to_be_clickable(self.PREV_MONTH_BUTTON))
                self.driver.execute_script("arguments[0].click();", prev_button)
            time.sleep(0.5)
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")

        # Select the day
        print(f"Looking for day: {target_day}")
        calendar_days = self.wait.until(
            EC.presence_of_all_elements_located(self.CALENDAR_DAY)
        )
        for day in calendar_days:
            if day.text == target_day and '_720kb-datepicker-disabled' not in day.get_attribute('class'):
                self.driver.execute_script("arguments[0].click();", day)
                print(f"Selected day: {target_day}")
                break

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
        # print("\nSetting TO date to today...")
        # to_calendar_icon = self.wait.until(
        #     EC.element_to_be_clickable(self.TO_DATE_CALENDAR_ICON)
        # )
        # self.driver.execute_script("arguments[0].click();", to_calendar_icon)
        
        # today_button = self.wait.until(
        #     EC.element_to_be_clickable(self.TODAY_BUTTON)
        # )
        # self.driver.execute_script("arguments[0].click();", today_button)
        # time.sleep(2)

        # Click Apply button
        apply_button = self.wait.until(
            EC.element_to_be_clickable(self.APPLY_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", apply_button)

        

