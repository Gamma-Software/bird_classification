import sys
import time
import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
import dl
from PIL import Image
import io


def classify(module, image):
    """Use the TensorFlow model to detect and classify the image of the bird"""
    if image:
        return module(image)
    return None

def credential():
        f = open("data/credential.txt")
        user = f.readline()
        passwd = f.readline()
        f.close()
        return user, passwd


# cherrypick from https://github.com/cmoon4/backyard_birdbot/blob/main/bird_detect.py
if __name__ == "__main__":
    module = hub.KerasLayer('https://tfhub.dev/google/aiy/vision/classifier/birds_V1/1')
    user_name, password = credential()
    try:
        images = dl.download_images(user_name, password)
        image_cropped = [image.crop((450, 200, 900, 800)).resize([224, 244]) for image in images]
        bird_classified = [classify(module, image) for image in image_cropped]
        print(bird_classified)
        sys.exit(0)
        while True:
            bird_classified = [classify(module, image) for image in image_cropped]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
