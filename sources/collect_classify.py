import email
import sys
import time
from retrieve_image_mail import EmailParser
import io
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os


def credential():
        f = open("/mnt/data/workspace/bird_classification/data/credential.txt")
        user = f.readline().strip("\n")
        passwd = f.readline().strip("\n")
        f.close()
        return user, passwd

# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    user_name, password = credential()
    email_parser = EmailParser(user_name, password)
    database_file = 'sqlite:////mnt/data/workspace/bird_classification/data/database.db'
    try:
        engine = create_engine(database_file, echo=False)
        last_data = pd.read_sql('dates', database_file)
        new_data = email_parser.get_todays_email()
        #email_parser.get_all_email().to_sql('dates', con=engine, if_exists='append')
        data_appened = np.append(np.array(last_data.iloc[:, 1]), np.array(new_data.iloc[:]))
        to_pandas = pd.DataFrame(data_appened).rename(columns={0: "dates"}).sort_values("dates", ascending=False).reset_index(drop=True)
        to_pandas.to_sql('dates', con=engine, if_exists='replace')
    except KeyboardInterrupt:
        sys.exit(0)
