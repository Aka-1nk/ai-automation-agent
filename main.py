from flask import Flask, request, render_template_string
import requests
import smtplib
import re

# 🔑 ADD YOUR KEYS HERE
WEATHER_API_KEY = "c04aac96dd31b391df363c4007f89f2a"

app = Flask(__name__)

# 🌦️ Fetch real weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if "main" in response:
        temp = response['main']['temp']
        humidity = response['main']['humidity']
        condition = response['weather'][0]['description']

        return f"""City: {city}
Temperature: {temp}°C
Humidity: {humidity}%
Condition: {condition}
"""
    else:
        return "City not found. Try again."


# 📧 Send email
from email.mime.text import MIMEText

def send_email(content):
    sender = "akankshat2005@gmail.com"
    receiver = "akankshatschool@gmail.com"
    password = "fvru vdbx zalz hmex"

    try:
        print("➡️ Connecting to server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        print("➡️ Logging in...")
        server.login(sender, password)

        print("➡️ Preparing message...")
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = "Weather Report"
        msg["From"] = sender
        msg["To"] = receiver

        print("➡️ Sending email...")
        server.sendmail(sender, receiver, msg.as_string())

        server.quit()
        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:", e)


# 🧠 Extract city
def extract_city(user_input):
    match = re.search(r"in ([a-zA-Z]+)", user_input.lower())
    if match:
        return match.group(1).capitalize()
    return "Chennai"


# 🧠 Intent detection
def get_intent(user_input):
    user_input = user_input.lower()

    if ("send" in user_input or "email" in user_input) and "weather" in user_input:
        return "email"
    elif "weather" in user_input:
        return "weather"
    else:
        return "general"


# 🌐 Web UI
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        user_input = request.form["input"]

        intent = get_intent(user_input)
        city = extract_city(user_input)

        if intent == "weather":
            result = get_weather(city)

        elif intent == "email":
            data = get_weather(city)
            send_email(data)
            result = f"Weather report sent for {city}! (Check inbox/spam)"

        else:
            result = "Try: 'weather in Mumbai' or 'send weather in Delhi'"

    return render_template_string("""
        <h2>AI Automation Agent</h2>
        <form method="post">
            <input name="input" placeholder="Type request" style="width:300px;">
            <button>Submit</button>
        </form>
        <pre>{{result}}</pre>
    """, result=result)


app.run(debug=True)