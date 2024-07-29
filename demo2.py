from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

website = 'https://www.yatra.com/'

option = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(options=option)

def web_scraping():
    try:
        print("Starting web scraping...")
        driver.get(website)

        # Depart from form
        depart_form = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "flight_origin"))
        )
        depart_form.click()
        time.sleep(2)
        
        country = "Banglore"  # Hardcoded for simplicity
        depart_form.send_keys(country)
        time.sleep(1)
        depart_form.send_keys(Keys.ENTER)
        
        print("Depart from location set")

        # Going to form
        going_to = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "flight_destination"))
        )
        going_to.click()
        time.sleep(2)
        
        destination = "mumbai"  # Hardcoded for simplicity
        going_to.send_keys(destination)
        time.sleep(1)
        going_to.send_keys(Keys.ENTER)
        
        print("Going to location set")

    finally:
        input("Press Enter to quit the browser...")
        driver.quit()

def main():
    try:
        web_scraping()  # Call the function
    except Exception as e:
        print(f"Error occurred while scraping data: {e}")

if __name__ == "__main__":
    main()
