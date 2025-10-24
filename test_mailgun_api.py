import os
import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox164383bdb1864606b4c832581a4e2b83.mailgun.org/messages",
        auth=("api", os.getenv('API_KEY', 'API_KEY')),
        data={"from": "Mailgun Sandbox <postmaster@sandbox164383bdb1864606b4c832581a4e2b83.mailgun.org>",
              "to": "Ajaz jamadar <ajaxjamadar121@gmail.com>",
              "subject": "Hello Ajaz jamadar",
              "text": "Congratulations Ajaz jamadar, you just sent an email with Mailgun! You are truly awesome!"})

if __name__ == "__main__":
    print("Sending test email via Mailgun API...")
    response = send_simple_message()
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("✓ Email sent successfully!")
    else:
        print("✗ Failed to send email")
