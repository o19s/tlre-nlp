var map = L.map('map').setView([0, 0], 1);


var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
}).addTo(map);

function onEachFeature(feature, layer) {
  var count = feature.properties.count.toLocaleString();
  layer.bindPopup(count);
}


// Create and add a solrHeatmap layer to the map
var solr = L.solrHeatmap('http://127.0.0.1:8983/solr/tmdb', {
  // Solr field with geospatial data (should be type Spatial Recursive Prefix Tree)
  field: 'location_rpt',

  // Set type of visualization. Allowed types: 'geojsonGrid', 'clusters' Note: 'clusters' requires LeafletMarkerClusterer
  type: 'geojsonGrid',
  //type: 'heatmap',

  // Inherited from L.GeoJSON
  onEachFeature: onEachFeature
}).addTo(map);

solr.on('dataAdded', function(data) {
  $('#responseTime').html('Solr response time: ' + solr.responseTime + ' ms');
  var docsCount = solr.count;
  $('#numDocs').html('Number of docs: ' + docsCount.toLocaleString());
  $('#renderTime').html('Render time: ' + solr.renderTime + ' ms');
});


// An example of requestNearby in use with Leaflet click handlers
map.on('click', function (e) {
  solr.requestNearby(e.layerPoint);
});
solr.on('click', function (e) {
  solr.requestNearby(e.layerPoint);
});

solr.on('nearbyQueried', function(data) {
  var rect = L.rectangle(data.bounds);
  $('#pointQuery').html('Query returned: ' + data.response.numFound + ' results')
  rect.on('add', function() {
    setTimeout(function() {
      rect.removeFrom(map);
    }, 500)
  })  
  rect.addTo(map);
});


//http://127.0.0.1:8983/solr/tmdb/select?location_rpt&json.wrf=jQuery33107168202815042635_1546539949092&q=*%3A*&wt=json&facet=true&facet.heatmap=location_rpt&facet.heatmap.geom=%5B"-180%20-90"%20TO%20"180%2090"%5D&fq=location_rpt%3A"Intersects(ENVELOPE(-180%2C%20180%2C%2090%2C%20-90))"&_=1546539949093