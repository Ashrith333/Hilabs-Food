from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

USERNAME = "0467"  # Replace with your username
PASSWORD = "1908199"  # Replace with your password

# Set up the Chrome driver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    driver.get("https://khanakhazana.hilabs.com/")

    wait = WebDriverWait(driver, 20)
    try:
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "userId")))
        password_input = driver.find_element(By.NAME, "password")
    except Exception as e:
        print("Could not find username/password fields. Printing page source for debugging:")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved to page_source.html. Please inspect this file to find the correct field names or structure.")
        raise e

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_button.click()

    # Wait for dashboard to load
    time.sleep(5)

    # --- ORDERING ACTIONS ---
    # 1. Click 'Non Veg' for Lunch (if enabled)
    try:
        lunch_nonveg_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[contains(translate(text(), 'LUNCH', 'lunch'), 'lunch')]/following::span[contains(text(), 'Non Veg')][1]/parent::div[not(contains(@class, 'Mui-disabled'))]"
        )))
        lunch_nonveg_btn.click()
        print("Clicked 'Non Veg' for Lunch.")
        time.sleep(1)
    except Exception as e:
        print("Could not click 'Non Veg' for Lunch (maybe already ordered or disabled):", e)

    # 2. Click 'Non Veg' for Dinner (if enabled)
    try:
        dinner_nonveg_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[contains(translate(text(), 'DINNER', 'dinner'), 'dinner')]/following::span[contains(text(), 'Non Veg')][1]/parent::div[not(contains(@class, 'Mui-disabled'))]"
        )))
        dinner_nonveg_btn.click()
        print("Clicked 'Non Veg' for Dinner.")
        time.sleep(1)
    except Exception as e:
        print("Could not click 'Non Veg' for Dinner (maybe already ordered or disabled):", e)

    # 3. Click '+ Add' for Snacks
    try:
        snacks_add_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[translate(normalize-space(text()), 'SNACKS', 'snacks')='snacks']/following::span[text()='+ Add'][1]/parent::div[@tabindex='0']"
        )))
        snacks_add_btn.click()
        print("Clicked '+ Add' for Snacks.")
        time.sleep(1)
    except Exception as e:
        print("Could not click '+ Add' for Snacks (maybe already added):", e)

    # 4. Click 'Confirm Order' button
    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//text()[contains(.,'Confirm Order')]]"
        )))
        confirm_btn.click()
        print("Clicked 'Confirm Order' button.")
    except Exception as e:
        print("Could not click 'Confirm Order' button:", e)

    print("Order actions attempted. Please verify on the site.")

finally:
    time.sleep(5)
    driver.quit() 