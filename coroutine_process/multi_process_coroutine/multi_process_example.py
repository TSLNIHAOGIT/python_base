import requests
import time

start = time.time()

def request():
    url = 'http://127.0.0.1:5000'
    print('Waiting for', url)
    result = requests.get(url).text
    print('Get response from', url, 'Result:', result)

for _ in range(100):
    request()

end = time.time()
print('Cost time:', end - start)