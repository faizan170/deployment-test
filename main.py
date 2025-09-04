from flask import Flask, request, render_template
from infer import process_image

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
        image.save("input.jpg")
        coordinates, final_path = process_image("input.jpg")
        return {
            "status": "Image processed successfully",
            "coordinates": coordinates,
            "output_image": request.host_url.replace("http", "https") + final_path
        }
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
