import requests

data = {
    'room_type': 'Entire home/apt',
    'neighbourhood': 'SIXTH WARD',
    'minimum_nights': 2,
    'number_of_reviews': 302,
    'reviews_per_month': 2.53,
    'calculated_host_listings_count': 4,
    'availability_365': 253,
    'number_of_reviews_ltm': 16
    }


url = 'http://localhost:9696/predict'
response = requests.post(url, json=data)
print(response.json())