import temo
def processData(image,fetched_data,reader,jdata,uname,readeren):
    data=[]
    for predict in fetched_data["predictions"]:
       list_classes=["name","co","gender","address","dob","id_num"] 
       if predict['class'].lower() in list_classes:
            switch = {
                "name": temo.name,
                "co": temo.CO,
                "gender": temo.gender,
                "address": temo.address,
                "dob": temo.DOB,
                "id_num": temo.ID_num
            }
            result = switch.get(predict['class'].lower(), lambda image, predict, reader, readeren, uname, doc_type: "Invalid case")(image, predict, reader, readeren, uname, jdata["doc_type"])
            # result = switch.get(predict['class'], lambda: "Invalid case")(image,predict,reader,readeren,uname,jdata["doc_type"])  # Call the function corresponding to the case name
            print(result)
            if result != "Invalid case":
                data.append(result)
    return data

        
        
 
 
 
        # name,namestatus=temo.name(image,predict,reader,uname)
