from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get("https://www.bankalfalah.com/personal-banking/cards/privileges-discounts/discounts")

# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)

# Find the elements containing the discount content
discount_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "common_class_div")))

# List to store all discounts
discounts = []
count = 0

# Iterate over each element and extract relevant data
for element in discount_elements:
    discount_data = {}
    count += 1
    if count == 6:
        break
    
    # Extract category
    try:
        category_element = element.find_element(By.CLASS_NAME, 'discountCategory')
        discount_data['category'] = category_element.text.strip() if category_element else ''
    except:
        discount_data['category'] = ''
    
    # Extract location
    try:
        location_element = element.find_element(By.CLASS_NAME, 'locationDta')
        discount_data['location'] = location_element.text.strip() if location_element else ''
    except:
        discount_data['location'] = ''
    
    # Extract merchant name
    try:
        merchant_element = element.find_element(By.CLASS_NAME, 'headingDiscount')
        discount_data['merchant'] = merchant_element.text.strip() if merchant_element else ''
    except:
        discount_data['merchant'] = ''
    
    # Extract discount description (concatenate all <p> tags in contentDiscount)
    try:
        description_elements = element.find_element(By.CLASS_NAME, 'contentDiscount').find_elements(By.TAG_NAME, 'p')
        discount_data['description'] = ' '.join([desc.text.strip() for desc in description_elements if desc.text.strip()])
    except:
        discount_data['description'] = ''
    
    # Extract discount percentages by card type
    discount_data['discounts'] = []
    try:
        rows = element.find_element(By.CLASS_NAME, 'readmorecontent').find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            card_discount = {
                'card': cells[0].text.strip(),
                'discount': cells[1].text.strip()
            }
            discount_data['discounts'].append(card_discount)
    except:
        # Handle cases where the discount table might not be present
        pass
    
    # Add to the list
    discounts.append(discount_data)

# Close the browser
driver.quit()

# Print the dictionary containing all the discount data
for discount in discounts:
    print(discount)
