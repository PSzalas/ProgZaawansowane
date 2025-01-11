import uuid
from collections import namedtuple
from typing import Union

import cv2
import numpy as np
import requests
import os

from werkzeug.datastructures import FileStorage

from Enums.TaskStatus import TaskStatus
from Task import Task

RESULTS_DIR = "../ProgramowanieZaawansowaneProjectFiles/Results"
TEMP_DIR = "../ProgramowanieZaawansowaneProjectFiles/Temp"
MODELS_DIR = "../ProgramowanieZaawansowaneProjectFiles/Models"
LOCALIMAGES_DIR = "../ProgramowanieZaawansowaneProjectFiles/LocalImages"
UPLOADES_DIR = "../ProgramowanieZaawansowaneProjectFiles/Uploads"

PROCESSEDIMAGE = namedtuple('ProcecssedImage', ['result_path', 'person_count'])


def download_image(url: str, save_path: str) -> str:
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    return save_path


def save_image(image: FileStorage) -> Union[Task, str]:
    try:
        task_id = str(uuid.uuid4())

        if not os.path.exists(UPLOADES_DIR):
            os.makedirs(UPLOADES_DIR)

        file_path = f'{UPLOADES_DIR}/{task_id}-{image.filename}'
        image.save(file_path)
    except Exception as ex:
        return f'{ex}'

    task = Task(task_id, file_path)
    return task


def check_status(task_id: str) -> Union[Task, str]:
    task_info = Task()
    task_info.task_id = task_id

    # Search for the file in the results directory
    # that matches task_id in its name
    for filename in os.listdir(RESULTS_DIR):
        # Check if the filename matches the pattern
        # "[task_id]-[number_of_people].jpg"
        if filename.startswith(f"[{task_id}]-"):
            try:
                # Example filename:
                # "bb12ce21-bb0b-4a90-a7aa-b9340717e6a8-5.jpg"
                base_name, ext = os.path.splitext(filename)
                task_info.image_path = os.path.join(RESULTS_DIR, filename)
                task_info.number_of_people = (
                    int(base_name.split('-')[-1].strip("[]")))
                task_info.status = TaskStatus.COMPLETED
                break
            except Exception as ex:
                return f"Error parsing file: {ex}"

    return task_info


def detect_people(image_path: str) -> PROCESSEDIMAGE:
    try:
        # Load YOLO
        net = cv2.dnn.readNet(f'{MODELS_DIR}/yolov4/yolov4.weights',
                              f'{MODELS_DIR}/yolov4/yolov4.cfg')
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in
                         net.getUnconnectedOutLayers()]

        # Load COCO class labels (person is class ID 0 in COCO)
        with open(f'{MODELS_DIR}/yolov4/coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or cannot be read.")

        height, width, _ = image.shape

        # Prepare the image for YOLO
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0),
                                     True, crop=False)
        net.setInput(blob)

        # Run YOLO detection
        detections = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        person_count = 0

        for out in detections:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Only consider person confidence > 0.5
                    # COCO class for 'person'
                    if classes[class_id] == 'person':
                        person_count += 1
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

        # Apply Non-Maximum Suppression to remove redundant overlapping boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences,
                                   score_threshold=0.5, nms_threshold=0.4)

        person_count = len(indices)
        # Draw bounding boxes around people
        if len(indices) > 0:
            for i in indices:
                x, y, w, h = boxes[i]  # Use the index to get the bounding box
                # Draw the bounding box
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the result image
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)

        result_path = f"{RESULTS_DIR}/temp-{os.path.basename(image_path)}"
        cv2.imwrite(result_path, image)

        processed_image = (
            PROCESSEDIMAGE(result_path=result_path, person_count=person_count))

        return processed_image

    except Exception as e:
        print(f"Error in detect_people: {e}")
        raise


def process_image_task(task: Task) -> PROCESSEDIMAGE:
    if task.image_url is not None:
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        image_path = download_image(task.image_url,
                                    f"{TEMP_DIR}/{task.task_id}.jpg")
    else:
        image_path = task.image_path

    processed_image = detect_people(image_path)

    if task.image_url is not None:
        os.remove(image_path)

    return processed_image
