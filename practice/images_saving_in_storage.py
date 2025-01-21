import os
from flask import Flask, request, jsonify
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.abspath('./uploads')  # creating folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ensures if the folder exists, if not it will create it if necessary
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class ImageHandler:

    def upload_image(self, request):
        try:
            # Check if the input field exists
            if 'image' not in request.files:
                return jsonify({"status": "No file part"}), 400

            file = request.files['image']
            if file.filename == '':
                return jsonify({"status": "No selected file"}), 400

            # Save the file to the uploads directory
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            return {"status": "Image uploaded successfully!", "file_path": file_path}, 201
        except Error as e:
            return jsonify({"Error": str(e)}), 400

    def view_image(self, data):
        try:
            image_name = data['image_name']
            if not image_name:
                return jsonify({"status": "Image name is required"}), 400
            # Construct the file path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

            # Check if the file exists
            if not os.path.exists(file_path):
                return jsonify({"status": "Image not found"}), 404

            return jsonify({"image_name": image_name, "file_path": file_path}), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 400


image_handler = ImageHandler()


@app.route('/upload', methods=['POST'])
def upload():
    response, status_code = image_handler.upload_image(request)
    return jsonify(response), status_code


@app.route('/view_image', methods=['POST'])
def view_image():
    data = request.get_json()
    response = image_handler.view_image(data)
    return response


if __name__ == "__main__":
    app.run(debug=True)
