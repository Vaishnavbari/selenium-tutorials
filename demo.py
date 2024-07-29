from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

website = 'https://www.yatra.com/'

option = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(options=option)

def web_scraping():

    try:
      print("Starting web scraping...")
      driver.get(website)

      # driver.get_screenshot_as_file("main.png") # Get screenshot for whole page 
    
      #  Start auto selection in selenium
      depart_form = driver.find_element(By.NAME , "flight_origin")  # Get depart form
      depart_form.click()
      time.sleep(2)
      
      country = input("Enter depart form") 

      depart_form_data = driver.find_elements(By.XPATH, "//div[@class='viewport']/div/div/li")

      for data in depart_form_data:

          if "delhi" in data.text.lower():
              print("Found Delhi")
              depart_form.send_keys(f"{country}")
              depart_form.send_keys(Keys.ENTER)
          
      print("start to get going to date")
      going_to  = driver.find_element(By.NAME , "flight_destination")  # Get going to 
      going_to.click()
      time.sleep(2)
      country = input("Enter going_to") 

      depart_form_data = driver.find_elements(By.XPATH, "//div[@class='viewport']/div/div/li")

      for data in depart_form_data:

          if "mumbai" in data.text.lower():
              print("Found Delhi")
              depart_form.send_keys(f"{country}")
              depart_form.send_keys(Keys.ENTER)
 
    finally:
        input("Press Enter to quit the browser...")
        driver.quit()


def main():
    
    try:
        web_scraping()  # Call the function
    except:
        print("Error occurred while scraping data. Please try again later.")

        
if __name__ == "__main__":
    main()