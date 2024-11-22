import requests

data = {
    'room_type': 'Entire home/apt',
    'neighbourhood': 'SIXTH WARD',
    'latitude': 42.65222,
    'longitude': -73.76724,
    'minimum_nights': 2,
    'number_of_reviews': 302,
    'reviews_per_month': 2.53,
    'availability_365': 253
    }


url = 'http://localhost:9696/predict'
response = requests.post(url, json=data)
print(response.json())