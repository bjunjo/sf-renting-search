from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "YOU DRIVER PATH"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
google_form_link = "YOUR GOOGLE LINK"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-123.38021315527344%2C%22east%22%3A-122.43264235449219%2C%22south%22%3A37.6044034633095%2C%22north%22%3A38.0404839035864%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6"
}

response = requests.get(url=zillow_link, headers=headers)
webpage = response.text

# TODO: Fix why the price,link, and address don't match
# TODO: Parse the webpage
soup = BeautifulSoup(webpage, "html.parser")

# Create a list of links for all the listings you scraped
links = []
for link in soup.find_all("a", class_="list-card-link"):
    # If link has '/b/, then add "https://www.zillow.com/"
    if not link['href'].startswith('http'):
        link['href'] = "https://www.zillow.com/" + link['href']
    if link['href'] not in links:
        links.append(link['href'])

print(links)
print(len(links))

# Create a list of prices for all the listings you scraped
prices = []
for price in soup.find_all("div", class_="list-card-price"):
    each_price = re.sub(r"\+", "", price.getText().split()[0])
    prices.append(re.sub(r"/mo", "", each_price))

print(prices)
print(len(prices))

# Create a list of addresses for all the listings you scraped
addresses = [address.getText() for address in soup.find_all("address", class_="list-card-addr")]
print(addresses)
print(len(addresses))

# TODO: Use Selenium to fill in the form you created (step 1,2,3 above).
#   Each listing should have its price/address/link added to the form.
#   You will need to fill in a new form for each new listing.

for i in range(len(addresses)):
    driver.get(google_form_link)
    time.sleep(2)
    address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.click()
    address_input.send_keys(addresses[i])

    price_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.click()
    price_input.send_keys(prices[i])

    link_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.click()
    link_input.send_keys(links[i])

    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span').click()
driver.quit()