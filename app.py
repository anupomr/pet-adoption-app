from flask import Flask, render_template, request, redirect, url_for
import boto3, json, os
from uuid import uuid4

app = Flask(__name__)
S3_BUCKET = '4cl3-project-image'
s3 = boto3.client('s3')
DATA_FILE = 'pets.json'

def load_pets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_pets(pets):
    with open(DATA_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = load_pets()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        file = request.files['image']

        if file:
            image_name = f"{uuid4().hex}_{file.filename}"
            s3.upload_fileobj(file, S3_BUCKET, image_name)
            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{image_name}"

            pets = load_pets()
            pets.append({
                'name': name,
                'age': age,
                'breed': breed,
                'image': image_url
            })
            save_pets(pets)

        return redirect(url_for('index'))
    return render_template('add_pet.html')

@app.route('/pet/<name>')
def pet(name):
    pets = load_pets()
    for pet in pets:
        if pet['name'].lower() == name.lower():
            return render_template('pet.html', pet=pet)
    return "Pet not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

