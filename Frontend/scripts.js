const API_URL = "http://127.0.0.1:8000/trips/"; // Backend API URL

// Retrieve or generate session ID
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID(); // Generate a unique session ID
    localStorage.setItem("session_id", sessionId);
}

// Submit Trip Form
document.getElementById("tripForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Collect form data
    const destination = document.getElementById("destination").value;
    const date = document.getElementById("date").value;
    const days = parseInt(document.getElementById("days").value);
    const budget = parseFloat(document.getElementById("budget").value);
    const travelers = document.getElementById("travelers").value;

    // Get selected activities
    const activities = Array.from(document.querySelectorAll("input[type=checkbox]:checked"))
                           .map(cb => cb.value);

    const tripData = { destination, date, days, budget, travelers, activities };

    // Send trip data to backend
    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tripData)
    });

    if (response.ok) {
        loadTrips(); // Refresh trip list
        document.getElementById("tripForm").reset();
    } else {
        alert("Failed to save trip!");
    }
});

// Load Trips
async function loadTrips() {
    const response = await fetch(API_URL, { method: "GET" });

    if (response.ok) {
        const trips = await response.json();
        const tripsList = document.getElementById("tripsList");
        tripsList.innerHTML = ""; // Clear list

        trips.forEach(trip => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";

            // Format `created_at`
            const createdAt = new Date(trip.created_at).toLocaleString();

            li.innerHTML = `
                <div>
                    <strong>${trip.destination}</strong> - ${trip.date} (${trip.days} days) - $${trip.budget}
                    <br><small>Travelers: ${trip.travelers} | Activities: ${trip.activities.join(", ")}</small>
                    <br><small><em>Created on: ${createdAt}</em></small>
                </div>
                <button class="btn btn-danger btn-sm" onclick="deleteTrip(${trip.id})">Delete</button>
            `;

            tripsList.appendChild(li);
        });
    }
}

// Delete Trip
async function deleteTrip(tripId) {
    const response = await fetch(`${API_URL}${tripId}`, { method: "DELETE" });

    if (response.ok) {
        loadTrips(); // Refresh list
    } else {
        alert("Failed to delete trip!");
    }
}

// Load trips when page loads
loadTrips();
