import requests
import datetime
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tables.html')

@app.route('/api/get_slots')
def hello_world():
    # 141 	 Central Delhi
    # 145 	 East Delhi
    # 140 	 New Delhi
    # 146 	 North Delhi
    # 147 	 North East Delhi
    # 143 	 North West Delhi
    # 148 	 Shahdara
    # 149 	 South Delhi
    # 144 	 South East Delhi
    # 150 	 South West Delhi
    # 142 	 West Delhi
    numdays = int(request.args.get('numdays'))
    age = int(request.args.get('age'))
    pin = int(request.args.get('pin'))
    isPin = int(request.args.get('isPin'))

    district = ['141','145','140','146','147','143','148','149','144','150','142']
    base = (datetime.datetime.today() + datetime.timedelta(days=numdays)).strftime("%d-%m-%Y")
    
    flag = False
    result = []
    #url ='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=141&date=08-05-2021'
    # FOR SEARCHING BY PINCODE
    #url - 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=152002&date=31-03-2021'
    if(isPin == 0):
        for dist_code in district:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_code, str(base))
            response = requests.get(URL)
            if response.ok:
                resp_json = response.json()['centers']
                #print(json.dumps(resp_json, indent = 1))
                for center in resp_json:
                    for session in center['sessions']:
                        if(int(session['min_age_limit']) == age):
                            if(session['available_capacity'] >= 0):
                                slot = [center['name'],center["district_name"],session['vaccine'],str(session['date']),str(session['available_capacity'])]
                                result.append(slot)
                                flag = True
    elif(isPin == 1):
        URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin, str(base))
        response = requests.get(URL)
        if response.ok:
            resp_json = response.json()['sessions']
            #print(json.dumps(resp_json, indent = 1))
            for center in resp_json:
                if(int(center['min_age_limit']) == age):
                    if(center['available_capacity'] >= 0):
                        slot = [center['name'],center["district_name"],center['vaccine'],str(center['date']),str(center['available_capacity'])]
                        result.append(slot)
                        flag = True
    else:
        flag=False

    if flag:
        return(jsonify({'data':result}))
    else:
        return("No Slots Available")
            