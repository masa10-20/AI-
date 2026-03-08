import os
import requests
import json
from datetime import datetime, timedelta
import google.generativeai as genai

# GitHub Secretsから取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Geminiの初期化
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_news_summary():
    """最新のAI関連ニュースを検索して要約する"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    prompt = f"""
    最新のAI関連ニュース（{yesterday}から本日まで）を以下の構成で合計5件ピックアップし、
    日本のユーザー向けに分かりやすく要約してください。
    
    【構成】
    1. 生成AI関連（画像生成、動画生成、LLMなど）：3件
    2. その他のAI関連（ロボティクス、医療AI、AI規制、ハードウェアなど）：2件
    
    フォーマット：
    【AIニュースまとめ】 (日付)
    
    ■ 生成AI関連 (3件)
    1. [ニュースタイトル]
    要約内容...
    
    2. [ニュースタイトル]
    要約内容...
    
    3. [ニュースタイトル]
    要約内容...
    
    ■ その他のAI関連 (2件)
    4. [ニュースタイトル]
    要約内容...
    
    5. [ニュースタイトル]
    要約内容...
    
    最後に「今日も一日頑張りましょう！」と一言添えてください。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ニュースの取得中にエラーが発生しました: {str(e)}"

def send_line_message(text):
    """LINE Messaging APIを使用してメッセージを送信する"""
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
        response = requests.post(url, headers=headers, data=json.dumps(payload ))
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
