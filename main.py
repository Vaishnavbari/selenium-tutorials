from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os

website = 'https://www.yatra.com/'

option = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(options=option)

def web_scraping():

    try:
      pass

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