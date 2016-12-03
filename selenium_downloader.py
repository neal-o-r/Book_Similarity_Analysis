# SELENIUM web scraper example

# import time module to pause our script while the html loads
import time

# selenium is what we use to operate a web browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# here we are telling selenium to use chrome.
# if you search "selenium chromedriver", you will be able to download this driver.
browser = webdriver.Chrome(executable_path='/home/blake/Drive/Other/GITHUB/Book_Analysis/chromedriver')

# we are interested in a website which loads using javascript (that is, normal webscraping will fail)

print "Getting MetaData"

browser.get("https://www.gutenberg.org/browse/scores/top")
raw = browser.page_source.split("\n")

addresses = []
names = []
successes = []

for i in raw:
	if '<a href="/ebooks/' in i:
		print i
		address = i.split('"')[1].split("/")[-1]
		name = i.split('"')[2][1:-10].split("(")[0]

		addresses.append(address)
		names.append(name)

		break

print "Got the metadata, waiting"

time.sleep(10)

for index, value in enumerate(addresses):
	try:
		browser.get("https://www.gutenberg.org/ebooks/" + value )
		raw2 = browser.page_source.split("\n")


		for i in raw2:
			if "Plain Text UTF-8" in i:
				break

		download_addr = i.split('<a href="')[1][2:].split('"')[0]

		browser.get("https://" + download_addr)
		raw3 = browser.page_source

		f = open("/home/blake/Drive/Other/GITHUB/Book_Analysis/texts/" + names[index].replace(" ", "_") + ".txt", 'w')

		
		f.write(raw3.encode('utf8'))

		f.close()
		
		print "SUCCESS", names[index], "\n"
		successes.append(True)
	except:
		print "FAILED", names[index], "\n"
		successes.append(False)
	time.sleep(10)
	
browser.close()

f = open("/home/blake/Drive/Other/GITHUB/Book_Analysis/texts/SUCCESSES.txt", 'w')

for x, y in zip(names, successes):
	f.write(str(x) + "\t" + str(successes) + "\n")

f.close()








