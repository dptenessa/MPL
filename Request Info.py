import requests

url = "http://127.0.0.1:5000/events?param1=iPhone XS white&param2=128&param3=L&param4=T Centers&param5=GA&param6=Nothing&param7=24"
response = requests.get(url)
text = response.text

print(text)
