#!/usr/bin/env python
# coding: utf-8

# ![Capture1.PNG](attachment:Capture1.PNG)

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def create_dataframe(data):
    FIELDS = ["title", "description", "link"]
    df = pd.DataFrame(data, columns=FIELDS)
    display(df)
    df.to_csv('ws.csv', sep=',', index=False, header=True)
    print('Web Scraping Successful!')

def news_api(keyword):
    url = ('https://newsapi.org/v2/everything?'
           'q={keyword}&'
           'apiKey=4e70cabb80884db08524a28ac33cdc1d'.format(keyword=keyword))
    response = requests.get(url)
    
    if response.status_code == 200:
        print('API call successful!')
        json_response = response.json()
        
        if len(json_response['articles']) == 0:
            print('No News Articles Found')
        else:
            articles_data = []
            for article in json_response['articles']:
                title = article['title']
                description = article['description']
                link = article['url']
                articles_data.append((title, description, link))
                
            create_dataframe(articles_data)
    else:
        print('Status code: ', response.status_code)

def requests_web_scraping(location):
    url = ('https://earthdata.nasa.gov/search?q={location}'.format(location=location))
    response = requests.get(url)
    
    if response.status_code == 200:
        HTMLPage = BeautifulSoup(response.text, 'html.parser')
        
        data = []
        for lists in HTMLPage.find_all(class_='result'):
            if lists.span.text != '' and len(lists.find_all('p')) != 0:
                title = lists.span.text
                description = lists.find('p', class_='').text
                link = lists.find('p', class_='search-link').text
                data.append((title, description, link))
        
        create_dataframe(data)
    else:
        print('Status code: ', response.status_code)

keyword = input('Enter Keyword to be searched: ').lower()
news_api(keyword)

location = input('Enter Location: ').lower()
requests_web_scraping(location)

