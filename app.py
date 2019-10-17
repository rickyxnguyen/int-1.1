from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from PIL import Image
from werkzeug.utils import secure_filename
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
import skimage
from skimage import io, filters
import numpy as np

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(APP_ROOT, 'images')
thumbnails_directory = os.path.join(APP_ROOT, 'thumbnails')

if not os.path.isdir(images_directory):
    os.mkdir(images_directory)
if not os.path.isdir(thumbnails_directory):
    os.mkdir(thumbnails_directory)


@app.route('/')
def index():
    thumbnail_names = os.listdir('./thumbnails')

    return render_template('base.html', thumbnail_names=thumbnail_names)


@app.route('/thumbnails/<filename>')
def thumbnails(filename):
    return send_from_directory('thumbnails', filename)


@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)


@app.route('/public/<path:filename>')
def static_files(filename):
    return send_from_directory('./public', filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for upload in request.files.getlist('images'):
            filename = upload.filename
            # Always a good idea to secure a filename before storing it
            filename = secure_filename(filename)
            # This is to verify files are supported
            ext = os.path.splitext(filename)[1][1:].strip().lower()
            if ext not in set(['jpg', 'jpeg', 'png']):
                return render_template('error.html', message='Uploaded files are not supported...')
            destination = '/'.join([images_directory, filename])
            # Save original image
            upload.save(destination)
            # Save a copy of the thumbnail image
            image = Image.open(destination)
            image.thumbnail((1200, 1200))
            image.save('/'.join([thumbnails_directory, filename]))
        return redirect(url_for('index'))
    return render_template('upload.html')


@app.route('/filter/sharpen')
def sharpen():
    for img in os.listdir('./thumbnails'):
        image = skimage.img_as_float(io.imread(img))
        blurred = filters.gaussian(image, sigma=10, multichannel=True)
        sharper = np.clip(image * 1.3 - blurred * 0.3, 0, 1.0)
        return sharper


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
