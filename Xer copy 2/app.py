# from flask import Flask, request, render_template, jsonify
# import os
# from werkzeug.utils import secure_filename
# import win32print
# import win32api

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'

# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# @app.route('/')
# def index():
#     printers = [printer[2] for printer in win32print.EnumPrinters(2)]
#     return render_template('index.html', printers=printers)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'status': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'status': 'No selected file'})
#     if file:
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return jsonify({'status': 'File uploaded successfully', 'filename': filename})

# @app.route('/print', methods=['POST'])
# def print_file():
#     data = request.get_json()
#     filename = data.get('filename')
#     printer = data.get('printer')
#     copies = int(data.get('copies', 1))
#     page_size = data.get('page_size', 'A4')
#     pages_per_sheet = int(data.get('pages_per_sheet', 1))
#     scale = data.get('scale', 'Default')
#     two_sided = data.get('two_sided', False)

#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
#     try:
#         # Check if the file exists
#         if not os.path.exists(file_path):
#             return jsonify({'status': 'Failed to print', 'error': 'File not found'}), 404

#         # Open the printer
#         printer_handle = win32print.OpenPrinter(printer)
#         # Define the document info
#         doc_info = {
#             "pDocName": filename,
#             "pOutputFile": None,
#             "pDatatype": None
#         }
#         # Start a print job
#         job_id = win32print.StartDocPrinter(printer_handle, 1, doc_info)
#         # Start a page
#         win32print.StartPagePrinter(printer_handle)

#         # Read the file and send to printer
#         with open(file_path, 'rb') as file:
#             raw_data = file.read()
#             win32print.WritePrinter(printer_handle, raw_data)

#         # End the page
#         win32print.EndPagePrinter(printer_handle)
#         # End the print job
#         win32print.EndDocPrinter(printer_handle)
#         # Close the printer
#         win32print.ClosePrinter(printer_handle)
        
#         return jsonify({'status': 'Print command sent successfully'})
#     except Exception as e:
#         error_message = f"Error: {e}"
#         print(error_message)
#         return jsonify({'status': 'Failed to print', 'error': error_message}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import win32print
import win32api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    return render_template('index.html', printers=printers)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'status': 'File uploaded successfully', 'filename': filename})

@app.route('/print', methods=['POST'])
def print_file():
    data = request.get_json()
    filename = data.get('filename')
    printer = data.get('printer')
    copies = int(data.get('copies', 1))
    page_size = data.get('page_size', 'A4')
    pages_per_sheet = int(data.get('pages_per_sheet', 1))
    scale = data.get('scale', 'Default')
    two_sided = data.get('two_sided', False)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            return jsonify({'status': 'Failed to print', 'error': 'File not found'}), 404

        # Open the printer
        printer_handle = win32print.OpenPrinter(printer)
        # Define the document info
        doc_info = {
            "pDocName": filename,
            "pOutputFile": None,
            "pDatatype": None
        }
        # Start a print job
        job_id = win32print.StartDocPrinter(printer_handle, 1, doc_info)
        try:
            # Start a page
            win32print.StartPagePrinter(printer_handle)

            # Read the file and send to printer
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                win32print.WritePrinter(printer_handle, raw_data)

            # End the page
            win32print.EndPagePrinter(printer_handle)
            # End the print job
            win32print.EndDocPrinter(printer_handle)
        except Exception as e:
            # Abort the print job in case of an error
            win32print.AbortPrinter(printer_handle)
            raise e
        finally:
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
        
        return jsonify({'status': 'Print command sent successfully'})
    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        return jsonify({'status': 'Failed to print', 'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
