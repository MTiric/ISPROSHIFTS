import smtplib
import ssl
from email.message import EmailMessage
import pyDBcheckHZPPprod as main

import mailovi




# Define email sender and receiver
email_sender = 'jenkinsmtiric@gmail.com'
email_password = 'hoxaomqupdadaswv'
email_receiver = mailovi.mailingLista


# Set the subject and body of the email
subject = 'DATABASE SHIFT EXPORT'
body = """
No new WEB or Smartphone shifts in database in more than 2 hours!
"""
stringsatiWEB="WEB sati: " + str(main.hoursWEB)
stringsatiSmartphone="\nSmartphone sati: " + str(main.hoursSmartPhone)
body=body+stringsatiWEB+stringsatiSmartphone

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

print("Poslan mail za WEB 2h")