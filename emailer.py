import smtplib
import mimetypes
import glob
import os
import urllib2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

CONNECTION_TIMEOUT = 10 # How long we wait for an internet connection before failing out
TEST_URL = 'http://74.125.228.100' # The url we test for connectivity; defaults to a Google IP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def attach_files(msg, attachments):
    for attachment in attachments:
        attachment = attachment.strip()
        for path in glob.glob(attachment):
            filename = os.path.basename(path)
            if not os.path.isfile(path):
                continue
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                # Note: we should handle calculating the charset
                part = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(path, 'rb')
                part = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(path, 'rb')
                part = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(path, 'rb')
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(part)
            # Set the filename parameter
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(part)


def sendemail(email_name, email_user, email_pswd, mailto, subject, body, attachments):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = mailto
    msg['From'] = email_name + " <" + email_user + ">"
    msg.attach(MIMEText(body, 'plain'))
    attach_files(msg, attachments)

    # Attempt to connect and send the email
    smtpObj = ''
    # Check for SMTP over SSL by port number and connect accordingly
    if( SMTP_PORT == 465):
        smtpObj = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
    else:
        smtpObj = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    smtpObj.ehlo()
    # StartTLS if using the default TLS port number
    if(SMTP_PORT == 587):
        smtpObj.starttls()
        smtpObj.ehlo
    # Login, send and close the connection.
    smtpObj.login(email_user, email_pswd)
    smtpObj.sendmail(email_user, mailto, msg.as_string())
    smtpObj.close()
    return True


def internet_is_on():
    '''
    Checks if we have an internet connection. A problem with the original script is if you weren't connected
    to WiFi or data, things would just fail.

    http://stackoverflow.com/questions/3764291/checking-network-connection
    '''

    try:
        response = urllib2.urlopen(TEST_URL, timeout=CONNECTION_TIMEOUT)
        return True
    except urllib2.URLError:
        return False
