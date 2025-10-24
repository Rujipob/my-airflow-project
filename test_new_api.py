import requests

url = "https://opend.data.go.th/get-ckan/datastore_search"
params = {
    'resource_id': 'a7ce8130-e941-4b46-901c-9fb12ca1d855',  # Zoo Visitors 2568
    'limit': 5
}
headers = {
    'api-key': 'iFWOIOiQvAKwxrdzQtHEctOZyQvuoSgw'
}

print("Testing new API endpoint...")
print(f"URL: {url}")
print(f"Resource ID: {params['resource_id']}")
print()

response = requests.get(url, params=params, headers=headers)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Total records: {data.get('result', {}).get('total', 0)}")
    print(f"Records returned: {len(data.get('result', {}).get('records', []))}")
    
    if data.get('result', {}).get('records'):
        print("\nFirst record sample:")
        first_record = data['result']['records'][0]
        print(f"Keys: {list(first_record.keys())[:5]}...")
else:
    print(f"Error: {response.text}")
