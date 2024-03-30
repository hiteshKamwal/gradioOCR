import re
import GP
from PIL import Image
from dateutil.parser import parse
CPFP="temp_image/cropped_image" 
 

def name(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    name=None
    namestatus=False

    image2=Image.open(image)

                
    roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)
                    

    cropped_image = image2.crop(roi)

    # Save the cropped image
    cropped_image.save(UFname)
    dimg=GP.GP_imageConvert(UFname,uname,reader,predict['class'])
    img_text = reader.readtext(dimg)
    
    filtered_text = ""
    for result in img_text:
        text = result[1]
        text=GP.checkup(text)
        filtered_text += re.sub("[^a-zA-Z]+", " ", text)
        # print(filtered_text)
        
        name = filtered_text
        if name is not None:
            namestatus=True    
        else:
            namestatus = False
        result={"name":name,"namestatus":namestatus}
    return result

def ID_num(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    ID_num=None
    ID_numstatus=False
    image2=Image.open(image)
    roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

    cropped_image = image2.crop(roi)

    # Save the cropped image
    cropped_image.save(UFname)
    dimg=GP.GP_imageConvert(UFname,uname,reader,predict['class'])
    img_text = readeren.readtext(dimg)

    if doctype=="pan":
        print ("pan")
        ID_num = None

        for result in img_text:
            text = result[1]
            

            if re.match(r'^[A-Z]{5}\d{4}[A-Z]$', text):
                ID_num=re.match(r'^[A-Z]{5}\d{4}[A-Z]$', text).group()

                if ID_num is not None:
                    ID_numstatus = True
                else:
                    ID_numstatus = False
        result = {"ID_num":ID_num,"ID_numstatus":ID_numstatus}        
        return result
    elif doctype=="aadhar":
        print ("aadhar")
        ID_num = None

        for result in img_text:
            text = result[1]
            if re.match("^\d{4}\s\d{4}\s\d{4}$|^\d{12}$|^\d{4}$", text):
                # AadharNumber = text
                ID_num = text[-4:] if len(text) > 4 else "********" + text if len(text) == 4 else None
                if ID_num is not None:
                    ID_numstatus = True
                else:
                    ID_numstatus = False
        result = {"ID_num":ID_num,"ID_numstatus":ID_numstatus}        
        return result
def DOB(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    dob=None
    dobstatus=False
    roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)
    image2=Image.open(image)
    cropped_image = image2.crop(roi)

    # Save the cropped image
    cropped_image.save(UFname)
    dimg=GP.GP_imageConvert(UFname,uname,reader,predict['class'])

    # Read text from the image
    # reader = reader.Reader(['en'])
    # img_text = reader.readtext('cropped_image.jpg')
    img_text = readeren.readtext(dimg)
    for result in img_text:
        text = result[1]

    # img_text = ' '.join(result[1] for result in (reader.readtext(dimg)))
        try:
            parse(text)
            print(f"'{text}' is a valid date.")
            dob=text
            dobstatus=True
        except ValueError:
            text = None
            print(f"'{text}' is not a valid date.")

    if text==None:
        try:
            if any(word in img_text.lower() for word in ['dob', 'date of birth']):
                # Filter out non-digit characters
                filtered_text = ''.join(c for c in img_text if c.isdigit())

                # Check if the filtered text is a valid date of birth
                if len(filtered_text) == 8:
                    dob = filtered_text[:2] + '/' + filtered_text[2:4] + '/' + filtered_text[4:]
                    
                    
                elif 'yob' in text.lower():
                    # Extract year of birth from the text
                    year_match = re.search(r'\d{4}', text)
                    if year_match:
                        dob = year_match.group()
        except:
            if text is not None:
                dob = text
            elif img_text is not None:
                filtered_text = ''.join(c for c in img_text if c.isdigit())

                # Check if the filtered text is a valid date of birth
                if len(filtered_text) == 8:
                    dob = filtered_text[:2] + '/' + filtered_text[2:4] + '/' + filtered_text[4:]
                
                elif len(filtered_text) == 4:
                    dob = re.search(r'\d{4}', text).group
                
        if dob is not None:
            dobstatus = True
            result={"dob":dob,"dobstatus":dobstatus}
        else:
            dobstatus = False
            result={"dob":dob,"dobstatus":dobstatus}
    else:
        result={"dob":dob,"dobstatus":dobstatus}
    return result

def CO(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    co=None
    costatus=False
    image2=Image.open(image)
    roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)
    cropped_image = image2.crop(roi)
    # Save the cropped image
    cropped_image.save(UFname)
    dimg=GP.GP_imageConvert(UFname,uname,reader,predict['class'])
    img_text = reader.readtext(dimg)    
    filtered_text = ""
    for result in img_text:
        text = result[1]
        text=GP.checkup(text)
        filtered_text += re.sub("[^a-zA-Z]+", " ", text)
            
        co = filtered_text
        if co is not None:
            costatus = True
        else:
            costatus = False
    result={"co":co,"costatus":costatus}
    return result

def gender(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    gender=None
    genderstatus=False
    image2=Image.open(image)
    roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

    cropped_image = image2.crop(roi)

    # Save the cropped image
    cropped_image.save(UFname)
    dimg=GP.GP_imageConvert(UFname,uname,reader,predict['class'])


    # Read text from the image
    # reader = easyocr.Reader(['en'])
    # img_text = reader.readtext(CPFP)
    img_text = ' '.join(result[1] for result in (readeren.readtext(dimg)))
    # text = img_text[0][1]

    filtered_text = ""
    if any(word in img_text.lower() for word in ['male', 'female','m','f']):
        filtered_text = ''.join(c.lower() for c in img_text if c.isalpha())
    
    gender= filtered_text
    if gender is not None:
        genderstatus = True
    else:
        genderstatus = False
    result={"gender":gender,"genderstatus":genderstatus}

def address(image,predict,reader,readeren,uname,doctype):
    UFname=CPFP+uname+".jpg"
    address=None
    addressstatus=False
    image2=Image.open(image)
