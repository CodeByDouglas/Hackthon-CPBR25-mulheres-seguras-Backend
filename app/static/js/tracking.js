// Inicializa o mapa
const map = L.map('map').setView([window.lat, window.lng], 15);

// Adiciona o tile layer do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Ícone SVG customizado no estilo Google Maps, cor #b18be4
const userIcon = L.divIcon({
    className: '',
    iconSize: [28, 34],
    iconAnchor: [14, 34],
    popupAnchor: [0, -34],
    html: `
      <svg width="28" height="34" viewBox="0 0 40 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="20" cy="16" rx="12" ry="12" fill="#b18be4" fill-opacity="0.95"/>
        <path d="M20 0C11.1634 0 4 7.16344 4 16C4 27.2 20 48 20 48C20 48 36 27.2 36 16C36 7.16344 28.8366 0 20 0ZM20 24C15.5817 24 12 20.4183 12 16C12 11.5817 15.5817 8 20 8C24.4183 8 28 11.5817 28 16C28 20.4183 24.4183 24 20 24Z" fill="#b18be4" fill-opacity="0.95"/>
        <ellipse cx="20" cy="16" rx="7" ry="7" fill="#fff" fill-opacity="0.85"/>
      </svg>
    `
});

// Adiciona o marcador com a última localização
let userMarker = L.marker([window.lat, window.lng], {icon: userIcon})
    .addTo(map)
    .bindPopup('Última localização conhecida')
    .openPopup();

// Desenha a rota se houver pontos
let routePoints = window.routePoints;
let polyline = L.polyline(routePoints, {color: 'red'}).addTo(map);
map.fitBounds(polyline.getBounds());

// Função para atualizar a rota a cada 30 segundos
function updateRoute() {
    const url = `/${window.token_nfc}/${window.call_id}/route`;
    console.log('Buscando rota em:', url);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Nova rota recebida:', data.route);
            if (data.route && data.route.length > 0) {
                polyline.setLatLngs(data.route);
                map.fitBounds(polyline.getBounds());
                // Atualiza o marcador para o último ponto da rota
                const lastPoint = data.route[data.route.length - 1];
                userMarker.setLatLng([lastPoint.lat, lastPoint.lng]);
            }
        })
        .catch(error => console.error('Erro ao atualizar rota:', error));
}

// Atualiza a rota a cada 30 segundos
setInterval(updateRoute, 30000); 