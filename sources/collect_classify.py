import sys
import time
from retrieve_image_mail import EmailParser
import io
import numpy as np


def credential():
        f = open("data/credential.txt")
        user = f.readline().strip("\n")
        passwd = f.readline().strip("\n")
        f.close()
        return user, passwd


# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    user_name, password = credential()
    try:
        #images = retrieve_image_mail.download_images(user_name, password)
        #[print(dc.detect_bird(image)) for image in images]
        #image = Image.open("tests/data/01.jpg")

        sys.exit(0)
        while True:
            bird_classified = [classify(module, image) for image in image_cropped]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
