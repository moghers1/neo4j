# neo4j

crawl yelp listings and scrape data in preparation of neo4j graph analysis.

neo4j relations:

	restaurants-[serves]->person
	restaurants-[caters]->food
	restaurants-[located_in]->county
	review-[given_to]->restaurants
	person-[went_to]->restaurants
	person-[rated]->restaurants
	person-[wrote]->person
	person-[knows]->person
	person->[knows]-person
	person-[lives_in]->county

neo4j nodes & node properties:

	restaurants 	- location, average_rating
	person 		    - firstname, location, total_reviews
	review 		    - dateofreview, stars, comments
	county 		    - county, city, state

