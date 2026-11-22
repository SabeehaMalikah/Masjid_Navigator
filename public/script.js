async function init() {
    const [{ AdvancedMarkerElement }] = await Promise.all([
        google.maps.importLibrary('marker'),
        google.maps.importLibrary('maps'),
    ]);

    const mapElement = document.querySelector('gmp-map');
    if (!mapElement) return;

    const innerMap = mapElement.innerMap;
    innerMap.setOptions({
        mapTypeControl: false,
    });

    // Marker positioned at Brooklyn center coordinates from index.html
    new AdvancedMarkerElement({
        map: innerMap,
        position: mapElement.center,
        title: 'Nearby Masjid (Brooklyn, NY)',
    });
}

void init();