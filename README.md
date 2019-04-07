# Facebook Reactions Scraper

This project use [Selenium](https://www.seleniumhq.org/) to crawling facebook reaciton list and  parsing it to csv file with xpath. You can get `post_url`, `user`,`reaction`,`user_url` as output(in csv), and you need to provide post url as input.  
I recommend to use [rugantio/fbcrawl](https://github.com/rugantio/fbcrawl) to crawl post link of page if you need  
## Disclaimer

This software is not authorized by Facebook, **use it at your own risk**. Scraping facebook data does not follow Facebook robots.txt and violating terms and condition of Facebook.This software is provided only in educational propose, show how to scrap faceook page   

## Installation

Only support Windows now, you can modified selenium parameter to support macOS or Linux if you need  
Of course, make sure you have already install `python3`, and required python packages are as following:   

- `seleinum` 
- `pandas`
- `tqdm`
- `lxml`

Or simply install with `pip install -r requirements.txt`  

This project also use Chrome as selenium browser, so that make sure you have already install `Google Chrome`   

By default,it should be all right if you installed latest chrome ,however if the version of webdriver is not consistent with Chrome, please replace [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) in project folder   

## Usage 

1. Make sure your chrome have already login Facebook,do not remove facebook cookies (You need to login to see reaction list) , and turn your facebook display language to English
2. Close all Chrome windows to avoid preventing selenium start 
3. Put the link(in txt fromat) you want to scrap in `INPUT_DIR` 
   - you can split all post url in several txt file to estimate scraping speed(by tqdm) or to split output file
   - Scraper would ouptut one txt file after crawling all link in one txt file in `INPUT_DIR`
   - support `www.facebook`, `m.faceboook`, `mbasic` link (you can see sample input in input folder)
4. `python3 scarper.py INPUT_DIR OUTPUT_DIR`

## Known Issue
- [ ] Miss data in big reaction count(might be the problem of `mbasic.facebook`)
	- a post with about 5k up reaction, would only crawled 1-2k reaction
- [ ] slow down when big reactions count
## something else
- you can remove `options.add_argument('headless')` to see full scraping progress in Chrome