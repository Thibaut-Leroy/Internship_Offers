from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime as dt
import os


def email_sender(filename):

    # Paramètres du serveur SMTP
    smtp_server = 'smtp-mail.outlook.com'  # Remplacez par votre serveur SMTP
    smtp_port = 587  # Port SMTP (habituellement 587 ou 465)
    smtp_user = 'thibaut.leroy@edhec.com'  # Remplacez par votre adresse email
    smtp_password = 'Vyruna*428700'  # Remplacez par votre mot de passe

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'thibaut.leroy@edhec.com'
    day_date = str(dt.date.today())
    msg['Subject'] = 'Offres de stage SG + CACIB -' + day_date

    # Corps du message
    body = 'Ci-joint, les offres de stage SG et CACIB en date du ' + day_date
    msg.attach(MIMEText(body, 'plain'))

    # Pièce jointe
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
    msg.attach(part)
    attachment.close()

    # Connexion au serveur SMTP et envoi de l'email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Sécurisation de la connexion
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(smtp_user, 'thibaut.leroy@edhec.com', text)
    server.quit()
    
    print("Mail envoyé")

if __name__ == "__main__":
    email_sender()
