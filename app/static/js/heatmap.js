document.addEventListener('DOMContentLoaded', function () {
    // Coordenadas para o centro do Brasil
    const centerLat = -14.2350;
    const centerLng = -51.9253;

    // Inicializa o mapa, centralizado no Brasil
    const map = L.map('map').setView([centerLat, centerLng], 5);

    // Adiciona o tile layer do OpenStreetMap (tema escuro)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);

    // Verifica se há pontos de calor para renderizar
    if (window.heatPoints && window.heatPoints.length > 0) {
        // Cria a camada de calor (heatmap) com os pontos fornecidos
        const heatLayer = L.heatLayer(window.heatPoints, {
            radius: 25,          // Raio de influência de cada ponto
            blur: 15,            // Nível de desfoque
            maxZoom: 12,         // Zoom máximo para a camada de calor
            gradient: {          // Gradiente de cores (rosa -> vermelho -> amarelo)
                0.4: '#d94474',
                0.6: '#e46262',
                1.0: '#f5d5e2'
            }
        }).addTo(map);

        // Ajusta o zoom do mapa para englobar todos os pontos de calor
        const bounds = L.latLngBounds(window.heatPoints.map(p => [p[0], p[1]]));
        if (bounds.isValid()) {
            map.fitBounds(bounds);
        }
    } else {
        console.log("Nenhum dado de calor para exibir.");
    }
}); 