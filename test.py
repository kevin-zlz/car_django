import json

with open('carsdetail.json','r',encoding='utf-8') as f:
    d=json.load(f)
    link=[]

    for car in d:
        link.append(
            {
                "carname":car['fullname'].split('/')[0],
                "carurl":car['little_picture'][1]
            }
        )
    print(link)