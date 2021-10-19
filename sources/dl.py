# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.

import email
import getpass, imaplib
import os
import sys

def download_images(user_name=None, password=None):
    """
    Download the images using Gmail
    @param user_name: User name of the Gmail account
    @param password: password of the Gmail account
    """
    if not user_name or not password:
        raise "no credential provided"
    try:
        imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
        typ, accountDetails = imapSession.login(user_name, password)
        if typ != 'OK':
            raise 'Not able to sign in!'
        
        imapSession.select("INBOX")
        typ, data = imapSession.search(None, 'ALL')
        if typ != 'OK':
            raise 'Error searching Inbox.0'
        
        filenames = []
        for num in data[0].split():
            typ, data = imapSession.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
            # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            # downloading attachments
            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet... 
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filenames.append(part.get_payload(decode=True))
        imapSession.close()
        imapSession.logout()
    except :
        print('Not able to download all attachments.')
    if filenames == []:
        return [None]
    else:
        return filenames