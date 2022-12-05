from typing import Type
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import logging
import pickle
import os
from dotenv import load_dotenv


# Set logging level and driver paths for selenium
logging.basicConfig(level = logging.INFO, format = '%(levelname)s:%(message)s')
PATH = os.getenv("path")
driver = webdriver.Chrome(PATH)
driver.get("https://www.nrlsupercoachstats.com/combinedstats.php")

time.sleep(3) # Pause so it has time to open the webpage 

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

    
headings = WebDriverWait(driver,60,ignored_exceptions=ignored_exceptions).until(
    EC.visibility_of_element_located((By.XPATH,"/html/body/table/tbody/tr/td/div/div/div[3]/div[2]/div/table/thead/tr[1]"))
) # This will be the heading for end dataframe

first_table = WebDriverWait(driver,10,ignored_exceptions=ignored_exceptions).until(
    EC.visibility_of_element_located((By.ID,"list1"))
) # Pull the NRL stats on page 1 

# Clean Headings
out = []
buff = []
for c in headings.text.strip():
    if c == '\n':
        out.append(''.join(buff))
        buff = []
    else:
        buff.append(c)
else:
    if buff:
       out.append(''.join(buff))

heading_list = []
for i in out:
    final_string = i.lstrip()
    final_string = final_string.rstrip()
    heading_list.append(final_string)


heading_list.remove('Pow')
heading_list[27] = 'BasePow PPM'
heading_list[28] = 'Base+ Pow'
heading_list = heading_list[:-6 or None]
heading_list.pop(29)
heading_list.append('Neg Avg')
heading_list.append('Base +Pow Avg')
heading_list.append('Name')

# Function to clean and turn html table to dataframe
def clean_table(scraped_table):
    table_final_df = pd.DataFrame(pd.read_html(scraped_table.get_attribute('outerHTML'))[0])
    table_final_df = table_final_df.iloc[1:,2:].reset_index()
    table_final_df = table_final_df.drop(columns = ["index",5])
    return table_final_df


table_final_df = clean_table(first_table)

# Iterate through every page and add each loaded table to the table_final_df 
# This DF makes the full NRL data repo 

range = 1 
while range < 3614: # Amount of pages - at the time of creation there was 3614 pages however this will likely grow

    next_page = WebDriverWait(driver,10,ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_element_located((By.ID,"next_list1_pager"))
    )
    next_page.click() # Moves to next page
    table = WebDriverWait(driver,10,ignored_exceptions=ignored_exceptions).until(
                    EC.visibility_of_element_located((By.ID,"list1"))
                )
    table_df = clean_table(table)
    table_final_df = pd.concat([table_final_df,table_df],ignore_index=True)
    range+=1
    
table_final_df.columns = heading_list
# Drop last column as there is two name columns
table_final_df=table_final_df.iloc[:,:-1]

#Save to pickle
table_final_df.to_pickle("NRL_Stats.pickle")

# #Save to csv
# table_final_df.to_csv("NRL_Stats.csv")

# Close the driver
driver.quit()