function select(svg, geojson) {
    var bbox = [geojson.bbox[0], geojson.bbox[1], geojson.bbox[2]-geojson.bbox[0], geojson.bbox[3]-geojson.bbox[1]];

    var width = svg.getBoundingClientRect().width;
    var height = svg.getBoundingClientRect().height;

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


    var blocks = {};

    var once = false;

    var path = [];
    var svgbox = svg.getBoundingClientRect();
    var pathdraw = svg.lastChild;
    function record(event) {
        var coordinate = [event.clientX - svgbox.left, event.clientY - svgbox.top];
        path.push(coordinate);
        pathdraw.setAttribute("d", pathdraw.getAttribute("d") + " L " + coordinate[0] + ", " + coordinate[1]);
    }


    svg.addEventListener("click", function(event) {
        if (event.target.tagName.toLowerCase() == "path") {
            if (event.target.getAttribute("id") in blocks) {
                event.target.style.fill = "";
                delete blocks[event.target.getAttribute("id")];
            }
            else {
                event.target.style.fill = "blue";
                blocks[event.target.getAttribute("id")] = true;
            }
        }
    }, false);

    svg.addEventListener("mousedown", function(event) {
        event.preventDefault();
        var coordinate = [event.clientX - svgbox.left, event.clientY - svgbox.top]

        if (once)
            return false;

        path = [];
        path.push(coordinate);
        pathdraw.setAttribute("d", "M " + coordinate[0] + ", " + coordinate[1]);
        svg.addEventListener("mousemove", record, false);
    }, false);
    svg.addEventListener("mouseup", function(event) {
        if (once)
            return;
        once = true;
        svg.removeEventListener("mousemove", record, false);
        if (path.length > 1) {
            event.preventDefault();
            pathdraw.setAttribute("d", "M " + path.join(" L ") + " Z");
            path.push(path[0]);

            // let's try to find nearby shapes
            // first, convert to lat/long and find bbox
            var temp = path.map(unmap);
            var pathbox = {
                xmin: temp[0][0],
                xmax: temp[0][0],
                ymin: temp[0][1],
                ymax: temp[0][1]
            };
            for (var i = 1; i < temp.length; i++) {
                pathbox.xmin = Math.min(pathbox.xmin, temp[i][0]);
                pathbox.xmax = Math.max(pathbox.xmax, temp[i][0]);
                pathbox.ymin = Math.min(pathbox.ymin, temp[i][1]);
                pathbox.ymax = Math.max(pathbox.ymax, temp[i][1]);
            }

            var intersection = [];
            for (var i = 0; i < geojson.features.length; i++) {
                var shapebox = geojson.features[i].bbox; // xmin, ymin, xmax, ymax
                if (!(shapebox[2] < pathbox.xmin || pathbox.xmax < shapebox[0] || shapebox[3] < pathbox.ymin || pathbox.ymax < shapebox[1])) {
                    if (polygonInPolygon(geojson.features[i].geometry.coordinates[0], temp)) {
                        svg.childNodes[i+1].style.fill = "blue";
                        blocks[svg.childNodes[i+1].getAttribute("id")] = true;
                    }
                }
            }


            path = [];
        }
    }, false);

    return blocks;
}
