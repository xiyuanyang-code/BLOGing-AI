// url judgement
function isValidUrl(url) {
    const pattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return pattern.test(url);
}

const sending_status = document.getElementById("status-sending")
// ! backend port: 5000
const backendApiUrl = 'http://127.0.0.1:5000/api/process_text'

document.getElementById("click-to-send").onclick = async function() {
    const responseArea = document.getElementById("response-area");
    const input_url = document.getElementById("user-input").value
    if (input_url == "") {
        window.alert(`WARNING! Empty input.`)
        return
    }

    if (isValidUrl(input_url) == false) {
        window.alert(`Warning! ${input_url} is not a valid url!`)
        return
    }
    // test passed

    // sending urls to the backend
    try {
        // sending with fetch api
        const response = await fetch(backendApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({url: input_url})
        });

        if (!response.ok) {
            throw new Error(`HTTP Error! Code: ${response.status}`);
        }
        sending_status.textContent = `Sending urls to the AI hiding behind...`

        const data = await response.json();
        responseArea.textContent = JSON.stringify(data, null, 2);
        sending_status.textContent = "Successfully received response!";

    } catch (error) {
        console.error('Error: ', error);
        responseArea.textContent = `Error: ${error.message}.`;
    }
}
