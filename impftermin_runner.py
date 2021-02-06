import os
import smtplib
import socket
from email.message import EmailMessage

import yaml

from impftermin_website import ImpfterminWebsite

if __name__ == "__main__":
    mail_body = ""
    send_email = False

    config_file_path = f'{os.path.dirname(os.path.realpath(__file__))}/config.yml'
    if not os.path.isfile(config_file_path):
        raise Exception("Please create config.yml first")

    config = None
    with open(config_file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Step 1: Check appointment availability information from website
    with ImpfterminWebsite(config['url_1'], headless=False) as iw_1:
        iw_1.open_website()
        # Step 2: If there is a first appointment available, check for availability of second appointment
        if iw_1.has_available_slot():
            with ImpfterminWebsite(config['url_2'], headless=False) as iw_2:
                iw_2.open_website()
                if iw_2.has_available_slot():
                    send_email = True
                    mail_body += "Es besteht die Moeglichkeit beide Impftermine zu buchen! Bitte schnell buchen:\n\n"
                    mail_body += f"- Termin 1: {config['url_1']}"
                    mail_body += f"- Termin 2: {config['url_2']}"
                else:
                    mail_body += "Kein 2. Impftermin verfuegbar"
        else:
            mail_body += "Kein 1. Impftermin verfuegbar"

    # Step 3: Send email about latest updates
    print(mail_body)
    if send_email:
        mailserver = None
        try:
            mailserver = smtplib.SMTP(
                config['smtp_server'], config['smtp_port'])
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.login(config['smtp_user'], config['smtp_pw'])

            from_email_address = config['from_email']
            to_email_addresses = config['to_email']

            msg = EmailMessage()
            msg.set_content(mail_body)
            msg['From'] = from_email_address
            msg['To'] = to_email_addresses
            msg['Subject'] = 'Impftermine verfuegbar!'

            mailserver.sendmail(from_addr=from_email_address,
                                to_addrs=to_email_addresses, msg=msg.as_string())
        except socket.gaierror as e:
            print("Socket issue while sending email - Are you in VPN/proxy?")
            raise e
        except Exception as e:
            print(f"Something went wrong while sending an email: {e}")
            raise e
        finally:
            if mailserver != None:
                mailserver.quit()
