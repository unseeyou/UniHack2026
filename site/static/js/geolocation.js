function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    // Geolocation is not supported by this browser
    console.log("Geolocation is not supported by this browser.");
  }
  return "e";
}

function showPosition(position) {
  // Access latitude and longitude
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
  // You can then use this data with mapping APIs like Google Maps or Leaflet.js
}

function showError(error) {
  // Handle cases where the user denies permission or location cannot be found
  switch(error.code) {
    case error.PERMISSION_DENIED:
      console.error("User denied the request for geolocation.");
      break;
    case error.POSITION_UNAVAILABLE:
      console.error("Location information is unavailable.");
      break;
    case error.TIMEOUT:
      console.error("The request to get user location timed out.");
      break;
    case error.UNKNOWN_ERROR:
      console.error("An unknown error occurred.");
      break;
  }
}

let geoInterval = null;

function enableGeo() {
  // Prevent multiple intervals from starting
  if (geoInterval) return;

  // This runs getLocation every 2000ms (2 seconds)
  geoInterval = setInterval(getLocation, 2000);
  console.log("Geolocation polling enabled.");
}

function disableGeo() {
  clearInterval(geoInterval);
  geoInterval = null;
  console.log("Geolocation polling disabled.");
}
