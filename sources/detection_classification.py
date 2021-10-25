import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
from PIL import Image

ts_detection_module = hub.KerasLayer("https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1")
ts_bird_module = hub.KerasLayer("https://tfhub.dev/google/aiy/vision/classifier/birds_V1/1")
# minimum score for the model to register it as a bird
minThresh=0.33

def manipulate_image(image_converted: Image.Image, crop = (450, 200, 900, 800)):
    # Crop where the bird is detected
    image_cropped = image_converted.crop(crop)
    # Resize to Tensorflow size
    image_resized = image_cropped.resize([224, 244])
    return image_resized

def detect_bird(image: Image.Image):
    # Convert image scale
    image_converted = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    print("Run bird detection")
    result = ts_detection_module(image_converted)
    
    result_bird={"names":[],"scores":[],"boxes":[]}
    for name, score, box in zip(result['detection_class_entities'], result['detection_scores'], result['detection_boxes']):
            if name=='Bird':
                if score>=minThresh:
                    result_bird["names"].append(name)
                    result_bird["scores"].append(score)
                    result_bird["boxes"].append(box)
    print(result_bird)
    return None

def classify_bird(image: Image.Image):
    """Use the TensorFlow model to detect and classify the image of the bird"""
    if image:
        return ts_bird_module(image)
    return None