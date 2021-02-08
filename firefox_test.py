from selenium import webdriver

firefox = webdriver.Firefox()
firefox.get('http://seleniumhq.org/')
print(firefox.find_element_by_css_selector('body').text)