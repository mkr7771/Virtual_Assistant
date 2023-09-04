// ...

function resetCounselling() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/reset", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Reset the emotion table
            updateEmotionTable({});
            // Update the stress level
            updateStressLevel(0); // Pass the stress level value you want to display
        }
    };
    xhr.send();
}

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

function redirectToLogin() {
    window.location.href = '/login';
}

function startCounselling() {
    window.location.href = '/process_route';
}

function redirectToRegister() {
    // Redirect the user to the registration page
    window.location.href = '/register'; // Update this URL to match your registration route
}

// ... (your existing code)

// Call initSSEConversation() when the page loads
window.addEventListener("load", initSSEConversation);

// Add a function to update stress level and emotion percentages when the page loads
window.addEventListener("load", function () {
    fetch("/process_route")
        .then(response => response.json())
        .then(data => {
            // Update the emotion table
            updateEmotionTable(data.emotion_percentages);
            // Update the stress level
            updateStressLevel(data.stress_level);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});

// ...
