import smtplib
import requests

def send_email_alert(sender, password, receiver, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        email = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender, receiver, email)
        server.quit()
    except:
        pass


def send_slack_alert(webhook_url, message):
    try:
        requests.post(webhook_url, json={"text": message})
    except:
        pass


def send_teams_alert(webhook_url, message):
    try:
        requests.post(webhook_url, json={"text": message})
    except:
        pass
