document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Get the URL from the HTML (The "Handoff")
    const loadingContainer = document.getElementById('loading-container');
    if (!loadingContainer) return; // Stop if element is missing
    const apiUrl = loadingContainer.getAttribute('data-api-url');

    // --- A. Funny Loading Messages ---
    const messages = [
        "Judging your life choices...",
        "Asking AI why you listen to this...",
        "Analyzing cringe levels...",
        "Reviewing your breakup songs...",
        "Generating insults...",
        "Trying not to laugh..."
    ];

    const loadText = document.getElementById('loading-text');
    let msgIndex = 0;

    // Change message every 1.5 seconds
    const msgInterval = setInterval(() => {
        if (loadText) {
            msgIndex = (msgIndex + 1) % messages.length;
            loadText.innerText = messages[msgIndex];
        }
    }, 1500);

    // --- B. The AJAX Call ---
    fetch(apiUrl) 
        .then(response => response.json())
        .then(data => {
            // 1. Stop the loading text cycle
            clearInterval(msgInterval);

            // 2. Inject Data into HTML
            const headline = document.getElementById('ui-headline');
            const body = document.getElementById('ui-roast-body');
            const score = document.getElementById('ui-score');
            const dating = document.getElementById('ui-dating');

            // Safety check: Only update if elements exist
            if (headline) headline.innerText = `"${data.headline}"`;
            if (body) body.innerHTML = data.roast_body;
            if (score) score.innerText = data.score;
            if (dating) dating.innerText = data.dating_life;

            // 3. Swap Views (Hide Loading -> Show Results)
            const resDiv = document.getElementById('result-container');

            loadingContainer.style.display = 'none'; // Hide Spinner
            
            if (resDiv) {
                resDiv.classList.remove('hidden'); // Show Roast
                resDiv.classList.add('fade-in'); // Trigger Animation
            }
        })
        .catch(error => {
            console.error("Error fetching roast:", error);
            if (loadText) {
                loadText.innerText = "Error: Your music taste was too bad for the AI.";
                loadText.style.color = "red";
            }
            const vinyl = document.querySelector('.vinyl-record');
            if (vinyl) vinyl.style.animationPlayState = 'paused';
        });
});