import os
import csv
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
WEBSITE = 'https://www.yatra.com/'
DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'tickets.csv')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_exceptions():
    def decorator(view_func):
        def wrapped_view(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                return None
        return wrapped_view
    return decorator

def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("The number cannot be negative.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

@handle_exceptions()
def get_user_inputs():
    depart_city = input("Enter depart city: ").title().strip()
    if not depart_city:
        raise ValueError("Depart city cannot be empty.")
    
    destination_city = input("Enter destination city: ").title().strip()
    if not destination_city:
        raise ValueError("Destination city cannot be empty.")
    
    departure_date = input("Enter departure date (e.g., 15/08/2024): ").strip()
    if not departure_date:
        raise ValueError("Departure date cannot be empty.")
    
    journey_date = datetime.strptime(departure_date, "%d/%m/%Y")
    if journey_date < datetime.now():
        raise ValueError("Departure date should be greater than today's date.")
    
    adult_count = get_positive_integer("Enter adult count: ")
    child_count = get_positive_integer("Enter child count: ")
    infant_count = get_positive_integer("Enter infant count: ")

    return depart_city, destination_city, journey_date, adult_count, child_count, infant_count

@handle_exceptions()
def set_location_field(driver, field_name, location):
    field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, field_name)))
    field.click()
    time.sleep(1)
    field.send_keys(location)
    time.sleep(1)
    field.send_keys(Keys.ENTER)
    logging.info(f"Location set to {location}")

@handle_exceptions()
def set_date_field(driver, field_name, formatted_date):
    field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, field_name)))
    field.click()
    time.sleep(2)
    date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//td[@data-date='{formatted_date}']")))
    date_element.click()
    time.sleep(2)
    logging.info(f"Date set to {formatted_date}")

@handle_exceptions()
def set_passenger_count(driver, adult_count, child_count, infant_count):
    if adult_count or child_count or infant_count:
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "flight_passengerBox")))
        dropdown.click()
        time.sleep(2)

        option_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'iePasenger')))
        
        if adult_count:
            adjust_passenger_count(option_div, "adult", adult_count)
        if child_count:
            adjust_passenger_count(option_div, "child", child_count)
        if infant_count:
            adjust_passenger_count(option_div, "infant", infant_count)

@handle_exceptions()
def adjust_passenger_count(option_div, passenger_type, count):
    passenger_div = option_div.find_element(By.CSS_SELECTOR, f'[data-flightagegroup="{passenger_type}"]')
    plus_button = passenger_div.find_element(By.CLASS_NAME, "ddSpinnerPlus")
    for _ in range(count):
        plus_button.click()
        time.sleep(1)
    logging.info(f"{count} {passenger_type}(s) set")

@handle_exceptions()
def toggle_checkbox(driver, checkbox_selector):
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox_selector)))
    if not checkbox.is_selected():
        checkbox.click()
        logging.info("Checkbox selected")

@handle_exceptions()
def search_flights(driver):
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BE_flight_flsearch_btn")))
    search_button.click()
    time.sleep(2)
    logging.info("Search button clicked")

@handle_exceptions()
def extract_ticket_data(driver):
    ticket_list = [["id", "ticket_provider_name", "start_station", "end_station", "start_time", "end_time", "total_travel_time", "weight_allowed"]]
    tickets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='flightItem border-shadow pr']")))
    
    for index, ticket in enumerate(tickets, start=1):
        provider_name = "Not Available"
        weight_allowed = "Not Available"
        start_time = "Not Available"
        start_station = "Not Available"
        travel_time = "Not Available"
        end_time = "Not Available"
        end_station = "Not Available"

        try:
            provider_name = ticket.find_element(By.XPATH, ".//span[@class='i-b bold']").text
        except Exception:
            logging.debug(f"Provider name not found for ticket {index}")

        try:
            weight_allowed = ticket.find_element(By.XPATH, ".//span[@class='fs-11 co2-pill']").text
        except Exception:
            logging.debug(f"Weight allowed not found for ticket {index}")
        
        try:
            start_time = ticket.find_element(By.XPATH, ".//div[@class='depart-details']/p[@class='fs-20 bold']").text
        except Exception:
            logging.debug(f"Start time not found for ticket {index}")
        
        try:
            start_station = ticket.find_element(By.XPATH, ".//div[@class='depart-details']/p[@class='fs-12 font-grey']").text
        except Exception:
            logging.debug(f"Start station not found for ticket {index}")
        
        try:
            travel_time = ticket.find_element(By.XPATH, ".//div[@class='stops-details font-lightgrey']/p").text
        except Exception:
            logging.debug(f"Travel time not found for ticket {index}")
        
        try:
            end_time = ticket.find_element(By.XPATH, ".//div[@class='arrival-details text-right']/p[2]").text
        except Exception:
            logging.debug(f"End time not found for ticket {index}")
        
        try:
            end_station = ticket.find_element(By.XPATH, ".//div[@class='arrival-details text-right']/p[4]").text
        except Exception:
            logging.debug(f"End station not found for ticket {index}")

        ticket_list.append([index, provider_name, start_station, end_station, start_time, end_time, travel_time, weight_allowed])
        logging.info(f"Ticket {index} extracted: {provider_name}, {start_station} to {end_station}")

    return ticket_list

@handle_exceptions()
def save_to_csv(data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerows(data)
    logging.info(f"Saved {len(data) - 1} tickets to {CSV_FILE}")

@handle_exceptions()
def web_scraping():
    driver = setup_driver()
    ticket_list = []

    try:
        logging.info("Starting web scraping...")
        driver.get(WEBSITE)

        depart_city, destination_city, journey_date, adult_count, child_count, infant_count = get_user_inputs()
        formatted_date = journey_date.strftime("%d/%m/%Y")

        set_location_field(driver, "flight_origin", depart_city)
        set_location_field(driver, "flight_destination", destination_city)
        set_date_field(driver, "flight_origin_date", formatted_date)
        set_passenger_count(driver, adult_count, child_count, infant_count)
        toggle_checkbox(driver, '[for="BE_flight_non_stop"]')
        search_flights(driver)
        
        ticket_list = extract_ticket_data(driver)
        save_to_csv(ticket_list)

    finally:
        input("Press Enter to quit the browser...")
        driver.quit()

def main():
    try:
        web_scraping()
    except Exception as e:
        logging.error(f"Error occurred while scraping data: {e}")

if __name__ == "__main__":
    main()
