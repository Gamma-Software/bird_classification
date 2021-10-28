import sys
import time
import retrieve_image_mail
import detection_classification as dc
import tensorflow.compat.v2 as tf
from PIL import Image
import io
import cv2 

import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

import numpy as np

def credential():
        f = open("data/credential.txt")
        user = f.readline()
        passwd = f.readline()
        f.close()
        return user, passwd


def display_image(image):
    fig = plt.figure(figsize=(20,15))
    plt.grid(False)
    plt.imshow(image)


# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    user_name, password = credential()
    try:
        #images = retrieve_image_mail.download_images(user_name, password)
        #[print(dc.detect_bird(image)) for image in images]
        #image = Image.open("tests/data/01.jpg")
        src = cv2.imread("tests/data/04.jpg")
        image = cv2.cvtColor(src, cv2.COLOR_BGR2RGB )
        image_converted = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
        result, res = dc.detect_bird(image_converted)
        result_plt={key:value.numpy() for key,value in result.items()}
        num_bird=np.size(res["names"])
        box_indices=tf.zeros(shape=(num_bird,),dtype=tf.int32)  
        cropped_img=tf.image.crop_and_resize(image_converted,res["boxes"],box_indices,[224,224])
        display_image(cropped_img)

        sys.exit(0)
        while True:
            bird_classified = [classify(module, image) for image in image_cropped]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
