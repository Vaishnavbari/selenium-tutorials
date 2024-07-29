from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

website = 'https://www.yatra.com/'

option = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(options=option)

def web_scraping():
    
    try:
        print("Starting web scraping...")
        driver.get(website)

        # Get user inputs before interacting with the browser
        depart_city = input("Enter depart city: ").title().strip()
        if not depart_city:
            print("Depart city cannot be empty.")
            return
        
        destination_city = input("Enter destination city: ").title().strip()

        if not destination_city:
            print("Destination city cannot be empty.")
            return
        
        departure_date = input("Enter departure date (e.g., 15/08/2024): ").strip()
        if not departure_date:
            print("Departure date cannot be empty.")
            return

        journey_date = datetime.strptime(departure_date, "%d/%m/%Y")
        formatted_date = journey_date.strftime("%d/%m/%Y")

        if journey_date < datetime.now():
            print("Departure date should be greater than today's date.")

        print("Formatted journey date:", journey_date)

        # Depart from
        depart_form = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "flight_origin"))
        )
        depart_form.click()
        time.sleep(1)
        depart_form.send_keys(depart_city)
        time.sleep(1)
        depart_form.send_keys(Keys.ENTER)
        print("Depart from location set")

        # Going to
        going_to = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "flight_destination"))
        )
        going_to.click()
        time.sleep(1)
        going_to.send_keys(destination_city)
        time.sleep(1)
        going_to.send_keys(Keys.ENTER)
        print("Going to location set")

        # Departure date
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "flight_origin_date"))
        )
        date_field.click()
        time.sleep(2)  # Wait for the calendar to load

        calendar_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[@data-date='{formatted_date}']"))
        )
        calendar_date.click()
        
        time.sleep(1)
        print("Date set")

        # Search results
        search_results = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_flsearch_btn"))
        )
        search_results.click()
        time.sleep(2)  # Wait for the calendar to load

        # Book the ticket 
        available_tickets = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='result-set pr grid']/div/div[@class='flightItem border-shadow pr']"))
        )

        data = driver.find_elements(By.XPATH, "//div[@class='result-set pr grid']/div/div[@class='flightItem border-shadow pr']")
        time.sleep(2)
         
        for tickets in data:
            ticket_provider = tickets.find_element(By.XPATH, "//span[@class='i-b bold']")
            ticket_provider_name = ticket_provider.text if ticket_provider else "Not Available"  # ticket provider name

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
