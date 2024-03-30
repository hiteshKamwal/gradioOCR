from flask import Flask, jsonify, request
import easyocr
from roboflow import Roboflow
import gradio as gr
import GP
import tempom

# Initialize the Roboflow API and model
rf = Roboflow(api_key="78jemcl9QfkUIKapDbT6")
project = rf.workspace().project("aadhar-brv84")
model = project.version(1).model
projectPAN=rf.workspace().project("pan-fz88k")
modelPAN=projectPAN.version(1).model
# Initialize the OCR reader
reader = easyocr.Reader(['hi','en'])
readeren = easyocr.Reader(['en'])
#     # Initialize the Roboflow API and model
# rf = Roboflow(api_key="bjF7t9SW782KAxLI2qUh")
# project = rf.workspace().project("aadhar_data_extraction")
# model = project.version(2).model
# projectPAN=rf.workspace().project("panextraction")
# modelPAN=projectPAN.version(2).model
# # Initialize the OCR reader
# reader = easyocr.Reader(['hi','en'])


# app = Flask(__name__)

# @app.route('/api/Extract_Data', methods=['POST'])
def start_service(request_datat):
    # def main_process():
    
        
    bitstreamdata = request_datat
    unique_filename = bitstreamdata['req_id']+ bitstreamdata['proposal_id']
    image_file=GP.base64toImg(bitstreamdata,unique_filename)
    if bitstreamdata['doc_type'] == 'aadhar': 
        # Perform the Aadhar data extraction
        extracted_data = process_aadhar_data(image_file, bitstreamdata,unique_filename)
    elif bitstreamdata['doc_type'].lower() == 'pan':
        extracted_data = process_pan_data(image_file, bitstreamdata,unique_filename)
    # Return the extracted data as a JSON response
    return jsonify(extracted_data)

def process_aadhar_data(image_path, jdata,uname):
    import ocrAPI_aadhar 

    # Perform OCR on the image,
    fetched_data = GP.predectImage(image_path, model)
    
    # Check if Aadhar QR code is present
    qrcheck, qrData, success = ocrAPI_aadhar.AadharQrcheck(image_path, fetched_data, jdata,uname)
    
    if qrcheck == False:
        # Extract data using OCR
        extracted_data=tempom.aadhar_P_ocr(image_path, fetched_data, reader,jdata,uname)

    else:
        extracted_data = qrData
    
    return extracted_data

def process_pan_data(image_path, jdata,uname):
    # import tempom

    fetched_data = GP.predectImage(image_path, modelPAN)
    extracted_data=tempom.Pan_P_ocr(image_path, fetched_data, reader,jdata,uname)
    return extracted_data

demo = gr.Interface(fn=start_service, inputs="json", outputs="json")
demo.launch(share=True)
# if __name__ == '__main__':
# Run the Flask app
    # app.run(host='0.0.0.0', debug=True, port=5000)
    
    # app.run(port=5000)
    # # Run the Flask app using Gunicorn for linux to start the server need to use the command "gunicorn -w 4 -b 0.0.0.0:5000 your_app_name:app"
    # # app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)