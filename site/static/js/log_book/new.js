import { startTransition } from "react";
import { getPosition, watchPosition } from "../geolocation.js";
import { CenterOnUserController } from "../map/center_on_user.js";

const coords = (await getPosition()).coords;
const map = L.map('map', {
    center: [coords.latitude, coords.longitude],
    zoom: 18
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 12,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const locationMarker = L.circleMarker([coords.latitude, coords.longitude]).addTo(map);
const tripTrail = L.polyline([]).addTo(map);

map.addControl(new CenterOnUserController(locationMarker, { position: "bottomright" }));

/**
 * @type {{
 *  start: Date,
 *  points: { lat: number, lng: number, time: Date }[]
 * } | null}
 */
let currentTrip = null;

/** @type {GeolocationCoordinates} */
let currentCoords = coords;

watchPosition(
    (position) => {
        const { latitude: lat, longitude: lng } = currentCoords = position.coords;

        if (currentTrip != null) {
            currentTrip.points.push({ time: new Date(), lat, lng });
        }

        updateMap();
    },
    (error) => console.error("Error tracking location:", error),
    {
        enableHighAccuracy: true,
        timeout: 1000
    }
);

let startOdometer = null;

window.confirmStart = function confirmStart() {
    const value = document.getElementById('odometer-input').value;

    if (!value) return;
    startOdometer = parseFloat(value);

    bootstrap.Modal.getInstance(document.getElementById('odometer-modal')).hide();

    startTrip();

    bootstrap.Offcanvas.getOrCreateInstance(document.getElementById('trip-stats')).show();
}

let timerIntervalId;

window.startTrip = function startTrip() {
    document.getElementById("start-btn").hidden = true;
    document.getElementById("end-btn").hidden = false;

    timerIntervalId = setInterval(updateTimer, 1000);
    updateTimer();

    currentTrip = {
        start: new Date(),
        points: []
    }
}

window.stopTrip = function stopTrip() {
    bootstrap.Offcanvas.getOrCreateInstance(document.getElementById('trip-stats')).hide();


    document.getElementById("start-btn").hidden = false;
    document.getElementById("end-btn").hidden = true;

    clearInterval(timerIntervalId);

    const body = JSON.stringify({
        start: currentTrip.start,
        end: new Date(),
        points: currentTrip.points
    });

    currentTrip = null;

    fetch("/api/trip", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: body,
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

    // redirect to /log-book
    window.location.href = "/log-book";
}

function updateTimer() {
    if (currentTrip == null) return;

    const seconds = Math.floor((new Date().getTime() - currentTrip.start.getTime()) / 1000);

    // Format the seconds into HH:MM:SS
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');

    document.getElementById("timer").textContent = `${hrs}:${mins}:${secs}`;
}

function updateMap() {
    locationMarker.setLatLng({ lat: currentCoords.latitude, lng: currentCoords.longitude });
    tripTrail.setLatLngs(currentTrip?.points ?? []);
}
