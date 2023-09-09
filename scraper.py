# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:00:26 2023

@author: AhmedOmar
"""

import requests
from bs4 import BeautifulSoup
from time import sleep

import database as my_database



# Function to extract Product Title
def get_amazon_id(item_link):
    
    amazon_id = -1
    try:
        
        data_1 = item_link.split('%2Fdp%2F')
        
        data_2 = data_1[1].split('%2F')
        
        amazon_id = str(data_2[0])

    except Exception as e:
        #print("get_amazon_id 1 "+str(e)+"   ***   "+str(item_link))
        
        try:
            
            data_1 = item_link.split('/dp/')
            
            data_2 = data_1[1].split('/')
            
            amazon_id = str(data_2[0])

        except Exception as ee:
            print("get_amazon_id 2 "+str(ee)+"   ***   "+str(item_link))
            amazon_id = -1

    return amazon_id


########################################################################
########################################################################
########################################################################

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


########################################################################
########################################################################
########################################################################

# Function to extract Product Price
def get_price(soup):

    try:
        #price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
        price = float(soup.find("span", attrs={'class':'a-price-whole'}).text)
        
        price_decimal = float(soup.find("span", attrs={'class':'a-price-fraction'}).text)
        
        if price_decimal > 10:
            price += (price_decimal/100)
        else:
            price += (price_decimal/10)
            

    except AttributeError as e:
        price = -1
        
        print("get_price "+str(e))
        
        


    return price


########################################################################
########################################################################
########################################################################

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating



########################################################################
########################################################################
########################################################################

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count


########################################################################
########################################################################
########################################################################

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


########################################################################
########################################################################
########################################################################


# Function to generat the search query
def get_query(query_item):
    
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})
    
    search_query = str(query_item).replace(' ', '+').replace('%20', '+')
    base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)
    
    ######################################
    
    my_database.init_scrapper_database()
    
    ######################################
    
    query_id = my_database.insert_query(search_query)
    
    if query_id == None:
        my_database.close_scrapper_connection()
        return None
    
    current_page = 1;
    
    while base_url != "":
        
        webpage = requests.get(base_url, headers=HEADERS)
    
        soup = BeautifulSoup(webpage.content, "html.parser")
    
        item_data(soup, query_id, HEADERS)
        
        #########################################
        
        pagination_link = soup.find("a", attrs={'aria-label':'Go to next page, page '+str(current_page +1)})
        current_page = current_page + 1
        
        if pagination_link is None:
            base_url = ""
        else:
            base_url = "https://www.amazon.com" + pagination_link.get('href')
            
            
            
    ######################################
    
    my_database.close_scrapper_connection()
    
    ######################################
    
    return query_id;


########################################################################
########################################################################
########################################################################
   
# Function to extract all the amazon item data
def item_data(soup, query_id, HEADERS):
    
    
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    
    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_link = "https://www.amazon.com" + link
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        
        
        print("*** "+str(get_title(new_soup))+" ***")
        
        
        amazon_item_id = my_database.insert_amazon_item(get_amazon_id(new_link), get_title(new_soup), get_price(new_soup),get_rating(new_soup), get_review_count(new_soup), get_availability(new_soup), new_link)

        if amazon_item_id == None:
            print("amazon_item_id is null ////")
            my_database.close_scrapper_connection()
            
            my_database.init_scrapper_database()
            continue
        
        insert_query_result_id = my_database.insert_query_result(query_id, amazon_item_id)
        
        if insert_query_result_id == None:
            print("insert_query_result_id is null ///")
            my_database.close_scrapper_connection()
            
            my_database.init_scrapper_database()
            continue
        
        
        
        print("*** "+str(query_id)+"  "+str(amazon_item_id)+"  "+str(insert_query_result_id)+"  "+"***")
        
        

