'''
Step 4: This step merged the data from step 3 with more county level census data. 

New columns added: ageover65, collegeOrHigher, totalResidents

Years covered: 2012, 2016, 2020

Outcome: Bxxxxx.xlsx

Census data:  https://www.census.gov/data/developers/data-sets/acs-5year.html. (five year estimates data - The 2018-2022 ACS 5-Year)
'''
import requests
import pandas as pd

api_key = "Your Key"

# change the "get=NAME,B06009_004E,B06009_005E,B06009_006E&for=county:*&in=state:" part accordingly
# in this extraction, we used group B01001 and B06009
# please see their categories in original web page
url = f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B06009_004E,B06009_005E,B06009_006E&for=county:*&in=state:*&key={api_key}"

response = requests.get(url)
data = response.json()

df = pd.DataFrame(data[1:], columns=data[0])

print(df.head())

# change the name accordingly
excel_path = "2020_B06009.xlsx"
df.to_excel(excel_path, index=False)


# Basic Excel calculations and join operations were performed for summation after extractions. 
# The data accuracy was maintained.
