from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
from datetime import datetime

website = 'https://www.yatra.com/'

option = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(options=option)

def web_scraping():

    ticket_list = [["id", "ticket_prover_name", "start-station", "end_station", "start_time", "end_time", "total_tavel_time", "weight_allowed"]]
    
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
        
        adult = int(input("Enter adult count"))
        child = int(input("Enter child count"))
        infant = int(input("Enter infant count"))

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
        time.sleep(2)  

        calendar_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[@data-date='{formatted_date}']"))
        )
        calendar_date.click()
        time.sleep(2)
        print("Date set")

        # Handle events with dropdown 
        if adult or child or infant :
            dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "flight_passengerBox"))
            )
            dropdown.click()
            time.sleep(2)

            option = dropdown.find_element(By.ID, "BE_flight_passengerBox")
        
            if option.is_displayed():
                # Get plus option 
                option_div = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'iePasenger'))
                        )
                 
                if adult:                   
                    adult_plus_div = option_div.find_element(By.CSS_SELECTOR, '[data-flightagegroup="adult"]')
                    plus = adult_plus_div.find_element(By.CLASS_NAME, "ddSpinnerPlus")
                    for i in range(adult):
                        plus.click()

                if child:                   
                    child_plus_div = option_div.find_element(By.CSS_SELECTOR, '[data-flightagegroup="child"]')
                    plus = child_plus_div.find_element(By.CLASS_NAME, "ddSpinnerPlus")
                    for i in range(child):
                        plus.click()

                if infant:
                    infant_plus_div = option_div.find_element(By.CSS_SELECTOR, '[data-flightagegroup="infant"]')
                    plus = infant_plus_div.find_element(By.CLASS_NAME, "ddSpinnerPlus")
                    for i in range(infant):
                        plus.click()
                        time.sleep(2)

        # checkbox event 
        check_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[for="BE_flight_non_stop"]'))
        )
        if not check_box.is_selected():
            check_box.click()
            print("Checkbox event selected")
        
        # Search results
        search_results = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_flsearch_btn"))
        )
        search_results.click()
        time.sleep(2)  
        print("Search results clicked")

        # Book the ticket 
        available_tickets = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='result-set pr grid']/div/div[@class='flightItem border-shadow pr']"))
        )

        data = driver.find_elements(By.XPATH, "//div[@class='result-set pr grid']/div/div[@class='flightItem border-shadow pr']")
        time.sleep(2)
         
        for index, tickets in enumerate(data, start=len(ticket_list)):
            ticket_provider = tickets.find_element(By.XPATH, "//span[@class='i-b bold']")
            ticket_provider_name = ticket_provider.text if ticket_provider else "Not Available"  # ticket provider name
            weight_allowed_div = ticket_provider.find_element(By.XPATH, "//span[@class='fs-11 co2-pill']")
            weight_allowed = weight_allowed_div.text if weight_allowed_div else "Not Available"  # weight
            
            # depart details 
            depart_details = tickets.find_element(By.XPATH, "//div[@class='depart-details']/p[@class='fs-20 bold']")
            start_time = depart_details.text if depart_details else "Not Available"  # depart details
            start_station  = tickets.find_element(By.XPATH, "//div[@class='depart-details']/p[@class='fs-12 font-grey']")
            start_station_name = start_station.text if start_station else "Not Available"  # start station
            
            # Travel time
            travel_time_div = tickets.find_element(By.XPATH, "//div[@class='stops-details font-lightgrey']")
            travel_time_p = travel_time_div.find_element(By.TAG_NAME, "p")
            travel_time = travel_time_p.text if travel_time_p else "Not Available"  # travel

            # arrived details 
            arrived_details = tickets.find_elements(By.XPATH, "//div[@class='arrival-details text-right']/p")
            end_time_div = arrived_details[1]
            end_time = end_time_div.text if end_time_div else "Not Available"  # end
            end_station_div = arrived_details[3]

            end_station_name = end_station_div.text if end_station_div else "Not Available"

            print(f"Ticket provider: {ticket_provider_name}")
            print(f"Weight allowed: {weight_allowed}")
            print(f"Depart details: {start_time} {start_station_name}")
            print(f"Travel time: {travel_time}")
            print(f"Arrived details: {end_time} {end_station_name}")

            ticket_list.append(
               [index, ticket_provider_name, start_station_name, end_station_name, start_time, end_time, travel_time, weight_allowed]
            )

        # Save data to CSV
        if not os.path.exists('data'):
            os.makedirs('data')

        # Append data to CSV file
        with open('data/tickets.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(ticket_list)
        
        print(f"Saved all available tickets to CSV.")

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
