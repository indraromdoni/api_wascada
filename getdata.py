from flask import Flask, request, jsonify
import requests
import json
import time
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def getWAScada(ProjName="MAPi", Tag="MF30T_KWH", start_time="2024-08-13 13:00:00", interval=30, unit="S", record=2):
    header = {"authorization": "Basic YWRtaW46"}
    '''payload = {
        "Tags":[{"Name":Tag}]
    }'''
    payload = {
        "StartTime":start_time,
        "IntervalType":unit,
        "Interval":interval,
        "Records":record,
        "Tags":[{
                 "Name":Tag,
                 "DataType":"0"
        }]
    }
    url = "https://192.168.25.208/WaWebService/Json/GetDataLog/"+ProjName
    response = requests.post(url, verify=False, headers=header, json=payload)
    if response is not None:
        h = json.loads(response.text)
    else:
        print("none")
        h = 0
    return h

@app.route('/getDataSCADA', methods=['GET'])
def getData():
    print(request.method)
    if request.method != "GET":
        return "Only receive GET method"
    tagName = request.args.get("tagname")
    dt = request.args.get("date")
    tm = request.args.get("time")
    print(tagName, dt+" "+tm)
    res = getWAScada("MAPi", tagName, dt+" "+tm, 1, "S", 1)
    print(res)
    return res["DataLog"][0]

if __name__ == '__main__':
    print(getWAScada())
    app.run(host='0.0.0.0', port=5080, debug=True)