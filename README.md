# Windows Event Viewer

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <img src="https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white" alt="Windows">
</p>

**A lightweight, browser-based interface for exploring local Windows Event Logs.**

Windows Event Viewer puts useful system diagnostics in reach, but drilling into individual records can take time. This project offers a simple Streamlit interface for querying common Windows logs, narrowing results with filters, and inspecting event details in one place.

<p align="center">
  <img src="Media/demo2.gif" alt="Demo of the Windows Event Viewer interface" width="850">
</p>


## What it does

- **Browse common event logs:** query the System, Application, Security, and Setup logs on the local Windows machine.
- **Narrow down results:** filter by event level, event ID, and an optional start and end time.
- **Choose the result count:** request between 10 and 2,000 events, with 100 selected by default.
- **Inspect event details:** expand an event to view its available fields, including source, date, event ID, level, task, user, computer, and description.
- **Use a familiar web interface:** interact with the tool in your browser using Streamlit.

The application uses Windows' built-in `wevtutil` utility to query event logs. It is designed as a convenient companion for quick lookups and basic troubleshooting.

## Quick start

### Requirements

- Windows, with the built-in `wevtutil` command available
- Python 3
- Permission to read the event logs you want to inspect

Some logs or records—especially Security events—may require an elevated terminal or additional Windows permissions.

### Install and run

1. **Clone the repository**

   ```powershell
   git clone https://github.com/edwinfredy/Windows-Event-Viewer.git
   cd Windows-Event-Viewer
   ```

2. **(Recommended) Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install the dependency**

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. **Launch the application**

   ```powershell
   streamlit run main.py
   ```

Streamlit will print a local URL in the terminal. Open that URL in your browser to use the interface.

## Using the interface

1. Select a log: **System**, **Application**, **Security**, or **Setup**.
2. Choose an event-level filter, or leave it set to **Any**.
3. Optionally enter an event ID.
4. Optionally enter a start time and/or end time in UTC.
5. Set how many events to retrieve and select **Query Logs**.
6. Expand an event to inspect its parsed details.

For time filters, use a UTC timestamp compatible with Windows Event Log queries, for example:

```text
2025-01-31T00:00:00.000Z
```

Leave optional filters empty when you do not need them. The number-of-events control limits how many records the query requests; it does not guarantee that the selected log contains that many matching events.

## Project structure

```text
Windows-Event-Viewer/
├── Media/
│   └── demo2.gif        # Interface demo
├── main.py              # Streamlit UI and event-log query logic
├── requirements.txt     # Python dependencies
└── README.md
```

## Technology

- **Python** for the query and data-processing logic
- **Streamlit** for the browser-based interface
- **Windows `wevtutil`** for retrieving local event-log records

The project is intentionally compact: the interface and query logic are contained in `main.py`, and `requirements.txt` currently lists Streamlit as its dependency.

## Troubleshooting

**The query fails or returns no events**

- Try another log or remove optional filters to check whether the filter is too restrictive.
- Verify that the timestamp values are valid UTC timestamps.
- If querying a restricted log, open the terminal with higher permissions and launch the app again. **Some events can only be viewed when the tool has administrator access.**

**The application does not start**

- Confirm Python is installed and available from your terminal.
- Reinstall the dependencies with `python -m pip install -r requirements.txt`.
- Start the app from the repository directory using `streamlit run main.py`.

## Scope

This project focuses on querying and inspecting recent local event records. It does not currently provide live monitoring, `.evtx` file import, saved searches, or CSV/JSON export.

## Contributing

Suggestions, issue reports, and pull requests are welcome. When reporting a problem, include the Windows version, the log being queried, the filters used, and the error message (excluding any sensitive event data).

## License

This project is licensed under the MIT License.
