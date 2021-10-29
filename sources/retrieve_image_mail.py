# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.

import email
import imaplib
from PIL import Image
import io
import pandas as pd
import datetime

class EmailParser():
    def __init__(self, user_name=None, password=None):
        self.user_name = user_name
        self.password = password

    def get_total_nb_mail(self):
        """
        Get the email metadata between to dates
        """
        if not self.user_name or not self.password:
            raise "no credential provided"
        total_nb_email = 0
        try:
            imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
            typ, _ = imapSession.login(self.user_name, self.password)

            if typ != 'OK':
                raise 'Not able to sign in!'
            
            total_nb_email = int(imapSession.select("INBOX")[1][0])
        except:
            print('Not able to download metadatas')
        finally:
            imapSession.close()
            imapSession.logout()
        return total_nb_email

    def get_todays_email(self):
        """
        Get the email metadata between to dates
        """
        if not self.user_name or not self.password:
            raise "no credential provided"
        todays_email = []
        try:
            imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
            typ, accountDetails = imapSession.login(self.user_name, self.password)

            if typ != 'OK':
                raise 'Not able to sign in!'
            
            imapSession.select("INBOX")
            typ, data = imapSession.search(None, 'ALL')
            if typ != 'OK':
                raise 'Error searching Inbox.0'
            for data in reversed(data[0].split()): # fetching is sorted by date
                typ, data = imapSession.fetch(data, '(RFC822)')
                raw_dates = data[0][1].decode('utf-8').split("\n")[7][6:-13]
                tz = int(data[0][1].decode('utf-8').split("\n")[7][-13:-9])
                date = datetime.datetime.strptime(raw_dates, "%a, %d %b %Y %H:%M:%S") - datetime.timedelta(hours= tz)
                if date.day == datetime.datetime.today().day:
                    todays_email.append(date)
                else:
                    break # no need to continue
        except:
            print('Not able to download metadatas')
        finally:
            imapSession.close()
            imapSession.logout()
        return pd.DataFrame(todays_email, columns=["dates"])
    
    def get_all_email(self):
        """
        Get the email metadata between to dates
        """
        if not self.user_name or not self.password:
            raise "no credential provided"
        emails = []
        imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
        typ, accountDetails = imapSession.login(self.user_name, self.password)

        if typ != 'OK':
            raise 'Not able to sign in!'
        
        imapSession.select("INBOX")
        typ, data = imapSession.search(None, 'ALL')
        if typ != 'OK':
            raise 'Error searching Inbox.0'
        for data in reversed(data[0].split()): # fetching is sorted by date
            typ, data = imapSession.fetch(data, '(RFC822)')
            try:
                raw_dates = data[0][1].decode('utf-8').split("\n")[7][6:-13]
                tz = int(data[0][1].decode('utf-8').split("\n")[7][-13:-9])
                date = datetime.datetime.strptime(raw_dates, "%a, %d %b %Y %H:%M:%S") - datetime.timedelta(hours= tz)
                emails.append(date)
            except:
                print("decoding failed")

        imapSession.close()
        imapSession.logout()
        return pd.DataFrame(emails, columns=["dates"])

    def download_images(self):
        """
        Download the images using Gmail
        @param user_name: User name of the Gmail account
        @param password: password of the Gmail account
        @return a PIL image
        """
        if not self.user_name or not self.password:
            raise "no credential provided"
        try:
            imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
            typ, accountDetails = imapSession.login(self.user_name, self.password)
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
                        filenames.append(Image.open(io.BytesIO(part.get_payload(decode=True))))
            imapSession.close()
            imapSession.logout()
        except :
            print('Not able to download all attachments.')
        if filenames == []:
            return [None]
        else:
            return filenames