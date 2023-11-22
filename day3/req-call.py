import requests
headers = {
'X-Auth-Header': ''
}
response = requests.get('http://localhost:5000/api/employee/1', headers=headers) #sending get request
print(response.text)
