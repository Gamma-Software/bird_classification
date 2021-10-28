import email
import sys
import time
from retrieve_image_mail import EmailParser
import io
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def credential():
        f = open("data/credential.txt")
        user = f.readline().strip("\n")
        passwd = f.readline().strip("\n")
        f.close()
        return user, passwd


# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    user_name, password = credential()
    email_parser = EmailParser(user_name, password)
    try:
        engine = create_engine('sqlite:///data/database.db', echo=False)
        email_parser.get_todays_email().to_sql('date', con=engine, if_exists='replace')
    except KeyboardInterrupt:
        sys.exit(0)
