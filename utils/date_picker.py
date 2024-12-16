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
        """Helper method to select a date from the calendar"""
        target_month = target_date.strftime("%B")
        target_year = target_date.strftime("%Y")
        target_day = str(target_date.day)

        logger.info(f"Attempting to select date: {target_date.strftime('%m/%d/%Y')}")

        try:
            # Wait for calendar header to be visible
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
            logger.info(f"Current calendar shows: {current_calendar_date.strftime('%m/%d/%Y')}")

            # If year is different, change it first
            if current_calendar_date.year != target_date.year:
                logger.info(f"Changing year from {current_calendar_date.year} to {target_year}")
                # Click year dropdown
                year_dropdown = self.wait.until(
                    EC.element_to_be_clickable(self.YEAR_DROPDOWN)
                )
                self.driver.execute_script("arguments[0].click();", year_dropdown)
                logger.info("Clicked year dropdown")

                time.sleep(1)  # Add small delay for dropdown to fully open

                # Select target year
                year_xpath = f"//div[contains(@class, '_720kb-datepicker-calendar') and contains(@class, '_720kb-datepicker-open')]//a[contains(@ng-click, 'setNewYear') and normalize-space(text())='{target_year}']"
                year_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, year_xpath))
                )
                logger.info(f"Found year option: {target_year}")
                self.driver.execute_script("arguments[0].click();", year_option)
                logger.info(f"Selected year: {target_year}")
                time.sleep(1)  # Small delay for calendar update

            # Now navigate months if needed
            current_month_year = self.wait.until(
                EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
            ).text.split()
            current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")
            
            while current_calendar_date.month != target_date.month:
                if current_calendar_date < target_date:
                    logger.info(f"Moving forward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                    next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", next_button)
                else:
                    logger.info(f"Moving backward from {current_calendar_date.strftime('%m/%d/%Y')} to reach {target_date.strftime('%m/%d/%Y')}")
                    prev_button = self.wait.until(EC.element_to_be_clickable(self.PREV_MONTH_BUTTON))
                    self.driver.execute_script("arguments[0].click();", prev_button)
                time.sleep(1)
                current_month_year = self.wait.until(
                    EC.presence_of_element_located(self.CURRENT_MONTH_YEAR)
                ).text.split()
                current_calendar_date = datetime.strptime(f"{current_month_year[0]} {current_month_year[1]}", "%B %Y")

            # Select the day
            logger.info(f"Looking for day: {target_day}")
            calendar_days = self.wait.until(
                EC.presence_of_all_elements_located(self.CALENDAR_DAY)
            )
            day_found = False
            for day in calendar_days:
                if day.text == target_day and '_720kb-datepicker-disabled' not in day.get_attribute('class'):
                    self.driver.execute_script("arguments[0].click();", day)
                    logger.info(f"Selected day: {target_day}")
                    day_found = True
                    break
            
            if not day_found:
                logger.warning(f"Day {target_day} not found or not clickable")
                logger.debug("Available days:", [day.text for day in calendar_days])

        except Exception as e:
            logger.error(f"Error during date selection: {str(e)}")
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
