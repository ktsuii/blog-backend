import requests

from settings import Config

# OpenAI API 请求参数
openai_params = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
}

# OpenAI API 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
}

# OpenAI API 请求地址
openai_api_url = "https://api.openai.com/v1/chat/completions"

try:
    response = requests.post(openai_api_url, json=openai_params, headers=headers)

    if response.status_code == 200:
        resp_info = response.json()
        msg = resp_info["choices"][0]["message"]['content']
        print(msg)
    else:
        print(f"OpenAI 请求失败，状态码: {response.status_code=}")
except Exception as e:
    print(f'OpenAI Unknown error: {e=}')
