from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from config.settings import DEFAULT_SLEEP_TIME
import time
import logging

logger = logging.getLogger(__name__)

class DatePicker:
    def __init__(self, driver, wait, date_input_ids=None):
        self.driver = driver
        self.wait = wait
        
        # Default IDs (for invoice details page)
        self.from_date_id = "from-date"
        self.to_date_id = "to-date"
        
        # Override IDs if provided (for liabilities page)
        if date_input_ids:
            self.from_date_id = date_input_ids.get('from_date', 'from-date')
            self.to_date_id = date_input_ids.get('to_date', 'to-date')
    
    @property
    def FROM_DATE_CALENDAR_ICON(self):
        return (By.XPATH, f"//input[@id='{self.from_date_id}']/following-sibling::span[@class='calendar-icon']")
    
    @property
    def TO_DATE_CALENDAR_ICON(self):
        return (By.XPATH, f"//input[@id='{self.to_date_id}']/following-sibling::span[@class='calendar-icon']")
    
    # Calendar navigation locators (these remain static)
    CALENDAR_DAY = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@class, '_720kb-datepicker-calendar-day') and not(contains(@class, '_720kb-datepicker-disabled'))]")
    NEXT_MONTH_BUTTON = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[@title='Next']")
    PREV_MONTH_BUTTON = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[@title='Prev']")
    CURRENT_MONTH_YEAR = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//div[contains(@class, '_720kb-datepicker-calendar-header-middle')]")
    YEAR_DROPDOWN = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//div[contains(@class, '_720kb-datepicker-calendar-header-middle')]//a")
    YEAR_OPTION = (By.XPATH, "//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@ng-click, 'setNewYear') and text()='{}']")

    def select_date(self, target_date):
        """Select a specific date from the calendar"""
        target_month = target_date.strftime("%B")
        target_year = target_date.strftime("%Y")
        target_day = str(target_date.day)

        try:
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")

            # Change year if needed
            if current_calendar_date.year != target_date.year:
                year_dropdown = self.wait.until(
                    EC.element_to_be_clickable(self.YEAR_DROPDOWN)
                )
                self.driver.execute_script("arguments[0].click();", year_dropdown)
                time.sleep(1)

                year_xpath = f"//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@ng-click, 'setNewYear') and normalize-space(text())='{target_year}']"
                year_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, year_xpath))
                )
                self.driver.execute_script("arguments[0].click();", year_option)
                time.sleep(1)

            # Navigate months if needed
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
            
            while current_calendar_date.month != target_date.month:
                if current_calendar_date < target_date:
                    next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", next_button)
                else:
                    prev_button = self.wait.until(EC.element_to_be_clickable(self.PREV_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", prev_button)
                time.sleep(1)
                current_month_year = self.wait.until(
                    EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
                ).text.split()
                current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")

            # Select the day
            calendar_days = self.wait.until(
                EC.presence_of_all_elements_located(self.CALENDAR_DAY)
            )
            for day in calendar_days:
                if day.text == target_day and '_720kb-datepicker-disabled' not in day.get_attribute('class'):
                    self.driver.execute_script("arguments[0].click();", day)
                    break

        except Exception as e:
            logger.error(f"Error selecting date: {str(e)}")
            raise

    def set_date_range(self, start_date, end_date):
        """Set the date range without applying/searching"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%m/%d/%Y")

        # Add sleep before clicking calendar icons
        time.sleep(DEFAULT_SLEEP_TIME)

        # Select start date
        from_calendar_icon = self.wait.until(
            EC.element_to_be_clickable(self.FROM_DATE_CALENDAR_ICON)
        )
        self.driver.execute_script("arguments[0].click();", from_calendar_icon)
        self.select_date(start_date)

        time.sleep(DEFAULT_SLEEP_TIME)  # Add sleep between date selections

        # Select end date
        to_calendar_icon = self.wait.until(
            EC.element_to_be_clickable(self.TO_DATE_CALENDAR_ICON)
        )
        self.driver.execute_script("arguments[0].click();", to_calendar_icon)
        self.select_date(end_date)
