let currentEvents = []
let presentEventCount = 0
let countToLoad = 100

function loadMore() {
    pullData(count = 100, index = presentEventCount - 1)
    drawTable(presentEventCount, 100)
}

function drawTable(start, count = 100, clearFirst = false) {
    if (document.getElementById("noEventsBanner") != null) {
        document.getElementById("noEventsBanner").remove()
    }
    console.log("running drawTable")
    if (clearFirst) {
        let table = document.getElementById("mainTable")
        while (table.children.length > 1) {
            table.removeChild(table.lastChild)
        }
        document.getElementById("detailsDescription").textContent = ""
        document.getElementById("detailsUser").textContent = ""
        document.getElementById("detailsComputer").textContent = ""
        document.getElementById("detailsKeywords").textContent = ""
    }
    function elementClicked() {
        function internalFunction(evt) {
            let detailsDescription = document.getElementById("detailsDescription")
            let detailsUser = document.getElementById("detailsUser")
            let detailsComputer = document.getElementById("detailsComputer")
            let detailsKeywords = document.getElementById("detailsKeywords")
            detailsDescription.textContent = `${currentEvents[Number(evt.currentTarget.getAttribute('data-index'))].Description}`
            detailsUser.textContent = `${currentEvents[Number(evt.currentTarget.getAttribute('data-index'))].User}`
            detailsComputer.textContent = `${currentEvents[Number(evt.currentTarget.getAttribute('data-index'))].Computer}`
            detailsKeywords.textContent = `${currentEvents[Number(evt.currentTarget.getAttribute('data-index'))].Keyword}`

        }
        return internalFunction
    }
    const timeStampFormat = {hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true, year: 'numeric', month: 'long', day: '2-digit'}
    if (document.getElementById('loadMore') != null) {
        document.getElementById('loadMore').remove()
    }
    console.log(currentEvents)
    console.log("start:", start, "start + count: ", start + count)
    currentEvents.slice(start, start + count).forEach(element => {
        let newTr = document.createElement('tr')
        newTr.addEventListener('click', elementClicked())
        newTr.setAttribute("data-index", `${presentEventCount}`)
        let levelTd = document.createElement('td')
        let timestampTd = document.createElement('td')
        let sourceTd = document.createElement('td')
        let eventIDTd = document.createElement('td')
        eventIDTd.id = "eventIDTd"
        timestampTd.textContent = new Date(element.Date).toLocaleDateString('en-US', timeStampFormat)
        levelTd.textContent = element.Level
        sourceTd.textContent = element.Source
        eventIDTd.textContent = element["Event ID"]
        newTr.appendChild(levelTd)
        newTr.appendChild(timestampTd)
        newTr.appendChild(sourceTd)
        newTr.appendChild(eventIDTd)
        document.getElementById("mainTable").appendChild(newTr);
        presentEventCount++
    })
    
    //Loadmore Button
    if (document.getElementById("mainTable").children.length > 1) {
        newTr = document.createElement('tr')
        newTd = document.createElement('td')
        newButton = document.createElement('button')
        newTr.id = "loadMore"
        newTd.colSpan = 4
        newButton.id = "loadMoreButton"
        newButton.textContent = "Load More"
        newButton.addEventListener('click', loadMore)
        newTd.appendChild(newButton)
        newTr.appendChild(newTd)
        document.getElementById("mainTable").appendChild(newTr)
    }
    else {
        newTr = document.createElement('tr')
        newTr.id = "noEventsBanner"
        newTd = document.createElement('td')
        newTd.colSpan = 4
        newTd.textContent = "No events"
        newTr.appendChild(newTd)
        document.getElementById("mainTable").appendChild(newTr)
    }
}

function runWevtutil(log = "", level = "", eventID = "", timeStart = "", timeEnd = "") {
    presentEventCount = 0
    if (timeStart != "") {
        timeStart = new Date(timeStart).toISOString()
    }
    if (timeEnd != "") {
        timeEnd = new Date(timeEnd).toISOString()
    }
    console.log("running runWevtutil with", log, level, eventID, timeStart, timeEnd)
    return new Promise((resolve, reject) => {
        currentEvents = []
        let xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    console.log("Wevtutil response is: ", xhr.responseText)
                    resolve(xhr.responseText)

                } else {
                    console.error("XHR Error in runWevtutil Oh No!")
                    reject("XHR Error in runWevtutil Oh No!")
                }
            }
        };
        xhr.open('GET', `/runWevtutil?log=${log}&level=${level}&eventID=${eventID}&timeStart=${timeStart}&timeEnd=${timeEnd}`, true);
        xhr.send();
    })
}

function pullData(count = 100, index = 0) {
    console.log("running pullData")
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    responseParsed = JSON.parse(xhr.responseText)
                    currentEvents = currentEvents.concat(responseParsed)
                    resolve(xhr.responseText)
                } else {
                    console.error("XHR Error in pullData Oh No!")
                }
            }
        };
        xhr.open('GET', `/pullData?index=${index}&count=${count}`, true);
        xhr.send();
    })
}

async function motherDriver() {
    await runWevtutil()
    await pullData()
    await drawTable(0, 100)
}

document.addEventListener('DOMContentLoaded', function() {
    motherDriver()
    document.getElementById("submit").addEventListener('click', async function() {
        let log = undefined
        for (const option of document.querySelectorAll('input[name="logSource"]')) {
            if (option.checked) {
                log = option.value
                break
            }
        }
        let level = undefined
        for (const option of document.querySelectorAll('input[name="logLevel"]')) {
            if (option.checked) {
                level = option.value
                break
            }
        }
        let eventID = document.getElementById("eventID").value
        let timeStart = document.getElementById("timeStart").value
        let timeEnd = document.getElementById("timeEnd").value
        console.log(log, level, eventID, timeStart, timeEnd)
        await runWevtutil(log, level, eventID, timeStart, timeEnd)
        await pullData()
        await drawTable(presentEventCount, 100, true)
    })
})
