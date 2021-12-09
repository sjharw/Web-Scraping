############################################################################################################################################
                                                    ### JobSite WebScraper ###
############################################################################################################################################

### ---------------------------------------- THIS SCRAPER IS FOR EDUCATIONAL PURPOSES ONLY --------------------------------------------- ###

# Import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By # By.XPATH
from selenium.webdriver.common.action_chains import ActionChains # for actions such as clicking next button
from selenium.webdriver.chrome.service import Service
import pandas as pd # for dataframes
import time



class JobSiteScraper():

                        ## Connect to website ##
    def __init__(self):
# Prevent ChromeDriver from throwing error message in terminal
        self.options = webdriver.ChromeOptions() # customise ChromeDriver options
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) # code derived from: https://stackoverflow.com/questions/69441767/error-using-selenium-chrome-webdriver-with-python
# Connect to chrome driver
# If you want to connect to a different browser, see link: https://pypi.org/project/webdriver-manager/
        self.service = Service("C:/YourFilePath/chromedriver.exe") # point to chromedriver.exe
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
# Launch website
        self.driver.get('http://www.jobsite.co.uk') # launches jobsite
# Keep track of page number and create lists to store job data
        self.page_num = 1 # set counter for page to keep track of number of pages that have been scraped
        self.ids_list = [] # list to store job ids
        self.jobs_list = [] # list to store jobs text 


                        ## Search website ##
    def job_search(self):
            print("Running job search, please wait.") # lets you know automated job search has started
# Accept cookies
            time.sleep(2) # wait for cookie pop up
            self.driver.execute_script("document.getElementById('ccmgt_explicit_accept').click()")
            time.sleep(2)
# This inputs location as UK, with a mile radius of 0, into job site search bar 
            self.driver.execute_script("document.getElementById('location').value='UK'")
            time.sleep(2) # timer to delay requests
            self.driver.execute_script("document.getElementById('Radius').value='0'")
            time.sleep(2)
# Excecute job search
            self.driver.execute_script("document.getElementById('search-button').click()")
            time.sleep(3) # must be 3 seconds otherwise challenge validation page is recieved


                        ## Retrieve job IDs and extract text for each job ID ##
# Code derived from: https://www.youtube.com/watch?v=Yvt28OCzWhI
    def job_extract(self):
# Locate specific HTML element
        job_ids = self.driver.find_elements(By.XPATH, "//*[contains(@id, 'job-item')]") # search HTML for elements with job-item in their XPath and retrieve element IDs
# Extract element text using element ID
        for i in range(len(job_ids)): # for each job in list of job IDs
                self.jobs_list.append(job_ids[i].text.split('\n')) # retrieve text for job using job ID, and append this text to list, each job is a nested list within list


                        ## Extract job for each page ##
# Run a loop for extracting jobs for a specified number of pages
    def scrape(self):
            N = int(input("Please input number of pages to scrape: ")) # asks you to input number of pages you want to extract jobs from
            print("Webscraping for {} pages has started.".format(N)) # lets you know that webscraping has commenced
            self.start_time = time.time() # log start time
            for _ in range(N):
                    time.sleep(5)
                    self.action = ActionChains(self.driver) # create action chain
# Create a new next_button for each page, otherwise you get a stale element error
                    self.next_button = self.driver.find_element(by=By.XPATH, value=
                    "//a[contains(@data-at, 'pagination-next')]" # create next button containing href link to next page
                    ) 
# Extract job text from page
                    self.job_extract()
# Move to next page
                    self.actions = self.action.move_to_element(self.next_button).click(self.next_button) # add actions to action chain
                    time.sleep(3)
                    self.actions.perform() # execute action chain to move to next page
                    time.sleep(2)
                    self.driver.refresh() # refresh page otherwise you get stale element error
# Track page number and the time taken for scraper to run for each page
                    print("Extracted page {} of {}. Scraper has been running for {} seconds.".format(_, N, round(time.time() - self.start_time)))


                        ## Close JobSite ##
    def window_close(self):
        time.sleep(5)
        self.driver.close() # close driver


                        ## Run web scraper ##
if __name__ == '__main__':
    scraper = JobSiteScraper() # create instance of JobSiteScraper() class
    scraper.job_search() # run job search function
    scraper.scrape() # run scraper function
    print("Webscraping has finished.") # lets you know scraper has finished
    scraper.window_close() # run close window function
# Print list output from sraper as dataframe of jobs
    print(pd.DataFrame(scraper.jobs_list, columns = ['advert_type' , 'new', 'job_title', 'partnership', 'company', 'location', 'posted', 'salary', 'description', 'more']))

