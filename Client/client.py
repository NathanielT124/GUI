# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:28:34 2022

@author: natha
"""

import requests
import json

people_string = '''
{
 "people": [
     {
      "name": "Nathaniel Thomas",
      "phone": "512-952-1017",
      "emails": ["nathaniel@swbell.net", "nathanielt124@gmail.com"],
      "has_license": false
      },
     {
      "name": "John Mane",
      "phone": "512-327-1182",
      "emails": ["john@hotmail.com", "jmane@gmail.com"],
      "has_license": true
      }
     ]
 }
'''

data = json.loads(people_string)

for person in data['people']:
    del person['phone']

new_string = json.dumps(data, indent=2, sort_keys=True)

# print(new_string)

with open('states.json') as f:
    data = json.load(f)
    
with open('new_states.json', 'w') as f:
    json.dump(data, f, indent=2, sort_keys=True)
    
res = requests.get("http://localhost:5000/drinks/1")
data = res.json()

print(data['name'])

