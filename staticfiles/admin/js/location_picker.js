document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const latInput = document.getElementById('id_latitude');
    const lngInput = document.getElementById('id_longitude');

    // Parse initial coordinates
    let initialLat = latInput.value ? parseFloat(latInput.value) : 42.8746;
    let initialLng = lngInput.value ? parseFloat(lngInput.value) : 74.5698;

    // Initialize map
    const map = L.map('map').setView([initialLat, initialLng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Initialize marker
    let marker = L.marker([initialLat, initialLng], {
        draggable: true
    }).addTo(map);

    // Initialize search control
    const provider = new GeoSearch.OpenStreetMapProvider({
        params: {
            'accept-language': 'ru,ky', // Russian and Kyrgyz
            countrycodes: 'kg', // Kyrgyzstan
        }
    });

    const searchControl = new GeoSearch.GeoSearchControl({
        provider: provider,
        style: 'bar',
        showMarker: false,
        searchLabel: 'Введите адрес на русском или кыргызском',
        autoComplete: true,
        autoCompleteDelay: 250,
        keepResult: true
    });

    map.addControl(searchControl);

    // Update coordinates function
    const updateCoordinates = (e) => {
        const coords = e.target.getLatLng();
        latInput.value = coords.lat.toFixed(6);
        lngInput.value = coords.lng.toFixed(6);
    };

    // Handle marker drag
    marker.on('dragend', updateCoordinates);

    // Handle map click
    map.on('click', function(e) {
        marker.setLatLng(e.latlng);
        updateCoordinates({ target: marker });
    });

    // Handle search result
    map.on('geosearch/showlocation', (result) => {
        const newCoords = result.location;
        marker.setLatLng([newCoords.y, newCoords.x]);
        map.setView([newCoords.y, newCoords.x], 16);
        latInput.value = newCoords.y.toFixed(6);
        lngInput.value = newCoords.x.toFixed(6);
    });

    // Handle search errors
    map.on('geosearch/error', (error) => {
        console.error('Search error:', error);
        alert('Адрес не найден. Пожалуйста, попробуйте другой вариант.');
    });
});