import datetime
# Get the current date and time
current_datetime = datetime.datetime.now()
# Create a unique filename with date, time, seconds, and milliseconds
unique_filename = current_datetime.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Remove last 3 digits for milliseconds

def GP_imageConvert(img,uname,reader,class_name):
    import cv2
    import matplotlib.pyplot as plt
    import PIL
    from PIL import ImageDraw
    # import easyocr
    class_name=class_name.lower()
    denoised_fname= "temp_image/denoised_image"+uname+".jpg"
    # Load the image
    image = cv2.imread(img)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Apply adaptive thresholding to enhance the visibility of English characters
    adaptive_threshold = cv2.adaptiveThreshold(denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    denoised_image = cv2.fastNlMeansDenoising(adaptive_threshold, None, h=10, templateWindowSize=7, searchWindowSize=21)

    cv2.imwrite(denoised_fname, denoised_image)
    if class_name == 'name' or class_name == 'co':
        im = PIL.Image.open(denoised_fname)
        bounds = reader.readtext(im)  # detail=0 argument will only give text in array
        draw = ImageDraw.Draw(im)
        for bound in bounds:
            #if bound is not text.isascii() then fill the box with white
            p0, p1, p2, p3 = bound[0]
            text = bound[1]
            if not text.isascii():
                draw.rectangle([*p0, *p2], fill='white')
        im.save(denoised_fname)
        return denoised_fname
    else:
        return denoised_fname

def predectImage(image, model):
        
    fetched_data=model.predict(image, confidence=50, overlap=30).json()
    return fetched_data

def base64toImg(data,uname):
    from PIL import Image
    import base64
    import imghdr

    # Get the uploaded image file
    filetype=check_file_type_from_base64(data['doc_base64'])
    if filetype == 'document':
        from pdf2image import convert_from_bytes

        
        pdf_data = base64.b64decode(data['doc_base64']) 
        
        # Convert PDF to images
        images = convert_from_bytes(pdf_data, dpi=300)
        # Concatenate all images into a single image
        combined_image = Image.new("RGB", (images[0].width, sum(image.height for image in images)))
        y_offset = 0
        for image in images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height

        # Save the combined image
        output_filename = "temp_image/output"+uname+".jpg"
        combined_image.save(output_filename)
        
        return output_filename

    else:
        # Decode the base64 data 
        doc_bytes = base64.b64decode(data['doc_base64'])
        # Get the file extension from the decoded data
        extension = imghdr.what(None, h=doc_bytes)

        output_filename = "temp_image/uplode"+uname+"."+extension
        with open(output_filename, "wb") as f:
            f.write(doc_bytes)
        return output_filename

def check_file_type_from_base64(data):
    import imghdr
    import magic
    import base64

    # Decode the base64 string
    decoded_data = base64.b64decode(data)
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'eps', 'raw', 'heic', 'tga', 'exr', 'psd', 'ai', 'ico', 'jfif', 'jif', 'jpe', 'jps', 'jpx', 'j2k', 'j2c', 'fpx', 'pbm', 'pgm', 'ppm', 'pnm', 'pam', 'pfm', 'pbm', 'pnm', 'pam', 'pfm', 'pnm', 'pcx', 'pct', 'pic', 'pict', 'xbm', 'xpm', 'xwd', 'cur', 'dds', 'dng', 'pdf', 'arw', 'cr2', 'nef', 'orf']
    document_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'txt', 'rtf', 'csv', 'xml', 'json', 'html', 'htm', 'md', 'markdown', 'log', 'msg', 'eml', 'dot', 'dotx', 'pot', 'potx', 'pps', 'ppsx', 'odg', 'otp', 'ots', 'ott', 'odm', 'oth', 'ott', 'pub', 'vsd', 'vsdx', 'indd', 'pages', 'key', 'numbers', 'csv', 'sql', 'tar', 'zip', '7z', 'rar', 'gz', 'bz2', 'tgz']
    # Check if it's an image
    image_type = imghdr.what(None, h=decoded_data)
    if image_type:
        
        if image_type.lower() in image_extensions:
            return "image"
        elif image_type.lower() in document_extensions:
            return "document"
            
            
    file_type = magic.from_buffer(decoded_data, mime=True)
    for comb in document_extensions:
        if comb in file_type:
            return "document"

def checkup(paragraph):
    import re
    black_listed_words = [
    "Name",
    "Father's Name",
    "Father s Name",
    "Fathers Name",
    "Father Name",
    "Father",
    "Date of Birth",
    "Date ",
    "Birth",
    "of",
    "Permanent",
    "Account",
    "Number",
    "PAN",
    "Signature",
    "Address",
    "Income",
    "Tax",
    "Department",
    "Government",
    "of",
    "India",
    "Taxpayer",
    "Cardholder",
    "Validity",
    "Photo"
]

    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, black_listed_words)))
    return re.sub(pattern, '', paragraph, flags=re.IGNORECASE)
