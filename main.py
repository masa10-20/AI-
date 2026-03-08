import os
import requests
import json
from datetime import datetime, timedelta
from google import genai

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_news_summary():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    prompt = f"最新のAI関連ニュース（{yesterday}から本日まで）を生成AI関連3件、その他2件の計5件で要約してください。"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text if response.text else "ニュースの取得に失敗しました。"
    except Exception as e:
        return f"ニュースの取得中にエラーが発生しました: {str(e)}"

def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": text}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

def main():
    summary = get_ai_news_summary()
    status_code, response_text = send_line_message(summary)
    if status_code == 200:
        print("Successfully sent the news to LINE.")
    else:
        print(f"Failed: {status_code}, {response_text}")

if __name__ == "__main__":
    main()
