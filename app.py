from flask import Flask, render_template, request, redirect
import boto3, json, uuid
import os

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = '4cl3-project-image'
JSON_FILE = 'pets.json'

def load_pets():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    return []

def save_pets(pets):
    with open(JSON_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = load_pets()
    return render_template('index.html', pets=pets)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        image = request.files['image']

        filename = str(uuid.uuid4()) + "-" + image.filename
        s3.upload_fileobj(image, BUCKET, filename, ExtraArgs={'ACL': 'public-read'})
        image_url = f'https://4cl3-project-image.s3.amazonaws.com/GR.jpg'

        pet = {"name": name, "age": age, "breed": breed, "image": image_url}
        pets = load_pets()
        pets.append(pet)
        save_pets(pets)

        return redirect('/')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

