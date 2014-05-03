import sys
import os
import android
import emailer
from datetime import datetime
from variables import *
import shutil


def get_vars(droid):
    try:
        email_name = droid.getIntent().result[u'extras'][u'%EMAIL_NAME']
    except:
        email_name = ''
      
    try:
        email_user = droid.getIntent().result[u'extras'][u'%EMAIL_USER']
    except:
        droid.makeToast('EMAIL_USER missing')
        sys.exit(1)
      
    try:
        email_pswd = droid.getIntent().result[u'extras'][u'%EMAIL_PSWD']
    except:
        droid.makeToast('EMAIL_PSWD missing')
        sys.exit(1)
      
    try:
        mailto = droid.getIntent().result[u'extras'][u'%EMAIL_TO']
    except:
        droid.makeToast('EMAIL_TO missing')
        sys.exit(1)
            
    try:
        body = droid.getIntent().result[u'extras'][u'%EMAIL_BODY']
    except:
        curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        body = 'Break-in attempt by this fool at %s' % curr_time
      
    return email_name, email_user, email_pswd, mailto, body


def send_email(directory):
    email_name, email_user, email_pswd, mailto, body = get_vars(droid)
    subject = 'Break-in attempt at %s - sending now that I have interwebs' % directory
    images = os.listdir(os.path.join(BACKUP_IMAGES_PATH, directory))
    images = [os.path.join(BACKUP_IMAGES_PATH, directory, x) for x in images]

    try:
        emailer.sendemail(email_name, email_user, email_pswd, mailto, subject, body, images)
    except Exception as err:
        with open(os.path.join(LOG_PATH, FAILED_EMAIL_LOG), 'a') as f:
            f.write('%s\n' % str(err))
        droid.makeToast('email failed')



if __name__ == '__main__':
    droid = android.Android()
    directories = os.listdir(BACKUP_IMAGES_PATH)
 
    if directories:
        if emailer.internet_is_on():
            for directory in directories:
                send_email(directory)
                shutil.rmtree(os.path.join(BACKUP_IMAGES_PATH, directory))
        else:
            curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            with open(os.path.join(LOG_PATH, MAIN_LOG), 'a') as f:
                f.write('%s -- There are emails to send, but no internet connection still.\n' % curr_time)