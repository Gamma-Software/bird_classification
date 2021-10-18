import sys
import time, thread
import tensorflow.compat.v2 as tf
import tensorflow_hub as hub


def get_images():
    """
    Check whether there's an email triggered by the camera.
    Returns: a list of images, None if there is no images"""
    return [None]

def classify(module, image):
    """Use the TensorFlow model to detect and classify the image of the bird"""
    if image:
        return module(image)
    return None

if __name__ == "__main__":
    lock = thread.allocate_lock()
    module = hub.KerasLayer('https://tfhub.dev/google/aiy/vision/classifier/birds_V1/1')

    try:
        while True:
            bird_classified = [classify(module, image) for image in get_images()]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
