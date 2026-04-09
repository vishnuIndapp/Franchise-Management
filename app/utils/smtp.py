import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to_email: str, otp: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = "Your OTP Code"

        body = f""" 
        Your OTP code is: {otp}
        This code is valid for 5 minutes.
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()


        return True
    except Exception as e:
    
        print("Error sending email:", str(e))
        return False

