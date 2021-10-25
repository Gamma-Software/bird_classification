import sys
import time
import retrieve_image_mail
import detection_classification as dc
from PIL import Image
import io
import cv2 

def credential():
        f = open("data/credential.txt")
        user = f.readline()
        passwd = f.readline()
        f.close()
        return user, passwd


# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    user_name, password = credential()
    try:
        #images = retrieve_image_mail.download_images(user_name, password)
        #[print(dc.detect_bird(image)) for image in images]
        #image = Image.open("tests/data/01.jpg")
        src = cv2.imread("tests/data/02.jpg")
        image = cv2.cvtColor(src, cv2.COLOR_BGR2RGB )
        print(dc.detect_bird(image))

        sys.exit(0)
        while True:
            bird_classified = [classify(module, image) for image in image_cropped]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
