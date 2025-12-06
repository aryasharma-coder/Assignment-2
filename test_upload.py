import requests

url = 'http://127.0.0.1:5000/upload'
files = {'file': open('test_image.png', 'rb')}  # put a test_image.png in same folder
response = requests.post(url, files=files)
print(response.status_code, response.text)
