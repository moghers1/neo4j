from random import randint, choice, random
import datetime
from string import ascii_lowercase as letters
import json
import sys
import os



# # # # #
# STEP 1: # generate random values (numbers, letters, dates)
# # # # #

def randNum(n):
	return int("".join([str(randint(0,9)) for _ in xrange(n)]))

def randLetters():
	return "".join([choice(list(letters)) for _ in xrange(randint(3,12))])

def randAddress():
	return " ".join([str(randint(1,1000)),randLetters(),choice(["STREET","LANE","AVENUE","PLACE","HIGHWAY"])])

def randState():
	return choice(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

def randEmail():
	return "".join([randLetters(),"@",randLetters(),".",choice(["com","org","edu"])])



# # # # #
# STEP 2: # begin to create attributes of a person using random values created in STEP 1
# # # # #

def demographic():
	d = {"FIRST_NAME":randLetters(), "LAST_NAME":randLetters(),"GENDER":choice(["M","F"]), "SSN":randNum(9)}
	return d

def address():
	d = {"ADDRESS":randAddress(),"STATE":randState(),"ZIPCODE":randNum(5),"COUNTY":randLetters()}
	return d

def contact():
	d = {"PHONE":randNum(10),"EMAIL":randEmail()}
	return d


# # # # #
# STEP 2: # combine all generators from above
# # # # #

def make_person():
	person = {}
	person.update(demographic())
	person["PERSON_CONTACTS"]=[contact() for _ in xrange(randint(1,3))]
	person["ADDRESS"]=[address() for _ in xrange(randint(1,2))]
	return person


if __name__=="__main__":
	n = int(sys.argv[1])
	fname = sys.argv[2]

	def append_record(record,fname):
		with open(fname, 'a') as f:
			json.dump(record, f, indent=4)
			f.write(os.linesep)

	for i in range(n):
		my_dict = make_person()
		append_record(my_dict,fname)