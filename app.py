import json

from flask import Flask, request, Response, jsonify
import os
import uuid

import tasks
from Enums.TaskStatus import TaskStatus
from Task import Task
from queue_manager import QueueManager

app = Flask(__name__)
queue_manager = QueueManager()


# Endpoint 1: Accepts image_path; returns task_id
@app.route('/detect-local', methods=['GET'])
def detect_local():
    image_path = request.args.get('image_path')
    if not image_path or not os.path.exists(image_path):
        return (jsonify({"error": "Image path is required or file not found"}),
                400)

    task = Task(str(uuid.uuid4()), image_path, None, None)
    queue_manager.publish_task(task)

    return jsonify({"task_id": task.task_id}), 202


# Endpoint 2: Accepts image_url; returns task_id
@app.route('/detect-url', methods=['GET'])
def detect_url():
    image_url = request.args.get('image_url')
    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    task = Task(str(uuid.uuid4()), None, image_url, None)
    queue_manager.publish_task(task)

    return jsonify({"task_id": task.task_id}), 202


# Endpoint 3: Upload image; returns task_id
@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image file uploaded"}), 400

    print(f'Saving image..')
    saved_image = tasks.save_image(image)

    if isinstance(saved_image, str):
        return (jsonify({"error": f"Error while saving a file {saved_image}"}),
                400)
    print(f'Successfully saved image as '
          f'{saved_image.image_path.split('/')[-1]}')

    print(f'Publishing task..')
    try:
        queue_manager.publish_task(saved_image)
    except Exception as ex:
        return jsonify({"error": f"Error while publishing task {ex}"}), 400
    print(f'Task published with id: {saved_image.task_id}')

    return jsonify({"task_id": saved_image.task_id}), 202


# Endpoint 4: Check task status
@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    print(f"Checking status of task with id: {task_id}")
    task_info = tasks.check_status(task_id)

    if isinstance(task_info, str):
        return jsonify({"error": task_info}), 500

    if task_info.status == TaskStatus.NOTFOUND:
        task_info = queue_manager.get_task_status(task_id)
        if task_info is None:
            return jsonify({"error": "Task not found"}), 404

    return (Response(json.dumps(task_info.__dict__()),
                     mimetype='application/json'), 202)


if __name__ == "__main__":
    app.run(debug=True)
