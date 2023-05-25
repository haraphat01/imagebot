# import requests
# import json

# # Replace 'YOUR_TELEGRAM_API_TOKEN' with your Telegram bot API token
# telegram_api_token = '6136916989:AAHMpyHlaDpCG9NiNgMYJUQJgjGlxFTj_OM'

# # Replace 'YOUR_DALLE_API_KEY' with your DALL·E API key
# dalle_api_key = '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'
import requests

# Replace 'YOUR_TELEGRAM_API_TOKEN' with your Telegram bot API token
telegram_api_token = 'laDJgjGlxFTj_OM'

# Replace 'YOUR_OPENAI_API_KEY' with your OpenAI API key
openai_api_key = 'RczBz'
openai_api_url = 'https://api.openai.com/v1/images/generations'

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{telegram_api_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()

def send_telegram_photo(chat_id, photo_url):
    url = f"https://api.telegram.org/bot{telegram_api_token}/sendPhoto"
    data = {
        'chat_id': chat_id,
        'photo': photo_url
    }
    response = requests.post(url, data=data)
    return response.json()

def generate_image(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

    data = {
        'prompt': prompt,
        'n': 2,
        'size': '1024x1024'
    }

    response = requests.post(openai_api_url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        urls = [result['url'] for result in response_json['data']]
        return urls
    return None

def process_telegram_message(message):
    chat_id = message['chat']['id']
    text = message['text']
    image_urls = generate_image(text)
    if image_urls:
        for url in image_urls:
            send_telegram_photo(chat_id, url)
    else:
        send_telegram_message(chat_id, "Image generation failed.")

def main():
    offset = None

    while True:
        url = f"https://api.telegram.org/bot{telegram_api_token}/getUpdates"
        params = {
            'offset': offset,
            'timeout': 60
        }
        response = requests.get(url, params=params)
        updates = response.json().get('result')

        if updates:
            for update in updates:
                process_telegram_message(update['message'])
                offset = update['update_id'] + 1

if __name__ == '__main__':
    main()
