import requests
import json
# [ key_scanner, classify, deep_classify, sentiment, sentiment_analysis, ictclas, key_extract, new_words_finder, summary, doc_extract, cluster, text_similarity, eye_checker ]
url = "https://online.lingjoin.com:5000/nlpir/request?instant=true&method=new_words_finder"



headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiXHU2YTBhXHU1YzExXHU3Njg3IiwidG9rZW5fZXhwaXJlIjoxODM5MTQyOTY4LCJhbGxvd19tZXRob2QiOlsiKiJdLCJqd3RfYWxnb3JpdGhtIjoiSFMyNTYiLCJ2ZXJpZnlfdG9rZW4iOiJkYjNhZTJhMmQ5MmRmODZiMzUwM2E1YzUzZmRhYzg0YjkyMmQ0Y2FlOWM5MzUwMWY0YTk2ZWY4MjA0NDliNjVmIiwiZW5jcnlwdF9rZXkiOiIzMTAyMmEwOTg0ZjJjMmM4YTk5NjBkMTgwYzk5YzJmNGMzMjRkN2VmNjk1OTkxMGFmY2QxYTQzOGI5ZGViZWYyYTZmNGY5OTJkMTZhMTRkZTQ1OTM2MjY4MjAyNTZhNzA2OGFhNWZjOSJ9.uUW6x78o_4AwJ4IotpsAoQ0isVzcHa5v2ZTfmZBpcqk'
}

def new_words_finder(data_list):
  payload = json.dumps({
  "data_type": "text",
  "data_list": data_list,
  # "data_list": [
  #   "用户访问前端页面时，前端页面的各个功能区通过各自的api接口向Django后端请求数据，",
  #   "用户访问前端页面时，前端页面的各个功能区通过各自的api接口向Django后端请求数据，"
  # ],
  "param": {
    "keys": 10
  }
})
  response = requests.request("POST", url, headers=headers, data=payload)
  return response.text


if __name__ == '__main__':
  a=new_words_finder(["前端页面的各个功能区通过各自的api接口向Dj", "前端页面的各个功能区通过各自的api接口向Dj"])
  print(a)