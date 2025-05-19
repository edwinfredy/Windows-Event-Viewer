import subprocess
import re
import streamlit as st

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

def queryWevtutil(count=1500, log='System', level=None, eventID=None, timeStart=None, timeEnd=None):
    wevtCommand = f'wevtutil qe {log} /format:text /rd:true /c:{count}'

    if log == "Setup":
        if level == "4":
            level = "0"
        if level != "0":
            level = "10"
    else:
        if level == "0":
            level = None

    if level or eventID or timeStart or timeEnd:
        queryParts = []
        wevtQuery = ' /q:"'
        if level:
            queryParts.append(f'Event/System[Level={level}]')
        if eventID:
            queryParts.append(f'Event/System/EventID={eventID}')
        if timeStart:
            queryParts.append(f"Event/System/TimeCreated[@SystemTime>='{timeStart}']")
        if timeEnd:
            queryParts.append(f"Event/System/TimeCreated[@SystemTime<='{timeEnd}']")
        wevtQuery += " and ".join(queryParts) + '"'
        wevtCommand += wevtQuery

    logs = subprocess.check_output(wevtCommand).decode('utf-8', errors='ignore')
    pattern = re.compile(r'Event\[\d+\](.*?)(?=Event\[\d+\]|$)', re.DOTALL)
    matches = re.findall(pattern, logs)
    matches.append(logs.rsplit('Event', 1)[-1].strip())
    system_events = [parse_event_log(event.strip()) for event in matches[:-1]]
    return system_events

# === Streamlit App ===

st.title("Windows Event Viewer")

log = st.selectbox("Select Log Type", ['System', 'Application', 'Security', 'Setup'])
level = st.selectbox("Event Level", ['Any', '1', '2', '3', '4', '0'])
eventID = st.text_input("Event ID (optional)", "")
timeStart = st.text_input("Start Time (UTC, optional)", "")
timeEnd = st.text_input("End Time (UTC, optional)", "")
count = st.slider("Number of Events", min_value=10, max_value=2000, value=100, step=10)

if st.button("Query Logs"):
    level_val = None if level == "Any" else level
    events = queryWevtutil(count=count, log=log, level=level_val,
                           eventID=eventID or None,
                           timeStart=timeStart or None,
                           timeEnd=timeEnd or None)
    st.success(f"Retrieved {len(events)} events")
    for i, event in enumerate(events):
        with st.expander(f"Event {i + 1} - {event['Source']} (ID: {event['Event ID']})"):
            st.json(event)
