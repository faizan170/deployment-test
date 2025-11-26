from flask import Flask, request, render_template
from infer import process_image
import os

app = Flask(__name__)


'''
GET => 
POST => (Image)
'''

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    try:
        image = request.files['image']
        filename = "temp/" + image.filename
        image.save(filename)
        coordinates, final_path = process_image(filename)
        
        url = request.host_url
        if os.environ.get("FLASK_ENV") == "production":
            url = url.replace("http", "https")
        return {
            "status": "Image processed successfully",
            "coordinates": coordinates,
            "output_image": url + final_path
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
