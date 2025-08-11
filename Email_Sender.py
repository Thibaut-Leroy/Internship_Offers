from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime as dt
import os


def email_sender(filename):

    # SMTP server params
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_user = 'MAIL'
    smtp_password = 'PASSWORD'

    # Message creation
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'MAIL'
    day_date = str(dt.date.today())
    msg['Subject'] = 'Internship Offers SG + CACIB -' + day_date

    # Text
    body = 'Find enclosed internships offers for SG and CACIB as of ' + day_date
    msg.attach(MIMEText(body, 'plain'))

    # Enclosure
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
    msg.attach(part)
    attachment.close()

    # Mail sending
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(smtp_user, 'MAIL', text)
    server.quit()
    
    print("Mail sent")

if __name__ == "__main__":
    email_sender()
