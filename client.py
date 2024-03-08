import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules import commons

def send_mail_notification(email_subject, email_body):
    """
    Gets Coordinates of City from OpenWeatherMap Geocoding API
    :param email_subject: Email address of the person that will receive the.
    :param email_body: Body of the mail that will be sent.
    """
    sender_email = commons.get_data_from_config("email_address")
    receiver_email = commons.get_data_from_config("email_address")
    sender_password = os.getenv('EMAIL_PASSWORD')

    # https://support.google.com/a/answer/176600?hl=en
    # https://docs.python.org/3/library/smtplib.html
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 
 
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = email_subject

    message.attach(MIMEText(email_body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(sender_email, sender_password)
        
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully from {sender_email} to {receiver_email} \nSubject: \n{email_subject} \nBody: \n{email_body}")
    except smtplib.SMTPAuthenticationError:
        print("AUTH ERROR: Authentication failed. Check username and APP Password.")
    finally:
        server.quit()

if __name__ == "__main__":
    temperature = 15
    humidity = 15
    email_subject = "Weather Notification - Threshold exceeded"
    email_body = f"Temperature is {temperature}°C and Humidity is {humidity}%"

    send_mail_notification(email_subject, email_body)