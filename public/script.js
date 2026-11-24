let currentSkip = 0;

async function fetchMosques(skip = 0) {
    const res = await fetch(`http://127.0.0.1:8000/mosques/?limit=15&skip=${skip}`)
    if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
    }

    return await res.json();
}

function populateMosqueCards(mosques) {
    const listSection = document.querySelector(".list-section");
    if (!listSection) return;

    listSection.innerHTML = "<h2>List View</h2>";

    mosques.forEach((mosque) => {
        const card = document.createElement("div");
        card.classList.add("mosque-card");
        
        const imagePath = `images/mosques/${mosque.google_places_id}.jpg`;

        card.innerHTML = `
            <img src="${imagePath}" alt="Photo of ${mosque.name}" onerror="this.onerror=null; this.src='images/empty_box.png';">
            <div class="card-details">
                <h3>
                    ${mosque.name}
                </h3>
                <p>
                    ${mosque.address}
                </p>
            <div class="badge-group">
                    <button class="mosque-feature verified">&#10003; Women's Section</button>
                    <button class="mosque-feature">&#9733; ${mosque.rating}</button>
                    <button class="mosque-feature">&#128205 Distance</button>
                </div>
            </div>
        `;

        listSection.appendChild(card);
    });
}

async function initMap() {
    const mapElement = document.querySelector("gmp-map");
    if (!mapElement) return null;

    const [{ AdvancedMarkerElement }] = await Promise.all([
        google.maps.importLibrary('marker'),
        google.maps.importLibrary('maps'),
    ]);

    const innerMap = mapElement.innerMap;
    innerMap.setOptions({
        mapTypeControl: false,
    });

    return { innerMap, AdvancedMarkerElement };
}

function renderMapMarkers(mosques, mapTools) {
    if (!mapTools) return;
    const { innerMap, AdvancedMarkerElement } = mapTools;

    mosques.forEach((mosque) => {
        if (mosque.latitude != null && mosque.longitude != null) {
            new AdvancedMarkerElement({
                map: innerMap,
                position: { lat: mosque.latitude, lng: mosque.longitude },
                title: mosque.name,
            });
        }
    });
}

async function initApp() {
    try {
        const [mosques, mapTools] = await Promise.all([
            fetchMosques(),
            initMap(),
        ]);

        populateMosqueCards(mosques);
        populateMapMarkers(mosques, mapTools);
    } catch (error) {
        console.error("Failed to initialize app:", error);
    }
}

void initApp();