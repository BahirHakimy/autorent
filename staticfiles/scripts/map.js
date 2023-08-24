var map = L.map('map').setView([34.540512, 69.170757], 13);
navigator.geolocation.getCurrentPosition((location) => {
  console.log(location.coords);
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
}).addTo(map);

const route = L.Routing.control({
  waypoints: [L.latLng(34.540512, 69.170757), L.latLng(34.7331354, 69.8804592)],
  routeWhileDragging: true,
});
// route.addTo(map);
route.on('routesfound', (e) => {
  console.log(e);
});
L.marker([34.540512, 69.170757]).addTo(map).bindPopup('Netlinks').openPopup();
