from selenium import webdriver
from selenium.webdriver.chrome.options import Options



options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get("https://www.example.com")