import numpy as np
import tensorflow as tf
import cv2, os
from google.cloud import storage    


# COCO 2017 Label Dictionary
# Model: ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu

category_index = {
    1: 'person',
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    13: 'stop sign',
    14: 'parking meter',
    15: 'bench',
    16: 'bird',
    17: 'cat',
    18: 'dog',
    19: 'horse',
    20: 'sheep',
    21: 'cow',
    22: 'elephant',
    23: 'bear',
    24: 'zebra',
    25: 'giraffe',
    27: 'backpack',
    28: 'umbrella',
    31: 'handbag',
    32: 'tie',
    33: 'suitcase',
    34: 'frisbee',
    35: 'skis',
    36: 'snowboard',
    37: 'sports ball',
    38: 'kite',
    39: 'baseball bat',
    40: 'baseball glove',
    41: 'skateboard',
    42: 'surfboard',
    43: 'tennis racket',
    44: 'bottle',
    46: 'wine glass',
    47: 'cup',
    48: 'fork',
    49: 'knife',
    50: 'spoon',
    51: 'bowl',
    52: 'banana',
    53: 'apple',
    54: 'sandwich',
    55: 'orange',
    56: 'broccoli',
    57: 'carrot',
    58: 'hot dog',
    59: 'pizza',
    60: 'donut',
    61: 'cake',
    62: 'chair',
    63: 'couch',
    64: 'potted plant',
    65: 'bed',
    67: 'dining table',
    70: 'toilet',
    72: 'tv',
    73: 'laptop',
    74: 'mouse',
    75: 'remote',
    76: 'keyboard',
    77: 'cell phone',
    78: 'microwave',
    79: 'oven',
    80: 'toaster',
    81: 'sink',
    82: 'refrigerator',
    84: 'book',
    85: 'clock',
    86: 'vase',
    87: 'scissors',
    88: 'teddy bear',
    89: 'hair drier',
    90: 'toothbrush'
}

# Helper function to get class name safely
def get_class_name(class_id):
    return category_index.get(class_id, "Unknown")

bucket_name = 'deployment-test-bucket-1234'
cloud_model_path = "ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz"
local_path = "ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8"
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

# download this model locally
if not os.path.exists(local_path):
    blob = bucket.blob(cloud_model_path)
    blob.download_to_filename(cloud_model_path)

    # extract model
    import tarfile

    with tarfile.open(cloud_model_path, "r:gz") as tar:
        tar.extractall(path=".")

# from src.utils import download_model
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)
# Model to Use
model_name = "ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"

# load model from path (it will download from url if not exists locally)
model= tf.saved_model.load(model_name)

def process_image(image_path):
    print("Processing Image:", image_path)
    # read image and preprocess
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_tensor = np.expand_dims(img, 0)

    # predict from model
    resp = model(input_tensor)
    coordinates = []
    # get the output of the prediction
    # iterate over boxes, class_index and score list
    for boxes, classes, scores in zip(resp['detection_boxes'].numpy(), resp['detection_classes'], resp['detection_scores'].numpy()):
        for box, cls, score in zip(boxes, classes, scores): # iterate over sub values in list
            if score > 0.6: # we are using only detection with confidence of over 0.8
                ymin = int(box[0] * h)
                xmin = int(box[1] * w)
                ymax = int(box[2] * h)
                xmax = int(box[3] * w)
                
                # draw on image
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (128, 0, 128), 4)
                cv2.putText(img, f"{get_class_name(int(cls))}: {int(score*100)}%", (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                coordinates.append({
                    "box": {
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax
                    },
                    "class": int(cls),
                    "class_name": get_class_name(int(cls)),
                    "score": float(score)
                })

    # convert back to bgr and save image
    final_path = f"{STATIC_DIR}/output.jpg"
    cv2.imwrite(final_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return coordinates, final_path