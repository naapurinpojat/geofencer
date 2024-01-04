var map = L.map('map').setView([62.7708962631589, 22.79477884392867], 13);
var geojsonFeature;
var dogmarker;
var geojsonobjects = [];
geojsonobjects.polygons = [];
geojsonobjects.markers = [];
const headerkeyword = 'Authorization';
const apiheader = {
    'Authorization': '0028b076-ca97-44c5-9603-bdfc38e2718e',
};

var url = '/snowdog/map.geojson';
// Create a synchronous XMLHttpRequest object
var xhr = new XMLHttpRequest();
xhr.open('GET', url, false); // The third parameter (false) makes the request synchronous
xhr.send();

// Check if the request was successful (status code 200)
if (xhr.status === 200) {
    // Log or do something with the response text
    //console.log(xhr.responseText);
    geojsonFeature = JSON.parse(xhr.responseText);
} else {
    // Handle errors
    console.error('Error:', xhr.statusText);
}

url = '/snowdog/api/version';
// Create a synchronous XMLHttpRequest object
xhr = new XMLHttpRequest();
xhr.open('GET', url, false); // The third parameter (false) makes the request synchronous
xhr.setRequestHeader(headerkeyword, apiheader.Authorization);
xhr.send();

// Check if the request was successful (status code 200)
if (xhr.status === 200) {
    // Log or do something with the response text
    console.log(xhr.responseText);
    var appversion = JSON.parse(xhr.responseText);
} else {
    // Handle errors
    console.error('Error:', xhr.statusText);
}

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors, Naapurinpojat,' + appversion.version + "<a href='https://github.com/bittikettu/snowdog' target='_blank'>Github</a>",
}).addTo(map);

// Example GeoJSON data


for (var i = 0; i < geojsonFeature.features.length; i++) {
    var defaultColor = "rgba(255, 255, 255,0.5)";
    geojsonFeature.features[i].properties.fill = defaultColor;
    geojsonFeature.features[i].properties.fillColor = defaultColor;
    geojsonFeature.features[i].properties.color = defaultColor;
    geojsonFeature.features[i].properties.tooltipContent = "";
    geojsonFeature.features[i].properties.fillOpacity = 0.41;
    geojsonFeature.features[i].properties.weight = 0;

    var active = 'text-label';
    var textLayer = L.divIcon({
        className: active,
        html: '<div><i class="iconoir-antenna-signal"><em>' + geojsonFeature.features[i].properties.name + '</em></div>'
    });

    geojsonobjects.polygons[geojsonFeature.features[i].properties.name] = L.geoJSON(geojsonFeature.features[i], {
        style: function (feature) {
            return {
                fillColor: feature.properties.fillColor, // Set the fill color to red, or use the specified fill color in the properties
                weight: feature.properties.weight,
                opacity: feature.properties.fillOpacity1,
                color: feature.properties.color,
                fillOpacity: feature.properties.fillOpacity
            };
        }
    }).addTo(map);

    var polygonCenter = geojsonobjects.polygons[geojsonFeature.features[i].properties.name].getBounds().getCenter();

    // Create a marker at the center of the polygon
    geojsonobjects.markers[geojsonFeature.features[i].properties.name] = L.marker(polygonCenter, { icon: textLayer }).addTo(map);

}
//console.log(geojsonobjects);


function calculateColor(timestamp, transitiondays = 3) {
    // Calculate the time difference in milliseconds
    const currentTime = new Date().getTime();
    const timeDifference = currentTime - timestamp;

    // Maximum time for a full transition to red (24 * 3 (3 days) hours in milliseconds)
    const maxTimeForFullRed = 24 * transitiondays * 60 * 60 * 1000;

    // Calculate the color value between red and green based on time
    let colorValue = Math.min(1, timeDifference / maxTimeForFullRed);

    // Calculate the RGB values based on the colorValue
    const green = Math.round(255 * (1 - colorValue));
    const red = Math.round(255 * colorValue);
    const blue = 0; // Blue component is set to 0

    // Return the color value as an RGB string
    return `rgb(${red}, ${green}, ${blue})`;
}

function calculateColorForMarker(timestamp) {
    // Calculate the time difference in milliseconds
    const currentTime = new Date().getTime();
    const timeDifference = currentTime - timestamp;

    // Maximum time for a full transition to red 3 minutes in milliseconds)
    const maxTimeForFullRed = 4 * 60 * 1000;

    if (timeDifference < maxTimeForFullRed) {
        return "text-label_infence";
    }
    else {
        return "text-label";
    }
}

function calculateOffline(timestamp) {
    // Calculate the time difference in milliseconds
    const currentTime = new Date().getTime();
    const timeDifference = currentTime - timestamp;

    // Maximum time for a full transition to red 3 minutes in milliseconds)
    const maxTimeForFullRed = 4 * 60 * 1000;

    if (timeDifference < maxTimeForFullRed) {
        return "Online";
    }
    else {
        return "Offline";
    }

}

function checkColors() {

    axios.get('/snowdog/api/geojson', {
        headers: apiheader
    })
        .then(response => {
            // Handle the JSON data
            for (var i = 0; i < response.data.length; i++) {

                const dateObject = new Date(response.data[i].latest_ts);
                const color = calculateColor(dateObject.getTime(), 5);

                try {
                    var updatestring = "Viimeksi käyty:<br>" + response.data[i].latest_ts;
                    geojsonobjects.polygons[response.data[i].in_area].setStyle({ fillColor: color });
                    geojsonobjects.polygons[response.data[i].in_area].bindPopup(updatestring);

                    var textLayer = L.divIcon({
                        className: calculateColorForMarker(dateObject.getTime()),
                        html: '<div><i class="iconoir-antenna-signal"></i><em>' + response.data[i].in_area + '</em></div>'
                    });

                    geojsonobjects.markers[response.data[i].in_area].setIcon(textLayer);
                    geojsonobjects.markers[response.data[i].in_area].bindPopup(updatestring);


                } catch (error) {
                    //console.log(error);
                }
            }
        })
        .catch(error => {
            // Handle errors
            console.error('Axios error:', error);
        });

    axios.get('/snowdog/api/lastonline', {
        headers: apiheader
    })
        .then(response => {
            // Handle the JSON data
            const dateObject = new Date(response.data.online);
            var updatestring = '<img src = "/snowdog/geofencer.svg" alt="Geofencer"/>';
            document.querySelector('.overlay-text-bottom').innerHTML = updatestring;

        })
        .catch(error => {
            // Handle errors
            console.error('Axios error:', error);
        });
    axios.get('/snowdog/api/lastlocation', {
        headers: apiheader
    })
        .then(response => {
            if(dogmarker == null) {
                var dogicon = L.icon({
                    iconUrl: 'dog.png',
                    iconSize:     [50, 64], // size of the icon
                    iconAnchor:   [25, 32], // point of the icon which will correspond to marker's location
                    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
                });
                dogmarker = L.marker([response.data.lat, response.data.lon],{icon: dogicon}).addTo(map);
            }
            else {
                var newLatLng = new L.LatLng(response.data.lat, response.data.lon);
                dogmarker.setLatLng(newLatLng);
            }
        })
        .catch(error => {
            // Handle errors
            console.error('Axios error:', error);
        });
}
