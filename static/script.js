function updateEmotionTable(emotionPercentages) {
    var tableBody = document.querySelector("#emotion-table tbody");
    tableBody.innerHTML = "";
    for (var emotion in emotionPercentages) {
        var row = tableBody.insertRow();
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.textContent = emotion;
        cell2.textContent = emotionPercentages[emotion] + "%";
    }
}

function updateStressLevel(stressLevel) {
    var stressLevelElement = document.querySelector("#stress-level");
    stressLevelElement.textContent = stressLevel;
}

function startCounselling() {
    window.location.href = '/process_route';
}

function resetCounselling() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/reset", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Redirect to the login page after resetting
            window.location.href = '/login';
        }
    };
    xhr.send();
}

const eventSource = new EventSource('/stream');
const conversationElement = document.getElementById("conversation");

eventSource.onmessage = function (event) {
    const newMessage = event.data.trim();  // Trim any leading/trailing whitespace
    if (newMessage) {
        // Append the new message to the conversation list
        appendMessageToConversation(newMessage);
    }
};

function toggleRecords() {
    const recordsElement = document.querySelector(".previous-stress-level");
    recordsElement.classList.toggle("expanded");
}

function appendMessageToConversation(message) {
    const conversationList = document.querySelector("#conversation ul");
    const messageElement = document.createElement("li");
    messageElement.classList.add("message");

    messageElement.textContent = message;
    conversationList.insertBefore(messageElement, conversationList.firstChild);
}

function togglePreviousRecords() {
    const previousRecords = document.getElementById("previous-records");
    if (previousRecords.style.display === "block") {
        previousRecords.style.display = "none";
    } else {
        previousRecords.style.display = "block";
    }
}