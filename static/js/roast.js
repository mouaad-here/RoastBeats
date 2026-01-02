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

            // 3. Update URL if roast_id is present
            if (data.roast_id) {
                const newUrl = `/r/${data.roast_id}/`;
                window.history.pushState({path: newUrl}, '', newUrl);
            }

            // 4. Swap Views (Hide Loading -> Show Results)
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

/* =========================================
   SHARE & PREVIEW LOGIC
   ========================================= */

let generatedImageData = null;

window.openShareModal = function() {
    // 1. Setup UI and show modal with spinner immediately
    const modal = document.getElementById('shareModal');
    const spinner = document.getElementById('preview-spinner');
    const imgPreview = document.getElementById('share-preview-img');
    
    modal.style.display = 'flex';
    spinner.style.display = 'block';
    imgPreview.style.display = 'none';

    // 2. Target the visible card and clone it for off-screen rendering
    const cardElement = document.querySelector('.glass-card');
    const clone = cardElement.cloneNode(true);
    
    // 3. Apply capture styles and position the clone off-screen
    clone.classList.add('capture-mode');
    clone.style.position = 'absolute';
    clone.style.left = '-9999px';
    clone.style.top = '0px';
    
    // Append to the body so it can be rendered by html2canvas
    document.body.appendChild(clone);

    // 4. Generate Image from the off-screen clone
    html2canvas(clone, {
        scale: 2, // High Res
        useCORS: true,
        logging: false,
        backgroundColor: '#121212' // Explicit dark background for the PNG
    }).then(canvas => {
        // 5. Cleanup the clone
        document.body.removeChild(clone);

        // 6. Show the final preview image in the modal
        generatedImageData = canvas.toDataURL("image/png");
        imgPreview.src = generatedImageData;
        
        spinner.style.display = 'none';
        imgPreview.style.display = 'block';

    }).catch(err => {
        console.error("Error generating image:", err);
        
        // Ensure clone is removed even on error
        if (document.body.contains(clone)) {
            document.body.removeChild(clone);
        }
        
        // Hide modal and show an alert
        modal.style.display = 'none';
        alert("Could not generate image. Please screenshot instead.");
    });
};

/**
 * Converts a base64 data URL to a File object.
 */
async function dataUrlToFile(dataUrl, fileName) {
    const res = await fetch(dataUrl);
    const blob = await res.blob();
    return new File([blob], fileName, { type: 'image/png' });
}

/**
 * Shares the generated roast card image using the Web Share API.
 */
async function shareImage() {
    if (!generatedImageData) {
        alert("Image has not been generated yet.");
        return;
    }

    const score = document.getElementById('ui-score').innerText || "N/A";
    const imageFile = await dataUrlToFile(generatedImageData, `RoastBeats_${score}.png`);
    
    const shareData = {
        files: [imageFile],
        title: `My RoastBeats Score: ${score}/100`,
        text: `The AI roasted my music taste and gave me a ${score}/100. See what it says about you!`,
        url: window.location.href
    };

    try {
        await navigator.share(shareData);
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error("Share failed:", err);
            alert("Something went wrong. Please try again.");
        }
    }
}

/**
 * Fallback function to share a URL to a specific platform.
 */
function shareTo(platform) {
    const url = window.location.href;
    const encUrl = encodeURIComponent(url);
    
    let link = "";
    if(platform === 'whatsapp') link = `https://wa.me/?text=${encUrl}`;
    if(platform === 'x') link = `https://x.com/intent/tweet?url=${encUrl}`;
    if(platform === 'facebook') link = `https://www.facebook.com/sharer/sharer.php?u=${encUrl}`;
    
    if(link) window.open(link, '_blank');
}

/**
 * Main handler for share button clicks. Prefers Web Share API for images,
 * otherwise falls back to sharing a link.
 */
window.handleShareClick = function(platform) {
    if (navigator.share) {
        shareImage();
    } else {
        shareTo(platform);
    }
};

window.savePreviewImage = function() {
    if (!generatedImageData) return;
    const link = document.createElement('a');
    const score = document.getElementById('ui-score').innerText || "Roast";
    link.download = `RoastBeats_${score}.png`;
    link.href = generatedImageData;
    link.click();
};

window.closeShareModal = function() {
    document.getElementById('shareModal').style.display = 'none';
};