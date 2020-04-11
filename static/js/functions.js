
var map = L.map('mapid').setView([51, 14], 3);


L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiamFyZWRlY28iLCJhIjoiY2s4bW4xOWEzMGVsZDNlb2N0a2V6OG85NSJ9.asyy8goul4W-iJwoN0xm-Q', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiamFyZWRlY28iLCJhIjoiY2s4bW4xOWEzMGVsZDNlb2N0a2V6OG85NSJ9.asyy8goul4W-iJwoN0xm-Q'
}).addTo(map);




L.control.scale().addTo(map);
var searchControl = new L.esri.Controls.Geosearch().addTo(map);
var results = new L.LayerGroup().addTo(map);
var geocoder = L.Control.Geocoder.nominatim();
var markers = []
var l_lat;
var data_markers = new Object();


window.onload = function () {
  fetch('/m')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        data_markers =  JSON.parse(text);
        var co = 0;
        
        console.log(Object.keys(data_markers).length)
        for(var key in data_markers) {
          co++;
          if (co <= (Object.keys(data_markers).length)/2)
            var ltt = 'latitude' + String(co)
            var lnn = 'longitude' + String(co)
            var valueltt = data_markers[ltt];
            var valuelnn = data_markers[lnn];
            console.log(co)
            marker = new L.marker([valueltt,valuelnn]);
            map.addLayer(marker);
};
    });
  
};



function onMapClick(e) {
  var id
  if (markers.length < 1) id = 0
  else id = markers[markers.length - 1]._id + 1
  var lat = (e.latlng.lat);
  var lng = (e.latlng.lng);

  var data_db = {
    latitude: lat,
    longitude: lng
  };
  fetch('/', {
    method: "POST",
    body: JSON.stringify(data_db),
    headers: new Headers({
      "content-type":"application/json"
    })
  });
  fetch('/m')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        data_markers =  text;
    });
  geocoder.reverse(e.latlng, map.options.crs.scale(map.getZoom()), function(results) {
  var r = results[0];
  var popupContent =
    '<a style="color:green;" class="btn" href="create_marker">Create Maker</a>' + 
    '<p>' + lat.toFixed(2) + ', ' + lng.toFixed(2) + '</p></br>' +
    '<p>' + r.name + '</p></br>' + 
    '<a  style="color: red; text-decoration: none; " class="btn" onclick="clearMarker(' + id + ')">Remove</a>';
  marker = new L.marker([lat,lng]);
  markers.push(marker);
  marker._id = id;
  map.addLayer(marker);
  marker.bindPopup(popupContent).openPopup();
  
})};

function clearMarker(id) {
  var new_markers = []
  markers.forEach(function(marker) {
    if (marker._id == id) map.removeLayer(marker)
    else new_markers.push(marker)
  })
  markers = new_markers
}

map.on('click', onMapClick);

map.addControl(new L.Control.Fullscreen({
    title: {
        'false': 'View Fullscreen',
        'true': 'Exit Fullscreen'
    }
}));


