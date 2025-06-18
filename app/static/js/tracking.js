// Inicializa o mapa
const map = L.map('map').setView([window.lat, window.lng], 15);

// Adiciona o tile layer do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Adiciona o marcador com a última localização
L.marker([window.lat, window.lng])
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
            }
        })
        .catch(error => console.error('Erro ao atualizar rota:', error));
}

// Atualiza a rota a cada 30 segundos
setInterval(updateRoute, 30000); 