from datetime import datetime, date, timedelta
import requests, json

auth_url = "https://api.makcorps.com/auth"
headers = {"Content-Type": "application/json"}
data = '{"username": "jonathandown","password": "3cF%Jm526wR6tdJ"}'

authentication_result = requests.post(auth_url, headers=headers, data=data)

auth_key = authentication_result.json()['access_token']

search_url = "https://api.makcorps.com/free/london"
headers = {'Authorization': f'JWT {auth_key}'}

results = requests.get(search_url, headers=headers).json()

with open('data.json', 'w') as f:
    json.dump(results, f)

# results = requests.post(search_url, headers=headers, data=data)
# print(r.json())