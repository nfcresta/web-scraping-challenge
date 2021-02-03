# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd

def scrape_():
    # NASA Mars News 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find('div', class_='list_text')
        
    news_title = articles.find('div', class_='content_title').text
    paragraph = articles.find('div', class_='article_teaser_body').text

    browser.quit()


    # JPL Mars Space Images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find('div', class_='thmbgroup')

    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{images.find_all('a')[1]['href']}"
    featured_image_url

    browser.quit()


    # Mars Facts
    url = 'https://space-facts.com/mars/'

    pandas_scrape = pd.read_html(url)
    pandas_scrape

    mars_df = pandas_scrape[0]
    mars_df.columns=['Description', 'Mars']
    mars_df = mars_df.set_index('Description')

    table_html = mars_df.to_html()


    ### Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    # create empty list to append dictionary to later
    mars_hemispheres = []

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # loop through page to find image urls and titles
    for x in range(4):
        titles = browser.find_by_tag('h3')
        titles[x].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('h2', class_='title').text.split(' E')[0]
        image = soup.find('img', class_='wide-image')['src']
        image_url = f"https://astrogeology.usgs.gov{image}"
        
        marsDict = {'title:': title, 'img_url': image_url}
        mars_hemispheres.append(marsDict)
        browser.back()

    mars_hemispheres

    browser.quit()

    # dictionary containing all scraped data
    scraped_data = {
        'news_title': news_title,
        'news_p': paragraph,
        'featured_image_url': featured_image_url,
        'mars_facts_table': table_html,
        'mars_hemispheres': mars_hemispheres
    }

    return scraped_data