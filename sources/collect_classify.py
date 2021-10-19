import sys
import time
#import tensorflow.compat.v2 as tf
#import tensorflow_hub as hub
import base64
from apiclient import errors


def get_images():
    """
    Check whether there's an email triggered by the camera.
    Returns: a list of images, None if there is no images"""

    def GetAttachments(service, user_id, msg_id):
        """Get and store attachment from Message with given id.

        :param service: Authorized Gmail API service instance.
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :param msg_id: ID of Message containing attachment.
        """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            for part in message['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                        data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']

                    with open(path, 'w') as f:
                        f.write(file_data)

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    return [None]

def classify(module, image):
    """Use the TensorFlow model to detect and classify the image of the bird"""
    if image:
        return module(image)
    return None

if __name__ == "__main__":
    module = hub.KerasLayer('https://tfhub.dev/google/aiy/vision/classifier/birds_V1/1')

    try:
        while True:
            bird_classified = [classify(module, image) for image in get_images()]
            time.sleep(60) # Do this every minutes
    except KeyboardInterrupt:
        sys.exit(0)
