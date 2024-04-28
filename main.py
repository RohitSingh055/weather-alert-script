import os
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText

load_dotenv()

def fetch_weather(api_key, city):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    url = BASE_URL + "appid=" + api_key + "&q=" + city
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        html_template = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #64a0dc; color: #333333; padding: 20px;">
        <div class="container" style="max-width: 600px; margin: 0 auto;">
        <div class="header" style="background-color: #d8ecff; color: #333333; padding: 20px; border-radius: 10px; text-align: center;">
            <span class="weather-icon cloud-icon" style="font-size: 35px; margin-right: 10px; color: #bbb;">&#9729;</span>
            <span class="weather-icon sun-icon" style="font-size: 35px; margin-right: 10px; color: #f7d328;">&#9728;</span>
            <span class="weather-icon rain-icon" style="font-size: 35px; margin-right: 10px; color: #4caf50;">&#9730;</span>
            <span class="weather-icon snow-icon" style="font-size: 35px; margin-right: 10px; color: #99aabb;">&#10052;</span>
            <span class="weather-icon thunderstorm-icon" style="font-size: 35px; margin-right: 10px; color: #9966ff;">&#9889;</span>
            <h1 style="text-align: center; background-color: #d8ecff; font-size: 25px; font-weight: bold;">Weather Notification</h1>
        </div>
        <div class="content" style="padding: 20px; background-color: #FFFFFF; border-radius: 10px; margin-top: 20px;">
            <ul class="message" style="font-size: 18px; line-height: 1.5; list-style-type: none; padding: 0;">
                {message}
            </ul>
        </div>
        <div class="footer" style="text-align: center; margin-top: 40px; font-size: 16px; color: #090909;">Awesome Mausam &copy; 2024 All rights reserved.</div>
        </div>
        </body>
        </html>
        """.format(message=message)

        msg = MIMEText(html_template, 'html')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        server.sendmail(sender_email, recipient_email, msg.as_string())

        server.quit()

    except Exception as e:
        print(f"Error sending email notification: {e}")


def check_weather_and_notify(api_key, city, sender_email, sender_password, recipient_email):
    weather_data = fetch_weather(api_key, city)
    if weather_data:
        weather_main = weather_data['weather'][0]['main']
        temp = weather_data['main']['temp'] - 273.15
        feels_like = weather_data['main']['feels_like'] - 273.15
        wind_speed = weather_data['wind']['speed']

        # Formatting the message
        message = f"<li>Weather: {weather_main}</li>"
        message += f"<li>Temperature: {temp:.1f}°C</li>"
        message += f"<li>Feels like: {feels_like:.1f}°C</li>"
        message += f"<li>Wind Speed: {wind_speed} m/s</li><br>"

        # Checking for heat waves
        if temp > 39.5:
            subject = f"Extreme Heat Wave Alert: {city}"
            message += "\n\nExtreme heat wave conditions are forecasted. Stay indoors and keep hydrated!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for rain
        elif weather_main == 'Rain':
            subject = f"Weather Alert: Rain in {city}"
            message += "\nIt's currently raining. Stay dry and safe!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for thunderstorm
        elif weather_main == 'Thunderstorm':
            subject = f"Weather Alert: Thunderstorm in {city}"
            message += "\nThunderstorm conditions are forecasted. Stay indoors and away from windows!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for snow
        elif weather_main == 'Snow':
            subject = f"Weather Alert: Snow in {city}"
            message += "\nIt's currently snowing. Stay warm and safe!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for extreme weather
        elif weather_main == 'Extreme':
            subject = f"Weather Alert: Extreme Weather in {city}"
            message += "\nExtreme weather conditions are forecasted. Please take necessary precautions!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for foggy/misty weather
        elif weather_main == 'Foggy' or weather_main == 'Misty':
            subject = f"Weather Alert: Fog/Mist in {city}"
            message += "\nIt's currently foggy/misty. Drive safely and use headlights!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")

        # Checking for windy weather
        elif wind_speed > 20:  # Adjust the threshold for abnormal wind speed as needed
            subject = f"Weather Alert: Windy Weather in {city}"
            message += f"\nWind speed is {wind_speed} m/s, which is abnormal. Exercise caution while outdoors!"
            send_email(sender_email, sender_password, recipient_email, subject, message)
            print(f"Email notification sent successfully! Recipient: {recipient_email}, City: {city}")
        else:
            print("No weather alerts.")

    else:
        print("Failed to fetch weather data.")


api_key = os.getenv('OPENWEATHER_API_KEY')

# Database work starts from here
api_endpoint = 'https://cloud.appwrite.io/v1'
project_id = os.getenv('PROJECT_ID')
collection_id = os.getenv('COLLECTION_ID')
secret_key = os.getenv('SECRET_KEY')
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')



from appwrite.client import Client
from appwrite.services.databases import Databases

client = Client()
client.set_endpoint(api_endpoint)
client.set_project(project_id)
client.set_key(secret_key)

databases = Databases(client)

def get_records():
  records = databases.list_documents(
    database_id = os.getenv('DATABASE_ID'),
    collection_id= os.getenv('COLLECTION_ID')
  )
  for item in records['documents']:
        email = item.get('email')
        city = item.get('city')
        check_weather_and_notify(api_key, city, sender_email, sender_password, email)


get_records()