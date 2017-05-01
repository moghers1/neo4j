##########################################################
# crawl yelp listings and scrape data in preparation of neo4j graph analysis
#
##########################################################

import requests
from bs4 import BeautifulSoup
import time
import json

def yelp_spider(page_start):
  page = 0
  while page <= page_start:
    url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Pittsburgh,+PA&start=" + str(page) +"&cflt=coffee"
    soup = soup_it(url)

    for link in soup.findAll('a', {'class': 'biz-name js-analytics-click'}):
      
      # crawl actual listing page
      href = "https://www.yelp.com" + link.get('href')  

      ####this will setup a brand-new list and dictionary for every link
      # get name of restaurant
      dict3 = {'Rest_Name': link.string}

      get_restaurant_reviews(href, dict3)

    page += 10



def get_restaurant_reviews(restaurant_url, restDict):
  soup = soup_it(restaurant_url)

  # pull avg rating from main restaurant page
  for rating in soup.findAll('div', {'class': 'biz-rating biz-rating-very-large clearfix'}):

    #could just split on ' ' ? if replacing with |, split on space would do the same thing
    #you could easly leave as separate lines for readabilty , I like single line things
    rest_review = rating.contents[3].string.strip().split()[0]
    restDict.update({'Rest_Reviews': rest_review})


  for link in soup.findAll('a', {'class': 'user-display-name js-analytics-click'}):
    profile_href = "https://www.yelp.com" + link.get('href')
    get_user_profile(profile_href, restDict)



#adds the name,city,total_reviews AND writes the final dictionary
def get_user_profile(profile_url, profileDict):
  soup = soup_it(profile_url)

  for profile in soup.findAll('div', {'class': 'user-profile_info arrange_unit'}): 

    # get customer name
    profileDict.update({'Cust_Name': profile.contents[1].text})

    # get city and state
    c,s = profile.contents[3].text.replace(',','|').replace(' ','').split('|')
    profileDict.update({'Cust_City':c, 'Cust_State':s})

    # get total reviews
    profileDict.update('Total_Reviews': profile.find('strong').text)

    # append data to json file 
    # i like the idea of a separate 'write' function, that way if you add more depths of spider, you can just reuse the function instead of rewriting the 2/3 lines of code
    json_appender(profileDict)

#helper function to return the beautiful soup representation of a url
def soup_it(url):
  source_code = requests.get(profile_url)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text)
  return soup

#could add in another input parameter of 'file_name' if you wanted this to be very reusable 
def json_appender(profileDict):
    with open('neo4j_prep.json', 'a') as outfile:
        json.dump(profileDict, outfile)

if __name__=="__main__":
    # crawl 1 page
    yelp_spider(0)

