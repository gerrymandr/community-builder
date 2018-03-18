"use strict";

function draw(geojson) {
    var svg = document.getElementById("draw");

    var bbox = [-81.045519866325, 35.104691487287496, -80.631147176075 + 81.045519866325, 35.3619157324125 - 35.104691487287496];

        //[-81.045519866325, 35.104691487287496, -80.631147176075, 35.3619157324125];
//    var bbox = [geojson.bbox[0], geojson.bbox[1], geojson.bbox[2]-geojson.bbox[0], geojson.bbox[3]-geojson.bbox[1]];
    var width = svg.getBoundingClientRect().width;
    var height = width * bbox[3] / bbox[2];

    svg.style.height = height + "px";
    var img = svg.getElementsByTagName("image")[0];
    img.setAttribute("height", height);
    img.style.display = "";




    var dx = width / bbox[2];
    var dy = height / bbox[3];
    var y1 = bbox[1] + bbox[3];
    // (lat,long) -> (x,y)
    function remap(coor) {
        return [
            (coor[0] - bbox[0]) * dx,
            (y1 - coor[1]) * dy
        ]
    }
    // (x,y) -> (lat,long)
    function unmap(coor) {
        return [
            coor[0] / dx + bbox[0],
            y1 - coor[1] / dy
        ];
    }


    var paths = document.createDocumentFragment();
    for (var i = 0; i < geojson.features.length; i++) {
        var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", "M " + geojson.features[i].geometry.coordinates[0].map(remap).join(" L ") + " Z");
        path.setAttribute("id", geojson.features[i].properties.id);
        paths.appendChild(path);
    }
    svg.insertBefore(paths,svg.lastChild);
}

