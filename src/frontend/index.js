// URL validation function
function isValidUrl(url) {
    const pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return pattern.test(url);
}


// ! backend port: 5000
const sendingStatus = document.getElementById("status-sending");
const backendApiUrl = 'http://127.0.0.1:5000/api/process_text';

document.getElementById("click-to-send").onclick = async function() {
    const responseArea = document.getElementById("response-area");
    const inputUrl = document.getElementById("user-input").value.trim();
    const webWindow = document.getElementById("webshow");

    // Clear previous status and response
    sendingStatus.textContent = "";
    responseArea.textContent = "";

    // Input validation
    if (!inputUrl) {
        window.alert("WARNING! Empty input.");
        return;
    }
    if (!isValidUrl(inputUrl)) {
        window.alert(`Warning! ${inputUrl} is not a valid url!`);
        return;
    }

    // Show the URL in the iframe
    webWindow.src = inputUrl;

    // Send URL to backend
    sendingStatus.textContent = "Sending URL to the AI backend...";
    try {
        const response = await fetch(backendApiUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: inputUrl})
        });

        if (!response.ok) {
            throw new Error(`HTTP Error! Code: ${response.status}`);
        }

        const data = await response.json();
        responseArea.textContent = JSON.stringify(data, null, 2);
        sendingStatus.textContent = "Successfully received response!";
    } catch (error) {
        console.error('Error:', error);
        responseArea.textContent = `Error: ${error.message}`;
        sendingStatus.textContent = "Failed to get response from backend.";
    }
};

const iframe = document.getElementById('myIframe');
let lastUrl = '';
setInterval(function() {
  try {
    const currentUrl = iframe.contentWindow.location.href;
    if (currentUrl !== lastUrl) {
      lastUrl = currentUrl;
      console.log('iframe URL changed to:', currentUrl);
    }
  } catch (e) {
    console.log('Cannot access iframe URL due to cross-origin policy');
  }
}, 1000);