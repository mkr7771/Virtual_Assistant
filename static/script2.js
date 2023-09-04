document.addEventListener("DOMContentLoaded", function () {
  // Get a reference to the conversation <div> element
  const conversationDiv = document.getElementById("conversation");

  // Function to add a message to the conversation
  function addMessageToConversation(message, sender) {
    // Create a <p> element for the message
    const messageElement = document.createElement("p");

    // Set the text content based on the sender
    if (sender === "User") {
      messageElement.textContent = "User: " + message;
    } else {
      messageElement.textContent = "AI Counselor: " + message;
    }

    // Append the <p> element to the conversation <div>
    conversationDiv.appendChild(messageElement);

    // Scroll the conversation <div> to the bottom to show the latest message
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
  }

  // Display a welcome message when the page loads
  addMessageToConversation("Welcome to the AI Counselor chat!", "AI Counselor");
});
