// ported from https://stackoverflow.com/a/2922778/4621930
function pointInPolygon(x, v) {
    var c = false;
    for (var i = 0, j = v.length-1; i < v.length; j = i++) {
        if (
            ((v[i][1] > x[1]) != (v[j][1] > x[1])) &&
            (x[0] < (v[j][0]-v[i][0]) * (x[1]-v[i][1]) / (v[j][1]-v[i][1]) + v[i][0])
        ) {
           c = !c;
        }
  }
  return c;
}

// does v0 intersect with v1?
// first pass: all vertices inside v1
function polygonInPolygon(v0,v1) {
    for (var i = 0; i < v0.length; i++) {
        if (pointInPolygon(v0[i], v1)) {
            return true;
        }
    }
    return false;
}

