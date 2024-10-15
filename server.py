import subprocess
import re
from flask import Flask, request

print("Initializing server...")

parsed_events = []

def parse_event_log(log_string):
    log_dict = {}
    log_dict["Source"] = re.search(r'Source: (.+?)\n', log_string).group(1).strip()
    log_dict["Date"] = re.search(r'Date: (.+?)\n', log_string).group(1).strip()
    log_dict["Event ID"] = re.search(r'Event ID: (.+?)\n', log_string).group(1).strip()
    log_dict["Task"] = re.search(r'Task: (.+?)\n', log_string).group(1).strip()
    log_dict["Level"] = re.search(r'Level: (.+?)\n', log_string).group(1).strip().replace("\u0000", "")
    log_dict["Opcode"] = re.search(r'Opcode: (.+?)\n', log_string).group(1).strip()
    log_dict["Keyword"] = re.search(r'Keyword: (.+?)\n', log_string).group(1).strip().replace("\u0000", "")
    log_dict["User"] = re.search(r'User: (.+?)\n', log_string).group(1).strip()
    log_dict["User Name"] = re.search(r'User Name: (.+?)\n', log_string).group(1).strip()
    log_dict["Computer"] = re.search(r'Computer: (.+?)\n', log_string).group(1).strip()
    log_dict["Description"] = re.search(r'Description:\s*(.+)', log_string, re.DOTALL).group(1).strip().replace("\u0000", "")
    return log_dict

def queryWevtutil(count=1500, log='System', level = None, eventID = None, timeStart = None, timeEnd = None):
    parsed_events.clear()
    wevtCommand = f'wevtutil qe {log} /format:text /rd:true /c:{count}'
    print("level is", level)
    if log == "Setup":
        if level == "4":
            level = "0"
        if level != "0":
            level = "10"
    else:
        if level == "0":
            level = None
    if level is not None or eventID is not None or timeStart is not None or timeEnd is not None:
        queryCommands = []
        wevtQuery = ' /q:"'
        if level is not None:
            queryCommands.append(f'Event/System[Level={level}]')
        if eventID is not None:
            queryCommands.append(f'Event/System/EventID={eventID}')
        if timeStart is not None:
            queryCommands.append(f'Event/System/TimeCreated[@SystemTime>=\'{timeStart}\']')
        if timeEnd is not None:
            queryCommands.append(f'Event/System/TimeCreated[@SystemTime<=\'{timeEnd}\']')
        wevtQuery += " and ".join(queryCommands) + '"'        
        wevtCommand += wevtQuery

    print('wevtCommand is:', wevtCommand)
    logs = subprocess.check_output(wevtCommand).decode('utf-8', errors='ignore')
    pattern = re.compile(r'Event\[\d+\](.*?)(?=Event\[\d+\]|$)', re.DOTALL)
    matches = re.findall(pattern, logs)
    matches.append(logs.rsplit('Event', 1)[-1].strip())
    system_events = [match.strip() for match in matches]
    system_events = system_events[:len(system_events) - 1]
    for event in system_events:
        parsed_events.append(parse_event_log(event))
    return system_events

# Server matters
app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/maincss.css')
def loadCss():
    return app.send_static_file('maincss.css')

@app.route('/bootstrap.css')
def loadBootstrap():
    return app.send_static_file('bootstrap.css')

@app.route('/mainscript.js')
def loadJs():
    return app.send_static_file('mainscript.js')

@app.route('/runWevtutil')
def runWevtutil():
    log = request.args.get('log')
    level = request.args.get('level')
    eventID = request.args.get('eventID')
    timeStart = request.args.get('timeStart')
    timeEnd = request.args.get('timeEnd')
    if (log == ""):
        log = None
    if (level == ""):
        level = None
    if (eventID == ""):
        eventID = None
    if (timeStart == ""):
        timeStart = None
    if (timeEnd == ""):
        timeEnd = None
    queryWevtutil(log = log or "System", level = level, eventID=eventID, timeStart=timeStart, timeEnd=timeEnd)
    return "OK"

@app.route('/pullData')
def pullData():
    index = int(request.args.get('index'))
    count = int(request.args.get('count'))
    return parsed_events[index : index + count]

app.run(debug=True)
