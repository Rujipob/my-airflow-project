import requests
import json

# Test different authentication methods
url = "https://opend.data.go.th/get-ckan/datastore_search"
params = {
    'resource_id': '15a9e41b-2f07-4b05-8e53-cb4119f24c7d',
    'q': 'jones'
}
token = 'iFWOIOiQvAKwxrdzQtHEctOZyQvuoSgw'

print("Testing different authentication methods:")
print("=" * 60)

# Method 1: Authorization header
print("\n1. Authorization header:")
response = requests.get(url, params=params, headers={'Authorization': token})
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Method 2: Authorization: Bearer
print("\n2. Authorization: Bearer header:")
response = requests.get(url, params=params, headers={'Authorization': f'Bearer {token}'})
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Method 3: api-key header (lowercase)
print("\n3. api-key header (lowercase):")
response = requests.get(url, params=params, headers={'api-key': token})
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Method 4: X-CKAN-API-Key header
print("\n4. X-CKAN-API-Key header:")
response = requests.get(url, params=params, headers={'X-CKAN-API-Key': token})
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# Method 5: Query parameter
print("\n5. Query parameter (api-key):")
params_with_key = params.copy()
params_with_key['api-key'] = token
response = requests.get(url, params=params_with_key)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Success: {data.get('success')}")
print(f"Total: {data.get('result', {}).get('total', 0)}")
print(f"Records: {len(data.get('result', {}).get('records', []))}")
if data.get('result', {}).get('records'):
    print(f"First record keys: {list(data['result']['records'][0].keys())}")
