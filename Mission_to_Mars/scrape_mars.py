
#scrape_mars.py

#import dependencies
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
import pandas as pd
import os
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[15]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', executable_path, headless=False)


# In[26]:

# NASA Mars News
def mars_news(browser):
# Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # import time
    time.sleep(5)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")


    # save the most recent article, title
    slide_element = soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")

    # Scrape the Latest News Title
    # Use Parent Element to Find First <a> Tag and Save it as news_title
    news_title = slide_element.find("div", class_="content_title").get_text()

    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
 
    return news_title, news_p
# In[19]:

# JPL Mars Space Images - Featured Image
# Open browser to JPL Featured Image
# URL of page to be scraped
def featured_image(browser):
    url="https://www.jpl.nasa.gov/images?search=&category=Mars"

    # Retrieve the page
    browser.visit(url)

    # Wait 3 seconds to load the page
    time.sleep(3)

    browser.links.find_by_partial_text('Image').click()

    # Wait 3 seconds to load the page
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    featured_image_url = soup.find('img', class_="BaseImage")['src']
    return featured_image_url


# In[31]:
# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")




# Visit the USGS Astrogeology Science Center Site
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls


# Main Web Scraping Bot
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
   
   
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": img_url,
    "facts": facts,
    "hemispheres": hemisphere_image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())