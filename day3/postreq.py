import requests
data = {
'name': 'Srihari',
'address': 'Tirupati'
}
headers = {
'Content-Type': 'application/json',
'X-Auth-Header': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMsImlzcyI6IkRTQ0UiLCJzdWIiOiJFbXBsb3llZSBNaWNyb3NlcnZpY2UgVG9rZW4ifQ.Dpd6Wv1VojYbfOn_h9_0w7_gG0pVkZIUotvabiLc2EY'
}
response = requests.post('http://localhost:5000/api/employee/', json=data, headers=headers)
print(response.text)