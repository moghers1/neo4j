# neo4j

crawl yelp listings and scrape data in preparation of neo4j graph analysis.


```
// import yelp listing data
CALL apoc.load.json("file:///tmp/Desktop/neo4j_listing.json") YIELD value AS listing
CREATE (l:Listing {listing_id: listing.listing_id})
SET 	l.name 			= listing.Rest_Name
```
```
WITH count(*) as dummy 
```
```
// import yelp restaurant data
CALL apoc.load.json("file:///tmp/Desktop/neo4j_restaurant.json") YIELD value AS restaurant
CREATE (r:Restaurant {restaurant_id: restaurant.restaurant_id})
SET 	r.name 			= restaurant.Rest_Name,
	r.reviews 		= restaurant.Rest_Reviews
```
```
WITH count(*) as dummy 
```
```
// import yelp user profile data
CALL apoc.load.json("file:///tmp/Desktop/neo4j_profile.json") YIELD value AS profile
CREATE (p:Profile {profile_id: profile.profile_id})
SET 	p.name 			= profile.Rest_Name,
	p.reviews 		= profile.Rest_Reviews,
	p.name 			= profile.Cust_Name,
	p.city 			= profile.Cust_City,
	p.state 		= profile.Cust_State,
	p.reviews 		= profile.Total_Reviews
```
```
WITH count(*) as dummy 
```
```
// create relationships
MATCH (l:Listing),(p:Profile) 
CREATE (p)-[:WENT_TO]->(l)
CREATE (l)-[:SERVED]->(p)
```

![Alt text](graph.png "Person/Restaurant Relationship")
