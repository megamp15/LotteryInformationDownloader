from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_lottery_site():
    # Configure Chrome options
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create Chrome driver instance
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 120)

    try:
        driver.get("https://txs.lotteryservices.com/RetailerWizard/#/home")

        # Wait for login elements
        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "loginEmail"))
        )

        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "passwdRetailer"))
        )

        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//translate[text()='Log In']]")
            )
        )

        # Fill in login credentials and click Log In
        email_input.send_keys("mpkasar@gmail.com")
        password_input.send_keys("TX786110.")
        login_button.click()

        # Wait for the Invoice Details link on Summary Dashboard EFT Amount Widget
        invoice_details_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[.//translate[text()='Invoice Details']]")
            )
        )
        driver.execute_script("arguments[0].click();", invoice_details_link)

        # -------------------- Invoice Details Page --------------------






        # -------------------- Side Menu Buttons Below --------------------

        # scratch_dashboard_link = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/dashboard-instant/']"))
        # )
        # print('Scratch Dashboard Link: ', scratch_dashboard_link.get_attribute('outerHTML'))
        # driver.execute_script("arguments[0].click();", scratch_dashboard_link)

        # reports_link = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/reports']"))
        # )
        # print('Reports Link: ', reports_link.get_attribute('outerHTML'))
        # driver.execute_script("arguments[0].click();", reports_link)

        # Keep the browser open until user input
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_lottery_site()
