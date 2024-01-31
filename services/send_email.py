import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

def create_email(sender, receiver, subject, body):
    email = EmailMessage()
    email['From'] = sender
    email['To'] = receiver
    # current_email['Bcc'] = 'andretorresdg@alumni.usp.br'
    email['Subject'] = subject
    email.set_content(body)
    return email

def send_email_with_attachments(receiver, filename):
    context = ssl.create_default_context()
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = receiver

    path_pasta_upload = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'website',
        'uploads'
    ).replace('\\', '/')
    
    with open(os.path.join(path_pasta_upload, filename), 'rb') as content_file:
        content = content_file.read()

    subject = "[Automação da geração de documentos ‘CONTRATO’]"
    
    body = """
    **Automação da geração de documentos ‘CONTRATO’!**

    Nome do documento em anexo:
    {}

    """.format(filename)

    current_email = create_email(email_sender, email_receiver, subject, body)
    current_email.add_attachment(content, maintype='application', subtype='pdf', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        try:
            smtp.send_message(current_email)
        except Exception as e:
            print(f"Mail failed: {e}")

    os.remove(os.path.join(path_pasta_upload, filename))
