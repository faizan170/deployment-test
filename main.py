from flask import Flask, request
from infer import process_image

app = Flask(__name__)


'''
GET => 
POST => (Image)
'''


@app.route('/process', methods=['POST'])
def process():
    image = request.files['image']
    image.save("input.jpg")
    coordinates, final_path = process_image("input.jpg")
    return {
        "status": "Image processed successfully",
        "coordinates": coordinates,
        "output_image": request.host_url + final_path
    }


if __name__ == '__main__':
    app.run(debug=True)
