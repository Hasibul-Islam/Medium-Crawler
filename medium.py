from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from datetime import datetime, timedelta
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.action_chains import ActionChains 

array_of_articles = []


chrome_driver_path = 'D:\DS Learning\Keyword Extraction\Scrapping\Selenium\medium\chromedriver'
# chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=en-GB')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--incognito")

url='https://medium.com/topics'
with webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options) as driver:
	driver.set_page_load_timeout(3000)
	# action = ActionChains(driver)
	driver.get(url)
	page_source = BeautifulSoup(driver.page_source,features="html.parser")
	driver.close()

topic_urls = page_source.find_all('a',{'class':'u-flex0 u-height180 u-backgroundCover'})
topic_urls = [url['href'] for url in topic_urls]

print(topic_urls)

for url in topic_urls[:1]:
	with webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options) as driver:
		driver.set_page_load_timeout(3000)
		# action = ActionChains(driver)
		driver.get(url)
		elem = driver.find_element_by_tag_name('body')
		no_of_pagedowns = 3
		while no_of_pagedowns:
			elem.send_keys(Keys.PAGE_DOWN)
			time.sleep(3)
			no_of_pagedowns-=1
			print(no_of_pagedowns)


		html_to_text = BeautifulSoup(driver.page_source,features="html.parser")
		driver.close()

array_of_articles = html_to_text.find_all('h3',{'class':'bj gb gh bl aw eo ep at eq av er gm aq'})

array_of_articles = [h3.find('a')['href'] for h3 in array_of_articles]
print(array_of_articles)

