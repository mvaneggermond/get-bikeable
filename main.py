# Import the script
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
import pandas as pd
import os
import time
import csv
from selenium.common.exceptions import TimeoutException

def scrape_bikeable():
    # Use a breakpoint in the code line below to debug your script.
    print('Start scraping')
    # Get this url
    url = "https://backend.bikeable.ch/api/v2/geojson-spots"
    # Get the page
    page = requests.get(url)
    # Parse the page with bs
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get the page - it is JSON - returns a dictionary
    data = json.loads(soup.get_text())  # a dictionary!
    # Uncomment to read the page
    # print(json.dumps(data, indent=4))
    # Initialize selenium
    # I installed the geckodriver with brew install geckodriver
    options = FirefoxOptions()
    options.add_argument("--headless")
    # Get the features from the dataset
    features = data['features']

    # Dir for saving images
    dirname = os.path.dirname(__file__)

    # Loop over the features
    # Set the i
    i = 0
    # Initialize an empty tuple to store the results
    res = []
    while i < len(features):
    #while i < 20:
        # Properties contain the id
        prop = data['features'][i]['properties']
        id = prop['_id']
        link = prop['link']
        print("Processing: " + str(i) + " " + link)

        # Coordinates are stored here
        coord = data['features'][i]['geometry']['coordinates']
        x = coord[0]
        y = coord[1]

        # Placeholder data
        header = ''
        desc = ''
        vote = ''
        vote_num = ''
        date = ''

        # Get the link with Selenium
        try:
            driver = webdriver.Firefox(options=options)
            driver.set_page_load_timeout(10)
            driver.get(link)
            driver.implicitly_wait(5)

            # Get the source
            page_details = (driver.page_source).encode('utf-8')
            # Parse the page with bs
            soup_details = BeautifulSoup(page_details, 'html.parser')
            # Get the lead desc
            for lead in soup_details.find_all('p', class_='lead__desc'):
                desc = lead.text.strip()
                print(desc)


            # We need to get the image and the text
            for div_header in soup_details.find_all('div', class_='entry__header'):
                for h1 in div_header.findAll("h1"):
                    header = h1.text.strip()
            # Get the vote
            for div_vote in soup_details.find_all('a', class_='entry__votes__button'):
                vote = div_vote['title']
            # Get the rating
            for div_vote_num in soup_details.find_all('span', class_='entry__votes__num'):
                vote_num = div_vote_num.text
            # Get the dat
            for div_date in soup_details.find_all('span', class_='date'):
                date = div_date.text

            # We need to get the image and the text
            for div_img in soup_details.find_all('div', class_='carousel-cell is-selected'):
                for img in div_img.findAll("img"):
                    image_url = img['src']
                    try:
                        img = Image.open(requests.get(image_url, stream=True).raw)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        filename = os.path.join(dirname, 'images/')
                        img.save(filename+str(i)+'_'+id+'.jpg')
                    except:  # catch *all* exceptions
                        print("Error")

            res.append((str(i), id, header, vote, vote_num, desc, date, str(i)+'_'+id, x, y))
            time.sleep(2)
            driver.close()
            driver.quit()
        except TimeoutException as ex:  # catch *all* exceptions
            isrunning = 0
            print("Exception has been thrown. " + str(ex))
            driver.close()
            driver.quit()


        i += 1
    df = pd.DataFrame(res, columns=("id", "bikeable_id", "title", "vote", "vote_num", "description", "date", "photo_name", "x", "y"))

    filename = os.path.join(dirname, '', 'bikeable.csv')
    df.to_csv(filename,  encoding='utf-8-sig')

    print(df.head(10))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_bikeable()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
