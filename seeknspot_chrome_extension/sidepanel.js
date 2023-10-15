chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    let currentTab = tabs[0];

    if (currentTab && currentTab.url && currentTab.url.includes('youtube.com')) {
        const youtubeURL = currentTab.url;

        // Send the YouTube URL to your Flask backend
        fetch('http://localhost:5001/receive-youtube-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ youtubeURL }),
        }).then(() => console.log("POST REQUEST SUCCESSFUL")).then(response => console.log(JSON.stringify(response)));
       

        // Optionally, store the URL in a variable for later use
        // const storedURL = youtubeURL;
    } else {
        // Handle the case when the current page is not a YouTube page
        alert("You're not on a YouTube page! Please retry the extension with a Youtube page!");
        setTimeout(function() {
            window.close();
        }, 1000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const openUrlButton = document.getElementById('openUrlButton');
    
    openUrlButton.addEventListener('click', function() {
        // Fetch the URL from the backend
        fetch('http://localhost:5001/get-url-file')
            .then(response => response.json())
            .then(data => {
                const url = data.url;
                console.log("Received URL:", url);
                
                // Update the current tab with the received URL
                chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                    const currentTab = tabs[0];
                    if (currentTab && url) {
                        chrome.tabs.update(currentTab.id, { url });
                        //chrome.runtime.reload();
                        //window.location.reload();
                        //chrome.tabs.reload(tabs.id);
                    } else {
                        alert("URL is empty or doesn't exist");
                    }
                });
            })
            .catch(error => {
                console.error("Error fetching URL:", error);
                alert("Failed to fetch URL");
            });
    });
});

document.addEventListener('click', function(event) {
    if (event.target.tagName === 'A') {
        window.location.reload();
    }
});