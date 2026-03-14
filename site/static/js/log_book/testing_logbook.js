function get_all_trips() {
    fetch("/api/get_trips", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) throw new Error('HTTP error ' + response.status);
        return response.json();
    })
    .then(trips => {
        const listElement = document.getElementById("trips-list");

        listElement.innerHTML = '';

        if (trips.length === 0) {
            listElement.innerHTML = '<li>No trips recorded yet.</li>';
            return;
        }

        trips.forEach(trip => {
            const li = document.createElement("li");

            // Format the date nicely
            const startDate = new Date(trip.start).toLocaleString();
            const pointCount = trip.points ? trip.points.length : 0;

            li.innerHTML = `
                <strong>Date:</strong> ${startDate} <br>
                <span>${pointCount} GPS points collected</span>
                <hr>
            `;

            listElement.appendChild(li);
        });
    })
    .catch((error) => {
        console.error('Error displaying trips:', error);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    get_all_trips();
});
