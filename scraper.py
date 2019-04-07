import os
import logging as log
from sys import argv,exit
from os.path import join

from tqdm import tqdm 
from lxml import html
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException


def url_formatter(url):
    if url.find('https://www.facebook.com/') != -1:
        return url[24:]
    elif url.find('https://mbasic.facebook.com/') != -1:
        return url[27:]
    elif url.find('https://m.facebook.com/') != -1:
        return url[22:]
    elif url.startswith('/'):
    	return url
    else : 
    	log.error('Post Url Format is not supported')
    	return None

# Enviroment and input parameters check
if len(argv) != 3:
	print('USAGE : python3 scarper.py INPUT_DIR OUTPUT_DIR')
	exit(1)
else :
	in_dir = argv[1]
	out_dir= argv[2]

if not os.path.isdir(out_dir):
	os.makedirs(out_dir)
if not os.path.isdir(in_dir):
	print('INPUT_DIR is not a directory, please read README.md')
	exit(1)

#Initialize selenium
options = webdriver.ChromeOptions()
user_data_path = os.getenv('LOCALAPPDATA')
user_data_path = join(user_data_path,'Google','Chrome','User Data')
options.add_argument("--user-data-dir=%s"%user_data_path)
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
log.basicConfig(level = log.INFO,format='%(asctime)-15s %(message)s')

for fp in tqdm([i for i in os.listdir(in_dir) if i.endswith('txt')][::-1]):
	#load input data
	links=[]
	with open (join(in_dir,fp),'r') as f:
		links = [i.strip('\n') for i in f.readlines()]

	#create output
	outpath = join(out_dir,fp.split('.txt')[0]+'.csv')
	log.info(outpath)
	df_result = pd.DataFrame(columns = ['post_url','user','reaction','user_url'])
	for index, raw_link in enumerate(links):
		#Crawling facebook page
		page_count = 0 
		init_link = url_formatter(raw_link)

		next_link = init_link
		next_link = 'https://mbasic.facebook.com' + next_link
		driver.get(next_link) # going to post url
		log.info('%s | Crawling : %s '%(outpath,next_link))
		tree = html.fromstring(driver.page_source)

		#Check if reactions exist
		next_link_list = tree.xpath("//a[contains(@href,'reaction/profile')]//img")
		next_link_list_check = tree.xpath('//a[contains(@href,"reaction/profile")][1]/div/div')
		if len(next_link_list) == 0 or len(next_link_list_check) == 0:
			log.info("Like Count = 0 QAQ")
			log.info(next_link)
			continue
		driver.find_element_by_xpath("//a[contains(@href,'reaction/profile')]").click() # Enter reactions list page

		while (True ):
			#Parse reactions
			tree = html.fromstring(driver.page_source)
			table_xpath = "//table//li/table/tbody/tr/td[@class]/table/tbody/tr"
			user = tree.xpath(table_xpath+"/td[3]//a/text()")
			user_url = tree.xpath(table_xpath+"/td[3]//a/@href")
			reaction = tree.xpath(table_xpath+"/td[2]//img/@alt")
			data= {'post_url':[init_link]*len(user),'user':user,'reaction':reaction,'user_url':user_url}
			df_result = df_result.append(pd.DataFrame(columns = df_result.columns,data=data))

			#Check if more reaction exist (check if "See more..." exist)
			next_link = tree.xpath('//span[contains(text() ,"See More")]/parent::a/@href')
			if len(next_link)!= 0:
				driver.find_element_by_xpath('//span[contains(text() ,"See More")]/parent::a').click()
				if page_count % 5 == 0 :
					log.info('crawled %d page' %page_count)
				page_count = page_count+1
			else :
				next_link = ''
				log.info('End Crawling %d link of %d '%(index+1, len(links)))

				break
	df_result.to_csv(outpath,index=False)

driver.close()
