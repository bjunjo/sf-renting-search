# sf-renting-search
## Problem: Searching one bed room apartment in SF automatically using Python!
## Solutions
1. Parse the webpage
```
soup = BeautifulSoup(webpage, "html.parser")
```
2. Create a list of links, prices, and addresses
```
# For example here's how you get the addresses

addresses = [address.getText() for address in soup.find_all("address", class_="list-card-addr")]
```
3. Use Selenium to fill in the form you created (step 2 above)
```
address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
address_input.click()
address_input.send_keys(addresses[i])
```
## Lesson
- Back in 1991 when the Internet just started, somebody said "I will replace your industry with 70 lines of Python code". It has happened since.
