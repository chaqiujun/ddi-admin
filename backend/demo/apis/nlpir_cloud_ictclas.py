import requests
import json

url = "https://online.lingjoin.com:5000/nlpir/request?instant=true&method=ictclas"

payload = json.dumps({
  "data_type": "text",
  "data_list": [
    "支持多人异地异时协同标注",
    "支持多人异地异时协同标注"
  ],
  "param": {
    "POS": "true"
  }
})

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiXHU2YTBhXHU1YzExXHU3Njg3IiwidG9rZW5fZXhwaXJlIjoxODM5MTQyOTY4LCJhbGxvd19tZXRob2QiOlsiKiJdLCJqd3RfYWxnb3JpdGhtIjoiSFMyNTYiLCJ2ZXJpZnlfdG9rZW4iOiJkYjNhZTJhMmQ5MmRmODZiMzUwM2E1YzUzZmRhYzg0YjkyMmQ0Y2FlOWM5MzUwMWY0YTk2ZWY4MjA0NDliNjVmIiwiZW5jcnlwdF9rZXkiOiIzMTAyMmEwOTg0ZjJjMmM4YTk5NjBkMTgwYzk5YzJmNGMzMjRkN2VmNjk1OTkxMGFmY2QxYTQzOGI5ZGViZWYyYTZmNGY5OTJkMTZhMTRkZTQ1OTM2MjY4MjAyNTZhNzA2OGFhNWZjOSJ9.uUW6x78o_4AwJ4IotpsAoQ0isVzcHa5v2ZTfmZBpcqk'
}

response = requests.request("POST", url, headers=headers, data=payload)
if __name__ == '__main__':
  print(response.text)