import time
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
CATEGORIES = {
    "Sports & Outdoor": "https://www.banggood.com/Wholesale-Sports-and-Outdoors-ca-6001.html",
    "Automobiles & Motorcycles": "https://www.banggood.com/Wholesale-Automobiles-and-Motorcycles-ca-4001.html",
    "Electronics": "https://www.banggood.com/Wholesale-Electronics-ca-2001.html",
    "Computers & Office": "https://www.banggood.com/Wholesale-Computers-and-Office-ca-5001.html",
    "Men & Women Clothing": "https://www.banggood.com/Wholesale-Men-and-Womens-Clothing-ca-18941.html"
}

SELECTORS = {
    "title": [".product-title-text", "h1", "a.title"],
    "price": [".main-price", ".current-price", "span.price"],
    "rating": [".review-score", ".star-num", "//span[contains(@class, 'score')]"],
    "reviews": [".review-num", "//*[contains(text(), 'Reviews') and contains(@class, 'num')]"]
}

# LIMITS
MAX_PRODUCTS_PER_CATEGORY = 40  
PAGES_TO_SCAN = 3               

def setup_driver():
    """Initializes an optimized headless Chrome browser."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Uncomment for invisible mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'eager'
    
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(25)
    return driver

def safe_get(driver, url, retries=3):
    """Attempts to load a URL with retries to handle network errors."""
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except TimeoutException:
            print("    > Timeout, stopping load (continuing)...")
            driver.execute_script("window.stop();")
            return True
        except WebDriverException as e:
            print(f"    > Connection Error (Attempt {attempt+1}/{retries}): {e.msg[:50]}...")
            time.sleep(5) # Wait for internet to recover
    return False

def get_product_links(driver, category_url):
    """Scrapes product URLs from the listing page."""
    links = []
    
    if not safe_get(driver, category_url):
        print("    > Skipping page due to connection failure.")
        return []

    time.sleep(3)
    
    # Scroll to trigger lazy load
    try:
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except: pass
        
    elements = driver.find_elements(By.TAG_NAME, "a")
    for elem in elements:
        try:
            href = elem.get_attribute("href")
            if href and "-p-" in href and ".html" in href:
                if href not in links:
                    links.append(href)
        except:
            continue
            
    return list(set(links))

def extract_product_details(driver, url, category):
    """Visits product page and extracts details."""
    product = {
        "Category": category,
        "Product Name": "N/A",
        "Price": "0.00",
        "Rating": "0.0",
        "Reviews": "0",
        "Product URL": url
    }
    
    if not safe_get(driver, url):
        return product # Return empty if load fails
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(0.5)
    except: pass
    
    try:
        # 1. NAME
        for sel in SELECTORS["title"]:
            try:
                product["Product Name"] = driver.find_element(By.CSS_SELECTOR, sel).text
                break
            except: continue
            
        # 2. PRICE
        for sel in SELECTORS["price"]:
            try:
                price_text = driver.find_element(By.CSS_SELECTOR, sel).text
                product["Price"] = price_text.replace("US", "").replace("$", "").strip()
                if product["Price"]: break
            except: continue
            
        # 3. RATING
        for sel in SELECTORS["rating"]:
            try:
                if "//" in sel: # XPath
                    product["Rating"] = driver.find_element(By.XPATH, sel).text
                else:
                    product["Rating"] = driver.find_element(By.CSS_SELECTOR, sel).text
                if product["Rating"]: break
            except: continue
            
        # 4. REVIEWS
        for sel in SELECTORS["reviews"]:
            try:
                if "//" in sel:
                    txt = driver.find_element(By.XPATH, sel).text
                else:
                    txt = driver.find_element(By.CSS_SELECTOR, sel).text
                
                nums = re.findall(r'\d+', txt)
                if nums:
                    product["Reviews"] = nums[0]
                    break
            except: continue
            
    except Exception as e:
        pass 
        
    return product

def main():
    # Ensure data directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "../data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    driver = setup_driver()

    try:
        for cat_name, base_link in CATEGORIES.items():
            print(f"--- Processing Category: {cat_name} ---")
            
            # 1. Collect Links
            product_urls = []
            for page in range(1, PAGES_TO_SCAN + 1):
                if len(product_urls) >= MAX_PRODUCTS_PER_CATEGORY:
                    break
                    
                if "?" in base_link:
                    page_url = f"{base_link}&page={page}"
                else:
                    page_url = f"{base_link}?page={page}"
                
                print(f"  Fetching links from page {page}...")
                new_links = get_product_links(driver, page_url)
                product_urls.extend(new_links)
                
                # Remove duplicates
                product_urls = list(set(product_urls))
            
            print(f"  Found {len(product_urls)} unique links. Scraping first {MAX_PRODUCTS_PER_CATEGORY}...")
            
            # 2. Extract Data for this Category
            category_data = []
            for i, url in enumerate(product_urls[:MAX_PRODUCTS_PER_CATEGORY]):
                print(f"    Scraping item {i+1}/{MAX_PRODUCTS_PER_CATEGORY}...")
                data = extract_product_details(driver, url, cat_name)
                
                if data["Product Name"] != "N/A":
                    category_data.append(data)
            
            # 3. Save Category-Specific CSV
            if category_data:
                safe_name = cat_name.lower().replace(" & ", "_").replace(" ", "_").replace("'", "")
                filename = f"{safe_name}.csv"
                file_path = os.path.join(data_dir, filename)
                
                df = pd.DataFrame(category_data)
                df.to_csv(file_path, index=False)
                print(f"  Saved {len(df)} items to data/{filename}")
            else:
                print(f"  No valid data found for {cat_name}")

    finally:
        driver.quit()
        print("\nScraping Complete.")

if __name__ == "__main__":
    main()