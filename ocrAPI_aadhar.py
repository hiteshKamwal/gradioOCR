from PIL import Image
def xml_to_jsonunsecured(root,jdata,success):
    name, gender, address, VTC, state, PC, DoB, uid, masked_uid, co = (root.attrib['name'],root.attrib['gender'],root.attrib['house'] + " " + root.attrib['street'] + " " + root.attrib['loc'] + " " + root.attrib['vtc'] + " " + root.attrib['po'] + " " + root.attrib['dist'] + " " + root.attrib['subdist'] + " ",root.attrib['vtc'],root.attrib['state'],root.attrib['pc'],root.attrib['dob'],"" * (len(root.attrib['uid']) - 4) + root.attrib['uid'][-4:],"************" + ("" * (len(root.attrib['uid']) - 4) + root.attrib['uid'][-4:]),root.attrib['co'])

# single line json same structure
    # data = {"req_id": jdata["req_id"], "proposal_id": jdata["proposal_id"], "success": success, "message": "", "result": {"name": name, "dob": DoB, "gender": gender, "address": address, "address_details": {"State": state, "City": VTC, "PIN": PC}, "aadhar_id": uid, "aadhar_masked_no": masked_uid, "father_spouse_name": co}}
    data = {
            "req_id": jdata["req_id"],
            "proposal_id" : jdata["proposal_id"],
            "success": success,
            "message" : "",
            "result":
           {
            "name": name,
            "dob": DoB,
            "gender": gender,
            "address": address,
            "address_details": {
                "State": state,
                "City": VTC,
                "PIN": PC
            },
            "aadhar_id": uid,
            "aadhar_masked_no": masked_uid,
            "father_spouse_name": co
        }
    }
    return data
def xml_to_jsonsecured(root, jdata,success):
    import json
    data = json.loads(json.dumps(root))
    name, gender, address, VTC, state, PC, DoB, uid, masked_uid, co = data['name'], data['gender'], f"{data['house']} {data['street']} {data['location']} {data['vtc']} {data['postoffice']} {data['district']} {data['subdistrict']}", data['vtc'], data['state'], data['pincode'], data['dob'], data['aadhaar_last_4_digit'], "************" + data['aadhaar_last_4_digit'], data['careof']
    

# single line json same structure
    # data = {"req_id": jdata["req_id"], "proposal_id": jdata["proposal_id"], "success": success, "message": "", "result": {"name": name, "dob": DoB, "gender": gender, "address": address, "address_details": {"State": state, "City": VTC, "PIN": PC}, "aadhar_id": uid, "aadhar_masked_no": masked_uid, "father_spouse_name": co}}
    data = {
            "req_id": jdata["req_id"],
            "proposal_id" : jdata["proposal_id"],
            "success": success,
            "message" : "",
            "result":
                    {
                            "name": name,
                            "dob": DoB,
                            "gender": gender,
                            "address": address,
                            "address_details": {
                                "State": state,
                                "City": VTC,
                                "PIN": PC
                            },
                            "aadhar_id": uid,
                            "aadhar_masked_no": masked_uid,
                            "father_spouse_name": co
                        }
            }
    return data


def AadharQrcheck(image, fetched_data, jdata,uname):
    iname="temp_image\cropped_image"+uname+".jpg"
    from pyaadhaar.decode import AadhaarSecureQr
    from pyaadhaar.utils import Qr_img_to_text, isSecureQr
    import cv2            

    is_aadhar_QR_present = False        
    for predict in fetched_data["predictions"]:
        if predict["class"] != "aadhar_QR":
            continue

        if predict["class"] == "aadhar_QR":
            is_aadhar_QR_present = True

            roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

            # x0 = predict['x'] - predict['width'] / 2
            # x1 = predict['x'] + predict['width'] / 2
            # y0 = predict['y'] - predict['height'] / 2
            # y1 = predict['y'] + predict['height'] / 2
            # roi=(x0, y0, x1, y1)
            image2=Image.open(image)

            cropped_image = image2.crop(roi)

            # Save the cropped image
            # image_file_name = cropped_image.convert("RGB")
            cropped_image.save(iname)
            

            # image_file_name = 'sQR.jpg';

            image_file_name = iname;
            # image_file_name = image_file_name.convert("RGB")



            img = cv2.imread(image_file_name, cv2.IMREAD_GRAYSCALE)  # Read image as grayscale.
            img2 = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2), interpolation=cv2.INTER_LANCZOS4)  # Resize by x2 using LANCZOS4 interpolation method.

            cv2.imwrite('temp_image\qr{uname}.png', img)

            img3 = cv2.imread('temp_image\qr{uname}.png')

            import xml.etree.ElementTree as ET
            qrData = Qr_img_to_text('temp_image\qr{uname}.png')
            
            if len(qrData) == 0:
                print("QR found but Unextracted !!")
                success=False
                return False, "QR found but Unextracted !!",success
            elif int(len(qrData[0]))>13:
                try:
                    strings=ET.fromstring(qrData[0])
                    success=True
                    data = xml_to_jsonunsecured(strings,jdata,success)
                    


                    print("QR data is in XML format","\n",data)
                    return True, data, success
                except ET.ParseError:
                    isSecureQR = (isSecureQr(qrData[0]))
                    if isSecureQR:
                        qrData_tobyte = int(qrData[0], 10)
                        # print(type(qrData_tobyte))
                        
                        obj  = AadhaarSecureQr(qrData_tobyte)
                        qrDecoy= obj.decodeddata()
                        data=xml_to_jsonsecured(qrDecoy,jdata,True) 
                        success=True
                        return True, data, success
                    print("QR data is not in XML format")
                # print (qrData)
                ############### Need to Convert xml data to Json formate before returning##########
                return True, qrData, success
            

            if qrData is None:
                data=int(len(qrData[0]))
                # print (data)
                if data>13:
                    if len(qrData) == 0:
                        print(" No QR Code Detected !!")
                    else:
                        isSecureQR = (isSecureQr(qrData[0]))
                        if isSecureQR:
                            qrData_tobyte = int(qrData[0], 10)
                            # print(type(qrData_tobyte))
                            
                            obj  = AadhaarSecureQr(qrData_tobyte)
                            qrDecoy= obj.decodeddata() 
                            # print(obj.decodeddata())
                            success=True

                            return True, qrDecoy , success
                

        print('in AadharQrcheck')
    else:
        success=False
        return False, "QR not found", success



def aadhar_P_ocr(image,fetched_data,reader,jdata,uname,readeren):
    import re
    import GP

    AadharHolderName, AadharNumber, AadharHolderDOB, AadharHolderGender, address_details, AadharHolderCO = None, None, None, None, None, None
   
    AadharHolderNamestatus , AadharHolderDOBstatus , aadhar_numberstatus , AadharHolderGenderstatus , AadharHolderCOstatus, address_detailsstatus=False,False,False,False,False,False
    CPFP="temp_image/cropped_image"+uname+".jpg"

    image2=Image.open(image)
    for predict in fetched_data["predictions"]:
            if predict['class'] == 'aadhar_holder_name':
                
                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])



                # Read text from the image
                # reader = easyocr.Reader(['en'])
                img_text = reader.readtext(dimg)

                filtered_text = ""
                for result in img_text:
                    text = result[1]
                    filtered_text += re.sub("[^a-zA-Z]+", " ", text)
                    # print(filtered_text)
                    
                    AadharHolderName = filtered_text
                    if AadharHolderName is not None:
                        AadharHolderNamestatus=True    
                    else:
                        AadharHolderNamestatus = False
                    
                    
        #FOR EXTRACTING NAME FROM THE IMAGE########## END ###################################################################################################        

        #FOR EXTRACTING AADHAR NUMBER FROM THE IMAGE########## START ###################################################################################################

            elif predict['class'] == 'aadhar_number':
                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                


                # Read text from the image
                # reader = easyocr.Reader(['en'])
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])
                img_text = reader.readtext(dimg)

                aadhar_number = None

                for result in img_text:
                    text = result[1]
                    if re.match("^\d{4}\s\d{4}\s\d{4}$|^\d{12}$|^\d{4}$", text):
                        # AadharNumber = text
                        AadharNumber = text[-4:] if len(text) > 4 else "********" + text if len(text) == 4 else None
                        if AadharNumber is not None:
                            aadhar_numberstatus = True
                        else:
                            aadhar_numberstatus = False
                        

                # text = img_text[0][1]
                # AadharNumber= text

                filtered_text = ""
#FOR EXTRACTING AADHAR NUMBER FROM THE IMAGE########## END ###################################################################################################        


#FOR EXTRACTING DOB FROM THE IMAGE########## START ###################################################################################################


            elif predict['class'] == 'aadhar_holder_DOB':

                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])

                # Read text from the image
                # reader = easyocr.Reader(['en'])
                # img_text = reader.readtext(CPFP)

                img_text = ' '.join(result[1] for result in (reader.readtext(dimg)))

                  
                if any(word in img_text.lower() for word in ['dob', 'date of birth']):
                    # Filter out non-digit characters
                    filtered_text = ''.join(c for c in img_text if c.isdigit())

                    # Check if the filtered text is a valid date of birth
                    if len(filtered_text) == 8:
                        AadharHolderDOB = filtered_text[:2] + '/' + filtered_text[2:4] + '/' + filtered_text[4:]
                         
                        
                    elif 'yob' in text.lower():
                        # Extract year of birth from the text
                        year_match = re.search(r'\d{4}', text)
                        if year_match:
                            AadharHolderDOB = year_match.group()
                    
                    if AadharHolderDOB is not None:
                        AadharHolderDOBstatus = True
                    else:
                        AadharHolderDOBstatus = False
        

                # if re.match("^\d{4}\s\d{4}\s\d{4}$", text):
                #     # Mask all digits except the last 4
                #     masked_text = re.sub("\d(?=\d{4})", "*", text)
                #     filtered_text += masked_text + " "
                # else:
                #     filtered_text += text + " "

                # print(filtered_text)
        


        #FOR EXTRACTING DOB FROM THE IMAGE########## END ###################################################################################################        

        #FOR EXTRACTING GENDER FROM THE IMAGE########## END ###################################################################################################        

            elif predict['class'] == 'aadhar_holder_gender':

                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])


                # Read text from the image
                # reader = easyocr.Reader(['en'])
                # img_text = reader.readtext(CPFP)
                img_text = ' '.join(result[1] for result in (readeren.readtext(dimg)))
                # text = img_text[0][1]

                filtered_text = ""
                if any(word in img_text.lower() for word in ['male', 'female','m','f']):
                    filtered_text = ''.join(c.lower() for c in img_text if c.isalpha())
                
                AadharHolderGender= filtered_text
                if AadharHolderGender is not None:
                    AadharHolderGenderstatus = True
                else:
                    AadharHolderGenderstatus = False
                

                # print(filtered_text)
                  
        #FOR EXTRACTING GENDER FROM THE IMAGE########## END ###################################################################################################

        #FOR EXTRACTING FATHER NAME FROM THE IMAGE########## START ###################################################################################################
            elif predict['class'] == 'father_name':

                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])


                # Read text from the image
                # reader = easyocr.Reader(['en'])
                # img_text = reader.readtext(CPFP)
                img_text = ' '.join(result[1] for result in (reader.readtext(dimg)))
                # text = img_text[0][1]
                filtered_text = ""
                for result in img_text:
                    text = result[1]
                    filtered_text += re.sub("[^a-zA-Z]+", " ", text)
                    # print(filtered_text)
                    
                    AadharHolderCO = filtered_text
                    if AadharHolderCO is not None:
                        AadharHolderCOstatus = True
                    else:
                        AadharHolderCOstatus = False
                    



        #FOR EXTRACTING FATHER NAME FROM THE IMAGE########## END ###################################################################################################        

 #FOR EXTRACTING ADDRESS FROM THE IMAGE########## START ###################################################################################################
                
            elif predict['class'] == 'address':
                roi=(predict['x'] - predict['width'] / 2,  predict['y'] - predict['height'] / 2,predict['x'] + predict['width'] / 2, predict['y'] + predict['height'] / 2)

                cropped_image = image2.crop(roi)

                # Save the cropped image
                cropped_image.save(CPFP)
                dimg=GP.GP_imageConvert(CPFP,uname,reader,predict['class'])


                # Read text from the image
                # reader = easyocr.Reader(['en'])
                # img_text = reader.readtext(CPFP)
                img_text = ' '.join(result[1] for result in (reader.readtext(dimg)))
                # text = img_text[0][1]
                filtered_text = ""
                for result in img_text:
                    text = result[1]
                    pin_code = re.search(r'\b\d{6}\b', text)
                    if pin_code:
                        pincode= pin_code.group()
                        import requests
                        #https://motionless-moth-overcoat.cyclic.app/pincode?Pincode=400051
                        api_url = 'https://motionless-moth-overcoat.cyclic.app/pincode'
                        response = requests.get(f'{api_url}?Pincode={pincode}',verify=False)
                        data = response.json()
                        # state=data[0]['StateName']
                        # city=""
                        address_details={
                            "State": data[0]['StateName'],
                            "City": "",
                            "PIN": pincode
                        }



                        # print("Pin code found:", pin_code.group())
                    else:
                        print("Pin code not found")

                    if address_details is not None:
                        address_detailsstatus = True
                    else:
                        address_detailsstatus = False
                    # print(filtered_text)

    success = AadharHolderNamestatus and AadharHolderDOBstatus and aadhar_numberstatus and AadharHolderGenderstatus and AadharHolderCOstatus and address_detailsstatus

 #FOR EXTRACTING ADDRESS FROM THE IMAGE########## START ###################################################################################################
    data = {
    "req_id": jdata["req_id"],
    "proposal_id" : jdata["proposal_id"],
    "success": success,
    "message" : "",
    "result":
            {
                    "name": AadharHolderName,
                    "dob": AadharHolderDOB,
                    "gender": AadharHolderGender,
                    "address": AadharNumber,
                    "address_details": address_details,
                    "aadhar_id": AadharNumber,
                    "aadhar_masked_no": AadharNumber,
                    "father_spouse_name": AadharHolderCO
                }
    }

# AadharHolderNamestatus
#AadharHolderName, AadharHolderDOB, AadharNumber,AadharHolderGender, AadharHolderCO
# AadharHolderNamestatus, AadharHolderDOBstatus, AadharNumberstatus,AadharHolderGenderstatus, AadharHolderCOststus,address_detailsstatus
    return data
            # break




