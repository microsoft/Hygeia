async function askQuestion() {
    const question = document.getElementById('question').value;
    const sessionId = document.getElementById('sessionId').value;
    const responseDiv = document.getElementById('response');
    const appUrl = 'https://hygeia-pj-demo.azurewebsites.net/api/ask'; // Update with your Azure Function URL

    try {
        const response = await fetch(appUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: question, sessionId: sessionId }) // Send the question as "prompt"
        });

        if (response.ok) {
            const data = await response.json();
            // Assuming data contains the "text" field from Azure Function response
            responseDiv.textContent = data.text; // Display the text response
        } else {
            responseDiv.textContent = 'Error: ' + response.statusText;
        }
    } catch (error) {
        responseDiv.textContent = 'Error: ' + error.message;
    }
}

