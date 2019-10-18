from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from PIL import Image
from werkzeug.utils import secure_filename
import os
import glob
import shutil

app = Flask(__name__)
# This will create directories for images and will add them into them
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(APP_ROOT, 'images')
thumbnails_directory = os.path.join(APP_ROOT, 'thumbnails')
# If they don't exist the app will make it automatically
if not os.path.isdir(images_directory):
    os.mkdir(images_directory)
if not os.path.isdir(thumbnails_directory):
    os.mkdir(thumbnails_directory)

# This will display all of the thumbnails added from the upload
@app.route('/')
def index():
    thumbnail_names = os.listdir('./thumbnails')

    return render_template('base.html', thumbnail_names=thumbnail_names)

# This should allow for users to open each image individually
@app.route('/thumbnails/<filename>')
def thumbnails(filename):
    return send_from_directory('thumbnails', filename)

# This will send the uploaded image directly into images folder
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)

# This will make the path to each image public to the app
@app.route('/public/<path:filename>')
def static_files(filename):
    return send_from_directory('./public', filename)


"""
This will allow the user to upload an image and will automatically create a thumbnail for each of them
and create a copy of the filename
"""
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
            image.thumbnail((300, 200))
            image.save('/'.join([thumbnails_directory, filename]))
        return redirect(url_for('index'))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    shutil.rmtree(thumbnails_directory)
    shutil.rmtree(images_directory)
    os.mkdir(images_directory)
    os.mkdir(thumbnails_directory)

    return redirect(url_for('index'))


files = glob.glob('/YOUR/PATH/*')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
