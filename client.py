import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules import commons, db_tools


def send_mail_notification(email_subject, email_body):
    """
    Gets Coordinates of City from OpenWeatherMap Geocoding API
    :param email_subject: Email address of the person that will receive the.
    :param email_body: Body of the mail that will be sent.
    """
    sender_email = commons.get_data_from_config("email_address")
    receiver_email = commons.get_data_from_config("email_address")
    sender_password = os.getenv('EMAIL_PASSWORD')

    # DOCS: https://support.google.com/a/answer/176600?hl=en
    # DOCS: https://docs.python.org/3/library/smtplib.html
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
        print(
            f"Email sent successfully from {sender_email} to {receiver_email} \nSubject: {email_subject} \nBody: {email_body}")
    except smtplib.SMTPAuthenticationError:
        print("AUTH ERROR: Authentication failed. Check username and APP Password.")
    finally:
        server.quit()


if __name__ == "__main__":
    latest_data_row = 1
    prev_data_row = 2
    temperature_threshold = commons.get_data_from_config("temperature_threshold")
    humidity_threshold = commons.get_data_from_config("humidity_threshold")

    print(f"Fetching latest data from DB")
    temperature, humidity = db_tools.read_from_db(latest_data_row)
    print(f"Latest data: \nTemperature = {temperature} \nHumidity = {humidity}")
    print(f"Fetching previous data from DB")
    prev_temperature, prev_humidity = db_tools.read_from_db(prev_data_row)
    print(f"Latest data: \nTemperature = {prev_temperature} \nHumidity = {prev_humidity}")

    if temperature > prev_temperature + temperature_threshold or \
            temperature < prev_temperature - temperature_threshold or \
            humidity > prev_humidity + humidity_threshold or \
            humidity < prev_humidity - humidity_threshold:
        print("Threshold exceeded")
        email_subject = "Weather Notification - Threshold exceeded"
        email_body = f"Temperature is {temperature}°C and Humidity is {humidity}%"

        print("Sending email")
        send_mail_notification(email_subject, email_body)

    else:
        print("Within thresholds - will not send email")

    print("Updating previous temperature and humidity values in the DB")
    db_tools.write_to_db(temperature, humidity, prev_data_row)
