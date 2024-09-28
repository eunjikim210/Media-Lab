from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

df = pd.read_csv('libraryZip/filtered_data.csv')

# Set the path for geckodriver.exe
geckodriver_path = './geckodriver-v0.34.0-win64/geckodriver.exe'
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service)

# Set a longer wait time to ensure the page loads
wait = WebDriverWait(driver, 10)

# Iterate through the first 10 rows of the DataFrame
for index, row in df.iloc[0:10].iterrows():
    driver.get('https://www.google.com/maps')
    sleep(2)

    try:
        # Search for the address
        search_box = wait.until(EC.element_to_be_clickable((By.ID, 'searchboxinput')))
        search_box.clear()
        search_box.send_keys(row['Address'])
        search_box.send_keys(Keys.ENTER)
        sleep(3)  # Wait for search results to load

        try:
            # Try to extract the zip code
            zip_code_element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div/div[2]/div[1]')))
            zip_code = zip_code_element.text
            df.at[index, 'zip'] = zip_code

        except (TimeoutException, NoSuchElementException):
            try:
                # If the zip code is not found, click the first address in the search results
                first_result = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.w6Uhzf > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)')))
                first_result.click()

                # Try to extract the zip code again
                zip_code_element = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'Io6YTe') and contains(@class, 'fontBodyMedium') and contains(@class, 'kR99db')]")))
                zip_code = zip_code_element.text
                df.at[index, 'zip'] = zip_code

            except (TimeoutException, NoSuchElementException):
                try:
                    # Try clicking the next button if still not found
                    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.hfpxzc')))
                    next_button.click()

                    # Try to extract the zip code again
                    zip_code_element = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'Io6YTe') and contains(@class, 'fontBodyMedium') and contains(@class, 'kR99db')]")))
                    zip_code = zip_code_element.text
                    df.at[index, 'zip'] = zip_code

                except Exception as e:
                    print(f"Error extracting zip code for address: {row['Address']} after all attempts. Error: {e}")

    except Exception as e:
        print(f"Error processing address: {row['Address']}. Error: {e}")

df.to_excel('libraryZip/aaa.xlsx', index=False)

# Close the browser
driver.quit()
