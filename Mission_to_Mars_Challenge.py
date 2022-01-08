#!/usr/bin/env python
# coding: utf-8

# In[60]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[61]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# the last line, we are accomplishing two things
# 1. we are searching for elements with a specific conbination of tag(div) and attribute (list_text). for ex: ul.item_list would be found in HTML as <ul class='item_list'>
# 2. we are telling out browser to wait one second before searching for components.
#    the optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy


# In[10]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# we have assigned slide_elem as the variable to look for the <div> tag and its descendent. this is our parent element.
# this means that this element holds all of the other elements within it and we will reference it when we want to filter search results even further
# div.list_text pinpoints the <div> tag with the class of list_text


# In[11]:


# we will want to assign the title and summary text to variables we will reference later
slide_elem.find('div', class_='content_title')

# the tile is in the mix of html in our output.


# In[12]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# we have created a new variable for the title, added the get_text() method and we are searching within the parent element for the title


# In[13]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Scrape Mars Data: Featured Image

# ### Featured Images

# In[14]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[15]:


# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] # although it said [1], it is the second one, start at [0]
full_image_elem.click()


# In[16]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[17]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# we will use the image tag and class <img>tag fancybox-img class to build the URL to the full-size image
# an img tag is nested within this HTML, sw we have included it
# .get('src') pulls the link to the image


# In[18]:


# use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Scrape Mars Data : Mars Facts

# In[19]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# first line: we are creating a new DataFrame from the HTML table. the read_html() specifically searches for and returns a list of tables found in the HTML
#             by specifying an index of 0, we only want the first table it encounters or the first item in the list and then return the tabl into a DataFrame
# second line: we assign columns to the new DataFrame for additional clarity
# third line: by using .set_index(), we are using yje Desciption column as the DataFrame's index. 
#             inplace=True means that the updated index will remian in place, without having to reassign the DataFram to a new variable


# In[20]:


# convert our DataFrame back into HTML-ready code using the .to_html() function
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 

# ### Hemispheres
# 

# In[62]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[63]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
new_img_soup = soup(html, 'html.parser')
# since there are four images on the web, we set range = 4
for i in range(4):
    # create a dictionary to hold the infos
    hemispheres = {}
    
    # click on the h3 which is the name of the image on the website
    browser.find_by_css('h3')[i].click()
    
    # since all of the image link end by full.jpg, we can use the links.find_by_partial_href to find the href link for the full image URL
    img_url = browser.links.find_by_partial_href('full.jpg')['href']
    
    
    # set the html equal to the html that we are browsing now
    html = browser.html
    # parse the resulting html with soup
    img_soup = soup(html, 'html.parser')
    
    # use the img_soup to find h2 with the class of title, put them in text form and save them in the title variable
    title = img_soup.find('h2', class_='title').get_text()
    
    # save the img_url and title into hemispheres dictionaries
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    
    # save the hemispheres dictionaries into the list
    hemisphere_image_urls.append(hemispheres)
    
    # browse back to do the second image
    browser.back()


# In[64]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[65]:


# 5. Quit the browser
browser.quit()


# In[ ]:




