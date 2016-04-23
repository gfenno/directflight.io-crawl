# -*- coding: utf-8 -*-
#!/usr/bin/python
import requests
import boto3
from bs4 import BeautifulSoup, UnicodeDammit
import string

#put a list of the current airports into dynamodb
# db = boto3.client('dynamodb')

# f = file.open('./')

# # Visit all airport Wiki Lists sorted by IATA code
# for letter in list(string.ascii_uppercase):
# 	print "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_" + letter

r = requests.get("https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_A")
soup = BeautifulSoup(r.text.encode('utf-8',errors='ignore'),"html.parser")

data = []
table = soup.find("table")
table_rows = table.find_all('tr')
for row in table_rows:
	cols = row.find_all('td')
	for item in cols:
		if item != None:
			# print item
			data.append(cols)

print data[0]
