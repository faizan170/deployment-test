import numpy as np
import tensorflow as tf
import cv2, os
# from src.utils import download_model
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)
# Model to Use
model_name = "ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"

# load model from path (it will download from url if not exists locally)
model= tf.saved_model.load(model_name)

def process_image(image_path):
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

                coordinates.append({
                    "box": {
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax
                    },
                    "class": int(cls),
                    "score": float(score)
                })

    # convert back to bgr and save image
    final_path = f"{STATIC_DIR}/output.jpg"
    cv2.imwrite(final_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return coordinates, final_path