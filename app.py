from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pdf2image import convert_from_path, exceptions

# Specify Poppler's path for Windows
poppler_path = r"C:\poppler-24.08.0\Library\bin"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
app.secret_key = 'your_secret_key'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('home.html')

# Resize Image
@app.route('/resize', methods=['GET', 'POST'])
def resize_image():
    if request.method == 'POST':
        width = request.form['width']
        height = request.form['height']
        image_file = request.files['file']

        if not allowed_file(image_file.filename):
            flash('Invalid file type')
            return redirect(request.url)

        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)

        try:
            with Image.open(filepath) as img:
                img_resized = img.resize((int(width), int(height)))
                resized_filename = 'resized_' + filename
                resized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], resized_filename)
                img_resized.save(resized_filepath)

                flash(f'Image has been resized to {width}x{height} and saved successfully!')
                return redirect(url_for('download_file', filename=resized_filename))
        except Exception as e:
            flash(f'Error resizing image: {str(e)}')
            return redirect(request.url)

    return render_template('resize.html')

# Convert Images to PDF
@app.route('/convert-to-pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('images')
        images = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                images.append(filepath)

        # Convert images to PDF using PIL
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
        images_for_pdf = [Image.open(image).convert('RGB') for image in images]
        images_for_pdf[0].save(pdf_path, save_all=True, append_images=images_for_pdf[1:])

        flash('Images have been successfully converted to PDF!')
        return redirect(url_for('download_file', filename='output.pdf'))

    return render_template('convert_pdf.html')

# Convert PDF to Images
@app.route('/convert-pdf-to-images', methods=['GET', 'POST'])
def convert_pdf_to_image():
    if request.method == 'POST':
        file = request.files['file']

        if not allowed_file(file.filename):
            flash('Invalid file type')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Convert PDF to images
            images = convert_from_path(filepath, poppler_path=poppler_path)
            pdf_images = []
            for i, image in enumerate(images):
                image_filename = f"output_page_{i+1}.png"
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(image_path)
                pdf_images.append(image_path)

            flash(f'PDF has been converted to {len(pdf_images)} images successfully!')
            return redirect(url_for('download_file', filename=os.path.basename(pdf_images[0])))  # Download the first image

        except exceptions.PDFPageCountError:
            flash('Error: The PDF file could not be processed. Ensure it is a valid PDF.')
            return redirect(request.url)
        except Exception as e:
            flash(f'Error converting PDF to images: {str(e)}')
            return redirect(request.url)

    return render_template('convert_pdf_to_image.html')

# Convert Image Format
@app.route('/convert-format', methods=['GET', 'POST'])
def convert_format():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_format = request.form['format']
            if new_format.upper() == 'JPG':
                new_format = 'JPEG'
            new_filename = os.path.splitext(filename)[0] + '.' + new_format
            new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            try:
                with Image.open(filepath) as img:
                    img.convert('RGB').save(new_filepath, new_format.upper())

                flash(f'File format has been converted and saved as {new_format.upper()}!')
                return redirect(url_for('download_file', filename=new_filename))
            except Exception as e:
                flash(f'Error converting image format: {str(e)}')
                return redirect(request.url)

        flash('Invalid file type or no file selected.')
        return redirect(url_for('home'))

    return render_template('convert_format.html')

# Download the processed file
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
