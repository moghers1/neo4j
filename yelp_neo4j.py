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
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text)

		for link in soup.findAll('a', {'class': 'biz-name js-analytics-click'}):
			
			# crawl actual listing page
			href = "https://www.yelp.com" + link.get('href')	

			# get name of restaurant
			dfRestName = []
			rn = link.string
			dfRestName.append(rn)

			dict3 = {}
			ListingDict = {'Rest_Name': v for v in dfRestName} 
			dict3.update(ListingDict)

			get_restaurant_reviews(href, dict3)

		page += 10


def get_restaurant_reviews(restaurant_url, restDict):
	source_code = requests.get(restaurant_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)

	# pull avg rating from main restaurant page
	for rating in soup.findAll('div', {'class': 'biz-rating biz-rating-very-large clearfix'}):
		dfRestReviews = []
		rr0 = str(rating.contents[3].string.strip().replace(' ','|'))
		spt = rr0.split('|')
		rr1 = spt[0]
		dfRestReviews.append(rr1)
		
		restaurantDict = {'Rest_Reviews': v for v in dfRestReviews} 	
		restDict.update(restaurantDict)


	for link in soup.findAll('a', {'class': 'user-display-name js-analytics-click'}):
		profile_href = "https://www.yelp.com" + link.get('href')
		get_user_profile(profile_href, restDict)


def get_user_profile(profile_url, profileDict):
	source_code = requests.get(profile_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)

	for profile in soup.findAll('div', {'class': 'user-profile_info arrange_unit'}): 

		# get name
		dfCustName = []
		n = str(profile.contents[1].text)
		dfCustName.append(n)

		DictCustName = {'Cust_Name': v for v in dfCustName}
		profileDict.update(DictCustName)

		# get city and state
		dfCustCity = []
		dfCustState = []
		loc = str(profile.contents[3].text.replace(',','|').replace(' ',''))
		spt = loc.split('|')
		c = spt[0]
		s = spt[1]
		dfCustCity.append(c)
		DictCustCity = {'Cust_City': v for v in dfCustCity}
		profileDict.update(DictCustCity)

		dfCustState.append(s)
		DictCustState = {'Cust_State': v for v in dfCustState}
		profileDict.update(DictCustState)

		# get total reviews
		for review in profile.find_all('strong'):
			dfTotReviews = []
			r = str(review.text)
			dfTotReviews.append(r)
			DictTotReviews = {'Total_Reviews': v for v in dfTotReviews}
			profileDict.update(DictTotReviews)

		# append data to json file
		with open('neo4j_prep.json', 'a') as outfile:
			json.dump(profileDict, outfile)


# crawl 1 page
yelp_spider(0)

