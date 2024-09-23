import requests

response = requests.post('https://httpbin.org/post', json={'key':'value'})
json_response = response.json()
print(json_response)
print(json_response['data'])

response = requests.get('https://httpbin.org/get', params={'key1':'value1', 'key2':'value2'})
print(response.status_code)
print(response.url)
print(response.text)
print(response.json())
print(response.headers)

