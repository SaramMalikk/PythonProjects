import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class Imagines:
    def __init__(self):
        """Initialize the database connection and cursor with hard-coded values"""
        self.host = 'localhost'
        self.user = 'root'  # Replace with your MySQL username
        self.password = 'saramali9'  # Replace with your MySQL password
        self.database = 'restaurant'  # Replace with your MySQL database name
        self.conn = None
        self.cursor = None

        # Create the database connection and cursor directly in the constructor
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                print("Successfully connected to the database.")
                self.cursor = self.conn.cursor(buffered=True)
                print("Cursor created successfully.")
        except Exception as e:
            print(f"Error: {e}")
            self.conn = None
            self.cursor = None

    def upload_image(self, request):
        try:
            # This is HTML part to check if input field exists or not
            if 'image' not in request.files:
                return jsonify({"status": "No file part"}), 400

            # In Flask (or similar web frameworks), the file uploads are accessed through the request.files object.
            file = request.files['image']
            # The uploaded file will be accessible in the server-side code via request.files['image']
            if file.filename == '':
                return jsonify({"status": "No selected file"}), 400
            # binary data is which machine understand
            # Read the file data as binary and extract the name from it
            image_data = file.read()

            image_name = file.filename  # file name
            self.cursor.execute("INSERT INTO images (image_name, image_data) VALUES (%s, %s)",
                                (image_name, image_data))
            self.conn.commit()

            return jsonify({"status": "Image uploaded successfully!"}), 201
        except Error as e:
            return {"Error": str(e)}, 400

    def view_image(self, data):
        try:
            self.cursor.execute("SELECT image_name, image_data FROM images WHERE image_name = %s",
                                (data['image_name'],))
            image = self.cursor.fetchone()

            if not image:
                return jsonify({"status": "Image not found"}), 404

            image_name = image[0]
            image_data = image[1]

            # Convert image data to base64 encoding
            encoded_image_data = base64.b64encode(image_data).decode('utf-8')

            return jsonify({
                "image_name": image_name,
                "image_data": encoded_image_data
            }), 200

        except Error as e:
            return {"Error":  str(e)}, 400


db = Imagines()


@app.route('/upload', methods=['POST'])
def upload():
    response, status_code = db.upload_image(request)  # Pass the 'request' object to the upload_image method
    return response, status_code


@app.route('/view_image', methods=['GET', 'POST'])
def view_image():
    data = request.get_json()
    response, status_code = db.view_image(data)
    return response, status_code


if __name__ == "__main__":
    app.run(debug=True)
