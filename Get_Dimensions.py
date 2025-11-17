# this is an app which gets the dimensions of an Image.
# the image must be in base64 format.
from flask import Flask, request, jsonify
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/image-dimensions', methods=['POST'])
def get_image_dimensions():
    try:
        data = request.get_json()

        # Expecting { "image_base64": "..." }
        if "image_base64" not in data:
            return jsonify({"error": "image_base64 field missing"}), 400

        image_b64 = data["image_base64"]

        # Decode base64 string
        try:
            image_bytes = base64.b64decode(image_b64)
        except Exception:
            return jsonify({"error": "Invalid base64 string"}), 400

        # Read the image using Pillow
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size

        return jsonify({
            "width": str(width),
            "height": str(height)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
