from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.error
import json

app = Flask(__name__)

GEMINI_API_KEY = "توکن جمنای و اینجا بذارید"
MODEL_NAME = "gemini-3.5-flash-lite"  # مدل سبک و با quota رایگان بیشتر


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({'response': 'لطفاً پیامی بنویسید.'})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
        bot_response = res_data['candidates'][0]['content']['parts'][0]['text']

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        if e.code == 429:
            bot_response = "متأسفم، سقف استفاده‌ی رایگان امروز پر شده. لطفاً کمی بعد دوباره امتحان کن."
        elif e.code == 404:
            bot_response = "خطا: مدل انتخاب‌شده در دسترس نیست."
        else:
            bot_response = f"خطای HTTP {e.code}: {error_body}"

    except urllib.error.URLError as e:
        bot_response = f"خطای شبکه: {str(e)}"

    except Exception as e:
        bot_response = f"خطای غیرمنتظره: {str(e)}"

    return jsonify({'response': bot_response})
