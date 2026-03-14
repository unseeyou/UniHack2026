let watchID;
let pathCoordinates;
let startTime;
let seconds = 0;
let timerInterval;

function enableGeo() {
    // disable the start button
    document.getElementById("start-btn").disabled = true;

    // enable the end button
    document.getElementById("end-btn").disabled = false;

    // This runs getLocation every 1000ms (1 second)
    pathCoordinates = [];

    startTime = new Date();
    timerInterval = setInterval(updateTimer, 1000);

    // This starts the tracking
    watchID = navigator.geolocation.watchPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        pathCoordinates.push({ time: new Date(), lat: latitude, lng: longitude });

        console.log("New point added to path:", latitude, longitude);
      },
      (error) => console.error("Error tracking location:", error),
      {
        enableHighAccuracy: true, // Uses GPS instead of just Wi-Fi
        timeout: 5000,
        maximumAge: 0
      }
    );

    console.log("Geolocation polling enabled.");
}

function disableGeo() {
    if (watchID) {
        navigator.geolocation.clearWatch(watchID);
    }

    // enable the start button
    document.getElementById("start-btn").disabled = false;

    // disable the end button
    document.getElementById("end-btn").disabled = true;

    console.log("Geolocation polling disabled.");

    clearInterval(timerInterval);

    fetch("/api/trip", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Inform the server the body is JSON
        },
        body: JSON.stringify({
            start: startTime,
            end: new Date(),
            points: pathCoordinates
        }),
    }).then(response => {
        if (!response.ok) {
            // Handle non-successful responses (e.g., 404, 500)
            throw new Error('HTTP error ' + response.status);
        }
        return response.json(); // Parse the JSON response body
    })
    .then(data => {
        console.log('Success:', data); // Handle the successful response data
    })
    .catch((error) => {
        console.error('Error:', error); // Handle network errors or rejected promises
    });
}

function updateTimer() {
    seconds++;

    // Format the seconds into HH:MM:SS
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');

    document.getElementById("timer").textContent = `${hrs}:${mins}:${secs}`;
}
