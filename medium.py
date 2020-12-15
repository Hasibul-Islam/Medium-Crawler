from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
# firefox_driver_path = 'D:\DS Learning\Keyword Extraction\Scrapping\Selenium\medium\geckodriver'
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument('--lang=en-GB')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--incognito")


# chrome_options.add_argument("--app=http://www.google.com")
chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})

url='https://medium.com/topics'
try_count = 3
while try_count>0:
	try:
		with webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options) as driver:
			driver.set_page_load_timeout(3000)
			# action = ActionChains(driver)
			driver.get(url)
			page_source = BeautifulSoup(driver.page_source,features="html.parser")
			driver.close()
			break
	except:
		print('trying again to fetch topics')
	try_count-=1

topic_urls = page_source.find_all('a',{'class':'u-flex0 u-height180 u-backgroundCover'})
topic_urls = [url['href'] for url in topic_urls]

print(len(topic_urls))

time.sleep(10)

for url in topic_urls[1:2]:
	try_count=3
	while try_count>0:
		try:
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
				break
		except:
			print('trying again to fetch urls')
		try_count-=1

array_of_articles = html_to_text.find_all('h3',{'class':'bj gb gh bl aw eo ep at eq av er gm aq'})

array_of_articles = [h3.find('a')['href'] for h3 in array_of_articles]
print(len(array_of_articles))

time.sleep(20)
for article_link in array_of_articles:

	try_count=3
	while try_count>0:
		try:
			if article_link.startswith('https'):
				link = article_link.split('?')[0]
			else:
				link ='https://medium.com'+ article_link.split('?')[0]
			with webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options) as driver:
				driver.set_page_load_timeout(3000)
				driver.get(link)
				html_to_text = BeautifulSoup(driver.page_source,features="html.parser")
				try:
					blog_title = html_to_text.find('h1').text.strip()
				except:
					blog_title = None
				blog_topic = ""
				print(blog_title)
				paragraphs = html_to_text.find_all('p')
				
				article_content = [para.text.strip() for para in paragraphs]
				# print(article_content)
				# iamages = html_to_text.find_all('img')
				# for img in iamages:
				# 	print(img['src'])
				# header_image = ''
				# try:
				# 	blog_author = html_to_text.find('a',{'class':'du gm bc bd be bf bg bh bi bj gn bm go gp'}).text.strip()
				# except:
				# 	blog_author = None
				# print(blog_author)
				# try:
				# 	published_at = html_to_text.find('a',{'class':'du gm bc bd be bf bg bh bi bj gn bm go gp'}).text.strip()
				# 	# published_at = datetime.strptime(published_at.split('T')[0], '%Y-%m-%d')
				# 	print(published_at)
				# except:
				# 	published_at = None
				# if not published_at:
				# 	print(link)
				# block_para = main_content.find_all('blockquote')
				# blockquotes = [block.text.strip() for block in block_para]
				# article = {
				# 	'title':blog_title,
				# 	'topic': blog_topic,
				# 	'author_name':blog_author,
				# 	'body':article_content,
				# 	'summary':article_content[:5],
				# 	'published_at':published_at,
				# 	'images_url':header_image,
				# 	'blockquote':blockquotes,
				# 	'heart':[],
				# 	'heart_count': 0,
				# 	'view_count': 0,
				# 	'comment':[],
				# 	'fetch_from_internet':True,
				# 	'domain': 'huffpost',
				# 	'article_url': link,

				# }
				

				# print(article)
				driver.close()
				break
		except:
			print("trying again to fetch content!")
			time.sleep(20)
		try_count-=1
	time.sleep(20)