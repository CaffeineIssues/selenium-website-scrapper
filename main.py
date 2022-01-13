from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import pandas as pd
import time
import csv


#chrome driver manager to automatically install and find the chromedriver.exe
driver = webdriver.Chrome(ChromeDriverManager().install())
#makes sure that the page is loaded before doing anything
driver.implicitly_wait(5)
#your url
driver.get("http://yoururlhere")

#The next line is an assertion to confirm that title is correct
assert "websitetitlehere" in driver.title

#the next lines are used if you need to login on the website you are trying to scrap

#finds the username input by name
username = driver.find_element(By.NAME,'usernameinput')
username.clear()
username.send_keys("username")

#finds the userpassword input by name
password = driver.find_element(By.NAME,'userpasswordinput')
password.clear()
password.send_keys("password")

#finds the submit button and uses the click() function to click on it and submit the form
driver.find_element(By.NAME,'submitbutton').click()

#make sure to use the clear() function to clear any placeholders

#get the default/dashboard/index page
#in this case i'm using a .net website as example
driver.get("http://yoururlhere/default.aspx")
#maximizes the browser window
driver.maximize_window()

#from now on you start scrapping
#for .net websites you usually got a website split on frames

#we use driver.switch_to.frame() to switch between frames then driver.switch_to.default_content() if you need to switch back to the main page.

# to find elements on the page we use the following syntax
# variable = driver.find_element(BY.PARAMETER, '') where PARAMETER can be ID, NAME, CSS selector and other elements
# use .click() to mark checkboxes and click on buttons

#heres an example of something that took me a bit of research to figure out
#in this case we got a .net page with multiple frames and some filters that when selected generate a table which at end we export as csv

#switch to the filter frame
driver.switch_to.frame("framenamehere1")
#finds a combobox
stime = driver.find_element(By.ID,'comboboxidhere')

#as the object in question is a combobox we need to use select_object to select an option
select_object = Select(stime)

#we use select_object.select_by_value('parameter') to select an option by value we can also use select_by_index
select_object.select_by_value('comboboxvalue')

#getting back to main content
driver.switch_to.default_content()

#switching to another frame which has a second type of filter with checkbox as input
driver.switch_to.frame("framenamehere2")
schkall = driver.find_element(By.ID, 'checkboxidhere').click()
#switching back to main content
driver.switch_to.default_content()
#switching back to the first frame to click on the submit button
driver.switch_to.frame("framenamehere1")
#clicks on submit button    
btnR = driver.find_element(By.ID,'submitbuttonidhere').click()
#switch back to main content
driver.switch_to.default_content()
#switch to the frame that nests the html table
driver.switch_to.frame("bodyframe")
#here we use BeautifulSoup to grab all the tables in the frame
soup = BS(driver.page_source, 'lxml')
tables = soup.find_all('table')
#dfs will be a list of the tables we got using BS and we use the following pandas function to convert it into a dataframe
dfs = pd.read_html(str(tables))
## as we only have 1 table on this page we can print(dfs[0]) and see it on console
#if you need to drop a row from the dataframe you can use the iloc function
#on my case i needed to drop the first row of my dataframe so i did:
finaltable = dfs[0].iloc[1:]
#to finish we use to_csv to save the dataframe as csv
finaltable.to_csv('myfile.csv', sep=',', encoding='utf-8')

#check pandas documentation for more on iloc and to_csv functions





