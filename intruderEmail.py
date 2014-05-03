import os
import sys
import android
import emailer
from datetime import datetime
from variables import *


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
        subject = droid.getIntent().result[u'extras'][u'%EMAIL_SUBJECT']
    except:
        subject = ''
      
    try:
        body = droid.getIntent().result[u'extras'][u'%EMAIL_BODY']
    except:
        curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        body = 'Break-in attempt by this fool at %s' % curr_time
      
    try:
        attachments = droid.getIntent().result[u'extras'][u'%EMAIL_ATTACH']
        attachments_list = [os.path.join(IMAGE_PATH, x) for x in attachments.split(',')]
    except:
        attachments_list = ''

    return email_name, email_user, email_pswd, mailto, subject, body, attachments_list


def backup_images(images):
    '''
    If we don't have an internet connection, we can backup the images so that a second task that runs every 10 minutes
    can check for unsent images, and send when a connection is available
    '''
    curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    backup_path = os.path.join(BACKUP_IMAGES_PATH, curr_time)
    os.makedirs(backup_path)
    for image in images:
        file_name = os.path.basename(os.path.normpath(image))
        new_image_path = os.path.join(backup_path, file_name)
        os.rename(image, new_image_path)

if __name__ == '__main__':
    if os.path.exists(LOG_PATH) == False:
        os.makedirs(LOG_PATH)
    
    droid = android.Android()
    email_name, email_user, email_pswd, mailto, subject, body, attachments_list = get_vars(droid)
    if(emailer.internet_is_on()):
        try:
            emailer.sendemail(email_name, email_user, email_pswd, mailto, subject, body, attachments_list)
        except Exception as err:
            with open(os.path.join(LOG_PATH, FAILED_EMAIL_LOG), 'a') as f:
                f.write(str(err))
            droid.makeToast('email failed')
            sys.exit(1)
    else:
        curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        with open(os.path.join(LOG_PATH, MAIN_LOG), 'a') as f:
            f.write('%s -- No internet connection. Backing up images for later sending.\n' % curr_time)
        backup_images(attachments_list)