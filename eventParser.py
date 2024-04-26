from evtx import PyEvtxParser
# from Evtx.Evtx import Evtx
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import json

records = []

parser = PyEvtxParser("C:\\Users\\HP\\Desktop\\Microsoft-Windows-AllJoyn%4Operational.evtx")
# parser = PyEvtxParser("C:\\Users\\HP\\Desktop\\Security.evtx")


counter = 0

for record in parser.records():
        records.append(record)
        counter = counter + 1

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/getEventID')
def giveEventID():
    print (records[0])
    return records[0:1000]

app.run(debug=True)
