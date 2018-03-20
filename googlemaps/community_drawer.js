/* Our project hopes to use the familiar googple maps api to allow users, likely people tied to drawing district lines, to visualize communities of interest 
Author: Lillian Geerts,
*/

// @Source https://developers.google.com/maps/documentation/javascript/earthquakes
// grabbed a basic google maps api tutorial map and edited


var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 5,
    center: new google.maps.LatLng(35, -79),
    mapTypeId: 'roadmap'
//    mapTypeId: 'satellite'
  });
  var coords = [];
   var poly = new google.maps.Polyline({
    strokeColor: '#000000',
    strokeOpacity: 1,
    strokeWeight: 3,
  //  draggable: true,
    map: map
  });
// console.log(poly.pathArr.getAt(1).lat());
  //coords.push(poly.get());
  //console.log("hello world!");
  //console.log(coords); 

  
  
  var drawingManager = new google.maps.drawing.DrawingManager({
          drawingMode: google.maps.drawing.OverlayType.MARKER,
          drawingControl: true,
          drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['marker', 'circle', 'polygon', 'polyline', 'rectangle']
          },
          markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'},
          circleOptions: {
            fillColor: '#ffff00',
            fillOpacity: 1,
            strokeWeight: 5,
            clickable: true,
            editable: true,
            zIndex: 1
          }
          
          
        });
        drawingManager.setMap(map);
/*   var coords = new google.maps.event.addListener(drawingManager, 'polylinecomplete', function(poly) {
  alert(poly.getPath().getArray().toString());
  console.log(line.getPath().getArray().toString());
  }); 
  console.log("hi hello");
  console.log(coords); */
  
google.maps.event.addListener(map, 'click', getPathVariableCode);
  
 // LoadStates();
 // map.setTilt(45);

  // Create a <script> tag and set the USGS URL as the source.
  var script = document.createElement('script');
  // This example uses a local copy of the GeoJSON stored at
  // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
  script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
  document.getElementsByTagName('head')[0].appendChild(script);
  LoadStates();
}



  
//draws the polygons for all states and adds them to the map with the attached click functions 


/* @Source
http://jmcconahie.com/Software/Scripts/GoogleMap.js
Outlining state lines more clearly than google maps allows
*/

var invisColor = "#000000";
var outlineColor = "#0ABA02";   //green
//var map = null;
var currentState = "";

//jquery animation function
//Note: comment out the contents of this function if you do not want to use jquery with the map
/*  function extend() {
    $('.dropbox').animate({ height: '25' }, 100);
    $('.dropbox').css('padding-top', '5px');
 }  */

//draws the polygons for all states and adds them to the map with the attached click functions 
function LoadStates()
{
  
  //North Carolina (TODO: Need better coastal border)
    points = [  
        new google.maps.LatLng(36.55 ,-75.929),      //top right
        new google.maps.LatLng(36.55 ,-75.966),
        new google.maps.LatLng(36.55 ,-75.884),
        new google.maps.LatLng(36.55 ,-75.894),
        new google.maps.LatLng(36.55 ,-75.988),
        new google.maps.LatLng(36.55 ,-76.006),
        new google.maps.LatLng(36.55 ,-76.035),
        new google.maps.LatLng(36.55 ,-76.156),
        new google.maps.LatLng(36.55 ,-76.161),
        new google.maps.LatLng(36.542 ,-78.917),
        new google.maps.LatLng(36.542 ,-79.138),
        new google.maps.LatLng(36.588 ,-81.677),     //top left
        new google.maps.LatLng(36.338 ,-81.706),
        new google.maps.LatLng(36.301 ,-81.908),
        new google.maps.LatLng(36.12 ,-82.033),
        new google.maps.LatLng(36.116 ,-82.354),
        new google.maps.LatLng(35.955 ,-82.561),
        new google.maps.LatLng(36.065 ,-82.638),
        new google.maps.LatLng(35.944 ,-82.898),
        new google.maps.LatLng(35.773 ,-82.993),
        new google.maps.LatLng(35.562 ,-83.499),
        new google.maps.LatLng(35.518 ,-83.881),
        new google.maps.LatLng(35.274 ,-84.046),
        new google.maps.LatLng(35.225 ,-84.29),
        new google.maps.LatLng(34.988 ,-84.322),      //left side of GA border
        new google.maps.LatLng(35 ,-83.108),
        new google.maps.LatLng(35.215 ,-82.394),
        new google.maps.LatLng(35.149 ,-81.032),
        new google.maps.LatLng(35.047 ,-81.043),
        new google.maps.LatLng(35.107 ,-80.935),
        new google.maps.LatLng(34.935 ,-80.782),
        new google.maps.LatLng(34.819 ,-80.797),
        new google.maps.LatLng(34.804 ,-79.675),
        new google.maps.LatLng(33.856 ,-78.556),      //bottom right
        new google.maps.LatLng(33.838483,-77.961731),
        new google.maps.LatLng(34.482788,-77.433701), 
        new google.maps.LatLng(34.580083,-76.533508),
        new google.maps.LatLng(35.218697,-75.52002),
        new google.maps.LatLng(35.588085,-75.451355),
        new google.maps.LatLng(35.721988,-75.484314)
    ];
    
     // Construct the polygon
  var Northcarolina = new google.maps.Polygon({
    paths: points,
    strokeColor: outlineColor,
    strokeOpacity: 0,
    strokeWeight: 2,
    fillColor: invisColor,
    fillOpacity: 0
  });
  
  //add event listeners to polygon, then add polygon to map
  google.maps.event.addListener(Northcarolina, 'mouseover',  function() { Northcarolina.setOptions({strokeOpacity: 1}); });
  google.maps.event.addListener(Northcarolina, 'mouseout', function() { Northcarolina.setOptions({strokeOpacity: 0}); });
  google.maps.event.addListener(Northcarolina, 'click', function() {   
  document.getElementById("StateName").innerHTML = "North Carolina"; extend(); });
  Northcarolina.setMap(map);
  };
  // end source code with modifications
  
function getPathVariableCode(poly){
  var codeStr = '  var linePath = [\n';
  var pathArr = poly.getPath();
  console.log("sup bitch");
  for (var i = 0; i < pathArr.length; i++){
      codeStr += '    {lat: ' + pathArr.getAt(i).lat() + ', lng: ' + pathArr.getAt(i).lng() + '}' ;
      if (i !== pathArr.length-1) {
          codeStr += ',\n';
      };
  };

  codeStr += '\n  ];';

//the coordinates path it´s print on the console of the browser

  console.log (codeStr);
  console.log(pathArr.length);

};
  
  