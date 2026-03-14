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
            const li = document.createElement("tr");

            // Format the date nicely
            const startDate = new Date(trip.start);
            const formattedDate = new Intl.DateTimeFormat('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                timeZone: 'Australia/Sydney'
            }).format(startDate);
            const startTime = startDate.toLocaleTimeString('en-GB', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Australia/Sydney'
            });
            const endDate = new Date(trip.end);
            const endTime = endDate.toLocaleTimeString('en-GB', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Australia/Sydney'
            });
            const pointCount = trip.points ? trip.points.length : 0;

            li.innerHTML = `
                <th>${formattedDate}</th>
                <td>[odometer start]</td>
                <td>[odometer end]</td>
                <td>${pointCount}</td>
                <td>[locations]</td>
                <td>[road types]</td>
                <td>[weather]</td>
                <td>[traffic]</td>
                <td>${startTime}</td>
                <td>${endTime}</td>
                <td>[time day]</td>
                <td>[time night]</td>
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
