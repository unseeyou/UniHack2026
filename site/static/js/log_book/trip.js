const points = [];

const pointsEl = document.getElementById("points");
for (const pointEl of pointsEl.children) {
    points.push({
        lat: parseFloat(pointEl.children[0].textContent),
        lng: parseFloat(pointEl.children[1].textContent)
    });
}

const map = L.map('map', {
    zoom: 18
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 12,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const tripTrail = L.polyline(points).addTo(map);

if (points.length == 1) {
    map.panTo(points[0]);
} else {
    map.fitBounds(tripTrail.getBounds());
}